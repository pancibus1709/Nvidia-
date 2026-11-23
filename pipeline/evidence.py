"""Create grounded evidence records.

A record is written only if the quote is found verbatim in the cached source. That makes
every research record grounded at the moment it is written, not checked afterwards.

  python3 -m pipeline.evidence add --ns r1 --path <cache_path> --quote "<verbatim, under 15 words>" \
      --section "Note 6 - Fair Value" --published 2026-02-25 --title "Form 10-K FY2026" \
      --supports rel_x.amounts.funded [--value 5000000000] [--scale-anchor "In millions"] \
      [--near 123456] [--publisher NVIDIA] [--kind sec_filing] [--sourcing filing] [--cites Bloomberg]
  python3 -m pipeline.evidence xbrl --ns r1 --cik 1045810 --concept us-gaap:EquitySecuritiesWithoutReadilyDeterminableFairValueAmount --end 2026-01-25 --supports ...
  python3 -m pipeline.evidence list --ns r1

Records go to research/evidence/<ns>.jsonl. Namespaces get id ranges so parallel researchers never collide.
`pipeline.merge_evidence` folds them into data/register/evidence.json.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import cache as cache_mod
from . import edgar
from .common import CACHE, ROOT, classify_domain, doc_text, enums, norm, sha256_file, table_scale, value_in_text, word_count

EV_DIR = ROOT / "research" / "evidence"
WINDOW = 300
MAX_QUOTE_WORDS = 14


class GroundingError(RuntimeError):
    pass


def _ns_base(ns: str) -> int:
    EV_DIR.mkdir(parents=True, exist_ok=True)
    reg = EV_DIR / "_namespaces.json"
    with open(EV_DIR / ".lock", "a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        data = json.loads(reg.read_text()) if reg.exists() else {}
        if ns not in data:
            data[ns] = (max(data.values()) + 10000) if data else 10000
            reg.write_text(json.dumps(data, indent=2))
        fcntl.flock(lock, fcntl.LOCK_UN)
    return data[ns]


def _next_id(ns: str) -> str:
    base = _ns_base(ns)
    f = EV_DIR / f"{ns}.jsonl"
    n = sum(1 for _ in open(f)) if f.exists() else 0
    return f"ev_{base + n + 1}"


def deep_link(url: str, quote: str) -> str:
    """Link that opens the source document itself and scrolls to the quoted passage.

    Uses a text fragment (#:~:text=). Browsers that do not support it still open the document.
    Not used for XBRL API responses, which have no readable page.
    """
    from urllib.parse import quote as q
    words = norm(quote).split()
    if not words or url.endswith(".json"):
        return url
    frag = q(" ".join(words[:8]), safe="")
    return url.split("#")[0] + "#:~:text=" + frag


def find_quote(text: str, quote: str, near: int | None = None) -> int:
    q = norm(quote)
    hits = [m.start() for m in re.finditer(re.escape(q), text)]
    if not hits:
        raise GroundingError("Quote not found verbatim in the cached source. Copy it exactly from `pipeline.cache grep` output.")
    if near is not None:
        return min(hits, key=lambda h: abs(h - near))
    return hits[0]


def build(ns, path, quote, supports, section="", published="", title="", publisher="", kind=None,
          sourcing=None, value=None, scale_anchor=None, near=None, cites=None, url=None, paywalled=False, pasted=False):
    path = Path(path)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        raise GroundingError(f"No cached file at {path}")
    meta = cache_mod.meta_for(path)
    url = url or meta.get("url")
    if not url:
        raise GroundingError("Cached file has no recorded URL. Pass --url.")
    info = classify_domain(url)
    if info["tier"] is None:
        raise GroundingError(f"Source domain {info['domain']} is not allowed ({info.get('reason')}).")
    if word_count(quote) > MAX_QUOTE_WORDS:
        raise GroundingError(f"Quote has {word_count(quote)} words. The limit is under fifteen.")
    text = doc_text(path)
    loc = find_quote(text, quote, near)
    scale_loc = None
    scale = None
    if scale_anchor:
        idxs = [m.start() for m in re.finditer(re.escape(norm(scale_anchor)), text, re.I) if m.start() <= loc]
        if not idxs:
            raise GroundingError(f"Scale anchor {scale_anchor!r} not found before the quote.")
        scale_loc = idxs[-1]
        scale = table_scale(text[scale_loc: scale_loc + 80])
        if not scale:
            raise GroundingError("Scale anchor found but it does not state thousands, millions or billions.")
    if value is not None:
        window = text[max(0, loc - WINDOW): loc + len(norm(quote)) + WINDOW]
        if not value_in_text(float(value), window, scale):
            raise GroundingError(f"Value {value} does not appear in the quote or within {WINDOW} characters of it (scale {scale}).")
    kind = kind or {"sec": "sec_filing", "company": "company_release", "regulators_courts": "regulator",
                    "rating_agencies": "rating_agency", "lien_registries": "lien_registry",
                    "tier2": "news", "market_data": "market_data"}[info["group"]]
    if kind not in enums()["evidence_kind"]:
        raise GroundingError(f"Unknown kind {kind}")
    sourcing = sourcing or ("filing" if kind == "sec_filing" else "named")
    cache_path, locator, content_hash = path, loc, None
    if info["tier"] == "2":
        # keep only the grounding window; the full article is never stored
        s, e = max(0, loc - WINDOW), min(len(text), loc + len(norm(quote)) + WINDOW)
        win = text[s:e]
        wdir = CACHE / "news"
        wdir.mkdir(parents=True, exist_ok=True)
        import hashlib
        wpath = wdir / (hashlib.sha256((url + norm(quote)).encode()).hexdigest()[:20] + ".txt")
        wpath.write_text(win, encoding="utf-8")
        cache_path, locator = wpath, loc - s
    content_hash = sha256_file(cache_path)
    acc = None
    m = re.search(r"/data/\d+/(\d{10})(\d{2})(\d{6})/", url)
    if m:
        acc = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    rec = {
        "id": _next_id(ns),
        "tier": info["tier"],
        "kind": kind,
        "publisher": publisher or info.get("publisher") or ("SEC EDGAR" if info.get("group") == "sec" else info["domain"]),
        "title": title,
        "url": url,
        "source_link": deep_link(url, quote),
        "accession": acc,
        "section": section,
        "published": published,
        "retrieved": meta.get("retrieved") or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "quote": norm(quote),
        "locator": str(locator),
        "unit_scale_locator": scale_loc,
        "parent_company": info.get("parent_company", publisher or ""),
        "cites_publisher": cites or [],
        "cache_path": str(Path(cache_path).resolve().relative_to(ROOT)),
        "content_hash": content_hash,
        "sourcing": sourcing,
        "paywalled": bool(paywalled),
        "pasted_by_reviewer": bool(pasted),
        "supports": supports or [],
        "grounded_value": float(value) if value is not None else None,
    }
    return rec


def append(ns: str, rec: dict):
    f = EV_DIR / f"{ns}.jsonl"
    with open(EV_DIR / ".lock", "a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        with open(f, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        fcntl.flock(lock, fcntl.LOCK_UN)


def xbrl_record(ns, cik, concept, end, supports, form=None, start=None):
    from . import xbrl
    fact, path = xbrl.fact(cik, concept, end, form=form, start=start)
    if fact is None:
        raise GroundingError(f"No XBRL fact for {concept} at {end}")
    meta = edgar.meta_for(path)
    return {
        "id": _next_id(ns), "tier": "1", "kind": "sec_filing", "publisher": "SEC EDGAR (XBRL company facts)",
        "title": f"{concept} as reported in {fact['form']} {fact.get('fp', '')} {fact.get('fy', '')}".strip(),
        "url": meta.get("url", ""), "accession": fact["accn"], "section": "XBRL fact",
        "published": fact.get("filed", ""), "retrieved": meta.get("retrieved", ""),
        "quote": f"{concept} = {fact['val']}",
        "locator": xbrl.fact_id(concept, fact), "unit_scale_locator": None,
        "parent_company": "SEC", "cites_publisher": [],
        "cache_path": str(Path(path).resolve().relative_to(ROOT)), "content_hash": sha256_file(path),
        "sourcing": "filing", "paywalled": False, "pasted_by_reviewer": False,
        "supports": supports or [], "grounded_value": float(fact["val"]),
    }


def load_ns(ns: str) -> list[dict]:
    f = EV_DIR / f"{ns}.jsonl"
    return [json.loads(l) for l in open(f, encoding="utf-8")] if f.exists() else []


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("add")
    a.add_argument("--ns", required=True); a.add_argument("--path", required=True); a.add_argument("--quote", required=True)
    a.add_argument("--supports", action="append", default=[]); a.add_argument("--section", default=""); a.add_argument("--published", default="")
    a.add_argument("--title", default=""); a.add_argument("--publisher", default=""); a.add_argument("--kind"); a.add_argument("--sourcing")
    a.add_argument("--value", type=float); a.add_argument("--scale-anchor"); a.add_argument("--near", type=int)
    a.add_argument("--cites", action="append", default=[]); a.add_argument("--url"); a.add_argument("--paywalled", action="store_true")
    a = sp.add_parser("xbrl")
    a.add_argument("--ns", required=True); a.add_argument("--cik", required=True); a.add_argument("--concept", required=True)
    a.add_argument("--end", required=True); a.add_argument("--start"); a.add_argument("--form"); a.add_argument("--supports", action="append", default=[])
    a = sp.add_parser("list"); a.add_argument("--ns", required=True)
    args = ap.parse_args(argv)
    try:
        if args.cmd == "add":
            rec = build(args.ns, args.path, args.quote, args.supports, args.section, args.published, args.title, args.publisher,
                        args.kind, args.sourcing, args.value, args.scale_anchor, args.near, args.cites, args.url, args.paywalled)
            append(args.ns, rec)
            print(json.dumps({k: rec[k] for k in ("id", "tier", "kind", "quote", "locator", "cache_path", "grounded_value")}))
        elif args.cmd == "xbrl":
            rec = xbrl_record(args.ns, args.cik, args.concept, args.end, args.supports, args.form, args.start)
            append(args.ns, rec)
            print(json.dumps({k: rec[k] for k in ("id", "quote", "locator", "accession", "published")}))
        elif args.cmd == "list":
            for r in load_ns(args.ns):
                print(r["id"], r["tier"], r["published"], r["quote"][:70], "->", ",".join(r["supports"]))
    except (GroundingError, edgar.SecConfigError, cache_mod.SourceNotAllowed) as e:
        sys.exit("REJECTED: " + str(e))


if __name__ == "__main__":
    main()
