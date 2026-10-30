# Result: Project Fire (spillover of a ruling to the litigant's industry)

Run 2026-10-30 against fire_prereg.md, SHA-256 f1ebe116062b8f01c9bd192842803cd3eea523a7bb9af97643a392cc59e28a13 (hashed before the run). Non-evidentiary: daily closes, equal-weighted SIC baskets, one parameter set, no costs.

## Population

- Universe: SCOTUS 1342 rulings (SCDB 2026_01); Federal Circuit 980 precedential opinions (CourtListener v4).
- Candidate events (Earth reacting, general application, at least three litigant control days): 11; with a usable peer basket: 9; in the difference: 9.

## Outcomes

| Statistic | Value |
|---|---|
| Mean signed basket reaction on day 0 | +0.44% (n = 9), bootstrap p 0.054 |
| Mean signed basket CAR(+1,+10) after rulings, F | +0.53%, bootstrap p 0.373 |
| Mean difference, ruling minus the basket's drift after the litigant's other big days | +0.54% (n = 9) |
| Bootstrap p, one-sided | 0.373 |
| cafc: events in difference, mean difference | 6, +1.96% |
| scotus: events in difference, mean difference | 3, -2.29% |

## Decision rule as registered

- Mean difference above zero: met (+0.54%).
- Bootstrap p below 0.05: not met (p = 0.373).
- At least 30 events in the difference: not met (9).

Registered outcome: UNSCORABLE.

## What this does not license

- Four-digit SIC baskets, equal-weighted, capped at 40 names in ascending CIK order; not the investable sector.
- The sign convention assumes peers sit on the litigant's side of the rule.
- Events share decision days and peers; treated as independent.

## Events

| Court | Date | Litigant | SIC | Peers | Litigant z(0) | Basket AR(0) signed | Basket CAR(+1,+10) signed | Control mean (n) | Difference |
|---|---|---|---|---|---|---|---|---|---|
| scotus | 2007-04-02 | DUK | 4931 | 14 | +2.37 | +1.44% | -1.89% | +0.61% (24) | -2.49% |
| cafc | 2012-08-22 | AMKR | 3674 | 37 | -2.77 | +0.94% | -1.10% | +0.01% (12) | -1.10% |
| cafc | 2012-08-24 | VZ | 4813 | 24 | +2.29 | +0.02% | +7.23% | -1.22% (17) | +8.45% |
| cafc | 2012-08-24 | LLY | 2834 | 37 | +3.36 | +1.97% | +0.15% | +0.37% (19) | -0.22% |
| cafc | 2013-05-03 | F | 3711 | 12 | +2.00 | -0.63% | +8.66% | +1.30% (19) | +7.36% |
| cafc | 2013-05-29 | CL | 2844 | 6 | -3.89 | -0.27% | -5.04% | -0.32% (19) | -4.71% |
| scotus | 2013-06-13 | MYGN | 2835 | 11 | -3.33 | -0.34% | +2.34% | -0.15% (20) | +2.49% |
| cafc | 2013-09-24 | RMBS | 3674 | 38 | +2.06 | +0.98% | +1.64% | -0.35% (19) | +1.99% |
| scotus | 2018-06-25 | AXP | 6199 | 34 | +2.24 | -0.13% | -7.24% | -0.37% (18) | -6.87% |

## Run notes

- ITW 2006-03-01: only 3 peers with data in SIC 3560; event excluded
- CMI 2012-12-05: only 4 peers with data in SIC 3510; event excluded
- Bootstrap: 10,000 draws, seed 20261030.
