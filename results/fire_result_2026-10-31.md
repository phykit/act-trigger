# Result: Project Fire (spillover of a ruling to the litigant's industry)

Run 2026-10-31 against fire_prereg.md, SHA-256 f1ebe116062b8f01c9bd192842803cd3eea523a7bb9af97643a392cc59e28a13 (hashed before the run). Non-evidentiary: daily closes, equal-weighted SIC baskets, one parameter set, no costs.

## Population

- Universe: SCOTUS 1342 rulings (SCDB 2026_01); Federal Circuit 2421 precedential opinions (GovInfo USCOURTS ca13).
- Candidate events (Earth reacting, general application, at least three litigant control days): 30; with a usable peer basket: 23; in the difference: 23.

## Outcomes

| Statistic | Value |
|---|---|
| Mean signed basket reaction on day 0 | +0.00% (n = 23), bootstrap p 0.460 |
| Mean signed basket CAR(+1,+10) after rulings, F | +1.56%, bootstrap p 0.026 |
| Mean difference, ruling minus the basket's drift after the litigant's other big days | +1.54% (n = 23) |
| Bootstrap p, one-sided | 0.035 |
| cafc: events in difference, mean difference | 20, +2.11% |
| scotus: events in difference, mean difference | 3, -2.29% |

## Decision rule as registered

- Mean difference above zero: met (+1.54%).
- Bootstrap p below 0.05: met (p = 0.035).
- At least 30 events in the difference: not met (23).

Registered outcome: UNSCORABLE.

## What this does not license

- Four-digit SIC baskets, equal-weighted, capped at 40 names in ascending CIK order; not the investable sector.
- The sign convention assumes peers sit on the litigant's side of the rule.
- Events share decision days and peers; treated as independent.

## Events

| Court | Date | Litigant | SIC | Peers | Litigant z(0) | Basket AR(0) signed | Basket CAR(+1,+10) signed | Control mean (n) | Difference |
|---|---|---|---|---|---|---|---|---|---|
| scotus | 2007-04-02 | DUK | 4931 | 14 | +2.37 | +1.44% | -1.89% | +0.61% (24) | -2.49% |
| cafc | 2013-05-03 | F | 3711 | 12 | +2.00 | -0.63% | +8.66% | +1.30% (19) | +7.36% |
| scotus | 2013-06-13 | MYGN | 2835 | 11 | -3.33 | -0.34% | +2.34% | -0.15% (20) | +2.49% |
| cafc | 2013-09-24 | RMBS | 3674 | 38 | +2.06 | +0.98% | +1.64% | -0.25% (16) | +1.88% |
| cafc | 2014-05-05 | SAP | 7372 | 36 | -2.21 | +0.73% | +2.17% | -1.19% (21) | +3.36% |
| cafc | 2014-05-05 | SAP | 7372 | 36 | -2.21 | +0.71% | +1.94% | -0.96% (21) | +2.90% |
| cafc | 2014-06-06 | INTC | 3674 | 38 | +2.03 | +0.12% | +2.13% | -0.02% (15) | +2.15% |
| cafc | 2014-07-11 | XRX | 3577 | 11 | +2.11 | +0.54% | +2.34% | -0.21% (26) | +2.55% |
| cafc | 2015-07-09 | SAP | 7372 | 38 | +2.14 | +0.63% | -2.95% | -0.41% (20) | -2.54% |
| cafc | 2016-01-06 | F | 3711 | 13 | -3.17 | +1.15% | +6.38% | +0.19% (19) | +6.19% |
| cafc | 2016-06-21 | IMMR | 3577 | 11 | +5.81 | +0.24% | -2.84% | -0.28% (15) | -2.56% |
| cafc | 2016-06-27 | T | 4813 | 26 | +3.17 | -0.77% | +3.46% | +1.17% (29) | +2.29% |
| cafc | 2016-11-09 | MDT | 3845 | 16 | -3.78 | +0.56% | -0.64% | +1.00% (16) | -1.64% |
| cafc | 2017-01-26 | CPIX | 2834 | 38 | +3.86 | -0.19% | +2.19% | -0.42% (33) | +2.61% |
| cafc | 2017-04-04 | ST | 3823 | 13 | -2.88 | +0.03% | -1.10% | -0.33% (18) | -0.77% |
| scotus | 2018-06-25 | AXP | 6199 | 34 | +2.24 | -0.13% | -7.24% | -0.37% (18) | -6.87% |
| cafc | 2019-03-15 | NAII | 2833 | 21 | +2.33 | -0.49% | -1.47% | +4.30% (25) | -5.77% |
| cafc | 2019-06-12 | MU | 3674 | 38 | -2.51 | +1.16% | -0.25% | +0.12% (12) | -0.37% |
| cafc | 2019-12-16 | AMGN | 2836 | 38 | +2.91 | -0.13% | +5.19% | -0.52% (14) | +5.71% |
| cafc | 2020-08-03 | ILMN | 3826 | 17 | +2.03 | -0.34% | +0.54% | -2.54% (9) | +3.08% |
| cafc | 2023-03-13 | EW | 3842 | 23 | +2.11 | -1.14% | -1.55% | -0.10% (14) | -1.46% |
| cafc | 2025-01-27 | AAPL | 3571 | 6 | +3.78 | -5.16% | +9.41% | -0.48% (18) | +9.89% |
| cafc | 2025-06-16 | ROKU | 4841 | 11 | +2.59 | +1.13% | +7.44% | +0.00% (13) | +7.43% |

## Run notes

- ITW 2006-03-01: only 3 peers with data in SIC 3560; event excluded
- AAPL 2014-09-10: only 3 peers with data in SIC 3571; event excluded
- AAPL 2015-12-15: only 3 peers with data in SIC 3571; event excluded
- AAPL 2015-12-15: only 3 peers with data in SIC 3571; event excluded
- AAPL 2017-05-05: only 3 peers with data in SIC 3571; event excluded
- GPRO 2018-07-27: only 3 peers with data in SIC 3861; event excluded
- HON 2019-10-01: only 4 peers with data in SIC 3724; event excluded
- Bootstrap: 10,000 draws, seed 20261030.
