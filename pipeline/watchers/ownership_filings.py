"""Schedules 13D and 13G and Forms 3 and 4 with Nvidia as filer or subject (spec/11 U1).

  python3 -m pipeline.watchers.ownership_filings [--since YYYY-MM-DD]

Source: Nvidia's submissions list, which holds both what Nvidia files about other companies and what
others file about Nvidia. For Forms 3 and 4 the ownership document is read to tell the two apart:
`role` is "reporting_owner" when Nvidia holds shares in another issuer, and "issuer" when an insider
or holder reports Nvidia's own shares (triage discards those).
"""
from __future__ import annotations

import re
import sys

from .. import edgar
from . import base

NAME = "ownership_filings"
LOOKBACK_DAYS = 5
SCHEDULES = ("SC 13D", "SC 13G", "SCHEDULE 13D", "SCHEDULE 13G")
FORMS34 = ("3", "4", "3/A", "4/A")


def wanted(form: str) -> bool:
    return form in FORMS34 or form.startswith(SCHEDULES)


def issuer_of(cik, accession: str) -> dict:
    """Issuer CIK and name from the ownership XML of a Form 3 or 4."""
    for d in edgar.filing_index(cik, accession):
        if d["name"].lower().endswith(".xml"):
            raw = edgar.get(d["url"]).read_text(errors="replace")
            m = re.search(r"<issuerCik>\s*(\d+)\s*</issuerCik>", raw)
            if m:
                n = re.search(r"<issuerName>\s*([^<]+?)\s*</issuerName>", raw)
                o = re.search(r"<rptOwnerName>\s*([^<]+?)\s*</rptOwnerName>", raw)
                return {"issuer_cik": m.group(1).zfill(10), "issuer_name": n.group(1) if n else None, "owner_name": o.group(1) if o else None, "url": d["url"]}
    return {}


def run(ctx):
    hits = []
    by_cik = {(e.get("cik") or "").lstrip("0"): e for e in ctx.entities() if e.get("cik")}
    for f in edgar.list_filings(edgar.NVIDIA_CIK, since=ctx.since, max_age_hours=2):
        if not wanted(f["form"]):
            continue
        extra = {"role": "schedule"}
        if f["form"] in FORMS34:
            try:
                info = issuer_of(edgar.NVIDIA_CIK, f["accession"])
            except edgar.SecConfigError:
                raise
            except Exception as err:  # noqa: BLE001
                info = {}
                ctx.warn(f"{f['accession']}: ownership document not read ({str(err)[:100]})")
            is_nvda = (info.get("issuer_cik") or "").lstrip("0") == edgar.NVIDIA_CIK.lstrip("0")
            ent = by_cik.get((info.get("issuer_cik") or "").lstrip("0"))
            extra = {"role": "issuer" if is_nvda else ("reporting_owner" if info else "unknown"), "issuer_cik": info.get("issuer_cik"),
                     "issuer_name": info.get("issuer_name"), "owner_name": info.get("owner_name"),
                     "counterparty": ent["id"] if ent and not is_nvda else None}
        hits.append(ctx.hit("ownership", f["accession"], entity=base.NVIDIA, entity_name="Nvidia", cik=f["cik"], form=f["form"],
                            accession=f["accession"], date=f["filed"], source_url=f.get("url"),
                            title=f"{f['form']} on Nvidia's filing list" + (f": {f['description']}" if f.get("description") else ""), **extra))
    return hits


if __name__ == "__main__":
    sys.exit(base.cli(sys.modules[__name__]))
