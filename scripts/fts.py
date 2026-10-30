"""EDGAR full-text search helper for Wood and Storm. No key: the SEC asks only for a User-Agent with a contact
(the SEC_CONTACT secret), and at most ten requests a second (appeals_common.sec_get keeps under eight).
Responses are cached by query under data/appeals/fts/ so reruns do not repeat requests.
"""
from __future__ import annotations

import datetime as dt
import gzip
import hashlib
import json
import re

import requests

from appeals_common import SELFTEST, adata, log, normalise, sec_get

GOV = re.compile(r"^(UNITED STATES|USA|U S|AMERICA|STATE|COMMONWEALTH|PEOPLE|CITY|COUNTY|TOWN|VILLAGE|DISTRICT OF COLUMBIA|"
                 r"SECRETARY|COMMISSIONER|DIRECTOR|ATTORNEY GENERAL|ADMINISTRATOR|DEPARTMENT|FEDERAL|NATIONAL LABOR|"
                 r"ENVIRONMENTAL PROTECTION|SECURITIES AND EXCHANGE|INTERNAL REVENUE|PATENT AND TRADEMARK|UNDER SECRETARY|"
                 r"INTERNATIONAL TRADE COMMISSION|MERIT SYSTEMS|DEPT|BOARD|OFFICE OF)\b")
STATES = {"ALABAMA", "ALASKA", "ARIZONA", "ARKANSAS", "CALIFORNIA", "COLORADO", "CONNECTICUT", "DELAWARE", "FLORIDA", "GEORGIA",
          "HAWAII", "IDAHO", "ILLINOIS", "INDIANA", "IOWA", "KANSAS", "KENTUCKY", "LOUISIANA", "MAINE", "MARYLAND", "MASSACHUSETTS",
          "MICHIGAN", "MINNESOTA", "MISSISSIPPI", "MISSOURI", "MONTANA", "NEBRASKA", "NEVADA", "NEW HAMPSHIRE", "NEW JERSEY",
          "NEW MEXICO", "NEW YORK", "NORTH CAROLINA", "NORTH DAKOTA", "OHIO", "OKLAHOMA", "OREGON", "PENNSYLVANIA", "RHODE ISLAND",
          "SOUTH CAROLINA", "SOUTH DAKOTA", "TENNESSEE", "TEXAS", "UTAH", "VERMONT", "VIRGINIA", "WASHINGTON", "WEST VIRGINIA",
          "WISCONSIN", "WYOMING"}


def is_government(name: str) -> bool:
    n = normalise(name)
    return not n or bool(GOV.match(n)) or n in STATES or n in {"FCC", "FTC", "EPA", "NLRB", "SEC", "IRS", "FDA", "PTO", "USPTO", "ITC"}


def term(name: str, words: int) -> str:
    """Normalised name (Earth item 3) cut to its first `words` words, in title case for the query."""
    return " ".join(normalise(name).split()[:words]).title()


def _cache_path(url: str):
    d = adata("fts")
    d.mkdir(parents=True, exist_ok=True)
    return d / (hashlib.sha256(url.encode()).hexdigest()[:24] + ".json.gz")


def search(q: str, forms: str, start: dt.date, end: dt.date, cik: str | None = None, max_pages: int = 20) -> list[dict]:
    """All hits (the _source dicts) for query `q`, paging 100 at a time. Raises on persistent failure."""
    if SELFTEST:
        h = int(hashlib.sha256((q + str(cik)).encode()).hexdigest()[:6], 16)
        n = h % 7
        return [dict(ciks=[f"{1000 + (h + k) % 120:010d}"], adsh=f"0000000000-00-{k:06d}", form="10-K", file_date=start.isoformat())
                for k in range(n)]
    hits, frm = [], 0
    while True:
        url = ("https://efts.sec.gov/LATEST/search-index?q=" + requests.utils.quote(q) + f"&forms={forms}"
               f"&dateRange=custom&startdt={start.isoformat()}&enddt={end.isoformat()}&from={frm}")
        if cik:
            url += f"&ciks={int(cik):010d}"
        f = _cache_path(url)
        if f.exists():
            j = json.loads(gzip.decompress(f.read_bytes()))
        else:
            j = sec_get(url).json()
            f.write_bytes(gzip.compress(json.dumps(j).encode()))
        page = [x["_source"] for x in j.get("hits", {}).get("hits", [])]
        hits.extend(page)
        total = j.get("hits", {}).get("total", {}).get("value", 0)
        frm += 100
        if not page or frm >= total or frm >= 100 * max_pages:
            if frm < total:
                log(f"full-text search capped at {len(hits)} of {total} hits for {q!r}")
            return hits
