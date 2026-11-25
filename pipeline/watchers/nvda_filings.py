"""New Nvidia filings, any form (spec/11 U1).

  python3 -m pipeline.watchers.nvda_filings [--since YYYY-MM-DD]

Source: data.sec.gov/submissions/CIK0001045810.json through pipeline.edgar.
Forms that the ownership and 13F watchers handle are left to them.
"""
from __future__ import annotations

import sys

from .. import edgar
from . import base

NAME = "nvda_filings"
LOOKBACK_DAYS = 5
LEFT_TO_OTHERS = ("13F-", "SC 13", "SCHEDULE 13", "3", "4", "5", "144")


def _other(form: str) -> bool:
    return form in ("3", "4", "5", "3/A", "4/A", "5/A", "144", "144/A") or form.startswith(("13F-", "SC 13", "SCHEDULE 13"))


def filing_hit(ctx, f: dict, entity: str, name: str) -> dict:
    return ctx.hit("filing", f["accession"], entity=entity, entity_name=name, cik=f["cik"], form=f["form"], accession=f["accession"],
                   date=f["filed"], report_date=f.get("report_date") or None, items=f.get("items") or "",
                   title=f"{name} {f['form']}" + (f": {f['description']}" if f.get("description") else ""), source_url=f.get("url"))


def run(ctx):
    rows = edgar.list_filings(edgar.NVIDIA_CIK, since=ctx.since, max_age_hours=0.5)
    return [filing_hit(ctx, f, base.NVIDIA, "Nvidia") for f in rows if not _other(f["form"])]


if __name__ == "__main__":
    sys.exit(base.cli(sys.modules[__name__]))
