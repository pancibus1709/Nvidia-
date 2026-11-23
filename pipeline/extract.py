"""Filing section extraction and filing-over-filing comparison.

  python3 -m pipeline.extract notes <cache_path>                    list note headings with offsets
  python3 -m pipeline.extract section <cache_path> "<heading regex>" [--max 20000]
  python3 -m pipeline.extract riskdiff <older cache_path> <newer cache_path> [--min-words 8]
       sentences in the newer filing's risk factors that are absent from the older one
  python3 -m pipeline.extract exhibits --cik <cik> --accession <acc>   list exhibits (credit agreements, indentures) in a filing
"""
from __future__ import annotations

import argparse
import re

from . import edgar
from .common import doc_text

_NOTE = re.compile(r"Note \d+\s?[-–—:.]\s?[A-Z][A-Za-z ,&'()/-]{3,70}")
_SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")


def notes(path):
    text = doc_text(path)
    seen, out = set(), []
    for m in _NOTE.finditer(text):
        name = m.group(0).strip()
        out.append((m.start(), name, name in seen))
        seen.add(name)
    return out


def section(path, heading: str, max_chars: int = 20000, occurrence: int = -1) -> tuple[int, str]:
    """Text from a heading to the next note heading. The last occurrence is used by default (the first is usually the table of contents)."""
    text = doc_text(path)
    hits = [m.start() for m in re.finditer(heading, text)]
    if not hits:
        return -1, ""
    start = hits[occurrence]
    nxt = _NOTE.search(text, start + 40)
    end = min(nxt.start() if nxt else len(text), start + max_chars)
    return start, text[start:end]


def risk_factors(path) -> str:
    text = doc_text(path)
    starts = [m.start() for m in re.finditer(r"Item 1A\.?\s+Risk Factors", text, re.I)]
    if not starts:
        return ""
    best = ""
    for s in starts:
        m = re.search(r"Item (1B|2)\.?\s+(Unresolved|Properties|Unregistered|Cybersecurity)", text[s + 50:], re.I)
        chunk = text[s: s + 50 + m.start()] if m else text[s: s + 400000]
        if len(chunk) > len(best):
            best = chunk
    return best


def _key(sentence: str) -> str:
    return re.sub(r"[^a-z]+", " ", sentence.lower()).strip()


def risk_diff(old_path, new_path, min_words: int = 8) -> list[str]:
    old = {_key(s) for s in _SENT.split(risk_factors(old_path))}
    out = []
    for s in _SENT.split(risk_factors(new_path)):
        if len(s.split()) >= min_words and _key(s) not in old:
            out.append(s.strip())
    return out


def exhibits(cik, accession):
    return [d for d in edgar.filing_index(cik, accession) if re.search(r"(?i)ex[-_]?\d|exhibit", d["name"])]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("notes"); a.add_argument("path")
    a = sp.add_parser("section"); a.add_argument("path"); a.add_argument("heading"); a.add_argument("--max", type=int, default=20000)
    a = sp.add_parser("riskdiff"); a.add_argument("old"); a.add_argument("new"); a.add_argument("--min-words", type=int, default=8); a.add_argument("--grep")
    a = sp.add_parser("exhibits"); a.add_argument("--cik", required=True); a.add_argument("--accession", required=True)
    args = ap.parse_args(argv)
    if args.cmd == "notes":
        for off, name, dup in notes(args.path):
            print(f"@{off}: {name}{'  (repeat)' if dup else ''}")
    elif args.cmd == "section":
        off, txt = section(args.path, args.heading, args.max)
        print(f"@{off}\n{txt}")
    elif args.cmd == "riskdiff":
        for s in risk_diff(args.old, args.new, args.min_words):
            if not args.grep or re.search(args.grep, s, re.I):
                print("+ " + s + "\n")
    elif args.cmd == "exhibits":
        for d in exhibits(args.cik, args.accession):
            print(f"{d['size']:>10}  {d['name']:<50} {d['url']}")


if __name__ == "__main__":
    main()
