# Running Project Water's blind coding through Legora

Legora is the agent coder under `prereg/water_prereg.md`. It sees the case list, the rubric and the legal materials, and nothing about prices.

## Steps

1. **Before you start, do not open anything under `results/`** in this repository, and do not open the `*.events.csv` files. They contain the returns the coding is meant to predict.
2. In Legora, open a fresh workspace with no other documents or connectors to market data.
3. Upload `input_moon37.csv` (37 rows: event id, date, docket, case name, the party, the listed parent's ticker and CIK, and links to the opinion and to the parent's 10-K and 10-Q filings dated before the ruling).
4. Either paste `prompt_master.md` (below its line) as a single instruction, or set up a tabular review with the column questions in `tabular_columns.md`, putting the blindness rule in the general instructions.
5. If Legora cannot follow links, download the opinion (Oyez or supremecourt.gov) and the last 10-K before the ruling for each row and upload them; the instructions are the same.
6. Export the result as CSV and save it as `data/water/moon37_coding_sheet_legora.csv`.
7. Check it: `python scripts/water_check_sheet.py data/water/moon37_coding_sheet_legora.csv`. Fix or re-run any rows it flags.
8. Commit the sheet before anything joins it to returns. The commit time is the record that the coding was blind.

## Your own coding (the second coder)

Fill in `data/water/moon37_coding_sheet_operator.csv` by the same rubric, without looking at Legora's sheet, and commit it separately. Mark `price_known` as 1 for any event whose share reaction you have seen or recall, including NantKwest, Coinbase and Tyson, which were quoted in our conversation.

## After both sheets are committed

The Water analysis joins both sheets to the Moon returns, reports the high-minus-low drift, the manipulation check (do high-stakes events react more on the day) and the agreement between you and Legora.
