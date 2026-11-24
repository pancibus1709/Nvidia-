"""Fold research evidence (research/evidence/*.jsonl) into the canonical store data/register/evidence.json.

Only records referenced by the register are kept, so the canonical store has no orphans.
  python3 -m pipeline.merge_evidence [--all]
"""
from __future__ import annotations

import json
import sys

from .checks import Register, _ev_ids
from .common import REGISTER, ROOT, save_json

REPORTS = ("R7_aggregates.md", "R9.md", "R8.md", "R2.md", "R4.md")
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
    import re
    for extra in ("loops.json", "central_bank.json", "relationships.json", "entities.json", "projects.json", "events.json", "nvidia_financials.json", "complex_links.json"):
        f = REGISTER / extra
        if f.exists():
            used |= set(re.findall(r"ev_\d+", f.read_text()))
    for rep in REPORTS:
        f = ROOT / "research" / "reports" / rep
        if f.exists():
            used |= set(re.findall(r"ev_\d+", f.read_text())) & set(pool)
    keep = pool.values() if "--all" in sys.argv else [e for i, e in pool.items() if i in used]
    out = sorted(keep, key=lambda e: int(e["id"].split("_")[1]))
    save_json(REGISTER / "evidence.json", out)
    print(f"{len(out)} evidence records in the canonical store ({len(pool)} gathered)")


if __name__ == "__main__":
    main()
