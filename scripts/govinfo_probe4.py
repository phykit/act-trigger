"""Diagnostic only: GovInfo rate limit, Federal Circuit (ca13) counts by year via the search service, and how the
docket text marks precedential status. Writes data/appeals/govinfo_probe4.md; the key is a header and is scrubbed."""
import collections, json, os, re, time
from pathlib import Path
import requests
KEY = os.environ.get("GOVINFO_API_KEY", "")
H = {"X-Api-Key": KEY, "User-Agent": "act-trigger research (https://github.com/phykit/act-trigger)"}
API = "https://api.govinfo.gov"
OUT = Path(__file__).resolve().parents[1] / "data" / "appeals" / "govinfo_probe4.md"
L = ["# Probe 4 (diagnostic only)\n"]

def post(q, size=100, mark="*"):
    r = requests.post(API + "/search", headers={**H, "Content-Type": "application/json"},
                      json={"query": q, "pageSize": size, "offsetMark": mark, "sorts": [{"field": "publishdate", "sortOrder": "ASC"}]}, timeout=90)
    try: return r.status_code, r.json(), r.headers
    except ValueError: return r.status_code, r.text, r.headers

st, j, hd = post("collection:USCOURTS")
L.append(f"- Rate-limit headers: limit {hd.get('X-RateLimit-Limit')}, remaining {hd.get('X-RateLimit-Remaining')}\n")
variants = ["collection:USCOURTS courtcode:ca13", "collection:(USCOURTS) AND courtcode:(ca13)",
            "collection:USCOURTS courtname:\"Court of Appeals for the Federal Circuit\"", "packageid:USCOURTS-ca13*"]
best = None
for q in variants:
    st, j, _ = post(q, size=5)
    cnt = j.get("count") if isinstance(j, dict) else None
    L.append(f"- query `{q}`: HTTP {st}, count {cnt}; sample {[x.get('packageId') for x in j.get('results', [])][:3] if isinstance(j, dict) else str(j)[:200]}")
    if isinstance(j, dict) and cnt and all(str(x.get("packageId", "")).startswith("USCOURTS-ca13") for x in j.get("results", [])):
        best = best or q
    time.sleep(1)
L.append(f"\n- Query used below: `{best}`\n")
if best:
    L.append("## ca13 packages by year of dateIssued (search service)\n\n| Year | packages |\n|---|---|")
    for y in range(2010, 2027):
        st, j, _ = post(f"{best} dateissued:range({y}-01-01,{y}-12-31)", size=5)
        L.append(f"| {y} | {j.get('count') if isinstance(j, dict) else st} |")
        time.sleep(0.5)
    # Precedential marking: first granule of up to 40 packages from 2013 and 2023
    for y in (2013, 2023):
        st, j, _ = post(f"{best} dateissued:range({y}-03-01,{y}-04-30)", size=40)
        tally = collections.Counter()
        ex = []
        for x in (j.get("results", []) if isinstance(j, dict) else []):
            pid = x["packageId"]
            g = requests.get(f"{API}/packages/{pid}/granules", headers=H, params={"pageSize": 20, "offsetMark": "*"}, timeout=90).json()
            for gr in g.get("granules", [])[:3]:
                s = requests.get(f"{API}/packages/{pid}/granules/{gr['granuleId']}/summary", headers=H, timeout=90).json()
                dt_ = s.get("docketText", "") or ""
                m = re.search(r"(?i)(non-?precedential|precedential)[^.]*\.", dt_)
                tally[m.group(0).strip() if m else "(no marker)"] += 1
                if len(ex) < 4: ex.append(dt_[:220])
            time.sleep(0.2)
        L.append(f"\n## Docket-text markers, packages issued Mar to Apr {y}: {dict(tally)}")
        L += [f"- e.g. {e}" for e in ex]
st, j, hd = post("collection:USCOURTS", size=1)
L.append(f"\n- Rate limit remaining at end: {hd.get('X-RateLimit-Remaining')} of {hd.get('X-RateLimit-Limit')}")
OUT.write_text("\n".join(L).replace(KEY, "[KEY]") + "\n")
