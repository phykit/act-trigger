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

## Rules for this repository

- The specification file is never edited. Any change is a new, separately hashed specification with its own result file.
- Results are appended, never overwritten.
- The next qualifying anticipated act is the first out-of-sample observation; it is recorded here before its outcome is known.
