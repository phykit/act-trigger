# Result: Project Storm (contagion to companies that disclosed exposure to the case)

Run 2026-10-31 against storm_prereg.md, SHA-256 dc9dfa628755037438d27ce746c645c3544ab84d8caaeb3af8909d88883335c7 (hashed before the run); cost gate prereg/cost_gate_prereg.md. Non-evidentiary: daily closes, equal-weighted baskets, one parameter set.

## Population

- Universe: SCOTUS 1342 rulings (SCDB 2026_01); Federal Circuit 2421 precedential opinions (GovInfo USCOURTS ca13).
- Rulings: searched (3722); out of scope (government or no usable caption) (41).
- With at least 3 exposed listed non-party companies: 592; with a usable basket window: 591.

## Outcomes

| Statistic | Value |
|---|---|
| Primary: mean basket abs(z_0) on ruling day | 0.764 (n = 591) |
| Null: mean abs(z) on random prior days | 0.778 |
| One-sided p | 0.654 |
| Reacting rulings (basket abs(z_0) >= 2): mean basket drift | +0.44% (n = 36), bootstrap p 0.181 |
| Cost gate on basket drift: median cost, mean net | +2.01%, -1.28% (not passed) |
| Median exposed names per ruling | 15 |
| cafc: rulings, mean abs(z_0) | 335, 0.741 |
| scotus: rulings, mean abs(z_0) | 256, 0.794 |

## Decision rule as registered

- At least 20 rulings: met (591).
- Support: p below 0.05; kill: observed at or below the null mean.
- Drift claim (separate): not made (needs at least 15 reacting rulings, drift above zero with p below 0.1, and the cost gate).

Registered outcome: KILL.

## What this does not license

- Two-word caption terms can match unrelated text; long-cited leading cases inflate exposure.
- The paired comparison with Fire's SIC baskets is not computed in this run and is reported separately.

