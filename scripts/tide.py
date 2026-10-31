"""Project Tide: continuation after a decisive legal decision, tested as a trade net of costs (prereg/tide_prereg.md).

Arms: PTAB final written decisions (primary), PTAB institution decisions (secondary), Earth v2's 40 reacting events
(companion). The PTAB arms read data/tide/ptab_decisions.csv (columns: trial, kind, date, side, name), built from
the ODP fetch; if it is absent, only the Earth arm runs and the PTAB arms are reported as not run.

Usage: python scripts/tide.py      (RULINGS_SELFTEST=1 for synthetic data)
"""
from __future__ import annotations

import datetime as dt
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appeals_common import (ROOT, SELFTEST, bootstrap_mean_p, bulk_prices, earnings_dates, edgar_tickers,  # noqa: E402
                            log, match_listed, near_earnings, result_path, rolling_ar, spec_hash)
from cost_gate import round_trip  # noqa: E402

EARTH_EVENTS = ROOT / "results" / "earth_v2_result_2026-10-31.events.csv"
PTAB_FILE = ROOT / "data" / "tide" / "ptab_decisions.csv"
PRIMARY = (dt.date(2014, 1, 1), dt.date(2025, 6, 30))
HOLDOUT = (dt.date(2025, 7, 1), dt.date(2026, 9, 30))
REACT_Z, CALM, OVERLAP, HOLD = 2.0, 0.02, 6, 5
CTRL_SPAN, CTRL_GAP = 252, 10
MIN_PTAB, MIN_EARTH = 100, 40


def fmt(x) -> str:
    return "n/a" if x is None or not np.isfinite(x) else f"{100 * x:+.2f}%"


def lagged_beta(px: pd.DataFrame, win: int = 250) -> pd.DataFrame:
    r = np.log(px).diff()
    rm = r["SPY"]
    out = {}
    for t in r.columns:
        if t == "SPY":
            continue
        cov = r[t].rolling(win, min_periods=200).cov(rm)
        out[t] = (cov / rm.rolling(win, min_periods=200).var()).shift(1)
    return pd.DataFrame(out)


def cost_for(t: str, day0: dt.date, beta: float) -> float:
    if not np.isfinite(beta):
        return float("nan")
    return round_trip([(t, 1.0), ("SPY", beta)], day0)


# ----------------------------------------------------------------------------- statistics

def arm_stats(ev: pd.DataFrame) -> dict:
    ok = ev[np.isfinite(ev["N"])]
    n = len(ok)
    if n == 0:
        return dict(n=0, missing_cost=int((~np.isfinite(ev["N"])).sum()) if len(ev) else 0)
    N, G = ok["N"].values, ok["G"].values
    k = max(2, math.ceil(0.05 * n))
    trimmed = float(np.sort(N)[:-k].mean()) if n > k else float("nan")
    return dict(n=n, missing_cost=int((~np.isfinite(ev["N"])).sum()), meanN=float(N.mean()), p=bootstrap_mean_p(N),
                medianN=float(np.median(N)), trimmedN=trimmed, k_trim=k, meanG=float(G.mean()), medianG=float(np.median(G)),
                pG=bootstrap_mean_p(G), trimmedG=float(np.sort(G)[:-k].mean()) if n > k else float("nan"),
                hitN=float((N > 0).mean()), median_cost=float(np.median(ok["cost"].values)))


def verdict(s: dict, min_n: int) -> str:
    if s.get("n", 0) < min_n:
        return "UNSCORABLE"
    net_ok = s["meanN"] > 0 and s["p"] < 0.05 and s["medianN"] > 0 and s["trimmedN"] > 0
    if net_ok:
        return "SUPPORT"
    gross_ok = s["meanG"] > 0 and s["pG"] < 0.05 and s["medianG"] > 0 and s["trimmedG"] > 0
    if gross_ok:
        return "SUPPORT (GROSS ONLY)"
    if s["meanN"] <= 0:
        return "KILL"
    return "INCONCLUSIVE"


def stats_rows(s: dict) -> list[str]:
    if not s.get("n"):
        return ["| Reacting events with costs | 0 |\n"]
    return [f"| Reacting events with costs (excluded for missing cost) | {s['n']} ({s['missing_cost']}) |\n",
            f"| Mean net return N | {fmt(s['meanN'])}, bootstrap p {s['p']:.3f} |\n",
            f"| Median N | {fmt(s['medianN'])} |\n",
            f"| Mean N without the largest {s['k_trim']} events | {fmt(s['trimmedN'])} |\n",
            f"| Mean gross return G (p); median G | {fmt(s['meanG'])} ({s['pG']:.3f}); {fmt(s['medianG'])} |\n",
            f"| Share with N above zero; median round-trip cost | {s['hitN']:.0%}; {fmt(s['median_cost'])} |\n"]


def split_rows(ev: pd.DataFrame, col: str, label: str) -> list[str]:
    out = []
    ok = ev[np.isfinite(ev["N"])]
    for key, g in ok.groupby(col):
        out.append(f"| {label}: {key} | {len(g)}, mean N {fmt(float(g['N'].mean()))}, mean G {fmt(float(g['G'].mean()))} |\n")
    return out


# ----------------------------------------------------------------------------- Earth arm

def earth_arm() -> pd.DataFrame:
    ev = pd.read_csv(EARTH_EVENTS)
    ev = ev[ev["reacting"].astype(str) == "True"].copy()
    ev["date"] = pd.to_datetime(ev["date"]).dt.date
    px = bulk_prices(sorted(set(ev["ticker"].astype(str))) + ["SPY"], "tide_earth")
    beta = lagged_beta(px)
    rows = []
    for _, r in ev.iterrows():
        t, d0 = str(r["ticker"]), r["date"]
        b = float(beta[t].get(pd.Timestamp(d0), np.nan)) if t in beta.columns else float("nan")
        c = cost_for(t, d0, b)
        g = float(r["signed_post"])
        rows.append(dict(arm="earth", ticker=t, date=d0, side=r["side"], direction="long" if r["ar0"] > 0 else "short",
                         year=d0.year, G=g, beta=b, cost=c, N=g - c if np.isfinite(c) else float("nan")))
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------- PTAB arms

def ptab_events(dec: pd.DataFrame, kind: str, tick: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    notes: dict[str, int] = {}
    d = dec[dec["kind"] == kind].copy()
    d["date"] = pd.to_datetime(d["date"]).dt.date
    d = d[(d["date"] >= PRIMARY[0]) & (d["date"] <= HOLDOUT[1])]
    m = []
    for name in d["name"].astype(str).unique():
        hit = match_listed(name, tick)
        if hit:
            m.append(dict(name=name, ticker=hit["ticker"], cik=hit["cik"]))
    mm = pd.DataFrame(m, columns=["name", "ticker", "cik"])
    d = d.merge(mm, on="name", how="inner").drop_duplicates(["trial", "side", "ticker"])
    both = d.groupby(["trial", "ticker"])["side"].nunique()
    both = set(both[both > 1].index)
    notes["ticker on both sides of a trial"] = len(both)
    d = d[[(a, b) not in both for a, b in zip(d["trial"], d["ticker"])]]
    return d, notes


def ptab_arm(dec: pd.DataFrame, kind: str, tick: pd.DataFrame, all_dec_dates: dict) -> tuple[pd.DataFrame, dict]:
    d, notes = ptab_events(dec, kind, tick)
    if d.empty:
        return pd.DataFrame(), notes
    px = bulk_prices(sorted(set(d["ticker"])) + ["SPY"], "tide_ptab")
    ars = rolling_ar(px[[c for c in px.columns if c != "SPY"]], px["SPY"])
    beta = lagged_beta(px)
    spy = np.log(px["SPY"]).diff()
    edates: dict[str, set] = {}
    rows = []
    for t, g in d.groupby("ticker"):
        if t not in ars:
            notes["no price history"] = notes.get("no price history", 0) + g["date"].nunique()
            continue
        ar = ars[t]
        idx = ar.index
        cik = str(g["cik"].iloc[0])
        # one event per (ticker, day 0), day 0 moved to the next trading day
        g = g.assign(pos=[int(idx.searchsorted(pd.Timestamp(x))) for x in g["date"]])
        last = None
        for pos, gg in g.sort_values("pos").groupby("pos", sort=True):
            if gg["side"].nunique() > 1:
                notes["different sides on one day"] = notes.get("different sides on one day", 0) + 1
                continue
            if last is not None and pos - last <= OVERLAP:
                notes["overlapping event"] = notes.get("overlapping event", 0) + 1
                continue
            last = pos
            if pos + 10 >= len(idx) or int(px[t].loc[:idx[pos]].notna().sum()) <= 260:
                notes["window incomplete"] = notes.get("window incomplete", 0) + 1
                continue
            a, sg = ar["ar"].values, ar["sigma"].values
            R = a[pos] + a[pos + 1]
            z = R / (sg[pos] * math.sqrt(2))
            d0, d1 = idx[pos].date(), idx[pos + 1].date()
            s0, s1 = float(spy.get(idx[pos], np.nan)), float(spy.get(idx[pos + 1], np.nan))
            calm = np.isfinite(s0) and np.isfinite(s1) and abs(s0) <= CALM and abs(s1) <= CALM
            earn = False
            if abs(z) >= REACT_Z:
                if cik not in edates:
                    try:
                        edates[cik] = earnings_dates(cik)
                    except Exception as exc:  # noqa: BLE001
                        log(f"earnings dates failed for {cik}: {str(exc)[:80]}")
                        edates[cik] = set()
                earn = near_earnings(d0, edates[cik]) or near_earnings(d1, edates[cik])
            reacting = abs(z) >= REACT_Z and calm and not earn
            row = dict(arm=f"ptab {kind}", ticker=t, cik=cik, date=d0, side=gg["side"].iloc[0], z=z, reacting=reacting,
                       sample="primary" if d0 <= PRIMARY[1] else "holdout", year=d0.year)
            if reacting:
                G = float(np.sign(R) * a[pos + 2: pos + 2 + HOLD].sum())
                b = float(beta[t].get(idx[pos], np.nan)) if t in beta.columns else float("nan")
                c = cost_for(t, d0, b)
                # control: the company's other two-day moves of |z| >= 2
                rpos = {int(idx.searchsorted(pd.Timestamp(x))) for x in all_dec_dates.get(t, set())}
                ctrl = []
                for q in range(max(1, pos - CTRL_SPAN), min(len(idx) - HOLD - 2, pos + CTRL_SPAN)):
                    if any(abs(q - rp) <= CTRL_GAP for rp in rpos):
                        continue
                    Rq = a[q] + a[q + 1]
                    if not np.isfinite(sg[q]) or abs(Rq / (sg[q] * math.sqrt(2))) < REACT_Z:
                        continue
                    sq0, sq1 = float(spy.get(idx[q], np.nan)), float(spy.get(idx[q + 1], np.nan))
                    if not (np.isfinite(sq0) and np.isfinite(sq1) and abs(sq0) <= CALM and abs(sq1) <= CALM):
                        continue
                    if near_earnings(idx[q].date(), edates[cik]) or near_earnings(idx[q + 1].date(), edates[cik]):
                        continue
                    ctrl.append(float(np.sign(Rq) * a[q + 2: q + 2 + HOLD].sum()))
                row.update(G=G, beta=b, cost=c, N=G - c if np.isfinite(c) else float("nan"),
                           direction="long" if R > 0 else "short", n_control=len(ctrl),
                           control_mean=float(np.mean(ctrl)) if ctrl else float("nan"))
            rows.append(row)
    return pd.DataFrame(rows), notes


def synthetic_ptab() -> pd.DataFrame:
    tick = edgar_tickers()
    names = list(tick["title"].astype(str).head(60))
    rng = np.random.default_rng(7)
    rows = []
    for i in range(1500):
        day = dt.date(2014, 1, 2) + dt.timedelta(days=int(rng.integers(0, 4600)))
        kind = "fwd" if i % 2 else "institution"
        rows.append(dict(trial=f"IPR{i:05d}", kind=kind, date=day, side="owner", name=names[int(rng.integers(0, 60))]))
        rows.append(dict(trial=f"IPR{i:05d}", kind=kind, date=day, side="petitioner", name=names[int(rng.integers(0, 60))]))
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------- report

def main() -> None:
    h = spec_hash("tide")
    L = ["# Result: Project Tide (continuation after a decisive legal decision, net of costs)\n\n",
         f"Run {dt.date.today().isoformat()} against tide_prereg.md, SHA-256 {h} (hashed before the run); cost gate "
         "prereg/cost_gate_prereg.md. Non-evidentiary: daily closes, one parameter set, no borrow cost.\n\n"]
    out = result_path("tide")
    frames = []

    # PTAB arms
    dec = synthetic_ptab() if SELFTEST else (pd.read_csv(PTAB_FILE) if PTAB_FILE.exists() else None)
    pstats = {}
    if dec is None:
        L.append("## PTAB arms\n\nNot run: `data/tide/ptab_decisions.csv` is absent (USPTO ODP fetch pending). "
                 "Tide is not decided by this run.\n\n")
    else:
        tick = edgar_tickers()
        dd = dec.copy()
        dd["date"] = pd.to_datetime(dd["date"]).dt.date
        all_dates: dict[str, set] = {}
        for name, g in dd.groupby("name"):
            hit = match_listed(str(name), tick)
            if hit:
                all_dates.setdefault(hit["ticker"], set()).update(g["date"])
        for kind, title in (("fwd", "final written decisions (primary; decides Tide)"),
                            ("institution", "institution decisions (secondary)")):
            ev, notes = ptab_arm(dec, kind, tick, all_dates)
            frames.append(ev)
            L.append(f"## PTAB arm: {title}\n\n")
            if ev.empty:
                L.append("No matched events.\n\n")
                continue
            prim = ev[(ev["sample"] == "primary") & ev["reacting"]]
            hold = ev[(ev["sample"] == "holdout") & ev["reacting"]]
            sp, sh = arm_stats(prim), arm_stats(hold)
            pstats[kind] = sp
            n_prim = int((ev["sample"] == "primary").sum())
            L.append(f"- Events with usable windows, primary sample: {n_prim}; reacting: {len(prim)} "
                     f"({len(prim) / max(n_prim, 1):.0%}).\n")
            L.append("- Excluded before the screen: " + "; ".join(f"{k} ({v})" for k, v in notes.items()) + "\n\n")
            L.append("| Primary sample | Value |\n|---|---|\n" + "".join(stats_rows(sp)))
            ctl = prim[prim["n_control"] >= 3] if "n_control" in prim else prim.iloc[0:0]
            if len(ctl):
                diff = (ctl["G"] - ctl["control_mean"]).values
                L.append(f"| Control (secondary): mean G minus control, p | {fmt(float(diff.mean()))} (n = {len(diff)}), "
                         f"{bootstrap_mean_p(diff):.3f} |\n")
            L += split_rows(prim, "direction", "Direction") + split_rows(prim, "side", "Side") + split_rows(prim, "year", "Year")
            v = verdict(sp, MIN_PTAB)
            L.append(f"\nRegistered outcome under the rule: **{v}**" + (" (decides Tide)" if kind == "fwd" else " (secondary)") + "\n\n")
            L.append("| Holdout (1 July 2025 to 30 September 2026) | Value |\n|---|---|\n" + "".join(stats_rows(sh)))
            if kind == "fwd" and v == "SUPPORT":
                ok = sh.get("n", 0) and sh["meanN"] > 0
                L.append(f"\nHoldout check: {'mean N above zero; carried forward to paper trading' if ok else 'Support, not confirmed in the holdout'}.\n")
            L.append("\n")
        ps = [pstats[k]["p"] for k in ("fwd", "institution") if k in pstats and pstats[k].get("n")]
        if len(ps) == 2:
            order = np.argsort(ps)
            adj = [0.0, 0.0]
            run = 0.0
            for rank, i in enumerate(order):
                run = max(run, min(1.0, (2 - rank) * ps[i]))
                adj[i] = run
            L.append(f"Holm across the two PTAB arms: final written decisions p {adj[0]:.3f}; institution p {adj[1]:.3f}.\n\n")

    # Earth arm
    ee = earth_arm()
    frames.append(ee)
    se = arm_stats(ee)
    L.append("## Earth arm (companion; Earth v2's 40 reacting events; gross totals seen before this specification)\n\n")
    L.append("| Statistic | Value |\n|---|---|\n" + "".join(stats_rows(se)) + "".join(split_rows(ee, "direction", "Direction")))
    L.append(f"\nOutcome under the rule (companion; cannot decide Tide): **{verdict(se, MIN_EARTH)}**\n\n")

    L.append("## Limitations\n\nAs `tide_prereg.md`: survivorship in the company list and prices; no borrow cost on short positions; "
             "closing-auction entry; events treated as independent.\n")
    out.write_text("".join(L))
    allev = pd.concat([f for f in frames if len(f)], ignore_index=True)
    allev.to_csv(out.with_suffix(".events.csv"), index=False)
    log(f"wrote {out}")


if __name__ == "__main__":
    main()
