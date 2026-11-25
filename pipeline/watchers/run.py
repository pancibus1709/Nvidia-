"""Run one watcher, several, or the ones that are due (spec/11 U1, U5).

  python3 -m pipeline.watchers.run                      every watcher, normal lookback
  python3 -m pipeline.watchers.run --only nvda_filings,ir_releases
  python3 -m pipeline.watchers.run --due                only the watchers the timetable says are due now
  python3 -m pipeline.watchers.run --since 2026-11-25   backfill (Gate Q)
  python3 -m pipeline.watchers.run --status             print data/inbox/_status.json in plain words

Each run is recorded in data/inbox/_status.json: last run, last success, hits, warnings, manual checks
and the count of consecutive failures. Three failures in a row set `alert` for that watcher; the
pending items summary puts those at the top. A failed watcher never stops the others, and it is tried
again at its next scheduled run. Exit code is 0 unless --strict is given and a watcher failed.

The timetable (Eastern time) lives in SCHEDULE below so that one hourly trigger can serve every
frequency: the workflow calls `--due` and this module decides what to run.
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
import traceback
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from ..common import load_json, save_json
from ..update_common import Paths, now_iso
from . import base

WATCHERS = ["earnings_calendar", "nvda_filings", "counterparty_filings", "fulltext_nvidia", "nvda_13f", "ownership_filings",
            "ir_releases", "ratings", "market_values", "liens", "staleness"]
ALERT_AFTER = 3
ET = ZoneInfo("America/New_York")

# every: hours between runs. weekdays: Monday to Friday only. hours: Eastern hours in which a run may start.
# not_before: (hour, minute) Eastern for once-a-day watchers.
SCHEDULE = {
    "earnings_calendar":    {"every": 24 * 7},
    "nvda_filings":         {"every": 2, "weekdays": True, "hours": (6, 22)},      # hourly for ten days after Nvidia earnings
    "counterparty_filings": {"every": 4, "weekdays": True},
    "fulltext_nvidia":      {"every": 24, "not_before": (7, 10)},
    "nvda_13f":             {"every": 24 * 7},                                      # daily for 45 days after each quarter end
    "ownership_filings":    {"every": 24, "not_before": (6, 30)},
    "ir_releases":          {"every": 4},
    "ratings":              {"every": 24, "not_before": (6, 45)},
    "market_values":        {"every": 24, "weekdays": True, "not_before": (16, 30)},
    "liens":                {"every": 24 * 30},
    "staleness":            {"every": 24, "not_before": (6, 0)},
}
SLACK = timedelta(minutes=20)   # a run that starts a little early still counts


def module(name: str):
    if name not in WATCHERS:
        raise SystemExit(f"Unknown watcher {name!r}. Known: {', '.join(WATCHERS)}")
    return importlib.import_module(f"pipeline.watchers.{name}")


def _after_quarter_end(d: date, days: int = 45) -> bool:
    for y in (d.year - 1, d.year):
        for m, last in ((3, 31), (6, 30), (9, 30), (12, 31)):
            q = date(y, m, last)
            if timedelta(0) <= d - q <= timedelta(days=days):
                return True
    return False


def _after_nvidia_earnings(d: date, paths: Paths, days: int = 10) -> bool:
    st = load_json(paths.inbox / "_earnings.json", {})
    for k in ("nvidia_last", "nvidia_next"):
        v = st.get(k)
        if v and timedelta(0) <= d - date.fromisoformat(v) <= timedelta(days=days):
            return True
    return False


def is_due(name: str, now: datetime, status: dict, paths: Paths) -> bool:
    """Whether the timetable in spec/11 U1 says this watcher should run at `now` (any timezone-aware time)."""
    rule = dict(SCHEDULE[name])
    et = now.astimezone(ET)
    if name == "nvda_filings" and _after_nvidia_earnings(et.date(), paths):
        rule["every"] = 1
    if name == "nvda_13f" and _after_quarter_end(et.date()):
        rule["every"] = 24
    if rule.get("weekdays") and et.weekday() >= 5:
        return False
    if "hours" in rule and not (rule["hours"][0] <= et.hour <= rule["hours"][1]):
        return False
    last = (status.get(name) or {}).get("last_run")
    last_dt = datetime.strptime(last, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) if last else None
    if "not_before" in rule:
        if (et.hour, et.minute) < rule["not_before"]:
            return False
        return last_dt is None or last_dt.astimezone(ET).date() < et.date()
    return last_dt is None or now - last_dt >= timedelta(hours=rule["every"]) - SLACK


def due_now(paths: Paths, now: datetime | None = None) -> list[str]:
    now = now or datetime.now(timezone.utc)
    status = load_json(paths.status, {})
    return [w for w in WATCHERS if is_due(w, now, status, paths)]


def run_watchers(names: list[str], since: str | None = None, paths: Paths | None = None, today: date | None = None) -> dict:
    paths = paths or Paths()
    status = load_json(paths.status, {})
    summary = {"ran": [], "failed": [], "new_hits": 0, "alerts": []}
    for name in names:
        st = status.setdefault(name, {"consecutive_failures": 0})
        st["last_run"] = now_iso()
        try:
            res = base.execute(module(name), since, paths, today)
        except Exception as err:  # noqa: BLE001
            st["consecutive_failures"] = st.get("consecutive_failures", 0) + 1
            st["last_error"] = f"{type(err).__name__}: {str(err)[:300]}"
            st["last_error_at"] = st["last_run"]
            summary["failed"].append(name)
            print(f"{name}: FAILED ({st['last_error']}). It will be tried again at the next scheduled run.", file=sys.stderr)
            if not isinstance(err, (RuntimeError, OSError)):
                traceback.print_exc()
        else:
            st.update({"consecutive_failures": 0, "last_ok": st["last_run"], "last_hits": res["hits"], "last_new": res["new"],
                       "warnings": res["warnings"][:20], "manual_checks": res["manual"][:20], "since": res["since"]})
            st.pop("last_error", None)
            summary["ran"].append(name)
            summary["new_hits"] += res["new"]
            print(f"{name}: {res['hits']} hits, {res['new']} new" + (f", {len(res['warnings'])} warnings" if res["warnings"] else "")
                  + (f", {len(res['manual'])} manual checks" if res["manual"] else ""))
        st["alert"] = st.get("consecutive_failures", 0) >= ALERT_AFTER
        if st["alert"]:
            summary["alerts"].append(name)
        paths.inbox.mkdir(parents=True, exist_ok=True)
        save_json(paths.status, status)
    for name in summary["alerts"]:
        print(f"ALERT: {name} has failed {status[name]['consecutive_failures']} times in a row: {status[name].get('last_error')}", file=sys.stderr)
    return summary


def alerts(paths: Paths | None = None) -> list[str]:
    status = load_json((paths or Paths()).status, {})
    return [f"{n} has failed {s.get('consecutive_failures')} times in a row: {s.get('last_error', '')}" for n, s in status.items() if s.get("alert")]


def print_status(paths: Paths) -> None:
    status = load_json(paths.status, {})
    for n in WATCHERS:
        s = status.get(n)
        if not s:
            print(f"{n}: never run")
            continue
        line = f"{n}: last run {s.get('last_run')}, last success {s.get('last_ok', 'never')}, {s.get('last_new', 0)} new hits"
        if s.get("consecutive_failures"):
            line += f", {s['consecutive_failures']} failures in a row ({s.get('last_error')})"
        print(line + ("  ALERT" if s.get("alert") else ""))
        for m in s.get("manual_checks", []):
            print(f"    manual check needed: {m}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="comma-separated watcher names")
    ap.add_argument("--due", action="store_true", help="run only what the timetable says is due now")
    ap.add_argument("--since", help="YYYY-MM-DD for backfill")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any watcher failed")
    args = ap.parse_args(argv)
    paths = Paths()
    if args.status:
        print_status(paths)
        return 0
    if args.since:
        date.fromisoformat(args.since)
    if args.only and args.only not in ("all", "due"):
        names = [n.strip() for n in args.only.split(",") if n.strip()]
        for n in names:
            module(n)
    elif args.due or args.only == "due":
        names = due_now(paths)
        print("Due now: " + (", ".join(names) or "nothing"))
    else:
        names = list(WATCHERS)
    res = run_watchers(names, args.since, paths)
    print(json.dumps({k: v for k, v in res.items()}, indent=None))
    return 1 if (args.strict and res["failed"]) else 0


if __name__ == "__main__":
    sys.exit(main())
