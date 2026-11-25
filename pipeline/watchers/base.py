"""What every watcher shares (spec/11 U1).

A watcher module defines NAME, LOOKBACK_DAYS and run(ctx), which returns a list of raw hits built with
ctx.hit(...). It never writes anything itself: `pipeline.watchers.run` and the module's own command line
both hand the hits to update_common.write_hits, which appends the new ones to
data/inbox/YYYY-MM-DD/<watcher>.jsonl. Watchers never write to data/register or data/published.

SEC pages are read only through pipeline.edgar; every other page only through pipeline.cache, which
refuses a domain that is not in config/sources_allowlist.json.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone

from ..common import load_json
from ..update_common import Paths, make_hit, write_hits

NVIDIA = "ent_nvidia"


@dataclass
class Context:
    name: str
    since: str
    paths: Paths = field(default_factory=Paths)
    today: date = field(default_factory=lambda: datetime.now(timezone.utc).date())
    warnings: list = field(default_factory=list)
    manual: list = field(default_factory=list)

    def hit(self, kind: str, key: str, **fields) -> dict:
        return make_hit(self.name, kind, key, **fields)

    def warn(self, msg: str) -> None:
        """A source that failed while others worked. Shown in the run log and in _status.json."""
        self.warnings.append(msg)
        print(f"  warning: {msg}", file=sys.stderr)

    def manual_check(self, msg: str) -> None:
        """Something a person has to look at because the page needs a login or has no feed."""
        self.manual.append(msg)
        print(f"  manual check needed: {msg}", file=sys.stderr)

    def entities(self) -> list[dict]:
        return load_json(self.paths.register / "entities.json", [])

    def relationships(self) -> list[dict]:
        return load_json(self.paths.register / "relationships.json", [])

    def counterparties_with_cik(self) -> list[dict]:
        seen, out = set(), []
        for e in self.entities():
            cik = (e.get("cik") or "").lstrip("0")
            if cik and e["id"] != NVIDIA and cik not in seen:
                seen.add(cik)
                out.append(e)
        return out


class AllSourcesFailed(RuntimeError):
    """Raised by a watcher when every source it tried was unreachable, so the run counts as a failure."""


def default_since(lookback_days: int, today: date | None = None) -> str:
    return ((today or datetime.now(timezone.utc).date()) - timedelta(days=lookback_days)).isoformat()


def execute(module, since: str | None = None, paths: Paths | None = None, today: date | None = None) -> dict:
    """Run one watcher and write its new hits. Raises whatever the watcher raises."""
    today = today or datetime.now(timezone.utc).date()
    ctx = Context(module.NAME, since or default_since(module.LOOKBACK_DAYS, today), paths or Paths(), today)
    hits = module.run(ctx) or []
    new = write_hits(ctx.paths, module.NAME, hits, today)
    return {"watcher": module.NAME, "since": ctx.since, "hits": len(hits), "new": new, "warnings": ctx.warnings, "manual": ctx.manual}


def cli(module, argv=None) -> int:
    ap = argparse.ArgumentParser(description=module.__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--since", help=f"YYYY-MM-DD for backfill. Default: {module.LOOKBACK_DAYS} days back.")
    args = ap.parse_args(argv)
    if args.since:
        date.fromisoformat(args.since)
    from .run import run_watchers
    res = run_watchers([module.NAME], since=args.since)
    return 1 if res["failed"] else 0
