# Pre-registration: Project Moon (propagation of a ruling to the listed parent of a subsidiary party)

Frozen before any result under this specification was computed. 30 October 2026.

## Hypothesis

When the party to a Supreme Court ruling is a subsidiary of a listed company, the parent's share price incorporates the ruling more slowly than when the listed company is itself the named party, because the parent's name and ticker are absent from the headline. Two testable implications: i) the parent's day-0 reaction, signed by whether its subsidiary won, is smaller than the direct-party reaction measured in Project Earth; ii) the parent's abnormal return over the following five days, signed the same way, is positive.

Registered sign: positive for the signed five-day drift. There is no prior art on this population; the nearest is Cohen and Frazzini (2008) on slow diffusion across economically linked firms.

## Universe (mechanical; no inspection)

1. Rulings: SCDB October Terms 2005 to 2024, decision types 1, 5, 6 and 7, with `partyWinning` equal to 0 or 1 (an unclear outcome is excluded).
2. Subsidiary parties: each side of the case name that fails Project Earth's exact match is searched as an exact phrase in EDGAR full-text search restricted to 10-K filings; a hit whose document type begins with "EX-21" (the filer's subsidiary list) identifies the filer as the parent. The parent is accepted when one filer accounts for all EX-21 hits, or for at least 80 per cent of them with at least three hits; otherwise the side is marked ambiguous and excluded. Full-text search covers filings from 2001, so a parent that stopped filing before then is not found and the side is excluded.
3. Ticker: the parent's first ticker in the EDGAR company list; price history must cover 260 trading days before the ruling and ten after.
4. Direction: +1 if the subsidiary's side won (petitioner and `partyWinning` = 1, or respondent and `partyWinning` = 0), otherwise -1.

## Definitions

1. Day 0, market model, sigma and z: as Project Earth.
2. Signed reaction S_0 = direction x AR_0; signed drift S = direction x CAR(+1,+5).
3. Comparison population: Project Earth's Supreme Court direct-party events with the same direction coding, whether or not they reacted.
4. Statistic for implication i): the difference in mean |z_0| between Moon events and the comparison population, with a two-sample bootstrap p (10,000 draws, seed 20261030).
5. Statistic for implication ii): mean S over Moon events, bootstrap p (one-sided, draws at or below zero).
6. Placebo: the same parents on dates drawn at random from the same calendar years, excluding windows around any ruling in the universe and earnings releases, with direction assigned at random; mean signed CAR(+1,+5) and its bootstrap p.
7. Secondary descriptives: mean S_0 and its p; the number of sides resolved to a parent, ambiguous, and unresolved.

## Decision rule (stated before the run)

- Support: mean S above zero, bootstrap p below 0.05, placebo mean not above the Moon mean, and at least 25 events.
- Kill: mean S at or below zero with at least 25 events.
- Unscorable: fewer than 25 events.
- Anything else: inconclusive; no trading.

Implication i) is reported but does not enter the decision rule.

## Operator inputs deliberately left blank

Minimum effect worth pursuing, minimum event count for a live decision, and a ratified pre-mortem are for the operator.

## Known limitations (stated before the run)

- Stakes are not coded, so most events are immaterial to the parent and dilute the mean towards zero; the test is of the channel, not of its size.
- EDGAR full-text search returns documents that contain the phrase anywhere, so a subsidiary name that is also a common phrase can produce spurious EX-21 hits from unrelated filers; the 80 per cent rule guards against this at the cost of excluding joint ventures.
- `partyWinning` records the formal winner; a mixed ruling (Myriad, 2013) is coded as one side winning.
- Supreme Court only: the Federal Circuit source carries no structured disposition, so direction cannot be coded mechanically there.
- One parameter set; no sensitivity sweep is used to select the reported result.
