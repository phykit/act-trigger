"""Project Wood: does the issuer's own pre-ruling disclosure of the case predict the size of the reaction
(prereg/wood_prereg.md)? Disclosure is found mechanically with EDGAR full-text search in the issuer's own 10-K and 10-Q.

Usage: python scripts/wood.py   (after scripts/build_universe.py; needs SEC_CONTACT for EDGAR)
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appeals_common import (SELFTEST, build_party_map, build_universe, compute_events, log, result_path,  # noqa: E402
                            spec_hash)
from fts import is_government, search, term  # noqa: E402

MIN_DISCLOSED = 20
P_THRESH = 0.05
SEED = 20261030


def fmt(x: float, pct: bool = True) -> str:
    if x is None or not np.isfinite(x):
        return "n/a"
    return f"{100 * x:+.2f}%" if pct else f"{x:.3f}"


def perm_p(a: np.ndarray, b: np.ndarray, draws: int = 10_000) -> float:
    """One-sided permutation p for mean(a) - mean(b) > 0."""
    rng = np.random.default_rng(SEED)
    obs = a.mean() - b.mean()
    pool = np.concatenate([a, b])
    na = len(a)
    cnt = 0
    for _ in range(draws):
        rng.shuffle(pool)
        cnt += (pool[:na].mean() - pool[na:].mean()) >= obs
    return float(cnt / draws)


def main() -> None:
    h = spec_hash("wood")
    uni, unote = build_universe()
    pm = build_party_map(uni)
    sc_idx = set(uni[uni["court"] == "scotus"].index)
    earth, _, _ = compute_events(uni, pm, ("listed",), "litigants", post=5)
    moon, _, _ = compute_events(uni, pm[pm["ruling"].astype(int).isin(sc_idx)], ("ex21 parent",), "parents", post=5)
    earth["population"], moon["population"] = "Earth", "Moon"
    ev = pd.concat([earth, moon], ignore_index=True)
    ev = ev[ev["status"] == "ok"].copy()
    rows = []
    for _, e in ev.iterrows():
        opp = pm[(pm["ruling"].astype(int) == int(e["ruling"])) & (pm["side"] != e["side"])]
        oname = str(opp["name"].iloc[0]) if len(opp) else ""
        rec = dict(e)
        if not oname or is_government(oname):
            rec.update(wood_status="unscorable (opposing side is a government or absent)", term="", disclosed=np.nan, accession="")
            rows.append(rec)
            continue
        t = term(oname, 3)
        d0 = e["date"] if isinstance(e["date"], dt.date) else pd.Timestamp(e["date"]).date()
        try:
            hits = search(f'"{t}"', "10-K,10-Q", d0 - dt.timedelta(days=400), d0 - dt.timedelta(days=1), cik=str(e["cik"]), max_pages=1)
            rec.update(wood_status="ok", term=t, disclosed=float(len(hits) > 0), accession=hits[0].get("adsh", "") if hits else "")
        except Exception as exc:  # noqa: BLE001
            rec.update(wood_status=f"search failed: {str(exc)[:60]}", term=t, disclosed=np.nan, accession="")
        rows.append(rec)
    w = pd.DataFrame(rows)
    sc = w[w["wood_status"] == "ok"].copy()
    sc["absz"] = sc["z0"].abs()
    dis, und = sc[sc["disclosed"] == 1], sc[sc["disclosed"] == 0]
    nd = len(dis)
    diff = float(dis["absz"].mean() - und["absz"].mean()) if nd and len(und) else float("nan")
    p = perm_p(dis["absz"].values, und["absz"].values) if nd and len(und) else float("nan")
    react = sc[sc["reacting"] == True]  # noqa: E712
    rd, ru = react[react["disclosed"] == 1], react[react["disclosed"] == 0]
    sec_diff = float(rd["signed_post"].mean() - ru["signed_post"].mean()) if len(rd) and len(ru) else float("nan")
    if nd < MIN_DISCLOSED:
        outcome = "UNSCORABLE"
    elif diff > 0 and p < P_THRESH:
        outcome = "SUPPORT"
    elif diff <= 0:
        outcome = "KILL"
    else:
        outcome = "INCONCLUSIVE"
    L = ["# Result: Project Wood (issuer's own pre-ruling disclosure as a measure of stakes)\n",
         f"Run {dt.date.today().isoformat()} against wood_prereg.md, SHA-256 {h} (hashed before the run). Non-evidentiary: daily closes, one parameter set, no costs.\n"]
    if SELFTEST:
        L.append("**SELF-TEST RUN ON SYNTHETIC DATA. Not a result.**\n")
    L += ["## Population\n", f"- Universe: {unote}.",
          f"- Earth and Moon events with usable windows: {len(w)}; scorable for Wood: {len(sc)}; disclosed: {nd}; not disclosed: {len(und)}.",
          "- " + "; ".join(f"{k} ({v})" for k, v in w["wood_status"].value_counts().items()) + "\n",
          "## Outcomes\n", "| Statistic | Value |", "|---|---|",
          f"| Mean abs(z_0), disclosed | {fmt(float(dis['absz'].mean()) if nd else float('nan'), False)} (n = {nd}) |",
          f"| Mean abs(z_0), not disclosed | {fmt(float(und['absz'].mean()) if len(und) else float('nan'), False)} (n = {len(und)}) |",
          f"| Primary: difference | {fmt(diff, False)} |",
          f"| Permutation p, one-sided | {fmt(p, False)} |",
          f"| Reacting events: signed CAR(+1,+5), disclosed minus not | {fmt(sec_diff)} ({len(rd)} v {len(ru)}) |"]
    for pop in ("Earth", "Moon"):
        s = sc[sc["population"] == pop]
        L.append(f"| {pop}: share disclosed | {int((s['disclosed'] == 1).sum())} of {len(s)} |")
    for court in sorted(sc["court"].unique()):
        s = sc[sc["court"] == court]
        L.append(f"| {court}: share disclosed | {int((s['disclosed'] == 1).sum())} of {len(s)} |")
    L += ["", "## Decision rule as registered\n",
          f"- At least {MIN_DISCLOSED} disclosed events: {'met' if nd >= MIN_DISCLOSED else 'not met'} ({nd}).",
          f"- Support: difference above zero with permutation p below {P_THRESH}; kill: difference at or below zero.\n",
          f"Registered outcome: {outcome}.\n",
          "## What this does not license\n",
          "- A three-word name can match unrelated text in the issuer's filings; a case described without the opponent's name is a miss.",
          "- Agreement with Water's component C is reported once Water's sheets are joined.\n"]
    out = result_path("wood")
    out.write_text("\n".join(L) + "\n")
    w.drop(columns=["control_days"], errors="ignore").to_csv(out.with_suffix(".events.csv"), index=False)
    log(f"wrote {out}; outcome {outcome}; diff {fmt(diff, False)} p={fmt(p, False)} disclosed={nd}")


if __name__ == "__main__":
    main()
