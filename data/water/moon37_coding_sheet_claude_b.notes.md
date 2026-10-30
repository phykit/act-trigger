# Coder 2b (Claude run B): notes returned with the sheet, in substance

- sec.gov, data.sec.gov, efts.sec.gov and court hosts were blocked from the agent's shell, EDGAR browse pages could not be fetched, and Firecrawl had no credits; filings were read with WebFetch from document URLs found by web search (W12 via the capedge mirror).
- WebFetch reads about the first 100,000 characters; C = 0 for W02, W05, W13, W20, W21, W23, W25, W27, W28, W29, W33 means "not found in the text that could be read".
- Figures not re-verified from primary text: W03, W16, W21, W25, W26 from recollection of the opinions; W28's $8.8bn from a law-firm case note.
- W37's C = 1 rests on a search-index hit plus recollection; the filing text was cut off before the contingencies note.
- W35's non-affiliate market value ($22.2bn) recorded as stated on the cover although it looks low.
- price_known = 0 throughout; no share-price material consulted.
