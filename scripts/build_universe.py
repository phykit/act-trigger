"""Build and cache the appellate-ruling universe and the party-to-ticker map (Projects Earth, Moon, Fire).

Usage: python scripts/build_universe.py
Writes data/appeals/universe.csv, data/appeals/party_map.csv and the caches they depend on.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appeals_common import build_party_map, build_universe, log  # noqa: E402


def main() -> None:
    uni, note = build_universe()
    log(f"universe: {len(uni)} rulings; {note}")
    pm = build_party_map(uni)
    counts = pm["basis"].value_counts().to_dict()
    log(f"party map: {len(pm)} sides; {counts}")


if __name__ == "__main__":
    main()
