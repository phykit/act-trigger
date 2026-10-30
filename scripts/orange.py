"""Project Orange: decision-day reaction and post-decision drift.

Runs the test registered in prereg/orange_prereg.md on the cases in data/ruling_cases.csv
and writes results/orange_result_<date>.md. Usage: python scripts/orange.py
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rulings_common import (ROOT, SELFTEST, check_dates, check_dates_scdb, fetch_close, fmt_pct,  # noqa: E402
                            load_cases, log, market_close, market_model, market_source, opinion_days,
                            result_path, spec_hash)

P_THRESH = 0.10
REACT_Z = 2.0
MIN_REACTING = 3
DRIFT_DAYS = 5
SECONDARY = {"ORCL_18-956": "GOOGL"}  # secondary legs reported, outside the decision rule


def event_stats(ar: pd.DataFrame, sigma: float, decided: dt.date) -> dict | None:
    idx = ar.index
    pos = idx.searchsorted(pd.Timestamp(decided))
    if pos >= len(idx) or idx[pos].date() != decided:
        return None
    if pos + DRIFT_DAYS >= len(idx) or pos - 5 < 0:
        return None
    ar0 = float(ar["ar"].iloc[pos])
    car1 = float(ar["ar"].iloc[pos + 1])
    car15 = float(ar["ar"].iloc[pos + 1: pos + 1 + DRIFT_DAYS].sum())
    pre = float(ar["ar"].iloc[pos - 5: pos].sum())
    sgn = 1.0 if ar0 >= 0 else -1.0
    return dict(ar0=ar0, z0=ar0 / sigma, car1=car1, car15=car15, pre=pre,
                signed1=sgn * car1, signed15=sgn * car15,
                z_drift=sgn * car15 / (sigma * np.sqrt(DRIFT_DAYS)),
                z_pre=pre / (sigma * np.sqrt(5)), day0=idx[pos].date())


def main() -> None:
    spec = sys.argv[sys.argv.index("--spec") + 1] if "--spec" in sys.argv else "orange"
    if spec not in ("orange", "orange_v2"):
        raise SystemExit("--spec must be orange or orange_v2")
    wide = spec == "orange_v2"
    register = ROOT / "data" / ("ruling_cases_wide.csv" if wide else "ruling_cases.csv")
    cases = load_cases(register)
    min_react = 15 if wide else MIN_REACTING
    h = spec_hash(spec)
    rows, secondary, notes = [], [], []
    for _, c in cases.iterrows():
        term = int(c["term"])
        if wide:
            chk = check_dates_scdb(c)
        else:
            try:
                _, slip = opinion_days(term)
            except Exception as exc:  # noqa: BLE001
                slip = pd.DataFrame(columns=["date", "docket", "name"])
                notes.append(f"{c['case_id']}: slip listing for OT{term:02d} unavailable ({exc}); decision date checked against Oyez only")
            chk = check_dates(c, slip)
        if not chk["include"]:
            notes.append(f"{c['case_id']}: {chk['decided_status']}; case excluded")
            continue
        argued, decided = chk["argued"], chk["decided"]
        start = argued - dt.timedelta(days=800)
        end = decided + dt.timedelta(days=15)
        legs = [(c["ticker"], True)]
        if not wide and c["case_id"] in SECONDARY:
            legs.append((SECONDARY[c["case_id"]], False))
        for ticker, primary in legs:
            try:
                stock, src_s = fetch_close(ticker, start, end)
                if wide:
                    mkt, src_m = market_close(c["market_proxy"]), market_source(c["market_proxy"])
                else:
                    mkt, src_m = fetch_close(c["market_proxy"], start, end)
                ar, mm = market_model(stock, mkt, argued)
            except Exception as exc:  # noqa: BLE001
                notes.append(f"{c['case_id']} {ticker}: price data or market model failed ({str(exc)[:120]}); leg skipped")
                continue
            ev = event_stats(ar, mm["sigma"], decided)
            if ev is None:
                notes.append(f"{c['case_id']} {ticker}: no trading-day return on {decided} or too few days after it; leg skipped")
                continue
            rec = dict(case=c["case_name"], ticker=ticker, decided=decided, **ev, sigma=mm["sigma"], beta=mm["beta"],
                       reacted=abs(ev["z0"]) >= REACT_Z, argued_status=chk["argued_status"],
                       decided_status=chk["decided_status"], source=f"{ticker}: {src_s}; {c['market_proxy']}: {src_m}")
            (rows if primary else secondary).append(rec)
            log(f"{c['case_id']} {ticker}: AR0 {100 * ev['ar0']:+.2f}% (z {ev['z0']:+.2f}), CAR(+1,+5) {100 * ev['car15']:+.2f}%")

    react = [r for r in rows if r["reacted"]]
    n_react = len(react)
    mean_signed15 = float(np.mean([r["signed15"] for r in react])) if react else float("nan")
    mean_signed1 = float(np.mean([r["signed1"] for r in react])) if react else float("nan")
    Z = float(np.sum([r["z_drift"] for r in react]) / np.sqrt(n_react)) if react else float("nan")
    p = float(1 - norm.cdf(Z)) if react else float("nan")
    cont = sum(1 for r in react if r["signed15"] > 0)

    if n_react < min_react:
        outcome = "UNSCORABLE"
    elif mean_signed15 > 0 and p < P_THRESH:
        outcome = "SUPPORT"
    elif mean_signed15 <= 0:
        outcome = "KILL"
    else:
        outcome = "INCONCLUSIVE"

    today = dt.date.today().isoformat()
    L = []
    L.append(f"# Result: Project Orange{' v2 (wide sample)' if wide else ''} (decision-day reaction and post-decision drift)\n")
    L.append(f"Run {today} against {spec}_prereg.md, SHA-256 {h} (hashed before the run). "
             "Non-evidentiary: daily data, one parameter set, no costs.\n")
    if SELFTEST:
        L.append("**SELF-TEST RUN ON SYNTHETIC DATA. Not a result.**\n")
    L.append("## Population\n")
    L.append(f"- {len(rows)} primary legs entered ({len(cases)} registered, register {register.name}); {n_react} reacted (abs(z_0) at or above {REACT_Z:.0f}), a reaction rate of {100 * n_react / max(len(rows), 1):.0f}% against the 37% Katz et al report on screened candidates.\n")
    L.append("## Outcomes (reacting cases)\n")
    L.append("| Statistic | Value |")
    L.append("|---|---|")
    L.append(f"| Reacting cases | {n_react} of {len(rows)} |")
    L.append(f"| Mean signed CAR(+1,+1) | {fmt_pct(mean_signed1)} |")
    L.append(f"| Mean signed CAR(+1,+5) | {fmt_pct(mean_signed15)} |")
    L.append(f"| Cases continuing over +1 to +5 | {cont} of {n_react} |")
    L.append(f"| Stouffer Z, one-sided p | {Z:.2f}, {p:.3f} |\n")
    L.append("## Decision rule as registered\n")
    L.append(f"- Mean signed CAR(+1,+5) above zero: {'met' if np.isfinite(mean_signed15) and mean_signed15 > 0 else 'not met'} ({fmt_pct(mean_signed15)}).")
    L.append(f"- Stouffer p below {P_THRESH}: {'met' if np.isfinite(p) and p < P_THRESH else 'not met'} (p = {p:.3f}).")
    L.append(f"- At least {min_react} reacting cases: {'met' if n_react >= min_react else 'not met'} ({n_react}).\n")
    L.append(f"Registered outcome: {outcome}.\n")
    L.append("## What this does not license\n")
    L.append("- The reaction rate depends on the register rule and the abs(z) threshold; it is not Katz et al's screened population." if wide else "- Cases chosen for salience: the day-0 reactions are large by construction and say nothing about the population rate Katz et al report (37% of candidates).")
    L.append("- Daily frequency: CAR(+1,+1) mixes the overnight gap with the next session.")
    L.append("- No costs, no hedging of the day-0 position.\n")
    L.append("## Cases\n")
    L.append("| Case | Ticker | Decided | AR(0) | z(0) | Reacted | CAR(-5,-1) | CAR(+1,+1) | CAR(+1,+5) | Signed CAR(+1,+5) | z drift | Sigma (daily) | Beta | Date checks | Price source |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows + secondary:
        tag = "" if r in rows else " (secondary leg)"
        L.append(f"| {r['case']}{tag} | {r['ticker']} | {r['decided']} | {fmt_pct(r['ar0'])} | {r['z0']:+.2f} | "
                 f"{'yes' if r['reacted'] else 'no'} | {fmt_pct(r['pre'])} | {fmt_pct(r['car1'])} | {fmt_pct(r['car15'])} | "
                 f"{fmt_pct(r['signed15'])} | {r['z_drift']:+.2f} | {100 * r['sigma']:.2f}% | {r['beta']:.2f} | "
                 f"argued {r['argued_status']}; decided {r['decided_status']} | {r['source']} |")
    L.append("")
    L.append("## Run notes\n")
    L.extend([f"- {n}" for n in notes] or ["- None."])
    out = result_path(spec)
    out.write_text("\n".join(L) + "\n")
    log(f"wrote {out}; outcome {outcome}; mean signed CAR(+1,+5) {fmt_pct(mean_signed15)} p={p:.3f}")


if __name__ == "__main__":
    main()
