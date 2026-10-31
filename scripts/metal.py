"""Project Metal: does legal complexity push more of the price adjustment after the ruling day (prereg/metal_prereg.md)?

Complexity (0 to 3): length above the population median, two or more opinions in the cluster, partial disposition.
Opinion metrics come from CourtListener and are cached as numbers only (no opinion text) in
data/appeals/metal_opinion_metrics.csv, so a throttled run resumes and reruns repeat no requests.

Usage: python scripts/metal.py   (after scripts/build_universe.py; needs COURTLISTENER_TOKEN)
"""
from __future__ import annotations

import datetime as dt
import html
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appeals_common import (SELFTEST, adata, build_party_map, build_universe, compute_events, log,  # noqa: E402
                            result_path, scdb_table, spec_hash)

MIN_GROUP = 30
P_THRESH = 0.05
SEED = 20261030


def fmt(x: float, pct: bool = True) -> str:
    if x is None or not np.isfinite(x):
        return "n/a"
    return f"{100 * x:+.2f}%" if pct else f"{x:.3f}"


CAP = int(os.environ.get("CL_MAX_REQUESTS", "0") or 0)   # per-run CourtListener request cap; 0 = no cap
REQ = [0]


class RequestCapReached(RuntimeError):
    pass


def _get(url: str, hdr: dict) -> requests.Response | None:
    for attempt in range(6):
        if CAP and REQ[0] >= CAP:
            raise RequestCapReached(f"CourtListener request cap of {CAP} reached")
        REQ[0] += 1
        r = requests.get(url, headers=hdr, timeout=90)
        if r.status_code == 200:
            return r
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(min(int(r.headers.get("Retry-After", 0) or 0) or 30 * (attempt + 1), 300))
            continue
        return None
    return None


def opinion_metrics(court: str, docket: str, date: dt.date) -> dict:
    """Word count of all opinions in the cluster, number of opinions, and the last 600 characters of the lead opinion."""
    if SELFTEST:
        h = abs(hash((court, docket))) % 1000
        return dict(status="ok", words=2000 + 40 * h, n_opinions=1 + h % 3, tail="AFFIRMED-IN-PART" if h % 4 == 0 else "AFFIRMED")
    hdr = {"User-Agent": "act-trigger research (https://github.com/phykit/act-trigger)"}
    tok = os.environ.get("COURTLISTENER_TOKEN")
    if tok:
        hdr["Authorization"] = "Token " + tok
    base = f"https://www.courtlistener.com/api/rest/v4/search/?type=o&court={court}"
    if court == "cafc":
        # GovInfo docket "14-01060, 14-01091": search the lead docket in both of CourtListener's forms
        yy, nn = str(docket).split(",")[0].strip().split("-")[:2]
        short, long_ = f"{yy}-{int(nn)}", f"20{yy}-{int(nn)}"
        q = f'{base}&q=' + requests.utils.quote(f'docketNumber:("{short}" OR "{long_}")')
    else:
        q = f"{base}&q=docketNumber%3A%22{requests.utils.quote(str(docket))}%22"
    if court == "cafc":
        q += f"&filed_after={(date - dt.timedelta(days=3)).isoformat()}&filed_before={(date + dt.timedelta(days=3)).isoformat()}"
    r = _get(q, hdr)
    if r is None:
        return dict(status="search failed")
    res = r.json().get("results", [])
    if not res:
        return dict(status="no cluster found")
    ops = [o for o in res[0].get("opinions", []) if o.get("id")]
    words, tail, n = 0, "", 0
    for k, op in enumerate(ops[:10]):
        o = _get(f"https://www.courtlistener.com/api/rest/v4/opinions/{op['id']}/", hdr)
        if o is None:
            return dict(status="opinion fetch failed")
        j = o.json()
        t = j.get("plain_text") or re.sub(r"(?s)<[^>]+>", " ", html.unescape(j.get("html_with_citations") or j.get("html") or j.get("xml_harvard") or ""))
        words += len(t.split())
        n += 1
        if k == 0:
            tail = re.sub(r"\s+", " ", t)[-600:]
        time.sleep(1)
    if n == 0:
        return dict(status="no opinion text")
    return dict(status="ok", words=words, n_opinions=n, tail=tail)


def perm_p(a: np.ndarray, b: np.ndarray, draws: int = 10_000) -> float:
    rng = np.random.default_rng(SEED)
    obs, pool, na, cnt = a.mean() - b.mean(), np.concatenate([a, b]), len(a), 0
    for _ in range(draws):
        rng.shuffle(pool)
        cnt += (pool[:na].mean() - pool[na:].mean()) >= obs
    return float(cnt / draws)


def main() -> None:
    h = spec_hash("metal")
    uni, unote = build_universe()
    pm = build_party_map(uni)
    ev, _, _ = compute_events(uni, pm, ("listed",), "litigants", post=5)
    ev = ev[ev["status"] == "ok"].copy()
    # SCDB disposition for Supreme Court rulings
    disp = {}
    if not SELFTEST:
        full, _ = scdb_table()
        for _, r in full.iterrows():
            disp[(str(r["docket"]), pd.to_datetime(r["dateDecision"]).date())] = r.get("caseDisposition")
    cache_f = adata("metal_opinion_metrics.csv")
    cache = pd.read_csv(cache_f, dtype={"docket": str}).to_dict("records") if cache_f.exists() else []
    have = {(c["court"], str(c["docket"]), str(c["date"])): c for c in cache if c.get("status") == "ok"}
    rows = []
    for rid in sorted(ev["ruling"].unique()):
        u = uni.loc[int(rid)]
        d0 = u["date"] if isinstance(u["date"], dt.date) else pd.Timestamp(u["date"]).date()
        key = (u["court"], str(u["docket"]), d0.isoformat())
        m = have.get(key)
        if m is None:
            try:
                m = dict(court=u["court"], docket=str(u["docket"]), date=d0.isoformat(), **opinion_metrics(u["court"], str(u["docket"]), d0))
            except RequestCapReached as exc:
                left = len([r for r in ev["ruling"].unique() if int(r) >= int(rid)])
                log(f"{exc}; {left} rulings still to fetch; metrics cached so far are committed and the next run resumes. "
                    "No result is written for an incomplete population.")
                return
            cache.append(m)
            pd.DataFrame(cache).to_csv(cache_f, index=False)
        if u["court"] == "scotus":
            cd = disp.get((str(u["docket"]), d0)) if not SELFTEST else (6 if int(rid) % 5 == 0 else 2)
            partial = 1 if pd.notna(cd) and int(cd) in (6, 7, 8) else 0
        else:
            partial = 1 if re.search(r"IN PART|REMAND", str(m.get("tail", "")), flags=re.I) else 0
        rows.append(dict(ruling=int(rid), court=u["court"], op_status=m.get("status"), words=m.get("words"),
                         n_opinions=m.get("n_opinions"), partial=partial))
    met = pd.DataFrame(rows)
    ev = ev.merge(met, on=["ruling", "court"], how="left")
    sc = ev[ev["op_status"] == "ok"].copy()
    med = float(pd.to_numeric(sc["words"]).median())
    sc["length"] = (pd.to_numeric(sc["words"]) > med).astype(int)
    sc["separate"] = (pd.to_numeric(sc["n_opinions"]) >= 2).astype(int)
    sc["score"] = sc["length"] + sc["separate"] + sc["partial"]
    sc["complex"] = sc["score"] >= 2
    tot = sc["ar0"].abs() + sc["car_post"].abs()
    sc = sc[tot >= sc["sigma"]].copy()
    sc["P"] = sc["car_post"].abs() / (sc["ar0"].abs() + sc["car_post"].abs())
    cx, sp = sc[sc["complex"]], sc[~sc["complex"]]
    diff = float(cx["P"].mean() - sp["P"].mean()) if len(cx) and len(sp) else float("nan")
    p = perm_p(cx["P"].values, sp["P"].values) if len(cx) and len(sp) else float("nan")
    react = sc[sc["reacting"] == True]  # noqa: E712
    rc, rs = react[react["complex"]], react[~react["complex"]]
    if len(cx) < MIN_GROUP or len(sp) < MIN_GROUP:
        outcome = "UNSCORABLE"
    elif diff > 0 and p < P_THRESH:
        outcome = "SUPPORT"
    elif diff <= 0:
        outcome = "KILL"
    else:
        outcome = "INCONCLUSIVE"
    unscor = ev[ev["op_status"] != "ok"]
    L = ["# Result: Project Metal (legal complexity and post-ruling share of movement)\n",
         f"Run {dt.date.today().isoformat()} against metal_prereg.md, SHA-256 {h} (hashed before the run). Non-evidentiary: daily closes, one parameter set, no costs.\n"]
    if SELFTEST:
        L.append("**SELF-TEST RUN ON SYNTHETIC DATA. Not a result.**\n")
    L += ["## Population\n", f"- Universe: {unote}.",
          f"- Earth events with usable windows: {len(ev)}; with opinion metrics: {int((ev['op_status'] == 'ok').sum())}; "
          f"after the minimum-movement exclusion: {len(sc)} ({len(cx)} complex, {len(sp)} simple). Median word count {med:,.0f}.",
          "- Unscorable (opinion metrics unavailable): " + ("; ".join(f"{k} ({v})" for k, v in unscor["op_status"].value_counts().items()) if len(unscor) else "none") + ".\n",
          "## Outcomes\n", "| Statistic | Value |", "|---|---|",
          f"| Mean post-ruling share P, complex | {fmt(float(cx['P'].mean()) if len(cx) else float('nan'), False)} (n = {len(cx)}) |",
          f"| Mean post-ruling share P, simple | {fmt(float(sp['P'].mean()) if len(sp) else float('nan'), False)} (n = {len(sp)}) |",
          f"| Primary: difference | {fmt(diff, False)} |",
          f"| Permutation p, one-sided | {fmt(p, False)} |",
          f"| Reacting events: signed CAR(+1,+5), complex minus simple | "
          f"{fmt(float(rc['signed_post'].mean() - rs['signed_post'].mean()) if len(rc) and len(rs) else float('nan'))} ({len(rc)} v {len(rs)}) |"]
    for comp in ("length", "separate", "partial"):
        a, b = sc[sc[comp] == 1], sc[sc[comp] == 0]
        L.append(f"| Component {comp}: P with minus without | {fmt(float(a['P'].mean() - b['P'].mean()) if len(a) and len(b) else float('nan'), False)} ({len(a)} v {len(b)}) |")
    for court in sorted(sc["court"].unique()):
        s = sc[sc["court"] == court]
        a, b = s[s["complex"]], s[~s["complex"]]
        L.append(f"| {court}: P complex minus simple | {fmt(float(a['P'].mean() - b['P'].mean()) if len(a) and len(b) else float('nan'), False)} ({len(a)} v {len(b)}) |")
    L += ["", "## Decision rule as registered\n",
          f"- At least {MIN_GROUP} complex and {MIN_GROUP} simple events: {'met' if len(cx) >= MIN_GROUP and len(sp) >= MIN_GROUP else 'not met'} ({len(cx)}, {len(sp)}).",
          f"- Support: difference above zero with permutation p below {P_THRESH}; kill: at or below zero.\n",
          f"Registered outcome: {outcome}.\n",
          "## What this does not license\n",
          "- Word and opinion counts are proxies for complexity; the share P is noisy when the day-0 move is small.\n"]
    out = result_path("metal")
    out.write_text("\n".join(L) + "\n")
    sc.drop(columns=["control_days"], errors="ignore").to_csv(out.with_suffix(".events.csv"), index=False)
    log(f"wrote {out}; outcome {outcome}; diff {fmt(diff, False)} p={fmt(p, False)}")


if __name__ == "__main__":
    main()
