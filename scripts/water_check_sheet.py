"""Check a returned Project Water coding sheet before it is committed. Reads no price data.

Usage: python scripts/water_check_sheet.py data/water/moon37_coding_sheet_legora.csv
Exit code 0 if the sheet is valid; prints every problem otherwise.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
COLS = ["event_id", "A_money_score", "A_figure_usd", "A_mcap_usd", "A_source_url", "B_core_business",
        "C_disclosed", "C_filing_accession", "D_figure_stated", "price_known", "reason"]
FORBIDDEN = ["car", "ar0", "z0", "return", "price_change", "drift", "abnormal"]


def main(path: str) -> int:
    sheet = pd.read_csv(path, dtype=str).fillna("")
    expected = pd.read_csv(ROOT / "data" / "water" / "legora" / "input_moon37.csv", dtype=str)["event_id"].tolist()
    problems = []
    missing = [c for c in COLS if c not in sheet.columns]
    if missing:
        problems.append(f"missing columns: {missing}")
    extra = [c for c in sheet.columns if c not in COLS]
    if any(any(f in c.lower() for f in FORBIDDEN) for c in extra):
        problems.append(f"sheet carries a price-like column, which breaks blindness: {extra}")
    if not missing:
        ids = sheet["event_id"].tolist()
        if sorted(ids) != sorted(expected):
            problems.append(f"event_id set differs: missing {sorted(set(expected) - set(ids))}, extra {sorted(set(ids) - set(expected))}")
        for _, r in sheet.iterrows():
            e = r["event_id"]
            if r["A_money_score"] not in ("0", "1", "2"):
                problems.append(f"{e}: A_money_score must be 0, 1 or 2")
            for c in ("B_core_business", "C_disclosed", "D_figure_stated", "price_known"):
                if r[c] not in ("0", "1"):
                    problems.append(f"{e}: {c} must be 0 or 1")
            for c in ("A_figure_usd", "A_mcap_usd"):
                if r[c] and not r[c].replace(".", "", 1).isdigit():
                    problems.append(f"{e}: {c} must be a plain number or blank")
            if r["A_figure_usd"] and r["A_mcap_usd"] and r["A_money_score"] in ("0", "1", "2"):
                ratio = float(r["A_figure_usd"]) / float(r["A_mcap_usd"]) if float(r["A_mcap_usd"]) else 0
                implied = "2" if ratio >= 0.05 else ("1" if ratio >= 0.01 else "0")
                if implied != r["A_money_score"]:
                    problems.append(f"{e}: A_money_score {r['A_money_score']} does not match figure/mcap = {ratio:.4f} (implies {implied})")
            if r["C_disclosed"] == "1" and not r["C_filing_accession"]:
                problems.append(f"{e}: C_disclosed is 1 but no accession number given")
            if not r["reason"].strip():
                problems.append(f"{e}: reason is empty")
    if problems:
        print(f"{len(problems)} problem(s) in {path}:")
        for p in problems:
            print(" -", p)
        return 1
    score = sheet["A_money_score"].astype(int) + sheet["B_core_business"].astype(int) + sheet["C_disclosed"].astype(int)
    print(f"OK: {len(sheet)} rows; high-stakes (score >= 2): {int((score >= 2).sum())}; price_known: {int((sheet['price_known'] == '1').sum())}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
