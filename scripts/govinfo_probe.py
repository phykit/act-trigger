"""Diagnostic only: what GovInfo and supremecourt.gov can supply, before any spec names them as a source.

Writes data/appeals/govinfo_probe.md. The API key is sent as a header, never as a URL parameter, and is scrubbed
from everything written. Reads nothing under results/.
"""
from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "appeals" / "govinfo_probe.md"
KEY = os.environ.get("GOVINFO_API_KEY", "")
API = "https://api.govinfo.gov"
H = {"X-Api-Key": KEY, "User-Agent": "act-trigger research (https://github.com/phykit/act-trigger)"}
L: list[str] = []


def scrub(s: str) -> str:
    return s.replace(KEY, "[KEY]") if KEY else s


def get(path: str, **params) -> tuple[int, dict | str]:
    url = path if path.startswith("http") else API + path
    for _ in range(4):
        r = requests.get(url, headers=H, params=params, timeout=90)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", 30) or 30))
            continue
        try:
            return r.status_code, r.json()
        except ValueError:
            return r.status_code, r.text
    return r.status_code, r.text


def block(title: str, obj, n: int = 3000) -> None:
    txt = obj if isinstance(obj, str) else json.dumps(obj, indent=1)
    L.extend([f"### {title}\n", "```", scrub(txt[:n]), "```", ""])


def main() -> None:
    L.append("# GovInfo and supremecourt.gov probe (diagnostic only)\n")
    L.append(f"- GOVINFO_API_KEY present: {'yes' if KEY else 'no'} (length {len(KEY)}).\n")

    # 1. Federal Circuit packages issued in one quarter
    st, j = get("/published/2024-01-01/2024-03-31", collection="USCOURTS", courtCode="cafc", pageSize=100, offsetMark="*")
    L.append(f"## 1. /published USCOURTS cafc 2024 Q1: HTTP {st}\n")
    if isinstance(j, dict):
        L.append(f"- count {j.get('count')}; first page {len(j.get('packages', []))} packages.\n")
        block("first two packages", j.get("packages", [])[:2])
    else:
        block("response", j, 1500)
    pkgs = j.get("packages", []) if isinstance(j, dict) else []
    if not pkgs:
        st2, j2 = get("/collections/USCOURTS/2024-01-01T00:00:00Z/2024-03-31T23:59:59Z", courtCode="cafc", pageSize=100, offsetMark="*")
        L.append(f"## 1b. /collections fallback: HTTP {st2}\n")
        block("response", j2, 2500)
        pkgs = j2.get("packages", []) if isinstance(j2, dict) else []

    # 2. Package, granules, granule summary and MODS for the first three packages
    for p in pkgs[:3]:
        pid = p.get("packageId")
        L.append(f"## 2. Package {pid}\n")
        st, s = get(f"/packages/{pid}/summary")
        block(f"summary (HTTP {st})", s, 2500)
        st, g = get(f"/packages/{pid}/granules", pageSize=100, offsetMark="*")
        block(f"granules (HTTP {st})", g, 1500)
        gr = g.get("granules", []) if isinstance(g, dict) else []
        if gr:
            gid = gr[0].get("granuleId")
            st, gs = get(f"/packages/{pid}/granules/{gid}/summary")
            block(f"granule summary {gid} (HTTP {st})", gs, 3000)
            links = gs.get("download", {}) if isinstance(gs, dict) else {}
            for k, u in links.items():
                try:
                    r = requests.get(u, headers=H, timeout=90)
                    L.append(f"- download {k}: HTTP {r.status_code}, {len(r.content)} bytes, type {r.headers.get('Content-Type')}")
                    if k.lower().startswith("mods") and r.ok:
                        mods = r.text
                        block(f"granule MODS {gid} (first 6000 chars)", mods, 6000)
                        hits = sorted(set(re.findall(r"(?i)\b(non-?precedential|precedential|unpublished|published)\b", mods)))
                        L.append("- MODS mentions precedential: " + (", ".join(hits) or "none"))
                except requests.RequestException as e:
                    L.append(f"- download {k}: error {type(e).__name__}")
            L.append("")
        time.sleep(1)

    # 3. Federal Circuit coverage by year (package counts by issue date)
    L.append("## 3. USCOURTS cafc package counts by calendar year (dateIssued)\n")
    L.append("| Year | HTTP | count |\n|---|---|---|")
    for y in range(2012, 2026):
        st, j = get(f"/published/{y}-01-01/{y}-12-31", collection="USCOURTS", courtCode="cafc", pageSize=10, offsetMark="*")
        L.append(f"| {y} | {st} | {j.get('count') if isinstance(j, dict) else 'n/a'} |")
        time.sleep(0.5)
    L.append("")

    # 4. Supreme Court: GovInfo collections that might hold opinions
    st, c = get("/collections")
    names = [x.get("collectionCode") for x in c.get("collections", [])] if isinstance(c, dict) else []
    L.append(f"## 4. GovInfo collections (HTTP {st}): {', '.join(n for n in names if n)}\n")
    if "USREPORTS" in names:
        st, u = get("/published/2005-01-01/2025-12-31", collection="USREPORTS", pageSize=100, offsetMark="*")
        L.append(f"- USREPORTS published 2005 to 2025: HTTP {st}, count {u.get('count') if isinstance(u, dict) else 'n/a'}")
        if isinstance(u, dict):
            block("USREPORTS sample", u.get("packages", [])[:3], 1500)

    # 5. supremecourt.gov reachability from the runner (slip-opinion index pages and one opinion PDF)
    L.append("## 5. supremecourt.gov from the runner\n")
    ua = {"User-Agent": "Mozilla/5.0 (act-trigger research; https://github.com/phykit/act-trigger)"}
    for t in ("05", "10", "15", "20", "23", "24"):
        try:
            r = requests.get(f"https://www.supremecourt.gov/opinions/slipopinion/{t}", headers=ua, timeout=60)
            pdfs = re.findall(r'href="(/opinions/\d{2}pdf/[^"]+\.pdf)"', r.text)
            L.append(f"- slipopinion/{t}: HTTP {r.status_code}, {len(r.content)} bytes, {len(pdfs)} opinion PDF links; first {pdfs[:1]}")
            if pdfs and t == "05":
                p = requests.get("https://www.supremecourt.gov" + pdfs[0], headers=ua, timeout=60)
                L.append(f"  - {pdfs[0]}: HTTP {p.status_code}, {len(p.content)} bytes, type {p.headers.get('Content-Type')}")
        except requests.RequestException as e:
            L.append(f"- slipopinion/{t}: error {type(e).__name__}")
        time.sleep(1)
    for path in ("/opinions/boundvolumes.aspx", "/opinions/USReports.aspx"):
        try:
            r = requests.get("https://www.supremecourt.gov" + path, headers=ua, timeout=60)
            npdf = len(re.findall(r"\.pdf", r.text))
            L.append(f"- {path}: HTTP {r.status_code}, {len(r.content)} bytes, {npdf} pdf links")
        except requests.RequestException as e:
            L.append(f"- {path}: error {type(e).__name__}")
    L.append("")
    OUT.write_text(scrub("\n".join(L)) + "\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
