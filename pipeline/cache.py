"""Document cache for every source, SEC or not.

  python3 -m pipeline.cache fetch <url>                 fetch through the cache, print the cache path
  python3 -m pipeline.cache grep <cache_path> <regex>   find text; prints offset and context (offsets index the text rendering)
  python3 -m pipeline.cache show <cache_path> <offset> [length]
  python3 -m pipeline.cache sections <cache_path>       list note and item headings with offsets

Only allowlisted domains are fetched (config/sources_allowlist.json). SEC URLs go through
pipeline.edgar (declared User-Agent, throttle). Other sources are fetched with a generic
client string. News articles (tier 2) land in research/cache/_tmp/ which is not committed:
only the grounding window around a quote is kept, written by pipeline.evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

from . import edgar
from .common import CACHE, ROOT, classify_domain, doc_text, domain_of, sha256_file

GENERIC_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


class SourceNotAllowed(RuntimeError):
    pass


def path_for(url: str, tier: str) -> Path:
    host = domain_of(url)
    digest = hashlib.sha256(url.encode()).hexdigest()[:16]
    tail = re.sub(r"[^A-Za-z0-9._-]+", "_", url.split("//", 1)[-1].split("/", 1)[-1])[:80] or "index"
    ext = ".json" if tail.endswith(".json") else ".html" if not re.search(r"\.(pdf|txt|htm|html|xml)$", tail) else ""
    base = CACHE / "_tmp" if tier == "2" else CACHE / "web"
    return base / host / f"{digest}_{tail}{ext}"


def fetch(url: str, refresh: bool = False) -> Path:
    info = classify_domain(url)
    if info["tier"] is None:
        raise SourceNotAllowed(f"{info['domain']} is not an allowed source ({info.get('reason')}). See spec/04_SOURCE_POLICY.md.")
    if info.get("group") == "sec":
        return edgar.get(url, max_age_hours=0 if refresh else None)
    path = path_for(url, info["tier"])
    meta = Path(str(path) + ".meta.json")
    if path.exists() and meta.exists() and not refresh:
        return path
    r = requests.get(url, headers={"User-Agent": GENERIC_UA, "Accept-Language": "en-US,en;q=0.9"}, timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code} for {url}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(r.content)
    meta.write_text(json.dumps({
        "url": url, "retrieved": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": 200, "content_hash": sha256_file(path)}, indent=2))
    return path


def meta_for(path) -> dict:
    p = Path(str(path) + ".meta.json")
    return json.loads(p.read_text()) if p.exists() else {}


def grep(path, pattern: str, context: int = 220, limit: int = 40, ignore_case: bool = True):
    text = doc_text(path)
    flags = re.I if ignore_case else 0
    out = []
    for m in re.finditer(pattern, text, flags):
        s, e = max(0, m.start() - context), min(len(text), m.end() + context)
        out.append((m.start(), text[s:e]))
        if len(out) >= limit:
            break
    return out


_HEAD = re.compile(r"(Note \d+\s?[-–—:.]\s?[A-Z][A-Za-z ,&'()/-]{3,70}|Item \d+[A-Z]?\.\s+[A-Z][A-Za-z ,&'()/-]{3,80})")


def sections(path):
    text = doc_text(path)
    return [(m.start(), m.group(1).strip()) for m in _HEAD.finditer(text)]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("fetch"); a.add_argument("url"); a.add_argument("--refresh", action="store_true")
    a = sp.add_parser("grep"); a.add_argument("path"); a.add_argument("pattern"); a.add_argument("-C", type=int, default=220); a.add_argument("--limit", type=int, default=40)
    a = sp.add_parser("show"); a.add_argument("path"); a.add_argument("offset", type=int); a.add_argument("length", type=int, nargs="?", default=1500)
    a = sp.add_parser("sections"); a.add_argument("path")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "fetch":
            p = fetch(args.url, args.refresh)
            print(f"{p.resolve().relative_to(ROOT)}  ({len(doc_text(p)):,} chars of text)")
        elif args.cmd == "grep":
            for off, ctx in grep(args.path, args.pattern, args.C, args.limit):
                print(f"@{off}: ...{ctx}...\n")
        elif args.cmd == "show":
            print(doc_text(args.path)[args.offset: args.offset + args.length])
        elif args.cmd == "sections":
            for off, name in sections(args.path):
                print(f"@{off}: {name}")
    except (SourceNotAllowed, edgar.SecConfigError) as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
