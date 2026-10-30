# Result: Project Fire (spillover of a ruling to the litigant's industry)

Run 2026-10-30 against fire_prereg.md, SHA-256 f1ebe116062b8f01c9bd192842803cd3eea523a7bb9af97643a392cc59e28a13 (hashed before the run). Non-evidentiary: daily closes, equal-weighted SIC baskets, one parameter set, no costs.

## Population

- Universe: SCOTUS 1342 rulings (SCDB 2026_01); Federal Circuit 0 precedential opinions (unavailable: _courtlistener_cafc: CourtListener status 401: {"detail":"Authentication credentials were not provided."} | _cafc_table: HTTPSConnectionPool(host='cafc.uscourts.gov', port=443): Max retries exceeded with url: /home/case-information/opinions-orders/ (Caused by SSLError(SSLCertVerif).
- Candidate events (Earth reacting, general application, at least three litigant control days): 1; with a usable peer basket: 1; in the difference: 1.

## Outcomes

| Statistic | Value |
|---|---|
| Mean signed basket reaction on day 0 | -0.13% (n = 1), bootstrap p 1.000 |
| Mean signed basket CAR(+1,+10) after rulings, F | -7.24%, bootstrap p 1.000 |
| Mean difference, ruling minus the basket's drift after the litigant's other big days | -6.87% (n = 1) |
| Bootstrap p, one-sided | 1.000 |
| scotus: events in difference, mean difference | 1, -6.87% |

## Decision rule as registered

- Mean difference above zero: not met (-6.87%).
- Bootstrap p below 0.05: not met (p = 1.000).
- At least 30 events in the difference: not met (1).

Registered outcome: UNSCORABLE.

## What this does not license

- Four-digit SIC baskets, equal-weighted, capped at 40 names in ascending CIK order; not the investable sector.
- The sign convention assumes peers sit on the litigant's side of the rule.
- Events share decision days and peers; treated as independent.

## Events

| Court | Date | Litigant | SIC | Peers | Litigant z(0) | Basket AR(0) signed | Basket CAR(+1,+10) signed | Control mean (n) | Difference |
|---|---|---|---|---|---|---|---|---|---|
| scotus | 2018-06-25 | AXP | 6199 | 34 | +2.24 | -0.13% | -7.24% | -0.37% (18) | -6.87% |

## Run notes

- None.
- Bootstrap: 10,000 draws, seed 20261030.
