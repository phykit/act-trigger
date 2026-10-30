# Pre-registration: Project Fire (spillover of a ruling to the litigant's industry, signed by the litigant's own reaction)

Frozen before any result under this specification was computed. 30 October 2026.

## Hypothesis

When an appellate ruling of general application moves a listed party's share price on the day it is released, the shares of other companies in the same industry move in the same direction over the following ten trading days, and do so more than after the same party's other large idiosyncratic moves. The litigant's day-0 reaction is the signal; the peers are the trade. The mechanism is limited attention to economically linked firms (Cohen and Frazzini, 2008; Menzly and Ozbas, 2010); the legal-specific prior art is the industry reaction to the 2012 health-care ruling (Hartley, 2012) and competitor effects in asbestos litigation (Hadlock and Sonti, 2012).

Registered sign: positive (signed peer drift after rulings minus signed peer drift after the litigant's other large moves, above zero).

## Universe (mechanical; no inspection)

1. Events: Project Earth's reacting events (|z_0| at or above 2, not earnings-adjacent, calm market day) in rulings of general application, defined as rulings where the opposing side is neither a listed company (Earth's exact match) nor the subsidiary of one (Moon's Exhibit 21 match). A dispute between two listed companies is excluded because the sign of the effect on peers is ambiguous there.
2. Industry: the litigant's four-digit SIC code from its EDGAR submissions record.
3. Peers: companies with the same four-digit SIC in EDGAR's company browse, mapped to tickers through the EDGAR company list, excluding the litigant and any other party to the ruling, taken in ascending CIK order up to 40 names with price history covering the event window. Equal weights.
4. Minimum basket: five peers with data; otherwise the event is excluded and listed.

## Definitions

1. Day 0, market model, sigma and z for the litigant: as Project Earth.
2. Basket: the equal-weighted daily log return of the peers; basket abnormal return from a rolling 250-day market model of the basket on SPY, lagged one day.
3. Signal: s = sign(AR_0 of the litigant).
4. Outcomes: signed basket reaction s x basket AR_0; signed basket drift F = s x basket CAR(+1,+10).
5. Control: the same basket after the litigant's other |z| at or above 2 days (Earth's control days for that company), signed by the litigant's sign on those days; the control value is the mean signed basket CAR(+1,+10) over those days. An event with fewer than three control days is dropped from the difference and listed.
6. Statistic: the mean over events of (F minus the event's control mean); bootstrap over events, 10,000 draws, seed 20261030; one-sided p = share of draws at or below zero.
7. Secondary descriptives: mean F alone and its p; mean signed basket reaction on day 0; the split by court.

## Decision rule (stated before the run)

- Support: mean difference above zero, bootstrap p below 0.05, at least 30 events in the difference.
- Kill: mean difference at or below zero with at least 30 events.
- Unscorable: fewer than 30 events.
- Anything else: inconclusive; no trading.

## Operator inputs deliberately left blank

Minimum effect worth pursuing, minimum event count for a live decision, and a ratified pre-mortem are for the operator.

## Known limitations (stated before the run)

- Four-digit SIC is a coarse definition of industry and EDGAR's codes are self-reported and stale for some filers.
- Ascending-CIK selection of peers is mechanical but arbitrary; older registrants are over-represented.
- Equal weighting and a 40-name cap mean the basket is not the investable sector.
- The sign convention assumes peers are on the litigant's side of the rule; where the litigant is the regulated exception rather than the representative, the sign is wrong and the effect is diluted.
- Dependence: many events share decision days in June and peers overlap across events in the same industry; the bootstrap treats events as independent.
- One parameter set; no sensitivity sweep is used to select the reported result.
