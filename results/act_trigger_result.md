# Result: Anticipated-act trigger (objective GPR definition)

Run 23 October 2026 against act_trigger_prereg.md, SHA-256 af0aeb33f85b5db06e731d61b712755297c39debed8459e5e1acf483360404e5 (hashed before the run). Non-evidentiary in the fntn sense: a single crude test, flat-vol pricing, no costs.

## Population

- 201 GPRD_ACT days at or above the trailing 99th percentile; 47 events after 30-day de-clustering (13 anticipated, 34 surprise).
- 45 tradable: the two 1989 events precede VIX and are dropped. Final: 13 anticipated, 32 surprise.
- Baseline: 7,978 trading days, 1988 to 2026, entry vol 15% to 45%.

## Outcomes (entry at the NDX close on the first trading day after the act day; 21 trading days)

| Group | n | Call spread 100/108 mean | Win | Bootstrap p vs baseline | NDX 21d mean | Up | VIX change |
|---|---|---|---|---|---|---|---|
| Anticipated | 13 | +2.01% | 69% | 0.042 | +4.01% | 77% | -2.70 |
| Surprise | 32 | +0.27% | 41% | 0.739 | +1.10% | 69% | +0.73 |
| All acts | 45 | +0.77% | 49% | 0.349 | +1.94% | 71% | -0.26 |
| Baseline | 7,978 | +0.61% | n/a | n/a | +1.43% | n/a | 0.00 |
| Anticipated, post-2000 (descriptive only) | 9 | +2.28% | 78% | 0.045 | +4.70% | 89% | -3.94 |

## Decision rule as registered

- Anticipated mean above baseline with one-sided bootstrap p below 0.10: met (p = 0.042).
- Surprise mean not above anticipated: met (+0.27% against +2.01%).
- At least 10 anticipated events: met (13).

Registered outcome: SUPPORT.

## What this does not license

- It does not establish a tradable edge. Thirteen events; one parameter set; bootstrap draws treat baseline days as independent.
- GPR daily is published weekly; live entry would be up to a week later than tested unless a real-time news count is built.
- Flat-vol pricing ignores skew and bid-offer; a 2% average on a 2% to 3% debit is sensitive to both.
- The act index includes terror acts, so "anticipated" here means "act during an elevated-threat period", which is broader than war with a prelude.
- The 2026-03-01 act (US-Israel strikes on Iran) was classified surprise by 0.2 index points. The classification is knife-edge exactly where the current conflict sits.

## Anticipated events

| Act day | Entry | Call spread | NDX 21d |
|---|---|---|---|
| 1990-08-13 | 1990-08-14 | -2.57% | -8.92% |
| 1990-10-01 | 1990-10-02 | -2.69% | -6.68% |
| 1990-12-31 | 1991-01-02 | +5.34% | +16.35% |
| 1999-12-20 | 1999-12-21 | +5.49% | +9.11% |
| 2011-03-07 | 2011-03-08 | -2.20% | -0.22% |
| 2013-04-17 | 2013-04-18 | +6.05% | +10.47% |
| 2013-09-23 | 2013-09-24 | +2.37% | +3.96% |
| 2014-07-18 | 2014-07-21 | +1.12% | +2.69% |
| 2022-02-23 | 2022-02-24 | +2.93% | +5.58% |
| 2023-10-16 | 2023-10-17 | +2.44% | +4.60% |
| 2025-05-07 | 2025-05-08 | +5.63% | +8.64% |
| 2025-06-20 | 2025-06-23 | +3.86% | +5.98% |
| 2025-11-03 | 2025-11-04 | -1.66% | +0.57% |

Sources: Caldara and Iacoviello GPR daily (vintage 2026-10-19); FRED NASDAQ100, VXNCLS, VIXCLS (retrieved 23 October 2026).
