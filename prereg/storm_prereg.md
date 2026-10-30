# Pre-registration: Project Storm (contagion to companies exposed to the same case)

Frozen before any result under this specification was computed. 30 October 2026. Adopts `prereg/cost_gate_prereg.md`.

## Hypothesis

The framework paper's contagion scope is the set of companies exposed to the same legal question, not the same industry. Fire's SIC peers are a coarse proxy for that set. A sharper and mechanical proxy is the set of listed non-party companies that name the case in their own 10-K or 10-Q before the ruling: they have judged it relevant to their business under their disclosure obligations. If that judgement is informative, these companies react to the ruling, and more than Fire's industry peers do.

Registered sign: positive. On ruling day the exposed basket's abs(z_0) exceeds its abs(z) on ordinary days.

## Population (mechanical)

1. Every ruling in the Earth universe (Supreme Court and Federal Circuit as Earth items 1 and 2) of the first Earth run whose universe contains the Federal Circuit for 2012 to June 2025. A listed party is not required; Supreme Court rulings between private parties or with government parties are in scope.
2. Search term: each side of the caption normalised as Earth item 3 and cut to its first two words; a side that is a bare government name (United States, a state, a federal agency) is dropped; if both sides drop, the ruling is out of scope.
3. Query: EDGAR full-text search for the quoted terms joined by AND (or the single remaining term with the word "Court"), forms 10-K and 10-Q, filed from 400 days before the ruling to the day before it.
4. Exposed companies: filers with a ticker in EDGAR's company list and at least one hit, excluding both parties and their Exhibit 21 parents where known. A ruling needs at least three exposed companies with price history covering 260 trading days before and ten after.

## Definitions

1. Basket: the equal-weighted mean of the exposed companies' market-model abnormal returns (as Earth). Basket sigma: the 60-day rolling standard deviation of the basket's abnormal return, lagged one day.
2. z_0 = basket AR_0 / basket sigma.
3. Basket drift: sign(basket AR_0) x basket CAR(+1,+5).

## Statistics

1. Primary: mean over rulings of abs(z_0); null distribution by drawing, for each ruling, one day at random from the basket's 250 trading days before the ruling (excluding the five days before it) and taking the mean of abs(z) across rulings; 10,000 draws, seed 20261030; one-sided p = share of draws at or above the observed mean.
2. Tradeable statistic (for the cost gate, if a drift claim is made): mean basket drift over rulings with abs(z_0) at or above 2, the position being the basket in the direction of its day-0 move from the close of day 0 to the close of day +5; cost is the weighted sum of each name's round-trip cost.
3. Secondary: mean basket drift and its bootstrap p (one-sided, continuation); for rulings that also have a Fire SIC basket, the paired difference in abs(z_0) between the Storm and Fire baskets; the number of exposed companies per ruling; each court separately.

## Decision rule (stated before the run)

- Support (exposure carries information): primary p below 0.05 with at least 20 rulings in scope.
- Kill: primary mean abs(z_0) at or below the null mean with at least 20 rulings.
- Unscorable: fewer than 20 rulings.
- Anything else: inconclusive.
- Separately, a drift claim is supported only if the basket drift is above zero with bootstrap p below 0.10 on at least 15 reacting rulings and the cost gate is passed; otherwise no drift claim is made.

## Known limitations (stated before the run)

- Two-word caption terms can match unrelated text (a common surname, a generic company word); requiring both sides' terms together limits this, but single-term rulings are noisier.
- Companies cite leading cases for years (Alice, eBay, KSR); a filer naming a case that is already decided is not exposed to the pending appeal of it. The 400-day window before the ruling limits this to citations of the pending case or of the decision below.
- EDGAR full-text search covers filings from 2001 and returns at most 100 hits per page; the runner pages through all hits.
- The runner, not this workspace, reaches EDGAR full-text search.
- One parameter set; no sensitivity sweep selects the reported result.
