# Project Water: column prompts for Legora Tabular Review

Use these if you run the coding as a tabular review (one row per matter, one column per question) rather than as a single prompt. Load `input_moon37.csv` as the rows. Put the blindness rule from `prompt_master.md` in the review's general instructions so it applies to every column.

| Column | Question to set | Expected answer |
|---|---|---|
| `A_figure_usd` | What is the largest money amount this Supreme Court ruling decides or puts at risk for the party (damages, tax, class exposure, or an amount the parent disclosed for this case)? Give a number in US dollars, or leave blank if none can be found. Do not use share prices. | Number or blank |
| `A_mcap_usd` | What aggregate market value of voting stock held by non-affiliates is stated on the cover page of the parent's last 10-K filed before the ruling date? | Number |
| `A_money_score` | Divide A_figure_usd by A_mcap_usd. Answer 2 if 5% or more, 1 if at least 1% and under 5%, 0 if under 1% or if A_figure_usd is blank. | 0, 1 or 2 |
| `A_source_url` | Give the URLs where you found A_figure_usd and A_mcap_usd. | URLs |
| `B_core_business` | Does the ruling directly govern one of the parent's core products, licences, franchises, patents, regulatory permissions, or its principal pricing or contracting practice? Answer 1 or 0. | 0 or 1 |
| `C_disclosed` | Does the parent's last 10-K or 10-Q filed before the ruling date name or unmistakably describe this case in Legal Proceedings, risk factors or the contingencies note? Answer 1 or 0. | 0 or 1 |
| `C_filing_accession` | If C_disclosed is 1, give the accession number of that filing. | Accession or blank |
| `D_figure_stated` | Does the ruling, or the parent's disclosure, state a money figure for the consequence of the ruling? Answer 1 or 0. | 0 or 1 |
| `price_known` | Do you already know, from memory, how the parent's shares reacted to this ruling? Answer 1 or 0. Do not look it up. | 0 or 1 |
| `reason` | In one sentence, explain the scores. | Text |

Export the review as CSV with the columns in this order:

`event_id,A_money_score,A_figure_usd,A_mcap_usd,A_source_url,B_core_business,C_disclosed,C_filing_accession,D_figure_stated,price_known,reason`
