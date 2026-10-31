# Result: Project Earth v2 (post-ruling drift in the litigant against a like-for-like control)

Run 2026-10-31 against earth_v2_prereg.md, SHA-256 f31acf8b9450f8bb24251d37e5e99addf30e1ec838030dc8aabfd611f644f510, with amendments 1 (SHA-256 7b9bc67ab1acd937a76207c2230690e7a39b45ac1250a44332acd62af4c3cfee) and 2 (SHA-256 e9bb34e882a280b85fabefeb753394daa9a68288b5f62bd739d21d1e6df52255), all hashed before the run. Non-evidentiary: daily closes, one parameter set, no costs.

## Population

- Universe: SCOTUS 1342 rulings (SCDB 2026_01); Federal Circuit 2421 precedential opinions (GovInfo USCOURTS ca13).
- Sides matched exactly to a listed company: 771 of 13695; events with usable price windows: 708 of 749; reacting (abs(z_0) >= 2, not earnings-adjacent, calm market): 40 (6% reaction rate); events in the difference (at least three control days): 40.

## Outcomes

| Statistic | Value |
|---|---|
| Mean signed CAR(+1,+5) after rulings, reacting events | +4.74% (n = 40) |
| Stouffer Z, one-sided p (rulings alone) | 6.35, 0.000 |
| Mean control drift (same companies' other abs(z) >= 2 days) | -0.49% |
| Mean difference, ruling minus control | +5.23% (n = 40) |
| Bootstrap p, one-sided | 0.005 |
| Reacting events continuing over +1 to +5 | 29 of 40 |
| cafc: events in difference, mean difference | 36, +5.22% |
| scotus: events in difference, mean difference | 4, +5.29% |
| General-application subset (opponent not a listed company or its subsidiary) | 30, +0.93% |

## Decision rule as registered

- Mean difference above zero: met (+5.23%).
- Bootstrap p below 0.05: met (p = 0.005).
- At least 40 events in the difference: met (40).

Registered outcome (primary arm, decides Earth): SUPPORT.

## Parent arm (secondary; Exhibit 21 parents, point in time; never pooled with the primary arm)

| Statistic | Value |
|---|---|
| Parent events with usable windows; reacting; in the difference | 365; 11; 11 |
| Mean difference, ruling minus control | +6.63% |
| Bootstrap p, one-sided (raw; Holm across the two arms) | 0.082; 0.082 |
| Primary arm p after Holm | 0.011 |
| Parent-arm outcome under the same thresholds (secondary) | UNSCORABLE |

## What this does not license

- Exact-name matching: subsidiaries and differently registered names are not here (Project Moon).
- Daily closes; Federal Circuit release times are untimestamped; rolling estimates lag a day.
- The control is any large idiosyncratic move not excluded by the screens; events are treated as independent.

## Reacting events

| Court | Date | Ticker | Case | AR(0) | z(0) | CAR(-5,-1) | CAR(+1,+1) | CAR(+1,+5) | Signed | Control mean (n) | Difference | Opponent |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scotus | 2006-03-01 | ITW | ILLINOIS TOOL WORKS INC., et al. v. INDEPENDENT INK, INC. | +1.95% | +2.04 | -1.83% | +0.33% | +2.85% | +2.85% | -0.28% (20) | +3.12% | unresolved (none) |
| scotus | 2007-04-02 | DUK | ENVIRONMENTAL DEFENSE, et al. v. DUKE ENERGY CORPORATION, et | +1.92% | +2.37 | +0.30% | -0.44% | -0.81% | -0.81% | +0.55% (24) | -1.37% | not a company |
| cafc | 2013-05-03 | F | Ford Motor Company v. US | +1.95% | +2.00 | -0.62% | +1.55% | +0.43% | +0.43% | +1.72% (19) | -1.28% | not a company |
| scotus | 2013-06-13 | MYGN | ASSOCIATION FOR MOLECULAR PATHOLOGY, et al., PETITIONERS v.  | -7.10% | -3.33 | +10.26% | -14.45% | -17.77% | +17.77% | -1.44% (20) | +19.21% | unresolved (none) |
| cafc | 2013-07-02 | FMS | Fresenius USA, Inc. v. Baxter International, Inc. | -9.93% | -9.67 | +0.22% | +0.37% | -1.71% | +1.71% | -0.07% (23) | +1.78% | listed |
| cafc | 2013-09-24 | RMBS | Rambus Inc. v. Rea | +4.21% | +2.06 | +4.36% | -0.81% | +4.23% | +4.23% | -0.71% (16) | +4.94% | not a company |
| cafc | 2014-05-05 | SAP | Microsoft Corporation v. Datatern, Inc. | -2.03% | -2.21 | +2.09% | +0.29% | -2.50% | +2.50% | +0.09% (21) | +2.41% | unresolved (none) |
| cafc | 2014-05-05 | SAP | SAP AG v. Datatern, Inc. | -2.03% | -2.21 | +2.09% | +0.29% | -2.50% | +2.50% | +0.09% (21) | +2.41% | unresolved (none) |
| cafc | 2014-06-06 | INTC | STC.UNM v. Intel Corporation | +1.42% | +2.03 | +1.71% | -1.01% | +6.42% | +6.42% | -0.78% (15) | +7.20% | not a company |
| cafc | 2014-07-11 | XRX | Digitech Image Technologies v. Electronics for Imaging, Inc. | +2.35% | +2.11 | +1.11% | -0.87% | +1.17% | +1.17% | -0.48% (26) | +1.65% | unresolved (none) |
| cafc | 2014-09-10 | AAPL | Interval Licensing LLC v. AOL, Inc. | +2.69% | +2.75 | -5.41% | +0.23% | -0.33% | -0.33% | -1.68% (10) | +1.36% | unresolved (none) |
| cafc | 2014-09-16 | VHC | VirnetX, Inc. v. Cisco Systems, Inc. | -59.74% | -24.54 | +5.89% | -8.25% | -47.95% | +47.95% | +1.96% (18) | +45.99% | listed |
| cafc | 2014-12-19 | SYK | Stryker Corporation v. Zimmer, Inc. | -1.54% | -2.35 | +1.18% | -0.26% | -0.17% | +0.17% | +0.34% (24) | -0.18% | ex21 parent |
| cafc | 2015-07-09 | SAP | Versata Development Group v. SAP America, Inc. | +1.81% | +2.14 | -1.54% | +2.28% | +3.38% | +3.38% | -0.69% (20) | +4.07% | unresolved (none) |
| cafc | 2015-12-15 | AAPL | SightSound Technologies, LLC v. Apple Inc. | -3.01% | -2.36 | -1.99% | -0.90% | -2.79% | +2.79% | -1.09% (10) | +3.88% | unresolved (none) |
| cafc | 2015-12-15 | AAPL | Openwave Systems, Inc. v. Apple Inc. | -3.01% | -2.36 | -1.99% | -0.90% | -2.79% | +2.79% | -1.09% (10) | +3.88% | unresolved (parent not listed) |
| cafc | 2016-01-06 | F | Ford Motor Company v. US | -3.22% | -3.17 | -1.20% | -0.61% | -1.59% | +1.59% | -1.01% (19) | +2.61% | not a company |
| cafc | 2016-06-21 | IMMR | Immersion Corporation v. HTC Corporation | +12.00% | +5.81 | +0.19% | -0.29% | +3.65% | +3.65% | -1.50% (15) | +5.15% | unresolved (none) |
| cafc | 2016-06-27 | T | BASCOM Global Internet v. AT&T Mobility LLC | +2.20% | +3.17 | +2.48% | -1.15% | +0.14% | +0.14% | -0.07% (29) | +0.21% | unresolved (none) |
| cafc | 2016-11-09 | MDT | In re: NuVasive, Inc. | -2.62% | -3.78 | +2.87% | -0.39% | -2.98% | +2.98% | -0.04% (16) | +3.03% | unresolved (parent not listed) |
| cafc | 2017-01-26 | CPIX | Cumberland Pharmaceuticals v. Mylan Institutional LLC | +7.48% | +3.86 | -2.49% | +1.26% | -1.85% | -1.85% | -1.39% (33) | -0.46% | unresolved (parent not listed) |
| cafc | 2017-04-04 | ST | Wasica Finance GmbH v. Continental Automotive Systems | -3.22% | -2.88 | -1.13% | -0.55% | -0.56% | +0.56% | -0.60% (18) | +1.15% | unresolved (none) |
| cafc | 2017-05-05 | AAPL | Affinity Labs of Texas, LLC v. Matal | +1.18% | +2.41 | +1.19% | +2.56% | +4.59% | +4.59% | +2.22% (14) | +2.36% | unresolved (none) |
| cafc | 2017-10-05 | AMGN | Amgen Inc. v. Sanofi | -1.67% | -2.05 | +0.55% | -0.36% | -1.98% | +1.98% | -0.02% (18) | +1.99% | listed |
| scotus | 2018-06-25 | AXP | OHIO v. AMERICAN EXPRESS CO. | +2.83% | +2.24 | -0.42% | -0.59% | +0.07% | +0.07% | -0.11% (18) | +0.18% | not a company |
| cafc | 2018-07-27 | GPRO | GoPro, Inc. v. Contour IP Holding LLC | -7.17% | -2.22 | -2.51% | -4.29% | +17.01% | -17.01% | -0.28% (15) | -16.73% | unresolved (none) |
| cafc | 2018-11-09 | CSCO | Arista Networks, Inc. v. Cisco Systems, Inc. | -1.61% | -2.15 | +2.19% | -0.84% | -0.12% | +0.12% | -0.14% (10) | +0.25% | listed |
| cafc | 2019-03-15 | NAII | Natural Alternatives Intl. v. Creative Compounds, LLC | +4.20% | +2.33 | -2.81% | -3.39% | -6.80% | -6.80% | -1.34% (25) | -5.46% | unresolved (none) |
| cafc | 2019-06-12 | MU | Samsung Electronics Co., Ltd. v. Elm 3DS Innovations, LLC | -4.94% | -2.51 | -3.37% | +0.75% | +1.20% | -1.20% | +1.05% (12) | -2.25% | unresolved (none) |
| cafc | 2019-08-01 | VHC | VirnetX Inc. v. Apple Inc. | -13.02% | -4.80 | +1.62% | -3.98% | -21.04% | +21.04% | -0.28% (17) | +21.33% | listed |
| cafc | 2019-10-01 | HON | Honeywell International Inc. v. Arkema Inc. | -1.89% | -2.14 | +1.62% | -0.22% | -1.93% | +1.93% | -0.10% (10) | +2.03% | not a company |
| cafc | 2019-12-16 | AMGN | Amgen Inc. v. Hospira, Inc. | +2.15% | +2.91 | +0.55% | -0.21% | -1.05% | -1.05% | -0.01% (14) | -1.03% | unresolved (parent not listed) |
| cafc | 2020-08-03 | ILMN | Illumina, Inc. v. Ariosa Diagnostics, Inc. | +3.36% | +2.03 | -1.87% | -1.47% | -13.95% | -13.95% | +0.06% (9) | -14.01% | unresolved (none) |
| cafc | 2020-09-24 | NTIP | Network-1 Technologies, Inc. v. Hewlett-Packard Company | +12.46% | +7.13 | +2.20% | +2.36% | +11.60% | +11.60% | -1.72% (18) | +13.32% | listed |
| cafc | 2020-09-25 | VPLM | Apple Inc. v. Voip-Pal.com, Inc. | +19.82% | +3.72 | -12.17% | +17.25% | +84.03% | +84.03% | -5.66% (24) | +89.69% | listed |
| cafc | 2021-12-01 | ABUS | ModernaTX, Inc. v. Arbutus Biopharma Corporation | +37.98% | +10.18 | +7.01% | -7.97% | -13.68% | -13.68% | -5.26% (19) | -8.43% | ex21 parent |
| cafc | 2023-03-13 | EW | Apple Inc. v. Vidal | +3.26% | +2.11 | -4.76% | +0.58% | +3.73% | +3.73% | -0.18% (14) | +3.91% | not a company |
| cafc | 2024-09-06 | PRKR | ParkerVision, Inc. v. Qualcomm Incorporated | +77.37% | +8.09 | +8.32% | -6.84% | +12.58% | +12.58% | -2.98% (24) | +15.56% | ex21 parent |
| cafc | 2025-01-27 | AAPL | Apple Inc. v. Gesture Technology Partners, LLC | +4.47% | +3.78 | -4.87% | +2.84% | -0.63% | -0.63% | +0.65% (18) | -1.28% | unresolved (none) |
| cafc | 2025-06-16 | ROKU | Ancora Technologies, Inc. v. Roku, Inc. | +8.07% | +2.59 | -4.82% | -0.32% | -0.47% | -0.47% | +2.57% (13) | -3.04% | unresolved (none) |

## Run notes

- 41 matched sides excluded for data reasons: day 0 not a trading day or window incomplete (34); no price history (7)
- Party-map bases: unresolved (none) (6342); not a company (5249); listed (771); ex21 parent (564); unresolved (ambiguous) (383); unresolved (parent not listed) (379); unresolved (error) (7)
- Bootstrap: 10,000 draws over events, seed 20261030; controls within 252 trading days, ten-day gap around rulings, earnings-adjacent and non-calm days excluded.
