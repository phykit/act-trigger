# Project Water coding files

- `moon37_coding_list.csv`: the 37 Moon events (run 4). No price or return columns. Coders must not open any file under `results/` before their sheet is committed.
- `moon37_coding_sheet_operator.csv`: not used. Under Water v2 the operator does not code; the empty template is kept as created.
- `moon37_coding_sheet_legora.csv`: the blind agent coder's sheet (Legora, run by the operator; kit in `legora/`).
- Rubric: `prereg/water_prereg.md`. Score = A + B + C; high stakes = 2 or more.

- `moon37_coding_sheet_claude_a.csv` and `moon37_coding_sheet_claude_b.csv`: coder 2 and its independent repeat (coder 2b), fresh Claude agents with no access to results.
- Specification in force: `prereg/water_v2_prereg.md`.

## Coder 3 (API coder), run 1 retired

Run 1 (30 October 2026, workflow run 41090567344) is kept as `moon37_coding_sheet_api_run1_no_opinion.csv` with its packs and responses in `api_coder_run1_no_opinion/`, and is not coder 3's score. CourtListener returned 429 (rate limited) on every opinion request, so all 37 document packs went to the model without the Supreme Court opinion, contrary to the pack defined in `prereg/water_v3_prereg.md`; W22 also failed on an unparseable reply. The coder now waits out rate limits, does not call the model for an event whose opinion is unavailable (the event is listed as not coded), stops after three such events at the start of a run, and retries an unparseable reply once. No returns were joined to run 1 before it was retired. Usage of run 1: 1,305,547 input and 14,479 output tokens.
