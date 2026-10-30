"""Project Void: do rulings with no stated money figure drift more, within stakes strata (prereg/void_prereg.md)?

Uses Water's committed coding (coder 3 primary) and the latest Moon and Earth event files. Adopts the cost gate.
Usage: python scripts/void.py
"""
from __future__ import annotations

import datetime as dt
import hashlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from water_join import CODERS, ROOT, population  # noqa: E402

MIN_GROUP = 10
P_THRESH = 0.10
SEED = 20261030


def fmt(x: float, pct: bool = True) -> str:
    if x is None or not np.isfinite(x):
        return "n/a"
    return f"{100 * x:+.2f}%" if pct else f"{x:.3f}"


def strat_perm_p(df: pd.DataFrame, label: str, strat: str, val: str, draws: int = 10_000) -> float:
    """One-sided p for mean(val | label==0) - mean(val | label==1), labels permuted within strata."""
    rng = np.random.default_rng(SEED)
    d = df[[label, strat, val]].dropna()
    obs = d.loc[d[label] == 0, val].mean() - d.loc[d[label] == 1, val].mean()
    groups = [g for _, g in d.groupby(strat)]
    cnt = 0
    for _ in range(draws):
        lab = np.concatenate([rng.permutation(g[label].values) for g in groups])
        v = np.concatenate([g[val].values for g in groups])
        cnt += (v[lab == 0].mean() - v[lab == 1].mean()) >= obs
    return float(cnt / draws)


def main() -> None:
    h = hashlib.sha256((ROOT / "prereg" / "void_prereg.md").read_bytes()).hexdigest()
    pop = population()
    if pop.empty or "c3_D_figure_stated" not in pop.columns:
        raise SystemExit("coder 3 sheet or event files missing; Void cannot run")
    d = pop.dropna(subset=["drift", "c3_D_figure_stated"]).copy()
    d["D"] = d["c3_D_figure_stated"].astype(int)
    d["stratum"] = d["c3_B_core_business"].fillna(0) + d["c3_C_disclosed"].fillna(0)
    n0, n1 = int((d["D"] == 0).sum()), int((d["D"] == 1).sum())
    diff = float(d.loc[d["D"] == 0, "drift"].mean() - d.loc[d["D"] == 1, "drift"].mean()) if n0 and n1 else float("nan")
    p = strat_perm_p(d, "D", "stratum", "drift") if n0 and n1 else float("nan")
    gross0 = float(d.loc[d["D"] == 0, "drift"].mean()) if n0 else float("nan")
    # Cost gate: the spread estimate needs prices; it is computed by the appeals runner and joined when available.
    cost_f = ROOT / "data" / "water" / "event_costs.csv"
    gate_txt, gate_pass = "not computed (event_costs.csv absent)", False
    if cost_f.exists():
        c = pd.read_csv(cost_f, dtype={"event_id": str}).set_index("event_id")["cost"]
        z = d[d["D"] == 0].join(c, on="event_id")
        net = float((z["drift"] - z["cost"]).mean())
        gate_pass = bool(np.isfinite(net) and net > 0)
        gate_txt = f"mean net {fmt(net)} ({'passed' if gate_pass else 'not passed'})"
    if n0 < MIN_GROUP or n1 < MIN_GROUP:
        outcome = "UNSCORABLE"
    elif diff > 0 and p < P_THRESH and gate_pass:
        outcome = "SUPPORT"
    elif diff > 0 and p < P_THRESH:
        outcome = "SUPPORT (GROSS ONLY)"
    elif diff <= 0:
        outcome = "KILL"
    else:
        outcome = "INCONCLUSIVE"
    L = ["# Result: Project Void (the quantification gap)\n",
         f"Run {dt.date.today().isoformat()} against void_prereg.md, SHA-256 {h} (hashed before the run); cost gate prereg/cost_gate_prereg.md. "
         "Non-evidentiary: daily closes, one parameter set.\n",
         "## Population\n",
         f"- Coded events with returns: {len(d)} ({', '.join(f'{k} {v}' for k, v in d['population'].value_counts().items())}); "
         f"no figure stated (D = 0): {n0}; figure stated (D = 1): {n1}.\n",
         "## Outcomes\n", "| Statistic | Value |", "|---|---|",
         f"| Mean signed drift, D = 0 | {fmt(gross0)} (n = {n0}) |",
         f"| Mean signed drift, D = 1 | {fmt(float(d.loc[d['D'] == 1, 'drift'].mean()) if n1 else float('nan'))} (n = {n1}) |",
         f"| Primary: difference (D = 0 minus D = 1) | {fmt(diff)} |",
         f"| Permutation p, labels permuted within B + C strata | {fmt(p, False)} |",
         f"| Cost gate on D = 0 drift | {gate_txt} |"]
    raw = float(d.loc[d["D"] == 0, "drift"].mean() - d.loc[d["D"] == 1, "drift"].mean()) if n0 and n1 else float("nan")
    L.append(f"| Unstratified difference | {fmt(raw)} |")
    for pop_name in sorted(d["population"].unique()):
        s = d[d["population"] == pop_name]
        a, b = s[s["D"] == 0], s[s["D"] == 1]
        L.append(f"| {pop_name}: difference | {fmt(float(a['drift'].mean() - b['drift'].mean()) if len(a) and len(b) else float('nan'))} ({len(a)} v {len(b)}) |")
    for code in CODERS:
        col = f"c{code}_D_figure_stated"
        if col in pop.columns and code != "3":
            s = pop.dropna(subset=["drift", col])
            a, b = s[s[col] == 0], s[s[col] == 1]
            L.append(f"| Coder {code}: difference | {fmt(float(a['drift'].mean() - b['drift'].mean()) if len(a) and len(b) else float('nan'))} ({len(a)} v {len(b)}) |")
    L += ["", "## Decision rule as registered\n",
          f"- At least {MIN_GROUP} events in each group: {'met' if n0 >= MIN_GROUP and n1 >= MIN_GROUP else 'not met'} ({n0}, {n1}).",
          f"- Support: difference above zero, p below {P_THRESH}, and the cost gate passed.\n",
          f"Registered outcome: {outcome}.\n"]
    from rulings_common import result_path  # noqa: PLC0415
    out = result_path("void")
    out.write_text("\n".join(L) + "\n")
    print(f"wrote {out}; outcome {outcome}", file=sys.stderr)


if __name__ == "__main__":
    main()
