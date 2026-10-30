# Project Water: materiality coding instructions (master prompt for Legora)

Paste everything below the line into Legora as the instruction for the review, and upload `input_moon37.csv` (37 rows) as the list of matters. Run it in a fresh workspace with no other documents.

---

You are coding the economic materiality of 37 US Supreme Court rulings to a listed company, for a pre-registered research study. Each row is one ruling; the party to the case is a subsidiary (or the company itself under an earlier name), and the listed company is identified by `parent_ticker` and `parent_cik`.

**Strict blindness rule.** You must not look at, search for, or rely on any share price, stock chart, market capitalisation history, analyst note, trading commentary or news coverage of how the company's shares reacted to the ruling. The study measures whether a lawyer's reading predicts the market's reaction, so any knowledge of the reaction invalidates the coding. If you already know from memory how the shares moved, set `price_known` to 1 for that row and still code it on the legal materials alone.

**Permitted sources.** The Supreme Court opinion and the opinion below (via the `oyez_url` or `scotus_docket_url` links, or any official or law-report copy); the parent company's 10-K and 10-Q filings on EDGAR filed **before** the ruling date (the `edgar_10k_before_ruling` and `edgar_10q_before_ruling` links list them); the parties' briefs.

**For each row, score three components and record one more field:**

A. **Money at stake relative to the parent** (`A_money_score`). Find the largest money figure that the ruling decides or puts at risk for the party: a damages award, a tax assessment, a class-wide exposure stated in the opinion or briefs, or an amount the parent disclosed for this case. Divide it by the parent's market capitalisation as stated on the cover page of the last 10-K filed before the ruling ("aggregate market value of the voting stock held by non-affiliates"). Score 2 if 5 per cent or more; 1 if at least 1 and under 5 per cent; 0 if under 1 per cent or if no figure can be found. Record the figure in `A_figure_usd`, the market value in `A_mcap_usd`, and where you found each in `A_source_url`.

B. **Core business** (`B_core_business`). 1 if the ruling directly governs one of the parent's core products, licences, franchises, patents, regulatory permissions, or its principal pricing or contracting practice (for example, an arbitration clause used in all its consumer contracts, or a tax that applies across its main network). 0 if it concerns a single employee, a single customer, a peripheral transaction or a procedural point of no wider effect on the business.

C. **Disclosed as material** (`C_disclosed`). 1 if the parent's last 10-K or 10-Q filed before the ruling names this case (or describes it unmistakably) in Legal Proceedings, the risk factors, or the contingencies note; 0 otherwise. Record the filing's accession number in `C_filing_accession` if 1.

D. **Figure stated** (`D_figure_stated`, recorded, not scored). 1 if the ruling itself, or the parent's disclosure, states a money figure for the consequence of the ruling; 0 otherwise.

Also record `price_known` (1 or 0, as above) and a one-sentence `reason` explaining the scores.

**Output.** Return one CSV with exactly these columns, in this order, one row per `event_id`, all 37 rows:

`event_id,A_money_score,A_figure_usd,A_mcap_usd,A_source_url,B_core_business,C_disclosed,C_filing_accession,D_figure_stated,price_known,reason`

Use plain numbers for USD amounts (no commas or currency signs). Leave a cell empty only where the instructions allow (no figure found, no accession because C is 0). Do not add a total; it is computed later.
