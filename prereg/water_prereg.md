# Pre-registration: Project Water (blind materiality coding of appellate rulings)

Frozen before any coding under this specification was done. 30 October 2026.

## Hypothesis

A ruling's materiality to the listed issuer, read from the judgment and the issuer's own filings without reference to any price, predicts the size of the price reaction and of the drift that follows. If it does, legal reading adds information that the event study alone does not; if it does not, the Moon and Earth averages are not something a lawyer can select on.

Registered sign: positive. High-stakes events have larger signed post-ruling drift than low-stakes events.

## Populations (fixed by rule before coding)

1. Moon: the 37 events in `results/moon_result_2026-10-30_2.events.csv` with status `ok` and a coded direction (run 4). The coding list is `data/water/moon37_coding_list.csv`, which carries no price or return column.
2. Earth: the reacting events (abs(z_0) at or above 2, not earnings-adjacent, calm market) of the first Earth run whose universe contains Federal Circuit opinions for the whole of 2012 to June 2025. The coding list for these is written without price columns before any coder sees it.

## Coders and blindness

- Two coders work independently: the operator, and an agent that is given only the coding list, this rubric and access to the judgment and EDGAR filings, and is instructed not to consult any price, return, chart or market commentary.
- The analyst who has seen the price results (the assistant that ran Earth and Moon) does not code.
- A coder who recognises an event's price reaction from memory records that in the `price_known` column; the analysis is reported with and without those events.
- The coding sheets are committed to the repository before any analysis joins them to returns. The commit time is the record of blindness.

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

1. Primary: the mean signed drift (Moon: S = direction x CAR(+1,+5); Earth: sign(AR_0) x CAR(+1,+5)) of high-stakes events minus that of low-stakes events, pooled across the two populations, using the mean of the two coders' scores (high if the mean is 2 or more). One-sided permutation p over the high and low labels, 10,000 draws, seed 20261030.
2. Manipulation check: mean abs(z_0) of high-stakes events above that of low-stakes events. If this fails, the coding does not measure materiality as the market sees it and the primary result is reported as uninterpretable.
3. Agreement: Cohen's kappa between the two coders on the high/low label, and the correlation of their scores.
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
- The operator has seen the returns of a handful of Moon events quoted in conversation (NantKwest, Coinbase, Tyson); those are flagged in `price_known` by rule.
- Market capitalisation from the 10-K cover is up to a year stale at the ruling date.
- Small populations; one parameter set; no sensitivity sweep selects the reported result.
