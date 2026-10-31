# Pre-registration: Project Earth v2 (post-ruling drift in the litigant against a like-for-like control)

Registered 31 October 2026. It replaces `earth_prereg.md` (v1, SHA-256 464c4ccfc0a89a22df4f58a38c4da514a50db910649e99714c61d27b71e3a5cf), which is left unchanged. The hypothesis, definitions, statistic and decision rule of v1 are carried over unchanged unless stated below.

## Why there is a version 2, and what the analyst has seen

1. Version 1 named CourtListener as the Federal Circuit source. The project's CourtListener allowance (125 requests a day since 7 May 2026) cannot deliver the 2012 to June 2025 list, and run 9 of 30 October 2026 failed for that reason.
2. Runs 6 and 8 under v1 used truncated Federal Circuit lists: run 6 covered January 2012 to September 2013; run 8 covered October 2014 to November 2015, 453 rulings. Both are retired.
   - The analyst saw the totals of run 8: the event count, the mean difference and its p.
   - The analyst did not see per-event results.
   - That knowledge was available when this version was written, and this disclosure is part of the registration.
3. The review of 31 October 2026 (`data/appeals/govinfo_review/README.md`) found two things.
   - CourtListener's "Published" status for the Federal Circuit includes summary affirmances under Federal Circuit Rule 36. These are judgments without an opinion: 182 of 416 items in January to October 2015.
   - So v1, as implemented, mixed judgments without an opinion into "every opinion marked precedential". Version 2 counts opinions only.
4. The choices below were made by the operator on 31 October 2026, after that review and before any run under this version:
   - the window;
   - the treatment of mandamus decisions;
   - matching every named party;
   - the parent arm.

## Universe

1. **Supreme Court.** As v1 item 1: SCDB, October Terms 2005 to 2024, decision types 1, 5, 6 and 7. The caption is split on " v. " and each side is matched on its first name, as v1 item 3.
2. **Federal Circuit.**
   - Source: GovInfo, collection USCOURTS, court code ca13, from the index `data/appeals/govinfo_cafc_index.csv` and the parties file `data/appeals/govinfo_cafc_parties.csv`.
   - Window: every precedential opinion issued 1 April 2013 to 30 June 2025. GovInfo's coverage is incomplete before April 2013 (review, item 1).
   - Counting rules:
     a) **Precedential.** An entry is a precedential opinion if its docket text carries the precedential marker ("Precedential Opinion" or "Precedential Per Curiam Opinion", not "Nonprecedential") and the entry is the filing of an opinion. Such entries begin "OPINION", "SEALED OPINION", "UNSEALED OPINION", "MODIFIED ENTRY: OPINION" or "SUPPLEMENTAL OPINION", ignoring markup.
     b) **Excluded entries.** Errata, errata entries, corrected entries, and the reissue as precedential of an opinion first issued as non-precedential ("PRECEDENTIAL OPINION ISSUED").
     c) **Consolidated appeals.** An opinion filed in several dockets is one ruling. Entries are the same opinion if they share the date of issue and either the docket-entry number or the caption. The ruling's parties are the union of the parties of those dockets.
     d) **Vacated opinions.** An opinion later vacated, for example on rehearing en banc, is kept, because it was released and public on its date of issue.
     e) **Mandamus and other miscellaneous dockets** (docket numbers below 1000) are excluded. GovInfo holds almost none of them. Precedential orders are not opinions and are outside the universe, as in v1.
   - Day 0 is the GovInfo date of issue.
3. **Parties (Federal Circuit).**
   - Who is matched: every party GovInfo lists for the ruling. The role sets the side:
     - one side is appellant, cross-appellant or petitioner;
     - the other is appellee, cross-appellee or respondent;
     - intervenors, "Not party" and unstructured entries are not matched.
   - How: each name is matched to EDGAR's company list exactly as v1 item 3, using the same normalisation and exact match.
   - Multiple matches: every matched listed company is an event. One event per (ruling, ticker), so a company listed twice on one ruling counts once.
   - Where a later rule needs a single "first name" per side, it uses the first party in GovInfo's order for that side.
4. **Ticker and price history:** as v1 item 4.
5. **Opposing side:** "listed" if any party on the other side is matched exactly, "parent" if none is but one resolves to a listed parent under item 6, and otherwise as v1.
6. **Parent arm (secondary).**
   - Who: a company party with no exact match, which is neither a government nor an individual under the rules of `scripts/appeals_common.py`.
   - When it resolves: it is assigned to a listed parent if that parent's Exhibit 21 names it in a 10-K filed in the three years up to and including day 0.
   - Search and threshold: EDGAR full-text search, with the same rule as Moon for a resolved parent (all hits, or at least three hits and 80% of them, on one CIK).
   - Point in time: the search is restricted to filings on or before day 0, so a later acquisition cannot assign a ruling to its eventual parent.
   - Coverage: this arm covers both courts. Its events are reported separately and never pooled with the primary arm.

## Definitions, statistic and decision rule

As v1 (day 0, market model, reacting event, outcome, control, statistic, bootstrap with seed 20261030, secondary descriptives).

- **Primary arm:** direct listed parties (items 1 and 3). It alone decides Project Earth under v1's rule: Support, Kill, Unscorable at fewer than 40 events, otherwise Inconclusive.
- **Parent arm:** reported with the same statistic and the same thresholds, labelled secondary. It cannot turn a primary Kill or Inconclusive into Support. Holm's correction across the two arms is reported alongside the raw p.

## Effect on the specifications that depend on Earth

- Fire, Strife, Death, Metal, Wood, Storm and Void refer to "the first Earth run whose universe contains Federal Circuit opinions for the whole of 2012 to June 2025". This is read as "the first Earth v2 run whose universe contains Federal Circuit opinions for the whole of 1 April 2013 to 30 June 2025".
- Where those specifications use a side's name from the caption of a Federal Circuit ruling, they use the first party in GovInfo's order for that side (item 3).
- Death's pairs are the first exactly matched listed company on each side.
- Nothing else in them changes.

## Known limitations (in addition to v1's)

- Mandamus decisions, including venue disputes involving listed companies, are absent.
- GovInfo's parties list may name a party differently from the opinion's caption, for example a former name or an abbreviation. Exact matching misses those, as in v1.
- The Exhibit 21 route finds only subsidiaries that a parent lists, which is usually its significant subsidiaries, and depends on the full-text search index.
- The window loses January 2012 to March 2013.

Implementation: `scripts/appeals_common.py` (`_govinfo_cafc`, `build_party_map`, `parent_map_pit`), `scripts/earth.py`.
