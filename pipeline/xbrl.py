"""XBRL company facts reader (data.sec.gov/api/xbrl/companyfacts).

  python3 -m pipeline.xbrl search --cik 1045810 "marketable|NonMarketable|PurchaseObligation|Prepaid"
  python3 -m pipeline.xbrl series --cik 1045810 us-gaap:PurchaseObligation [--since 2023-01-01]
"""
from __future__ import annotations

import argparse
import json
import re

from . import edgar


def facts(cik, max_age_hours=None):
    path = edgar.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{edgar.pad(cik)}.json", max_age_hours)
    return json.loads(path.read_text()), path


def _split(concept: str):
    tax, _, name = concept.partition(":")
    return (tax, name) if name else ("us-gaap", tax)


def series(cik, concept: str, since: str | None = None) -> list[dict]:
    data, _ = facts(cik)
    tax, name = _split(concept)
    node = data["facts"].get(tax, {}).get(name)
    if not node:
        return []
    rows = []
    for unit, items in node["units"].items():
        for it in items:
            if since and it["end"] < since:
                continue
            rows.append({**it, "unit": unit})
    rows.sort(key=lambda r: (r["end"], r.get("filed", "")))
    return rows


def fact(cik, concept: str, end: str, form: str | None = None, start: str | None = None):
    """The fact for a concept at a period end. Latest filing wins unless `form` is given."""
    _, path = facts(cik)
    rows = [r for r in series(cik, concept) if r["end"] == end and (not form or r["form"] == form) and (start is None or r.get("start") == start)]
    if not rows:
        return None, path
    return rows[-1], path


def fact_id(concept: str, f: dict) -> str:
    start = f.get("start") or ""
    return f"xbrl:{concept}|end={f['end']}|start={start}|accn={f['accn']}|unit={f.get('unit', 'USD')}"


def lookup(path, locator: str):
    """Resolve an xbrl: locator against a cached companyfacts file. Returns the value or None."""
    m = re.match(r"xbrl:([^|]+)\|end=([^|]*)\|start=([^|]*)\|accn=([^|]*)\|unit=(.*)$", locator)
    if not m:
        return None
    concept, end, start, accn, unit = m.groups()
    tax, name = _split(concept)
    data = json.loads(open(path).read())
    for it in data["facts"].get(tax, {}).get(name, {}).get("units", {}).get(unit, []):
        if it["end"] == end and it["accn"] == accn and (it.get("start") or "") == start:
            return float(it["val"])
    return None


def search(cik, pattern: str) -> list[tuple[str, str, int]]:
    data, _ = facts(cik)
    out = []
    for tax, concepts in data["facts"].items():
        for name, node in concepts.items():
            if re.search(pattern, name, re.I) or re.search(pattern, node.get("label") or "", re.I):
                n = sum(len(v) for v in node["units"].values())
                out.append((f"{tax}:{name}", node.get("label") or "", n))
    return sorted(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("search"); a.add_argument("--cik", required=True); a.add_argument("pattern")
    a = sp.add_parser("series"); a.add_argument("--cik", required=True); a.add_argument("concept"); a.add_argument("--since")
    args = ap.parse_args(argv)
    if args.cmd == "search":
        for c, label, n in search(args.cik, args.pattern):
            print(f"{c:<95} {n:>4}  {label}")
    else:
        for r in series(args.cik, args.concept, args.since):
            print(f"{r.get('start') or '':<10} {r['end']}  {r['val']:>18,}  {r['form']:<6} {r.get('fy')}{r.get('fp')}  filed {r.get('filed')}  {r['accn']}")


if __name__ == "__main__":
    main()
