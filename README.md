# Act Trigger

Pre-registered test of whether the geopolitical risk premium is released at an anticipated military or terror act, and whether a bought one-month Nasdaq-100 call spread entered after such an act earns more than the same trade on an ordinary day.

## Status

| Item | State |
|---|---|
| Specification | Frozen 23 October 2026: `prereg/act_trigger_prereg.md`, SHA-256 `af0aeb33f85b5db06e731d61b712755297c39debed8459e5e1acf483360404e5` |
| First run | 23 October 2026: `results/act_trigger_result.md`. Registered outcome SUPPORT (13 anticipated events, bootstrap p 0.042) |
| Evidentiary standing | Non-evidentiary. One crude test; flat-vol pricing; no costs; 13 events |
| Operator inputs | Not set: minimum effect worth pursuing, minimum event count for a live decision, ratified sign, pre-mortem. These are for the operator to supply and are deliberately left blank |
| Trading | None |

## Prior art

- Brune, Hens, Rieger and Wang (2015), The war puzzle: rising war probability lowers stock prices; the outbreak of an anticipated war raises them; a surprise war lowers them.
- Goncalves, Melone and Ricciardi (2025), The Risk Premium of Geopolitical Threats: threats are priced; acts are weakly priced.
- Baur and Smales (2020): gold hedges geopolitical threats more than acts.
- Kelly, Pastor and Veronesi (NBER w19812): options spanning political events carry an implied-vol premium.

## Reproduce

```
curl -o data_gpr_daily_recent.dta https://raw.githubusercontent.com/iacoviel/iacoviel.github.io/master/gpr_files/data_gpr_daily_recent.dta
python scripts/detect_events.py data_gpr_daily_recent.dta
python scripts/outcomes.py
```

GPR vintage used for the first run: 2026-10-19. Later vintages may revise recent days.

## Court-ruling tests: Projects Apple and Orange

Two sibling pre-registrations, first on five Supreme Court cases with a listed party chosen for salience (Myriad 2013, Halliburton 2014, American Express 2018, Oracle 2021, Amgen 2023), then on a mechanical register of 82 listed-party cases over October Terms 2012 to 2024. Both run on free daily data in GitHub Actions (`.github/workflows/rulings.yml`), which commits each run's result file and the fetched inputs under `results/` and `data/rulings/`.

| Item | State |
|---|---|
| Apple v1: opinion-day versus non-opinion-day abnormal variance in the argument-to-decision window (timing hazard), opinion days from the supremecourt.gov slip listing | Frozen 29 October 2026: `prereg/apple_prereg.md`, SHA-256 `068f59f04174f8018788084fb457ed9fa94d79da68ce902b34288af141dff17d`. Run 30 October 2026: `results/apple_result_2026-10-30.md`, registered outcome UNSCORABLE (slip listings retired for OT2012 and OT2013, truncated for OT2017; three cases against a four-case floor; on those three R = 0.72, p = 0.40) |
| Apple v2: as v1 with opinion days from the Supreme Court Database for all terms | Frozen 30 October 2026: `prereg/apple_v2_prereg.md`, SHA-256 `b84afa4aeeaddb8ca72c470d7656845f58c6550600ac0ffda76a56078c39682a`. Run 30 October 2026: `results/apple_v2_result_2026-10-30.md`, registered outcome KILL (five cases, 59 pooled non-decision opinion days; R = 0.64, permutation p = 0.69; placebo R = 0.73; four of five cases below one) |
| Apple v3: as v2 on a mechanical register of 82 listed-party cases, OT2012 to OT2024, dates from SCDB | Frozen 30 October 2026: `prereg/apple_v3_prereg.md`, SHA-256 `dc8719db5ce99d8a7ee885e273ed0b20de02df0d023c9cef714f4329af451bec`; register `data/ruling_cases_wide.csv`. Run 30 October 2026: `results/apple_v3_result_2026-10-30.md`, registered outcome INCONCLUSIVE (77 cases, 744 pooled opinion days; R = 1.000, permutation p = 0.41; placebo R = 0.83; per-case median ratio 0.71) |
| Orange v2: as Orange on the same wide register | Frozen 30 October 2026: `prereg/orange_v2_prereg.md`, SHA-256 `cc890423fd859552bc3246f71adb5e95dc7a2075f13d88534dccf0a65d2073bf`. Run 30 October 2026: `results/orange_v2_result_2026-10-30.md`, registered outcome UNSCORABLE (8 of 77 cases reacted, a 10% rate; mean signed CAR(+1,+5) +2.53%, Stouffer p = 0.003, 5 of 8 continued; the rule needs 15). Of the eight, one decision day coincides with the company's earnings release (Warner Chappell, 9 May 2024) and three fall in March to June 2020 market turbulence |
| Orange: decision-day abnormal return and drift over the following five days (Katz versus Davis) | Frozen 29 October 2026: `prereg/orange_prereg.md`, SHA-256 `c12e7b2990f4e211c8afafed5bf40f840b1675c15f4fb5f971781a7da7caa2cd`. Run 30 October 2026: `results/orange_result_2026-10-30.md` (re-run `_2.md` identical on cached inputs), registered outcome UNSCORABLE (two of five cases reacted on decision day; both continued; the rule needs three) |
| Evidentiary standing | Non-evidentiary. Five cases chosen for salience; daily closes; one parameter set; no costs |
| Operator inputs | Not set: minimum effect worth pursuing, minimum event count for a live decision, ratified pre-mortem |
| Trading | None |

Prior art for both: Katz, Bommarito, Soellinger and Chen (2017), Law on the Market? (37% of 211 SCOTUS cases react, mean 4.4% over two sessions, accruing over hours and days); Davis, Govindaraj and Suslava (2024), Global Finance Journal (500 cases, no leakage, no drift); Davis, Govindaraj, Liu and Suslava (2026), Journal of Futures Markets (option implied volatility at the cert grant anticipates the decision). The full prior-art review is the operator's document of 29 October 2026.

Reproduce locally:

```
pip install pandas numpy scipy requests lxml yfinance
python scripts/apple.py --spec apple_v3    # apple_v2 or apple for the pilot specs
python scripts/orange.py --spec orange_v2  # orange for the pilot spec
RULINGS_SELFTEST=1 RULINGS_SCRATCH=/tmp/selftest python scripts/apple.py   # synthetic data, writes nothing under results/
```

## Appellate-ruling tests: Projects Earth, Moon and Fire

Three pre-registrations on a mechanical universe: every argued Supreme Court case of October Terms 2005 to 2024 (SCDB) and every precedential Federal Circuit opinion from 2012 where the runner can reach a source, with parties matched to tickers by exact name against EDGAR's company list, subsidiaries resolved to parents through Exhibit 21 full-text search, earnings dates from 8-K item 2.02, and industry peers by four-digit SIC. The `appeals` workflow (`.github/workflows/appeals.yml`) builds the universe and runs all three, committing results and the fetched inputs under `results/` and `data/appeals/` (raw EDGAR submissions and peer prices are not committed). Setting the repository secret `SEC_CONTACT` to a name and email identifies the runner to EDGAR as its fair-access policy asks; without it the scripts send the repository URL.

| Item | State |
|---|---|
| Earth: post-ruling drift in the litigant, against the same company's other large moves | Frozen 30 October 2026: `prereg/earth_prereg.md`, SHA-256 `464c4ccfc0a89a22df4f58a38c4da514a50db910649e99714c61d27b71e3a5cf`. Runs 30 October 2026: run 3 `results/earth_result_2026-10-30.md` (name-cleaning defect, 62 listed sides, 1 event) and run 4 `results/earth_result_2026-10-30_2.md` (79 listed sides, 4 reacting; mean difference +5.29%, p = 0.072), both UNSCORABLE against the 40-event floor. Run 6 (first with the Federal Circuit, but truncated by the search API's ~1,000-result cap to January 2012 to September 2013): `results/earth_result_2026-10-30_4.md`, 11 reacting events, mean difference +3.19%, bootstrap p = 0.004, 9 of 11 continuing, UNSCORABLE (floor 40); Myriad alone contributes +19.21%, and without it the mean is about +1.6%. Supreme Court rulings alone cannot reach the floor: the remaining unmatched company names are almost all private, foreign or since acquired. The Federal Circuit (CourtListener token needed) is the route to the sample |
| Moon: propagation of a Supreme Court ruling to the listed parent of a subsidiary party | Frozen 30 October 2026: `prereg/moon_prereg.md`, SHA-256 `8f7171a0a5af054b8890339049913f12f4a4b00c8efc5f29bf8c9f2757d2f6e1`. Run 30 October 2026 (run 3, the first to reach EDGAR): `results/moon_result_2026-10-30.md`, registered outcome SUPPORT (35 events; mean signed CAR(+1,+5) +2.70%, p = 0.029; placebo -0.09%). Read with caution: one event (NantKwest, +55%) carries most of the mean, and four events are the named party under a later ticker (NantKwest, Facebook, LabCorp, Amalgamated) rather than a parent; without NantKwest +1.15%, p = 0.077; without the four, +1.44%, p = 0.048; median +0.85% throughout. Run 3 also ran under a name-cleaning defect ("et al." and SCDB role labels not removed, contrary to item 3 of the Earth spec), so Earth and Fire matched only 62 listed sides and were UNSCORABLE on one event each; the defect is fixed under the same specs and the rerun is appended. Run 4 `results/moon_result_2026-10-30_2.md`: SUPPORT again (37 events; +2.57%, p = 0.026; placebo -0.64%); without NantKwest +1.11%, p = 0.074; without the four renamed direct parties +1.37%, p = 0.044; median +0.61% to +0.82% |
| Fire: spillover to the litigant's SIC peers, signed by the litigant's own reaction | Frozen 30 October 2026: `prereg/fire_prereg.md`, SHA-256 `f1ebe116062b8f01c9bd192842803cd3eea523a7bb9af97643a392cc59e28a13`. Runs 30 October 2026: run 3 (1 event) and run 4 `results/fire_result_2026-10-30_2.md` (3 events; mean difference -2.29%), both UNSCORABLE against the 30-event floor; Fire draws its events from Earth's and is capped by the same sample |
| Evidentiary standing | Non-evidentiary. Daily closes; mechanical matching; one parameter set; no costs |
| Operator inputs | Not set: minimum effect worth pursuing, minimum event count for a live decision, ratified pre-mortem |
| Trading | None |

Reproduce locally:

```
pip install pandas numpy scipy requests lxml yfinance
python scripts/build_universe.py
python scripts/earth.py && python scripts/moon.py && python scripts/fire.py
RULINGS_SELFTEST=1 RULINGS_SCRATCH=/tmp/selftest python scripts/earth.py   # synthetic data, writes nothing under results/
```

## Rules for this repository

- The specification file is never edited. Any change is a new, separately hashed specification with its own result file.
- Results are appended, never overwritten.
- The next qualifying anticipated act is the first out-of-sample observation; it is recorded here before its outcome is known.
