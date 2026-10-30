"""Project Earth: post-ruling drift in the litigant against a like-for-like control (prereg/earth_prereg.md).

Usage: python scripts/earth.py   (run scripts/build_universe.py first, or let this build the caches)
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appeals_common import (SELFTEST, bootstrap_mean_p, build_party_map, build_universe, compute_events,  # noqa: E402
                            log, result_path, spec_hash)

MIN_EVENTS = 40
P_THRESH = 0.05


def fmt(x: float) -> str:
    return "n/a" if x is None or not np.isfinite(x) else f"{100 * x:+.2f}%"


def main() -> None:
    h = spec_hash("earth")
    uni, unote = build_universe()
    pm = build_party_map(uni)
    ev, _, _ = compute_events(uni, pm, ("listed",), "litigants", post=5)
    ok = ev[ev["status"] == "ok"].copy()
    react = ok[ok["reacting"]].copy()
    diff = react[react["n_control"] >= 3].copy()
    diff["d"] = diff["signed_post"] - diff["control_mean"]
    n = len(diff)
    mean_diff = float(diff["d"].mean()) if n else float("nan")
    p_diff = bootstrap_mean_p(diff["d"].values) if n else float("nan")
    mean_drift = float(react["signed_post"].mean()) if len(react) else float("nan")
    z_stouffer = float(np.sum(react["signed_post"] / (react["sigma"] * np.sqrt(5))) / np.sqrt(len(react))) if len(react) else float("nan")
    p_stouffer = float(1 - norm.cdf(z_stouffer)) if len(react) else float("nan")
    mean_ctrl = float(diff["control_mean"].mean()) if n else float("nan")

    if n < MIN_EVENTS:
        outcome = "UNSCORABLE"
    elif mean_diff > 0 and p_diff < P_THRESH:
        outcome = "SUPPORT"
    elif mean_diff <= 0:
        outcome = "KILL"
    else:
        outcome = "INCONCLUSIVE"

    today = dt.date.today().isoformat()
    L = [f"# Result: Project Earth (post-ruling drift in the litigant against a like-for-like control)\n",
         f"Run {today} against earth_prereg.md, SHA-256 {h} (hashed before the run). Non-evidentiary: daily closes, one parameter set, no costs.\n"]
    if SELFTEST:
        L.append("**SELF-TEST RUN ON SYNTHETIC DATA. Not a result.**\n")
    L.append("## Population\n")
    L.append(f"- Universe: {unote}.")
    L.append(f"- Sides matched exactly to a listed company: {int((pm['basis'] == 'listed').sum())} of {len(pm)}; "
             f"events with usable price windows: {len(ok)} of {len(ev)}; reacting (abs(z_0) >= 2, not earnings-adjacent, calm market): {len(react)} "
             f"({100 * len(react) / max(len(ok), 1):.0f}% reaction rate); events in the difference (at least three control days): {n}.\n")
    L.append("## Outcomes\n")
    L.append("| Statistic | Value |")
    L.append("|---|---|")
    L.append(f"| Mean signed CAR(+1,+5) after rulings, reacting events | {fmt(mean_drift)} (n = {len(react)}) |")
    L.append(f"| Stouffer Z, one-sided p (rulings alone) | {z_stouffer:.2f}, {p_stouffer:.3f} |")
    L.append(f"| Mean control drift (same companies' other abs(z) >= 2 days) | {fmt(mean_ctrl)} |")
    L.append(f"| Mean difference, ruling minus control | {fmt(mean_diff)} (n = {n}) |")
    L.append(f"| Bootstrap p, one-sided | {p_diff:.3f} |")
    if len(react):
        cont = int((react["signed_post"] > 0).sum())
        L.append(f"| Reacting events continuing over +1 to +5 | {cont} of {len(react)} |")
    for court in sorted(ok["court"].unique()):
        sub = diff[diff["court"] == court]
        L.append(f"| {court}: events in difference, mean difference | {len(sub)}, {fmt(float(sub['d'].mean()) if len(sub) else float('nan'))} |")
    gen = diff[~diff["opposing_basis"].isin(["listed", "ex21 parent"])]
    L.append(f"| General-application subset (opponent not a listed company or its subsidiary) | {len(gen)}, {fmt(float(gen['d'].mean()) if len(gen) else float('nan'))} |\n")
    L.append("## Decision rule as registered\n")
    L.append(f"- Mean difference above zero: {'met' if np.isfinite(mean_diff) and mean_diff > 0 else 'not met'} ({fmt(mean_diff)}).")
    L.append(f"- Bootstrap p below {P_THRESH}: {'met' if np.isfinite(p_diff) and p_diff < P_THRESH else 'not met'} (p = {p_diff:.3f}).")
    L.append(f"- At least {MIN_EVENTS} events in the difference: {'met' if n >= MIN_EVENTS else 'not met'} ({n}).\n")
    L.append(f"Registered outcome: {outcome}.\n")
    L.append("## What this does not license\n")
    L.append("- Exact-name matching: subsidiaries and differently registered names are not here (Project Moon).")
    L.append("- Daily closes; Federal Circuit release times are untimestamped; rolling estimates lag a day.")
    L.append("- The control is any large idiosyncratic move not excluded by the screens; events are treated as independent.\n")
    L.append("## Reacting events\n")
    L.append("| Court | Date | Ticker | Case | AR(0) | z(0) | CAR(-5,-1) | CAR(+1,+1) | CAR(+1,+5) | Signed | Control mean (n) | Difference | Opponent |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for _, r in react.sort_values("date").iterrows():
        case = str(uni.loc[r["ruling"], "case_name"])[:60]
        d = r["signed_post"] - r["control_mean"] if np.isfinite(r["control_mean"]) else float("nan")
        L.append(f"| {r['court']} | {r['date']} | {r['ticker']} | {case} | {fmt(r['ar0'])} | {r['z0']:+.2f} | {fmt(r['pre5'])} | {fmt(r['car1'])} | "
                 f"{fmt(r['car_post'])} | {fmt(r['signed_post'])} | {fmt(r['control_mean'])} ({int(r['n_control'])}) | {fmt(d)} | {r['opposing_basis']} |")
    L.append("")
    L.append("## Run notes\n")
    bad = ev[ev["status"] != "ok"]
    L.append(f"- {len(bad)} matched sides excluded for data reasons: " + "; ".join(f"{k} ({v})" for k, v in bad["status"].value_counts().items()) if len(bad) else "- No data exclusions.")
    L.append(f"- Party-map bases: " + "; ".join(f"{k} ({v})" for k, v in pm["basis"].value_counts().items()))
    L.append("- Bootstrap: 10,000 draws over events, seed 20261030; controls within 252 trading days, ten-day gap around rulings, earnings-adjacent and non-calm days excluded.")
    out = result_path("earth")
    out.write_text("\n".join(L) + "\n")
    ev.to_csv(out.with_suffix(".events.csv"), index=False)
    log(f"wrote {out}; outcome {outcome}; diff {fmt(mean_diff)} p={p_diff:.3f} n={n}")


if __name__ == "__main__":
    main()
