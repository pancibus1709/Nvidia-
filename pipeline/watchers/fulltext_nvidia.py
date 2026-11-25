"""New EDGAR full-text hits for queries Q1 to Q12, kept only when the terms fall within 50 words (spec/11 U1, spec/02 R2).

  python3 -m pipeline.watchers.fulltext_nvidia [--since YYYY-MM-DD]

Reuses the queries, form list and window rule of pipeline.fulltext. The normal run looks back 3 days.
A backfill that overflows the search cap is split into narrower date ranges, as in research.
"""
from __future__ import annotations

import sys

from .. import edgar, fulltext
from ..common import html_to_text
from . import base

NAME = "fulltext_nvidia"
LOOKBACK_DAYS = 3


def run(ctx):
    hits, log, errors, tried = [], [], 0, 0
    end = ctx.today.isoformat()
    by_cik = {(e.get("cik") or "").lstrip("0"): e for e in ctx.entities() if e.get("cik")}
    for qid, variants in fulltext.QUERIES.items():
        for terms in variants:
            q = " ".join(f'"{t}"' for t in terms)
            for h in fulltext.collect(terms, ctx.since, end, log):
                row = edgar.hit_to_row(h)
                if not row["url"] or row["cik"].lstrip("0") == edgar.NVIDIA_CIK.lstrip("0"):
                    continue
                tried += 1
                try:
                    text = html_to_text(edgar.fetch_text(row["url"]))
                except edgar.SecConfigError:
                    raise
                except Exception as err:  # noqa: BLE001
                    errors += 1
                    ctx.warn(f"{row['accession']} {row['file']}: {str(err)[:100]}")
                    continue
                win = fulltext.window_match(text, terms)
                if not win:
                    continue
                ent = by_cik.get(row["cik"].lstrip("0"))
                name = (row["names"] or ["Unknown filer"])[0]
                hits.append(ctx.hit("fulltext", f"{qid}|{q}|{row['accession']}|{row['file']}", qid=qid, query=q,
                                    entity=ent["id"] if ent else None, entity_name=ent["short_name"] if ent else name, cik=row["cik"],
                                    form=row["form"], accession=row["accession"], date=row["filed"], source_url=row["url"],
                                    title=f"{name}: {row['form']} matching {q}", snippet=win, has_money=bool(fulltext.MONEY.search(win))))
    for entry in log:
        if "overflow at minimum" in entry.get("action", ""):
            ctx.warn(f"{entry['query']} {entry['window']}: more hits than the search returns; narrow the dates by hand")
    if tried and errors == tried:
        raise base.AllSourcesFailed("no matching document could be fetched")
    return hits


if __name__ == "__main__":
    sys.exit(base.cli(sys.modules[__name__]))
