"""Project Storm: do non-party companies that name the case in their own pre-ruling 10-K or 10-Q react to the ruling
(prereg/storm_prereg.md)? Exposure is found with EDGAR full-text search; the basket is equal-weighted.

Usage: python scripts/storm.py   (after scripts/build_universe.py; needs SEC_CONTACT for EDGAR)
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appeals_common import (SELFTEST, bootstrap_mean_p, build_party_map, build_universe, bulk_prices,  # noqa: E402
                            edgar_tickers, log, result_path, rolling_ar, spec_hash)
from cost_gate import gate, round_trip  # noqa: E402
from fts import is_government, search, term  # noqa: E402

MIN_RULINGS = 20
MIN_NAMES = 3
P_THRESH = 0.05
DRIFT_MIN = 15
DRIFT_P = 0.10
SEED = 20261030
POST = 5


def fmt(x: float, pct: bool = True) -> str:
    if x is None or not np.isfinite(x):
        return "n/a"
    return f"{100 * x:+.2f}%" if pct else f"{x:.3f}"


def main() -> None:
    h = spec_hash("storm")
    uni, unote = build_universe()
    pm = build_party_map(uni)
    tick = edgar_tickers()
    cik2t = tick.drop_duplicates("cik").set_index("cik")["ticker"].to_dict()
    exposure, status = {}, {}
    for rid, u in uni.iterrows():
        sides = [s for s in (u.get("petitioner"), u.get("respondent")) if isinstance(s, str) and s.strip()]
        if not sides:
            from appeals_common import split_parties  # noqa: PLC0415
            sides = [s for s in split_parties(u["case_name"]) if s]
        terms = [term(s, 2) for s in sides if not is_government(s)]
        terms = [t for t in terms if t]
        if not terms:
            status[rid] = "out of scope (government or no usable caption)"
            continue
        q = " ".join(f'"{t}"' for t in terms) if len(terms) > 1 else f'"{terms[0]}" Court'
        d0 = u["date"] if isinstance(u["date"], dt.date) else pd.Timestamp(u["date"]).date()
        try:
            hits = search(q, "10-K,10-Q", d0 - dt.timedelta(days=400), d0 - dt.timedelta(days=1), max_pages=10)
        except Exception as exc:  # noqa: BLE001
            status[rid] = f"search failed: {str(exc)[:50]}"
            continue
        party_ciks = set(pm.loc[pm["ruling"].astype(int) == int(rid), "cik"].dropna().astype(str))
        ciks = {f"{int(c):010d}" for x in hits for c in (x.get("ciks") or [])}
        names = sorted({cik2t[c] for c in ciks - party_ciks if c in cik2t})
        exposure[rid] = names
        status[rid] = "searched"
    cand = {r: n for r, n in exposure.items() if len(n) >= MIN_NAMES}
    log(f"rulings searched: {sum(1 for s in status.values() if s == 'searched')}; with at least {MIN_NAMES} exposed names: {len(cand)}")
    alln = sorted({t for n in cand.values() for t in n})
    px = bulk_prices(alln + ["SPY"], "storm") if alln else pd.DataFrame()
    ars = rolling_ar(px[[c for c in px.columns if c != "SPY"]], px["SPY"]) if len(px) else {}
    rows, nulls = [], []
    for rid, names in cand.items():
        u = uni.loc[rid]
        d0 = u["date"] if isinstance(u["date"], dt.date) else pd.Timestamp(u["date"]).date()
        have = [t for t in names if t in ars]
        if len(have) < MIN_NAMES:
            rows.append(dict(ruling=rid, court=u["court"], date=d0, n_exposed=len(names), n_priced=len(have), status="fewer than three priced names"))
            continue
        basket = pd.concat([ars[t]["ar"] for t in have], axis=1).mean(axis=1, skipna=True).dropna()
        sig = basket.rolling(60, min_periods=40).std().shift(1)
        z = (basket / sig).dropna()
        idx = z.index
        pos = idx.searchsorted(pd.Timestamp(d0))
        if pos >= len(idx) or idx[pos].date() != d0 or pos + POST >= len(idx) or pos < 260:
            rows.append(dict(ruling=rid, court=u["court"], date=d0, n_exposed=len(names), n_priced=len(have), status="window incomplete"))
            continue
        bpos = basket.index.get_loc(idx[pos])
        ar0 = float(basket.iloc[bpos])
        drift = float(np.sign(ar0) * basket.iloc[bpos + 1: bpos + 1 + POST].sum())
        nulls.append(np.abs(z.values[pos - 250: pos - 5]))
        cost = round_trip([(t, 1.0 / len(have)) for t in have], d0)
        rows.append(dict(ruling=rid, court=u["court"], date=d0, n_exposed=len(names), n_priced=len(have), status="ok",
                         ar0=ar0, z0=float(z.values[pos]), drift=drift, cost=cost, names=" ".join(have[:40])))
    ev = pd.DataFrame(rows)
    ok = ev[ev["status"] == "ok"].copy() if len(ev) else ev
    n = len(ok)
    obs = float(ok["z0"].abs().mean()) if n else float("nan")
    if n:
        rng = np.random.default_rng(SEED)
        draws = np.column_stack([rng.choice(a, size=10_000) for a in nulls]).mean(axis=1)
        p = float(np.mean(draws >= obs))
        null_mean = float(draws.mean())
    else:
        p, null_mean = float("nan"), float("nan")
    react = ok[ok["z0"].abs() >= 2] if n else ok
    d_mean = float(react["drift"].mean()) if len(react) else float("nan")
    d_p = bootstrap_mean_p(react["drift"].values) if len(react) else float("nan")
    g = gate(react["drift"].values, react["cost"].values) if len(react) else dict(n=0, gross=np.nan, net=np.nan, median_cost=np.nan, passed=False, missing_cost=0)
    if n < MIN_RULINGS:
        outcome = "UNSCORABLE"
    elif p < P_THRESH:
        outcome = "SUPPORT"
    elif obs <= null_mean:
        outcome = "KILL"
    else:
        outcome = "INCONCLUSIVE"
    drift_claim = (len(react) >= DRIFT_MIN and d_mean > 0 and d_p < DRIFT_P and g["passed"])
    sv = pd.Series(status).value_counts()
    L = ["# Result: Project Storm (contagion to companies that disclosed exposure to the case)\n",
         f"Run {dt.date.today().isoformat()} against storm_prereg.md, SHA-256 {h} (hashed before the run); cost gate prereg/cost_gate_prereg.md. "
         "Non-evidentiary: daily closes, equal-weighted baskets, one parameter set.\n"]
    if SELFTEST:
        L.append("**SELF-TEST RUN ON SYNTHETIC DATA. Not a result.**\n")
    L += ["## Population\n", f"- Universe: {unote}.",
          "- Rulings: " + "; ".join(f"{k} ({v})" for k, v in sv.items()) + ".",
          f"- With at least {MIN_NAMES} exposed listed non-party companies: {len(cand)}; with a usable basket window: {n}.\n",
          "## Outcomes\n", "| Statistic | Value |", "|---|---|",
          f"| Primary: mean basket abs(z_0) on ruling day | {fmt(obs, False)} (n = {n}) |",
          f"| Null: mean abs(z) on random prior days | {fmt(null_mean, False)} |",
          f"| One-sided p | {fmt(p, False)} |",
          f"| Reacting rulings (basket abs(z_0) >= 2): mean basket drift | {fmt(d_mean)} (n = {len(react)}), bootstrap p {fmt(d_p, False)} |",
          f"| Cost gate on basket drift: median cost, mean net | {fmt(g['median_cost'])}, {fmt(g['net'])} ({'passed' if g['passed'] else 'not passed'}) |",
          f"| Median exposed names per ruling | {float(ok['n_priced'].median()) if n else float('nan'):.0f} |"]
    for court in sorted(ok["court"].unique()) if n else []:
        s = ok[ok["court"] == court]
        L.append(f"| {court}: rulings, mean abs(z_0) | {len(s)}, {fmt(float(s['z0'].abs().mean()), False)} |")
    L += ["", "## Decision rule as registered\n",
          f"- At least {MIN_RULINGS} rulings: {'met' if n >= MIN_RULINGS else 'not met'} ({n}).",
          f"- Support: p below {P_THRESH}; kill: observed at or below the null mean.",
          f"- Drift claim (separate): {'supported' if drift_claim else 'not made'} (needs at least {DRIFT_MIN} reacting rulings, drift above zero with p below {DRIFT_P}, and the cost gate).\n",
          f"Registered outcome: {outcome}.\n",
          "## What this does not license\n",
          "- Two-word caption terms can match unrelated text; long-cited leading cases inflate exposure.",
          "- The paired comparison with Fire's SIC baskets is not computed in this run and is reported separately.\n"]
    out = result_path("storm")
    out.write_text("\n".join(L) + "\n")
    ev.to_csv(out.with_suffix(".events.csv"), index=False)
    log(f"wrote {out}; outcome {outcome}; mean abs z {fmt(obs, False)} vs null {fmt(null_mean, False)} p={fmt(p, False)} n={n}")


if __name__ == "__main__":
    main()
