"""New filings by every counterparty that has a CIK (spec/11 U1).

  python3 -m pipeline.watchers.counterparty_filings [--since YYYY-MM-DD]

CIKs come from data/register/entities.json. Source: the SEC submissions endpoint per CIK, through
pipeline.edgar. Only forms that can carry a deal, a debt document or an ownership change are kept;
routine paper (insider Forms 4, structured note supplements from the banks, fund reports) is not.
"""
from __future__ import annotations

import sys

from .. import edgar
from . import base
from .nvda_filings import filing_hit

NAME = "counterparty_filings"
LOOKBACK_DAYS = 5
KEEP = {"10-K", "10-Q", "8-K", "S-1", "F-1", "424B4", "424B5", "424B1", "424B3", "20-F", "6-K", "40-F", "DEF 14A", "DEFM14A",
        "S-4", "F-4", "10-12B", "S-11", "SC 13D", "SC 13G", "SCHEDULE 13D", "SCHEDULE 13G", "8-K12B", "NT 10-K", "NT 10-Q", "15-12B", "25"}


def keep(form: str) -> bool:
    return form in KEEP or (form.endswith("/A") and form[:-2] in KEEP)


def run(ctx):
    hits, failed, ents = [], 0, ctx.counterparties_with_cik()
    for e in ents:
        try:
            rows = edgar.list_filings(e["cik"], since=ctx.since, max_age_hours=2)
        except edgar.SecConfigError:
            raise
        except Exception as err:  # noqa: BLE001
            failed += 1
            ctx.warn(f"{e['short_name']} (CIK {e['cik']}): {str(err)[:120]}")
            continue
        hits += [filing_hit(ctx, f, e["id"], e.get("short_name") or e["name"]) for f in rows if keep(f["form"])]
    if ents and failed == len(ents):
        raise base.AllSourcesFailed(f"the SEC submissions endpoint failed for all {failed} counterparties")
    return hits


if __name__ == "__main__":
    sys.exit(base.cli(sys.modules[__name__]))
