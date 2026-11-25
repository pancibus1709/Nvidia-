"""Earnings dates for Nvidia and each counterparty (spec/11 U1).

  python3 -m pipeline.watchers.earnings_calendar [--since YYYY-MM-DD]

Two sources, both tier 1:
- investor relations event pages listed in config/watch_sources.json (company domains only);
- results releases already filed: a Form 8-K with item 2.02 marks an earnings date.

It also writes data/inbox/_earnings.json with Nvidia's latest and next known earnings dates. The
scheduler reads that file to run nvda_filings hourly for the ten days after each Nvidia earnings date.
Nvidia's next date comes from `nvidia_next_earnings` in config/watch_sources.json when Thomas has entered it.
"""
from __future__ import annotations

import re
import sys
from datetime import date, timedelta

from .. import cache, edgar
from ..common import html_to_text, load_json, save_json
from . import base

NAME = "earnings_calendar"
LOOKBACK_DAYS = 100
_MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
_DATE = re.compile(rf"\b({_MONTHS})\s+(\d{{1,2}}),\s+(20\d\d)\b")
_WORDS = re.compile(r"(?i)earnings|financial results|quarter results|results conference call")


def dates_near_earnings(text: str, today: date) -> list[str]:
    """Future dates written within 200 characters of the word earnings or results."""
    months = _MONTHS.split("|")
    out = set()
    for m in _DATE.finditer(text):
        if not _WORDS.search(text[max(0, m.start() - 200): m.end() + 200]):
            continue
        try:
            d = date(int(m.group(3)), months.index(m.group(1)) + 1, int(m.group(2)))
        except ValueError:
            continue
        if d >= today:
            out.add(d.isoformat())
    return sorted(out)


def run(ctx):
    cfg = ctx.paths.cfg("watch_sources.json", {})
    hits = []
    for page in cfg.get("earnings_pages", []):
        try:
            text = html_to_text(cache.fetch(page["url"], refresh=True).read_text(errors="replace"))
        except cache.SourceNotAllowed:
            raise
        except Exception as err:  # noqa: BLE001
            ctx.manual_check(f"{page['entity']} events page could not be read ({str(err)[:80]}): {page['url']}")
            continue
        for d in dates_near_earnings(text, ctx.today):
            hits.append(ctx.hit("earnings_date", f"{page['entity']}|{d}", entity=page["entity"], date=d, source_url=page["url"],
                                title=f"Upcoming earnings date {d}", upcoming=True))
    ents = [{"id": base.NVIDIA, "short_name": "Nvidia", "cik": edgar.NVIDIA_CIK}] + ctx.counterparties_with_cik()
    nvda_last, failed = None, 0
    for e in ents:
        try:
            rows = [f for f in edgar.list_filings(e["cik"], {"8-K", "8-K/A"}, ctx.since, max_age_hours=12) if "2.02" in (f.get("items") or "")]
        except edgar.SecConfigError:
            raise
        except Exception as err:  # noqa: BLE001
            failed += 1
            ctx.warn(f"{e['short_name']}: {str(err)[:100]}")
            continue
        for f in rows:
            hits.append(ctx.hit("earnings_release", f["accession"], entity=e["id"], entity_name=e["short_name"], cik=f["cik"], form=f["form"],
                                accession=f["accession"], date=f["filed"], source_url=f.get("url"), items=f.get("items"),
                                title=f"{e['short_name']} results release (Form 8-K item 2.02)"))
        if e["id"] == base.NVIDIA and rows:
            nvda_last = max(f["filed"] for f in rows)
    if failed == len(ents):
        raise base.AllSourcesFailed("the SEC submissions endpoint failed for every company")
    state_file = ctx.paths.inbox / "_earnings.json"
    state = load_json(state_file, {})
    if nvda_last and nvda_last > (state.get("nvidia_last") or ""):
        state["nvidia_last"] = nvda_last
    nxt = cfg.get("nvidia_next_earnings")
    upcoming = sorted(h["date"] for h in hits if h["kind"] == "earnings_date" and h["entity"] == base.NVIDIA)
    state["nvidia_next"] = nxt or (upcoming[0] if upcoming else state.get("nvidia_next"))
    if not state.get("nvidia_next") or state["nvidia_next"] < ctx.today.isoformat():
        last = state.get("nvidia_last")
        if not last or date.fromisoformat(last) < ctx.today - timedelta(days=75):
            ctx.manual_check("Nvidia's next earnings date is not known: enter it as nvidia_next_earnings in config/watch_sources.json")
    state["updated"] = ctx.today.isoformat()
    save_json(state_file, state)
    return hits


if __name__ == "__main__":
    sys.exit(base.cli(sys.modules[__name__]))
