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

Two sibling pre-registrations on the same five Supreme Court cases with a listed party (Myriad 2013, Halliburton 2014, American Express 2018, Oracle 2021, Amgen 2023). Both run on free daily data in GitHub Actions (`.github/workflows/rulings.yml`), which commits each run's result file and the fetched inputs under `results/` and `data/rulings/`.

| Item | State |
|---|---|
| Apple v1: opinion-day versus non-opinion-day abnormal variance in the argument-to-decision window (timing hazard), opinion days from the supremecourt.gov slip listing | Frozen 29 October 2026: `prereg/apple_prereg.md`, SHA-256 `068f59f04174f8018788084fb457ed9fa94d79da68ce902b34288af141dff17d`. Run 30 October 2026: `results/apple_result_2026-10-30.md`, registered outcome UNSCORABLE (slip listings retired for OT2012 and OT2013, truncated for OT2017; three cases against a four-case floor; on those three R = 0.72, p = 0.40) |
| Apple v2: as v1 with opinion days from the Supreme Court Database for all terms | Frozen 30 October 2026: `prereg/apple_v2_prereg.md`, SHA-256 `b84afa4aeeaddb8ca72c470d7656845f58c6550600ac0ffda76a56078c39682a`. Run 30 October 2026: `results/apple_v2_result_2026-10-30.md`, registered outcome KILL (five cases, 59 pooled non-decision opinion days; R = 0.64, permutation p = 0.69; placebo R = 0.73; four of five cases below one) |
| Orange: decision-day abnormal return and drift over the following five days (Katz versus Davis) | Frozen 29 October 2026: `prereg/orange_prereg.md`, SHA-256 `c12e7b2990f4e211c8afafed5bf40f840b1675c15f4fb5f971781a7da7caa2cd`. Run 30 October 2026: `results/orange_result_2026-10-30.md` (re-run `_2.md` identical on cached inputs), registered outcome UNSCORABLE (two of five cases reacted on decision day; both continued; the rule needs three) |
| Evidentiary standing | Non-evidentiary. Five cases chosen for salience; daily closes; one parameter set; no costs |
| Operator inputs | Not set: minimum effect worth pursuing, minimum event count for a live decision, ratified pre-mortem |
| Trading | None |

Prior art for both: Katz, Bommarito, Soellinger and Chen (2017), Law on the Market? (37% of 211 SCOTUS cases react, mean 4.4% over two sessions, accruing over hours and days); Davis, Govindaraj and Suslava (2024), Global Finance Journal (500 cases, no leakage, no drift); Davis, Govindaraj, Liu and Suslava (2026), Journal of Futures Markets (option implied volatility at the cert grant anticipates the decision). The full prior-art review is the operator's document of 29 October 2026.

Reproduce locally:

```
pip install pandas numpy scipy requests lxml yfinance
python scripts/apple.py --spec apple_v2   # or --spec apple for v1
python scripts/orange.py
RULINGS_SELFTEST=1 RULINGS_SCRATCH=/tmp/selftest python scripts/apple.py   # synthetic data, writes nothing under results/
```

## Rules for this repository

- The specification file is never edited. Any change is a new, separately hashed specification with its own result file.
- Results are appended, never overwritten.
- The next qualifying anticipated act is the first out-of-sample observation; it is recorded here before its outcome is known.
