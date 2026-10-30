# Result: Project Apple v3 (wide sample) (timing hazard in the argument-to-decision window)

Run 2026-10-30 against apple_v3_prereg.md, SHA-256 dc8719db5ce99d8a7ee885e273ed0b20de02df0d023c9cef714f4329af451bec (hashed before the run). Non-evidentiary: daily data, one parameter set, no costs.

## Population

- 77 cases entered the live arm (82 registered, register ruling_cases_wide.csv); 744 pooled non-decision opinion days against 4223 non-opinion days inside the argument-to-decision windows.
- Placebo arm: 77 cases, windows shifted back 364 days.

## Outcomes

| Arm | Cases | Opinion days | Non-opinion days | Mean z^2 ratio R | Permutation p (one-sided) | Share of days with abs(z) > 1, opinion vs non-opinion |
|---|---|---|---|---|---|---|
| Live | 77 | 744 | 4223 | 1.000 | 0.408 | 25% vs 26% |
| Placebo (same ticker, one year earlier) | 77 | 734 | 4244 | 0.825 | 0.938 | n/a |

## Decision rule as registered

- R above 1: met (R = 1.000).
- Permutation p below 0.1: not met (p = 0.408).
- R above the placebo R: met (placebo R = 0.825).
- At least 40 cases and 200 pooled opinion days: met (77 cases, 744 opinion days).

Registered outcome: INCONCLUSIVE.

## What this does not license

- Daily closes; the test bounds the answer, it does not establish it.
- Opinion days are the realised release dates, not the calendar as known at the start of each window. Source: SCDB release 2026_01, all decision types.
- The placebo controls weekday composition and the ticker's own variance, not other calendar events in the live window (June FOMC, index rebalances).
- Standardisation by the pre-argument residual sigma weights cases unequally where volatility regimes changed between estimation and window.

## Cases

| Case | Ticker | Argued | Decided | Days in W | Opinion days | Mean z^2 opinion | Mean z^2 non-opinion | Ratio | Placebo ratio | abs(z) > 1 opinion vs non | Sigma (daily) | Beta | Date checks | Price source |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Comcast Corp. v. Behrend | CMCSA | 2012-11-05 | 2013-03-27 | 96 | 16 | 0.61 | 0.85 | 0.709 | 0.908 | 19% vs 25% | 0.98% | 0.91 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | CMCSA: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Amgen Inc. v. Connecticut Retirement Plans and Trust Funds | AMGN | 2012-11-05 | 2013-02-27 | 76 | 11 | 0.97 | 0.96 | 1.012 | 0.876 | 27% vs 25% | 1.05% | 0.70 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | AMGN: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Association for Molecular Pathology v. Myriad Genetics | MYGN | 2013-04-15 | 2013-06-13 | 41 | 9 | 1.05 | 2.12 | 0.494 | 0.812 | 44% vs 31% | 1.73% | 0.82 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | MYGN: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| American Express Co. v. Italian Colors Restaurant | AXP | 2013-02-27 | 2013-06-20 | 78 | 17 | 0.60 | 0.88 | 0.680 | 0.743 | 29% vs 26% | 0.88% | 1.12 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | AXP: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Already LLC v. Nike Inc. | NKE | 2012-11-07 | 2013-01-09 | 41 | 5 | 0.32 | 1.38 | 0.234 | 1.943 | 0% vs 22% | 1.29% | 0.65 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | NKE: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Kirtsaeng v. John Wiley & Sons Inc. | WLY | 2012-10-29 | 2013-03-19 | 94 | 14 | 3.59 | 2.59 | 1.389 | 0.563 | 43% vs 30% | 1.06% | 0.79 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | WLY: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| PPL Corp. v. Commissioner of Internal Revenue | PPL | 2013-02-20 | 2013-05-20 | 61 | 13 | 0.49 | 1.26 | 0.389 | 0.996 | 8% vs 38% | 0.72% | 0.33 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | PPL: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Halliburton Co. v. Erica P. John Fund Inc. | HAL | 2014-03-05 | 2014-06-23 | 75 | 15 | 0.54 | 0.75 | 0.722 | 0.889 | 13% vs 27% | 1.17% | 1.41 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | HAL: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Medtronic Inc. v. Mirowski Family Ventures LLC | MDT | 2013-11-05 | 2014-01-22 | 51 | 7 | 0.73 | 1.21 | 0.606 | 0.272 | 29% vs 30% | 0.76% | 0.94 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | MDT: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Limelight Networks Inc. v. Akamai Technologies Inc. | AKAM | 2014-04-30 | 2014-06-02 | 21 | 3 | 0.23 | 0.45 | 0.517 | 0.472 | 0% vs 11% | 2.07% | 1.50 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | AKAM: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| POM Wonderful LLC v. Coca-Cola Co. | KO | 2014-04-21 | 2014-06-12 | 36 | 8 | 0.64 | 0.41 | 1.554 | 1.242 | 12% vs 11% | 0.77% | 0.81 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | KO: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Fifth Third Bancorp v. Dudenhoeffer | FITB | 2014-04-02 | 2014-06-25 | 57 | 12 | 1.02 | 1.81 | 0.564 | 1.048 | 42% vs 31% | 0.75% | 1.04 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | FITB: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| CTS Corp. v. Waldburger | CTS | 2014-04-23 | 2014-06-09 | 31 | 5 | 4.28 | 1.52 | 2.809 | 1.908 | 40% vs 38% | 1.57% | 1.44 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | CTS: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Heimeshoff v. Hartford Life & Accident Insurance Co. | HIG | 2013-10-15 | 2013-12-16 | 42 | 6 | 0.16 | 0.48 | 0.330 | 0.197 | 0% vs 14% | 1.12% | 1.64 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | HIG: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Teva Pharmaceuticals USA Inc. v. Sandoz Inc. | TEVA | 2014-10-15 | 2015-01-20 | 64 | 6 | 0.01 | 0.65 | 0.019 | 2.372 | 0% vs 21% | 1.46% | 0.94 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | TEVA: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Young v. United Parcel Service Inc. | UPS | 2014-12-03 | 2015-03-25 | 75 | 13 | 1.06 | 6.31 | 0.167 | 1.669 | 38% vs 21% | 0.55% | 0.92 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | UPS: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Gelboim v. Bank of America Corp. | BAC | 2014-12-09 | 2015-01-21 | 27 | 4 | 1.24 | 1.13 | 1.092 | 0.499 | 25% vs 17% | 1.08% | 1.19 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | BAC: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Bank of America N.A. v. Caulkett | BAC | 2015-03-24 | 2015-06-01 | 46 | 9 | 1.09 | 0.42 | 2.598 | 0.664 | 22% vs 8% | 1.13% | 1.29 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | BAC: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Commil USA LLC v. Cisco Systems Inc. | CSCO | 2015-03-31 | 2015-05-26 | 37 | 5 | 0.32 | 0.59 | 0.545 | 0.074 | 0% vs 19% | 1.04% | 1.02 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | CSCO: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Tibble v. Edison International | EIX | 2015-02-24 | 2015-05-18 | 57 | 12 | 0.86 | 1.24 | 0.697 | 0.724 | 33% vs 40% | 1.03% | 0.43 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | EIX: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Oneok Inc. v. Learjet Inc. | OKE | 2015-01-12 | 2015-04-21 | 67 | 14 | 4.42 | 1.80 | 2.459 | 1.046 | 71% vs 40% | 1.34% | 1.37 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | OKE: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| EEOC v. Abercrombie & Fitch Stores Inc. | ANF | 2015-02-25 | 2015-06-01 | 65 | 13 | 4.20 | 1.58 | 2.654 | 1.194 | 23% vs 33% | 2.33% | 1.00 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | ANF: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Alabama Department of Revenue v. CSX Transportation Inc. | CSX | 2014-12-09 | 2015-03-04 | 56 | 9 | 0.80 | 1.21 | 0.663 | 0.385 | 33% vs 32% | 0.98% | 1.05 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | CSX: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| T-Mobile South LLC v. City of Roswell | TMUS | 2014-11-10 | 2015-01-14 | 43 | 4 | 4.98 | 0.41 | 12.084 | 1.095 | 50% vs 8% | 2.00% | 1.02 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | TMUS: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Tyson Foods Inc. v. Bouaphakeo | TSN | 2015-11-10 | 2016-03-22 | 89 | 9 | 0.64 | 2.12 | 0.301 | 0.257 | 22% vs 25% | 1.47% | 0.87 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | TSN: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Americold Realty Trust v. ConAgra Foods Inc. | CAG | 2016-01-19 | 2016-03-07 | 32 | 3 | 0.82 | 0.64 | 1.273 | 0.065 | 33% vs 24% | 1.32% | 0.80 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | CAG: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Kirtsaeng v. John Wiley & Sons Inc. (II) | WLY | 2016-04-25 | 2016-06-16 | 36 | 9 | 0.63 | 1.99 | 0.317 | 3.045 | 11% vs 19% | 1.27% | 0.94 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | WLY: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Universal Health Services Inc. v. United States ex rel. Escobar | UHS | 2016-04-19 | 2016-06-16 | 40 | 10 | 0.64 | 0.32 | 1.986 | 1.031 | 20% vs 7% | 1.75% | 1.00 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | UHS: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Dollar General Corp. v. Mississippi Band of Choctaw Indians | DG | 2015-12-07 | 2016-06-23 | 136 | 26 | 0.77 | 1.58 | 0.486 | 0.808 | 15% vs 32% | 1.25% | 0.71 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | DG: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Samsung Electronics Co. v. Apple Inc. | AAPL | 2016-10-11 | 2016-12-06 | 38 | 1 | 0.04 | 0.68 | 0.060 | 2.024 | 0% vs 14% | 1.29% | 1.04 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | AAPL: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Bank of America Corp. v. City of Miami | BAC | 2016-11-08 | 2017-05-01 | 117 | 16 | 0.99 | 1.09 | 0.911 | 1.047 | 19% vs 24% | 1.30% | 1.73 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | BAC: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Microsoft Corp. v. Baker | MSFT | 2017-03-21 | 2017-06-12 | 56 | 12 | 0.42 | 0.58 | 0.731 | 0.486 | 17% vs 11% | 0.94% | 1.17 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | MSFT: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Goodyear Tire & Rubber Co. v. Haeger | GT | 2017-01-10 | 2017-04-18 | 66 | 9 | 0.26 | 0.70 | 0.370 | 1.054 | 11% vs 14% | 1.60% | 1.45 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | GT: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Sandoz Inc. v. Amgen Inc. | AMGN | 2017-04-26 | 2017-06-12 | 31 | 5 | 1.26 | 0.41 | 3.054 | 0.613 | 20% vs 12% | 1.22% | 1.22 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | AMGN: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Bristol-Myers Squibb Co. v. Superior Court of California | BMY | 2017-04-25 | 2017-06-19 | 37 | 6 | 1.02 | 0.27 | 3.734 | 1.347 | 17% vs 3% | 1.98% | 0.55 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | BMY: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Bolivarian Republic of Venezuela v. Helmerich & Payne International Drilling Co. | HP | 2016-11-02 | 2017-05-01 | 121 | 16 | 0.43 | 0.75 | 0.578 | 0.711 | 0% vs 11% | 2.32% | 1.71 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | HP: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| TC Heartland LLC v. Kraft Foods Group Brands LLC | KHC | 2017-03-27 | 2017-05-22 | 38 | 8 | 0.37 | 0.34 | 1.090 | 0.142 | 25% vs 10% | 1.24% | 0.87 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | KHC: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Ohio v. American Express Co. | AXP | 2018-02-26 | 2018-06-25 | 82 | 17 | 1.24 | 3.22 | 0.385 | 0.224 | 29% vs 42% | 0.69% | 1.16 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | AXP: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Digital Realty Trust Inc. v. Somers | DLR | 2017-11-28 | 2018-02-21 | 56 | 4 | 1.40 | 2.47 | 0.568 | 0.197 | 50% vs 50% | 1.21% | 0.81 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | DLR: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Merit Management Group LP v. FTI Consulting Inc. | FCN | 2017-11-06 | 2018-02-27 | 75 | 6 | 0.49 | 0.85 | 0.578 | 0.386 | 17% vs 12% | 1.67% | 1.08 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | FCN: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| South Dakota v. Wayfair Inc. | W | 2018-04-17 | 2018-06-21 | 45 | 8 | 0.55 | 0.92 | 0.603 | 0.289 | 12% vs 24% | 3.45% | 1.05 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | W: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Oil States Energy Services LLC v. Greene's Energy Group LLC | OIS | 2017-11-27 | 2018-04-24 | 100 | 12 | 1.31 | 1.26 | 1.042 | 0.829 | 33% vs 33% | 2.25% | 1.91 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | OIS: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| U.S. Bank N.A. v. Village at Lakeridge LLC | USB | 2017-10-31 | 2018-03-05 | 83 | 8 | 1.09 | 1.81 | 0.602 | 1.338 | 25% vs 33% | 0.71% | 1.23 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | USB: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Weyerhaeuser Co. v. United States Fish and Wildlife Service | WY | 2018-10-01 | 2018-11-27 | 39 | 1 | 5.15 | 5.20 | 0.989 | 2.457 | 100% vs 58% | 0.86% | 0.64 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | WY: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Henry Schein Inc. v. Archer & White Sales Inc. | HSIC | 2018-10-29 | 2019-01-08 | 46 | 4 | 1.29 | 0.51 | 2.513 | 0.206 | 50% vs 12% | 1.65% | 0.78 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | HSIC: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Apple Inc. v. Pepper | AAPL | 2018-11-26 | 2019-05-13 | 113 | 20 | 0.50 | 1.60 | 0.312 | 0.983 | 15% vs 27% | 1.16% | 1.13 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | AAPL: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Helsinn Healthcare S.A. v. Teva Pharmaceuticals USA Inc. | TEVA | 2018-12-04 | 2019-01-22 | 30 | 4 | 1.23 | 0.68 | 1.803 | 0.217 | 25% vs 12% | 2.59% | 1.30 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | TEVA: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Rimini Street Inc. v. Oracle USA Inc. | RMNI | 2019-01-14 | 2019-03-04 | 32 | 7 | 0.33 | 0.69 | 0.484 | 0.610 | 14% vs 28% | 4.06% | 0.66 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | RMNI: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Merck Sharp & Dohme Corp. v. Albrecht | MRK | 2019-01-07 | 2019-05-20 | 91 | 18 | 0.25 | 1.18 | 0.214 | 2.259 | 0% vs 26% | 1.01% | 0.67 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | MRK: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Home Depot U.S.A. Inc. v. Jackson | HD | 2019-01-15 | 2019-05-28 | 90 | 17 | 0.94 | 0.88 | 1.073 | 0.434 | 18% vs 25% | 0.93% | 1.01 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | HD: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Comcast Corp. v. National Association of African American-Owned Media | CMCSA | 2019-11-13 | 2020-03-23 | 87 | 8 | 4.10 | 1.80 | 2.281 | 0.297 | 50% vs 32% | 0.97% | 0.81 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | CMCSA: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Romag Fasteners Inc. v. Fossil Inc. | FOSL | 2020-01-14 | 2020-04-23 | 68 | 8 | 8.46 | 5.70 | 1.484 | 0.715 | 75% vs 48% | 3.65% | 1.93 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | FOSL: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Intel Corp. Investment Policy Committee v. Sulyma | INTC | 2019-12-04 | 2020-02-26 | 55 | 5 | 0.06 | 1.27 | 0.045 | 0.171 | 0% vs 12% | 1.42% | 1.25 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | INTC: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| United States Patent and Trademark Office v. Booking.com B.V. | BKNG | 2020-05-04 | 2020-06-30 | 39 | 10 | 3.88 | 1.77 | 2.197 | 0.124 | 30% vs 52% | 1.57% | 1.04 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | BKNG: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Thole v. U.S. Bank N.A. | USB | 2020-01-13 | 2020-06-01 | 95 | 14 | 23.09 | 15.64 | 1.476 | 0.599 | 79% vs 64% | 0.74% | 0.90 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | USB: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Google LLC v. Oracle America Inc. | GOOGL | 2020-10-07 | 2021-04-05 | 121 | 13 | 4.63 | 1.21 | 3.823 | 0.788 | 31% vs 31% | 1.14% | 0.97 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | GOOGL: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Ford Motor Co. v. Montana Eighth Judicial District Court | F | 2020-10-07 | 2021-03-25 | 115 | 10 | 1.07 | 0.82 | 1.311 | 3.271 | 40% vs 20% | 2.47% | 1.14 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | F: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Facebook Inc. v. Duguid | META | 2020-12-08 | 2021-04-01 | 77 | 11 | 0.80 | 0.71 | 1.118 | 0.826 | 36% vs 24% | 1.92% | 1.02 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | META: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Goldman Sachs Group Inc. v. Arkansas Teacher Retirement System | GS | 2021-03-29 | 2021-06-21 | 57 | 14 | 0.90 | 0.37 | 2.435 | 0.788 | 29% vs 14% | 1.88% | 1.26 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | GS: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| TransUnion LLC v. Ramirez | TRU | 2021-03-30 | 2021-06-25 | 60 | 16 | 0.91 | 0.39 | 2.302 | 1.100 | 19% vs 5% | 1.79% | 1.27 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | TRU: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| BP p.l.c. v. Mayor and City Council of Baltimore | BP | 2021-01-19 | 2021-05-17 | 81 | 12 | 0.73 | 0.83 | 0.881 | 2.049 | 33% vs 25% | 2.80% | 1.28 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | BP: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Marietta Memorial Hospital Employee Health Benefit Plan v. DaVita Inc. | DVA | 2022-03-01 | 2022-06-21 | 76 | 15 | 0.45 | 1.32 | 0.337 | 1.542 | 0% vs 33% | 1.58% | 0.59 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | DVA: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Southwest Airlines Co. v. Saxon | LUV | 2022-03-28 | 2022-06-06 | 47 | 7 | 1.19 | 1.53 | 0.777 | 0.240 | 29% vs 38% | 1.80% | 1.18 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | LUV: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| LeDure v. Union Pacific Railroad Co. | UNP | 2022-03-28 | 2022-04-28 | 21 | 3 | 0.67 | 2.94 | 0.228 | 2.809 | 33% vs 56% | 1.09% | 0.68 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | UNP: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Axon Enterprise Inc. v. Federal Trade Commission | AXON | 2022-11-07 | 2023-04-14 | 107 | 5 | 0.57 | 1.06 | 0.534 | 0.593 | 20% vs 13% | 2.49% | 1.47 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | AXON: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Mallory v. Norfolk Southern Railway Co. | NSC | 2022-11-08 | 2023-06-27 | 156 | 18 | 0.23 | 0.84 | 0.278 | 0.696 | 0% vs 24% | 1.35% | 0.78 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | NSC: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Gonzalez v. Google LLC | GOOGL | 2023-02-21 | 2023-05-18 | 60 | 8 | 2.06 | 1.26 | 1.637 | 0.749 | 50% vs 33% | 1.37% | 1.34 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | GOOGL: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Amgen Inc. v. Sanofi | AMGN | 2023-03-27 | 2023-05-18 | 36 | 5 | 0.31 | 0.86 | 0.357 | 0.536 | 0% vs 23% | 1.18% | 0.34 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | AMGN: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Coinbase Inc. v. Bielski | COIN | 2023-03-21 | 2023-06-23 | 64 | 13 | 0.36 | 0.88 | 0.414 | 0.755 | 8% vs 27% | 5.77% | 3.12 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | COIN: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Murray v. UBS Securities LLC | UBS | 2023-10-10 | 2024-02-08 | 82 | 1 | 2.43 | 0.80 | 3.031 | 0.150 | 100% vs 21% | 1.68% | 1.18 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | UBS: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Coinbase Inc. v. Suski | COIN | 2024-02-28 | 2024-05-23 | 59 | 8 | 1.74 | 1.01 | 1.715 | 1.380 | 50% vs 39% | 4.55% | 2.45 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | COIN: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Warner Chappell Music Inc. v. Nealy | WMG | 2024-02-21 | 2024-05-09 | 54 | 6 | 0.32 | 1.10 | 0.290 | 0.203 | 17% vs 27% | 1.78% | 0.87 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | WMG: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Starbucks Corp. v. McKinney | SBUX | 2024-04-23 | 2024-06-13 | 35 | 5 | 2.95 | 8.03 | 0.368 | 0.286 | 60% vs 33% | 1.22% | 0.89 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | SBUX: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Cantero v. Bank of America N.A. | BAC | 2024-02-27 | 2024-05-30 | 64 | 9 | 1.46 | 0.65 | 2.243 | 1.136 | 33% vs 16% | 1.40% | 1.22 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | BAC: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Waetzig v. Halliburton Energy Services Inc. | HAL | 2025-01-14 | 2025-02-26 | 28 | 5 | 0.80 | 1.27 | 0.635 | 0.706 | 20% vs 39% | 1.65% | 0.73 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | HAL: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| McLaughlin Chiropractic v. McKesson Corp. | MCK | 2025-01-21 | 2025-06-20 | 103 | 18 | 0.87 | 0.69 | 1.260 | 0.596 | 22% vs 18% | 1.65% | 0.05 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | MCK: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |
| Smith & Wesson Brands Inc. v. Estados Unidos Mexicanos | SWBI | 2025-03-04 | 2025-06-05 | 64 | 11 | 0.11 | 0.63 | 0.177 | 0.071 | 0% vs 15% | 2.93% | 0.46 | argued SCDB, Oyez agrees; decided SCDB, Oyez agrees | SWBI: cache (source=yfinance fetched=2026-10-30); SPY: cache (source=yfinance fetched=2026-10-30) |

## Run notes

- CMCSA_11-864: slip listing for OT12 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- AMGN_11-1085: slip listing for OT12 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- MYGN_12-398: slip listing for OT12 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- AXP_12-133: slip listing for OT12 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- NKE_11-982: slip listing for OT12 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- WLY_11-697: slip listing for OT12 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- PPL_12-43: slip listing for OT12 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- HAL_13-317: slip listing for OT13 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- MDT_12-1128: slip listing for OT13 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- AKAM_12-786: slip listing for OT13 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- KO_12-761: slip listing for OT13 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- FITB_12-751: slip listing for OT13 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- CTS_13-339: slip listing for OT13 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- HIG_12-729: slip listing for OT13 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- TEVA_13-854: slip listing for OT14 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- UPS_12-1226: slip listing for OT14 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- BAC_13-1174: slip listing for OT14 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- BAC_13-1421: slip listing for OT14 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- CSCO_13-896: slip listing for OT14 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- EIX_13-550: slip listing for OT14 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- OKE_13-271: slip listing for OT14 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- ANF_14-86: slip listing for OT14 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- CSX_13-553: slip listing for OT14 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- TMUS_13-975: slip listing for OT14 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- TSN_14-1146: slip listing for OT15 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- CAG_14-1382: slip listing for OT15 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- SYK_14-1520: absent from SCDB; case excluded
- WLY_15-375: slip listing for OT15 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- UHS_15-7: slip listing for OT15 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- DG_13-1496: slip listing for OT15 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- AAPL_15-777: slip listing for OT16 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- BAC_15-1111: slip listing for OT16 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- WFC_15-1112: absent from SCDB; case excluded
- MSFT_15-457: slip listing for OT16 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- GT_15-1406: slip listing for OT16 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- AMGN_15-1039: slip listing for OT16 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- BMY_16-466: slip listing for OT16 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- HP_15-423: slip listing for OT16 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- KHC_16-341: slip listing for OT16 not available for cross-check (no slip-opinion table with Date and Docket columns at https://www.supremecourt.g)
- AXP_16-1454: cross-check inside W, SCDB 17 opinion days, slip listing 14; in SCDB only [datetime.date(2018, 2, 27), datetime.date(2018, 3, 5), datetime.date(2018, 3, 20)]; in slip listing only []
- DLR_16-1276: cross-check inside W, SCDB 4 opinion days, slip listing 0; in SCDB only [datetime.date(2017, 12, 20), datetime.date(2018, 1, 8), datetime.date(2018, 1, 22), datetime.date(2018, 2, 20)]; in slip listing only []
- FCN_16-784: cross-check inside W, SCDB 6 opinion days, slip listing 0; in SCDB only [datetime.date(2017, 11, 8), datetime.date(2017, 12, 20), datetime.date(2018, 1, 8), datetime.date(2018, 1, 22), datetime.date(2018, 2, 20), datetime.date(2018, 2, 21)]; in slip listing only []
- W_17-494: cross-check inside W, SCDB 8 opinion days, slip listing 8; in SCDB only []; in slip listing only []
- OIS_16-712: cross-check inside W, SCDB 12 opinion days, slip listing 4; in SCDB only [datetime.date(2017, 12, 20), datetime.date(2018, 1, 8), datetime.date(2018, 1, 22), datetime.date(2018, 2, 20), datetime.date(2018, 2, 21), datetime.date(2018, 2, 27), datetime.date(2018, 3, 5), datetime.date(2018, 3, 20)]; in slip listing only []
- MUR_16-307: absent from SCDB; case excluded
- USB_15-1509: cross-check inside W, SCDB 8 opinion days, slip listing 0; in SCDB only [datetime.date(2017, 11, 6), datetime.date(2017, 11, 8), datetime.date(2017, 12, 20), datetime.date(2018, 1, 8), datetime.date(2018, 1, 22), datetime.date(2018, 2, 20), datetime.date(2018, 2, 21), datetime.date(2018, 2, 27)]; in slip listing only []
- WY_17-71: cross-check inside W, SCDB 1 opinion days, slip listing 1; in SCDB only []; in slip listing only []
- HSIC_17-1272: cross-check inside W, SCDB 4 opinion days, slip listing 4; in SCDB only []; in slip listing only []
- AAPL_17-204: cross-check inside W, SCDB 20 opinion days, slip listing 20; in SCDB only []; in slip listing only []
- TEVA_17-1229: cross-check inside W, SCDB 4 opinion days, slip listing 4; in SCDB only []; in slip listing only []
- RMNI_17-1625: cross-check inside W, SCDB 7 opinion days, slip listing 7; in SCDB only []; in slip listing only []
- MRK_17-290: cross-check inside W, SCDB 18 opinion days, slip listing 18; in SCDB only []; in slip listing only []
- HD_17-1471: cross-check inside W, SCDB 17 opinion days, slip listing 17; in SCDB only []; in slip listing only []
- CMCSA_18-1171: cross-check inside W, SCDB 8 opinion days, slip listing 8; in SCDB only []; in slip listing only []
- FOSL_18-1233: cross-check inside W, SCDB 8 opinion days, slip listing 8; in SCDB only []; in slip listing only []
- INTC_18-1116: cross-check inside W, SCDB 5 opinion days, slip listing 5; in SCDB only []; in slip listing only []
- BKNG_19-46: cross-check inside W, SCDB 10 opinion days, slip listing 10; in SCDB only []; in slip listing only []
- USB_17-1712: cross-check inside W, SCDB 14 opinion days, slip listing 14; in SCDB only []; in slip listing only []
- GOOGL_18-956: cross-check inside W, SCDB 13 opinion days, slip listing 14; in SCDB only []; in slip listing only [datetime.date(2020, 11, 25)]
- F_19-368: cross-check inside W, SCDB 10 opinion days, slip listing 11; in SCDB only []; in slip listing only [datetime.date(2020, 11, 25)]
- META_19-511: cross-check inside W, SCDB 11 opinion days, slip listing 11; in SCDB only []; in slip listing only []
- GS_20-222: cross-check inside W, SCDB 14 opinion days, slip listing 15; in SCDB only []; in slip listing only [datetime.date(2021, 4, 9)]
- TRU_20-297: cross-check inside W, SCDB 16 opinion days, slip listing 17; in SCDB only []; in slip listing only [datetime.date(2021, 4, 9)]
- HOLX_20-440: price data or market model failed (no price source worked for HOLX: yfinance: yfinance returned no rows | stooq: stooq returned no usable rows: '<!DOCTYPE ); case excluded
- BP_19-1189: cross-check inside W, SCDB 12 opinion days, slip listing 13; in SCDB only []; in slip listing only [datetime.date(2021, 4, 9)]
- DVA_20-1641: cross-check inside W, SCDB 15 opinion days, slip listing 16; in SCDB only []; in slip listing only [datetime.date(2022, 3, 23)]
- LUV_21-309: cross-check inside W, SCDB 7 opinion days, slip listing 7; in SCDB only []; in slip listing only []
- UNP_20-807: cross-check inside W, SCDB 3 opinion days, slip listing 3; in SCDB only []; in slip listing only []
- HLX_21-984: price data or market model failed (no price source worked for HLX: yfinance: yfinance returned no rows | stooq: stooq returned no usable rows: '<!DOCTYPE h); case excluded
- AXON_21-86: cross-check inside W, SCDB 5 opinion days, slip listing 5; in SCDB only []; in slip listing only []
- NSC_21-1168: cross-check inside W, SCDB 18 opinion days, slip listing 18; in SCDB only []; in slip listing only []
- GOOGL_21-1333: cross-check inside W, SCDB 8 opinion days, slip listing 8; in SCDB only []; in slip listing only []
- AMGN_21-757: cross-check inside W, SCDB 5 opinion days, slip listing 5; in SCDB only []; in slip listing only []
- COIN_22-105: cross-check inside W, SCDB 13 opinion days, slip listing 13; in SCDB only []; in slip listing only []
- UBS_22-660: cross-check inside W, SCDB 1 opinion days, slip listing 1; in SCDB only []; in slip listing only []
- COIN_23-3: cross-check inside W, SCDB 8 opinion days, slip listing 8; in SCDB only []; in slip listing only []
- WMG_22-1078: cross-check inside W, SCDB 6 opinion days, slip listing 6; in SCDB only []; in slip listing only []
- SBUX_23-367: cross-check inside W, SCDB 5 opinion days, slip listing 5; in SCDB only []; in slip listing only []
- BAC_22-529: cross-check inside W, SCDB 9 opinion days, slip listing 9; in SCDB only []; in slip listing only []
- HAL_23-971: cross-check inside W, SCDB 5 opinion days, slip listing 5; in SCDB only []; in slip listing only []
- MCK_23-1226: cross-check inside W, SCDB 18 opinion days, slip listing 21; in SCDB only []; in slip listing only [datetime.date(2025, 4, 4), datetime.date(2025, 4, 7), datetime.date(2025, 5, 16)]
- SWBI_23-1141: cross-check inside W, SCDB 11 opinion days, slip listing 14; in SCDB only []; in slip listing only [datetime.date(2025, 4, 4), datetime.date(2025, 4, 7), datetime.date(2025, 5, 16)]
- Permutations: 10000, seed 20261029. Estimation window: 2011-10-21 to 2012-10-17 for the first case; 250 trading days ending 10 trading days before argument for each.
