# Pre-registration: Project Metal (does legal complexity slow price discovery?)

Frozen before any result under this specification was computed. 30 October 2026.

## Hypothesis

The framework paper's core thesis: when a judgment is long, split across several opinions, or disposes of the appeal only in part, the market takes longer to work out its economic meaning, so more of the price adjustment happens after the ruling day. Registered sign: positive. Complex rulings show larger post-ruling abnormal movement, relative to the day-0 move, than simple rulings.

## Population

Every Earth event with status `ok` in the first Earth run whose universe contains Federal Circuit opinions for the whole of 2012 to June 2025, whether or not it reacted.

## Complexity score (mechanical, 0 to 3)

For each ruling, from CourtListener (opinion cluster and its opinions) and SCDB:

1. Length: 1 if the total word count of all opinions in the cluster is above the median of the population; otherwise 0.
2. Separate opinions: 1 if the cluster has two or more opinions (a majority plus at least one concurrence or dissent); otherwise 0.
3. Partial disposition: Supreme Court, 1 if SCDB `caseDisposition` is 6 or 7 (affirmed and reversed or vacated in part, with or without remand) or 8 (vacated, where SCDB codes a vacatur without full reversal); Federal Circuit, 1 if the last 600 characters of the majority opinion contain "IN PART" or "REMAND" (case-insensitive); otherwise 0.

Complex = score of 2 or more. A ruling whose opinion text cannot be retrieved is unscorable and listed.

## Statistics

1. Primary: the post-ruling share of the movement, P = abs(CAR(+1,+5)) / (abs(AR_0) + abs(CAR(+1,+5))), averaged over complex events minus over simple events; one-sided permutation p over the labels, 10,000 draws, seed 20261030. Events with abs(AR_0) + abs(CAR(+1,+5)) below one day's sigma are excluded as containing no movement to apportion.
2. Secondary: among reacting events (abs(z_0) at or above 2), mean signed CAR(+1,+5) for complex minus simple; each complexity component separately; split by court.

## Decision rule (stated before the run)

- Support: primary difference above zero, permutation p below 0.05, at least 30 complex and 30 simple events.
- Kill: primary difference at or below zero with those counts.
- Unscorable: fewer than 30 in either group.
- Anything else: inconclusive.

## Known limitations (stated before the run)

- Word count and opinion count are proxies; a long opinion can be clear and a short one obscure.
- The share P is noisy when the day-0 move is small; the exclusion threshold limits but does not remove this.
- The quantification gap and contagion scope in the paper's score need coding and are covered by Water and Fire.
- One parameter set; no sensitivity sweep selects the reported result.
