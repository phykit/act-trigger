# Pre-registration: Project Orange v2 (decision-day reaction and post-decision drift, wide sample)

Frozen before any result under this specification was computed. 30 October 2026.

Supersedes orange_prereg.md (SHA-256 c12e7b2990f4e211c8afafed5bf40f840b1675c15f4fb5f971781a7da7caa2cd) on the sample and the date source only, as apple_v3_prereg.md does for Apple. The v1 result stands as recorded (UNSCORABLE: two of five cases reacted).

## Hypothesis

Katz, Bommarito, Soellinger and Chen (2017) report that abnormal returns after Supreme Court decisions accrue over hours and days rather than minutes, often overnight. Davis, Govindaraj and Suslava (2024) report no post-event drift at daily frequency over 500 cases. Orange replicates the daily-frequency question on the five pilot cases: after the decision-day abnormal return, does the litigant continue in the same direction over the following five trading days?

Registered sign: positive continuation (signed drift above zero), which is the Katz reading. The Davis reading is the null.

## Data

Daily adjusted closes for the litigant and SPY (yfinance, Stooq fallback). Argument and decision dates from SCDB `dateArgument` (or `dateRearg`) and `dateDecision` for the registered docket; a docket absent from SCDB is excluded and listed; the Oyez timeline is reported as a cross-check and does not exclude.

## Sample

The register of apple_v3_prereg.md, `data/ruling_cases_wide.csv`, fixed before any price was seen, with the same one-ticker-per-case rule. No secondary legs.

## Definitions

1. Market model as Apple: residual abnormal return AR_t and estimation-window residual standard deviation sigma per case.
2. Day 0: the decision day. Opinions are released at 10:00 ET, so the day-0 close-to-close return contains the jump.
3. AR_0 and z_0 = AR_0 / sigma. A case has reacted if |z_0| is at or above 2.
4. Drift: CAR(+1,+5) = sum of AR over the five trading days after day 0. Signed drift = sign(AR_0) x CAR(+1,+5). CAR(+1,+1) is reported alongside because the overnight move Katz et al describe falls into day +1 at daily frequency.
5. Per-case statistic: z_c = signed drift / (sigma x sqrt(5)). Pooled statistic: Stouffer Z = sum of z_c / sqrt(n) over reacting cases; one-sided p from the normal distribution.
6. Secondary descriptives: CAR(-5,-1) before the decision as a leakage check; the share of cases that reacted, for comparison with the 37 per cent Katz et al report on their screened candidates.

## Decision rule (stated before the run)

- Support: mean signed drift above zero over reacting cases, Stouffer p below 0.10, and at least 15 reacting cases.
- Kill: mean signed drift at or below zero with at least 15 reacting cases.
- Unscorable: fewer than 15 reacting cases.
- Anything else: inconclusive; no trading.

## Operator inputs deliberately left blank

Minimum effect worth pursuing, minimum event count for a live decision, and a ratified pre-mortem are for the operator and are not supplied here.

## Known limitations (stated before the run)

- The register is mechanical, so most cases carry small stakes and will not react; any drift found is conditional on a large day-0 move and on the reaction threshold.
- Daily frequency cannot distinguish a slow intraday build from an overnight gap; CAR(+1,+1) is the nearest proxy.
- Where the decision-day headline is misread (Myriad, 2013), AR_0 may have the opposite sign to the eventual move; the specification does not adjust for this.
- A Stouffer combination over reacting cases treats cases as independent; decision days cluster in late June, so market-wide shocks on those days are shared.
- One parameter set; no sensitivity sweep is used to select the reported result.
