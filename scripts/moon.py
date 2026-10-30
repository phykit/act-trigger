"""Project Moon: propagation of a Supreme Court ruling to the listed parent of a subsidiary party (prereg/moon_prereg.md).

Usage: python scripts/moon.py
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appeals_common import (SELFTEST, bootstrap_mean_p, build_party_map, build_universe, compute_events,  # noqa: E402
                            earnings_dates, log, near_earnings, result_path, spec_hash)

MIN_EVENTS = 25
P_THRESH = 0.05
SEED = 20261030


def fmt(x: float) -> str:
    return "n/a" if x is None or not np.isfinite(x) else f"{100 * x:+.2f}%"


def direction(row: pd.Series) -> float:
    pw = row.get("party_winning")
    if pw not in (0, 1, 0.0, 1.0):
        return float("nan")
    won = (row["side"] == "petitioner" and pw == 1) or (row["side"] == "respondent" and pw == 0)
    return 1.0 if won else -1.0


def two_sample_p(a: np.ndarray, b: np.ndarray, draws: int = 10_000) -> float:
    """One-sided bootstrap p for mean(a) < mean(b) (Moon reactions smaller than direct reactions)."""
    rng = np.random.default_rng(SEED)
    a, b = a[np.isfinite(a)], b[np.isfinite(b)]
    if len(a) == 0 or len(b) == 0:
        return float("nan")
    da = rng.choice(a, size=(draws, len(a)), replace=True).mean(axis=1)
    db = rng.choice(b, size=(draws, len(b)), replace=True).mean(axis=1)
    return float(np.mean(da - db >= 0))


def main() -> None:
    h = spec_hash("moon")
    uni, unote = build_universe()
    pm = build_party_map(uni)
    sc = uni[uni["court"] == "scotus"]
    pm_sc = pm[pm["ruling"].astype(int).isin(sc.index)]
    ev_par, ars, px = compute_events(uni, pm_sc, ("ex21 parent",), "parents", post=5)
    ev_dir, _, _ = compute_events(uni, pm_sc, ("listed",), "litigants", post=5)
    for df in (ev_par, ev_dir):
        if len(df) and "status" in df.columns:
            df["dir"] = df.apply(direction, axis=1) if "party_winning" in df.columns else np.nan
    moon = ev_par[(ev_par["status"] == "ok") & ev_par["dir"].notna()].copy() if len(ev_par) else pd.DataFrame()
    direct = ev_dir[(ev_dir["status"] == "ok") & ev_dir["dir"].notna()].copy() if len(ev_dir) else pd.DataFrame()
    if len(moon):
        moon["S0"] = moon["dir"] * moon["ar0"]
        moon["S"] = moon["dir"] * moon["car_post"]
    n = len(moon)
    mean_S = float(moon["S"].mean()) if n else float("nan")
    p_S = bootstrap_mean_p(moon["S"].values) if n else float("nan")
    mean_S0 = float(moon["S0"].mean()) if n else float("nan")
    p_S0 = bootstrap_mean_p(moon["S0"].values) if n else float("nan")
    absz_moon = float(moon["z0"].abs().mean()) if n else float("nan")
    absz_dir = float(direct["z0"].abs().mean()) if len(direct) else float("nan")
    p_absz = two_sample_p(moon["z0"].abs().values, direct["z0"].abs().values) if n and len(direct) else float("nan")

    # placebo: random dates for the same parents, random direction
    rng = np.random.default_rng(SEED)
    plac = []
    if n:
        ruling_dates = {}
        for _, r in pm.dropna(subset=["ticker"]).iterrows():
            ruling_dates.setdefault(str(r["ticker"]), set()).add(pd.Timestamp(uni.loc[int(r["ruling"]), "date"]))
        for _, r in moon.iterrows():
            t = r["ticker"]
            ar = ars.get(t)
            if ar is None:
                continue
            ed = earnings_dates(str(r["cik"])) if not SELFTEST else set()
            yr = pd.Timestamp(r["date"]).year
            cand = ar.index[(ar.index.year == yr)]
            cand = [c for c in cand if all(abs((c - d).days) > 15 for d in ruling_dates.get(t, set())) and not near_earnings(c.date(), ed)]
            if len(cand) < 10:
                continue
            for c in rng.choice(cand, size=5, replace=False):
                pos = ar.index.get_loc(c)
                if pos + 6 >= len(ar):
                    continue
                plac.append(rng.choice([-1.0, 1.0]) * float(ar["ar"].values[pos + 1: pos + 6].sum()))
    mean_plac = float(np.mean(plac)) if plac else float("nan")
    p_plac = bootstrap_mean_p(np.array(plac)) if plac else float("nan")

    if n < MIN_EVENTS:
        outcome = "UNSCORABLE"
    elif mean_S > 0 and p_S < P_THRESH and (not np.isfinite(mean_plac) or mean_plac <= mean_S):
        outcome = "SUPPORT"
    elif mean_S <= 0:
        outcome = "KILL"
    else:
        outcome = "INCONCLUSIVE"

    today = dt.date.today().isoformat()
    L = [f"# Result: Project Moon (propagation of a ruling to the listed parent of a subsidiary party)\n",
         f"Run {today} against moon_prereg.md, SHA-256 {h} (hashed before the run). Non-evidentiary: daily closes, one parameter set, no costs.\n"]
    if SELFTEST:
        L.append("**SELF-TEST RUN ON SYNTHETIC DATA. Not a result.**\n")
    L.append("## Population\n")
    L.append(f"- Universe: {unote}. Supreme Court sides: {len(pm_sc)}; resolved to a listed parent through Exhibit 21: "
             f"{int((pm_sc['basis'] == 'ex21 parent').sum())}; " + "; ".join(f"{k} ({v})" for k, v in pm_sc["basis"].value_counts().items()) + ".")
    L.append(f"- Moon events with usable windows and a coded direction: {n}; direct-party comparison events: {len(direct)}.\n")
    L.append("## Outcomes\n")
    L.append("| Statistic | Value |")
    L.append("|---|---|")
    L.append(f"| Mean signed day-0 reaction S_0 (parent) | {fmt(mean_S0)}, bootstrap p {p_S0:.3f} |")
    L.append(f"| Mean signed CAR(+1,+5) S (parent) | {fmt(mean_S)} (n = {n}), bootstrap p {p_S:.3f} |")
    L.append(f"| Mean abs(z_0): parents vs direct parties | {absz_moon:.2f} vs {absz_dir:.2f}; p(parents not smaller) {p_absz:.3f} |")
    L.append(f"| Placebo: random dates, random direction, same parents | {fmt(mean_plac)} (n = {len(plac)}), p {p_plac:.3f} |\n")
    L.append("## Decision rule as registered\n")
    L.append(f"- Mean S above zero: {'met' if np.isfinite(mean_S) and mean_S > 0 else 'not met'} ({fmt(mean_S)}).")
    L.append(f"- Bootstrap p below {P_THRESH}: {'met' if np.isfinite(p_S) and p_S < P_THRESH else 'not met'} (p = {p_S:.3f}).")
    L.append(f"- Placebo mean not above Moon mean: {'met' if np.isfinite(mean_plac) and mean_plac <= mean_S else 'n/a or not met'}.")
    L.append(f"- At least {MIN_EVENTS} events: {'met' if n >= MIN_EVENTS else 'not met'} ({n}).\n")
    L.append(f"Registered outcome: {outcome}.\n")
    L.append("## What this does not license\n")
    L.append("- Stakes are not coded; most parent events are immaterial and dilute the mean towards zero.")
    L.append("- partyWinning codes the formal winner; mixed rulings are signed as one side winning.")
    L.append("- Supreme Court only; events treated as independent.\n")
    L.append("## Events\n")
    L.append("| Date | Parent | Subsidiary party | Side won | AR(0) | z(0) | CAR(+1,+5) | S |")
    L.append("|---|---|---|---|---|---|---|---|")
    for _, r in moon.sort_values("date").iterrows():
        L.append(f"| {r['date']} | {r['ticker']} | {str(r['name'])[:50]} | {'yes' if r['dir'] > 0 else 'no'} | {fmt(r['ar0'])} | {r['z0']:+.2f} | {fmt(r['car_post'])} | {fmt(r['S'])} |")
    L.append("")
    L.append("## Run notes\n")
    bad = ev_par[ev_par["status"] != "ok"] if len(ev_par) else pd.DataFrame()
    L.append(f"- {len(bad)} parent sides excluded for data reasons." if len(bad) else "- No data exclusions among parent sides.")
    L.append("- Bootstrap: 10,000 draws, seed 20261030.")
    out = result_path("moon")
    out.write_text("\n".join(L) + "\n")
    if len(ev_par):
        ev_par.to_csv(out.with_suffix(".events.csv"), index=False)
    log(f"wrote {out}; outcome {outcome}; S {fmt(mean_S)} p={p_S:.3f} n={n}")


if __name__ == "__main__":
    main()
