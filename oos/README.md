# Out-of-sample log

Each qualifying act is recorded in `log.csv` as soon as it is detected, before its outcome is known. Outcomes are added later in the same row; nothing is deleted or overwritten except blank outcome cells being filled.

## Live conventions (these differ from the backtest and are stated here, not in the frozen spec)

- **Detection.** `scripts/monitor.py` runs weekly after the GPR daily index is updated (Mondays). Rule identical to the frozen specification.
- **Live entry date.** The NDX close on the first trading day after the detection date, not after the act day. This captures the real publication latency of GPR daily (up to about a week). The backtest's act-day entry is recorded alongside for comparison.
- **Outcome.** After 21 trading days from the live entry: NDX 21-day return; P&L of a bought one-month 100/108 NDX call spread priced off VXN at the live entry close; VIX change. Computed from FRED NASDAQ100, VXNCLS and VIXCLS, with source values quoted.
- **Revisions.** GPR daily is preliminary and can be revised. The vintage date that first showed the event is recorded; later revisions do not remove a logged event.
- **No trading is implied.** This log measures; it does not instruct.

## Columns

`detected_on, gpr_vintage_end, act_day, gprd_act, p99, threat30, threat_p75, type, backtest_entry, live_entry, ndx_entry, vxn_entry, ndx_exit, exit_date, ndx_21d, call_spread_pnl, vix_change, status, notes`
