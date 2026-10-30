# Pre-registration: Project Death (pair trades where both sides are listed)

Frozen before any result under this specification was computed. 30 October 2026. Adopts `prereg/cost_gate_prereg.md`.

## Hypothesis

Where both sides of an appeal are listed companies (common in Federal Circuit patent cases), the ruling transfers value from one to the other. A long-winner, short-loser position removes market and much of industry risk, so if incorporation is slow the pair's drift after day 0 should be cleaner than Earth's single-stock drift. The opponent should also mirror the litigant: a ruling that is only absorbed by one side is a sign of mis-pricing.

Registered sign: positive. The pair's abnormal return over days +1 to +5 continues in the direction of its day-0 move.

## Population (mechanical)

1. Every ruling in the Earth universe (Supreme Court OT2005 to OT2024 as Earth item 1; Federal Circuit precedential opinions 2012 to June 2025 as Earth item 2) of the first Earth run whose universe contains the Federal Circuit for that whole period.
2. Both sides of the caption match EDGAR's company list under Earth's normalisation (Earth item 3), to two different CIKs. Where a side has several listed names, the first is used (as Earth). Parents through Exhibit 21 are not used: both legs are named parties.
3. Price history for both legs as Earth item 4. One pair per ruling.

## Definitions

1. For each leg, AR and the rolling sigma as Earth (market model on SPY, 60-day sigma lagged one day).
2. Pair abnormal return on day t: P_t = AR_A,t - AR_B,t, where A is the leg with the higher AR on day 0 (the market's winner). Pair sigma = sqrt(sigma_A^2 + sigma_B^2).
3. Reacting pair: abs(P_0) / pair sigma at or above 2.
4. Pair drift: CAR_P(+1,+5) = sum of P_t over t = +1 to +5. Positive means continuation.
5. Control, as Earth: the same pair's other days in the 250 trading days before the ruling with abs(P_t) / pair sigma at or above 2, excluding days within five trading days of either leg's earnings (EDGAR 8-K item 2.02) and days on which SPY's absolute return exceeds twice its own 60-day sigma; the control drift is signed by that day's P_t.

## Statistics

1. Primary: mean over reacting pairs of (pair drift minus that pair's mean control drift); one-sided bootstrap p, 10,000 draws, seed 20261030.
2. Tradeable statistic (for the cost gate): mean pair drift, the position being long A and short B in equal value from the close of day 0 to the close of day +5; cost is both legs' round-trip cost.
3. Secondary: mean pair drift without the control; the mirror test (correlation across reacting pairs of AR_A,0 with -AR_B,0, and the share of pairs where both legs move in opposite directions on day 0); for Supreme Court pairs, agreement of the market's winner with SCDB `partyWinning`; each court separately.

## Decision rule (stated before the run)

- Support: primary above zero, bootstrap p below 0.10, at least 15 reacting pairs, and the cost gate passed.
- SUPPORT (GROSS ONLY): as Support but the gate fails.
- Kill: primary at or below zero with at least 15 reacting pairs.
- Unscorable: fewer than 15 reacting pairs.
- Anything else: inconclusive.

## Known limitations (stated before the run)

- Both sides must be listed under exact name matches; the population may be small, and is not known until the universe is built.
- The market's winner is defined by the day-0 move, not the formal outcome; that is what a trader can observe at the close of day 0.
- No borrow cost on the short leg, and hard-to-borrow small caps may not be shortable at all; the cost gate understates cost on the short side.
- Pairs of very different size: equal value weighting is fixed here, not beta- or volatility-weighted.
- One parameter set; no sensitivity sweep selects the reported result.
