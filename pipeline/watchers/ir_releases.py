"""Nvidia and counterparty releases from each company's own feed (spec/11 U1).

  python3 -m pipeline.watchers.ir_releases [--since YYYY-MM-DD]

Feeds are listed in config/watch_sources.json and fetched through pipeline.cache, so only a company's
own allowlisted domain is ever read. Counterparties with no confirmed feed are reported once per run
as a manual check; a feed is never guessed and a press release distribution site is never substituted.
"""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

from .. import cache
from ..common import html_to_text
from . import base

NAME = "ir_releases"
LOOKBACK_DAYS = 3


def _date(s: str | None) -> str | None:
    if not s:
        return None
    s = s.strip()
    if re.match(r"\d{4}-\d{2}-\d{2}", s):
        return s[:10]
    try:
        return parsedate_to_datetime(s).date().isoformat()
    except (TypeError, ValueError):
        return None


def parse_feed(raw: bytes) -> list[dict]:
    """Items of an RSS or Atom feed: title, link, date, summary."""
    root = ET.fromstring(raw)
    out = []
    for it in root.iter():
        tag = it.tag.split("}")[-1]
        if tag not in ("item", "entry"):
            continue
        g = {}
        for ch in it:
            t = ch.tag.split("}")[-1]
            if t == "link":
                g.setdefault("link", (ch.text or "").strip() or ch.attrib.get("href"))
            elif t in ("title", "pubDate", "published", "updated", "date", "description", "summary"):
                g.setdefault(t, (ch.text or "").strip())
        out.append({"title": g.get("title") or "", "url": g.get("link"), "date": _date(g.get("pubDate") or g.get("published") or g.get("date") or g.get("updated")),
                    "summary": html_to_text(g.get("description") or g.get("summary") or "")[:600]})
    return out


def run(ctx):
    cfg = ctx.paths.cfg("watch_sources.json", {})
    feeds = cfg.get("release_feeds", [])
    names = {e["id"]: e.get("short_name") or e["name"] for e in ctx.entities()}
    hits, failed = [], 0
    for f in feeds:
        try:
            raw = cache.fetch(f["url"], refresh=True).read_bytes()
            items = parse_feed(raw)
        except cache.SourceNotAllowed:
            raise
        except Exception as err:  # noqa: BLE001
            failed += 1
            ctx.warn(f"{f['url']}: {str(err)[:120]}")
            continue
        for it in items:
            if not it["url"] or (it["date"] and it["date"] < ctx.since):
                continue
            if f.get("keep") == "nvidia" and "nvidia" not in (it["title"] + " " + it["summary"]).lower():
                continue
            hits.append(ctx.hit("release", it["url"], entity=f["entity"], entity_name=names.get(f["entity"], f["entity"]), date=it["date"],
                                title=it["title"], source_url=it["url"], snippet=it["summary"]))
    have = {f["entity"] for f in feeds}
    with_site = {e["id"] for e in ctx.entities() if e.get("domains")}
    missing = sorted(n for i, n in names.items() if i not in have and i in with_site and any(r.get("to") == i for r in ctx.relationships()))
    if missing:
        ctx.manual_check(f"no release feed is configured for {len(missing)} counterparties; check their newsrooms by hand: " + ", ".join(missing))
    if feeds and failed == len(feeds):
        raise base.AllSourcesFailed("every configured release feed failed")
    return hits


if __name__ == "__main__":
    sys.exit(base.cli(sys.modules[__name__]))
