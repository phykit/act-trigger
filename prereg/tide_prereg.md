# Pre-registration: Project Tide (continuation after a decisive legal decision, tested as a trade net of costs)

Registered 31 October 2026, before any Patent Trial and Appeal Board (PTAB) record or any price for the PTAB arm was read. It adopts the cross-thread cost gate, `prereg/cost_gate_prereg.md`, by name.

## Question

When a listed party's share price makes a large idiosyncratic move on the day a decisive legal decision is published, does the move continue over the following five trading days by enough to pay for trading it?

## Why Tide exists, and what the analyst has seen

1. Earth v2 (run of 31 October 2026, `results/earth_v2_result_2026-10-31.md`) returned Support on 40 reacting events, the registered minimum.
2. After that run, and before this specification, the analyst computed these totals on Earth v2's 40 reacting events:
   - mean signed drift +4.74%, median +1.82%;
   - 29 of 40 positive;
   - 23 long events at +4.32% and 17 short events at +5.30%;
   - the three largest events carry 81% of the summed drift, and the mean without them is +0.99% (+0.17% without the largest five);
   - the median absolute z on day 0 is 2.4, and the median daily residual volatility is 1.15%.

   No per-event result was read, and no cost estimate for those events has been computed.
3. Two weaknesses follow: Earth trades about twice a year, and its mean rests on a handful of events. Tide therefore:
   - tests the same mechanism where decisions are frequent (the PTAB arm, which decides Tide);
   - prices Earth's own events net of costs (the Earth arm, a companion that cannot decide Tide, because its gross totals have been seen);
   - adds two conditions that a result carried by a few events cannot meet.

## Arms

1. **PTAB arm, final written decisions (primary; decides Tide).**
   - Source: USPTO Open Data Portal, PTAB trials API (`api.uspto.gov/api/v1/patent/trials/`), decisions and proceedings.
   - Population: every final written decision in an inter partes review, post-grant review or covered business method review.
   - Primary sample: decision dates 1 January 2014 to 30 June 2025.
   - Holdout: decision dates 1 July 2025 to 30 September 2026. It is computed and reported separately, never pooled with the primary sample.
2. **PTAB arm, institution decisions (secondary).** As item 1, for decisions granting or denying institution of a trial. It is reported with the same statistic and Holm's correction across the two PTAB arms. It cannot decide Tide.
3. **Earth arm (companion).** The 40 reacting events of Earth v2's run of 31 October 2026, read from `results/earth_v2_result_2026-10-31.events.csv`, with Earth's day 0 and Earth's timing (item 7). It is reported under the same rule but labelled a companion. Its gross totals are known (above), so it measures the effect of costs on Earth's result and nothing more.

## PTAB counting rules

1. **Decision type.** The ODP decision record's own type field identifies the decision. A final written decision includes one entered on remand or after rehearing only if the record types it as a final written decision. Decisions on rehearing requests, terminations, settlements, adverse judgments and orders are excluded.
2. **Decision date.** Day 0 is the decision's issue date in the ODP record. A date that is not a trading day moves to the next trading day.
3. **Parties.**
   - The patent owner side is the patent owner name and every real party in interest listed for the patent owner.
   - The petitioner side is the petitioner name and every real party in interest listed for the petitioner.
   - Each name is matched to EDGAR's company list exactly as Earth v1 item 3 (same normalisation, exact match, same exclusion of governments and individuals).
   - A ticker matched on both sides of the same trial is excluded from that trial.
4. **One event per (ticker, day 0).** Several decisions issued on one day that involve the same listed company are one event. The event's side is the side that company is on. If it is on different sides in different trials that day, the event is excluded.
5. **Overlapping events.** Events for a ticker are taken in date order. An event whose day 0 falls within six trading days after the day 0 of the last event kept for that ticker, in the same arm, is excluded. This means within the kept event's reaction and holding window. The rule is applied before the reaction screen, so it does not depend on prices.
6. **Ticker and price history:** as Earth v1 item 4 (the first ticker in the EDGAR list; 260 trading days of history before day 0 and ten after).

## Definitions

1. **Market model and z.** As Earth v1 definition 2: a rolling 250-day OLS on SPY, lagged one day; residual volatility sigma over the trailing 60 days, lagged one day.
2. **Timing, PTAB arms.** The ODP record carries a date but no time. To ensure the decision was public before entry, the reaction is measured over two days and the position is entered at the close of day +1.
   - Reaction: R = AR(0) + AR(+1), and z = R / (sigma × √2), with sigma taken at day 0.
   - Reacting event: |z| at or above 2.
   - Screens: SPY's return within ±2% on both day 0 and day +1, and no 8-K item 2.02 filing within two business days of day 0 or of day +1.
   - Position: in the direction of R, from the close of day +1 to the close of day +6.
   - Gross return: G = sign(R) × CAR(+2, +6).
3. **Timing, Earth arm.** As Earth: reaction on day 0 (|z_0| at or above 2, with Earth's screens), position from the close of day 0 to the close of day +5, and G = sign(AR_0) × CAR(+1, +5). This assumes a position can be taken at the closing auction once the day's move is known. Supreme Court opinions issue at 10:00 ET and Federal Circuit opinions during the court's session, so the decision is public by then.
4. **The position.** Long or short the stock, hedged with SPY at the event's lagged beta. G is its return, measured as the sum of daily market-model residuals.
5. **Cost (cost gate).**
   - Round trip on the stock = twice its Corwin and Schultz spread over the 20 trading days ending the day before day 0.
   - Plus |beta| times twice SPY's spread over the same days.
   - Net return N = G minus that cost.
   - An event whose cost cannot be computed is excluded from every statistic and counted.
6. **Control (secondary, PTAB arms).**
   - For each reacting event, the control days are the same company's other trading days within 252 trading days either side of day 0 on which the two-day z, defined as in item 2, is at or above 2.
   - Days within ten trading days of any PTAB decision for that company are excluded, as are days within two business days of an 8-K item 2.02 filing and days on which SPY moved more than 2% on either day.
   - Control value: the mean of sign(R) × CAR(+2, +6) over those days.
   - Reported statistic: the mean of (G minus control) with its bootstrap p, over events with at least three control days. It shows whether a decision's move continues more than the company's other large moves. It does not decide Tide.

## Statistics and decision rule

Statistics, for each arm:

- **Tradeable statistic:** the mean of N over reacting events.
- **Inference:** a bootstrap over events, 10,000 draws, seed 20261030; one-sided p is the share of draws at or below zero.
- **Concentration conditions:**
  - the median of N is above zero;
  - the mean of N, after removing the largest 5% of events by N (at least two events), is above zero.

**PTAB final-written-decision arm, primary sample (decides Tide):**

- **Support:** mean N above zero; bootstrap p below 0.05; both concentration conditions met; at least 100 reacting events with costs.
- **SUPPORT (GROSS ONLY):** the same conditions are met on G but not on N. This is not a Support.
- **Kill:** mean N at or below zero, with at least 100 reacting events with costs.
- **Unscorable:** fewer than 100 reacting events with costs.
- **Inconclusive:** anything else.

**Holdout:** reported with the same statistics. It does not change the verdict. A Support is carried forward to paper trading only if the holdout's mean N is also above zero. Otherwise it is reported as "Support, not confirmed in the holdout".

**PTAB institution arm:** reported under the same rule, labelled secondary, with Holm's correction across the two PTAB arms.

**Earth arm:** reported under the same rule with a minimum of 40 events, labelled companion. It cannot turn any PTAB verdict into a Support.

**Secondary descriptives (all arms):**
- mean G;
- the share of events with N above zero;
- the median cost;
- long and short events separately (short events carry no borrow cost; item 2 of the limitations);
- patent owner and petitioner sides separately;
- by year.

## Known limitations (stated before the run)

1. **Survivorship.** EDGAR's company list and the price source cover companies listed now. Companies since delisted or acquired are missing, and the direction of the resulting bias is unknown.
2. **Costs.** The cost of borrowing stock for short positions is not estimated. Corwin and Schultz is noisy in thin names. Market impact beyond the doubled spread is not modelled.
3. **Timing.**
   - Entry at the close of day +1 forgoes any continuation on day +1 when the decision was published before the close of day 0.
   - The Earth arm's entry at the close of day 0 assumes a closing-auction order placed on the day's move.
4. **Outcomes.** Final written decisions are often anticipated from the institution decision and the oral hearing, so their surprise content is lower than the Federal Circuit's. Claim-level outcomes are not used.
5. **Clustering.** Events share dates (several trials decided together) and companies (frequent petitioners). The bootstrap treats events as independent.
6. **One parameter set.** No sensitivity sweep is used to choose the reported result.

## Operator inputs left blank

These are for the operator:
- a minimum net effect worth trading above the cost gate's floor;
- position sizing;
- a ratified pre-mortem.

Implementation: `scripts/tide_ptab_fetch.py` (ODP fetch and flattening), `scripts/tide.py` (events, costs, statistics), `.github/workflows/tide.yml`.
