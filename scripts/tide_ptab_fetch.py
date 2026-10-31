"""Tide: fetch PTAB trial decisions and proceedings from the USPTO Open Data Portal (prereg/tide_prereg.md).

Usage:
  TIDE_PROBE=1 python scripts/tide_ptab_fetch.py   # one page of each endpoint: field structure only -> data/tide/odp_probe.md
  python scripts/tide_ptab_fetch.py                # every page, OCR text dropped -> data/tide/odp_*.json.gz

The key is read from USPTO_ODP_API_KEY and sent only as the X-API-KEY header to api.uspto.gov; it is never printed.
No prices are read here.
"""
from __future__ import annotations

import collections
import gzip
import json
import os
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "tide"
BASE = "https://api.uspto.gov/api/v1/patent/trials"
PAGE = 100
SLEEP = 0.4
DROP_KEYS = ("ocr", "documenttext", "fulltext")


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def session() -> requests.Session:
    key = os.environ.get("USPTO_ODP_API_KEY", "").strip()
    if not key:
        raise SystemExit("USPTO_ODP_API_KEY is not set (add it as an Actions secret)")
    s = requests.Session()
    s.headers.update({"X-API-KEY": key, "Accept": "application/json",
                      "User-Agent": "act-trigger research scripts (https://github.com/phykit/act-trigger)"})
    return s


def get(s: requests.Session, endpoint: str, offset: int, limit: int) -> dict:
    url = f"{BASE}/{endpoint}/search"
    for attempt in range(6):
        r = s.get(url, params={"offset": offset, "limit": limit}, timeout=120)
        if r.status_code == 200:
            return r.json()
        if r.status_code in (429, 500, 502, 503, 504):
            wait = int(r.headers.get("Retry-After", "0") or 0) or 10 * (attempt + 1)
            log(f"{endpoint} offset {offset}: HTTP {r.status_code}, waiting {wait}s")
            time.sleep(wait)
            continue
        raise SystemExit(f"{endpoint} offset {offset}: HTTP {r.status_code} {r.text[:200]}")
    raise SystemExit(f"{endpoint} offset {offset}: gave up after retries")


def records(payload: dict) -> list[dict]:
    """The list of records in a search response, whatever its key is called."""
    for k, v in payload.items():
        if isinstance(v, list) and v and isinstance(v[0], dict):
            return v
    return []


def strip(obj):
    """Drop OCR and full-text fields, recursively."""
    if isinstance(obj, dict):
        return {k: strip(v) for k, v in obj.items() if not any(d in k.lower() for d in DROP_KEYS)}
    if isinstance(obj, list):
        return [strip(v) for v in obj]
    return obj


def paths(obj, prefix: str = "", out=None):
    out = out if out is not None else collections.defaultdict(list)
    if isinstance(obj, dict):
        for k, v in obj.items():
            paths(v, f"{prefix}.{k}" if prefix else k, out)
    elif isinstance(obj, list):
        for v in obj:
            paths(v, f"{prefix}[]", out)
    else:
        out[prefix].append(obj)
    return out


def probe() -> None:
    s = session()
    OUT.mkdir(parents=True, exist_ok=True)
    lines = ["# ODP PTAB probe (field structure only; no prices)\n"]
    for ep in ("decisions", "proceedings"):
        payload = get(s, ep, 0, 25)
        recs = [strip(r) for r in records(payload)]
        top = {k: (v if not isinstance(v, (list, dict)) else type(v).__name__) for k, v in payload.items()}
        lines.append(f"\n## {ep}\n\nTop-level keys: {json.dumps(top)[:400]}\n\nRecords on page: {len(recs)}\n")
        lines.append("| path | type | distinct on page | examples |\n|---|---|---|---|\n")
        for p, vals in sorted(paths(recs).items()):
            ex = [str(v)[:60].replace("|", "/") for v in list(dict.fromkeys(vals))[:3]]
            lines.append(f"| {p} | {type(vals[0]).__name__} | {len(set(map(str, vals)))} | {'; '.join(ex)} |\n")
        time.sleep(SLEEP)
    (OUT / "odp_probe.md").write_text("".join(lines))
    log("probe written to data/tide/odp_probe.md")


def fetch_all(ep: str, s: requests.Session) -> list[dict]:
    first = get(s, ep, 0, PAGE)
    total = next((v for k, v in first.items() if isinstance(v, int) and "count" in k.lower()), None)
    out = [strip(r) for r in records(first)]
    log(f"{ep}: total reported {total}")
    offset = PAGE
    while total is None or offset < total:
        time.sleep(SLEEP)
        batch = records(get(s, ep, offset, PAGE))
        if not batch:
            break
        out.extend(strip(r) for r in batch)
        offset += PAGE
        if (offset // PAGE) % 25 == 0:
            log(f"{ep}: {len(out)} records")
    log(f"{ep}: {len(out)} records fetched")
    return out


def main() -> None:
    if os.environ.get("TIDE_PROBE") == "1":
        probe()
        return
    s = session()
    OUT.mkdir(parents=True, exist_ok=True)
    for ep in ("decisions", "proceedings"):
        recs = fetch_all(ep, s)
        with gzip.open(OUT / f"odp_{ep}.json.gz", "wt") as f:
            json.dump(recs, f)


if __name__ == "__main__":
    main()
