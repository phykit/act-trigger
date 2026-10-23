# Pre-registration: Anticipated-act trigger (objective GPR definition)

Frozen before any result under this specification was computed. 23 October 2026.

## Hypothesis

For conflicts with a visible prelude, the geopolitical risk premium is released at the act (Brune, Hens, Rieger and Wang, 2015; Goncalves, Melone and Ricciardi, 2025). After an anticipated act, Nasdaq-100 outperforms and implied vol falls over the following month; after a surprise act, it does not.

Registered sign: positive for anticipated acts (NDX 21-day return above baseline; bought call spread P&L above baseline). This is the hypothesis being tested, not a ratified programme input.

## Data

- Caldara and Iacoviello daily GPR (data_gpr_daily_recent, GitHub mirror iacoviel/iacoviel.github.io, vintage to 2026-10-19): GPRD_ACT, GPRD_THREAT.
- FRED: NASDAQ100, VXNCLS, VIXCLS.

## Event definition (no look-ahead; all percentiles on trailing data only)

1. Act day: GPRD_ACT on day t is at or above the 99th percentile of GPRD_ACT over the trailing 1,095 calendar days (t excluded).
2. De-clustering: an act day counts only if no act day occurred in the previous 30 calendar days.
3. Anticipated vs surprise: anticipated if the mean of GPRD_THREAT over days t-30 to t-1 is at or above the 75th percentile of the 30-day rolling mean of GPRD_THREAT over the trailing 1,095 days; otherwise surprise.
4. Sample: act days from 1988-01-01 (three years of burn-in) to 2026-09-20 (21 trading days of forward data required).

## Trade definition

- Entry: NDX close on the first trading day strictly after the act day (t+1 or later).
- Hold: 21 trading days.
- Primary outcome: P&L of a bought 1-month 100/108 NDX call spread, priced Black-Scholes off VXN at entry (VIX x 1.3 before VXN exists), settled on the realised NDX ratio; as a fraction of spot.
- Secondary outcomes: NDX 21-day return; VIX change over 21 days.
- Baseline: the same trade entered on every trading day 1988-2026 with entry vol between 15% and 45%.

## Decision rule (stated before the run)

- Support: anticipated-act mean call-spread P&L exceeds baseline with a one-sided bootstrap p below 0.10, and surprise-act mean does not exceed anticipated.
- Kill: anticipated-act mean at or below baseline, or fewer than 10 anticipated events.
- Anything else: inconclusive; no trading.

## Known limitations (stated before the run)

- GPR daily is published weekly (Mondays); a live trader would need a real-time news count or would enter up to a week late. This test validates the event classifier, not live latency.
- Flat-vol pricing ignores skew and bid-offer.
- One parameter set; no sensitivity sweep is used to select the reported result.
