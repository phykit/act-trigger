# Pre-registration: Project Water v2 (AI materiality coding of appellate rulings)

Frozen before any coding under this specification was done. 30 October 2026.

Supersedes water_prereg.md (SHA-256 c0a3d9873dd0bfb364bcd41b1fc4de06023e4fedf98990604e3aaec9fe128c83) on the coders only. The operator will not code: the strategy is only operable if the materiality reading is done by AI, so the question is whether AI coding adds information, and whether two independent AI coders agree well enough to rely on. Populations, rubric, statistics and decision rule are otherwise unchanged. No coding was done under v1.

## Hypothesis

A ruling's materiality to the listed issuer, read by an AI coder from the judgment and the issuer's own filings without reference to any price, predicts the size of the price reaction and of the drift that follows. If it does, AI legal reading adds information that the event study alone does not and can be run at scale; if it does not, the Moon and Earth averages are not something an AI reader can select on.

Registered sign: positive. High-stakes events have larger signed post-ruling drift than low-stakes events.

## Populations (fixed by rule before coding)

1. Moon: the 37 events in `results/moon_result_2026-10-30_2.events.csv` with status `ok` and a coded direction (run 4). The coding list is `data/water/moon37_coding_list.csv`, which carries no price or return column.
2. Earth: the reacting events (abs(z_0) at or above 2, not earnings-adjacent, calm market) of the first Earth run whose universe contains Federal Circuit opinions for the whole of 2012 to June 2025. The coding list for these is written without price columns before any coder sees it.

## Coders and blindness

- Coder 1: Legora, run by the operator in a fresh workspace with the kit in `data/water/legora/`. The operator does not edit its answers.
- Coder 2: a fresh Claude agent that has never seen this repository's results, given only the price-free coding list, the rubric and web access to opinions and EDGAR, and instructed not to consult any price, return, chart or market commentary.
- Coder 2 is run a second time, independently, on the same list (coder 2b) to measure run-to-run stability.
- The analyst who has seen the price results (the assistant that ran Earth and Moon) does not code and does not edit any sheet.
- A coder that recognises an event's price reaction from memory records that in `price_known`; results are reported with and without those events.
- Each sheet is committed to the repository before any analysis joins it to returns. The commit time is the record of blindness.

## Rubric (score per event, 0 to 4)

A. Money at stake relative to the issuer, from the judgment, the opinion below, or the issuer's last 10-K or 10-Q before the ruling, divided by the issuer's market capitalisation as stated on the cover of that 10-K (aggregate market value held by non-affiliates) or, failing that, recorded as unknown:
   - 2 if 5 per cent or more;
   - 1 if at least 1 and under 5 per cent;
   - 0 if under 1 per cent, or if no figure can be found.
B. Core business: 1 if the ruling directly governs a core product, licence, franchise, patent, regulatory permission or the issuer's principal pricing or contracting practice; otherwise 0.
C. Disclosed as material: 1 if the issuer's last 10-K or 10-Q before the ruling names the case in Legal Proceedings, the risk factors or the contingencies note; otherwise 0.
D. Quantification gap (recorded, not scored): whether the ruling or the issuer states a money figure for the consequence (yes or no).

Score = A + B + C. High stakes = score of 2 or more.

The coding sheet records for each event: score components, the figure and its source with URL, the filing used (accession number), D, `price_known`, and a one-line reason.

## Statistics

1. Primary: the mean signed drift (Moon: S = direction x CAR(+1,+5); Earth: sign(AR_0) x CAR(+1,+5)) of high-stakes events minus that of low-stakes events, pooled across the two populations, using the mean of coder 1's and coder 2's scores (high if the mean is 2 or more); if coder 1's sheet is not committed by the time Earth's coding list exists, coder 2 alone is primary and this is stated in the result. One-sided permutation p over the high and low labels, 10,000 draws, seed 20261030.
2. Manipulation check: mean abs(z_0) of high-stakes events above that of low-stakes events. If this fails, the coding does not measure materiality as the market sees it and the primary result is reported as uninterpretable.
3. Reliability: Cohen's kappa between coders 1 and 2 on the high/low label and the correlation of their scores (inter-coder); the same between coders 2 and 2b (run-to-run). A kappa below 0.4 between independent AI coders is reported as a finding against operability, whatever the primary result.
4. Secondary: each population separately; each coder separately; excluding `price_known` events; excluding the four Moon events that are the named party under a later ticker (NantKwest, Facebook, LabCorp, Amalgamated).
5. Cost check: the high-stakes mean signed drift against twice the Corwin and Schultz (2012) high-low spread estimate for each stock on day 0, reported as net of spread.

## Decision rule (stated before coding)

- Support: primary difference above zero, permutation p below 0.10, and the manipulation check passes.
- Kill: primary difference at or below zero.
- Uninterpretable: manipulation check fails.
- Anything else: inconclusive; no trading.

The 0.10 threshold reflects the small populations (about 37 plus the Earth reacting events); a supported result is a reason to forward-test (Air), not to trade.

## Known limitations (stated before coding)

- An agent coder may recall the outcome of famous cases; the outcome is in the judgment in any case and is not what is being hidden. What is hidden is the price reaction.
- AI coders may carry memory of famous price reactions from training data (Myriad, NantKwest); `price_known` is self-reported and cannot be verified.
- Market capitalisation from the 10-K cover is up to a year stale at the ruling date.
- Small populations; one parameter set; no sensitivity sweep selects the reported result.
