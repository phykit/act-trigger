"""Compute trade outcomes for the events in data/gpr_events.csv, per the frozen spec.

Needs FRED series NASDAQ100, VXNCLS, VIXCLS (downloads them unless CSVs are supplied).
Usage: python scripts/outcomes.py
The 23 October 2026 run was executed as equivalent browser JavaScript against the same
FRED series; this script reproduces it (bootstrap seed differs, so p-values vary slightly).
"""
import math
import numpy as np
import pandas as pd
from scipy.stats import norm

FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}&cosd=1985-01-01"

def fred(sid):
    s = pd.read_csv(FRED.format(sid), index_col=0, parse_dates=True, na_values=".").iloc[:, 0]
    return pd.to_numeric(s, errors="coerce")

def call(S, K, T, v):
    d1 = (math.log(S / K) + 0.5 * v * v * T) / (v * math.sqrt(T))
    return S * norm.cdf(d1) - K * norm.cdf(d1 - v * math.sqrt(T))

def main():
    ndx = fred("NASDAQ100").dropna()
    vix = fred("VIXCLS").reindex(ndx.index).ffill(limit=5)
    vxn = fred("VXNCLS").reindex(ndx.index).ffill(limit=5)
    vol = (vxn / 100).fillna(1.3 * vix / 100)
    idx = ndx.index

    def trade(i):
        v = vol.iloc[i]
        if not np.isfinite(v) or i + 21 >= len(idx):
            return None
        T = 30 / 365
        debit = call(1, 1, T, v) - call(1, 1.08, T, v)
        x = ndx.iloc[i + 21] / ndx.iloc[i]
        return dict(cs=max(x - 1, 0) - max(x - 1.08, 0) - debit, eq=x - 1,
                    dvix=vix.iloc[i + 21] - vix.iloc[i])

    ev = pd.read_csv("data/gpr_events.csv", parse_dates=["act_day"])
    rows = []
    for r in ev.itertuples():
        i = idx.searchsorted(r.act_day, side="right")                # first trading day strictly after act day
        t = trade(i)
        if t:
            rows.append(dict(act_day=r.act_day.date(), entry=idx[i].date(), type=r.type, **t))
    res = pd.DataFrame(rows)
    start = idx.searchsorted(pd.Timestamp("1988-01-01"))
    base = pd.DataFrame([t for i in range(start, len(idx) - 22)
                         if 0.15 <= vol.iloc[i] <= 0.45 and (t := trade(i))])
    rng = np.random.default_rng(0)

    def bootp(obs, n, key, R=20000):
        draws = rng.choice(base[key].to_numpy(), size=(R, n)).mean(axis=1)
        return (draws >= obs).mean()

    for lab, g in [("anticipated", res[res.type == "anticipated"]), ("surprise", res[res.type == "surprise"]), ("all", res)]:
        print(f"{lab:12} n={len(g):2d}  call spread {g.cs.mean():+.2%} (base {base.cs.mean():+.2%}, win {np.mean(g.cs > 0):.0%}, "
              f"p {bootp(g.cs.mean(), len(g), 'cs'):.3f})  NDX21 {g.eq.mean():+.2%} (base {base.eq.mean():+.2%})  dVIX {g.dvix.mean():+.2f}")
    res.to_csv("results/event_outcomes.csv", index=False)

if __name__ == "__main__":
    main()
