# Pre-registration: Project Wood (the issuer's own pre-ruling disclosure as a measure of stakes)

Frozen before any result under this specification was computed. 30 October 2026.

## Hypothesis

A listed issuer that names a pending appeal in its 10-K or 10-Q (Legal Proceedings, risk factors, contingencies note) has judged it material under its disclosure obligations. If that judgement is informative, rulings in disclosed cases move the issuer's price more than rulings in undisclosed cases. This is a mechanical, price-free and pre-ruling measure of stakes, available for every event, and it is the free substitute for the framework's options-implied prior.

Registered sign: positive. Mean abs(z_0) is larger for disclosed events.

## Population

Every Earth event (listed party, exact match) and every Moon event (listed parent through Exhibit 21) with status `ok` in the first Earth and Moon runs whose universe contains Federal Circuit opinions for the whole of 2012 to June 2025.

## Disclosure test (mechanical)

1. Search term: the opposing side's name from the case caption, normalised as in Earth (suffixes, "et al." and role labels removed), then cut to its first three words. If the opposing side is a bare government name (United States, a state, or a federal agency without a distinctive name of three or more words) the event is unscorable for Wood and is listed.
2. Query: EDGAR full-text search for the quoted term, restricted to the issuer's CIK (the parent's CIK for Moon events), forms 10-K and 10-Q, filed from 400 days before the ruling to the day before it.
3. Disclosed = at least one hit. The accession number of the first hit is recorded.

## Statistics

1. Primary: mean abs(z_0) for disclosed events minus undisclosed events; one-sided permutation p over the labels, 10,000 draws, seed 20261030.
2. Secondary: among reacting events (abs(z_0) at or above 2), mean signed CAR(+1,+5) for disclosed minus undisclosed events; the share of events disclosed by court and by population; agreement between Wood's disclosed flag and Water's component C where both exist.

## Decision rule (stated before the run)

- Support: primary difference above zero, permutation p below 0.05, and at least 20 disclosed events.
- Kill: primary difference at or below zero with at least 20 disclosed events.
- Unscorable: fewer than 20 disclosed events.
- Anything else: inconclusive.

## Known limitations (stated before the run)

- A three-word name can match unrelated text in the same filing (a customer or supplier of the same name); the search is restricted to the issuer's own filings to limit this.
- Full-text search covers filings from 2001; all events in scope are later.
- Issuers sometimes describe a case without naming the opposing party (for example "a patent infringement action in Delaware"), which is a miss for this test; misses dilute towards the null.
- Loss-contingency accrual amounts (XBRL `LossContingencyAccrualAtCarryingValue`, `LossContingencyEstimateOfPossibleLoss`) are not used here; they are aggregated across cases and would need case-level coding (Water).
- One parameter set; no sensitivity sweep selects the reported result.
