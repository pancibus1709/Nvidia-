"""Shared pieces of the continuous update loop (spec/11): paths, the inbox, the queue, the diff format.

A diff is a list of changes: {"path": "relationships/rel_x/amounts/funded/value", "old": <value now>, "new": <proposed>}.
The first path segment is a register collection, the second a record id, the rest keys or list indexes.
A path that stops at the record id adds a whole record (old null) or removes one (new null).

Every function takes a Paths object, so tests point the whole loop at a temporary directory.
"""
from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path

from .common import ROOT, load_json, save_json

LIST_COLLECTIONS = ("relationships", "entities", "projects", "events", "complex_links", "evidence")
DICT_COLLECTIONS = ("nvidia_financials", "central_bank")
HUMAN_AMOUNT_FIELDS = ("headline", "committed_total", "funded", "contingent_max")
HUMAN_CHANGE_TYPES = ("added", "status_changed", "reconciliation_changed", "dates_changed", "corrected", "reverified",
                      "amount_changed", "evidence_added", "removed_from_display")


@dataclass
class Paths:
    root: Path = ROOT

    def __post_init__(self):
        self.root = Path(self.root)

    @property
    def inbox(self): return self.root / "data" / "inbox"
    @property
    def queue(self): return self.root / "data" / "queue"
    @property
    def approved(self): return self.root / "data" / "approved"
    @property
    def applied(self): return self.root / "data" / "approved" / "_applied"
    @property
    def rejected(self): return self.root / "data" / "queue" / "_rejected"
    @property
    def register(self): return self.root / "data" / "register"
    @property
    def published(self): return self.root / "data" / "published"
    @property
    def changelog(self): return self.root / "data" / "changelog.json"
    @property
    def drafts(self): return self.root / "research" / "drafts"
    @property
    def evidence_dir(self): return self.root / "research" / "evidence"
    @property
    def config(self): return self.root / "config"
    @property
    def status(self): return self.inbox / "_status.json"
    @property
    def triaged(self): return self.inbox / "_triaged.jsonl"

    def cfg(self, name: str, default=None):
        """A config file from this root, falling back to the repository's own copy."""
        f = self.config / name
        if f.exists():
            return load_json(f)
        f = ROOT / "config" / name
        if f.exists():
            return load_json(f)
        if default is not None:
            return default
        raise FileNotFoundError(name)


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha(*parts) -> str:
    h = hashlib.sha256()
    for p in parts:
        h.update((p if isinstance(p, str) else json.dumps(p, sort_keys=True, ensure_ascii=False)).encode("utf-8"))
        h.update(b"\x1f")
    return h.hexdigest()


def read_jsonl(path) -> list[dict]:
    path = Path(path)
    if not path.exists():
        return []
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def append_jsonl(path, rows) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


# ---------------------------------------------------------------- inbox

def make_hit(watcher: str, kind: str, key: str, **fields) -> dict:
    """A raw hit. `key` is what makes the hit the same hit next time (accession number, URL, item plus date)."""
    return {"hash": sha(watcher, kind, key), "watcher": watcher, "kind": kind, "key": key, **fields}


def seen_hashes(paths: Paths, watcher: str | None = None) -> set[str]:
    out = set()
    if not paths.inbox.exists():
        return out
    for f in paths.inbox.glob("*/*.jsonl"):
        if watcher and f.stem != watcher:
            continue
        for r in read_jsonl(f):
            out.add(r.get("hash"))
    return out


def write_hits(paths: Paths, watcher: str, hits: list[dict], today: date | None = None) -> int:
    """Append new hits to data/inbox/YYYY-MM-DD/<watcher>.jsonl. A hash already in the inbox is skipped."""
    seen = seen_hashes(paths, watcher)
    day = (today or datetime.now(timezone.utc).date()).isoformat()
    new, stamp = [], now_iso()
    for h in hits:
        if h["hash"] in seen:
            continue
        seen.add(h["hash"])
        new.append({**h, "found_at": h.get("found_at") or stamp})
    if new:
        append_jsonl(paths.inbox / day / f"{watcher}.jsonl", new)
    return len(new)


def inbox_hits(paths: Paths) -> list[dict]:
    out = []
    if not paths.inbox.exists():
        return out
    for f in sorted(paths.inbox.glob("*/*.jsonl")):
        for r in read_jsonl(f):
            r.setdefault("watcher", f.stem)
            r["_inbox_file"] = str(f.relative_to(paths.root))
            out.append(r)
    return out


# ---------------------------------------------------------------- register access for diffs

def load_collections(directory) -> dict:
    d = Path(directory)
    out = {}
    for name in LIST_COLLECTIONS:
        out[name] = load_json(d / f"{name}.json", [])
    for name in DICT_COLLECTIONS:
        out[name] = load_json(d / f"{name}.json", {})
    return out


class DiffError(ValueError):
    pass


def split_path(path: str) -> list[str]:
    parts = [p for p in path.strip("/").split("/") if p != ""]
    if not parts or parts[0] not in LIST_COLLECTIONS + DICT_COLLECTIONS:
        raise DiffError(f"path {path!r} does not start with a register collection")
    return parts


def _record(coll, rid):
    for row in coll:
        if row.get("id") == rid:
            return row
    return None


def _step(node, key):
    if isinstance(node, list):
        try:
            return node[int(key)]
        except (ValueError, IndexError):
            raise KeyError(key)
    if isinstance(node, dict):
        return node[key]
    raise KeyError(key)


def get_path(data: dict, path: str):
    """Value at a diff path, or None if any step is absent."""
    parts = split_path(path)
    node = data.get(parts[0])
    rest = parts[1:]
    if parts[0] in LIST_COLLECTIONS:
        if not rest:
            return node
        node = _record(node or [], rest[0])
        rest = rest[1:]
    try:
        for k in rest:
            node = _step(node, k)
    except (KeyError, TypeError):
        return None
    return node


def set_path(data: dict, path: str, new) -> None:
    """Apply one change in place. Missing dictionaries along the way are created; list indexes must exist or be the next one."""
    parts = split_path(path)
    coll = data.setdefault(parts[0], [] if parts[0] in LIST_COLLECTIONS else {})
    rest = parts[1:]
    if parts[0] in LIST_COLLECTIONS:
        if not rest:
            raise DiffError(f"path {path!r} names a whole collection")
        rec = _record(coll, rest[0])
        if len(rest) == 1:
            if new is None:
                if rec is None:
                    raise DiffError(f"{path}: no such record to remove")
                coll.remove(rec)
            elif rec is None:
                if not isinstance(new, dict) or new.get("id") != rest[0]:
                    raise DiffError(f"{path}: a new record must be an object whose id matches the path")
                coll.append(new)
            else:
                rec.clear()
                rec.update(new)
            return
        if rec is None:
            raise DiffError(f"{path}: record {rest[0]} does not exist")
        node, rest = rec, rest[1:]
    else:
        node = coll
        if not rest:
            raise DiffError(f"path {path!r} names a whole file")
    for k in rest[:-1]:
        if isinstance(node, dict):
            node = node.setdefault(k, {})
        else:
            try:
                node = node[int(k)]
            except (ValueError, IndexError, TypeError):
                raise DiffError(f"{path}: cannot step into {k!r}")
    last = rest[-1]
    if isinstance(node, list):
        i = int(last)
        if i == len(node):
            node.append(new)
        elif 0 <= i < len(node):
            node[i] = new
        else:
            raise DiffError(f"{path}: list index {i} out of range")
    elif isinstance(node, dict):
        if new is None and last not in node:
            return
        node[last] = new
    else:
        raise DiffError(f"{path}: parent is not a container")


def apply_diff(data: dict, diff: list[dict], check_old: bool = True) -> dict:
    """A patched deep copy. With check_old, a change whose `old` no longer matches the data is refused."""
    out = copy.deepcopy(data)
    for ch in diff:
        if check_old and get_path(out, ch["path"]) != ch.get("old"):
            raise DiffError(f"{ch['path']}: the register no longer holds the value this change was drafted against "
                            f"(expected {json.dumps(ch.get('old'))[:80]}, found {json.dumps(get_path(out, ch['path']))[:80]})")
        set_path(out, ch["path"], copy.deepcopy(ch.get("new")))
    return out


def subject_of(path: str) -> tuple[str, str | None]:
    """(collection, record id) a diff path belongs to."""
    parts = split_path(path)
    return parts[0], (parts[1] if parts[0] in LIST_COLLECTIONS and len(parts) > 1 else None)


def amount_field_of(path: str) -> str | None:
    """'funded' for relationships/rel_x/amounts/funded/value. None if the path is not inside an amount."""
    parts = path.strip("/").split("/")
    if "amounts" in parts:
        i = parts.index("amounts")
        if len(parts) > i + 1:
            return parts[i + 1]
    return None


def touched_amounts(diff: list[dict]) -> list[str]:
    """Paths of the amount objects a diff touches: the ones a person approving it has re-checked."""
    out = []
    for ch in diff:
        parts = ch["path"].strip("/").split("/")
        if amount_field_of(ch["path"]):
            p = "/".join(parts[: parts.index("amounts") + 2])
        elif parts[-1] in ("last_verified", "value") and len(parts) > 2:
            p = "/".join(parts[:-1])
        else:
            continue
        if p not in out:
            out.append(p)
    return out


# ---------------------------------------------------------------- approval rule (spec/11 U3)

def needs_human(item: dict, auto_cfg: dict) -> tuple[bool, str]:
    """Whether a queue item must be approved by a person, and why. Only market_value and link_repair can pass without one."""
    ct = item.get("change_type")
    auto = set(auto_cfg.get("auto", []))
    if ct not in auto:
        return True, f"change type {ct or 'not set'} always needs a person"
    if item.get("state") != "ready":
        return True, f"item is {item.get('state')}, not ready"
    if not item.get("diff"):
        return True, "no proposed change"
    if any(c.get("result") == "fail" for c in item.get("checks", [])):
        return True, "a check failed"
    for ch in item["diff"]:
        parts = ch["path"].strip("/").split("/")
        field = amount_field_of(ch["path"])
        if ct == "market_value":
            ok = (field == "market_value") or (parts[0] == "evidence" and len(parts) == 2 and ch.get("old") is None)
            if not ok:
                return True, f"a market value update may only touch market_value: {ch['path']}"
            if field == "market_value" and parts[-1] in ("market_value", "value") and ch.get("old") is None:
                return True, "a first market value needs a person to check and date it"
            if parts[-1] == "last_verified":
                return True, "an automatic change never sets last_verified"
        elif ct == "link_repair":
            if not (parts[0] == "evidence" and parts[-1] in ("url", "source_link", "link_status")):
                return True, f"a link repair may only touch an evidence link: {ch['path']}"
        if field in HUMAN_AMOUNT_FIELDS:
            return True, f"{field} changes at any size need a person"
    return False, f"auto rule: {ct}"


# ---------------------------------------------------------------- queue

def queue_items(paths: Paths, include_held: bool = True) -> list[dict]:
    out = []
    if not paths.queue.exists():
        return out
    for f in sorted(paths.queue.glob("*.json")):
        if f.name.startswith("_"):
            continue            # _spend.json and other bookkeeping files are not queue items
        it = load_json(f)
        if not include_held and it.get("state") == "hold":
            continue
        out.append(it)
    return out


def save_item(directory, item: dict) -> Path:
    f = Path(directory) / f"{item['id']}.json"
    save_json(f, item)
    return f
