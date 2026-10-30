"""Project Strife: when the day-0 price moves against the formal outcome, does the price keep going (prereg/strife_prereg.md)?

Population: Supreme Court events with a coded formal direction, from Earth (listed parties) and Moon (listed parents).
Usage: python scripts/strife.py   (after scripts/build_universe.py)
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appeals_common import (SELFTEST, bootstrap_mean_p, build_party_map, build_universe, compute_events,  # noqa: E402
                            log, result_path, spec_hash)

Z_THRESH = 1.5
MIN_EVENTS = 10
P_THRESH = 0.10


def fmt(x: float) -> str:
    return "n/a" if x is None or not np.isfinite(x) else f"{100 * x:+.2f}%"


def direction(row: pd.Series) -> float:
    pw = row.get("party_winning")
    if pw not in (0, 1, 0.0, 1.0):
        return float("nan")
    won = (row["side"] == "petitioner" and pw == 1) or (row["side"] == "respondent" and pw == 0)
    return 1.0 if won else -1.0


def main() -> None:
    h = spec_hash("strife")
    uni, unote = build_universe()
    pm = build_party_map(uni)
    sc = uni[uni["court"] == "scotus"]
    pm_sc = pm[pm["ruling"].astype(int).isin(sc.index)]
    parts = []
    for bases, label, pop in ((("listed",), "litigants", "Earth (listed party)"), (("ex21 parent",), "parents", "Moon (listed parent)")):
        ev, _, _ = compute_events(uni, pm_sc, bases, label, post=5)
        if len(ev) and "status" in ev.columns:
            ev = ev[ev["status"] == "ok"].copy()
            ev["population"] = pop
            parts.append(ev)
    ev = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()
    ev["F"] = ev.apply(direction, axis=1)
    ev = ev[ev["F"].notna()].copy()
    ev["D"] = np.sign(ev["ar0"]) * ev["car_post"]
    big = ev["z0"].abs() >= Z_THRESH
    dis = ev[big & (np.sign(ev["ar0"]) == -ev["F"])].copy()
    agr = ev[big & (np.sign(ev["ar0"]) == ev["F"])].copy()
    n = len(dis)
    m_dis = float(dis["D"].mean()) if n else float("nan")
    p_dis = bootstrap_mean_p(dis["D"].values) if n else float("nan")
    p_rev = bootstrap_mean_p(-dis["D"].values) if n else float("nan")
    m_agr = float(agr["D"].mean()) if len(agr) else float("nan")

    if n < MIN_EVENTS:
        outcome = "UNSCORABLE"
    elif m_dis > 0 and p_dis < P_THRESH:
        outcome = "SUPPORT (the price is right)"
    elif m_dis < 0 and p_rev < P_THRESH:
        outcome = "REVERSE FINDING (the headline is right)"
    else:
        outcome = "INCONCLUSIVE"

    L = ["# Result: Project Strife (price against the formal outcome)\n",
         f"Run {dt.date.today().isoformat()} against strife_prereg.md, SHA-256 {h} (hashed before the run). Non-evidentiary: daily closes, one parameter set, no costs.\n"]
    if SELFTEST:
        L.append("**SELF-TEST RUN ON SYNTHETIC DATA. Not a result.**\n")
    L += ["## Population\n", f"- Universe: {unote}.",
          f"- Supreme Court events with a coded formal direction: {len(ev)} ({', '.join(f'{k} {v}' for k, v in ev['population'].value_counts().items())}).",
          f"- abs(z_0) >= {Z_THRESH}: {int(big.sum())}; disagreement events: {n}; agreement events: {len(agr)}.\n",
          "## Outcomes\n", "| Statistic | Value |", "|---|---|",
          f"| Mean D on disagreement events (continuation positive) | {fmt(m_dis)} (n = {n}) |",
          f"| Bootstrap p, one-sided, D > 0 | {p_dis:.3f} |",
          f"| Bootstrap p, one-sided, D < 0 | {p_rev:.3f} |",
          f"| Mean D on agreement events | {fmt(m_agr)} (n = {len(agr)}) |",
          f"| Difference, disagreement minus agreement | {fmt(m_dis - m_agr) if n and len(agr) else 'n/a'} |\n",
          "## Decision rule as registered\n",
          f"- At least {MIN_EVENTS} disagreement events: {'met' if n >= MIN_EVENTS else 'not met'} ({n}).",
          f"- Support: mean D above zero with p below {P_THRESH}; reverse finding: below zero with p below {P_THRESH} for the opposite sign.\n",
          f"Registered outcome: {outcome}.\n",
          "## What this does not license\n",
          "- SCDB's formal winner is the party favoured by the disposition, not the economic winner; some disagreements are coding, not economics.",
          "- Supreme Court only; events treated as independent; one parameter set.\n"]
    out = result_path("strife")
    out.write_text("\n".join(L) + "\n")
    pd.concat([dis.assign(group="disagreement"), agr.assign(group="agreement")]).to_csv(out.with_suffix(".events.csv"), index=False)
    log(f"wrote {out}; outcome {outcome}; mean D {fmt(m_dis)} n={n}")


if __name__ == "__main__":
    main()
