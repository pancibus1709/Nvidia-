"""New Nvidia Form 13F-HR filings (spec/11 U1).

  python3 -m pipeline.watchers.nvda_13f [--since YYYY-MM-DD]

Each hit carries the holdings table (issuer, CUSIP, shares, reported value) read by pipeline.thirteenf,
so triage can compare it with the holdings in the register.
"""
from __future__ import annotations

import sys

from .. import edgar, thirteenf
from . import base

NAME = "nvda_13f"
LOOKBACK_DAYS = 14
FORMS = {"13F-HR", "13F-HR/A"}


def run(ctx):
    hits = []
    for f in edgar.list_filings(edgar.NVIDIA_CIK, FORMS, ctx.since, max_age_hours=2):
        holdings, url, cache_path = [], f.get("url"), None
        try:
            rows, table_url, cache_path = thirteenf.info_table(edgar.NVIDIA_CIK, f["accession"])
            url = table_url or url
            merged = {}
            for h in rows:
                m = merged.setdefault(h["cusip"], {"issuer": h["issuer"], "cusip": h["cusip"], "class": h["class"], "shares": 0.0, "value": 0.0})
                m["shares"] += h["shares"]
                m["value"] += h["value"]
            holdings = sorted(merged.values(), key=lambda h: -h["value"])
        except edgar.SecConfigError:
            raise
        except Exception as err:  # noqa: BLE001
            ctx.warn(f"{f['accession']}: holdings table not read ({str(err)[:100]})")
        hits.append(ctx.hit("13f", f["accession"], entity=base.NVIDIA, entity_name="Nvidia", cik=f["cik"], form=f["form"],
                            accession=f["accession"], date=f["filed"], report_date=f["report_date"], source_url=url, cache_path=cache_path,
                            title=f"Nvidia {f['form']} for the quarter ended {f['report_date']}", holdings=holdings))
    return hits


if __name__ == "__main__":
    sys.exit(base.cli(sys.modules[__name__]))
