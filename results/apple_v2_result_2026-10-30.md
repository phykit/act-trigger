# Result: Project Apple v2 (timing hazard in the argument-to-decision window)

Run 2026-10-30 against apple_v2_prereg.md, SHA-256 b84afa4aeeaddb8ca72c470d7656845f58c6550600ac0ffda76a56078c39682a (hashed before the run). Non-evidentiary: five cases, daily data, one parameter set, no costs.

## Population

- 5 cases entered the live arm (5 registered); 59 pooled non-decision opinion days against 296 non-opinion days inside the argument-to-decision windows.
- Placebo arm: 5 cases, windows shifted back 364 days.

## Outcomes

| Arm | Cases | Opinion days | Non-opinion days | Mean z^2 ratio R | Permutation p (one-sided) | Share of days with abs(z) > 1, opinion vs non-opinion |
|---|---|---|---|---|---|---|
| Live | 5 | 59 | 296 | 0.639 | 0.691 | 25% vs 25% |
| Placebo (same ticker, one year earlier) | 5 | 58 | 298 | 0.729 | 0.646 | n/a |

## Decision rule as registered

- R above 1: not met (R = 0.639).
- Permutation p below 0.1: not met (p = 0.691).
- R above the placebo R: not met (placebo R = 0.729).
- At least 4 cases and 15 pooled opinion days: met (5 cases, 59 opinion days).

Registered outcome: KILL.

## What this does not license

- Five cases and daily closes. The test bounds the answer; it does not establish it.
- Opinion days are the realised release dates, not the calendar as known at the start of each window. Source: SCDB release 2026_01, all decision types.
- The placebo controls weekday composition and the ticker's own variance, not other calendar events in the live window (June FOMC, index rebalances).
- Standardisation by the pre-argument residual sigma weights cases unequally where volatility regimes changed between estimation and window.

## Cases

| Case | Ticker | Argued | Decided | Days in W | Opinion days | Mean z^2 opinion | Mean z^2 non-opinion | Ratio | Placebo ratio | abs(z) > 1 opinion vs non | Sigma (daily) | Beta | Date checks | Price source |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Association for Molecular Pathology v. Myriad Genetics | MYGN | 2013-04-15 | 2013-06-13 | 41 | 9 | 1.05 | 2.12 | 0.494 | 0.812 | 44% vs 31% | 1.73% | 0.82 | argued verified (Oyez); decided verified (Oyez and SCDB 2026_01) | MYGN: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Halliburton Co. v. Erica P. John Fund | HAL | 2014-03-05 | 2014-06-23 | 75 | 15 | 0.54 | 0.75 | 0.722 | 0.889 | 13% vs 27% | 1.17% | 1.41 | argued verified (Oyez); decided verified (Oyez and SCDB 2026_01) | HAL: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Ohio v. American Express | AXP | 2018-02-26 | 2018-06-25 | 82 | 17 | 1.24 | 3.22 | 0.385 | 0.224 | 29% vs 42% | 0.69% | 1.16 | argued verified (Oyez); decided verified (Oyez and SCDB 2026_01) | AXP: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Google LLC v. Oracle America | ORCL | 2020-10-07 | 2021-04-05 | 121 | 13 | 1.25 | 0.87 | 1.434 | 1.251 | 31% vs 14% | 1.56% | 0.95 | argued verified (Oyez); decided verified (Oyez and SCDB 2026_01) | ORCL: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Amgen Inc. v. Sanofi | AMGN | 2023-03-27 | 2023-05-18 | 36 | 5 | 0.31 | 0.86 | 0.357 | 0.536 | 0% vs 23% | 1.18% | 0.34 | argued verified (Oyez); decided verified (Oyez and SCDB 2026_01) | AMGN: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |

## Run notes

- MYGN_12-398: slip listing for OT12 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- HAL_13-317: slip listing for OT13 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- AXP_16-1454: cross-check inside W, SCDB 17 opinion days, slip listing 14; in SCDB only [datetime.date(2018, 2, 27), datetime.date(2018, 3, 5), datetime.date(2018, 3, 20)]; in slip listing only []
- ORCL_18-956: cross-check inside W, SCDB 13 opinion days, slip listing 14; in SCDB only []; in slip listing only [datetime.date(2020, 11, 25)]
- AMGN_21-757: cross-check inside W, SCDB 5 opinion days, slip listing 5; in SCDB only []; in slip listing only []
- Permutations: 10000, seed 20261029. Estimation window: 2012-03-29 to 2013-03-28 for the first case; 250 trading days ending 10 trading days before argument for each.
