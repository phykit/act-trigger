# Result: Project Fire (spillover of a ruling to the litigant's industry)

Run 2026-10-30 against fire_prereg.md, SHA-256 f1ebe116062b8f01c9bd192842803cd3eea523a7bb9af97643a392cc59e28a13 (hashed before the run). Non-evidentiary: daily closes, equal-weighted SIC baskets, one parameter set, no costs.

## Population

- Universe: SCOTUS 1342 rulings (SCDB 2026_01); Federal Circuit 453 precedential opinions (CourtListener v4).
- Candidate events (Earth reacting, general application, at least three litigant control days): 6; with a usable peer basket: 3; in the difference: 3.

## Outcomes

| Statistic | Value |
|---|---|
| Mean signed basket reaction on day 0 | +0.32% (n = 3), bootstrap p 0.300 |
| Mean signed basket CAR(+1,+10) after rulings, F | -2.26%, bootstrap p 0.851 |
| Mean difference, ruling minus the basket's drift after the litigant's other big days | -2.29% (n = 3) |
| Bootstrap p, one-sided | 0.851 |
| scotus: events in difference, mean difference | 3, -2.29% |

## Decision rule as registered

- Mean difference above zero: not met (-2.29%).
- Bootstrap p below 0.05: not met (p = 0.851).
- At least 30 events in the difference: not met (3).

Registered outcome: UNSCORABLE.

## What this does not license

- Four-digit SIC baskets, equal-weighted, capped at 40 names in ascending CIK order; not the investable sector.
- The sign convention assumes peers sit on the litigant's side of the rule.
- Events share decision days and peers; treated as independent.

## Events

| Court | Date | Litigant | SIC | Peers | Litigant z(0) | Basket AR(0) signed | Basket CAR(+1,+10) signed | Control mean (n) | Difference |
|---|---|---|---|---|---|---|---|---|---|
| scotus | 2007-04-02 | DUK | 4931 | 14 | +2.37 | +1.44% | -1.89% | +0.61% (24) | -2.49% |
| scotus | 2013-06-13 | MYGN | 2835 | 11 | -3.33 | -0.34% | +2.34% | -0.15% (20) | +2.49% |
| scotus | 2018-06-25 | AXP | 6199 | 34 | +2.24 | -0.13% | -7.24% | -0.37% (18) | -6.87% |

## Run notes

- ITW 2006-03-01: only 3 peers with data in SIC 3560; event excluded
- WDC 2015-01-09: only 3 peers with data in SIC 3572; event excluded
- NTAP 2015-10-09: only 3 peers with data in SIC 3572; event excluded
- Bootstrap: 10,000 draws, seed 20261030.
