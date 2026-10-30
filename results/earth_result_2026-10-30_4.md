# Result: Project Earth (post-ruling drift in the litigant against a like-for-like control)

Run 2026-10-30 against earth_prereg.md, SHA-256 464c4ccfc0a89a22df4f58a38c4da514a50db910649e99714c61d27b71e3a5cf (hashed before the run). Non-evidentiary: daily closes, one parameter set, no costs.

## Population

- Universe: SCOTUS 1342 rulings (SCDB 2026_01); Federal Circuit 980 precedential opinions (CourtListener v4).
- Sides matched exactly to a listed company: 175 of 4539; events with usable price windows: 161 of 175; reacting (abs(z_0) >= 2, not earnings-adjacent, calm market): 11 (7% reaction rate); events in the difference (at least three control days): 11.

## Outcomes

| Statistic | Value |
|---|---|
| Mean signed CAR(+1,+5) after rulings, reacting events | +2.99% (n = 11) |
| Stouffer Z, one-sided p (rulings alone) | 2.65, 0.004 |
| Mean control drift (same companies' other abs(z) >= 2 days) | -0.20% |
| Mean difference, ruling minus control | +3.19% (n = 11) |
| Bootstrap p, one-sided | 0.004 |
| Reacting events continuing over +1 to +5 | 9 of 11 |
| cafc: events in difference, mean difference | 7, +1.99% |
| scotus: events in difference, mean difference | 4, +5.29% |
| General-application subset (opponent not a listed company or its subsidiary) | 11, +3.19% |

## Decision rule as registered

- Mean difference above zero: met (+3.19%).
- Bootstrap p below 0.05: met (p = 0.004).
- At least 40 events in the difference: not met (11).

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
| cafc | 2012-08-22 | AMKR | Amkor Technology, Inc. v. International Trade Commission | -5.43% | -2.77 | -4.90% | -0.19% | -3.38% | +3.38% | -1.19% (12) | +4.57% | not a company |
| cafc | 2012-08-24 | VZ | Activevideo Networks, Inc. v. Verizon Communications, Inc. | +1.82% | +2.29 | -4.17% | -1.02% | -0.70% | -0.70% | +0.81% (17) | -1.51% | unresolved (none) |
| cafc | 2012-08-24 | LLY | Eli Lilly and Co. v. Teva Parenteral Medicines, Inc. | +3.00% | +3.36 | -0.45% | +1.59% | +2.24% | +2.24% | -0.68% (19) | +2.92% | unresolved (none) |
| cafc | 2012-12-05 | CMI | Cummins, Inc. v. Tas Distributing Co., Inc. | +3.80% | +3.07 | -3.20% | -1.41% | +2.27% | +2.27% | -1.73% (9) | +4.01% | unresolved (none) |
| cafc | 2013-05-03 | F | Ford Motor Co. v. United States | +1.95% | +2.00 | -0.62% | +1.55% | +0.43% | +0.43% | +1.72% (19) | -1.28% | not a company |
| cafc | 2013-05-29 | CL | Asher v. Colgate-Palmolive Co. | -2.97% | -3.89 | +0.26% | -0.19% | -1.19% | +1.19% | +0.02% (19) | +1.17% | not a company |
| scotus | 2013-06-13 | MYGN | ASSOCIATION FOR MOLECULAR PATHOLOGY, et al., PETITIONERS v.  | -7.10% | -3.33 | +10.26% | -14.45% | -17.77% | +17.77% | -1.44% (20) | +19.21% | unresolved (none) |
| cafc | 2013-09-24 | RMBS | Rambus Inc. v. Rea | +4.21% | +2.06 | +4.36% | -0.81% | +4.23% | +4.23% | +0.16% (19) | +4.07% | not a company |
| scotus | 2018-06-25 | AXP | OHIO v. AMERICAN EXPRESS CO. | +2.83% | +2.24 | -0.42% | -0.59% | +0.07% | +0.07% | -0.11% (18) | +0.18% | not a company |

## Run notes

- 14 matched sides excluded for data reasons: day 0 not a trading day or window incomplete (12); no price history (2)
- Party-map bases: not a company (2546); unresolved (none) (1579); listed (175); ex21 parent (85); unresolved (parent not listed) (79); unresolved (ambiguous) (71); unresolved (error) (4)
- Bootstrap: 10,000 draws over events, seed 20261030; controls within 252 trading days, ten-day gap around rulings, earnings-adjacent and non-calm days excluded.
