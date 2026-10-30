"""Shared data and market-model code for Projects Apple and Orange (court-ruling tests).

Everything that touches the network lives here, and every fetched object is written to
data/rulings/ so that a later run reproduces the same inputs without refetching.

Set RULINGS_SELFTEST=1 to replace every network call with deterministic synthetic data;
the self-test exercises the code paths and writes nothing under results/ or data/.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "data" / "ruling_cases.csv"
RDATA = ROOT / "data" / "rulings"
RESULTS = ROOT / "results"
SELFTEST = os.environ.get("RULINGS_SELFTEST") == "1"
UA = {"User-Agent": "act-trigger research scripts (https://github.com/phykit/act-trigger)"}

EST_DAYS = 250      # market-model estimation window, trading days
EST_GAP = 10        # trading days between the end of the estimation window and the argument


def spec_hash(name: str) -> str:
    p = ROOT / "prereg" / f"{name}_prereg.md"
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_cases() -> pd.DataFrame:
    df = pd.read_csv(CASES, parse_dates=["argued", "decided"])
    df["term"] = df["term"].astype(int)
    return df


def _rdata_path(name: str) -> Path:
    base = Path(os.environ.get("RULINGS_SCRATCH", RDATA)) if SELFTEST else RDATA
    base.mkdir(parents=True, exist_ok=True)
    return base / name


# ----------------------------------------------------------------------------- prices

def _yf_close(ticker: str, start: str, end: str) -> pd.Series:
    import yfinance as yf

    df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False, threads=False)
    if df is None or len(df) == 0:
        raise RuntimeError("yfinance returned no rows")
    if isinstance(df.columns, pd.MultiIndex):
        close = df["Close"]
        close = close[ticker] if ticker in close.columns else close.iloc[:, 0]
    else:
        close = df["Close"]
    close = pd.to_numeric(close, errors="coerce").dropna()
    close.index = pd.to_datetime(close.index).tz_localize(None).normalize()
    return close.rename(ticker)


def _stooq_close(ticker: str, start: str, end: str) -> pd.Series:
    url = (f"https://stooq.com/q/d/l/?s={ticker.lower()}.us&i=d"
           f"&d1={start.replace('-', '')}&d2={end.replace('-', '')}")
    r = requests.get(url, headers=UA, timeout=60)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    if "Close" not in df.columns or "Date" not in df.columns or len(df) == 0:
        raise RuntimeError(f"stooq returned no usable rows: {r.text[:80]!r}")
    s = pd.Series(pd.to_numeric(df["Close"], errors="coerce").values,
                  index=pd.to_datetime(df["Date"])).dropna()
    return s.rename(ticker)


def _synthetic_close(ticker: str, start: str, end: str) -> pd.Series:
    seed = int(hashlib.sha256(ticker.encode()).hexdigest()[:8], 16)
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range(start, end)
    vol = 0.010 if ticker == "SPY" else 0.022
    ret = rng.normal(0.0003, vol, len(idx))
    return pd.Series(100 * np.exp(np.cumsum(ret)), index=idx, name=ticker)


def fetch_close(ticker: str, start: dt.date, end: dt.date) -> tuple[pd.Series, str]:
    """Adjusted daily close; returns (series, source). Cached under data/rulings/."""
    s_, e_ = start.isoformat(), end.isoformat()
    cache = _rdata_path(f"prices_{ticker}_{s_}_{e_}.csv")
    if cache.exists() and not SELFTEST:
        first = cache.read_text().splitlines()[0]
        src = first[1:] if first.startswith("#") else "unknown"
        s = pd.read_csv(cache, index_col=0, parse_dates=True, comment="#").iloc[:, 0]
        return s.rename(ticker), f"cache ({src})"
    if SELFTEST:
        return _synthetic_close(ticker, s_, e_), "synthetic"
    errors = []
    for name, fn in (("yfinance", _yf_close), ("stooq", _stooq_close)):
        try:
            s = fn(ticker, s_, e_)
            if len(s) < 100:
                raise RuntimeError(f"only {len(s)} rows")
            with open(cache, "w") as fh:
                fh.write(f"#source={name} fetched={dt.date.today().isoformat()}\n")
                s.to_csv(fh, header=["close"], index_label="date")
            return s, name
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{name}: {exc}")
    raise RuntimeError(f"no price source worked for {ticker}: " + " | ".join(errors))


# ----------------------------------------------------------------------------- dates

def oyez_dates(term: int, docket: str) -> dict | None:
    """Argued and decided dates from the Oyez API timeline, or None if unreachable."""
    if SELFTEST:
        return None
    cache = _rdata_path(f"oyez_{2000 + term}_{docket}.json")
    try:
        if cache.exists():
            j = json.loads(cache.read_text())
        else:
            r = requests.get(f"https://api.oyez.org/cases/{2000 + term}/{docket}", headers=UA, timeout=60)
            r.raise_for_status()
            j = r.json()
            cache.write_text(json.dumps(j)[:200000])
        out = {}
        for item in j.get("timeline") or []:
            ev = str(item.get("event", "")).lower()
            dates = item.get("dates") or []
            if not dates:
                continue
            d = dt.datetime.fromtimestamp(int(dates[-1]), tz=dt.timezone.utc).date()
            if ev.startswith("argued"):
                out["argued"] = d
            elif ev.startswith("decided"):
                out["decided"] = d
        return out or None
    except Exception:  # noqa: BLE001
        return None


def opinion_days(term: int) -> tuple[list[dt.date], pd.DataFrame]:
    """All slip-opinion release dates for October Term `term` (two-digit), plus the listing."""
    cache = _rdata_path(f"opinion_days_OT{term:02d}.csv")
    if cache.exists():
        df = pd.read_csv(cache, parse_dates=["date"])
    elif SELFTEST:
        start = dt.date(2000 + term, 10, 1)
        days = pd.bdate_range(start, start + dt.timedelta(days=270))[::7]
        df = pd.DataFrame({"date": days, "docket": [f"{term}-{i}" for i in range(len(days))],
                           "name": ["synthetic"] * len(days)})
        reg = load_cases()
        reg = reg[reg["term"] == term]
        df = pd.concat([df, pd.DataFrame({"date": reg["decided"], "docket": reg["docket"],
                                          "name": reg["case_name"]})], ignore_index=True)
    else:
        url = f"https://www.supremecourt.gov/opinions/slipopinion/{term:02d}"
        r = requests.get(url, headers=UA, timeout=60)
        r.raise_for_status()
        tables = pd.read_html(io.StringIO(r.text))
        rows = []
        for t in tables:
            cols = {str(c).strip().lower(): c for c in t.columns}
            if "date" in cols and "docket" in cols:
                sub = t[[cols["date"], cols["docket"], cols.get("name", cols["docket"])]].copy()
                sub.columns = ["date", "docket", "name"]
                rows.append(sub)
        if not rows:
            raise RuntimeError(f"no slip-opinion table with Date and Docket columns at {url}")
        df = pd.concat(rows, ignore_index=True)
        df["date"] = pd.to_datetime(df["date"].astype(str).str.strip(), format="mixed", errors="coerce")
        df = df.dropna(subset=["date"])
        df["docket"] = df["docket"].astype(str).str.strip()
        if len(df) < 20:
            raise RuntimeError(f"only {len(df)} opinions parsed for OT{term:02d}; refusing to proceed")
        df.sort_values("date").to_csv(cache, index=False)
    days = sorted({d.date() for d in pd.to_datetime(df["date"])})
    return days, df


def check_dates(case: pd.Series, slip: pd.DataFrame) -> dict:
    """Apply the registered date checks. Returns status fields and the dates to use."""
    argued = case["argued"].date()
    decided = case["decided"].date()
    oy = oyez_dates(int(case["term"]), case["docket"])
    slip_dates = set()
    if slip is not None and len(slip):
        m = slip[slip["docket"].astype(str).str.contains(case["docket"], regex=False)]
        slip_dates = {d.date() for d in pd.to_datetime(m["date"])}
    decided_ok = (decided in slip_dates) or (oy is not None and oy.get("decided") == decided)
    if oy is None:
        argued_status = "recollection (Oyez unreachable)"
    elif oy.get("argued") == argued:
        argued_status = "verified (Oyez)"
    else:
        argued_status = f"MISMATCH (Oyez {oy.get('argued')})"
    if decided in slip_dates and oy is not None and oy.get("decided") == decided:
        decided_status = "verified (Oyez and slip listing)"
    elif decided in slip_dates:
        decided_status = "verified (slip listing)"
    elif oy is not None and oy.get("decided") == decided:
        decided_status = "verified (Oyez)"
    else:
        decided_status = f"FAILED (Oyez {None if oy is None else oy.get('decided')}; slip {sorted(slip_dates)})"
    return dict(argued=argued, decided=decided, argued_status=argued_status,
                decided_status=decided_status, include=bool(decided_ok))


# ----------------------------------------------------------------------------- market model

def market_model(stock: pd.Series, mkt: pd.Series, argued: dt.date) -> tuple[pd.DataFrame, dict]:
    """Residual abnormal returns from an OLS market model estimated before the argument."""
    px = pd.concat([stock.rename("s"), mkt.rename("m")], axis=1).dropna()
    r = np.log(px).diff().dropna()
    pre = r[r.index < pd.Timestamp(argued)]
    if len(pre) < EST_DAYS + EST_GAP:
        raise RuntimeError(f"only {len(pre)} pre-argument returns; need {EST_DAYS + EST_GAP}")
    est = pre.iloc[-(EST_DAYS + EST_GAP):-EST_GAP]
    x = np.column_stack([np.ones(len(est)), est["m"].values])
    beta = np.linalg.lstsq(x, est["s"].values, rcond=None)[0]
    resid = est["s"].values - x @ beta
    sigma = float(np.std(resid, ddof=2))
    out = r.copy()
    out["ar"] = out["s"] - (beta[0] + beta[1] * out["m"])
    out["z"] = out["ar"] / sigma
    return out, dict(alpha=float(beta[0]), beta=float(beta[1]), sigma=sigma, n_est=int(len(est)),
                     est_start=est.index[0].date(), est_end=est.index[-1].date())


# ----------------------------------------------------------------------------- results

def result_path(name: str) -> Path:
    base = Path(os.environ.get("RULINGS_SCRATCH", RESULTS)) if SELFTEST else RESULTS
    base.mkdir(parents=True, exist_ok=True)
    stem = f"{name}_result_{dt.date.today().isoformat()}"
    p = base / f"{stem}.md"
    k = 2
    while p.exists():  # results are appended as new files, never overwritten
        p = base / f"{stem}_{k}.md"
        k += 1
    return p


def fmt_pct(x: float) -> str:
    return "n/a" if x is None or not np.isfinite(x) else f"{100 * x:+.2f}%"


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)
