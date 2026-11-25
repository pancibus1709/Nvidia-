"""Rating actions on counterparties (spec/11 U1).

  python3 -m pipeline.watchers.ratings [--since YYYY-MM-DD]

Reads only public agency press release pages listed in config/watch_sources.json (rating_pages).
Moody's, S&P Global Ratings and Fitch keep most rating actions behind a login; those pages are skipped
and the rated counterparties are listed as "manual check needed" in data/inbox/_status.json.
A hit is a counterparty name found on a public page: the page text around the name, not a parsed rating.
"""
from __future__ import annotations

import sys

from .. import cache
from ..common import html_to_text
from ..update_common import sha
from . import base

NAME = "ratings"
LOOKBACK_DAYS = 2
AGENCIES = ("Moody's", "S&P Global Ratings", "Fitch")


def rated_entities(ctx) -> list[dict]:
    return [e for e in ctx.entities() if (e.get("credit") or {}).get("public_ratings")]


def run(ctx):
    pages = ctx.paths.cfg("watch_sources.json", {}).get("rating_pages", [])
    rated = rated_entities(ctx)
    names = sorted(e.get("short_name") or e["name"] for e in rated)
    hits, failed = [], 0
    for p in pages:
        try:
            text = html_to_text(cache.fetch(p["url"], refresh=True).read_text(errors="replace"))
        except cache.SourceNotAllowed:
            raise
        except Exception as err:  # noqa: BLE001
            failed += 1
            ctx.manual_check(f"{p['agency']} page needs a login or could not be read ({str(err)[:60]}): {p['url']}")
            continue
        low = text.lower()
        for e in ctx.entities():
            if e["id"] == base.NVIDIA or not any(r.get("to") == e["id"] for r in ctx.relationships()):
                continue
            name = (e.get("short_name") or e["name"]).lower()
            i = low.find(name)
            if len(name) < 4 or i < 0:
                continue
            snippet = text[max(0, i - 200): i + 300]
            hits.append(ctx.hit("rating_page", f"{p['url']}|{e['id']}|{sha(snippet)[:16]}", entity=e["id"], entity_name=e.get("short_name"),
                                agency=p["agency"], date=ctx.today.isoformat(), source_url=p["url"], snippet=snippet,
                                title=f"{p['agency']} page mentions {e.get('short_name')}"))
    covered = {p["agency"] for p in pages}
    for a in AGENCIES:
        if a not in covered and names:
            ctx.manual_check(f"{a}: no public page configured; check rating actions by hand for " + ", ".join(names))
    if pages and failed == len(pages):
        raise base.AllSourcesFailed("every configured rating page failed")
    return hits


if __name__ == "__main__":
    sys.exit(base.cli(sys.modules[__name__]))
