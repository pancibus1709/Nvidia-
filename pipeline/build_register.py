"""Assemble the register from the research drafts (R7 step 1).

  python3 -m pipeline.build_register

Reads research/drafts/cluster_*.json and research/drafts/lead_*.json, merges entities that several
researchers created (the fullest record wins, depth takes the lowest), and writes data/register/*.json.
Then run `make evidence measure check`.
"""
from __future__ import annotations

import json
from pathlib import Path

from .common import REGISTER, ROOT, load_json, save_json

DRAFTS = ROOT / "research" / "drafts"
BASE_ENTITIES = [
    {"id": "ent_nvidia", "name": "NVIDIA Corporation", "short_name": "Nvidia", "cluster": "nvidia", "depth": 0, "public": True, "ticker": "NVDA",
     "cik": "0001045810", "country": "US", "description": "Designer of accelerated computing systems. The center of the map.", "domains": ["nvidia.com"]},
    {"id": "ent_nvidia_unattributed", "name": "Unattributed carrying value", "short_name": "Unattributed", "cluster": "other", "depth": 1, "public": False,
     "ticker": None, "cik": None, "country": None,
     "description": "Synthetic entity for the part of a disclosed Nvidia aggregate that no named relationship explains. Excluded from every total."},
]


def richness(e: dict) -> int:
    return len(json.dumps(e.get("credit") or {})) + len(json.dumps(e.get("compute_commitments") or [])) + len(e.get("description") or "")


def merge_entity(a: dict, b: dict) -> dict:
    hi, lo = (a, b) if richness(a) >= richness(b) else (b, a)
    out = dict(lo)
    out.update({k: v for k, v in hi.items() if v not in (None, "", [], {})})
    out["depth"] = min(a.get("depth", 2), b.get("depth", 2))
    # a depth 1 cluster beats a generic depth 2 label
    primary = a if a.get("depth", 2) <= b.get("depth", 2) else b
    if primary.get("cluster") and primary["cluster"] not in ("other",):
        out["cluster"] = primary["cluster"] if a.get("depth") != b.get("depth") else hi.get("cluster", primary["cluster"])
    cc = {json.dumps(c, sort_keys=True): c for c in (a.get("compute_commitments") or []) + (b.get("compute_commitments") or [])}
    if cc:
        out["compute_commitments"] = list(cc.values())
    out["domains"] = sorted(set((a.get("domains") or []) + (b.get("domains") or [])))
    out["evidence"] = sorted(set((a.get("evidence") or []) + (b.get("evidence") or [])))
    return out


def main():
    ents = {e["id"]: e for e in BASE_ENTITIES}
    rels, projs, evts, log = {}, {}, {}, []
    files = sorted(DRAFTS.glob("cluster_*.json")) + sorted(DRAFTS.glob("lead_*.json"))
    for f in files:
        d = load_json(f)
        for e in d.get("entities", []):
            if e["id"] in ents and e["id"] not in ("ent_nvidia", "ent_nvidia_unattributed"):
                ents[e["id"]] = merge_entity(ents[e["id"]], e)
                if f.name.startswith("lead_") and e.get("credit"):
                    # a later credit review replaces the earlier credit block whole, however long the earlier one was
                    ents[e["id"]]["credit"] = e["credit"]
                log.append(f"entity {e['id']} merged from {f.name}")
            elif e["id"] not in ents:
                ents[e["id"]] = e
        for name, store in (("relationships", rels), ("projects", projs), ("events", evts)):
            for r in d.get(name, []):
                if r["id"] in store:
                    log.append(f"DUPLICATE {name[:-1]} {r['id']} in {f.name}: kept the first")
                    continue
                store[r["id"]] = r
    if (DRAFTS / "lead_financials.json").exists():
        pass
    fin = load_json(DRAFTS / "nvidia_financials.json", {})
    save_json(REGISTER / "entities.json", list(ents.values()))
    save_json(REGISTER / "relationships.json", list(rels.values()))
    save_json(REGISTER / "projects.json", list(projs.values()))
    save_json(REGISTER / "events.json", sorted(evts.values(), key=lambda e: e["date"]))
    if fin:
        save_json(REGISTER / "nvidia_financials.json", fin)
    print(f"{len(ents)} entities, {len(rels)} relationships, {len(projs)} projects, {len(evts)} events from {len(files)} drafts")
    for l in log:
        if l.startswith("DUPLICATE"):
            print(l)
    print(f"{sum(1 for l in log if l.startswith('entity'))} entity merges")


if __name__ == "__main__":
    main()
