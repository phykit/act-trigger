"""Official Supreme Court opinion PDFs without CourtListener (prereg/water_v3_amendment_1.md).

Order, per event:
  1. supremecourt.gov slip opinion for the October Term containing the decision date (terms 2017 onwards; earlier
     slip-opinion pages redirect to the bound volumes), matched on the docket number in the PDF file name and,
     where the table row shows one, the decision date.
  2. GovInfo United States Reports (collection USREPORTS): the per-case granule whose caption matches the case
     name and whose decisionDate equals the decision date.
  3. Neither: the caller falls back to CourtListener.

Usage (diagnostic): python scripts/scotus_opinions.py LIST.csv OUT.csv   writes one row per event: source, pages,
characters. No opinion text is written by the diagnostic. The cache directory is not committed.
"""
from __future__ import annotations

import datetime as dt
import html
import io
import json
import os
import re
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path(os.environ.get("OPINION_CACHE", ROOT / ".opinion_cache"))
GOVINFO_KEY = os.environ.get("GOVINFO_API_KEY", "")
GI = "https://api.govinfo.gov"
SC = "https://www.supremecourt.gov"
UA = {"User-Agent": "Mozilla/5.0 (act-trigger research; https://github.com/phykit/act-trigger)"}
USR_VOLUMES = range(545, 600)  # October Term 2004 onwards; volumes not yet on GovInfo return nothing
STOP = {"INC", "CORP", "CORPORATION", "CO", "COMPANY", "LLC", "LTD", "LP", "PLC", "NA", "THE", "OF", "AND", "ET", "AL",
        "US", "USA", "U", "S", "A", "V", "VS", "IN", "RE", "EX", "REL", "FOR", "ON", "BEHALF", "OTHERS", "SIMILARLY",
        "SITUATED", "INDIVIDUALLY", "ALL", "HOLDINGS", "GROUP", "SA", "AG", "BV", "NV", "SE", "DBA", "LLP"}


def _log(m: str) -> None:
    print(m, file=sys.stderr, flush=True)


_LAST: dict[str, float] = {}
STATUS: dict[str, str] = {}


def _get(url: str, headers: dict, params: dict | None = None, attempts: int = 4) -> requests.Response | None:
    host = url.split("/")[2]
    for a in range(attempts):
        gap = (2.0 if "supremecourt" in host else 0.3) - (time.time() - _LAST.get(host, 0))
        if gap > 0:
            time.sleep(gap)
        _LAST[host] = time.time()
        try:
            r = requests.get(url, headers=headers, params=params, timeout=300)
        except requests.RequestException as exc:
            STATUS[url] = type(exc).__name__
            time.sleep(10 * (a + 1))
            continue
        STATUS[url] = str(r.status_code)
        if r.status_code == 200:
            return r
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(min(int(r.headers.get("Retry-After", 0) or 0) or 15 * (a + 1), 120))
            continue
        return None
    return None


def _gi(url: str, **params) -> dict | None:
    if not GOVINFO_KEY:
        return None
    r = _get(url if url.startswith("http") else GI + url, {"X-Api-Key": GOVINFO_KEY, **UA}, params)
    try:
        return r.json() if r is not None else None
    except ValueError:
        return None


def _tokens(s: str) -> set[str]:
    return {w for w in re.sub(r"[^A-Z0-9 ]", " ", s.upper()).split() if w not in STOP and len(w) > 1}


def _sides(case_name: str) -> list[set[str]]:
    parts = re.split(r"\s+v\.?\s+", case_name, maxsplit=1, flags=re.I)
    return [_tokens(re.split(r",", p)[0]) for p in parts]


def term_of(date: str) -> int:
    d = dt.date.fromisoformat(date)
    return d.year if d.month >= 10 else d.year - 1


# ----------------------------------------------------------------------------- 1. slip opinions

def _slip_rows(term: int) -> list[dict]:
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / f"slip2_{term % 100:02d}.json"
    if f.exists():
        return json.loads(f.read_text())
    rows: list[dict] = []
    for attempt in range(3):
        rows = _parse_slip(_get(f"{SC}/opinions/slipopinion/{term % 100:02d}", UA))
        if len(rows) >= 5:
            f.write_text(json.dumps(rows))
            return rows
        time.sleep(30 * (attempt + 1))
    return rows


def _parse_slip(r: requests.Response | None) -> list[dict]:
    """One row per opinion link on a term's opinions page. The link may be the slip opinion, or, once the Court has
    replaced it, a preliminary-print or bound-volume PDF with a #page anchor. Markup-independent: the text between
    the previous link and this one holds this row's date and docket (the last of each is taken); the text after the
    link holds the citation (for example "587 U.S. 299")."""
    rows = []
    if r is None or "/slipopinion/" not in r.url:
        return rows
    pat = re.compile(r'(?i)href=["\']([^"\']*/opinions/(?:\d{2}pdf|preliminaryprint|boundvolumes)/[^"\'#]+\.pdf(?:#page=\d+)?)')
    ms = list(pat.finditer(r.text))
    plain = lambda a, b: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", r.text[a:b])))  # noqa: E731
    seen = set()
    for i, m in enumerate(ms):
        seg = plain(ms[i - 1].end() if i else 0, m.start())
        post = plain(m.end(), ms[i + 1].start() if i + 1 < len(ms) else min(len(r.text), m.end() + 3000))
        href = m.group(1)
        href = href if href.startswith("http") else SC + "/" + href.lstrip("./").lstrip("/")
        if href in seen:
            continue
        seen.add(href)
        dates = re.findall(r"(\d{1,2})/(\d{1,2})/(\d{2,4})", seg)
        date = ""
        if dates:
            mo, d, y = (int(x) for x in dates[-1])
            try:
                date = dt.date(y + 2000 if y < 100 else y, mo, d).isoformat()
            except ValueError:
                date = ""
        dockets = re.findall(r"(?<![\w-])(\d{2}[-A]\d{1,5}|\d{2,3}[Oo]rig|\d{2}O\d{1,4})(?![\w-])", seg)
        cit = re.search(r"\b(\d{3})\s*U\.\s*S\.\s*(\d{1,4})\b", post)
        rows.append(dict(href=href, date=date, docket=dockets[-1] if dockets else "", text=seg[-300:],
                         citation=f"{cit.group(1)} U.S. {cit.group(2)}" if cit else ""))
    return rows


def slip_pdf(docket: str, date: str) -> tuple[bytes | None, str]:
    term = term_of(date)
    if term < 2017:
        return None, "no slip opinion page before OT2017"
    # File names are docket-based up to OT2021 (17-290_6j37.pdf) and citation-based after (598us1r1_3e04.pdf);
    # the docket number is matched in the file name or in the table row's own docket cell.
    pat = re.compile(rf"/{re.escape(docket)}_[A-Za-z0-9]+\.pdf$", re.I)
    cell = re.compile(rf"(?<![\w-]){re.escape(docket)}(?![\w-])")
    rows = _slip_rows(term)
    cands = [r for r in rows if pat.search(r["href"]) or r.get("docket") == docket]
    cands = cands or [r for r in rows if cell.search(r.get("text", "")[-120:])]
    if not cands:
        return None, f"docket {docket} not on the Court's opinions page OT{term} ({len(rows)} opinion links parsed)"
    best = [r for r in cands if r["date"] == date] or cands
    best = sorted(best, key=lambda r: "#page=" in r["href"])  # the slip opinion itself first, where still posted
    row = best[0]
    href = row["href"]
    if "#page=" in href:
        pdf, src = _anchored_range(href, rows)
    else:
        r = _get(href, UA)
        pdf, src = (r.content, f"supremecourt.gov slip opinion {href.replace(SC, '')}") if r is not None and r.content[:4] == b"%PDF" \
            else (None, f"slip opinion PDF not retrieved ({href}; {STATUS.get(href, '?')})")
    if pdf is None and row.get("citation"):
        # The Court's own table gives the citation; the United States Reports granule of that citation is the same case.
        vol, _, page = row["citation"].partition(" U.S. ")
        summ = _gi(f"/packages/USREPORTS-{vol}/granules/USREPORTS-{vol}-{page}/summary")
        link = (summ or {}).get("download", {}).get("pdfLink")
        r = _get(link, {"X-Api-Key": GOVINFO_KEY, **UA}) if link else None
        if r is not None and r.content[:4] == b"%PDF":
            return r.content, f"GovInfo USREPORTS-{vol}-{page} ({row['citation']}, by the citation in the Court's table for docket {docket})"
        src += f"; GovInfo USREPORTS-{vol}-{page} not available"
    return pdf, src


def _anchored_range(href: str, rows: list[dict]) -> tuple[bytes | None, str]:
    """Cut one case out of a preliminary-print part or bound volume: from its #page anchor to the page before the
    next case's anchor in the same file (at most 120 pages)."""
    from pypdf import PdfReader, PdfWriter  # noqa: PLC0415
    base, _, pg = href.partition("#page=")
    start = int(pg or 1)
    starts = sorted({int(r["href"].partition("#page=")[2]) for r in rows
                     if r["href"].startswith(base + "#page=") and r["href"].partition("#page=")[2].isdigit()})
    later = [p for p in starts if p > start]
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / ("pp_" + base.rsplit("/", 1)[-1])
    if not f.exists():
        r = _get(base, UA)
        if r is None or r.content[:4] != b"%PDF":
            return None, f"{base.replace(SC, '')} not retrieved ({STATUS.get(base, '?')})"
        f.write_bytes(r.content)
    rd = PdfReader(str(f))
    end = min((later[0] - 1) if later else start + 119, start + 119, len(rd.pages))
    w = PdfWriter()
    for i in range(start - 1, end):
        w.add_page(rd.pages[i])
    buf = io.BytesIO()
    w.write(buf)
    kind = "bound volume" if "/boundvolumes/" in base else "preliminary print"
    return buf.getvalue(), f"supremecourt.gov {kind} {base.replace(SC, '')} pages {start} to {end}"


# ----------------------------------------------------------------------------- 2. United States Reports

def _usr_index() -> list[dict]:
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / "usreports_index.json"
    if f.exists():
        return json.loads(f.read_text())
    idx = []
    for vol in USR_VOLUMES:
        j = _gi(f"/packages/USREPORTS-{vol}/granules", pageSize=1000, offsetMark="*")
        while j:
            idx += [dict(vol=vol, granule=g["granuleId"], title=g.get("title", "")) for g in j.get("granules", [])
                    if g.get("granuleClass") == "CASE" or " v. " in (g.get("title") or "")]
            j = _gi(j["nextPage"]) if j.get("nextPage") else None
        time.sleep(0.3)
    if idx:
        f.write_text(json.dumps(idx))
    return idx


def usreports_pdf(case_name: str, date: str) -> tuple[bytes | None, str]:
    if not GOVINFO_KEY:
        return None, "GOVINFO_API_KEY not set"
    sides = _sides(case_name)
    scored = []
    for g in _usr_index():
        gs = _sides(re.sub(r",\s*\d+\s+U\.\s*S\..*$", "", g["title"]))
        s = sum(len(a & b) for a, b in zip(sides, gs))
        if s and all(a & b for a, b in zip(sides, gs) if a and b):
            scored.append((s, g))
    seen_dates = []
    for _, g in sorted(scored, key=lambda x: -x[0])[:8]:
        summ = _gi(f"/packages/USREPORTS-{g['vol']}/granules/{g['granule']}/summary")
        if not summ or (summ.get("decisionDate") or {}).get("date") != date:
            seen_dates.append(f"{g['granule']} {(summ or {}).get('decisionDate')}")
            continue
        link = (summ.get("download") or {}).get("pdfLink")
        r = _get(link, {"X-Api-Key": GOVINFO_KEY, **UA}) if link else None
        if r is not None and r.content[:4] == b"%PDF":
            return r.content, f"GovInfo {g['granule']} ({summ.get('fullCitation') or summ.get('usCitation')})"
    return None, f"no United States Reports granule matching caption and date ({len(scored)} caption candidates: {'; '.join(seen_dates)[:200]})"


# ----------------------------------------------------------------------------- combined

def official_pdf(docket: str, case_name: str, date: str) -> tuple[bytes | None, str]:
    notes = []
    for fn in (lambda: slip_pdf(docket, date), lambda: usreports_pdf(case_name, date)):
        try:
            pdf, src = fn()
        except Exception as exc:  # noqa: BLE001
            pdf, src = None, f"error {type(exc).__name__}: {str(exc)[:80]}"
        if pdf:
            return pdf, src
        notes.append(src)
    return None, "; ".join(notes)


def pdf_text(pdf: bytes) -> tuple[str, int]:
    from pypdf import PdfReader  # noqa: PLC0415
    rd = PdfReader(io.BytesIO(pdf))
    return "\n".join((p.extract_text() or "") for p in rd.pages), len(rd.pages)


def main(inp: str, out: str) -> None:
    import pandas as pd  # noqa: PLC0415
    rows = []
    for _, e in pd.read_csv(inp, dtype=str).iterrows():
        pdf, src = official_pdf(e["docket"], e["case_name"], e["date"])
        text, pages = pdf_text(pdf) if pdf else ("", 0)
        rows.append(dict(event_id=e["event_id"], date=e["date"], docket=e["docket"], source=src, pages=pages, chars=len(text),
                         caption_in_text=int(bool(_sides(e["case_name"])[0] & _tokens(text[:6000]))) if text else 0))
        _log(f"{e['event_id']}: {src} ({pages} pages, {len(text)} chars)")
    pd.DataFrame(rows).to_csv(out, index=False)
    ok = sum(1 for r in rows if r["pages"])
    _log(f"wrote {out}: {ok} of {len(rows)} events have an official PDF")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
