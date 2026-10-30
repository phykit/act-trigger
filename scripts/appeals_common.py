"""Shared data layer for Projects Earth, Moon and Fire (appellate rulings and listed companies).

Sources, all free: SCDB (Supreme Court), CourtListener or the CAFC opinions table (Federal Circuit),
EDGAR (company list, submissions, full-text search of Exhibit 21, browse by SIC), yfinance (prices).
Everything fetched is cached under data/appeals/ so a rerun reproduces the inputs. RULINGS_SELFTEST=1
replaces every network call with synthetic data and writes nothing under data/ or results/.
"""
from __future__ import annotations

import datetime as dt
import gzip
import hashlib
import io
import json
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rulings_common import ROOT, SELFTEST, log, result_path, scdb_table, spec_hash  # noqa: E402,F401

ADATA = ROOT / "data" / "appeals"
SEC_UA = os.environ.get("SEC_CONTACT") or "Simon Kittson skittson@gmail.com"  # SEC fair-access format: name and email
UA_PLAIN = {"User-Agent": "act-trigger research scripts (https://github.com/phykit/act-trigger)"}
TERMS = list(range(5, 25))                 # OT2005 to OT2024
CAFC_FROM, CAFC_TO = dt.date(2012, 1, 1), dt.date(2025, 6, 30)
PRICE_START = dt.date(2004, 1, 1)
SUFFIXES = {"INC", "INCORPORATED", "CORP", "CORPORATION", "CO", "COMPANY", "LLC", "LTD", "LIMITED", "LP",
            "PLC", "NA", "N A", "HOLDINGS", "HOLDING", "GROUP", "THE", "AG", "SA", "SE", "NV", "BV", "ET AL"}
_last_sec = [0.0]
GOV_EXACT = {"UNITED STATES", "US", "U S", "UNITED STATES OF AMERICA", "USA"}
GOV_WORDS = (r"\b(COMMISSIONER|SECRETARY|DEPARTMENT|DEPT|BOARD OF|COMMISSION|AGENCY|ADMINISTRATION|ADMINISTRATOR|"
             r"ATTORNEY GENERAL|STATE OF|COMMONWEALTH|CITY OF|COUNTY|TOWN OF|VILLAGE OF|FEDERAL|NATIONAL LABOR|"
             r"TRADE COMMISSION|SECURITIES AND EXCHANGE|PATENT AND TRADEMARK|USPTO|NLRB|EPA|FTC|SEC|FCC|FDA|IRS|"
             r"IANCU|KAPPOS|VIDAL|HIRSHFELD|SQUIRES|STEWART|DIRECTOR|GOVERNOR|TREASURY|INTERNAL REVENUE|UNIVERSITY|"
             r"SCHOOL DISTRICT|REPUBLIC OF|KINGDOM OF|GOVERNMENT|MINISTRY|TRIBE|NATION|BAND OF|PUEBLO|JUDICIAL DISTRICT|"
             r"SUPERIOR COURT|DISTRICT COURT)\b")


def adata(name: str) -> Path:
    base = Path(os.environ.get("RULINGS_SCRATCH", ADATA)) if SELFTEST else ADATA
    base.mkdir(parents=True, exist_ok=True)
    return base / name


# ----------------------------------------------------------------------------- EDGAR

def sec_get(url: str, timeout: int = 60, tries: int = 3) -> requests.Response:
    """GET against SEC hosts at no more than eight requests a second, with the declared user agent."""
    for attempt in range(tries):
        wait = 0.13 - (time.time() - _last_sec[0])
        if wait > 0:
            time.sleep(wait)
        _last_sec[0] = time.time()
        r = requests.get(url, headers={"User-Agent": SEC_UA, "Accept-Encoding": "gzip, deflate"}, timeout=timeout)
        if r.status_code == 200:
            return r
        if r.status_code in (403, 429, 503):
            time.sleep(5 * (attempt + 1))
            continue
        r.raise_for_status()
    r.raise_for_status()
    return r


def normalise(name: str) -> str:
    s = str(name).upper()
    s = s.split(";")[0]
    s = re.sub(r"\bET\s*AL\b\.?", " ", s)                                            # "et al." (spec item 3)
    s = re.sub(r",?\s*\b(PETITIONERS?|RESPONDENTS?|APPELLANTS?|APPELLEES?)\b\.?", " ", s)  # SCDB role labels
    s = re.sub(r"/[^/]*/", " ", s)       # EDGAR state suffixes such as /DE/ or /NEW/
    s = re.sub(r"\bN\.?A\.?(?=\s|$|,)", " ", s)   # national association suffix
    s = re.sub(r"\(.*?\)", " ", s)
    s = s.replace("&", " AND ")
    s = re.sub(r"[^A-Z0-9 ]+", " ", s)
    toks = [t for t in s.split() if t not in SUFFIXES and t != "AND"]
    return " ".join(toks)


def edgar_tickers() -> pd.DataFrame:
    """EDGAR's company list: one row per ticker, with the normalised title."""
    cache = adata("edgar_company_tickers.csv")
    if cache.exists():
        return pd.read_csv(cache, dtype={"cik": str, "ticker": str, "title": str, "norm": str})
    if SELFTEST:
        rng = np.random.default_rng(3)
        names = [f"SYNTH{c:03d}" for c in range(120)]
        df = pd.DataFrame({"cik": [f"{1000 + i:010d}" for i in range(120)], "ticker": [f"S{i:03d}" for i in range(120)],
                           "title": [f"{n} Inc." for n in names], "sic": rng.choice(["1000", "2000", "3000", "4000"], 120)})
        df["norm"] = df["title"].map(normalise)
        df.to_csv(cache, index=False)
        return df
    try:
        r = sec_get("https://www.sec.gov/files/company_tickers.json")
        j = r.json()
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"EDGAR company list unavailable ({str(exc)[:160]}); user agent was {SEC_UA!r}") from exc
    rows = [dict(cik=f"{int(v['cik_str']):010d}", ticker=str(v["ticker"]), title=str(v["title"])) for v in j.values()]
    df = pd.DataFrame(rows)
    df["norm"] = df["title"].map(normalise)
    df.to_csv(cache, index=False)
    return df


def match_listed(name: str, tick: pd.DataFrame) -> dict | None:
    n = normalise(name)
    if not n:
        return None
    hit = tick[tick["norm"] == n]
    if len(hit) == 0:
        return None
    row = hit.iloc[0]
    return dict(cik=row["cik"], ticker=row["ticker"], title=row["title"])


def ex21_parent(name: str, tick: pd.DataFrame) -> dict:
    """Find the filer whose Exhibit 21 lists `name`; status resolved | ambiguous | none | error."""
    cache = adata("ex21_lookups.json")
    store = json.loads(cache.read_text()) if cache.exists() else {}
    key = name.strip()
    if key in store:
        return store[key]
    if SELFTEST:
        m = re.search(r"SYNTH(\d{3})", key)
        if m and int(m.group(1)) % 2 == 1:
            row = tick[tick["title"].str.contains(f"SYNTH{m.group(1)}")].iloc[0]
            out = dict(status="resolved", cik=row["cik"], ticker=row["ticker"], title=row["title"], hits=3, total=3)
        else:
            out = dict(status="none", cik=None, hits=0, total=0)
        store[key] = out
        cache.write_text(json.dumps(store))
        return out
    phrase = re.sub(r"[^A-Za-z0-9 .&'-]", " ", key).strip()
    url = ("https://efts.sec.gov/LATEST/search-index?q=" + requests.utils.quote(f'"{phrase}"')
           + "&forms=10-K&dateRange=custom&startdt=2001-01-01&enddt=2026-12-31")
    try:
        j = sec_get(url).json()
        hits = [h["_source"] for h in j.get("hits", {}).get("hits", [])]
    except Exception as exc:  # noqa: BLE001
        out = dict(status="error", cik=None, hits=0, total=0, error=str(exc)[:100])
        store[key] = out
        cache.write_text(json.dumps(store))
        return out
    ex21 = [h for h in hits if str(h.get("file_type", "")).upper().startswith("EX-21")]
    counts: dict[str, int] = {}
    for h in ex21:
        for c in h.get("ciks", []) or []:
            counts[f"{int(c):010d}"] = counts.get(f"{int(c):010d}", 0) + 1
    total = sum(counts.values())
    if total == 0:
        out = dict(status="none", cik=None, hits=0, total=0)
    else:
        cik, n = max(counts.items(), key=lambda kv: kv[1])
        if n == total or (n >= 3 and n / total >= 0.8):
            out = dict(status="resolved", cik=cik, hits=n, total=total)
        else:
            out = dict(status="ambiguous", cik=None, hits=n, total=total)
    if out["status"] == "resolved":
        t = tick[tick["cik"] == out["cik"]]
        out["ticker"] = t["ticker"].iloc[0] if len(t) else None
        out["title"] = t["title"].iloc[0] if len(t) else None
        if out["ticker"] is None:
            out["status"] = "parent not listed"
    store[key] = out
    cache.write_text(json.dumps(store))
    return out


def submissions(cik: str) -> dict:
    raw = adata("raw")
    raw.mkdir(parents=True, exist_ok=True)
    cache = raw / f"sub_{cik}.json"
    if cache.exists():
        return json.loads(cache.read_text())
    if SELFTEST:
        rng = np.random.default_rng(int(cik[-4:]))
        dates = sorted({(dt.date(2006, 1, 15) + dt.timedelta(days=int(d))).isoformat()
                        for d in rng.integers(0, 7000, 80)})
        j = dict(cik=cik, sic=str(rng.choice(["1000", "2000", "3000", "4000"])),
                 filings=dict(recent=dict(form=["8-K"] * len(dates), filingDate=dates, items=["2.02,9.01"] * len(dates)),
                              files=[]))
        cache.write_text(json.dumps(j))
        return j
    j = sec_get(f"https://data.sec.gov/submissions/CIK{cik}.json").json()
    extra = []
    for f in j.get("filings", {}).get("files", []) or []:
        try:
            extra.append(sec_get(f"https://data.sec.gov/submissions/{f['name']}").json())
        except Exception as exc:  # noqa: BLE001
            log(f"submissions extra file failed for {cik}: {exc}")
    j["_extra"] = extra
    cache.write_text(json.dumps(j))
    return j


def _compact(name: str) -> dict:
    p = adata(name)
    return json.loads(p.read_text()) if p.exists() else {}


def _compact_put(name: str, key: str, value) -> None:
    p = adata(name)
    d = json.loads(p.read_text()) if p.exists() else {}
    d[key] = value
    p.write_text(json.dumps(d))


def earnings_dates(cik: str) -> set[dt.date]:
    store = _compact("earnings_dates.json")
    if cik in store:
        return {dt.date.fromisoformat(d) for d in store[cik]}
    j = submissions(cik)
    out = set()
    blocks = [j.get("filings", {}).get("recent", {})] + list(j.get("_extra", []))
    for b in blocks:
        forms, dates, items = b.get("form", []), b.get("filingDate", []), b.get("items", [])
        for f, d, it in zip(forms, dates, items):
            if str(f).startswith("8-K") and "2.02" in str(it):
                out.add(dt.date.fromisoformat(d))
    _compact_put("earnings_dates.json", cik, sorted(d.isoformat() for d in out))
    return out


def sic_of(cik: str) -> str | None:
    store = _compact("sic_map.json")
    if cik in store:
        return store[cik] or None
    s = submissions(cik).get("sic")
    s = str(s) if s else None
    _compact_put("sic_map.json", cik, s)
    return s


def sic_peers(sic: str, tick: pd.DataFrame) -> list[dict]:
    """Companies with this SIC in EDGAR's browse, mapped to tickers, ascending CIK."""
    cache = adata(f"sic_{sic}.json")
    if cache.exists():
        ciks = json.loads(cache.read_text())
    elif SELFTEST:
        ciks = sorted(tick[tick["sic"].astype(str) == str(sic)]["cik"].tolist()) if "sic" in tick.columns else []
        cache.write_text(json.dumps(ciks))
    else:
        ciks = []
        start = 0
        while True:
            url = (f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&SIC={sic}&type=10-K&dateb=&owner=include"
                   f"&count=100&start={start}&output=atom")
            txt = sec_get(url).text
            found = re.findall(r"CIK=(\d{1,10})", txt)
            found = [f"{int(c):010d}" for c in found]
            new = [c for c in found if c not in ciks]
            ciks.extend(new)
            if len(found) < 100 or not new or start > 2000:
                break
            start += 100
        ciks = sorted(set(ciks))
        cache.write_text(json.dumps(ciks))
    out = []
    for c in ciks:
        t = tick[tick["cik"] == c]
        if len(t):
            out.append(dict(cik=c, ticker=t["ticker"].iloc[0], title=t["title"].iloc[0]))
    return out


# ----------------------------------------------------------------------------- universe

def split_parties(case_name: str) -> tuple[str, str]:
    s = str(case_name)
    parts = re.split(r"\s+v\.?\s+", s, maxsplit=1, flags=re.IGNORECASE)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return s.strip(), ""


def scdb_rulings() -> pd.DataFrame:
    full, ver = scdb_table()
    df = full[full["term"].isin([2000 + t for t in TERMS])].copy()
    df = df[df["decisionType"].isin([1, 5, 6, 7])] if "decisionType" in df.columns else df
    argued = pd.to_datetime(df.get("dateArgument"), errors="coerce")
    rearg = pd.to_datetime(df.get("dateRearg"), errors="coerce") if "dateRearg" in df.columns else pd.Series(pd.NaT, index=df.index)
    df["argued"] = pd.concat([argued, rearg], axis=1).max(axis=1)
    df = df.dropna(subset=["argued", "dateDecision"])
    out = pd.DataFrame({
        "court": "scotus", "date": pd.to_datetime(df["dateDecision"]).dt.date, "argued": df["argued"].dt.date,
        "docket": df["docket"].astype(str), "case_name": df["caseName"].astype(str),
        "party_winning": pd.to_numeric(df.get("partyWinning"), errors="coerce"),
        "decision_type": df.get("decisionType"), "precedential": True, "source": f"SCDB {ver}",
    })
    out[["petitioner", "respondent"]] = out["case_name"].apply(lambda s: pd.Series(split_parties(s)))
    return out.reset_index(drop=True)


def _courtlistener_cafc() -> pd.DataFrame:
    """Federal Circuit opinions from the CourtListener v4 search API; precedential ones kept client-side."""
    hdr = dict(UA_PLAIN)
    tok = os.environ.get("COURTLISTENER_TOKEN")
    if tok:
        hdr["Authorization"] = "Token " + tok
    # The search API stops paginating after about 1,000 results, so fetch in quarterly windows.
    windows = []
    q = pd.Timestamp(CAFC_FROM)
    while q.date() <= CAFC_TO:
        e = min((q + pd.offsets.QuarterEnd(0)).date(), CAFC_TO)
        windows.append((q.date(), e))
        q = pd.Timestamp(e) + pd.Timedelta(days=1)
    rows, pages = [], 0
    for w_from, w_to in windows:
      url = ("https://www.courtlistener.com/api/rest/v4/search/?type=o&court=cafc"
             f"&filed_after={w_from.isoformat()}&filed_before={w_to.isoformat()}&order_by=dateFiled%20asc")
      wpages = 0
      while url and wpages < 60:
          r = None
          for attempt in range(4):
              r = requests.get(url, headers=hdr, timeout=90)
              if r.status_code == 200:
                  break
              if r.status_code in (429, 500, 502, 503, 504):
                  time.sleep(10 * (attempt + 1))
                  continue
              raise RuntimeError(f"CourtListener status {r.status_code}: {r.text[:120]}")
          j = r.json()
          if pages == 0:
              first = (j.get("results") or [{}])[0]
              log(f"CourtListener first result keys: {sorted(first.keys())[:30]}; count {j.get('count')}")
          for it in j.get("results", []):
              ops = it.get("opinions") or [{}]
              status = str(it.get("status") or (ops[0].get("status") if isinstance(ops[0], dict) else "") or "")
              rows.append(dict(date=str(it.get("dateFiled"))[:10], docket=str(it.get("docketNumber", "")),
                               case_name=str(it.get("caseName", "")), status=status))
          url = j.get("next")
          pages += 1
          wpages += 1
          if pages % 50 == 0:
              log(f"CourtListener: {pages} pages, {len(rows)} rows")
          time.sleep(0.4)
      if wpages >= 60:
          log(f"CourtListener window {w_from} to {w_to} hit the page cap; window may be truncated")
    log(f"CourtListener: {len(windows)} quarterly windows, {pages} pages, {len(rows)} rows")
    if not rows:
        raise RuntimeError("CourtListener returned no rows")
    df = pd.DataFrame(rows)
    log(f"CourtListener status values: {df['status'].value_counts().to_dict()}")
    keep = df["status"].str.lower().isin(["published", "precedential"])
    df = df[keep].copy()
    if df.empty:
        raise RuntimeError("CourtListener returned rows but none marked published or precedential")
    df["source"] = "CourtListener v4"
    return df


def _cafc_table() -> pd.DataFrame:
    page = requests.get("https://cafc.uscourts.gov/home/case-information/opinions-orders/", headers=UA_PLAIN, timeout=60).text
    m = re.search(r"wdtNonce[\"']?\s*[:=]\s*[\"']([0-9a-f]+)", page)
    nonce = m.group(1) if m else ""
    rows, start, length = [], 0, 1000
    while start < 60000:
        data = {"draw": 1, "start": start, "length": length, "search[value]": "", "order[0][column]": 0,
                "order[0][dir]": "desc", "wdtNonce": nonce}
        for i in range(7):
            data[f"columns[{i}][data]"] = i
            data[f"columns[{i}][searchable]"] = "true"
            data[f"columns[{i}][orderable]"] = "true"
            data[f"columns[{i}][search][value]"] = ""
        r = requests.post("https://www.cafc.uscourts.gov/wp-admin/admin-ajax.php?action=get_wdtable&table_id=1",
                          data=data, headers=UA_PLAIN, timeout=120)
        if r.status_code != 200:
            raise RuntimeError(f"CAFC table status {r.status_code}")
        j = r.json()
        batch = j.get("data", [])
        if not batch:
            break
        for row in batch:
            cells = [re.sub(r"<[^>]+>", " ", str(c)).strip() for c in row]
            txt = " | ".join(cells)
            name = max((c for c in cells if re.search(r"\sv\.?\s", c, re.I)), key=len, default="")
            date = next((c for c in cells if re.match(r"\d{1,2}/\d{1,2}/\d{4}", c)), "")
            docket = next((c for c in cells if re.match(r"^\d{2}-\d{3,5}$", c)), "")
            if "OPINION" in txt.upper() and name:
                rows.append(dict(date=pd.to_datetime(date, errors="coerce"), docket=docket, case_name=name,
                                 status="Precedential" if "PRECEDENTIAL" in txt.upper() and "NONPRECEDENTIAL" not in txt.upper() else "Nonprecedential"))
        start += length
        time.sleep(1)
    if not rows:
        raise RuntimeError("CAFC table returned no opinion rows")
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")
    df = df[df["status"] == "Precedential"]
    df["source"] = "cafc.uscourts.gov table"
    return df


def cafc_rulings() -> tuple[pd.DataFrame, str]:
    cache = adata("cafc_precedential.csv")
    if cache.exists():
        df = pd.read_csv(cache, dtype=str)
        return df, (df["source"].iloc[0] if len(df) else "cache")
    if SELFTEST:
        return pd.DataFrame(columns=["date", "docket", "case_name", "status", "source"]), "none (self-test)"
    errors = []
    for fn in (_courtlistener_cafc, _cafc_table):
        try:
            df = fn()
            df = df.dropna(subset=["date"])
            df = df[(df["date"] >= CAFC_FROM.isoformat()) & (df["date"] <= CAFC_TO.isoformat())]
            df.to_csv(cache, index=False)
            log(f"Federal Circuit: {len(df)} precedential opinions from {df['source'].iloc[0]}")
            return df, df["source"].iloc[0]
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{fn.__name__}: {str(exc)[:160]}")
    log("Federal Circuit unavailable: " + " | ".join(errors))
    return pd.DataFrame(columns=["date", "docket", "case_name", "status", "source"]), "unavailable: " + " | ".join(errors)


def build_universe() -> tuple[pd.DataFrame, str]:
    """All rulings (SCOTUS plus Federal Circuit where reachable), one row per ruling, with both sides."""
    cache = adata("universe.csv")
    if cache.exists():
        df = pd.read_csv(cache, dtype={"docket": str})
        df["date"] = pd.to_datetime(df["date"]).dt.date
        note = adata("universe_note.txt").read_text() if adata("universe_note.txt").exists() else ""
        return df, note
    if SELFTEST:
        rng = np.random.default_rng(11)
        tick = edgar_tickers()
        rows = []
        for i in range(90):
            d = dt.date(2008, 1, 1) + dt.timedelta(days=int(rng.integers(0, 6000)))
            a, b = rng.choice(tick["title"], 2, replace=False)
            if rng.random() < 0.4:
                b = "United States"
            if rng.random() < 0.3:
                a = f"Opco Subsidiary of {a.replace(' Inc.', '')} LLC"
            rows.append(dict(court="scotus" if i % 2 else "cafc", date=d, argued=d - dt.timedelta(days=90), docket=f"{d.year % 100:02d}-{i}",
                             case_name=f"{a} v. {b}", party_winning=int(rng.integers(0, 2)), decision_type=1, precedential=True,
                             source="synthetic", petitioner=a, respondent=b))
        df = pd.DataFrame(rows)
        note = "synthetic"
    else:
        sc = scdb_rulings()
        cafc, src = cafc_rulings()
        if len(cafc):
            cafc = cafc.assign(court="cafc", date=pd.to_datetime(cafc["date"]).dt.date, argued=pd.NaT, party_winning=np.nan,
                               decision_type=np.nan, precedential=True)
            cafc[["petitioner", "respondent"]] = cafc["case_name"].apply(lambda s: pd.Series(split_parties(s)))
            df = pd.concat([sc, cafc[sc.columns]], ignore_index=True)
        else:
            df = sc
        note = f"SCOTUS {len(sc)} rulings ({sc['source'].iloc[0] if len(sc) else 'n/a'}); Federal Circuit {len(cafc)} precedential opinions ({src})"
    df.to_csv(cache, index=False)
    adata("universe_note.txt").write_text(note)
    return df, note


def build_party_map(universe: pd.DataFrame) -> pd.DataFrame:
    """One row per (ruling, side): listed match, Exhibit 21 parent, or unresolved."""
    cache = adata("party_map.csv")
    if cache.exists():
        df = pd.read_csv(cache, dtype=str)
        df["ruling"] = df["ruling"].astype(int)
        return df
    tick = edgar_tickers()
    rows = []
    seen_ex21: dict[str, dict] = {}
    for i, r in universe.iterrows():
        for side in ("petitioner", "respondent"):
            name = str(r[side])
            if not name or name.lower() in ("nan", ""):
                continue
            m = match_listed(name, tick)
            if m:
                rows.append(dict(ruling=i, side=side, name=name, basis="listed", cik=m["cik"], ticker=m["ticker"], title=m["title"]))
                continue
            key = normalise(name)
            gov = (key in GOV_EXACT or (key.startswith("UNITED STATES") and len(key.split()) <= 4)
                   or bool(re.search(GOV_WORDS, key)) or len(key) == 0)
            individual = len(key.split()) <= 2 and not re.search(r"\b(INC|CORP|LLC|CO|LTD|PLC|GROUP|HOLDINGS|TRUST|FUND|BANK|PARTNERS|ASSOCIATES)\b", str(name).upper().replace(".", ""))
            if gov or individual:
                rows.append(dict(ruling=i, side=side, name=name, basis="not a company", cik=None, ticker=None, title=None))
                continue
            if key not in seen_ex21:
                seen_ex21[key] = ex21_parent(name, tick)
            p = seen_ex21[key]
            if p.get("status") == "resolved":
                rows.append(dict(ruling=i, side=side, name=name, basis="ex21 parent", cik=p["cik"], ticker=p["ticker"], title=p.get("title")))
            else:
                rows.append(dict(ruling=i, side=side, name=name, basis=f"unresolved ({p.get('status')})", cik=None, ticker=None, title=None))
        if i % 100 == 0:
            log(f"party map: {i} rulings processed")
    df = pd.DataFrame(rows)
    df.to_csv(cache, index=False)
    df["ruling"] = df["ruling"].astype(int)
    return df


# ----------------------------------------------------------------------------- prices and market model

def _synthetic_prices(tickers: list[str]) -> pd.DataFrame:
    idx = pd.bdate_range(PRICE_START, dt.date.today())
    out = {}
    for t in tickers:
        seed = int(hashlib.sha256(t.encode()).hexdigest()[:8], 16)
        rng = np.random.default_rng(seed)
        vol = 0.010 if t == "SPY" else 0.022
        out[t] = 100 * np.exp(np.cumsum(rng.normal(0.0002, vol, len(idx))))
    return pd.DataFrame(out, index=idx)


def bulk_prices(tickers: list[str], label: str) -> pd.DataFrame:
    """Adjusted closes, wide (date x ticker), cached as a gzipped CSV under the given label."""
    tickers = sorted(set(str(t) for t in tickers if isinstance(t, str) and t and t.lower() != "nan"))
    cache = adata(f"prices_{label}.csv.gz")
    have = pd.DataFrame()
    if cache.exists():
        have = pd.read_csv(cache, index_col=0, parse_dates=True, compression="gzip")
    missing = [t for t in tickers if t not in have.columns]
    if missing:
        if SELFTEST:
            new = _synthetic_prices(missing)
        else:
            import yfinance as yf
            frames = []
            for k in range(0, len(missing), 150):
                chunk = missing[k:k + 150]
                for attempt in range(3):
                    try:
                        df = yf.download(chunk, start=PRICE_START.isoformat(), auto_adjust=True, progress=False, threads=True, group_by="column")
                        close = df["Close"] if isinstance(df.columns, pd.MultiIndex) else df[["Close"]].rename(columns={"Close": chunk[0]})
                        frames.append(close)
                        break
                    except Exception as exc:  # noqa: BLE001
                        log(f"yfinance chunk failed ({attempt}): {str(exc)[:100]}")
                        time.sleep(5 * (attempt + 1))
                time.sleep(1)
            new = pd.concat(frames, axis=1) if frames else pd.DataFrame()
            new = new.loc[:, ~new.columns.duplicated()] if len(new) else new
        if len(new):
            new.index = pd.to_datetime(new.index).tz_localize(None).normalize()
            have = pd.concat([have, new], axis=1) if len(have) else new
            have = have.loc[:, ~have.columns.duplicated()]
            have.to_csv(cache, compression="gzip")
    cols = [t for t in tickers if t in have.columns]
    return have[cols].sort_index()


def rolling_ar(px: pd.DataFrame, mkt: pd.Series, beta_win: int = 250, sig_win: int = 60) -> dict[str, pd.DataFrame]:
    """Per ticker: log return, lagged rolling market-model abnormal return, lagged rolling sigma, z."""
    r = np.log(px).diff()
    rm = np.log(mkt).diff().reindex(r.index)
    out = {}
    for t in r.columns:
        s = r[t]
        ok = s.notna() & rm.notna()
        if ok.sum() < beta_win + sig_win + 20:
            continue
        cov = s.rolling(beta_win, min_periods=200).cov(rm)
        var = rm.rolling(beta_win, min_periods=200).var()
        beta = (cov / var).shift(1)
        alpha = (s.rolling(beta_win, min_periods=200).mean() - beta * rm.rolling(beta_win, min_periods=200).mean()).shift(1)
        ar = s - (alpha + beta * rm)
        sigma = ar.rolling(sig_win, min_periods=40).std().shift(1)
        z = ar / sigma
        out[t] = pd.DataFrame({"ret": s, "ar": ar, "sigma": sigma, "z": z}).dropna(subset=["ar", "z"])
    return out


def window_stats(ar: pd.DataFrame, day0: dt.date, post: int = 5) -> dict | None:
    idx = ar.index
    pos = idx.searchsorted(pd.Timestamp(day0))
    if pos >= len(idx) or idx[pos].date() != day0 or pos + post >= len(idx) or pos < 6:
        return None
    a = ar["ar"].values
    return dict(pos=pos, ar0=float(a[pos]), z0=float(ar["z"].values[pos]), car1=float(a[pos + 1]),
                car_post=float(a[pos + 1: pos + 1 + post].sum()), pre5=float(a[pos - 5: pos].sum()))


def near_earnings(day0: dt.date, edates: set[dt.date], bdays: int = 2) -> bool:
    """Within `bdays` business days of an 8-K item 2.02 filing date (the filing can lag the release by a day)."""
    d0 = np.datetime64(day0)
    for e in edates:
        if abs((day0 - e).days) <= 7 and abs(int(np.busday_count(np.datetime64(e), d0))) <= bdays:
            return True
    return False


# ----------------------------------------------------------------------------- events

REACT_Z = 2.0
CALM_SPY = 0.02
CTRL_SPAN = 252
CTRL_GAP = 10


def compute_events(universe: pd.DataFrame, pmap: pd.DataFrame, bases: tuple[str, ...], label: str,
                   post: int = 5) -> tuple[pd.DataFrame, dict[str, pd.DataFrame], pd.DataFrame]:
    """Events for every (ruling, side) whose basis is in `bases`: day-0 stats, screens, and control days.

    Returns (events, ars, prices). Each event carries its control-day dates as a JSON list.
    """
    sel = pmap[pmap["basis"].isin(bases)].copy()
    tickers = sorted(set(sel["ticker"].dropna().astype(str)))
    px = bulk_prices(tickers + ["SPY"], label)
    if "SPY" not in px.columns:
        raise RuntimeError("SPY prices unavailable")
    ars = rolling_ar(px[[c for c in px.columns if c != "SPY"]], px["SPY"])
    spy_ret = np.log(px["SPY"]).diff()
    edates: dict[str, set[dt.date]] = {}
    # ruling dates per ticker, from every side mapped to that ticker (any basis), for the control exclusion
    all_dates: dict[str, set[dt.date]] = {}
    for _, r in pmap.dropna(subset=["ticker"]).iterrows():
        d = universe.loc[int(r["ruling"]), "date"]
        all_dates.setdefault(str(r["ticker"]), set()).add(d if isinstance(d, dt.date) else pd.Timestamp(d).date())
    rows = []
    for _, r in sel.iterrows():
        t, cik = str(r["ticker"]), str(r["cik"])
        u = universe.loc[int(r["ruling"])]
        day0 = u["date"] if isinstance(u["date"], dt.date) else pd.Timestamp(u["date"]).date()
        if t not in ars:
            rows.append(dict(ruling=int(r["ruling"]), court=u["court"], date=day0, ticker=t, cik=cik, side=r["side"], name=r["name"],
                             basis=r["basis"], status="no price history"))
            continue
        ar = ars[t]
        w = window_stats(ar, day0, post)
        if w is None:
            rows.append(dict(ruling=int(r["ruling"]), court=u["court"], date=day0, ticker=t, cik=cik, side=r["side"], name=r["name"],
                             basis=r["basis"], status="day 0 not a trading day or window incomplete"))
            continue
        if cik not in edates:
            try:
                edates[cik] = earnings_dates(cik)
            except Exception as exc:  # noqa: BLE001
                log(f"earnings dates failed for {cik}: {str(exc)[:80]}")
                edates[cik] = set()
        earn_adj = near_earnings(day0, edates[cik])
        sret = float(spy_ret.get(pd.Timestamp(day0), np.nan))
        calm = np.isfinite(sret) and abs(sret) <= CALM_SPY
        reacting = abs(w["z0"]) >= REACT_Z and not earn_adj and calm
        other = pmap[(pmap["ruling"].astype(int) == int(r["ruling"])) & (pmap["side"] != r["side"])]
        opp = str(other["basis"].iloc[0]) if len(other) else "not a company"
        # control days
        pos = w["pos"]
        idx = ar.index
        lo, hi = max(0, pos - CTRL_SPAN), min(len(idx) - post - 1, pos + CTRL_SPAN)
        rpos = {idx.searchsorted(pd.Timestamp(d)) for d in all_dates.get(t, set())}
        ctrl = []
        zvals = ar["z"].values
        avals = ar["ar"].values
        for q in range(lo, hi):
            if abs(zvals[q]) < REACT_Z or any(abs(q - rp) <= CTRL_GAP for rp in rpos):
                continue
            dq = idx[q].date()
            if near_earnings(dq, edates[cik]):
                continue
            sq = float(spy_ret.get(idx[q], np.nan))
            if not (np.isfinite(sq) and abs(sq) <= CALM_SPY):
                continue
            ctrl.append((dq.isoformat(), float(np.sign(avals[q]) * avals[q + 1: q + 1 + post].sum())))
        rows.append(dict(ruling=int(r["ruling"]), court=u["court"], date=day0, ticker=t, cik=cik, side=r["side"], name=r["name"],
                         basis=r["basis"], status="ok", ar0=w["ar0"], z0=w["z0"], car1=w["car1"], car_post=w["car_post"], pre5=w["pre5"],
                         spy_ret0=sret, earn_adj=earn_adj, calm=calm, reacting=reacting, opposing_basis=opp,
                         signed_post=float(np.sign(w["ar0"]) * w["car_post"]),
                         n_control=len(ctrl), control_mean=float(np.mean([c[1] for c in ctrl])) if ctrl else float("nan"),
                         control_days=json.dumps([c[0] for c in ctrl]), party_winning=u.get("party_winning"),
                         sigma=float(ar["sigma"].values[pos])))
    ev = pd.DataFrame(rows)
    return ev, ars, px


def bootstrap_mean_p(values: np.ndarray, draws: int = 10_000, seed: int = 20261030) -> float:
    rng = np.random.default_rng(seed)
    v = np.asarray(values, dtype=float)
    v = v[np.isfinite(v)]
    if len(v) == 0:
        return float("nan")
    means = rng.choice(v, size=(draws, len(v)), replace=True).mean(axis=1)
    return float(np.mean(means <= 0))
