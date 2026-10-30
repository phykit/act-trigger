# Pre-registration: Project Earth (post-ruling drift in the litigant against a like-for-like control)

Frozen before any result under this specification was computed. 30 October 2026.

## Hypothesis

When an appellate ruling moves a listed party's share price on the day it is released, the abnormal return over the following five trading days continues in the same direction, and does so more than after the same company's other large idiosyncratic moves. The first clause is the Katz, Bommarito, Soellinger and Chen (2017) reading of slow incorporation; the second is what makes it a claim about rulings rather than about large moves in general, since large idiosyncratic moves ordinarily reverse.

Registered sign: positive (ruling drift minus control drift above zero). The prior art is a null at daily frequency (Davis, Govindaraj and Suslava, 2024); Orange v1 and v2 found positive signed drift on two and eight reacting cases, below their floors.

## Universe (mechanical; no inspection)

1. Supreme Court: every case in the Supreme Court Database (SCDB, latest release reachable) for October Terms 2005 to 2024 with an argument date and a decision date, decision types 1, 5, 6 and 7 (argued cases decided by opinion, judgment, or an equally divided Court).
2. Federal Circuit: every opinion marked precedential released 1 January 2012 to 30 June 2025, from the CourtListener search API (court cafc, published status) where the runner can reach it anonymously, otherwise from the court's own opinions table where its data endpoint responds. If neither source responds, the Federal Circuit is absent from the run and the result says so.
3. Parties: the case name is split on " v. " and each side is matched to EDGAR's company list (`company_tickers.json`) after normalisation (upper case; punctuation removed; corporate suffixes Inc, Corp, Corporation, Co, Company, LLC, Ltd, LP, PLC, NA, Holdings, Group, The, AG, SA, SE, NV, BV removed; "et al" removed). An exact match on the normalised name is a listed party. A side with several names separated by ";" or "," is matched on its first name only.
4. Ticker: where a company has several tickers in the EDGAR list, the first listed is used. Price history must cover 260 trading days before the ruling and ten after; otherwise the event is excluded and listed.
5. One event per (ruling, ticker); a ruling with two listed parties gives two events.

## Definitions

1. Day 0: the release date (SCDB `dateDecision`; CourtListener `dateFiled`). Supreme Court opinions issue at 10:00 ET; Federal Circuit opinions issue during the session; both are inside the day-0 close-to-close return.
2. Market model: rolling 250-day OLS of the stock's log return on SPY's, lagged one day; abnormal return AR_t is the residual; sigma_t is the standard deviation of AR over the trailing 60 days, lagged one day; z_t = AR_t / sigma_t.
3. Reacting event: |z_0| at or above 2, and day 0 not within one trading day of an earnings release (an 8-K with item 2.02 for the company, from EDGAR submissions), and |SPY log return on day 0| at or below 2%.
4. Outcome: signed drift D = sign(AR_0) x CAR(+1,+5), where CAR sums AR over the five trading days after day 0.
5. Control: for each reacting event, the same company's other trading days within 252 trading days either side of day 0 on which |z| is at or above 2, excluding days within ten trading days of any ruling in the universe for that company and days within one trading day of an earnings release. The control value is the mean of sign(AR) x CAR(+1,+5) over those days. An event with fewer than three control days is dropped from the difference and listed.
6. Statistic: the mean over events of (D minus the event's control mean). Inference by bootstrap over events, 10,000 draws, seed 20261030; one-sided p = share of draws at or below zero.
7. Secondary descriptives: mean D alone and its Stouffer p, as in Orange; the reaction rate; the split by court and by whether the opposing party is a listed company.

## Decision rule (stated before the run)

- Support: mean difference above zero, bootstrap p below 0.05, at least 40 events in the difference.
- Kill: mean difference at or below zero with at least 40 events.
- Unscorable: fewer than 40 events in the difference.
- Anything else: inconclusive; no trading.

## Operator inputs deliberately left blank

Minimum effect worth pursuing (the round-trip cost in liquid names is roughly 10 to 20 bp and is the floor any supported effect must clear), minimum event count for a live decision, and a ratified pre-mortem are for the operator.

## Known limitations (stated before the run)

- Exact-name matching misses parties named differently from their EDGAR registration and matches nothing for subsidiaries; those are Project Moon's population, not an omission here.
- Federal Circuit release times are not timestamped in the source; an opinion released after the close would place the reaction on day +1 and the event would fail the reaction screen rather than contaminate it.
- Rolling estimates lag by one day, so a regime change in volatility between the estimation window and day 0 is not removed.
- The control conditions on |z| at or above 2 regardless of cause, so it contains earnings-adjacent and news-driven days other than those excluded; that is the intended comparison.
- Decision days cluster in June; the bootstrap treats events as independent.
- One parameter set; no sensitivity sweep is used to select the reported result.
