"""Project Water coder 3: reproducible API materiality coder (prereg/water_v3_prereg.md).

For each event in a price-free coding list it builds a document pack from primary sources (the
Supreme Court opinion from CourtListener; the parent's last 10-K and 10-Q before the ruling from
EDGAR), sends it with the frozen rubric to a pinned model, and writes a coding sheet.

Usage: python scripts/ai_coder.py data/water/legora/input_moon37.csv data/water/moon37_coding_sheet_api.csv
Needs ANTHROPIC_API_KEY, COURTLISTENER_TOKEN, SEC_CONTACT (optional). Reads nothing under results/.
AI_CODER_DRYRUN=1 replaces every network call with synthetic text and a canned answer.
"""
from __future__ import annotations

import gzip
import hashlib
import html
import json
import os
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
MODEL = "claude-sonnet-5-5"
DRY = os.environ.get("AI_CODER_DRYRUN") == "1"
SEC_UA = os.environ.get("SEC_CONTACT") or "Simon Kittson skittson@gmail.com"
CL_TOKEN = os.environ.get("COURTLISTENER_TOKEN", "")
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OUT_DIR = ROOT / "data" / "water" / "api_coder"
CAP_OPINION, CAP_SECTION, CAP_WINDOWS, WINDOW = 45_000, 15_000, 10, 3_000
_last_sec = [0.0]

SYSTEM = """You are coding the economic materiality of a US Supreme Court ruling to a listed company, for a pre-registered study. You are given a document pack: the Supreme Court opinion and extracts from the listed parent's last 10-K and 10-Q filed before the ruling. Use only the pack. You have no price or market information and must not use any knowledge of how the company's shares reacted; if you recall the reaction, set price_known to 1 and code on the pack alone.

Score:
A. Money at stake relative to the parent (A_money_score). The largest money figure the ruling decides or puts at risk for the party (damages award, tax assessment, class-wide exposure, or an amount the parent disclosed for this case), divided by the parent's market value held by non-affiliates as stated on the 10-K cover. 2 if 5% or more; 1 if at least 1% and under 5%; 0 if under 1% or if no figure is in the pack. Report A_figure_usd and A_mcap_usd as plain numbers, or null.
B. Core business (B_core_business). 1 if the ruling directly governs one of the parent's core products, licences, franchises, patents, regulatory permissions, or its principal pricing or contracting practice; 0 if it concerns a single employee, a single customer, a peripheral transaction, or a procedural point of no wider business effect.
C. Disclosed as material (C_disclosed). 1 if the 10-K or 10-Q extracts name this case or describe it unmistakably in Legal Proceedings, risk factors or the contingencies note; 0 otherwise. Give the accession number of that filing (from the pack header) in C_filing_accession, or null.
D. Figure stated (D_figure_stated). 1 if the opinion or the parent's disclosure states a money figure for the consequence of the ruling; 0 otherwise.

Return only a JSON object with keys: A_money_score, A_figure_usd, A_mcap_usd, B_core_business, C_disclosed, C_filing_accession, D_figure_stated, price_known, reason (one sentence)."""

PROMPT_SHA = hashlib.sha256(SYSTEM.encode()).hexdigest()


def log(m: str) -> None:
    print(m, file=sys.stderr, flush=True)


def strip_html(t: str) -> str:
    t = re.sub(r"(?is)<(script|style).*?</\1>", " ", t)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    t = html.unescape(t)
    return re.sub(r"[ \t\r\f\v]+", " ", re.sub(r"\n\s*\n+", "\n", t))


def sec_get(url: str) -> requests.Response:
    for attempt in range(4):
        wait = 0.15 - (time.time() - _last_sec[0])
        if wait > 0:
            time.sleep(wait)
        _last_sec[0] = time.time()
        r = requests.get(url, headers={"User-Agent": SEC_UA, "Accept-Encoding": "gzip, deflate"}, timeout=90)
        if r.status_code == 200:
            return r
        if r.status_code in (403, 429, 503):
            time.sleep(5 * (attempt + 1))
            continue
        r.raise_for_status()
    r.raise_for_status()
    return r


# ----------------------------------------------------------------------------- sources

def cl_get(url: str, hdr: dict, attempts: int | None = None) -> requests.Response:
    """CourtListener GET that waits out rate limits (429) rather than giving up."""
    for attempt in range(attempts or int(os.environ.get("CL_ATTEMPTS", "8"))):
        r = requests.get(url, headers=hdr, timeout=90)
        if r.status_code == 429 or r.status_code >= 500:
            wait = int(r.headers.get("Retry-After", 0) or 0) or 30 * (attempt + 1)
            log(f"CourtListener {r.status_code}; waiting {wait}s")
            time.sleep(min(wait, 300))
            continue
        r.raise_for_status()
        return r
    r.raise_for_status()
    return r


def opinion_text(docket: str, case_name: str, date: str = "") -> tuple[str, str]:
    if DRY:
        return f"SYNTHETIC OPINION for {case_name}. The judgment of $50,000,000 is affirmed.", "dry"
    # Water v3 amendment 1: the official text first (supremecourt.gov slip opinion, then GovInfo United States
    # Reports); CourtListener only where neither has the opinion.
    import scotus_opinions as so  # noqa: PLC0415
    pdf, src = so.official_pdf(docket, case_name, date)
    if pdf:
        text, _ = so.pdf_text(pdf)
        if len(text) > 2000:
            return text, src
        src += " (PDF had no extractable text)"
    if os.environ.get("CL_FALLBACK", "1") != "1":
        return "", f"official sources failed ({src}); CourtListener fallback disabled"
    hdr = {"Authorization": f"Token {CL_TOKEN}"} if CL_TOKEN else {}
    base = "https://www.courtlistener.com/api/rest/v4/search/?type=o&court=scotus"
    queries = [f"{base}&q=docketNumber%3A%22{requests.utils.quote(docket)}%22"]
    first = re.split(r"\s+v\.?\s+|,", case_name, maxsplit=1, flags=re.I)[0].strip()
    if first and date:
        y, m, d = date.split("-")
        queries.append(f"{base}&q=caseName%3A%22{requests.utils.quote(first)}%22"
                       f"&filed_after={int(y)}-{m}-01&filed_before={date}")
    res = []
    for url in queries:
        res = cl_get(url, hdr).json().get("results", [])
        if res:
            break
        time.sleep(0.5)
    if not res:
        return "", f"official sources failed ({src}); no CourtListener cluster for docket {docket}"
    cid = res[0].get("cluster_id")
    texts = []
    for op in res[0].get("opinions", [])[:6]:
        oid = op.get("id")
        if not oid:
            continue
        o = cl_get(f"https://www.courtlistener.com/api/rest/v4/opinions/{oid}/", hdr).json()
        t = o.get("plain_text") or strip_html(o.get("html_with_citations") or o.get("html") or o.get("xml_harvard") or "")
        texts.append(f"[{op.get('type', 'opinion')}]\n{t}")
        time.sleep(1.0)
    return "\n\n".join(texts), f"CourtListener cluster {cid} (official sources failed: {src})"


def filings_before(cik: str, date: str, form: str) -> dict | None:
    if DRY:
        return dict(accession="0000000000-00-000000", url="dry", filed="2000-01-01", form=form)
    j = sec_get(f"https://data.sec.gov/submissions/CIK{int(cik):010d}.json").json()
    blocks = [j.get("filings", {}).get("recent", {})]
    for f in j.get("filings", {}).get("files", []) or []:
        try:
            blocks.append(sec_get(f"https://data.sec.gov/submissions/{f['name']}").json())
        except Exception as exc:  # noqa: BLE001
            log(f"submissions page failed: {exc}")
    best = None
    for b in blocks:
        for fm, fd, acc, doc in zip(b.get("form", []), b.get("filingDate", []), b.get("accessionNumber", []), b.get("primaryDocument", [])):
            if fm in (form, form + "405") and fd < date and (best is None or fd > best["filed"]):
                best = dict(form=fm, filed=fd, accession=acc,
                            url=f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-', '')}/{doc}")
    return best


def filing_text(meta: dict) -> str:
    if DRY:
        return ("aggregate market value of the voting stock held by non-affiliates was $1,000,000,000. "
                "Item 3. Legal Proceedings. The company is a party to a case pending in the Supreme Court. Item 4.")
    return strip_html(sec_get(meta["url"]).text)


def extract(text: str, names: list[str]) -> str:
    low = text.lower()
    parts = []
    m = re.search(r"aggregate market value[^.]{0,400}(?:\.[^.]{0,200}){0,2}", text, flags=re.I)
    if m:
        parts.append("[cover] " + m.group(0)[:1200])
    best = ""
    for it in re.finditer(r"item\s*3\.?\s*[-:]?\s*legal\s+proceedings", low):
        end = re.search(r"item\s*4\.?", low[it.end():])
        sec = text[it.start(): it.end() + (end.start() if end else CAP_SECTION)]
        if len(sec) > len(best):
            best = sec
    if best:
        parts.append("[Item 3] " + best[:CAP_SECTION])
    keys = [k for k in names if k and len(k) >= 4] + ["Supreme Court"]
    spans = []
    for k in keys:
        for mm in re.finditer(re.escape(k.lower()), low):
            spans.append((max(0, mm.start() - WINDOW // 2), min(len(text), mm.end() + WINDOW // 2)))
    spans.sort()
    merged = []
    for s, e in spans:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    for s, e in merged[:CAP_WINDOWS]:
        parts.append("[passage] " + text[s:e])
    return "\n\n".join(parts)


def name_keys(case_name: str, party: str) -> list[str]:
    sides = re.split(r"\s+v\.?\s+", case_name, maxsplit=1, flags=re.I)
    out = []
    for s in sides + [party]:
        s = re.sub(r",?\s*(et al\.?|petitioners?|respondents?)", "", s, flags=re.I)
        s = re.sub(r"\b(inc|corp|corporation|co|company|llc|ltd|l\.?p|n\.?a|b\.?v)\b\.?", "", s, flags=re.I)
        words = [w for w in re.split(r"[\s,]+", s) if w]
        if words:
            out.append(" ".join(words[:3]))
            out.append(max(words, key=len))
    return sorted(set(o for o in out if len(o) >= 4))


# ----------------------------------------------------------------------------- model

def call_model(pack: str) -> tuple[dict, dict]:
    if DRY:
        ans = dict(A_money_score=1, A_figure_usd=50000000, A_mcap_usd=1000000000, B_core_business=1, C_disclosed=1,
                   C_filing_accession="0000000000-00-000000", D_figure_stated=1, price_known=0, reason="dry run")
        return ans, dict(input_tokens=0, output_tokens=0)
    body = dict(model=MODEL, max_tokens=4000, system=SYSTEM, messages=[{"role": "user", "content": pack}])
    for attempt in range(5):
        r = requests.post("https://api.anthropic.com/v1/messages", json=body, timeout=300,
                          headers={"x-api-key": API_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"})
        if r.status_code == 200:
            break
        if r.status_code in (429, 500, 502, 503, 529):
            time.sleep(15 * (attempt + 1))
            continue
        raise RuntimeError(f"Anthropic API status {r.status_code}: {r.text[:300]}")
    j = r.json()
    txt = "".join(c.get("text", "") for c in j.get("content", []) if c.get("type") == "text")
    m = re.search(r"\{.*\}", txt, flags=re.S)
    if not m:
        raise RuntimeError(f"no JSON in model reply (stop_reason {j.get('stop_reason')}): {txt[:200]}")
    return json.loads(m.group(0)), j.get("usage", {})


def call_model_retry(pack: str) -> tuple[dict, dict]:
    try:
        return call_model(pack)
    except (ValueError, RuntimeError) as exc:
        if "status" in str(exc) and "Anthropic" in str(exc):
            raise
        log(f"unparseable reply, retrying once: {str(exc)[:120]}")
        return call_model(pack)


def num(x) -> str:
    if x in (None, "", "null"):
        return ""
    try:
        v = float(str(x).replace(",", "").replace("$", ""))
        return str(int(v)) if v == int(v) else str(v)
    except ValueError:
        return ""


def main(inp: str, out: str) -> None:
    if not DRY and not API_KEY:
        raise SystemExit("ANTHROPIC_API_KEY is not set")
    lst = pd.read_csv(inp, dtype=str)
    if any(c.lower() in ("car", "ar0", "z0", "car_post", "signed_post") for c in lst.columns):
        raise SystemExit("coding list carries price columns; refusing to code")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows, usage_tot, mismatches, no_opinion = [], dict(input_tokens=0, output_tokens=0), 0, 0
    for _, e in lst.iterrows():
        eid = e["event_id"]
        notes = []
        try:
            op, op_src = opinion_text(e["docket"], e["case_name"], e["date"])
        except Exception as exc:  # noqa: BLE001
            op, op_src = "", f"opinion fetch failed: {str(exc)[:100]}"
        keys = name_keys(e["case_name"], e["subsidiary_party"])
        pack = [f"EVENT {eid}\nCase: {e['case_name']} (docket {e['docket']}), decided {e['date']}.\n"
                f"Party: {e['subsidiary_party']} ({e['side']}). Listed parent: {e['parent_ticker']} (CIK {e['parent_cik']}).\n",
                f"=== SUPREME COURT OPINION ({op_src}) ===\n{op[:CAP_OPINION] if op else '[not available]'}"]
        for form in ("10-K", "10-Q"):
            try:
                meta = filings_before(e["parent_cik"], e["date"], form)
                if not meta:
                    pack.append(f"=== {form}: none filed before the ruling ===")
                    continue
                ext = extract(filing_text(meta), keys)
                pack.append(f"=== {meta['form']} filed {meta['filed']}, accession {meta['accession']} ({meta['url']}) ===\n{ext or '[no relevant passages found]'}")
            except Exception as exc:  # noqa: BLE001
                pack.append(f"=== {form}: fetch failed ===")
                notes.append(f"{form} failed: {str(exc)[:80]}")
        pack_txt = "\n\n".join(pack)
        pack_sha = hashlib.sha256(pack_txt.encode()).hexdigest()
        (OUT_DIR / "packs").mkdir(exist_ok=True)
        with gzip.open(OUT_DIR / "packs" / f"{eid}.txt.gz", "wt") as fh:
            fh.write(pack_txt)
        if not op:
            ans, usage = dict(reason=f"not coded: opinion unavailable ({op_src[:100]})"), {}
            notes.append("opinion unavailable; model not called")
            no_opinion += 1
            if no_opinion >= 3 and no_opinion == len(rows) + 1:
                raise SystemExit(f"opinion unavailable for the first {no_opinion} events ({op_src}); aborting before spending on the rest")
        else:
            try:
                ans, usage = call_model_retry(pack_txt)
            except Exception as exc:  # noqa: BLE001
                ans, usage = dict(reason=f"model call failed: {str(exc)[:150]}"), {}
                notes.append("model failed")
        for k in usage_tot:
            usage_tot[k] += int(usage.get(k, 0) or 0)
        # The rubric defines A by the ratio; where the model gives both figures, the score is the ratio's band.
        # The model's own A is kept in the response file and mismatches are counted in run_meta.json.
        fig, cap = num(ans.get("A_figure_usd")), num(ans.get("A_mcap_usd"))
        if fig and cap and float(cap) > 0:
            ratio = float(fig) / float(cap)
            band = 2 if ratio >= 0.05 else (1 if ratio >= 0.01 else 0)
            if str(ans.get("A_money_score")) != str(band):
                notes.append(f"A recomputed from ratio {ratio:.4f}: model said {ans.get('A_money_score')}, band {band}")
                mismatches += 1
            ans["A_money_score_model"] = ans.get("A_money_score")
            ans["A_money_score"] = band
        (OUT_DIR / "responses").mkdir(exist_ok=True)
        (OUT_DIR / "responses" / f"{eid}.json").write_text(json.dumps(dict(event_id=eid, model=MODEL, prompt_sha256=PROMPT_SHA,
                                                                           pack_sha256=pack_sha, usage=usage, answer=ans, notes=notes), indent=1))
        rows.append(dict(event_id=eid, A_money_score=str(ans.get("A_money_score", "")), A_figure_usd=num(ans.get("A_figure_usd")),
                         A_mcap_usd=num(ans.get("A_mcap_usd")), A_source_url=f"pack {pack_sha[:12]}",
                         B_core_business=str(ans.get("B_core_business", "")), C_disclosed=str(ans.get("C_disclosed", "")),
                         C_filing_accession=str(ans.get("C_filing_accession") or ""), D_figure_stated=str(ans.get("D_figure_stated", "")),
                         price_known=str(ans.get("price_known", "")), reason=str(ans.get("reason", "")).replace("\n", " ")))
        log(f"{eid}: A={ans.get('A_money_score')} B={ans.get('B_core_business')} C={ans.get('C_disclosed')} tokens={usage}")
    pd.DataFrame(rows).to_csv(out, index=False)
    meta = dict(model=MODEL, prompt_sha256=PROMPT_SHA, events=len(rows), usage=usage_tot, input=inp, output=out,
                a_score_recomputed_from_ratio=mismatches, opinion_unavailable=no_opinion,
                failed_events=[r["event_id"] for r in rows if r["A_money_score"] in ("", "None")],
                run_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    (OUT_DIR / "run_meta.json").write_text(json.dumps(meta, indent=1))
    log(f"wrote {out}; usage {usage_tot}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
