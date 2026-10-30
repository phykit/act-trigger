"""Join committed Water coding sheets to returns, for Water and Void. Runs only after every sheet it reads has been
committed; it never feeds anything back to a coder.

Populations: Moon (data/water/legora/input_moon37.csv, events from the latest Moon result) and Earth (a price-free
coding list data/water/earth_coding_list.csv when it exists, events from the latest Earth result).
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
WATER = ROOT / "data" / "water"
CODERS = {"1": "legora", "2": "claude_a", "2b": "claude_b", "3": "api"}


def latest_events(project: str) -> Path | None:
    files = list((ROOT / "results").glob(f"{project}_result_*.events.csv"))
    if not files:
        return None

    def key(p: Path):
        m = re.search(r"_(\d{4}-\d{2}-\d{2})(?:_(\d+))?\.events\.csv$", p.name)
        return (m.group(1), int(m.group(2) or 1)) if m else ("", 0)
    return max(files, key=key)


def sheets(prefix: str) -> dict[str, pd.DataFrame]:
    out = {}
    for code, name in CODERS.items():
        f = WATER / f"{prefix}_coding_sheet_{name}.csv"
        if f.exists():
            s = pd.read_csv(f, dtype=str).fillna("")
            for c in ("A_money_score", "B_core_business", "C_disclosed", "D_figure_stated", "price_known"):
                s[c] = pd.to_numeric(s[c], errors="coerce")
            s["score"] = s["A_money_score"] + s["B_core_business"] + s["C_disclosed"]
            s["high"] = s["score"] >= 2
            out[code] = s.set_index("event_id")
    return out


def population() -> pd.DataFrame:
    """One row per coded event: event_id, population, signed drift, abs(z_0), and each coder's components."""
    parts = []
    moon_ev = latest_events("moon")
    lst = WATER / "legora" / "input_moon37.csv"
    if moon_ev and lst.exists():
        ev = pd.read_csv(moon_ev)
        ev = ev[ev["status"] == "ok"].copy()
        ev["date"] = ev["date"].astype(str)
        L = pd.read_csv(lst, dtype=str)
        m = L.merge(ev, left_on=["date", "parent_ticker"], right_on=["date", "ticker"], how="left")
        m["drift"] = m["dir"] * m["car_post"]
        m["population"] = "Moon"
        parts.append((m[["event_id", "population", "date", "drift", "z0"]], sheets("moon37")))
    earth_ev = latest_events("earth")
    elst = WATER / "earth_coding_list.csv"
    if earth_ev and elst.exists():
        ev = pd.read_csv(earth_ev)
        ev = ev[ev["status"] == "ok"].copy()
        ev["date"] = ev["date"].astype(str)
        L = pd.read_csv(elst, dtype=str)
        m = L.merge(ev, on=["date", "ticker"], how="left")
        m["drift"] = np.sign(m["ar0"]) * m["car_post"]
        m["population"] = "Earth"
        parts.append((m[["event_id", "population", "date", "drift", "z0"]], sheets("earth")))
    rows = []
    for base, sh in parts:
        b = base.set_index("event_id")
        for code, s in sh.items():
            cols = s[["A_money_score", "B_core_business", "C_disclosed", "D_figure_stated", "price_known", "score", "high"]]
            b = b.join(cols.add_prefix(f"c{code}_"), how="left")
        rows.append(b.reset_index())
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
