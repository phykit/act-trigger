# Result: Project Death (pair trades where both sides are listed)

Run 2026-10-31 against death_prereg.md, SHA-256 6599a20ef77840c5233a2c77133012863620968d5267521a545e57e72c9402ba (hashed before the run); cost gate prereg/cost_gate_prereg.md. Non-evidentiary: daily closes, one parameter set, no borrow cost.

## Population

- Universe: SCOTUS 1342 rulings (SCDB 2026_01); Federal Circuit 2421 precedential opinions (GovInfo USCOURTS ca13).
- Rulings with both sides listed: 38; with usable windows: 35; reacting pairs (abs(P_0)/sigma >= 2.0): 5; with at least one control day: 5.

## Outcomes

| Statistic | Value |
|---|---|
| Mean pair drift, reacting pairs (gross) | +34.23% (n = 5) |
| Mean control drift | +0.24% |
| Primary: mean pair drift minus control | +33.98% (n = 5) |
| Bootstrap p, one-sided | 0.000 |
| Cost gate: median round-trip cost (both legs) | +3.47% |
| Cost gate: mean net pair drift | +29.79% (passed; 0 without a cost estimate) |
| Mirror: corr(winner AR_0, minus loser AR_0); share moving opposite ways on day 0 | -0.63; 0 of 5 |

## Decision rule as registered

- At least 15 reacting pairs: not met (5).
- Primary above zero, p below 0.1, and the cost gate passed.

Registered outcome: UNSCORABLE.

## What this does not license

- Exact-name matching on both sides; equal-value legs; no borrow cost or short availability.
- The market's winner is the day-0 leader, not the formal winner.

