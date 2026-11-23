"""Nvidia's 13F-HR holdings by quarter, with quarter-over-quarter changes.

  python3 -m pipeline.thirteenf [--since 2023-01-01]
Writes research/evidence/nvda_13f.json: per report date, every holding (issuer, CUSIP, shares, value)
and events (new position, exit, change of half or more).
"""
from __future__ import annotations

import argparse
import json
import re

from lxml import etree

from . import edgar
from .common import ROOT

OUT = ROOT / "research" / "evidence" / "nvda_13f.json"


def info_table(cik, accession):
    docs = edgar.filing_index(cik, accession)
    cands = [d for d in docs if d["name"].lower().endswith(".xml") and "primary_doc" not in d["name"].lower()]
    for d in cands:
        path = edgar.get(d["url"])
        raw = path.read_bytes()
        if b"infoTable" not in raw:
            continue
        root = etree.fromstring(raw)
        rows = []
        for it in root.iter("{*}infoTable"):
            g = lambda tag: (it.findtext(f".//{{*}}{tag}") or "").strip()
            rows.append({"issuer": g("nameOfIssuer"), "class": g("titleOfClass"), "cusip": g("cusip"),
                         "value": float(g("value") or 0), "shares": float(g("sshPrnamt") or 0), "share_type": g("sshPrnamtType"),
                         "put_call": g("putCall") or None})
        return rows, d["url"], str(path.resolve().relative_to(ROOT))
    return [], None, None


def run(since="2023-01-01"):
    filings = [f for f in edgar.list_filings(edgar.NVIDIA_CIK, {"13F-HR", "13F-HR/A"}, since)]
    filings.sort(key=lambda f: (f["report_date"], f["filed"]))
    quarters = {}
    for f in filings:
        rows, url, path = info_table(edgar.NVIDIA_CIK, f["accession"])
        # values were reported in thousands of dollars before 2023 filings; since then in dollars
        quarters[f["report_date"]] = {"accession": f["accession"], "form": f["form"], "filed": f["filed"], "url": url, "cache_path": path, "holdings": rows}
    out, prev = [], {}
    for rd in sorted(quarters):
        q = quarters[rd]
        cur = {}
        for h in q["holdings"]:
            k = h["cusip"]
            if k in cur:
                cur[k]["shares"] += h["shares"]; cur[k]["value"] += h["value"]
            else:
                cur[k] = dict(h)
        events = []
        for k, h in cur.items():
            p = prev.get(k)
            if p is None:
                events.append({"kind": "new_position", "issuer": h["issuer"], "shares": h["shares"], "value": h["value"]})
            elif p["shares"] and abs(h["shares"] - p["shares"]) / p["shares"] >= 0.5:
                events.append({"kind": "position_changed", "issuer": h["issuer"], "from_shares": p["shares"], "to_shares": h["shares"]})
        for k, p in prev.items():
            if k not in cur:
                events.append({"kind": "exit", "issuer": p["issuer"], "from_shares": p["shares"]})
        out.append({"report_date": rd, **{k: q[k] for k in ("accession", "form", "filed", "url", "cache_path")},
                    "total_value": sum(h["value"] for h in cur.values()), "holdings": sorted(cur.values(), key=lambda h: -h["value"]), "events": events})
        prev = cur
    OUT.write_text(json.dumps(out, indent=1))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="2023-01-01")
    args = ap.parse_args()
    for q in run(args.since):
        print(f"\n{q['report_date']}  filed {q['filed']}  {q['accession']}  total ${q['total_value']:,.0f}")
        for h in q["holdings"]:
            print(f"   {h['issuer'][:32]:<32} {h['cusip']}  {h['shares']:>14,.0f} sh  ${h['value']:>16,.0f}")
        for e in q["events"]:
            print("   EVENT", e)


if __name__ == "__main__":
    main()
