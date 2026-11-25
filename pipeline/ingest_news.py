"""Put hits from the scheduled news task into the inbox (spec/11 U1, last paragraph).

  python3 -m pipeline.ingest_news <hits.jsonl>
  python3 -m pipeline.ingest_news --counterparties      the names the news task searches for

The news task (pipeline/tasks/news_watch.md) cannot write to the repository. It hands over a file of
JSON lines, and ingest_news.yml runs this command inside the shared concurrency group, so the commit
never races another job. Each line needs: url, title, publisher, published (YYYY-MM-DD), and should
carry counterparty, keywords, claim, paywalled and sourcing.

A line is refused, with the reason printed, when its domain is not a tier 2 publication in
config/sources_allowlist.json, when it is not valid JSON, or when a required field is missing.
Accepted lines go to data/inbox/YYYY-MM-DD/news.jsonl with a content hash, so a report already in the
inbox is not added twice. The inbox publishes nothing: every hit still goes through triage and review.
No article text is stored here; `claim` is the task's own one-sentence summary, never a long quotation.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

from .common import classify_domain, word_count
from .update_common import Paths, make_hit, write_hits

REQUIRED = ("url", "title", "publisher", "published")
MAX_LINES = 500


def to_hit(row: dict) -> tuple[dict | None, str | None]:
    missing = [k for k in REQUIRED if not row.get(k)]
    if missing:
        return None, f"missing {', '.join(missing)}"
    url = str(row["url"]).split("#")[0]
    if not url.startswith("https://"):
        return None, "url must start with https://"
    info = classify_domain(url)
    if info.get("tier") != "2":
        return None, f"{info.get('domain')} is not a tier 2 publication ({info.get('reason') or 'tier ' + str(info.get('tier'))})"
    if not re.match(r"\d{4}-\d{2}-\d{2}$", str(row["published"])):
        return None, "published must be YYYY-MM-DD"
    claim = str(row.get("claim") or "")[:600]
    quote = str(row.get("quote") or "")
    if quote and word_count(quote) >= 15:
        quote = ""            # a quote of fifteen words or more is never kept
    ent = row.get("counterparty") if str(row.get("counterparty") or "").startswith("ent_") else None
    return make_hit("news", "news", url, entity=ent, entity_name=row.get("counterparty_name") or row.get("counterparty"),
                    date=row["published"], title=str(row["title"])[:300], source_url=url, publisher=info["publisher"],
                    parent_company=info["parent_company"], snippet=claim, quote=quote, keywords=list(row.get("keywords") or [])[:12],
                    paywalled=bool(row.get("paywalled")), sourcing=row.get("sourcing"), cites_publisher=list(row.get("cites_publisher") or []),
                    search=row.get("search")), None


def ingest(path, paths: Paths | None = None, today: date | None = None) -> dict:
    paths = paths or Paths()
    hits, refused = [], []
    lines = [l for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]
    for n, line in enumerate(lines[:MAX_LINES], 1):
        try:
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError("not an object")
        except ValueError as err:
            refused.append((n, f"not valid JSON: {err}"))
            continue
        hit, why = to_hit(row)
        if hit is None:
            refused.append((n, why))
        else:
            hits.append(hit)
    if len(lines) > MAX_LINES:
        refused.append((MAX_LINES + 1, f"{len(lines) - MAX_LINES} line(s) over the limit of {MAX_LINES} were not read"))
    new = write_hits(paths, "news", hits, today)
    return {"lines": len(lines), "accepted": len(hits), "new": new, "refused": refused}


def counterparties(paths: Paths | None = None) -> list[dict]:
    """Every entity Nvidia has a relationship with: the names the news task searches for."""
    from .common import load_json
    paths = paths or Paths()
    to = {r["to"] for r in load_json(paths.register / "relationships.json", [])}
    return [{"id": e["id"], "name": e.get("short_name") or e["name"], "listed": bool(e.get("public"))}
            for e in load_json(paths.register / "entities.json", []) if e["id"] in to and e["id"] != "ent_nvidia_unattributed"]


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv == ["--counterparties"]:
        for c in counterparties():
            print(f"{c['id']}\t{c['name']}\t{'listed' if c['listed'] else 'private'}")
        return 0
    if len(argv) != 1:
        print(__doc__)
        return 2
    res = ingest(argv[0])
    for n, why in res["refused"]:
        print(f"line {n} refused: {why}")
    print(f"{res['lines']} line(s): {res['accepted']} accepted, {res['new']} new in the inbox, {len(res['refused'])} refused")
    return 0


if __name__ == "__main__":
    sys.exit(main())
