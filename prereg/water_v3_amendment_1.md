# Water v3, amendment 1: source of the Supreme Court opinion text

Registered 30 October 2026, before coder 3 has produced any valid coding. It amends `water_v3_prereg.md` (SHA-256 42770b136d63fc814cd31adec797e021439c9d3bffe2ef639678cd7ef3b8c05a), which is left unchanged; every provision of v3 not mentioned here stands.

## Reason

Version 3 names CourtListener as the source of the opinion text in coder 3's document pack. CourtListener has refused nearly every request from this project's token since the afternoon of 30 October 2026 (HTTP 429). Coder 3's first run was retired because its packs had no opinions (`data/water/README.md`), and the rerun of 30 October was cancelled at its time limit with nothing committed. The same documents are published by two official sources that the GitHub runner can reach, as shown by the diagnostics committed at `data/appeals/govinfo_probe2.md` and `govinfo_probe3.md`.

## Change

For each event, the Supreme Court opinion is taken from the first of the following that has it:

1. The Supreme Court's own slip opinion (supremecourt.gov, `/opinions/slipopinion/{term}`), for October Term 2017 onwards. The PDF is matched on the docket number in its file name and, where the table row shows one, on the decision date.
2. The United States Reports on GovInfo (collection USREPORTS). This is the per-case PDF whose caption matches the case name on both sides and whose `decisionDate` equals the event date.
3. CourtListener, as in v3, where neither official source has the opinion.

The text is extracted from the PDF (pypdf) and capped as in v3. The pack header and the response file record which source was used. An event with no opinion from any of the three is not coded, as before.

The same order applies to the Legora document bundle (coder 1), which includes the official PDF itself rather than a text rendering.

## What this does not change

- The rubric, the prompt, the model, the primary score, the decision rule and the population.
- Blindness. None of the three sources carries price or market data, and the scripts still read nothing under `results/`.
- The 10-K and 10-Q extracts, which come from EDGAR as before.

## Expected effect

The opinion is the same judgment in each source. The slip opinion is the text released on the day of the ruling. The United States Reports text is the bound version, which can include later minor corrections. Neither difference bears on the money figures, the business the ruling governs, or whether a figure is stated; those are the only things the rubric codes from the opinion.

Implementation: `scripts/scotus_opinions.py`; `scripts/ai_coder.py` (`opinion_text`); `scripts/legora_bundle.py` (`opinion_pdf`).
