"""Project Air capture (prereg/air_prereg.md): detect new rulings, store one-minute and daily prices while they can
still be fetched, and log events. Runs daily after the US close in GitHub Actions; never recomputes old captures.

Supreme Court: the term's slip-opinion page, matched by docket to data/air/ot2026_register.csv.
Federal Circuit: precedential opinions after 30 October 2026 from CourtListener (one small query per day),
parties matched to EDGAR exactly (Earth item 3) or through Exhibit 21 (Moon).

AIR_SELFTEST=1 runs on synthetic inputs in a scratch folder and touches no network.
"""
from __future__ import annotations

import datetime as dt
import io
import os
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
SELFTEST = os.environ.get("AIR_SELFTEST") == "1"
AIR = Path(os.environ.get("AIR_DIR") or ROOT / "data" / "air")
CAFC_FROM = dt.date(2026, 10, 31)
CAFC_TO = dt.date(2027, 6, 30)
SCOTUS_TERM = "26"
EVENTS = AIR / "events.csv"
EV_COLS = ["event_id", "court", "decision_date", "docket", "case_name", "outcome", "ticker", "role", "side",
           "category", "detected_utc", "minute_captured_utc", "daily_captured_utc", "note"]


def log(m: str) -> None:
    print(m, file=sys.stderr, flush=True)


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_events() -> pd.DataFrame:
    if EVENTS.exists():
        return pd.read_csv(EVENTS, dtype=str).fillna("")
    return pd.DataFrame(columns=EV_COLS)


# ----------------------------------------------------------------------------- detection

def scotus_decisions() -> pd.DataFrame:
    """Rows: date, docket, case_name, from the term's slip-opinion table."""
    if SELFTEST:
        return pd.DataFrame([dict(date="2026-11-04", docket="25-100", case_name="Synth Corp. v. Doe")])
    url = f"https://www.supremecourt.gov/opinions/slipopinion/{SCOTUS_TERM}"
    r = requests.get(url, headers={"User-Agent": "act-trigger research (https://github.com/phykit/act-trigger)"}, timeout=60)
    if r.status_code != 200:
        log(f"slip-opinion page status {r.status_code}")
        return pd.DataFrame(columns=["date", "docket", "case_name"])
    try:
        tables = pd.read_html(io.StringIO(r.text))
    except ValueError:
        return pd.DataFrame(columns=["date", "docket", "case_name"])
    rows = []
    for t in tables:
        cols = [str(c).lower() for c in t.columns]
        if not any("docket" in c for c in cols):
            continue
        t.columns = cols
        dcol = next(c for c in cols if "date" in c)
        kcol = next(c for c in cols if "docket" in c)
        ncol = next(c for c in cols if "name" in c)
        for _, x in t.iterrows():
            try:
                d = pd.to_datetime(str(x[dcol])).date().isoformat()
            except (ValueError, TypeError):
                continue
            rows.append(dict(date=d, docket=str(x[kcol]).strip(), case_name=str(x[ncol]).strip()))
    return pd.DataFrame(rows, columns=["date", "docket", "case_name"])


def cafc_decisions(since: dt.date) -> pd.DataFrame:
    if SELFTEST:
        return pd.DataFrame([dict(date="2026-11-05", docket="25-1234", case_name="SYNTH001 Inc. v. SYNTH002 Inc.")])
    hdr = {"User-Agent": "act-trigger research (https://github.com/phykit/act-trigger)"}
    tok = os.environ.get("COURTLISTENER_TOKEN")
    if tok:
        hdr["Authorization"] = "Token " + tok
    url = ("https://www.courtlistener.com/api/rest/v4/search/?type=o&court=cafc"
           f"&filed_after={since.isoformat()}&order_by=dateFiled%20asc")
    rows = []
    while url:
        for attempt in range(6):
            r = requests.get(url, headers=hdr, timeout=90)
            if r.status_code == 200:
                break
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(int(r.headers.get("Retry-After", 0) or 0) or 30 * (attempt + 1))
                continue
            raise RuntimeError(f"CourtListener {r.status_code}")
        else:
            raise RuntimeError("CourtListener throttled; detection retried next run")
        j = r.json()
        for it in j.get("results", []):
            if str(it.get("status", "")).lower() not in ("published", "precedential"):
                continue
            rows.append(dict(date=str(it.get("dateFiled"))[:10], docket=str(it.get("docketNumber", "")),
                             case_name=str(it.get("caseName", ""))))
        url = j.get("next")
        time.sleep(1)
    return pd.DataFrame(rows, columns=["date", "docket", "case_name"])


# ----------------------------------------------------------------------------- party matching (Federal Circuit)

def cafc_parties(case_name: str) -> list[dict]:
    if SELFTEST:
        return [dict(ticker="S001", role="direct", side="appellant"), dict(ticker="S002", role="direct", side="appellee")]
    sys.path.insert(0, str(ROOT / "scripts"))
    import appeals_common as ac  # noqa: PLC0415
    tick = ac.edgar_tickers()
    out = []
    a, b = ac.split_parties(case_name)
    for side, name in (("first-named", a), ("second-named", b)):
        if not name:
            continue
        m = ac.match_listed(name, tick)
        if m:
            out.append(dict(ticker=m["ticker"], role="direct", side=side))
            continue
        p = ac.ex21_parent(name, tick)
        if p.get("status") == "resolved" and p.get("ticker"):
            out.append(dict(ticker=p["ticker"], role="parent", side=side))
    return out


# ----------------------------------------------------------------------------- prices

def minute_bars(ticker: str) -> pd.DataFrame:
    if SELFTEST:
        idx = pd.date_range("2026-11-04 14:30", periods=390, freq="1min", tz="UTC")
        return pd.DataFrame({"Close": range(390)}, index=idx)
    import yfinance as yf  # noqa: PLC0415
    df = yf.download(ticker, period="7d", interval="1m", progress=False, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


def daily_bars(ticker: str, day0: dt.date) -> pd.DataFrame:
    if SELFTEST:
        idx = pd.bdate_range(day0 - dt.timedelta(days=400), day0 + dt.timedelta(days=20))
        return pd.DataFrame({"Close": range(len(idx)), "High": range(len(idx)), "Low": range(len(idx))}, index=idx)
    import yfinance as yf  # noqa: PLC0415
    df = yf.download(ticker, start=(day0 - dt.timedelta(days=400)).isoformat(),
                     end=(day0 + dt.timedelta(days=25)).isoformat(), progress=False, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


# ----------------------------------------------------------------------------- main

def main() -> None:
    AIR.mkdir(parents=True, exist_ok=True)
    (AIR / "minute").mkdir(exist_ok=True)
    (AIR / "daily").mkdir(exist_ok=True)
    ev = load_events()
    seen = set(ev["event_id"])
    today = dt.date.today() if not SELFTEST else dt.date(2026, 11, 6)
    new = []

    reg_path = AIR / "ot2026_register.csv"
    if reg_path.exists():
        reg = pd.read_csv(reg_path, dtype=str).fillna("")
        sc = scotus_decisions()
        for _, d in sc.iterrows():
            for _, r in reg[reg["docket"].str.strip() == d["docket"]].iterrows():
                eid = f"SC-{d['docket']}-{r['ticker']}"
                if eid not in seen:
                    new.append(dict(event_id=eid, court="scotus", decision_date=d["date"], docket=d["docket"],
                                    case_name=d["case_name"], outcome="", ticker=r["ticker"],
                                    role={"a": "direct", "b": "parent", "c": "industry"}.get(r.get("category", ""), r.get("category", "")),
                                    side=r.get("side", ""), category=r.get("category", ""), detected_utc=now()))
    else:
        log("no Supreme Court register committed yet; Supreme Court detection skipped")

    try:
        last = max([dt.date.fromisoformat(x) for x in ev.loc[ev["court"] == "cafc", "decision_date"]] or [CAFC_FROM])
        cf = cafc_decisions(max(CAFC_FROM, last - dt.timedelta(days=3)))
        for _, d in cf.iterrows():
            if not (CAFC_FROM.isoformat() <= d["date"] <= CAFC_TO.isoformat()):
                continue
            for p in cafc_parties(d["case_name"]):
                eid = f"FC-{d['docket']}-{p['ticker']}"
                if eid not in seen and eid not in {n["event_id"] for n in new}:
                    new.append(dict(event_id=eid, court="cafc", decision_date=d["date"], docket=d["docket"],
                                    case_name=d["case_name"], outcome="", ticker=p["ticker"], role=p["role"],
                                    side=p["side"], category="mechanical", detected_utc=now()))
    except Exception as exc:  # noqa: BLE001
        log(f"Federal Circuit detection failed this run, retried next run: {str(exc)[:160]}")

    if new:
        ev = pd.concat([ev, pd.DataFrame(new)], ignore_index=True).fillna("")
        log(f"{len(new)} new events")

    # One-minute capture: possible only within seven calendar days of the decision.
    for i, e in ev.iterrows():
        if e["minute_captured_utc"]:
            continue
        d0 = dt.date.fromisoformat(e["decision_date"])
        if (today - d0).days > 6:
            if not e["note"]:
                ev.at[i, "note"] = "minute capture missed (more than seven days after decision)"
            continue
        if (today - d0).days < 0:
            continue
        ok = True
        for t in (e["ticker"], "SPY"):
            f = AIR / "minute" / f"{e['event_id']}_{t}.csv.gz"
            if t == "SPY":
                f = AIR / "minute" / f"SPY_{e['decision_date']}.csv.gz"
                if f.exists():
                    continue
            try:
                df = minute_bars(t)
                if df.empty:
                    ok = False
                    continue
                df.to_csv(f)
            except Exception as exc:  # noqa: BLE001
                ok = False
                log(f"minute bars failed {t}: {str(exc)[:100]}")
        if ok:
            ev.at[i, "minute_captured_utc"] = now()

    # Daily capture once ten trading days have passed (about 15 calendar days).
    for i, e in ev.iterrows():
        if e["daily_captured_utc"]:
            continue
        d0 = dt.date.fromisoformat(e["decision_date"])
        if (today - d0).days < 15:
            continue
        try:
            for t in (e["ticker"], "SPY"):
                daily_bars(t, d0).to_csv(AIR / "daily" / f"{e['event_id']}_{t}.csv.gz")
            ev.at[i, "daily_captured_utc"] = now()
        except Exception as exc:  # noqa: BLE001
            log(f"daily bars failed {e['event_id']}: {str(exc)[:100]}")

    ev[EV_COLS].to_csv(EVENTS, index=False)
    log(f"events: {len(ev)}; minute captured {int((ev['minute_captured_utc'] != '').sum())}; "
        f"daily captured {int((ev['daily_captured_utc'] != '').sum())}")


if __name__ == "__main__":
    main()
