# Project Water, coder 1: running the coding in Legora

You run Legora; you do not code, judge or edit any answer. The sheet Legora returns is committed as it comes back.

## What you upload

From `legora_moon37_bundle.zip` (the artifact of the `legora-bundle` workflow run in phykit/act-trigger, or the copy Claude sends you), unzipped:

- the folder `moon37_documents/`, holding **37 PDFs, `W01.pdf` to `W37.pdf`**. Each PDF is one event: a cover page (case, party, listed parent, ticker, CIK, ruling date), then the Supreme Court opinion, then the parent's last 10-K and last 10-Q filed before the ruling. Nothing in them postdates the ruling.

Upload nothing else: not `input_moon37.csv`, not the manifest, and nothing from the GitHub repository.

## Steps

1. Do not open anything under `results/` in the repository, or any `*.events.csv` file.
2. In Legora, start a **new Tabular Review** in a fresh project with no other documents and no market-data connectors. If Legora offers web search for the review, turn it off.
3. Upload the 37 PDFs. Each becomes one row.
4. Paste the **General instructions** below into the review's instructions field (it may be called "instructions", "context" or "system prompt").
5. Add the **ten columns** below, in the order given. For each: paste the column name exactly as given, and paste the question exactly as given. Where Legora asks for an answer format, use the one shown.
6. Run the review on all 37 rows. Do not correct any cell. If a cell is blank or errors, re-run that cell once; if it still fails, leave it.
7. Export to CSV. Make sure the file has a column for the document name (W01 to W37); rename that column `event_id` and strip `.pdf` from the values if Legora adds it. Nothing else in the file should be edited.
8. Send the CSV to Claude (attach it in the chat) or commit it as `data/water/moon37_coding_sheet_legora.csv`. Claude runs `scripts/water_check_sheet.py` on it and commits it before any join to returns.

## General instructions (paste exactly)

You are coding the economic materiality of a US Supreme Court ruling to a listed company, for a pre-registered research study. Each document is one ruling. Its cover page names the case, the party to the case, the listed parent company, its ticker and SEC CIK, and the ruling date. The document then contains the Supreme Court opinion and the parent's last 10-K and 10-Q filed before the ruling.

Strict blindness rule: you must not look at, search for, or rely on any share price, stock chart, market capitalisation history, analyst note, trading commentary or news coverage of how the company's shares reacted to the ruling. The study measures whether a reading of the legal and disclosure materials predicts the market's reaction, so any knowledge of the reaction invalidates the coding. Use only the document. If you already know from memory how the shares moved after this ruling, answer 1 in the price_known column and still code every other column on the document alone.

Answer each column for this document only. Use plain numbers for US dollar amounts, with no commas, currency signs or words such as "million".

## Columns (name, then question; paste exactly)

1. **A_figure_usd** (number, or blank)
   What is the largest money amount that this Supreme Court ruling decides or puts at risk for the party: a damages award, a tax assessment, a class-wide exposure stated in the opinion, or an amount the parent disclosed for this case in the 10-K or 10-Q? Answer with a plain number in US dollars. Leave blank if no such figure appears in the document. Do not use share prices or market values.

2. **A_mcap_usd** (number)
   What aggregate market value of the voting stock held by non-affiliates is stated on the cover page of the 10-K in this document? Answer with a plain number in US dollars.

3. **A_money_score** (0, 1 or 2)
   Divide A_figure_usd by A_mcap_usd. Answer 2 if the result is 0.05 or more; 1 if it is at least 0.01 and under 0.05; 0 if it is under 0.01 or if A_figure_usd is blank.

4. **A_source_url** (text)
   State where in the document you found A_figure_usd and A_mcap_usd (the section and page), or "none" if A_figure_usd is blank.

5. **B_core_business** (0 or 1)
   Does the ruling directly govern one of the parent's core products, licences, franchises, patents, regulatory permissions, or its principal pricing or contracting practice (for example, an arbitration clause used in all its consumer contracts, or a tax that applies across its main network)? Answer 1 if yes. Answer 0 if it concerns a single employee, a single customer, a peripheral transaction or a procedural point of no wider effect on the business.

6. **C_disclosed** (0 or 1)
   Does the 10-K or 10-Q in this document name this case, or describe it unmistakably, in Legal Proceedings, the risk factors, or the contingencies or litigation note to the financial statements? Answer 1 or 0.

7. **C_filing_accession** (text, or blank)
   If C_disclosed is 1, give the accession number of the filing that discloses the case, as shown on this document's cover page. Otherwise leave blank.

8. **D_figure_stated** (0 or 1)
   Does the opinion, or the parent's disclosure in the 10-K or 10-Q, state a money figure for the consequence of the ruling? Answer 1 or 0.

9. **price_known** (0 or 1)
   Do you already know, from memory, how the parent's shares reacted to this ruling? Answer 1 or 0. Do not look it up.

10. **reason** (text)
    In one sentence, explain the scores in columns A_money_score, B_core_business and C_disclosed.

## Order of columns in the exported CSV

`event_id,A_money_score,A_figure_usd,A_mcap_usd,A_source_url,B_core_business,C_disclosed,C_filing_accession,D_figure_stated,price_known,reason`

If Legora exports the columns in another order, leave them; Claude reorders by name without changing any value.
