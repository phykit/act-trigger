"""Project Fire: spillover of a ruling to the litigant's industry, signed by the litigant's own reaction (prereg/fire_prereg.md).

Usage: python scripts/fire.py
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appeals_common import (SELFTEST, bootstrap_mean_p, build_party_map, build_universe, bulk_prices,  # noqa: E402
                            compute_events, edgar_tickers, log, result_path, rolling_ar, sic_of, sic_peers, spec_hash)

MIN_EVENTS = 30
P_THRESH = 0.05
POST = 10
MAX_PEERS = 40
MIN_PEERS = 5


def fmt(x: float) -> str:
    return "n/a" if x is None or not np.isfinite(x) else f"{100 * x:+.2f}%"


def main() -> None:
    h = spec_hash("fire")
    uni, unote = build_universe()
    pm = build_party_map(uni)
    tick = edgar_tickers()
    ev, ars, px = compute_events(uni, pm, ("listed",), "litigants", post=5)
    ok = ev[ev["status"] == "ok"]
    cand = ok[ok["reacting"] & ~ok["opposing_basis"].isin(["listed", "ex21 parent"]) & (ok["n_control"] >= 3)].copy()
    notes = []
    # peers per litigant
    peers_by_cik: dict[str, list[str]] = {}
    sic_by_cik: dict[str, str] = {}
    for cik in sorted(set(cand["cik"].astype(str))):
        try:
            sic = sic_of(cik)
        except Exception as exc:  # noqa: BLE001
            notes.append(f"{cik}: SIC lookup failed ({str(exc)[:60]})")
            continue
        if not sic:
            notes.append(f"{cik}: no SIC in EDGAR")
            continue
        sic_by_cik[cik] = sic
        try:
            peers = [p for p in sic_peers(sic, tick) if p["cik"] != cik]
        except Exception as exc:  # noqa: BLE001
            notes.append(f"{cik}: peer browse failed for SIC {sic} ({str(exc)[:60]})")
            continue
        peers_by_cik[cik] = [p["ticker"] for p in peers][:MAX_PEERS * 2]  # extra, trimmed after data availability
    party_tickers = set(pm["ticker"].dropna().astype(str))
    all_peers = sorted({t for lst in peers_by_cik.values() for t in lst})
    ppx = bulk_prices(all_peers + ["SPY"], "peers")
    rows = []
    for _, r in cand.iterrows():
        cik, t = str(r["cik"]), str(r["ticker"])
        plist = [p for p in peers_by_cik.get(cik, []) if p in ppx.columns and p != t]
        other = pm[(pm["ruling"].astype(int) == int(r["ruling"]))]["ticker"].dropna().astype(str).tolist()
        plist = [p for p in plist if p not in other][:MAX_PEERS]
        day0 = pd.Timestamp(r["date"])
        sub = ppx[plist]
        # peers with data across the event window and the controls' span
        lo, hi = day0 - pd.Timedelta(days=420), day0 + pd.Timedelta(days=400)
        sub = sub[(sub.index >= lo) & (sub.index <= hi)]
        good = [p for p in plist if sub[p].notna().mean() > 0.9]
        if len(good) < MIN_PEERS:
            notes.append(f"{t} {r['date']}: only {len(good)} peers with data in SIC {sic_by_cik.get(cik)}; event excluded")
            continue
        basket = np.exp(np.log(ppx[good]).diff().mean(axis=1)).cumprod()  # equal-weighted log-return index
        basket.name = "BASKET"
        bar = rolling_ar(basket.to_frame(), ppx["SPY"]).get("BASKET")
        if bar is None:
            notes.append(f"{t} {r['date']}: basket history too short; event excluded")
            continue
        idx = bar.index
        pos = idx.searchsorted(day0)
        if pos >= len(idx) or idx[pos] != day0 or pos + POST >= len(idx):
            notes.append(f"{t} {r['date']}: basket window incomplete; event excluded")
            continue
        s = 1.0 if r["ar0"] >= 0 else -1.0
        a = bar["ar"].values
        F = s * float(a[pos + 1: pos + 1 + POST].sum())
        b0 = s * float(a[pos])
        ctrl = []
        for d in json.loads(r["control_days"]):
            q = idx.searchsorted(pd.Timestamp(d))
            if q >= len(idx) or idx[q] != pd.Timestamp(d) or q + POST >= len(idx):
                continue
            lit = ars[t]
            lq = lit.index.searchsorted(pd.Timestamp(d))
            sq = 1.0 if lit["ar"].values[lq] >= 0 else -1.0
            ctrl.append(sq * float(a[q + 1: q + 1 + POST].sum()))
        if len(ctrl) < 3:
            notes.append(f"{t} {r['date']}: fewer than three basket control days; event excluded from the difference")
            rows.append(dict(ruling=r["ruling"], court=r["court"], date=r["date"], ticker=t, sic=sic_by_cik.get(cik), n_peers=len(good),
                             z0=r["z0"], ar0=r["ar0"], basket_ar0=b0, F=F, n_control=len(ctrl), control_mean=np.nan, d=np.nan))
            continue
        cm = float(np.mean(ctrl))
        rows.append(dict(ruling=r["ruling"], court=r["court"], date=r["date"], ticker=t, sic=sic_by_cik.get(cik), n_peers=len(good),
                         z0=r["z0"], ar0=r["ar0"], basket_ar0=b0, F=F, n_control=len(ctrl), control_mean=cm, d=F - cm))
    fe = pd.DataFrame(rows)
    diff = fe[fe["d"].notna()] if len(fe) else pd.DataFrame()
    n = len(diff)
    mean_diff = float(diff["d"].mean()) if n else float("nan")
    p_diff = bootstrap_mean_p(diff["d"].values) if n else float("nan")
    mean_F = float(fe["F"].mean()) if len(fe) else float("nan")
    p_F = bootstrap_mean_p(fe["F"].values) if len(fe) else float("nan")
    mean_b0 = float(fe["basket_ar0"].mean()) if len(fe) else float("nan")
    p_b0 = bootstrap_mean_p(fe["basket_ar0"].values) if len(fe) else float("nan")

    if n < MIN_EVENTS:
        outcome = "UNSCORABLE"
    elif mean_diff > 0 and p_diff < P_THRESH:
        outcome = "SUPPORT"
    elif mean_diff <= 0:
        outcome = "KILL"
    else:
        outcome = "INCONCLUSIVE"

    today = dt.date.today().isoformat()
    L = [f"# Result: Project Fire (spillover of a ruling to the litigant's industry)\n",
         f"Run {today} against fire_prereg.md, SHA-256 {h} (hashed before the run). Non-evidentiary: daily closes, equal-weighted SIC baskets, one parameter set, no costs.\n"]
    if SELFTEST:
        L.append("**SELF-TEST RUN ON SYNTHETIC DATA. Not a result.**\n")
    L.append("## Population\n")
    L.append(f"- Universe: {unote}.")
    L.append(f"- Candidate events (Earth reacting, general application, at least three litigant control days): {len(cand)}; with a usable peer basket: {len(fe)}; in the difference: {n}.\n")
    L.append("## Outcomes\n")
    L.append("| Statistic | Value |")
    L.append("|---|---|")
    L.append(f"| Mean signed basket reaction on day 0 | {fmt(mean_b0)} (n = {len(fe)}), bootstrap p {p_b0:.3f} |")
    L.append(f"| Mean signed basket CAR(+1,+10) after rulings, F | {fmt(mean_F)}, bootstrap p {p_F:.3f} |")
    L.append(f"| Mean difference, ruling minus the basket's drift after the litigant's other big days | {fmt(mean_diff)} (n = {n}) |")
    L.append(f"| Bootstrap p, one-sided | {p_diff:.3f} |")
    for court in sorted(fe["court"].unique()) if len(fe) else []:
        sub = diff[diff["court"] == court]
        L.append(f"| {court}: events in difference, mean difference | {len(sub)}, {fmt(float(sub['d'].mean()) if len(sub) else float('nan'))} |")
    L.append("")
    L.append("## Decision rule as registered\n")
    L.append(f"- Mean difference above zero: {'met' if np.isfinite(mean_diff) and mean_diff > 0 else 'not met'} ({fmt(mean_diff)}).")
    L.append(f"- Bootstrap p below {P_THRESH}: {'met' if np.isfinite(p_diff) and p_diff < P_THRESH else 'not met'} (p = {p_diff:.3f}).")
    L.append(f"- At least {MIN_EVENTS} events in the difference: {'met' if n >= MIN_EVENTS else 'not met'} ({n}).\n")
    L.append(f"Registered outcome: {outcome}.\n")
    L.append("## What this does not license\n")
    L.append("- Four-digit SIC baskets, equal-weighted, capped at 40 names in ascending CIK order; not the investable sector.")
    L.append("- The sign convention assumes peers sit on the litigant's side of the rule.")
    L.append("- Events share decision days and peers; treated as independent.\n")
    L.append("## Events\n")
    L.append("| Court | Date | Litigant | SIC | Peers | Litigant z(0) | Basket AR(0) signed | Basket CAR(+1,+10) signed | Control mean (n) | Difference |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for _, r in (fe.sort_values("date") if len(fe) else fe).iterrows():
        L.append(f"| {r['court']} | {r['date']} | {r['ticker']} | {r['sic']} | {int(r['n_peers'])} | {r['z0']:+.2f} | {fmt(r['basket_ar0'])} | {fmt(r['F'])} | "
                 f"{fmt(r['control_mean'])} ({int(r['n_control'])}) | {fmt(r['d'])} |")
    L.append("")
    L.append("## Run notes\n")
    L.extend([f"- {x}" for x in notes[:60]] or ["- None."])
    if len(notes) > 60:
        L.append(f"- ... and {len(notes) - 60} further notes in the events file.")
    L.append("- Bootstrap: 10,000 draws, seed 20261030.")
    out = result_path("fire")
    out.write_text("\n".join(L) + "\n")
    if len(fe):
        fe.to_csv(out.with_suffix(".events.csv"), index=False)
    log(f"wrote {out}; outcome {outcome}; diff {fmt(mean_diff)} p={p_diff:.3f} n={n}")


if __name__ == "__main__":
    main()
