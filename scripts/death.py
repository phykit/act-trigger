"""Project Death: long-winner, short-loser pairs where both sides are listed (prereg/death_prereg.md).

Usage: python scripts/death.py   (after scripts/build_universe.py)
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appeals_common import (SELFTEST, bootstrap_mean_p, build_party_map, build_universe, bulk_prices,  # noqa: E402
                            earnings_dates, log, near_earnings, result_path, rolling_ar, spec_hash)
from cost_gate import gate, round_trip  # noqa: E402

REACT = 2.0
POST = 5
CTRL_SPAN = 250
CTRL_GAP = 5
MIN_PAIRS = 15
P_THRESH = 0.10


def fmt(x: float) -> str:
    return "n/a" if x is None or not np.isfinite(x) else f"{100 * x:+.2f}%"


def main() -> None:
    h = spec_hash("death")
    uni, unote = build_universe()
    pm = build_party_map(uni)
    lst = pm[pm["basis"] == "listed"].dropna(subset=["ticker"]).copy()
    pairs = []
    for rid, g in lst.groupby(lst["ruling"].astype(int)):
        sides = g.drop_duplicates("side")
        if len(sides) >= 2 and sides["cik"].nunique() >= 2:
            a, b = sides.iloc[0], sides.iloc[1]
            pairs.append(dict(ruling=rid, t1=str(a["ticker"]), c1=str(a["cik"]), t2=str(b["ticker"]), c2=str(b["cik"])))
    log(f"rulings with both sides listed: {len(pairs)}")
    tick = sorted({p["t1"] for p in pairs} | {p["t2"] for p in pairs})
    px = bulk_prices(tick + ["SPY"], "litigants")
    ars = rolling_ar(px[[c for c in px.columns if c != "SPY"]], px["SPY"])
    spy = np.log(px["SPY"]).diff()
    spy_sig = spy.rolling(60, min_periods=40).std().shift(1)
    ed: dict[str, set] = {}

    def edates(cik: str) -> set:
        if cik not in ed:
            try:
                ed[cik] = earnings_dates(cik)
            except Exception:  # noqa: BLE001
                ed[cik] = set()
        return ed[cik]

    rows = []
    for p in pairs:
        u = uni.loc[p["ruling"]]
        d0 = u["date"] if isinstance(u["date"], dt.date) else pd.Timestamp(u["date"]).date()
        base = dict(ruling=p["ruling"], court=u["court"], date=d0, t1=p["t1"], t2=p["t2"])
        if p["t1"] not in ars or p["t2"] not in ars:
            rows.append({**base, "status": "no price history"})
            continue
        j = ars[p["t1"]][["ar", "sigma"]].join(ars[p["t2"]][["ar", "sigma"]], lsuffix="_1", rsuffix="_2", how="inner")
        idx = j.index
        pos = idx.searchsorted(pd.Timestamp(d0))
        if pos >= len(idx) or idx[pos].date() != d0 or pos + POST >= len(idx) or pos < 6:
            rows.append({**base, "status": "day 0 not a trading day or window incomplete"})
            continue
        a1, a2 = j["ar_1"].values, j["ar_2"].values
        sig = np.sqrt(j["sigma_1"].values ** 2 + j["sigma_2"].values ** 2)
        win, lose = (p["t1"], p["t2"]) if a1[pos] >= a2[pos] else (p["t2"], p["t1"])
        sgn = 1.0 if a1[pos] >= a2[pos] else -1.0
        P = sgn * (a1 - a2)                      # pair AR with A = market's winner on day 0
        zP0 = P[pos] / sig[pos]
        drift = float(P[pos + 1: pos + 1 + POST].sum())
        ctrl = []
        for q in range(max(0, pos - CTRL_SPAN), pos - CTRL_GAP):
            if not np.isfinite(sig[q]) or abs(P[q] / sig[q]) < REACT:
                continue
            dq = idx[q].date()
            if near_earnings(dq, edates(p["c1"])) or near_earnings(dq, edates(p["c2"])):
                continue
            sq, ss = float(spy.get(idx[q], np.nan)), float(spy_sig.get(idx[q], np.nan))
            if not (np.isfinite(sq) and np.isfinite(ss) and abs(sq) <= 2 * ss):
                continue
            ctrl.append(float(np.sign(P[q]) * P[q + 1: q + 1 + POST].sum()))
        cost = round_trip([(win, 1.0), (lose, 1.0)], d0)
        rows.append({**base, "status": "ok", "winner": win, "loser": lose, "ar_w0": float(max(a1[pos], a2[pos])),
                     "ar_l0": float(min(a1[pos], a2[pos])), "opposite_day0": bool(np.sign(a1[pos]) != np.sign(a2[pos])),
                     "zP0": float(zP0), "reacting": bool(abs(zP0) >= REACT), "pair_drift": drift,
                     "n_control": len(ctrl), "control_mean": float(np.mean(ctrl)) if ctrl else float("nan"),
                     "cost": cost, "party_winning": u.get("party_winning")})
    ev = pd.DataFrame(rows)
    ok = ev[ev.get("status", pd.Series(dtype=str)) == "ok"].copy() if len(ev) else ev
    react = ok[ok["reacting"]].copy() if len(ok) else ok
    diff = react[react["n_control"] >= 1].copy() if len(react) else react
    if len(diff):
        diff["d"] = diff["pair_drift"] - diff["control_mean"]
    n = len(diff)
    m = float(diff["d"].mean()) if n else float("nan")
    p = bootstrap_mean_p(diff["d"].values) if n else float("nan")
    g = gate(react["pair_drift"].values, react["cost"].values) if len(react) else dict(n=0, gross=np.nan, net=np.nan, median_cost=np.nan, passed=False, missing_cost=0)
    if n < MIN_PAIRS:
        outcome = "UNSCORABLE"
    elif m > 0 and p < P_THRESH and g["passed"]:
        outcome = "SUPPORT"
    elif m > 0 and p < P_THRESH:
        outcome = "SUPPORT (GROSS ONLY)"
    elif m <= 0:
        outcome = "KILL"
    else:
        outcome = "INCONCLUSIVE"
    mirror = float(np.corrcoef(react["ar_w0"], -react["ar_l0"])[0, 1]) if len(react) >= 3 else float("nan")
    L = ["# Result: Project Death (pair trades where both sides are listed)\n",
         f"Run {dt.date.today().isoformat()} against death_prereg.md, SHA-256 {h} (hashed before the run); cost gate prereg/cost_gate_prereg.md. "
         "Non-evidentiary: daily closes, one parameter set, no borrow cost.\n"]
    if SELFTEST:
        L.append("**SELF-TEST RUN ON SYNTHETIC DATA. Not a result.**\n")
    L += ["## Population\n", f"- Universe: {unote}.",
          f"- Rulings with both sides listed: {len(pairs)}; with usable windows: {len(ok)}; reacting pairs (abs(P_0)/sigma >= {REACT}): {len(react)}; "
          f"with at least one control day: {n}.\n",
          "## Outcomes\n", "| Statistic | Value |", "|---|---|",
          f"| Mean pair drift, reacting pairs (gross) | {fmt(g['gross'])} (n = {g['n']}) |",
          f"| Mean control drift | {fmt(float(diff['control_mean'].mean()) if n else float('nan'))} |",
          f"| Primary: mean pair drift minus control | {fmt(m)} (n = {n}) |",
          f"| Bootstrap p, one-sided | {p:.3f} |",
          f"| Cost gate: median round-trip cost (both legs) | {fmt(g['median_cost'])} |",
          f"| Cost gate: mean net pair drift | {fmt(g['net'])} ({'passed' if g['passed'] else 'not passed'}; {g['missing_cost']} without a cost estimate) |",
          f"| Mirror: corr(winner AR_0, minus loser AR_0); share moving opposite ways on day 0 | {mirror:.2f}; "
          f"{int(react['opposite_day0'].sum()) if len(react) else 0} of {len(react)} |\n",
          "## Decision rule as registered\n",
          f"- At least {MIN_PAIRS} reacting pairs: {'met' if n >= MIN_PAIRS else 'not met'} ({n}).",
          f"- Primary above zero, p below {P_THRESH}, and the cost gate passed.\n",
          f"Registered outcome: {outcome}.\n",
          "## What this does not license\n",
          "- Exact-name matching on both sides; equal-value legs; no borrow cost or short availability.",
          "- The market's winner is the day-0 leader, not the formal winner.\n"]
    out = result_path("death")
    out.write_text("\n".join(L) + "\n")
    ev.to_csv(out.with_suffix(".events.csv"), index=False)
    log(f"wrote {out}; outcome {outcome}; primary {fmt(m)} n={n}")


if __name__ == "__main__":
    main()
