# Appellate rulings and listed securities: investigation register

Opened 30 October 2026. One row per thread; each thread has its own frozen specification under `prereg/` and appends its results under `results/`. Threads are named after primal elements. Specifications are never edited; a change is a new, separately hashed version. Status is as at the date in the row.

## Threads

| Thread | Question | Registered hypothesis (sign) | Data | Status |
|---|---|---|---|---|
| Apple (v1 to v3) | Does the litigant's abnormal variance rise on opinion days before its own ruling? | Higher on non-decision opinion days (positive) | SCDB, yfinance | Closed. v3 (77 cases): R = 1.000, p = 0.41, INCONCLUSIVE; a null at daily frequency |
| Orange (v1, v2) | After a decision-day move, does the litigant drift on? | Continuation (positive) | As Apple | Closed. UNSCORABLE (2 and 8 reacting cases); direction positive in both |
| Earth | Post-ruling drift in the litigant against the same company's other large moves | Positive | SCDB, GovInfo (Federal Circuit, v2), EDGAR, yfinance | v1 runs 6 and 8 retired (truncated Federal Circuit lists). Earth v2 registered 31 October 2026 (`prereg/earth_v2_prereg.md`): GovInfo source, Federal Circuit 1 April 2013 to 30 June 2025, mandamus excluded, every named party, point-in-time Exhibit 21 parent arm (secondary). Review: `data/appeals/govinfo_review/README.md` |
| Moon | Propagation of a Supreme Court ruling to the listed parent of a subsidiary party | Positive signed drift | SCDB, EDGAR Exhibit 21 | SUPPORT on 37 events (+2.57%, p = 0.026); fragile to one outlier and four misrouted direct parties |
| Fire | Spillover to the litigant's SIC peers, signed by the litigant's reaction | Positive | As Earth, EDGAR SIC | UNSCORABLE (9 events); awaits run 7 |
| **Water** | Does a lawyer's blind reading of materiality predict which events move and drift? | High-stakes events drift more (positive) | Judgments, 10-K and 10-Q disclosures; no prices | Specified 30 October 2026; v3 in force (`prereg/water_v3_prereg.md`, with amendments 1 and 2 of 30 October 2026 taking the Supreme Court opinion from the Court's own site or GovInfo before CourtListener): AI coders only. Coder 3, the API coder (`scripts/ai_coder.py`, workflow `water-coder`, model `claude-sonnet-5-5`), is primary; Legora (coder 1) and two Claude agent runs (2, 2b; kappa 1.00 between them) are reported alongside. Kit in `data/water/legora/` |
| **Wood** | Does the issuer's own pre-ruling disclosure of the case (Item 3, contingencies note) predict the size of the reaction? | Disclosed cases react more (positive) | EDGAR full-text search, 10-K and 10-Q | Specified 30 October 2026 (`prereg/wood_prereg.md`) |
| **Metal** | Framework thesis: does legal complexity slow price discovery? | Complex rulings show larger post-ruling abnormal movement (positive) | CourtListener opinion text and counts, SCDB disposition | Specified 30 October 2026 (`prereg/metal_prereg.md`) |
| **Strife** | Framework "Pyrrhic victory": when the price moves against the formal outcome, who is right, the price or the headline? | The price: drift continues in the day-0 direction (positive) | SCDB partyWinning, Earth and Moon events | Specified 30 October 2026 (`prereg/strife_prereg.md`) |
| **Void** | Framework quantification gap: do rulings with no stated money figure drift more? | No-figure events drift more, within stakes strata (positive) | Water coder 3's coding (component D); Moon and Earth returns | Specified 30 October 2026 (`prereg/void_prereg.md`); runs with Water |
| **Death** | Framework pair trades: where both sides are listed, does the long-winner, short-loser pair drift on, against the same pair's other large moves? | Continuation (positive) | Earth universe, both sides listed | Specified 30 October 2026 (`prereg/death_prereg.md`); population known after run 8 |
| **Storm** | Framework contagion scope: do non-party companies that name the case in their own 10-K or 10-Q before the ruling react to it, and more than Fire's SIC peers? | Exposed basket reacts on ruling day (positive) | EDGAR full-text search; Earth universe | Specified 30 October 2026 (`prereg/storm_prereg.md`); runs on GitHub with Wood |
| **Air** | Forward test: Earth, Moon and Water predictions applied to rulings not yet decided, with a paper-trading log net of costs | Positive (Earth-forward, Moon-forward, Water-forward); intraday share descriptive | OT2026 register (frozen per row by commit time); Federal Circuit precedential opinions after 30 October 2026, matched mechanically; one-minute bars within seven days | Specified and frozen 30 October 2026 (`prereg/air_prereg.md`); daily capture workflow `air` live; Supreme Court register being compiled. Evaluated once, after 1 July 2027 |
| **Love** | Delaware Supreme Court corporate-law rulings and listed parties | Earth, Moon and Water designs applied to Delaware | CourtListener (court `del`), covered by the existing token | Backlog (third in the agreed order) |
| **Aether** | UK Supreme Court and Court of Appeal: does the one-week (UKSC) or one-day (CoA) public hand-down notice move the litigant, and is there drift after hand-down? | Variance rises at listing; drift as Earth | Find Case Law API, UKSC future-judgments archive (Wayback), LSE prices via yfinance | Backlog |
| **Ice** | Prediction-market prior: do Kalshi and Polymarket odds on Supreme Court cases measure legal surprise, and does surprise predict drift? | Larger surprise, larger drift | Kalshi and Polymarket public market data | Backlog; feeds Air |
| **Light** | Supreme Court author inference: does the litigant move on the date the opinion's author becomes inferable from released opinions? | Price moves on inference date, in the direction implied by the author | SCDB (opinion author, sitting) | Backlog |
| **Thunder** | US circuits: does panel disclosure move the litigant? | Unfavourable panel, negative move | CourtListener dockets (`panel`, `date_argued`), circuit calendars | Backlog; excludes the 4th, 7th and Federal Circuits, which name panels on argument day |
| **Shadow** | Framework Stage II priors from options (straddles, 25-delta risk reversals), credit (CDS, bonds) and intraday (+5m, +30m) history | Options-implied move and skew predict surprise | Paid data only (OptionMetrics, Markit, TRACE history, intraday vendor) | Parked: no free source. Forward intraday capture is folded into Air |

## Mark-up of the framework paper (Appellate Judgment Event-Driven Strategy Framework)

Verdict in one line: the paper's core thesis, that complexity slows incorporation, is consistent with what Earth has found so far and is testable on free data; the parts that depend on options, credit and intraday history are not testable without paid data, and the claim that the edge is measured in seconds conflicts with the multi-day drift we observe.

| Paper element | Assessment | Where it goes |
|---|---|---|
| Core thesis: alpha is interpretation latency, not network latency | Accepted as a hypothesis. Earth's drift over days (9 of 11 continuing in run 6) and Katz et al. (2017) both point to slow interpretation, not fast feeds | Metal tests it directly |
| "Determine within seconds of public release" | Rejected as a research requirement. If the drift runs over days, seconds add nothing measurable on daily data; the claim is untestable without intraday history | Air captures intraday prices prospectively |
| Materiality = change in value / market capitalisation | Accepted; this is Water's rubric, with the numerator from the judgment and the issuer's own disclosures | Water, Wood |
| Legal surprise = realised minus expected outcome | Accepted in principle; the expected term needs a prior. Free priors: issuer disclosure (Wood), prediction markets (Ice), the market's own day-0 move (Earth, Strife). Options and CDS priors are Shadow | Wood, Ice, Strife |
| Stage I universe across UK, EU, South Africa, Australia, Canada and US courts | Narrowed. US and UK first: free judgment feeds, free prices, and enough listed-company litigation. EU (EUR-Lex), Canada (CanLII, free key on request) and Australia later; South Africa and Australia have limited free bulk access | Love, Aether; others backlog |
| Corporate hierarchy mapping to the ultimate listed issuer and its instruments | Accepted. Exhibit 21 matching (Moon) misrouted four of 37 events; filings that name the case (Wood) give a second, more direct link | Moon, Wood |
| Pre-release scenario matrix (branches, probabilities, value impacts) | Accepted for prospective use only. A historical scenario tree built now is contaminated by hindsight, and any language model asked to build one knows the outcomes of past cases | Air |
| "Pyrrhic victory" (formal win, economic loss) | Accepted as a testable claim: rulings where the price moves against the formal winner | Strife |
| Stage II market prior from straddles, risk reversals and CDS | Not testable on free data | Shadow |
| Stage III event study at +5m, +30m, close, +1d, +5d | Close, +1d and +5d done (Earth). Intraday windows need paid history | Air (prospective) |
| Legal Complexity Score (length, disposition, quantification gap, contagion scope) | Accepted. Length, number of separate opinions and partial disposition are mechanical (Metal); the quantification gap is tested on Water's coding (Void); contagion scope by industry is Fire and by disclosed exposure is Storm | Metal, Void, Fire, Storm |
| Live LLM extraction pipeline | Deferred to Air: its value is only measurable prospectively, and the extraction schema is close to Water's coding sheet | Air |
| Trade hurdle: predicted CAR > spread + impact + model margin | Accepted as the decision criterion for any trading claim. Spreads from free daily high-low data (Corwin and Schultz, 2012). Frozen as a cross-thread gate (`prereg/cost_gate_prereg.md`): binds Void, Death, Storm and every later version; specifications frozen before it keep their rules | All new specifications |
| Instrument selection (equities, straddles, credit, pair trades) | Equities testable (Earth, Fire); pair trades where both sides are listed (Death). Straddles need options data; credit needs bond or CDS data | Death, Shadow |
| Compliance: public dissemination only; MAR treats imminence as inside information | Accepted, with one correction: UK Supreme Court hand-down dates are published a week ahead, so imminence is public there; embargoed drafts are not | Aether, Air audit trail |
| Audit trail: pre-release file, UTC download timestamp, pre-defined plan | Accepted for Air: each forward entry is committed to git before the ruling, so the commit time is the dated research file | Air |

## Agreed order (30 October 2026)

1. Freeze Water's rubric and the Air forward register before any further results are seen.
2. Code the 37 Moon events and Earth's reacting events from the first complete Federal Circuit run, blind to prices.
3. Add Delaware (Love).

## Free data sources in use or needed

| Source | Used by | Access |
|---|---|---|
| Supreme Court Database (SCDB) | Apple, Earth, Moon, Strife, Light | Free download |
| CourtListener API | Metal, Love, Thunder, Air; Water only as a fallback (Earth v1 only) | Free token (set as the Actions secret `COURTLISTENER_TOKEN`) |
| supremecourt.gov opinions pages (slip opinions, preliminary prints, bound volumes) | Water (opinion text, OT2017 onwards) | Free, no key; reachable from the GitHub runner, not from this workspace |
| GovInfo API (United States Reports; United States Courts Opinions, Federal Circuit as court code ca13) | Water (opinion text to volume 586); Earth v2 and its dependants (Federal Circuit universe and parties) | Free api.data.gov key, Actions secret `GOVINFO_API_KEY` |
| EDGAR (company list, submissions, full-text search, XBRL company facts) | All US threads; Wood | Free; user agent with a contact email |
| yfinance (daily; one-minute bars for the last seven days) | All | Free |
| Find Case Law (The National Archives) | Aether | Free, no key |
| Companies House API (persons with significant control, for UK parent mapping) | Aether | Free key on registration |
| Kalshi and Polymarket public market data | Ice | Free, no key for market data |
| Anthropic API (Water coder 3) | Water, later Air | Actions secret `ANTHROPIC_API_KEY` (key `act-trigger-coder`, expires 29 November 2026); promotional credit of $200 expires 27 November 2026. Each run logs its token use in `data/water/api_coder/run_meta.json` |
| CanLII API | Canada (backlog) | Free key on request |
