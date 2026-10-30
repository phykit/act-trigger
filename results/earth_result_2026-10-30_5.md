# Result: Project Earth (post-ruling drift in the litigant against a like-for-like control)

Run 2026-10-30 against earth_prereg.md, SHA-256 464c4ccfc0a89a22df4f58a38c4da514a50db910649e99714c61d27b71e3a5cf (hashed before the run). Non-evidentiary: daily closes, one parameter set, no costs.

## Population

- Universe: SCOTUS 1342 rulings (SCDB 2026_01); Federal Circuit 453 precedential opinions (CourtListener v4).
- Sides matched exactly to a listed company: 150 of 3542; events with usable price windows: 148 of 150; reacting (abs(z_0) >= 2, not earnings-adjacent, calm market): 6 (4% reaction rate); events in the difference (at least three control days): 6.

## Outcomes

| Statistic | Value |
|---|---|
| Mean signed CAR(+1,+5) after rulings, reacting events | +2.89% (n = 6) |
| Stouffer Z, one-sided p (rulings alone) | 1.41, 0.080 |
| Mean control drift (same companies' other abs(z) >= 2 days) | -0.22% |
| Mean difference, ruling minus control | +3.11% (n = 6) |
| Bootstrap p, one-sided | 0.190 |
| Reacting events continuing over +1 to +5 | 4 of 6 |
| cafc: events in difference, mean difference | 2, -1.24% |
| scotus: events in difference, mean difference | 4, +5.29% |
| General-application subset (opponent not a listed company or its subsidiary) | 6, +3.11% |

## Decision rule as registered

- Mean difference above zero: met (+3.11%).
- Bootstrap p below 0.05: not met (p = 0.190).
- At least 40 events in the difference: not met (6).

Registered outcome: UNSCORABLE.

## What this does not license

- Exact-name matching: subsidiaries and differently registered names are not here (Project Moon).
- Daily closes; Federal Circuit release times are untimestamped; rolling estimates lag a day.
- The control is any large idiosyncratic move not excluded by the screens; events are treated as independent.

## Reacting events

| Court | Date | Ticker | Case | AR(0) | z(0) | CAR(-5,-1) | CAR(+1,+1) | CAR(+1,+5) | Signed | Control mean (n) | Difference | Opponent |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scotus | 2006-03-01 | ITW | ILLINOIS TOOL WORKS INC., et al. v. INDEPENDENT INK, INC. | +1.95% | +2.04 | -1.83% | +0.33% | +2.85% | +2.85% | -0.28% (20) | +3.12% | unresolved (none) |
| scotus | 2007-04-02 | DUK | ENVIRONMENTAL DEFENSE, et al. v. DUKE ENERGY CORPORATION, et | +1.92% | +2.37 | +0.30% | -0.44% | -0.81% | -0.81% | +0.55% (24) | -1.37% | not a company |
| scotus | 2013-06-13 | MYGN | ASSOCIATION FOR MOLECULAR PATHOLOGY, et al., PETITIONERS v.  | -7.10% | -3.33 | +10.26% | -14.45% | -17.77% | +17.77% | -1.44% (20) | +19.21% | unresolved (none) |
| cafc | 2015-01-09 | WDC | Guzik Technical Enterprises, Inc. v. Western Digital Corp. | +2.58% | +2.44 | -0.72% | -0.82% | -4.04% | -4.04% | +0.29% (16) | -4.33% | unresolved (none) |
| cafc | 2015-10-09 | NTAP | Summit Data Systems LLC v. NetApp Inc. | +2.76% | +2.12 | +6.82% | +0.63% | +1.51% | +1.51% | -0.34% (9) | +1.85% | unresolved (none) |
| scotus | 2018-06-25 | AXP | OHIO v. AMERICAN EXPRESS CO. | +2.83% | +2.24 | -0.42% | -0.59% | +0.07% | +0.07% | -0.11% (18) | +0.18% | not a company |

## Run notes

- 2 matched sides excluded for data reasons: day 0 not a trading day or window incomplete (2)
- Party-map bases: not a company (2024); unresolved (none) (1190); listed (150); ex21 parent (70); unresolved (parent not listed) (65); unresolved (ambiguous) (37); unresolved (error) (6)
- Bootstrap: 10,000 draws over events, seed 20261030; controls within 252 trading days, ten-day gap around rulings, earnings-adjacent and non-calm days excluded.
