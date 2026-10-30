# Project Water coding files

- `moon37_coding_list.csv`: the 37 Moon events (run 4). No price or return columns. Coders must not open any file under `results/` before their sheet is committed.
- `moon37_coding_sheet_operator.csv`: not used. Under Water v2 the operator does not code; the empty template is kept as created.
- `moon37_coding_sheet_legora.csv`: the blind agent coder's sheet (Legora, run by the operator; kit in `legora/`).
- Rubric: `prereg/water_prereg.md`. Score = A + B + C; high stakes = 2 or more.

- `moon37_coding_sheet_claude_a.csv` and `moon37_coding_sheet_claude_b.csv`: coder 2 and its independent repeat (coder 2b), fresh Claude agents with no access to results.
- Specification in force: `prereg/water_v2_prereg.md`.

## Coder 3: official opinion sources (amendments 1 and 2)

CourtListener throttled the project's token through the afternoon of 30 October 2026; the coder rerun that day (workflow run 41109989235) was cancelled at its two-hour limit with nothing committed. `prereg/water_v3_amendment_1.md` and `water_v3_amendment_2.md` take the opinion from the Court's own opinions page (slip opinion, or the case's pages in a preliminary print or bound volume) and from the GovInfo United States Reports, with CourtListener only as a fallback. The source check (`opinion_sources/input_moon37_sources.csv`, counts only) found an official PDF for all 37 Moon events: 21 from GovInfo and 16 from supremecourt.gov.

## Coder 3 sheet, 30 October 2026

Workflow run 41138259855 coded 35 of 37 events; W21 failed on a reply the parser could not read (a greedy match spanning trailing text), and W34's official opinion was not retrieved at run time and CourtListener returned 429. The parser was fixed to take the first complete JSON object, and run 41140860413 re-coded only those two events (failed attempts kept as `responses/W21_attempt1.json` and `W34_attempt1.json`). Every one of the 37 packs carries the official opinion (21 GovInfo, 16 supremecourt.gov). Sheet check: 37 rows, 4 high-stakes, price_known 0 throughout. No returns have been joined.

## Coder 3 (API coder), run 1 retired

Run 1 (30 October 2026, workflow run 41090567344) is kept as `moon37_coding_sheet_api_run1_no_opinion.csv` with its packs and responses in `api_coder_run1_no_opinion/`, and is not coder 3's score. CourtListener returned 429 (rate limited) on every opinion request, so all 37 document packs went to the model without the Supreme Court opinion, contrary to the pack defined in `prereg/water_v3_prereg.md`; W22 also failed on an unparseable reply. The coder now waits out rate limits, does not call the model for an event whose opinion is unavailable (the event is listed as not coded), stops after three such events at the start of a run, and retries an unparseable reply once. No returns were joined to run 1 before it was retired. Usage of run 1: 1,305,547 input and 14,479 output tokens.
