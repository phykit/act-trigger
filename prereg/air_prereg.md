# Pre-registration: Project Air (forward test on rulings not yet decided)

Frozen 30 October 2026, before any OT2026 Supreme Court opinion in an argued case and before any event under this specification was observed. Adopts `prereg/cost_gate_prereg.md`.

## Purpose

Every historical thread (Earth, Moon, Water, Strife, Void, Death) is exposed to two contaminations that no amount of care removes: hindsight in the choice of design after earlier runs, and AI coders that may remember famous past price reactions. Air applies the same predictions to rulings that have not happened yet. Its results are the only ones in this programme that can support a trading decision.

## Populations

1. **Supreme Court register.** Every (case, ticker) row in `data/air/ot2026_register.csv`, a list of October Term 2026 cases granted review with a listed party (category a), a listed parent of a subsidiary party (category b), or a federal or state party in a case that directly governs an identifiable listed industry (category c, with two to five named tickers). A row counts only if the commit that adds it to the repository precedes the case's decision date; the git commit time is the record. Rows may be added after this specification is frozen; they count from their commit time. No row is ever removed or edited after commit; a correction is a new row, and the superseded row is listed as such in `data/air/register_corrections.csv`.
2. **Federal Circuit, mechanical.** Every precedential Federal Circuit opinion released after 30 October 2026 and before 1 July 2027, with parties matched to EDGAR's company list exactly as Earth item 3 (direct parties) and through Exhibit 21 as Moon (parents). No register is needed: the rule is frozen here.

## Capture (automated; no human step)

1. A scheduled workflow runs each US trading day after the close. It detects new decisions (the Supreme Court's slip-opinion page for the term; the Federal Circuit's opinions list, or CourtListener where the court's page does not respond) and, for each event, records the decision date and the release time where the source gives one. The formal outcome is coded afterwards from the opinion itself (Supreme Court: affirmed, reversed, vacated, or mixed, from the syllabus line; Federal Circuit: the disposition line), mechanically and before any return for that event is computed.
2. Within seven calendar days of the decision, it stores one-minute bars (yfinance) for every ticker on the event's row and for SPY, and daily closes from 260 trading days before to ten after once available. One-minute history older than seven days cannot be fetched later; an event whose capture window is missed is listed as missed, not back-filled.
3. Each capture is committed with its fetch time. Nothing is recomputed from later downloads.

## Pre-decision coding (Water, forward)

Before a register case is decided, the Water API coder (`scripts/ai_coder.py`, same model, same rubric) codes A, B, C and D for each category a and b row from a pre-decision pack: the question presented, the opinion of the court below, and the parent's last 10-K and 10-Q filed before the coding date. The coded sheet is committed before the decision. This is the forward version of Water: the coder cannot know the outcome or the reaction.

## Predictions tested (registered signs, all positive)

1. **Earth-forward.** For direct-party events with abs(z_0) at or above 2 (z as Earth), sign(AR_0) x CAR(+1,+5) is above zero.
2. **Moon-forward.** For category b events, direction x CAR(+1,+5) is above zero, with direction = +1 if the parent's subsidiary won formally and -1 if it lost; mixed outcomes are excluded and listed.
3. **Water-forward.** Among Supreme Court category a and b events, mean abs(z_0) is higher for high-stakes rows (A + B + C at or above 2) than for low-stakes rows (manipulation check), and mean signed drift as in 1 and 2 is higher for high-stakes rows.
4. **Intraday (framework Stage III).** For reacting events with one-minute data, the share of the day-0 abnormal move (stock minus beta x SPY, beta from the daily market model) completed by +30 minutes after release, where the release time is known. No sign is registered; this is descriptive and answers whether the edge, if any, is in seconds (the framework's claim) or in days (Earth's).

## Paper-trading log

For every event in predictions 1 and 2, a notional position is entered at the close of day 0 in the predicted direction and exited at the close of day +5, equal notional per event. The log records gross return, the cost-gate round-trip cost, and net return. No position is ever taken with money under this specification.

## Statistics and decision rule (evaluated once, after 1 July 2027 captures complete)

1. Predictions 1 and 2 pooled: mean net return of the paper-trading log; one-sided bootstrap p, 10,000 draws, seed 20261030.
   - Support: mean net return above zero, p below 0.10, at least 15 events. A Support is the programme's first evidence that would justify a live, small-scale trading test, subject to the operator's minimum effect and event count.
   - Kill: mean gross return at or below zero with at least 15 events. A kill of Air closes the drift hypothesis for this programme regardless of the historical results.
   - Unscorable: fewer than 15 events. The register then rolls into OT2027 under a new version, with the OT2026 events carried forward.
   - Anything else: inconclusive.
2. Prediction 3: reported with its own permutation p (10,000 draws, seed 20261030); Support requires the manipulation check to pass and p below 0.10 on at least 8 high-stakes events.
3. Prediction 4: reported, not scored.
4. Each prediction is also reported by court and by category.

## Known limitations (stated before the run)

- One Supreme Court term yields few events: at the historical rate (about one in ten listed-party rulings reacts at abs(z_0) of 2 or more), the register alone may give two or three reacting events. The Federal Circuit population is what makes the 15-event floor reachable, and it is mechanical, so it carries the Earth universe's matching limits.
- yfinance one-minute data is retained for seven days and is not an audited source; a missed capture is a lost event.
- Supreme Court opinion release times are within the 10:00 Eastern sitting; Federal Circuit opinions are posted without a stated time, so the intraday measure is mostly a Supreme Court measure.
- Category c rows (industries affected by government cases) rest on a judgement made when the row is added; that judgement is dated and frozen but not mechanical.
- Paper trades ignore borrow, capacity and the operator's own execution; the cost gate is an estimate.
