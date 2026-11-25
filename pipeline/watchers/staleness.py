"""Amounts past their re-verification limit (spec/11 U1 and the staleness rule).

  python3 -m pipeline.watchers.staleness [--since YYYY-MM-DD]

Internal: reads data/register only. Limits come from config/staleness.json and the test is
pipeline.checks.is_stale, the same one the published build uses for the "Not re-verified since" badge.
One hit per amount and last verified date, so an amount is queued once each time it goes stale.
`--since` has no effect.
"""
from __future__ import annotations

import re
import sys

from ..checks import Register, is_stale, iter_amounts, stale_limit_days
from . import base

NAME = "staleness"
LOOKBACK_DAYS = 1
_PREFIX = {"rel_": "relationships", "ent_": "entities", "proj_": "projects", "cx_": "complex_links"}


def diff_path(amount_path: str) -> str:
    """'rel_x.amounts.funded' or 'ent_x.compute_commitments[0].amount' as a diff path."""
    head, _, rest = amount_path.partition(".")
    rest = re.sub(r"\[(\d+)\]", r".\1", rest).replace(".", "/")
    if head == "nvidia_financials":
        return f"nvidia_financials/{rest}"
    for p, coll in _PREFIX.items():
        if head.startswith(p):
            return f"{coll}/{head}/{rest}"
    return f"relationships/{head}/{rest}"


def run(ctx):
    cfg = ctx.paths.cfg("staleness.json")
    reg = Register(ctx.paths.register)
    hits = []
    for path, field, a, owner in iter_amounts(reg):
        if a.get("value") is None or a.get("not_applicable") or not a.get("last_verified"):
            continue
        rel = owner if isinstance(owner, dict) and "amounts" in owner and "status" in owner else None
        if not is_stale(a, rel, cfg, ctx.today):
            continue
        oid = owner.get("id") if isinstance(owner, dict) and owner.get("id") else "nvidia_financials"
        hits.append(ctx.hit("stale_amount", f"{path}|{a['last_verified']}", record=oid, relationship=oid if oid.startswith("rel_") else None,
                            entity=(owner.get("to") if rel else (oid if oid.startswith("ent_") else None)), field=field, amount_path=path,
                            path=diff_path(path), last_verified=a["last_verified"], limit_days=stale_limit_days(rel, cfg), value=a.get("value"),
                            evidence_ids=list(a.get("evidence") or []) + [i for c in a.get("components") or [] for i in c["evidence"]],
                            date=ctx.today.isoformat(), title=f"{path} not re-verified since {a['last_verified']}"))
    return hits


if __name__ == "__main__":
    sys.exit(base.cli(sys.modules[__name__]))
