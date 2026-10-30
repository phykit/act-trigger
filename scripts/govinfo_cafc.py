"""Index of Federal Circuit opinions on GovInfo (United States Courts Opinions, court code ca13), metadata only.

One row per granule (an opinion or order in a docket's package): package and granule IDs, case number, title,
date issued, the docket-text entry, and the precedential marker read from it. No prices, no opinion text.
Resumable: data/appeals/govinfo_cafc_index.csv is reread and packages already indexed are skipped.

Usage: python scripts/govinfo_cafc.py   (needs GOVINFO_API_KEY; GOVINFO_MINUTES caps the run, default 240)
"""
from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "appeals" / "govinfo_cafc_index.csv"
KEY = os.environ.get("GOVINFO_API_KEY", "")
API = "https://api.govinfo.gov"
H = {"X-Api-Key": KEY, "User-Agent": "act-trigger research (https://github.com/phykit/act-trigger)"}
QUERY = "collection:USCOURTS courtcode:ca13"
COLS = ["package_id", "granule_id", "case_number", "title", "date_issued", "precedential", "docket_text"]


def log(m: str) -> None:
    print(m, file=sys.stderr, flush=True)


def call(method: str, url: str, **kw) -> dict | None:
    for a in range(6):
        try:
            r = requests.request(method, url if url.startswith("http") else API + url, headers=H, timeout=120, **kw)
        except requests.RequestException:
            time.sleep(10 * (a + 1))
            continue
        if r.status_code == 200:
            try:
                return r.json()
            except ValueError:
                return None
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(min(int(r.headers.get("Retry-After", 0) or 0) or 20 * (a + 1), 300))
            continue
        log(f"HTTP {r.status_code} for {url[:120]}")
        return None
    return None


def marker(text: str) -> str:
    """'nonprecedential', 'precedential', or '' from the docket-text entry (for example 'Nonprecedential Opinion.')."""
    t = text or ""
    if re.search(r"(?i)\bnon-?precedential\b", t):
        return "nonprecedential"
    if re.search(r"(?i)\bprecedential\b", t):
        return "precedential"
    return ""


def package_ids() -> list[str]:
    ids, mark = [], "*"
    while True:
        j = call("POST", "/search", json={"query": QUERY, "pageSize": 1000, "offsetMark": mark,
                                          "sorts": [{"field": "publishdate", "sortOrder": "ASC"}]})
        if not j:
            break
        res = j.get("results", [])
        ids += [x["packageId"] for x in res if str(x.get("packageId", "")).startswith("USCOURTS-ca13-")]
        nxt = j.get("offsetMark")
        if not res or not nxt or nxt == mark:
            break
        mark = nxt
    log(f"search: {len(ids)} ca13 packages (count reported {j.get('count') if j else 'n/a'})")
    return sorted(set(ids))


def main() -> None:
    if not KEY:
        raise SystemExit("GOVINFO_API_KEY not set")
    budget = time.time() + 60 * float(os.environ.get("GOVINFO_MINUTES", "240"))
    rows = pd.read_csv(OUT, dtype=str).fillna("").to_dict("records") if OUT.exists() else []
    done = {r["package_id"] for r in rows}
    ids = package_ids()
    todo = [p for p in ids if p not in done]
    log(f"{len(done)} packages already indexed; {len(todo)} to go")
    for k, pid in enumerate(todo):
        if time.time() > budget:
            log(f"time budget reached at package {k} of {len(todo)}; the next run resumes")
            break
        g = call("GET", f"/packages/{pid}/granules", params={"pageSize": 100, "offsetMark": "*"})
        grs = (g or {}).get("granules", [])
        if not grs:
            rows.append(dict(package_id=pid, granule_id="", case_number=pid.split("ca13-")[-1], title="",
                             date_issued="", precedential="", docket_text="(no granules)"))
        for gr in grs:
            s = call("GET", f"/packages/{pid}/granules/{gr['granuleId']}/summary") or {}
            dtext = re.sub(r"\s+", " ", s.get("docketText", "") or "")
            rows.append(dict(package_id=pid, granule_id=gr["granuleId"], case_number=pid.split("ca13-")[-1],
                             title=s.get("title", gr.get("title", "")), date_issued=s.get("dateIssued", gr.get("dateIssued", "")),
                             precedential=marker(dtext), docket_text=dtext[:300]))
        if k % 200 == 199:
            pd.DataFrame(rows, columns=COLS).to_csv(OUT, index=False)
            log(f"{k + 1} of {len(todo)} packages; {len(rows)} granules indexed")
    df = pd.DataFrame(rows, columns=COLS)
    df.to_csv(OUT, index=False)
    d = df[df["date_issued"] != ""].copy()
    d["year"] = d["date_issued"].str[:4]
    tab = d.pivot_table(index="year", columns="precedential", values="granule_id", aggfunc="count", fill_value=0)
    log("granules by year and marker:\n" + tab.to_string())
    (OUT.parent / "govinfo_cafc_coverage.md").write_text(
        "# GovInfo Federal Circuit coverage (granules by year of issue and docket-text marker)\n\n"
        f"Packages in the search: {len(ids)}; indexed: {df['package_id'].nunique()}.\n\n" + tab.to_markdown() + "\n")


if __name__ == "__main__":
    main()
