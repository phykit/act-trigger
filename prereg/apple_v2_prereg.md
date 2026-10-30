# Pre-registration: Project Apple v2 (timing hazard in the argument-to-decision window)

Frozen before any result under this specification was computed. 30 October 2026.

Supersedes apple_prereg.md (SHA-256 068f59f04174f8018788084fb457ed9fa94d79da68ce902b34288af141dff17d) on one point only: the source of opinion days. The first run under v1 (results/apple_result_2026-10-30.md) found that supremecourt.gov retires slip-opinion listings once a bound volume is published, so OT2012 and OT2013 had no listing at all and the OT2017 listing began on 21 March 2018, after the Ohio v. American Express argument, which mislabelled the early opinion days of that window. Hypothesis, sample, definitions, statistic, test, placebo and decision rule are unchanged. The v1 result stands as recorded and is not superseded by this specification.

## Hypothesis

A Supreme Court ruling is a jump of unknown size at an unknown date inside a known window: the Court decides by the end of its term but on an unannounced day, and it releases opinions only on scheduled opinion days. If the equity market prices that timing hazard, the litigant's abnormal variance should be higher on opinion days on which its case could have been decided but was not than on days on which no ruling could arrive.

Registered sign: positive (the pooled ratio of mean squared standardised abnormal returns on non-decision opinion days to non-opinion days is above one). This is the hypothesis being tested, not a ratified programme input. The prior art is a null: Davis, Govindaraj and Suslava (2024) find no leakage or drift at daily frequency, and Katz, Bommarito, Soellinger and Chen (2017) find oral-argument returns uninformative about direction. Nobody has tested opinion-day variance.

## Data

- Daily adjusted closes for the litigant and SPY, from Yahoo Finance via yfinance, with Stooq as the fallback source. The source used is recorded in the result.
- Opinion days: the set of decision dates (`dateDecision`) recorded in the Supreme Court Database (SCDB, case-centred citation file, latest release reachable at run time, all decision types) for cases of that term. The derived list is written to `data/rulings/opinion_days_OT<yy>_scdb.csv` with the SCDB release used, and committed with the run. Where the supremecourt.gov slip-opinion listing still exists for the term it is read and the set difference against SCDB inside each window is reported as a cross-check; it does not enter the statistic.
- Argument and decision dates: `data/ruling_cases.csv`, recorded from recollection and checked at run time. The decision date must match the Oyez API timeline or the slip-opinion listing; a case whose decision date matches neither is excluded and the exclusion is reported. The argument date is checked against Oyez where Oyez responds, and is otherwise carried as recollection and flagged in the result.

## Sample (fixed before any price was seen)

Five merits cases with a US-listed party whose ticker still trades, one per term, chosen for salience and data availability:

| Case | Docket | Ticker | Argued | Decided |
|---|---|---|---|---|
| Association for Molecular Pathology v. Myriad Genetics | 12-398 | MYGN | 2013-04-15 | 2013-06-13 |
| Halliburton Co. v. Erica P. John Fund | 13-317 | HAL | 2014-03-05 | 2014-06-23 |
| Ohio v. American Express | 16-1454 | AXP | 2018-02-26 | 2018-06-25 |
| Google LLC v. Oracle America | 18-956 | ORCL | 2020-10-07 | 2021-04-05 |
| Amgen Inc. v. Sanofi | 21-757 | AMGN | 2023-03-27 | 2023-05-18 |

## Definitions

1. Market model: for each case, regress the litigant's daily log return on SPY's over the 250 trading days ending 10 trading days before the argument date. Abnormal return AR_t is the residual applied out of the estimation window; sigma is the estimation-window residual standard deviation; z_t = AR_t / sigma.
2. Window W: trading days from the first trading day after the argument date to the trading day before the decision date, inclusive. The decision day is excluded by construction.
3. Opinion day: a trading day in W on which SCDB records at least one decision of that term. Every opinion day in W is a non-decision opinion day for the case.
4. Statistic: R = (mean of z^2 over all opinion days in W, pooled across cases) / (mean of z^2 over all non-opinion days in W, pooled across cases). Per-case ratios are reported alongside.
5. Test: permutation. Within each case, the opinion-day labels are reassigned at random across the days of W, preserving the count per case; R is recomputed; 10,000 permutations with seed 20261029; one-sided p = share of permuted R at or above the observed R.
6. Placebo arm: the same ticker over the same calendar window shifted back exactly 364 days, with the same opinion-day labels shifted by 364 days, so that weekday composition is preserved and no ruling could have arrived. R_placebo and its permutation p are computed identically. Placebo dates that are not trading days are dropped.
7. Secondary descriptive: the share of days with |z| above 1 on opinion versus non-opinion days.

## Decision rule (stated before the run)

- Support: R above 1, permutation p below 0.10, and R above R_placebo.
- Kill: R at or below 1.
- Unscorable: fewer than 15 pooled opinion days in W, or fewer than four cases surviving the date checks.
- Anything else: inconclusive; no trading.

## Operator inputs deliberately left blank

Minimum effect worth pursuing, minimum event count for a live decision, and a ratified pre-mortem are for the operator and are not supplied here.

## Known limitations (stated before the run)

- Five cases. The test bounds the answer; it cannot establish it.
- Daily data cannot see the intraday and overnight build that Katz et al report; opinions are released at 10:00 ET, so the day-0 close-to-close captures the jump and the pre-10:00 positioning on a non-decision opinion day is diluted by the rest of the session.
- Opinion days are taken ex post from the recorded decision dates, and SCDB records summary per curiam decisions issued with order lists as well as announced opinions, so some labelled days are order days on which an argued case could not have been decided; this dilutes the opinion-day group towards the null. The Court's calendar announces non-argument opinion days only days in advance, so the ex ante set known at the start of W is smaller; the test therefore measures response to opinion days as realised, which is the stronger assumption.
- The placebo window may contain the ticker's own idiosyncratic events; the ORCL placebo window (October 2019 to April 2020) spans the COVID crash, which the market model only partly removes.
- The five cases were chosen for salience, which biases decision-day reactions upward but has no obvious bearing on non-decision opinion-day variance.
- One parameter set; no sensitivity sweep is used to select the reported result.
