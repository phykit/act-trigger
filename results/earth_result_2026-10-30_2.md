# Result: Project Earth (post-ruling drift in the litigant against a like-for-like control)

Run 2026-10-30 against earth_prereg.md, SHA-256 464c4ccfc0a89a22df4f58a38c4da514a50db910649e99714c61d27b71e3a5cf (hashed before the run). Non-evidentiary: daily closes, one parameter set, no costs.

## Population

- Universe: SCOTUS 1342 rulings (SCDB 2026_01); Federal Circuit 0 precedential opinions (unavailable: _courtlistener_cafc: CourtListener status 401: {"detail":"Authentication credentials were not provided."} | _cafc_table: HTTPSConnectionPool(host='cafc.uscourts.gov', port=443): Max retries exceeded with url: /home/case-information/opinions-orders/ (Caused by SSLError(SSLCertVerif).
- Sides matched exactly to a listed company: 79 of 2682; events with usable price windows: 79 of 79; reacting (abs(z_0) >= 2, not earnings-adjacent, calm market): 4 (5% reaction rate); events in the difference (at least three control days): 4.

## Outcomes

| Statistic | Value |
|---|---|
| Mean signed CAR(+1,+5) after rulings, reacting events | +4.97% (n = 4) |
| Stouffer Z, one-sided p (rulings alone) | 2.32, 0.010 |
| Mean control drift (same companies' other abs(z) >= 2 days) | -0.32% |
| Mean difference, ruling minus control | +5.29% (n = 4) |
| Bootstrap p, one-sided | 0.072 |
| Reacting events continuing over +1 to +5 | 3 of 4 |
| scotus: events in difference, mean difference | 4, +5.29% |
| General-application subset (opponent not a listed company or its subsidiary) | 4, +5.29% |

## Decision rule as registered

- Mean difference above zero: met (+5.29%).
- Bootstrap p below 0.05: not met (p = 0.072).
- At least 40 events in the difference: not met (4).

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
| scotus | 2018-06-25 | AXP | OHIO v. AMERICAN EXPRESS CO. | +2.83% | +2.24 | -0.42% | -0.59% | +0.07% | +0.07% | -0.11% (18) | +0.18% | not a company |

## Run notes

- No data exclusions.
- Party-map bases: not a company (1712); unresolved (none) (809); listed (79); ex21 parent (40); unresolved (parent not listed) (20); unresolved (ambiguous) (18); unresolved (error) (4)
- Bootstrap: 10,000 draws over events, seed 20261030; controls within 252 trading days, ten-day gap around rulings, earnings-adjacent and non-calm days excluded.
