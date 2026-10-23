"""Live monitor: apply the frozen act-trigger rule (prereg/act_trigger_prereg.md) to the latest GPR vintage.

Usage:
    python scripts/monitor.py path/to/data_gpr_daily_recent.dta [--lookback 21]

Prints a JSON object listing qualifying act days in the last `lookback` days of the
vintage that are not already in oos/log.csv. The rule is identical to
scripts/detect_events.py except that there is no fixed end date and de-clustering
looks back across the full history (an act day counts only if no act day at or above
the trailing 99th percentile occurred in the previous 30 calendar days).

This script never edits the frozen specification and never computes outcomes.
"""
import argparse
import json
import os
import pandas as pd

def qualifying(path):
    d = pd.read_stata(path)[["date", "GPRD_ACT", "GPRD_THREAT"]].set_index("date").sort_index().asfreq("D")
    act, thr = d.GPRD_ACT, d.GPRD_THREAT
    thr30 = thr.shift(1).rolling(30, min_periods=25).mean()
    p99 = act.shift(1).rolling(1095, min_periods=900).quantile(0.99)
    p75 = thr30.shift(1).rolling(1095, min_periods=900).quantile(0.75)
    cand = d.index[(act >= p99) & (d.index >= "1988-01-01")]
    events, prev = [], None
    for t in cand:
        if prev is None or (t - prev).days > 30:
            events.append(t)
        prev = t
    vintage_end = d.index[d.GPRD_ACT.notna()].max()
    return events, act, thr30, p99, p75, vintage_end

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dta")
    ap.add_argument("--lookback", type=int, default=21)
    a = ap.parse_args()
    events, act, thr30, p99, p75, vend = qualifying(a.dta)
    logged = set()
    if os.path.exists("oos/log.csv"):
        logged = set(pd.read_csv("oos/log.csv").act_day.astype(str))
    recent = [t for t in events if (vend - t).days <= a.lookback and str(t.date()) not in logged]
    out = {
        "vintage_end": str(vend.date()),
        "latest_gprd_act": round(float(act[vend]), 1),
        "latest_p99_threshold": round(float(p99[vend]), 1),
        "new_events": [
            {"act_day": str(t.date()), "gprd_act": round(float(act[t]), 1),
             "p99": round(float(p99[t]), 1), "threat30": round(float(thr30[t]), 1),
             "threat_p75": round(float(p75[t]), 1),
             "type": "anticipated" if thr30[t] >= p75[t] else "surprise"}
            for t in recent
        ],
    }
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
