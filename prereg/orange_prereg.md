# Pre-registration: Project Orange (decision-day reaction and post-decision drift)

Frozen before any result under this specification was computed. 29 October 2026.

## Hypothesis

Katz, Bommarito, Soellinger and Chen (2017) report that abnormal returns after Supreme Court decisions accrue over hours and days rather than minutes, often overnight. Davis, Govindaraj and Suslava (2024) report no post-event drift at daily frequency over 500 cases. Orange replicates the daily-frequency question on the five pilot cases: after the decision-day abnormal return, does the litigant continue in the same direction over the following five trading days?

Registered sign: positive continuation (signed drift above zero), which is the Katz reading. The Davis reading is the null.

## Data

As Project Apple: daily adjusted closes for the litigant and SPY (yfinance, Stooq fallback); argument and decision dates from `data/ruling_cases.csv`, with the decision date required to match the Oyez API timeline or the slip-opinion listing (otherwise the case is excluded) and the argument date checked against Oyez where it responds.

## Sample

The five cases of Project Apple, fixed before any price was seen. For Google v. Oracle the registered ticker is ORCL; GOOGL is reported as a secondary leg and does not enter the decision rule.

## Definitions

1. Market model as Apple: residual abnormal return AR_t and estimation-window residual standard deviation sigma per case.
2. Day 0: the decision day. Opinions are released at 10:00 ET, so the day-0 close-to-close return contains the jump.
3. AR_0 and z_0 = AR_0 / sigma. A case has reacted if |z_0| is at or above 2.
4. Drift: CAR(+1,+5) = sum of AR over the five trading days after day 0. Signed drift = sign(AR_0) x CAR(+1,+5). CAR(+1,+1) is reported alongside because the overnight move Katz et al describe falls into day +1 at daily frequency.
5. Per-case statistic: z_c = signed drift / (sigma x sqrt(5)). Pooled statistic: Stouffer Z = sum of z_c / sqrt(n) over reacting cases; one-sided p from the normal distribution.
6. Secondary descriptive: CAR(-5,-1) before the decision, as a leakage check.

## Decision rule (stated before the run)

- Support: mean signed drift above zero over reacting cases, Stouffer p below 0.10, and at least three reacting cases.
- Kill: mean signed drift at or below zero with at least three reacting cases.
- Unscorable: fewer than three reacting cases.
- Anything else: inconclusive; no trading.

## Operator inputs deliberately left blank

Minimum effect worth pursuing, minimum event count for a live decision, and a ratified pre-mortem are for the operator and are not supplied here.

## Known limitations (stated before the run)

- Five cases chosen for salience: decision-day reactions are biased upward relative to the population Katz et al screened, and any drift found is conditional on a large day-0 move.
- Daily frequency cannot distinguish a slow intraday build from an overnight gap; CAR(+1,+1) is the nearest proxy.
- Myriad's decision-day path (an initial rise on a misread headline, then a fall) means AR_0 may have the opposite sign to the eventual move; the specification does not adjust for this.
- Five observations and a Stouffer combination: the test bounds, it does not establish.
- One parameter set; no sensitivity sweep is used to select the reported result.
