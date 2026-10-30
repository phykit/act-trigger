# Result: Project Orange (decision-day reaction and post-decision drift)

Run 2026-10-30 against orange_prereg.md, SHA-256 c12e7b2990f4e211c8afafed5bf40f840b1675c15f4fb5f971781a7da7caa2cd (hashed before the run). Non-evidentiary: five cases chosen for salience, daily data, one parameter set, no costs.

## Population

- 5 primary legs entered (5 registered); 2 reacted (abs(z_0) at or above 2).

## Outcomes (reacting cases)

| Statistic | Value |
|---|---|
| Reacting cases | 2 of 5 |
| Mean signed CAR(+1,+1) | +6.87% |
| Mean signed CAR(+1,+5) | +8.87% |
| Cases continuing over +1 to +5 | 2 of 2 |
| Stouffer Z, one-sided p | 3.28, 0.001 |

## Decision rule as registered

- Mean signed CAR(+1,+5) above zero: met (+8.87%).
- Stouffer p below 0.1: met (p = 0.001).
- At least 3 reacting cases: not met (2).

Registered outcome: UNSCORABLE.

## What this does not license

- Cases chosen for salience: the day-0 reactions are large by construction and say nothing about the population rate Katz et al report (37% of candidates).
- Daily frequency: CAR(+1,+1) mixes the overnight gap with the next session.
- No costs, no hedging of the day-0 position, five observations.

## Cases

| Case | Ticker | Decided | AR(0) | z(0) | Reacted | CAR(-5,-1) | CAR(+1,+1) | CAR(+1,+5) | Signed CAR(+1,+5) | z drift | Sigma (daily) | Beta | Date checks | Price source |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Association for Molecular Pathology v. Myriad Genetics | MYGN | 2013-06-13 | -7.02% | -4.06 | yes | +10.55% | -14.33% | -17.61% | +17.61% | +4.56 | 1.73% | 0.82 | argued verified (Oyez); decided verified (Oyez) | MYGN: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Halliburton Co. v. Erica P. John Fund | HAL | 2014-06-23 | +0.24% | +0.21 | no | +1.95% | -2.33% | +1.08% | +1.08% | +0.41 | 1.17% | 1.41 | argued verified (Oyez); decided verified (Oyez) | HAL: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Ohio v. American Express | AXP | 2018-06-25 | +2.94% | +4.28 | yes | -0.28% | -0.59% | +0.12% | +0.12% | +0.08 | 0.69% | 1.16 | argued verified (Oyez); decided verified (Oyez and slip listing) | AXP: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Google LLC v. Oracle America | ORCL | 2021-04-05 | +1.86% | +1.19 | no | +1.86% | +0.21% | +1.77% | +1.77% | +0.51 | 1.56% | 0.95 | argued verified (Oyez); decided verified (Oyez and slip listing) | ORCL: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Amgen Inc. v. Sanofi | AMGN | 2023-05-18 | -0.70% | -0.59 | no | -3.32% | -0.33% | -2.79% | +2.79% | +1.06 | 1.18% | 0.34 | argued verified (Oyez); decided verified (Oyez and slip listing) | AMGN: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Google LLC v. Oracle America (secondary leg) | GOOGL | 2021-04-05 | +2.70% | +2.38 | yes | +1.92% | -0.40% | -0.18% | -0.18% | -0.07 | 1.14% | 0.97 | argued verified (Oyez); decided verified (Oyez and slip listing) | GOOGL: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |

## Run notes

- MYGN_12-398: slip listing for OT12 unavailable (no slip-opinion table with Date and Docket columns at https://www.supremecourt.gov/opinions/slipopinion/12); decision date checked against Oyez only
- HAL_13-317: slip listing for OT13 unavailable (no slip-opinion table with Date and Docket columns at https://www.supremecourt.gov/opinions/slipopinion/13); decision date checked against Oyez only
