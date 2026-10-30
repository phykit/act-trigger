# Result: Project Apple (timing hazard in the argument-to-decision window)

Run 2026-10-30 against apple_prereg.md, SHA-256 068f59f04174f8018788084fb457ed9fa94d79da68ce902b34288af141dff17d (hashed before the run). Non-evidentiary: five cases, daily data, one parameter set, no costs.

## Population

- 3 cases entered the live arm (5 registered); 33 pooled non-decision opinion days against 206 non-opinion days inside the argument-to-decision windows.
- Placebo arm: 3 cases, windows shifted back 364 days.

## Outcomes

| Arm | Cases | Opinion days | Non-opinion days | Mean z^2 ratio R | Permutation p (one-sided) | Share of days with abs(z) > 1, opinion vs non-opinion |
|---|---|---|---|---|---|---|
| Live | 3 | 33 | 206 | 0.718 | 0.400 | 27% vs 24% |
| Placebo (same ticker, one year earlier) | 3 | 32 | 208 | 0.700 | 0.541 | n/a |

## Decision rule as registered

- R above 1: not met (R = 0.718).
- Permutation p below 0.1: not met (p = 0.400).
- R above the placebo R: met (placebo R = 0.700).
- At least 4 cases and 15 pooled opinion days: not met (3 cases, 33 opinion days).

Registered outcome: UNSCORABLE.

## What this does not license

- Five cases and daily closes. The test bounds the answer; it does not establish it.
- Opinion days are the realised release dates, not the calendar as known at the start of each window.
- The placebo controls weekday composition and the ticker's own variance, not other calendar events in the live window (June FOMC, index rebalances).
- Standardisation by the pre-argument residual sigma weights cases unequally where volatility regimes changed between estimation and window.

## Cases

| Case | Ticker | Argued | Decided | Days in W | Opinion days | Mean z^2 opinion | Mean z^2 non-opinion | Ratio | Placebo ratio | abs(z) > 1 opinion vs non | Sigma (daily) | Beta | Date checks | Price source |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ohio v. American Express | AXP | 2018-02-26 | 2018-06-25 | 82 | 14 | 1.44 | 3.09 | 0.468 | 0.275 | 36% vs 40% | 0.69% | 1.16 | argued verified (Oyez); decided verified (Oyez and slip listing) | AXP: yfinance; SPY: yfinance |
| Google LLC v. Oracle America | ORCL | 2020-10-07 | 2021-04-05 | 121 | 14 | 1.17 | 0.88 | 1.320 | 1.152 | 29% vs 14% | 1.56% | 0.95 | argued verified (Oyez); decided verified (Oyez and slip listing) | ORCL: yfinance; SPY: yfinance |
| Amgen Inc. v. Sanofi | AMGN | 2023-03-27 | 2023-05-18 | 36 | 5 | 0.31 | 0.86 | 0.357 | 0.536 | 0% vs 23% | 1.18% | 0.34 | argued verified (Oyez); decided verified (Oyez and slip listing) | AMGN: yfinance; SPY: yfinance |

## Run notes

- MYGN_12-398: opinion-day listing for OT12 unavailable (no slip-opinion table with Date and Docket columns at https://www.supremecourt.gov/opinions/slipopinion/12); case excluded
- HAL_13-317: opinion-day listing for OT13 unavailable (no slip-opinion table with Date and Docket columns at https://www.supremecourt.gov/opinions/slipopinion/13); case excluded
- Permutations: 10000, seed 20261029. Estimation window: 2017-02-13 to 2018-02-08 for the first case; 250 trading days ending 10 trading days before argument for each.
