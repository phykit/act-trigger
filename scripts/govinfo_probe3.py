"""Diagnostic only: is USCOURTS court code ca13 the Federal Circuit, and does it flag precedential status?"""
import json, os, re, time
from pathlib import Path
import requests
KEY = os.environ.get("GOVINFO_API_KEY", "")
H = {"X-Api-Key": KEY, "User-Agent": "act-trigger research (https://github.com/phykit/act-trigger)"}
API = "https://api.govinfo.gov"
OUT = Path(__file__).resolve().parents[1] / "data" / "appeals" / "govinfo_probe3.md"
L = ["# Probe 3 (diagnostic only)\n"]
def get(u, **p):
    r = requests.get(u if u.startswith("http") else API + u, headers=H, params=p, timeout=90)
    try: return r.status_code, r.json()
    except ValueError: return r.status_code, r.text
ids, pages = [], 0
st, j = get("/published/2024-03-01/2024-03-31", collection="USCOURTS", pageSize=1000, offsetMark="*")
while isinstance(j, dict) and pages < 15:
    ids += [p["packageId"] for p in j.get("packages", []) if p.get("packageId", "").startswith("USCOURTS-ca13-")]
    pages += 1
    if not j.get("nextPage"): break
    st, j = get(j["nextPage"])
L.append(f"- ca13 packages found in March 2024: {len(ids)}; sample {ids[:5]}\n")
for pid in ids[:4]:
    st, s = get(f"/packages/{pid}/summary")
    L += [f"## {pid} (HTTP {st})", "```", json.dumps(s, indent=1)[:1800], "```"]
    st, g = get(f"/packages/{pid}/granules", pageSize=50, offsetMark="*")
    for x in (g.get("granules", []) if isinstance(g, dict) else [])[:3]:
        s2, gs = get(f"/packages/{pid}/granules/{x['granuleId']}/summary")
        L += [f"### granule {x['granuleId']}", "```", json.dumps(gs, indent=1)[:1500], "```"]
        mods = (gs.get("download") or {}).get("modsLink") if isinstance(gs, dict) else None
        if mods:
            m = requests.get(mods, headers=H, timeout=90).text
            hits = sorted(set(re.findall(r"(?i)(non-?precedential|precedential|unpublished|nonprecedential|opinion|order)", m)))
            L.append(f"- MODS terms: {hits}")
        txt = (gs.get("download") or {}).get("txtLink") if isinstance(gs, dict) else None
        L.append(f"- txtLink present: {bool(txt)}")
    time.sleep(1)
L.append("\n## ca13 package counts by year (prefix filter is impossible server-side; counted from /published pages is too slow, so sample one month per year)\n")
for y in (2012, 2016, 2020, 2025):
    n, pages = 0, 0
    st, j = get(f"/published/{y}-03-01/{y}-03-31", collection="USCOURTS", pageSize=1000, offsetMark="*")
    while isinstance(j, dict) and pages < 15:
        n += sum(1 for p in j.get("packages", []) if p.get("packageId", "").startswith("USCOURTS-ca13-"))
        pages += 1
        if not j.get("nextPage"): break
        st, j = get(j["nextPage"])
    L.append(f"- March {y} (published date): {n} ca13 packages over {pages} pages")
OUT.write_text("\n".join(L).replace(KEY, "[KEY]") + "\n")
