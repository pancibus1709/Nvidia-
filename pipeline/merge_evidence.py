"""Fold research evidence (research/evidence/*.jsonl) into the canonical store data/register/evidence.json.

Only records referenced by the register are kept, so the canonical store has no orphans.
  python3 -m pipeline.merge_evidence [--all]
"""
from __future__ import annotations

import json
import sys

from .checks import Register, _ev_ids
from .common import REGISTER, save_json
from .evidence import EV_DIR


def main():
    reg = Register()
    pool = {e["id"]: e for e in reg.evidence}
    for f in sorted(EV_DIR.glob("*.jsonl")):
        for line in open(f, encoding="utf-8"):
            e = json.loads(line)
            if str(e.get("id", "")).startswith("ev_"):
                pool[e["id"]] = e
    used = set()
    for coll in (reg.relationships, reg.entities, reg.projects, reg.events, [reg.financials]):
        for row in coll:
            used |= set(_ev_ids(row))
    keep = pool.values() if "--all" in sys.argv else [e for i, e in pool.items() if i in used]
    out = sorted(keep, key=lambda e: int(e["id"].split("_")[1]))
    save_json(REGISTER / "evidence.json", out)
    print(f"{len(out)} evidence records in the canonical store ({len(pool)} gathered)")


if __name__ == "__main__":
    main()
