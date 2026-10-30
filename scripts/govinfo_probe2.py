"""Diagnostic only, second pass: which courts USCOURTS holds, per-case granules in USREPORTS, and the slip-opinion
link format on supremecourt.gov. Writes data/appeals/govinfo_probe2.md; the key is a header and is scrubbed."""
from __future__ import annotations

import collections
import json
import os
import re
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "appeals" / "govinfo_probe2.md"
KEY = os.environ.get("GOVINFO_API_KEY", "")
API = "https://api.govinfo.gov"
H = {"X-Api-Key": KEY, "User-Agent": "act-trigger research (https://github.com/phykit/act-trigger)"}
UA = {"User-Agent": "Mozilla/5.0 (act-trigger research; https://github.com/phykit/act-trigger)"}
L: list[str] = []


def scrub(s: str) -> str:
    return s.replace(KEY, "[KEY]") if KEY else s


def get(url: str, **params):
    url = url if url.startswith("http") else API + url
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


def block(title, obj, n=2500):
    txt = obj if isinstance(obj, str) else json.dumps(obj, indent=1)
    L.extend([f"### {title}\n", "```", scrub(txt[:n]), "```", ""])


def main():
    L.append("# Probe 2 (diagnostic only)\n")
    # 1. Which courts are in USCOURTS: tally package-ID prefixes over one month, up to 20 pages
    tally, nxt, pages, st = collections.Counter(), None, 0, None
    st, j = get("/published/2024-03-01/2024-03-31", collection="USCOURTS", pageSize=1000, offsetMark="*")
    while isinstance(j, dict) and pages < 20:
        for p in j.get("packages", []):
            m = re.match(r"USCOURTS-([a-z0-9]+)-", p.get("packageId", ""))
            tally[m.group(1) if m else "?"] += 1
        pages += 1
        nxt = j.get("nextPage")
        if not nxt:
            break
        st, j = get(nxt)
    L.append(f"## 1. USCOURTS packages published March 2024 (first {pages} pages; HTTP {st}); total listed {sum(tally.values())}\n")
    app = {k: v for k, v in tally.items() if k.startswith("ca") or "fc" in k or k.endswith("a")}
    L.append(f"- Court codes that look appellate: {dict(sorted(app.items()))}")
    L.append(f"- All codes ({len(tally)}): {', '.join(sorted(tally))}\n")
    for code in ("cafc", "fc", "cofc", "cit", "ca1", "ca2", "ca9", "cadc"):
        s2, j2 = get("/published/2024-01-01/2024-12-31", collection="USCOURTS", courtCode=code, pageSize=10, offsetMark="*")
        L.append(f"- courtCode={code}: HTTP {s2}, count {j2.get('count') if isinstance(j2, dict) else 'n/a'}")
        time.sleep(0.5)
    L.append("")

    # 2. USREPORTS: volumes, and per-case granules in two volumes
    st, j = get("/published/1990-01-01/2026-12-31", collection="USREPORTS", pageSize=1000, offsetMark="*")
    vols = sorted(int(p["packageId"].split("-")[1]) for p in j.get("packages", []) if p.get("packageId", "").split("-")[1].isdigit()) if isinstance(j, dict) else []
    L.append(f"## 2. USREPORTS volumes listed (HTTP {st}): {len(vols)}; range {vols[:1]} to {vols[-1:]}; 540 and above: {[v for v in vols if v >= 540]}\n")
    for vol in (547, 585):
        st, g = get(f"/packages/USREPORTS-{vol}/granules", pageSize=200, offsetMark="*")
        gr = g.get("granules", []) if isinstance(g, dict) else []
        L.append(f"### Volume {vol}: HTTP {st}, {g.get('count') if isinstance(g, dict) else 'n/a'} granules")
        block("first five granules", gr[:5], 1500)
        for x in gr[:40]:
            if "v." in (x.get("title") or ""):
                s3, gs = get(f"/packages/USREPORTS-{vol}/granules/{x['granuleId']}/summary")
                block(f"granule summary {x['granuleId']} (HTTP {s3})", gs, 3500)
                for k, u in (gs.get("download", {}) if isinstance(gs, dict) else {}).items():
                    r = requests.get(u, headers=H, timeout=90)
                    L.append(f"- download {k}: HTTP {r.status_code}, {len(r.content)} bytes, {r.headers.get('Content-Type')}")
                L.append("")
                break
    # 3. supremecourt.gov slip-opinion link format and term coverage
    L.append("## 3. supremecourt.gov slip opinions\n")
    for t in ("16", "17", "18", "19", "23"):
        r = requests.get(f"https://www.supremecourt.gov/opinions/slipopinion/{t}", headers=UA, timeout=60)
        hrefs = [h for h in re.findall(r'href=["\']([^"\']+)["\']', r.text) if "pdf" in h.lower()]
        L.append(f"- slipopinion/{t}: HTTP {r.status_code}, final URL {r.url}, {len(r.content)} bytes, {len(hrefs)} pdf hrefs; first three {hrefs[:3]}")
        time.sleep(1)
    r = requests.get("https://www.supremecourt.gov/opinions/USReports.aspx", headers=UA, timeout=60)
    hrefs = [h for h in re.findall(r'href=["\']([^"\']+)["\']', r.text) if "pdf" in h.lower()]
    L.append(f"- USReports.aspx pdf hrefs (sample of the last five): {hrefs[-5:]}")
    OUT.write_text(scrub("\n".join(L)) + "\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
