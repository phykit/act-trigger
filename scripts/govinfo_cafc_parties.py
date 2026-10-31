"""Parties (name and role, in GovInfo's order) for every Federal Circuit docket on GovInfo with a precedential entry.

Reads data/appeals/govinfo_cafc_index.csv; writes data/appeals/govinfo_cafc_parties.csv. Metadata only; resumable.
Usage: python scripts/govinfo_cafc_parties.py   (needs GOVINFO_API_KEY)
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
IDX = ROOT / "data" / "appeals" / "govinfo_cafc_index.csv"
OUT = ROOT / "data" / "appeals" / "govinfo_cafc_parties.csv"
KEY = os.environ.get("GOVINFO_API_KEY", "")
H = {"X-Api-Key": KEY, "User-Agent": "act-trigger research (https://github.com/phykit/act-trigger)"}
COLS = ["package_id", "order", "role", "full_name", "first_name", "last_name", "origin"]


def log(m: str) -> None:
    print(m, file=sys.stderr, flush=True)


def summary(pid: str) -> dict | None:
    for a in range(6):
        try:
            r = requests.get(f"https://api.govinfo.gov/packages/{pid}/summary", headers=H, timeout=120)
        except requests.RequestException:
            time.sleep(10 * (a + 1))
            continue
        if r.status_code == 200:
            return r.json()
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(min(int(r.headers.get("Retry-After", 0) or 0) or 20 * (a + 1), 300))
            continue
        log(f"HTTP {r.status_code} for {pid}")
        return None
    return None


def main() -> None:
    if not KEY:
        raise SystemExit("GOVINFO_API_KEY not set")
    idx = pd.read_csv(IDX, dtype=str).fillna("")
    pids = sorted(idx.loc[idx["precedential"] == "precedential", "package_id"].unique())
    rows = pd.read_csv(OUT, dtype=str).fillna("").to_dict("records") if OUT.exists() else []
    done = {r["package_id"] for r in rows}
    todo = [p for p in pids if p not in done]
    log(f"{len(pids)} dockets with a precedential entry; {len(done)} done; {len(todo)} to fetch")
    for k, pid in enumerate(todo):
        s = summary(pid) or {}
        parties = s.get("parties") or []
        origin = str(s.get("originatingCourt") or s.get("courtType") or "")
        if not parties:
            rows.append(dict(package_id=pid, order="", role="", full_name="(no parties)", first_name="", last_name="", origin=origin))
        for i, p in enumerate(parties):
            if not isinstance(p, dict):
                p = {"fullName": str(p), "role": "(unstructured)"}
            rows.append(dict(package_id=pid, order=i, role=p.get("role", ""), full_name=p.get("fullName", ""),
                             first_name=p.get("firstName", ""), last_name=p.get("lastName", ""), origin=origin))
        if k % 250 == 249:
            pd.DataFrame(rows, columns=COLS).to_csv(OUT, index=False)
            log(f"{k + 1} of {len(todo)}")
    df = pd.DataFrame(rows, columns=COLS)
    df.to_csv(OUT, index=False)
    log(f"done: {df['package_id'].nunique()} dockets, {len(df)} party rows; roles: {df['role'].value_counts().head(20).to_dict()}")


if __name__ == "__main__":
    main()
