"""Cross-thread cost gate (prereg/cost_gate_prereg.md): Corwin and Schultz (2012) high-low spread, averaged over
the 20 trading days ending on day -1, negative two-day estimates set to zero; round trip per leg = 2 x spread.
"""
from __future__ import annotations

import datetime as dt
import hashlib

import numpy as np
import pandas as pd

from appeals_common import SELFTEST, adata, log

K = 3 - 2 * np.sqrt(2)
_cache: dict[str, pd.DataFrame] = {}


def _ohlc(ticker: str) -> pd.DataFrame:
    if ticker in _cache:
        return _cache[ticker]
    f = adata(f"ohlc_{ticker}.csv.gz")
    if f.exists():
        df = pd.read_csv(f, index_col=0, parse_dates=True)
    elif SELFTEST:
        idx = pd.bdate_range("2004-01-01", dt.date.today())
        rng = np.random.default_rng(int(hashlib.sha256(ticker.encode()).hexdigest()[:8], 16))
        c = 100 * np.exp(np.cumsum(rng.normal(0, 0.02, len(idx))))
        rngh = np.abs(rng.normal(0.012, 0.004, len(idx)))
        df = pd.DataFrame({"High": c * (1 + rngh), "Low": c * (1 - rngh)}, index=idx)
    else:
        import yfinance as yf  # noqa: PLC0415
        df = yf.download(ticker, start="2004-01-01", auto_adjust=False, progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df = df[["High", "Low"]].dropna()
        df.index = pd.to_datetime(df.index).tz_localize(None).normalize()
        df.to_csv(f, compression="gzip")
    _cache[ticker] = df
    return df


def cs_spread(ticker: str, day0: dt.date, window: int = 20) -> float:
    """Mean Corwin-Schultz spread over the `window` trading days ending on day -1; NaN if unavailable."""
    try:
        df = _ohlc(ticker)
    except Exception as exc:  # noqa: BLE001
        log(f"OHLC unavailable for {ticker}: {str(exc)[:80]}")
        return float("nan")
    pre = df[df.index < pd.Timestamp(day0)].tail(window)
    if len(pre) < window:
        return float("nan")
    h, l = np.log(pre["High"].values), np.log(pre["Low"].values)
    beta = (h[:-1] - l[:-1]) ** 2 + (h[1:] - l[1:]) ** 2
    gamma = (np.maximum(h[:-1], h[1:]) - np.minimum(l[:-1], l[1:])) ** 2
    alpha = (np.sqrt(2 * beta) - np.sqrt(beta)) / K - np.sqrt(gamma / K)
    s = 2 * (np.exp(alpha) - 1) / (1 + np.exp(alpha))
    return float(np.mean(np.maximum(s, 0)))


def round_trip(tickers_weights: list[tuple[str, float]], day0: dt.date) -> float:
    """Sum over legs of |weight| x 2 x spread. NaN if any leg's spread is unavailable."""
    total = 0.0
    for t, w in tickers_weights:
        s = cs_spread(t, day0)
        if not np.isfinite(s):
            return float("nan")
        total += abs(w) * 2 * s
    return total


def gate(gross: np.ndarray, cost: np.ndarray) -> dict:
    ok = np.isfinite(gross) & np.isfinite(cost)
    net = gross[ok] - cost[ok]
    return dict(n=int(ok.sum()), gross=float(np.mean(gross[ok])) if ok.any() else float("nan"),
                net=float(np.mean(net)) if ok.any() else float("nan"),
                median_cost=float(np.median(cost[ok])) if ok.any() else float("nan"),
                passed=bool(ok.any() and np.mean(net) > 0), missing_cost=int((~np.isfinite(cost)).sum()))
