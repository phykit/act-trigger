# Result: Project Earth (post-ruling drift in the litigant against a like-for-like control)

Run 2026-10-30 against earth_prereg.md, SHA-256 464c4ccfc0a89a22df4f58a38c4da514a50db910649e99714c61d27b71e3a5cf (hashed before the run). Non-evidentiary: daily closes, one parameter set, no costs.

## Population

- Universe: SCOTUS 1342 rulings (SCDB 2026_01); Federal Circuit 0 precedential opinions (unavailable: _courtlistener_cafc: CourtListener status 401: {"detail":"Authentication credentials were not provided."} | _cafc_table: HTTPSConnectionPool(host='cafc.uscourts.gov', port=443): Max retries exceeded with url: /home/case-information/opinions-orders/ (Caused by SSLError(SSLCertVerif).
- Sides matched exactly to a listed company: 62 of 2682; events with usable price windows: 62 of 62; reacting (abs(z_0) >= 2, not earnings-adjacent, calm market): 1 (2% reaction rate); events in the difference (at least three control days): 1.

## Outcomes

| Statistic | Value |
|---|---|
| Mean signed CAR(+1,+5) after rulings, reacting events | +0.07% (n = 1) |
| Stouffer Z, one-sided p (rulings alone) | 0.03, 0.490 |
| Mean control drift (same companies' other abs(z) >= 2 days) | -0.11% |
| Mean difference, ruling minus control | +0.18% (n = 1) |
| Bootstrap p, one-sided | 0.000 |
| Reacting events continuing over +1 to +5 | 1 of 1 |
| scotus: events in difference, mean difference | 1, +0.18% |
| General-application subset (opponent not a listed company or its subsidiary) | 1, +0.18% |

## Decision rule as registered

- Mean difference above zero: met (+0.18%).
- Bootstrap p below 0.05: met (p = 0.000).
- At least 40 events in the difference: not met (1).

Registered outcome: UNSCORABLE.

## What this does not license

- Exact-name matching: subsidiaries and differently registered names are not here (Project Moon).
- Daily closes; Federal Circuit release times are untimestamped; rolling estimates lag a day.
- The control is any large idiosyncratic move not excluded by the screens; events are treated as independent.

## Reacting events

| Court | Date | Ticker | Case | AR(0) | z(0) | CAR(-5,-1) | CAR(+1,+1) | CAR(+1,+5) | Signed | Control mean (n) | Difference | Opponent |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scotus | 2018-06-25 | AXP | OHIO v. AMERICAN EXPRESS CO. | +2.83% | +2.24 | -0.42% | -0.59% | +0.07% | +0.07% | -0.11% (18) | +0.18% | not a company |

## Run notes

- No data exclusions.
- Party-map bases: not a company (1590); unresolved (none) (949); listed (62); ex21 parent (38); unresolved (parent not listed) (20); unresolved (ambiguous) (18); unresolved (error) (5)
- Bootstrap: 10,000 draws over events, seed 20261030; controls within 252 trading days, ten-day gap around rulings, earnings-adjacent and non-calm days excluded.
