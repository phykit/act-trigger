# Pre-registration: Project Void (the quantification gap)

Frozen before any result under this specification was computed. 30 October 2026. Adopts `prereg/cost_gate_prereg.md`.

## Hypothesis

The framework paper counts a ruling whose economic consequence is not stated in money as more complex: the market must estimate the number itself. If complexity slows incorporation (Metal's thesis), rulings with no stated figure should keep moving after day 0 more than rulings with one.

Registered sign: positive. Mean signed drift is higher for events with no stated figure (D = 0) than for events with one (D = 1), holding the coded stakes otherwise equal.

## Population

The events coded under `prereg/water_v3_prereg.md`: the 37 Moon events and the Earth reacting events from the first Earth run whose universe contains Federal Circuit opinions for the whole of 2012 to June 2025. Void uses Water's coding and adds no coding of its own.

## Definitions

1. D: component D (figure stated) from Water's coder 3, the API coder. Coders 1, 2 and 2b are secondary.
2. Signed drift, as Water: Moon S = direction x CAR(+1,+5); Earth sign(AR_0) x CAR(+1,+5).
3. Stakes stratum: B + C from the same coder (0, 1 or 2). Component A is excluded from the stratum because a missing figure forces A to 0, so A and D are not separable.

## Statistics

1. Primary: mean signed drift of D = 0 events minus D = 1 events; one-sided permutation p with D labels permuted within stakes strata (so stakes cannot drive the difference), 10,000 draws, seed 20261030.
2. Tradeable statistic (for the cost gate): mean signed drift of D = 0 events, the position being long the parent or party in the direction of the day-0 move (Earth) or of the formal outcome (Moon) from the close of day 0 to the close of day +5.
3. Secondary: the unstratified difference; each population separately; each coder separately; mean abs(z_0) by D (does the market react less on the day when no figure is stated, which is the mechanism).

## Decision rule (stated before the run)

- Support: primary difference above zero, permutation p below 0.10, at least 10 events in each of D = 0 and D = 1, and the cost gate passed.
- SUPPORT (GROSS ONLY): as Support but the gate fails.
- Kill: primary difference at or below zero with at least 10 events in each group.
- Unscorable: fewer than 10 events in either group.
- Anything else: inconclusive.

## Known limitations (stated before the run)

- Void runs on Water's population and coding; it is not independent of Water, and a coding error in D affects both.
- Most Supreme Court opinions state no figure, so D = 1 may be rare and the test unscorable.
- One parameter set; no sensitivity sweep selects the reported result.
