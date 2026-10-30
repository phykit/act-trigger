# Pre-registration: Project Strife (when the price disagrees with the formal outcome, which is right?)

Frozen before any result under this specification was computed. 30 October 2026.

## Hypothesis

The framework paper's "Pyrrhic victory": a party can win formally and lose economically (a patent upheld but construed narrowly; a judgment affirmed with damages remitted). When the day-0 price moves against the formal outcome, two readings compete: the market has seen the economic substance (the price is right and keeps moving), or the market has misread the headline (the price reverses towards the formal outcome). Registered sign: positive. On disagreement events the abnormal return over days +1 to +5 continues in the direction of the day-0 move.

## Population

Supreme Court events with a coded formal direction: Earth's listed-party events and Moon's parent events with status `ok` in the first runs whose universe contains Federal Circuit opinions for the whole of 2012 to June 2025, where SCDB `partyWinning` is 0 or 1. Federal Circuit events are excluded because the source carries no structured disposition.

## Definitions

1. Formal direction F = +1 if the listed party's side won, -1 if it lost (as Moon).
2. Disagreement event: sign(AR_0) = -F and abs(z_0) at or above 1.5. Agreement event: sign(AR_0) = F and abs(z_0) at or above 1.5. (The threshold is lower than Earth's because the population is smaller; it is fixed here.)
3. Outcome: D = sign(AR_0) x CAR(+1,+5).

## Statistics

1. Primary: mean D over disagreement events; one-sided bootstrap p (draws at or below zero), 10,000 draws, seed 20261030.
2. Secondary: mean D over agreement events; the difference between the two; the list of disagreement events with SCDB `caseDisposition`.

## Decision rule (stated before the run)

- Support (the price is right): mean D on disagreement events above zero, p below 0.10, at least 10 disagreement events.
- Reverse finding (the headline is right): mean D below zero with one-sided p below 0.10 for the opposite sign; reported as a finding, not a kill of the framework.
- Unscorable: fewer than 10 disagreement events.
- Anything else: inconclusive.

## Known limitations (stated before the run)

- Disagreement events are rare; the population may be unscorable.
- SCDB's formal winner is the party favoured by the disposition, which is not the economic winner by construction; that is the point of the test but also means some disagreements reflect coding, not economics.
- One parameter set; no sensitivity sweep selects the reported result.
