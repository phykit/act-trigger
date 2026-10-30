"""Project Apple: timing hazard in the argument-to-decision window.

Runs the test registered in prereg/apple_prereg.md on the cases in data/ruling_cases.csv
and writes results/apple_result_<date>.md. Usage: python scripts/apple.py
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rulings_common import (SELFTEST, check_dates, fetch_close, fmt_pct, load_cases, log,  # noqa: E402
                            market_model, opinion_days, result_path, scdb_opinion_days, spec_hash)

PERMS = 10_000
SEED = 20261029
P_THRESH = 0.10
MIN_OPINION_DAYS = 15
MIN_CASES = 4
PLACEBO_SHIFT = 364  # days; preserves weekday


def arm(ar: pd.DataFrame, argued: dt.date, decided: dt.date, op_dates: set[dt.date], shift: int) -> pd.DataFrame:
    """Days strictly inside (argued, decided) shifted back by `shift` days, labelled by shifted opinion days."""
    lo = pd.Timestamp(argued) - pd.Timedelta(days=shift)
    hi = pd.Timestamp(decided) - pd.Timedelta(days=shift)
    sub = ar[(ar.index > lo) & (ar.index < hi)].copy()
    sub["is_op"] = [(t + pd.Timedelta(days=shift)).date() in op_dates for t in sub.index]
    sub["z2"] = sub["z"] ** 2
    return sub[["ar", "z", "z2", "is_op"]]


def pooled_ratio(groups: list[tuple[np.ndarray, np.ndarray]]) -> float:
    op = np.concatenate([z2[m] for z2, m in groups])
    non = np.concatenate([z2[~m] for z2, m in groups])
    if len(op) == 0 or len(non) == 0:
        return float("nan")
    return float(op.mean() / non.mean())


def permutation_p(groups: list[tuple[np.ndarray, np.ndarray]], observed: float) -> float:
    rng = np.random.default_rng(SEED)
    tot_op = sum(int(m.sum()) for _, m in groups)
    tot_non = sum(int((~m).sum()) for _, m in groups)
    totals = [float(z2.sum()) for z2, _ in groups]
    ks = [int(m.sum()) for _, m in groups]
    count = 0
    for _ in range(PERMS):
        s_op = 0.0
        for (z2, _), k in zip(groups, ks):
            if k:
                s_op += z2[rng.permutation(len(z2))[:k]].sum()
        s_non = sum(totals) - s_op
        r = (s_op / tot_op) / (s_non / tot_non)
        if r >= observed:
            count += 1
    return count / PERMS


def main() -> None:
    spec = sys.argv[sys.argv.index("--spec") + 1] if "--spec" in sys.argv else "apple"
    if spec not in ("apple", "apple_v2"):
        raise SystemExit("--spec must be apple or apple_v2")
    use_scdb = spec == "apple_v2"
    cases = load_cases()
    h = spec_hash(spec)
    rows, groups, placebo_groups, notes = [], [], [], []
    scdb_ver = "n/a"
    for _, c in cases.iterrows():
        term = int(c["term"])
        try:
            if use_scdb:
                op_days, listing, scdb_ver = scdb_opinion_days(term)
                listing_name = f"SCDB {scdb_ver}"
            else:
                op_days, listing = opinion_days(term)
                listing_name = "slip listing"
        except Exception as exc:  # noqa: BLE001
            notes.append(f"{c['case_id']}: opinion-day source for OT{term:02d} unavailable ({exc}); case excluded")
            continue
        chk = check_dates(c, listing, listing_name)
        if not chk["include"]:
            notes.append(f"{c['case_id']}: decision date check {chk['decided_status']}; case excluded")
            continue
        argued, decided = chk["argued"], chk["decided"]
        start = argued - dt.timedelta(days=800)
        end = decided + dt.timedelta(days=15)
        stock, src_s = fetch_close(c["ticker"], start, end)
        mkt, src_m = fetch_close(c["market_proxy"], start, end)
        ar, mm = market_model(stock, mkt, argued)
        op_set = set(op_days)
        if use_scdb:
            try:
                slip_days, _ = opinion_days(term)
                in_w = lambda d: argued < d < decided  # noqa: E731
                s_in = {d for d in slip_days if in_w(d)}
                o_in = {d for d in op_set if in_w(d)}
                notes.append(f"{c['case_id']}: cross-check inside W, SCDB {len(o_in)} opinion days, slip listing {len(s_in)}; "
                             f"in SCDB only {sorted(o_in - s_in)}; in slip listing only {sorted(s_in - o_in)}")
            except Exception as exc:  # noqa: BLE001
                notes.append(f"{c['case_id']}: slip listing for OT{term:02d} not available for cross-check ({str(exc)[:80]})")
        live = arm(ar, argued, decided, op_set, 0)
        plac = arm(ar, argued, decided, op_set, PLACEBO_SHIFT)
        for name, a in (("live", live), ("placebo", plac)):
            if a["is_op"].sum() == 0 or (~a["is_op"]).sum() == 0:
                notes.append(f"{c['case_id']}: {name} arm has no opinion or no non-opinion days; arm skipped")
        if live["is_op"].sum() and (~live["is_op"]).sum():
            groups.append((live["z2"].values, live["is_op"].values))
        if plac["is_op"].sum() and (~plac["is_op"]).sum():
            placebo_groups.append((plac["z2"].values, plac["is_op"].values))

        def ratio(a: pd.DataFrame) -> float:
            if a["is_op"].sum() == 0 or (~a["is_op"]).sum() == 0:
                return float("nan")
            return float(a.loc[a["is_op"], "z2"].mean() / a.loc[~a["is_op"], "z2"].mean())

        rows.append(dict(
            case=c["case_name"], ticker=c["ticker"], argued=argued, decided=decided,
            days=len(live), op=int(live["is_op"].sum()),
            z2_op=float(live.loc[live["is_op"], "z2"].mean()) if live["is_op"].sum() else float("nan"),
            z2_non=float(live.loc[~live["is_op"], "z2"].mean()) if (~live["is_op"]).sum() else float("nan"),
            ratio=ratio(live), placebo_ratio=ratio(plac), placebo_days=len(plac),
            big_op=float((live.loc[live["is_op"], "z"].abs() > 1).mean()) if live["is_op"].sum() else float("nan"),
            big_non=float((live.loc[~live["is_op"], "z"].abs() > 1).mean()) if (~live["is_op"]).sum() else float("nan"),
            sigma=mm["sigma"], beta=mm["beta"], est=f"{mm['est_start']} to {mm['est_end']}",
            argued_status=chk["argued_status"], decided_status=chk["decided_status"],
            source=f"{c['ticker']}: {src_s}; {c['market_proxy']}: {src_m}",
        ))
        log(f"{c['case_id']}: {len(live)} days, {int(live['is_op'].sum())} opinion days, ratio {ratio(live):.3f}")

    n_cases = len(groups)
    tot_op = sum(int(m.sum()) for _, m in groups)
    tot_non = sum(int((~m).sum()) for _, m in groups)
    R = pooled_ratio(groups) if groups else float("nan")
    p = permutation_p(groups, R) if groups else float("nan")
    Rp = pooled_ratio(placebo_groups) if placebo_groups else float("nan")
    pp = permutation_p(placebo_groups, Rp) if placebo_groups else float("nan")
    big_op = float(np.mean(np.concatenate([np.abs(np.sqrt(z2[m])) > 1 for z2, m in groups]))) if groups else float("nan")
    big_non = float(np.mean(np.concatenate([np.abs(np.sqrt(z2[~m])) > 1 for z2, m in groups]))) if groups else float("nan")

    if n_cases < MIN_CASES or tot_op < MIN_OPINION_DAYS:
        outcome = "UNSCORABLE"
    elif np.isfinite(R) and R > 1 and p < P_THRESH and (not np.isfinite(Rp) or R > Rp):
        outcome = "SUPPORT"
    elif np.isfinite(R) and R <= 1:
        outcome = "KILL"
    else:
        outcome = "INCONCLUSIVE"

    today = dt.date.today().isoformat()
    L = []
    L.append(f"# Result: Project Apple{' v2' if use_scdb else ''} (timing hazard in the argument-to-decision window)\n")
    L.append(f"Run {today} against {spec}_prereg.md, SHA-256 {h} (hashed before the run). "
             "Non-evidentiary: five cases, daily data, one parameter set, no costs.\n")
    if SELFTEST:
        L.append("**SELF-TEST RUN ON SYNTHETIC DATA. Not a result.**\n")
    L.append("## Population\n")
    L.append(f"- {n_cases} cases entered the live arm ({len(cases)} registered); {tot_op} pooled non-decision opinion days "
             f"against {tot_non} non-opinion days inside the argument-to-decision windows.")
    L.append(f"- Placebo arm: {len(placebo_groups)} cases, windows shifted back {PLACEBO_SHIFT} days.\n")
    L.append("## Outcomes\n")
    L.append("| Arm | Cases | Opinion days | Non-opinion days | Mean z^2 ratio R | Permutation p (one-sided) | Share of days with abs(z) > 1, opinion vs non-opinion |")
    L.append("|---|---|---|---|---|---|---|")
    L.append(f"| Live | {n_cases} | {tot_op} | {tot_non} | {R:.3f} | {p:.3f} | {100 * big_op:.0f}% vs {100 * big_non:.0f}% |")
    L.append(f"| Placebo (same ticker, one year earlier) | {len(placebo_groups)} | "
             f"{sum(int(m.sum()) for _, m in placebo_groups)} | {sum(int((~m).sum()) for _, m in placebo_groups)} | "
             f"{Rp:.3f} | {pp:.3f} | n/a |\n")
    L.append("## Decision rule as registered\n")
    L.append(f"- R above 1: {'met' if np.isfinite(R) and R > 1 else 'not met'} (R = {R:.3f}).")
    L.append(f"- Permutation p below {P_THRESH}: {'met' if np.isfinite(p) and p < P_THRESH else 'not met'} (p = {p:.3f}).")
    L.append(f"- R above the placebo R: {'met' if np.isfinite(Rp) and R > Rp else ('not met' if np.isfinite(Rp) else 'n/a, no placebo')} (placebo R = {Rp:.3f}).")
    L.append(f"- At least {MIN_CASES} cases and {MIN_OPINION_DAYS} pooled opinion days: "
             f"{'met' if n_cases >= MIN_CASES and tot_op >= MIN_OPINION_DAYS else 'not met'} ({n_cases} cases, {tot_op} opinion days).\n")
    L.append(f"Registered outcome: {outcome}.\n")
    L.append("## What this does not license\n")
    L.append("- Five cases and daily closes. The test bounds the answer; it does not establish it.")
    L.append("- Opinion days are the realised release dates, not the calendar as known at the start of each window." + (f" Source: SCDB release {scdb_ver}, all decision types." if use_scdb else " Source: supremecourt.gov slip-opinion listing, which is retired progressively once bound volumes publish."))
    L.append("- The placebo controls weekday composition and the ticker's own variance, not other calendar events in the live window (June FOMC, index rebalances).")
    L.append("- Standardisation by the pre-argument residual sigma weights cases unequally where volatility regimes changed between estimation and window.\n")
    L.append("## Cases\n")
    L.append("| Case | Ticker | Argued | Decided | Days in W | Opinion days | Mean z^2 opinion | Mean z^2 non-opinion | Ratio | Placebo ratio | abs(z) > 1 opinion vs non | Sigma (daily) | Beta | Date checks | Price source |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        L.append(f"| {r['case']} | {r['ticker']} | {r['argued']} | {r['decided']} | {r['days']} | {r['op']} | "
                 f"{r['z2_op']:.2f} | {r['z2_non']:.2f} | {r['ratio']:.3f} | {r['placebo_ratio']:.3f} | "
                 f"{100 * r['big_op']:.0f}% vs {100 * r['big_non']:.0f}% | {100 * r['sigma']:.2f}% | {r['beta']:.2f} | "
                 f"argued {r['argued_status']}; decided {r['decided_status']} | {r['source']} |")
    L.append("")
    L.append("## Run notes\n")
    L.extend([f"- {n}" for n in notes] or ["- None."])
    L.append(f"- Permutations: {PERMS}, seed {SEED}. Estimation window: {rows[0]['est'] if rows else 'n/a'} for the first case; 250 trading days ending 10 trading days before argument for each.")
    out = result_path(spec)
    out.write_text("\n".join(L) + "\n")
    log(f"wrote {out}; outcome {outcome}; R={R:.3f} p={p:.3f} placebo R={Rp:.3f}")


if __name__ == "__main__":
    main()
