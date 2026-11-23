"""R2: the counterparty filings sweep. Runs queries Q1 to Q12 against EDGAR full-text search,
fetches each hit, and keeps it only if the query terms fall within a 50-word window.

  python3 -m pipeline.fulltext run [--only Q1,Q2] [--start 2023-01-01] [--end YYYY-MM-DD] [--max-docs 500]
  python3 -m pipeline.fulltext report

Output: research/evidence/fulltext_hits.ndjson (one line per kept hit, with the window as the paragraph)
and research/evidence/fulltext_log.json (totals, overflow flags, discards).
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import date, timedelta
from pathlib import Path

from . import edgar
from .common import ROOT, doc_text, html_to_text

# Root forms: the search API matches amendments (S-1/A, 10-K/A ...) under their root form. Listing "S-1/A"
# separately turns into an AND filter and silently drops almost every hit, so it is not listed.
FORMS = ["10-K", "10-Q", "8-K", "S-1", "F-1", "424B4", "424B5", "20-F", "6-K", "DEF 14A"]
QUERIES = {
    "Q1": [["NVIDIA", "backstop"]],
    "Q2": [["NVIDIA", "unused capacity"], ["NVIDIA", "unsold capacity"], ["NVIDIA", "residual capacity"]],
    "Q3": [["NVIDIA", "guarantee"], ["NVIDIA", "guaranty"]],
    "Q4": [["NVIDIA", "subscription agreement"], ["NVIDIA", "securities purchase agreement"], ["NVIDIA", "investment agreement"]],
    "Q5": [["NVIDIA", "warrant"]],
    "Q6": [["NVIDIA", "master services agreement"], ["NVIDIA", "cloud services agreement"]],
    "Q7": [["NVIDIA", "lease", "GPU"], ["NVIDIA", "leaseback"]],
    "Q8": [["NVIDIA", "prepayment"], ["NVIDIA", "prepaid"], ["NVIDIA", "deposit"]],
    "Q9": [["NVIDIA", "principal stockholder"], ["NVIDIA", "beneficial owner"]],
    "Q10": [["NVIDIA", "collateral"], ["NVIDIA", "security interest"], ["NVIDIA", "GPU-backed"]],
    "Q11": [["NVIDIA", "concentration", "supplier"]],
    "Q12": [["NVIDIA", "license", "non-exclusive"]],
}
CAP = 500
OUT = ROOT / "research" / "evidence" / "fulltext_hits.ndjson"
LOG = ROOT / "research" / "evidence" / "fulltext_log.json"
MONEY = re.compile(r"\$\s?\d|\bmillion\b|\bbillion\b|\bshares\b|\bcommit", re.I)


def window_match(text: str, terms: list[str], words: int = 50) -> str | None:
    """Smallest stretch of at most `words` words containing every term. None if there is none."""
    toks = [(m.group(0), m.start(), m.end()) for m in re.finditer(r"\S+", text)]
    low = text.lower()
    pos = {}
    for t in terms:
        tl = t.lower()
        pos[t] = [m.start() for m in re.finditer(re.escape(tl), low)]
        if not pos[t]:
            return None
    starts = [s for _, s, _ in toks]
    import bisect
    anchor = terms[1] if len(terms) > 1 else terms[0]
    best = None
    for p in pos[anchor]:
        i = bisect.bisect_right(starts, p) - 1
        lo_i, hi_i = max(0, i - words), min(len(toks) - 1, i + words)
        ok_spans = []
        for t in terms:
            near = [q for q in pos[t] if toks[lo_i][1] <= q <= toks[hi_i][2]]
            if not near:
                ok_spans = None
                break
            ok_spans.append(min(near, key=lambda q: abs(q - p)))
        if ok_spans is None:
            continue
        a, b = min(ok_spans + [p]), max(ok_spans + [p])
        ia, ib = bisect.bisect_right(starts, a) - 1, bisect.bisect_right(starts, b) - 1
        if ib - ia + 1 <= words:
            pad = (words - (ib - ia + 1)) // 2 + 15
            s, e = toks[max(0, ia - pad)][1], toks[min(len(toks) - 1, ib + pad)][2]
            cand = (ib - ia, text[s:e])
            if best is None or (MONEY.search(cand[1]) and not MONEY.search(best[1])) or cand[0] < best[0] and bool(MONEY.search(cand[1])) >= bool(MONEY.search(best[1])):
                best = cand
    return best[1] if best else None


def date_windows(start: str, end: str, pieces: int):
    s, e = date.fromisoformat(start), date.fromisoformat(end)
    step = (e - s) / pieces
    out = []
    for i in range(pieces):
        a = s + step * i + (timedelta(days=1) if i else timedelta(0))
        b = s + step * (i + 1) if i < pieces - 1 else e
        out.append((a.isoformat(), b.isoformat()))
    return out


def collect(terms, start, end, log, depth=0):
    """All hits for one query in a date window. Splits the window when the result overflows the cap."""
    q = " ".join(f'"{t}"' for t in terms)
    first = edgar.fulltext_search(q, FORMS, start, end)
    total = first["hits"]["total"]["value"]
    if total > CAP and depth < 5 and start != end:
        log.append({"query": q, "window": [start, end], "total": total, "action": "overflow: date range narrowed"})
        hits = []
        for a, b in date_windows(start, end, 2):
            hits += collect(terms, a, b, log, depth + 1)
        return hits
    hits = list(first["hits"]["hits"])
    off = 100
    while off < min(total, CAP):
        hits += edgar.fulltext_search(q, FORMS, start, end, off)["hits"]["hits"]
        off += 100
    log.append({"query": q, "window": [start, end], "total": total, "fetched": len(hits),
                "action": "ok" if total <= CAP else "overflow at minimum window: capped"})
    return hits


def run(only=None, start="2023-01-01", end=None, max_docs=None):
    end = end or date.today().isoformat()
    log, kept, seen = [], [], set()
    stats = {}
    if OUT.exists():
        for line in open(OUT):
            r = json.loads(line)
            seen.add((r["qid"], r["query"], r["accession"], r["file"]))
            kept.append(r)
    with open(OUT, "a", encoding="utf-8") as fh:
        for qid, variants in QUERIES.items():
            if only and qid not in only:
                continue
            for terms in variants:
                q = " ".join(f'"{t}"' for t in terms)
                hits = collect(terms, start, end, log)
                n_keep = n_drop = n_err = 0
                for h in hits[: max_docs or len(hits)]:
                    row = edgar.hit_to_row(h)
                    if not row["url"] or row["cik"].lstrip("0") == edgar.NVIDIA_CIK.lstrip("0"):
                        continue
                    key = (qid, q, row["accession"], row["file"])
                    if key in seen:
                        n_keep += 1
                        continue
                    try:
                        # read without caching; only documents that pass the window filter are kept on disk
                        text = html_to_text(edgar.fetch_text(row["url"]))
                    except Exception as e:  # noqa: BLE001
                        n_err += 1
                        continue
                    win = window_match(text, terms)
                    if not win:
                        n_drop += 1
                        continue
                    try:
                        edgar.get(row["url"])
                    except Exception:  # noqa: BLE001
                        pass
                    rec = {"qid": qid, "query": q, **row, "names": row["names"][:2], "paragraph": win, "has_money": bool(MONEY.search(win))}
                    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    fh.flush()
                    seen.add(key)
                    n_keep += 1
                stats[q] = {"qid": qid, "hits": len(hits), "kept_within_50_words": n_keep, "dropped_outside_window": n_drop, "fetch_errors": n_err}
                print(f"{qid} {q}: {len(hits)} hits, {n_keep} kept, {n_drop} outside window, {n_err} errors", flush=True)
    global LOG
    if only:
        LOG = LOG.with_name("fulltext_log_" + "_".join(sorted(only)) + ".json")
    prev = json.loads(LOG.read_text()) if LOG.exists() else {"stats": {}, "log": []}
    prev["stats"].update(stats)
    prev["log"] += log
    prev["window"] = [start, end]
    LOG.write_text(json.dumps(prev, indent=1))


def report():
    rows = [json.loads(l) for l in open(OUT)]
    by = {}
    for r in rows:
        name = (r["names"] or ["?"])[0]
        d = by.setdefault(name, {"n": 0, "q": set(), "money": 0, "forms": set(), "last": ""})
        d["n"] += 1; d["q"].add(r["qid"]); d["money"] += r["has_money"]; d["forms"].add(r["form"]); d["last"] = max(d["last"], r["filed"] or "")
    for name, d in sorted(by.items(), key=lambda kv: -kv[1]["money"]):
        print(f"{d['money']:>4} money / {d['n']:>4} hits  {name[:60]:<60} {','.join(sorted(d['q'], key=lambda x: int(x[1:])))}  last {d['last']}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["run", "report"])
    ap.add_argument("--only"); ap.add_argument("--start", default="2023-01-01"); ap.add_argument("--end"); ap.add_argument("--max-docs", type=int)
    args = ap.parse_args(argv)
    if args.cmd == "run":
        run(set(args.only.split(",")) if args.only else None, args.start, args.end, args.max_docs)
    else:
        report()


if __name__ == "__main__":
    main()
