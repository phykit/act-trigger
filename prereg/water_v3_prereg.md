# Pre-registration: Project Water v3 (AI materiality coding, with a reproducible API coder)

Frozen before the API coder coded anything. 30 October 2026.

Supersedes water_v2_prereg.md (SHA-256 956347eee67817baa6416040ce6e554f2eb4b824a503fd9b0829416e28f53321) by adding a third coder and changing the primary score; everything else is unchanged. Coders 2 and 2b (Claude agents) coded under v2 before this version was written; their sheets are used as committed. Both reported that they could not read whole filings (web tools truncate at about 100,000 characters, and EDGAR full-text search was blocked to them), so component C is weak in their sheets. Coder 3 reads the filings in full on the GitHub runner.

## Hypothesis

A ruling's materiality to the listed issuer, read by an AI coder from the judgment and the issuer's own filings without reference to any price, predicts the size of the price reaction and of the drift that follows. If it does, AI legal reading adds information that the event study alone does not and can be run at scale; if it does not, the Moon and Earth averages are not something an AI reader can select on.

Registered sign: positive. High-stakes events have larger signed post-ruling drift than low-stakes events.

## Populations (fixed by rule before coding)

1. Moon: the 37 events in `results/moon_result_2026-10-30_2.events.csv` with status `ok` and a coded direction (run 4). The coding list is `data/water/moon37_coding_list.csv`, which carries no price or return column.
2. Earth: the reacting events (abs(z_0) at or above 2, not earnings-adjacent, calm market) of the first Earth run whose universe contains Federal Circuit opinions for the whole of 2012 to June 2025. The coding list for these is written without price columns before any coder sees it.

## Coders and blindness

- Coder 1: Legora, run by the operator with the kit in `data/water/legora/`; the operator does not edit its answers.
- Coders 2 and 2b: two independent Claude agent runs (coded under v2; sheets `moon37_coding_sheet_claude_a.csv` and `_b.csv`).
- Coder 3: the API coder, `scripts/ai_coder.py`, run in GitHub Actions. For each event it assembles a document pack from primary sources only: the Supreme Court opinion text (CourtListener), and from the parent's last 10-K and last 10-Q filed before the ruling (EDGAR) the cover-page statement of non-affiliate market value, Item 3 (Legal Proceedings) and every passage naming the party, the opposing party or the Supreme Court. It sends the pack with the rubric below to model `claude-sonnet-5-5`, records the model identifier, the prompt's SHA-256, the document pack's SHA-256 and token usage, and commits the sheet and the packs.
- No coder receives any price, return or market data; the coding lists carry none. The API coder's script reads no file under `results/`.
- The analyst who has seen the price results does not code and does not edit any sheet.
- Each sheet is committed before any analysis joins it to returns.

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

1. Primary: the mean signed drift (Moon: S = direction x CAR(+1,+5); Earth: sign(AR_0) x CAR(+1,+5)) of high-stakes events minus that of low-stakes events, pooled across the two populations, using coder 3's score (high if 2 or more), because coder 3 is the reproducible instrument that would be operated; coders 1, 2 and 2b are reported alongside it, and the mean of all available coders is a secondary result. One-sided permutation p over the high and low labels, 10,000 draws, seed 20261030.
2. Manipulation check: mean abs(z_0) of high-stakes events above that of low-stakes events. If this fails, the coding does not measure materiality as the market sees it and the primary result is reported as uninterpretable.
3. Reliability: Cohen's kappa on the high/low label and the score correlation for each pair of coders (1, 2, 2b, 3); coders 2 and 2b measure run-to-run stability, coder 1 against coder 3 measures agreement between independent AI systems. A kappa below 0.4 between coder 1 and coder 3 is reported as a finding against operability, whatever the primary result.
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
