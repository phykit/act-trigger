"""Build the Legora document bundle for Project Water coder 1.

One PDF per event (W01.pdf ... W37.pdf), each: a cover page (case, party, listed parent, ticker, CIK, ruling date),
the Supreme Court opinion, and the parent's last 10-K and 10-Q filed before the ruling. Price-free by construction:
every filing predates the ruling. Reads nothing under results/. One PDF per event lets a Legora tabular review
have one row per event.

Usage: python scripts/legora_bundle.py data/water/legora/input_moon37.csv bundle_dir
"""
from __future__ import annotations

import html
import os
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd
import requests
from pypdf import PdfWriter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ai_coder as ac  # noqa: E402

CHROME = next((c for c in ("google-chrome", "chromium", "chromium-browser")
               if subprocess.call(["which", c], stdout=subprocess.DEVNULL) == 0), None)


def to_pdf(src: Path, dst: Path) -> bool:
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
                        f"--print-to-pdf={dst}", src.resolve().as_uri()], capture_output=True, timeout=300)
    return r.returncode == 0 and dst.exists() and dst.stat().st_size > 1000


def text_pdf(title: str, body: str, dst: Path) -> bool:
    src = dst.with_suffix(".html")
    src.write_text(f"<html><body style='font-family:serif;font-size:11pt'><h2>{html.escape(title)}</h2>"
                   f"<pre style='white-space:pre-wrap;font-family:serif'>{html.escape(body)}</pre></body></html>")
    ok = to_pdf(src, dst)
    src.unlink()
    return ok


def opinion_pdf(e, work: Path) -> tuple[Path | None, str]:
    # Water v3 amendment 1: the official PDF first; CourtListener only where neither official source has it.
    import scotus_opinions as so  # noqa: PLC0415
    dst = work / f"{e['event_id']}_opinion.pdf"
    pdf, src = so.official_pdf(e["docket"], e["case_name"], e["date"])
    if pdf:
        dst.write_bytes(pdf)
        return dst, src
    if os.environ.get("CL_FALLBACK", "1") != "1":
        return None, f"missing ({src})"
    hdr = {"Authorization": f"Token {ac.CL_TOKEN}"} if ac.CL_TOKEN else {}
    base = "https://www.courtlistener.com/api/rest/v4/search/?type=o&court=scotus"
    res = ac.cl_get(f"{base}&q=docketNumber%3A%22{requests.utils.quote(e['docket'])}%22", hdr).json().get("results", [])
    dst = work / f"{e['event_id']}_opinion.pdf"
    if res:
        for op in res[0].get("opinions", [])[:1]:
            lp = op.get("local_path")
            if lp:
                r = requests.get(f"https://storage.courtlistener.com/{lp}", timeout=120)
                if r.status_code == 200 and r.content[:4] == b"%PDF":
                    dst.write_bytes(r.content)
                    return dst, "official PDF"
    text, src = ac.opinion_text(e["docket"], e["case_name"], e["date"])
    if text and text_pdf(f"Supreme Court opinion: {e['case_name']} ({e['docket']})", text, dst):
        return dst, f"text ({src})"
    return None, "missing"


def filing_pdf(e, form: str, work: Path) -> tuple[Path | None, str]:
    meta = ac.filings_before(e["parent_cik"], e["date"], form)
    if not meta:
        return None, "none filed before ruling"
    raw = work / f"{e['event_id']}_{form}.htm"
    raw.write_bytes(ac.sec_get(meta["url"]).content)
    dst = raw.with_suffix(".pdf")
    if to_pdf(raw, dst):
        return dst, f"{meta['form']} filed {meta['filed']}, accession {meta['accession']}"
    return None, f"conversion failed ({meta['accession']})"


def main(inp: str, out_dir: str) -> None:
    """Resumable: events whose PDF already exists (restored from the Actions cache) are skipped; the loop stops
    at the time budget so the partial bundle and its manifest are still uploaded."""
    if not CHROME:
        raise SystemExit("no headless Chrome on the runner")
    budget = time.time() + 60 * float(os.environ.get("BUNDLE_MINUTES", "80"))
    out = Path(out_dir)
    work = out.parent / "_work"
    out.mkdir(parents=True, exist_ok=True)
    work.mkdir(exist_ok=True)
    mpath = out.parent / "bundle_manifest.csv"
    manifest = pd.read_csv(mpath, dtype=str).to_dict("records") if mpath.exists() else []
    done = {m["event_id"] for m in manifest if (out / f"{m['event_id']}.pdf").exists()}
    manifest = [m for m in manifest if m["event_id"] in done]
    for _, e in pd.read_csv(inp, dtype=str).iterrows():
        eid = e["event_id"]
        if eid in done:
            continue
        if time.time() > budget:
            ac.log(f"time budget reached before {eid}; the next run resumes from here")
            break
        parts, row = [], dict(event_id=eid)
        for key, fn in (("opinion", lambda: opinion_pdf(e, work)),
                        ("10-K", lambda: filing_pdf(e, "10-K", work)),
                        ("10-Q", lambda: filing_pdf(e, "10-Q", work))):
            try:
                path, note = fn()
            except Exception as exc:  # noqa: BLE001
                path, note = None, f"failed: {str(exc)[:80]}"
            row[key] = note
            parts.append((key, path, note))
        cover = (f"Event {eid}\n\nCase: {e['case_name']}\nDocket: {e['docket']}\nRuling date: {e['date']}\n"
                 f"Party: {e['subsidiary_party']} ({e['side']})\nListed parent: {e['parent_ticker']} (SEC CIK {e['parent_cik']})\n\n"
                 "This file contains, in order:\n" + "\n".join(f"  - {k}: {n}" for k, _, n in parts) +
                 "\n\nAll filings in this file were made before the ruling date. It contains no share price reaction to the ruling.")
        cpdf = work / f"{eid}_cover.pdf"
        text_pdf(f"Project Water, event {eid}", cover, cpdf)
        w = PdfWriter()
        for p in [cpdf] + [p for _, p, _ in parts if p]:
            w.append(str(p))
        w.write(str(out / f"{eid}.pdf"))
        manifest.append(row)
        ac.log(str(row))
        pd.DataFrame(manifest).to_csv(mpath, index=False)
        time.sleep(1)
    pd.DataFrame(manifest).to_csv(mpath, index=False)
    ac.log(f"bundle holds {len(manifest)} of 37 events")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
