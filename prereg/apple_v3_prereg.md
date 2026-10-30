# Pre-registration: Project Apple v3 (timing hazard in the argument-to-decision window, wide sample)

Frozen before any result under this specification was computed. 30 October 2026.

Supersedes apple_v2_prereg.md (SHA-256 b84afa4aeeaddb8ca72c470d7656845f58c6550600ac0ffda76a56078c39682a) on two points: the sample, which moves from five cases chosen for salience to every case meeting a stated rule over October Terms 2012 to 2024, and the source of argument and decision dates, which moves from recollection to the Supreme Court Database. Hypothesis, definitions, statistic, test and placebo are unchanged; the decision rule's floors are raised to match the larger sample. The v1 and v2 results stand as recorded (v2: KILL on five cases, R = 0.64).

## Hypothesis

A Supreme Court ruling is a jump of unknown size at an unknown date inside a known window: the Court decides by the end of its term but on an unannounced day, and it releases opinions only on scheduled opinion days. If the equity market prices that timing hazard, the litigant's abnormal variance should be higher on opinion days on which its case could have been decided but was not than on days on which no ruling could arrive.

Registered sign: positive (the pooled ratio of mean squared standardised abnormal returns on non-decision opinion days to non-opinion days is above one). This is the hypothesis being tested, not a ratified programme input. The prior art is a null: Davis, Govindaraj and Suslava (2024) find no leakage or drift at daily frequency, and Katz, Bommarito, Soellinger and Chen (2017) find oral-argument returns uninformative about direction. Nobody has tested opinion-day variance.

## Data

- Daily adjusted closes for the litigant and SPY, from Yahoo Finance via yfinance, with Stooq as the fallback source. The source used is recorded in the result.
- Opinion days: the set of decision dates (`dateDecision`) recorded in the Supreme Court Database (SCDB, case-centred citation file, latest release reachable at run time, all decision types) for cases of that term. The derived list is written to `data/rulings/opinion_days_OT<yy>_scdb.csv` with the SCDB release used, and committed with the run. Where the supremecourt.gov slip-opinion listing still exists for the term it is read and the set difference against SCDB inside each window is reported as a cross-check; it does not enter the statistic.
- Argument and decision dates: SCDB `dateArgument` (or `dateRearg` where the case was reargued; the window opens after the last argument) and `dateDecision` for the registered docket. A docket absent from SCDB is excluded and listed. The Oyez API timeline is read where it responds and any disagreement with SCDB is reported; it does not exclude a case.

## Sample (fixed before any price was seen)

Every argued merits case of October Terms 2012 to 2024 (decided by 30 June 2025) in which a party named in the SCDB case name is i) a company whose common stock or NYSE-listed American depositary shares traded on NYSE or Nasdaq at the decision date and still trade there in October 2026 (a renamed ticker counts where it is the same security), or ii) a subsidiary, plan or committee of such a company whose SCDB name shares its leading name with the parent's listed name, plus Google LLC as the one named exception for Alphabet. Subsidiaries trading under other names, foreign parents without an NYSE or Nasdaq line, cases dismissed as improvidently granted, and companies delisted before October 2026 are excluded. One ticker per case: the petitioner's where the petitioner qualifies, otherwise the respondent's.

The register is `data/ruling_cases_wide.csv` (82 rows, with the basis for each). It was compiled by inspection of the Supreme Court dockets for those terms, not by code; any qualifying case omitted is a sampling omission, not a selection choice, and omissions found later are recorded in the result and may be added only under a new specification. Consolidated cases registered under a non-lead docket are expected to be absent from SCDB and are excluded by the date check.

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
- Unscorable: fewer than 200 pooled opinion days in W, or fewer than 40 cases surviving the date checks.
- Anything else: inconclusive; no trading.

## Operator inputs deliberately left blank

Minimum effect worth pursuing, minimum event count for a live decision, and a ratified pre-mortem are for the operator and are not supplied here.

## Known limitations (stated before the run)

- Daily closes on 82 registered cases at most, many of them with small economic stakes relative to the company; dilution towards the null is expected and is the price of a mechanical register.
- Daily data cannot see the intraday and overnight build that Katz et al report; opinions are released at 10:00 ET, so the day-0 close-to-close captures the jump and the pre-10:00 positioning on a non-decision opinion day is diluted by the rest of the session.
- Opinion days are taken ex post from the recorded decision dates, and SCDB records summary per curiam decisions issued with order lists as well as announced opinions, so some labelled days are order days on which an argued case could not have been decided; this dilutes the opinion-day group towards the null. The Court's calendar announces non-argument opinion days only days in advance, so the ex ante set known at the start of W is smaller; the test therefore measures response to opinion days as realised, which is the stronger assumption.
- The placebo window may contain the ticker's own idiosyncratic events; placebo windows falling in February to April 2020 span the COVID crash, which the market model only partly removes.
- The register was compiled by inspection, so coverage errors are possible; they are visible in the register and do not depend on any price.
- One parameter set; no sensitivity sweep is used to select the reported result.
