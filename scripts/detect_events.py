"""Detect GPR act events by the rule frozen in prereg/act_trigger_prereg.md.

Input: Caldara and Iacoviello daily GPR (data_gpr_daily_recent.dta), e.g. from
https://raw.githubusercontent.com/iacoviel/iacoviel.github.io/master/gpr_files/data_gpr_daily_recent.dta
Output: data/gpr_events.csv

Usage: python scripts/detect_events.py path/to/data_gpr_daily_recent.dta
"""
import sys
import pandas as pd

def main(path, out="data/gpr_events.csv"):
    d = pd.read_stata(path)[["date", "GPRD_ACT", "GPRD_THREAT"]].set_index("date").sort_index().asfreq("D")
    act, thr = d.GPRD_ACT, d.GPRD_THREAT
    thr30 = thr.shift(1).rolling(30, min_periods=25).mean()                    # mean of t-30..t-1
    p99 = act.shift(1).rolling(1095, min_periods=900).quantile(0.99)           # trailing, t excluded
    p75 = thr30.shift(1).rolling(1095, min_periods=900).quantile(0.75)
    cand = d.index[(act >= p99) & (d.index >= "1988-01-01") & (d.index <= "2026-09-20")]
    events, prev = [], None
    for t in cand:                                                              # de-cluster: no act day in prior 30 days
        if prev is None or (t - prev).days > 30:
            events.append(t)
        prev = t
    rows = [(t.date(), round(act[t], 1), round(thr30[t], 1), round(p75[t], 1),
             "anticipated" if thr30[t] >= p75[t] else "surprise") for t in events]
    ev = pd.DataFrame(rows, columns=["act_day", "GPRD_ACT", "threat30", "threat_p75", "type"])
    ev.to_csv(out, index=False)
    print(f"{len(cand)} act days at p99; {len(ev)} events; {ev.type.value_counts().to_dict()}")

if __name__ == "__main__":
    main(sys.argv[1])
