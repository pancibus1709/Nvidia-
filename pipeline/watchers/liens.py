"""New charges and financing statements naming counterparties (spec/11 U1).

  python3 -m pipeline.watchers.liens [--since YYYY-MM-DD]

UK Companies House registers of charges are public and are read for the companies listed in
config/watch_sources.json (companies_house). State UCC search portals need an account or a paid
search, so they are skipped and logged as "manual check needed" once a month.
"""
from __future__ import annotations

import re
import sys
from datetime import datetime

from .. import cache
from ..common import html_to_text
from . import base

NAME = "liens"
LOOKBACK_DAYS = 35
CH = "https://find-and-update.company-information.service.gov.uk"
_CHARGE = re.compile(r'(?s)id="mortgage-heading-\d+"\s+href="(/company/[0-9A-Z]+/charges/[^"]+)"[^>]*>\s*([^<]+?)\s*</a>(.*?)(?=<div class="mortgage-\d+">|\Z)')
_CREATED = re.compile(r'(?s)id="mortgage-created-on-\d+"[^>]*>\s*([^<]+?)\s*<')
_STATUS = re.compile(r'(?s)id="mortgage-status-\d+"[^>]*>(.*?)</dd>')
_PERSONS = re.compile(r'(?s)<ul id="persons-entitled-\d+"[^>]*>(.*?)</ul>')


def parse_charges(page: str) -> list[dict]:
    out = []
    for m in _CHARGE.finditer(page):
        body = m.group(3)
        c = _CREATED.search(body)
        created = None
        if c:
            try:
                created = datetime.strptime(c.group(1).strip(), "%d %B %Y").date().isoformat()
            except ValueError:
                created = None
        s = _STATUS.search(body)
        p = _PERSONS.search(body)
        out.append({"url": CH + m.group(1), "code": m.group(2).strip(), "created": created, "status": html_to_text(s.group(1)) if s else None,
                    "persons_entitled": html_to_text(p.group(1)) if p else None})
    return out


def run(ctx):
    cfg = ctx.paths.cfg("watch_sources.json", {})
    names = {e["id"]: e.get("short_name") or e["name"] for e in ctx.entities()}
    hits, failed, companies = [], 0, cfg.get("companies_house", [])
    for c in companies:
        url = f"{CH}/company/{c['company_number']}/charges"
        try:
            charges = parse_charges(cache.fetch(url, refresh=True, user_agent="Mozilla/5.0").read_text(errors="replace"))
        except cache.SourceNotAllowed:
            raise
        except Exception as err:  # noqa: BLE001
            failed += 1
            ctx.warn(f"Companies House {c['company_number']}: {str(err)[:100]}")
            continue
        for ch in charges:
            if ch["created"] and ch["created"] < ctx.since:
                continue
            hits.append(ctx.hit("charge", ch["url"], entity=c["entity"], entity_name=names.get(c["entity"], c["entity"]), date=ch["created"],
                                source_url=ch["url"], title=f"{names.get(c['entity'], c['entity'])}: {ch['code']}", charge_status=ch["status"],
                                snippet=f"Persons entitled: {ch['persons_entitled']}" if ch["persons_entitled"] else ""))
    for p in cfg.get("ucc_portals", []):
        if p.get("needs_login", True):
            ctx.manual_check(f"{p['state']} UCC search needs a login: search the counterparties by hand at {p['url']}")
    if not companies:
        ctx.manual_check("no Companies House numbers are configured in config/watch_sources.json (companies_house)")
    if companies and failed == len(companies):
        raise base.AllSourcesFailed("Companies House failed for every configured company")
    return hits


if __name__ == "__main__":
    sys.exit(base.cli(sys.modules[__name__]))
