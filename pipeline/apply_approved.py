"""Apply approved changes and publish (spec/11 U4).

  python3 -m pipeline.apply_approved                 apply data/approved/*.json, then rebuild and publish
  python3 -m pipeline.apply_approved --dry-run       check every approved item against the register; write nothing
  python3 -m pipeline.apply_approved --no-publish    apply only (used by tests and by hand when the site must wait)
  python3 -m pipeline.apply_approved --publish-anyway   run the publish steps even when nothing is approved

For each approved item, in order of approval:
1. Refuse it unless its approval is valid: a person's name on anything the auto rule does not cover.
2. Make sure every new source is in the cache (fetching it if it is not) and run every check on the
   proposed change again, against the register as it stands now. One failure stops the whole run.
3. Apply the diff. Records that are assembled from research drafts are changed in the draft that
   holds them (research/drafts/), so `pipeline.build_register` reproduces the change; new records go to
   research/drafts/cluster_updates.json or complex_updates.json. New evidence goes to
   research/evidence/upd.jsonl. Other files are changed in data/register/.
4. Increment `version` on each changed record. Set `last_verified` only on the amounts the approver
   re-checked. An automatic change never touches `last_verified`.
5. Append one entry per changed field to data/changelog.json and move the item to data/approved/_applied/.

Then run, in order: pipeline.build_register, pipeline.system_view, pipeline.publish, pipeline.build_site.
The first failure stops the run. Everything this run changed is put back (register, drafts, evidence,
change log, approved items, data/published, site), so the live site keeps showing the last good publish.
"""
from __future__ import annotations

import argparse
import copy
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path

from . import triage
from .common import ROOT, load_json, save_json
from .update_common import (DICT_COLLECTIONS, DiffError, LIST_COLLECTIONS, Paths, amount_field_of, append_jsonl, get_path, load_collections,
                            needs_human, now_iso, read_jsonl, save_item, set_path, subject_of)

STEPS = ["pipeline.build_register", "pipeline.system_view", "pipeline.publish", "pipeline.build_site"]
EVIDENCE_NS = "upd"
DRAFT_COLLECTIONS = ("relationships", "entities", "projects", "events", "complex_links")


class Blocked(RuntimeError):
    """An approved item that must not be applied. Carries the item id and the reason."""

    def __init__(self, item_id: str, reason: str):
        super().__init__(f"{item_id}: {reason}")
        self.item_id, self.reason = item_id, reason


# ---------------------------------------------------------------- validation

def check_approval(item: dict, paths: Paths) -> None:
    ap = item.get("approval_record") or {}
    if not ap.get("at") or ap.get("mode") not in ("human", "auto"):
        raise Blocked(item["id"], "no approval record")
    human, why = needs_human({**item, "state": "ready"}, paths.cfg("auto_approve.json", {"auto": []}))
    if ap["mode"] == "auto":
        if human:
            raise Blocked(item["id"], f"approved by rule but it needs a person: {why}")
        if any(ch["path"].endswith("/last_verified") for ch in item.get("diff", [])) or ap.get("rechecked"):
            raise Blocked(item["id"], "an automatic change may not set last_verified")
    elif not ap.get("by"):
        raise Blocked(item["id"], "approved without a name")
    if not item.get("diff"):
        raise Blocked(item["id"], "nothing to apply: the diff is empty")


def fetch_source(url: str) -> Path:
    """Fetch a source through the cache. Separate so tests can make a source unreachable."""
    from . import cache
    return cache.fetch(url)


def ensure_sources(item: dict, paths: Paths) -> None:
    """Every new evidence record must point at a cached file that exists. A missing one is fetched; failure blocks the item."""
    for ev in item.get("evidence") or []:
        target = paths.root / ev["cache_path"]
        if target.exists() or (ROOT / ev["cache_path"]).exists():
            continue
        if ev.get("tier") == "2":
            raise Blocked(item["id"], f"source unreachable: the grounding window {ev['cache_path']} is missing and news is never fetched again")
        try:
            got = fetch_source(ev["url"])
        except Exception as err:  # noqa: BLE001
            raise Blocked(item["id"], f"source unreachable: {ev['url']} ({type(err).__name__}: {str(err)[:120]})")
        if Path(got).resolve() != target.resolve():
            raise Blocked(item["id"], f"source unreachable: {ev['url']} was fetched but not to {ev['cache_path']}")


def with_verification(item: dict) -> list[dict]:
    """The diff as it will be applied: last_verified set on the amounts the approver re-checked."""
    ap = item["approval_record"]
    diff = copy.deepcopy(item["diff"])
    if ap["mode"] != "human":
        return diff
    day = ap["at"][:10]
    for ch in diff:
        if ch["path"].endswith("/last_verified") and ch.get("new") is not None:
            ch["new"] = day          # the date a person confirmed it, not the date triage drafted it
    touched = {ch["path"] for ch in diff}
    for amount_path in ap.get("rechecked") or []:
        whole = next((ch for ch in diff if ch["path"] == amount_path and isinstance(ch.get("new"), dict)), None)
        if whole is not None:
            whole["new"]["last_verified"] = day
        elif f"{amount_path}/last_verified" not in touched:
            diff.append({"path": f"{amount_path}/last_verified", "old": "__current__", "new": day})
    return diff


def prepare(item: dict, paths: Paths, data: dict, today: date | None) -> dict:
    """Validate one approved item against `data`. Returns the item with the diff as it will be applied."""
    check_approval(item, paths)
    ensure_sources(item, paths)
    ready = copy.deepcopy(item)
    ready["diff"] = with_verification(item)
    for ch in ready["diff"]:
        if ch.get("old") == "__current__":
            ch["old"] = get_path(data, ch["path"])
    results = triage.evaluate(ready, paths, today, data)
    failed = [r for r in results if r["result"] == "fail"]
    if failed:
        raise Blocked(item["id"], "; ".join(f"{r['check']} failure: {r['detail']}" for r in failed)[:1500])
    return ready


# ---------------------------------------------------------------- writing

def _next_evidence_ids(paths: Paths, data: dict, n: int) -> list[str]:
    if n == 0:
        return []
    used = {int(e["id"].split("_")[1]) for e in data["evidence"] if str(e.get("id", "")).startswith("ev_")}
    if paths.evidence_dir.exists():
        reg = paths.evidence_dir / "_namespaces.json"
        ns = load_json(reg, {})
        if EVIDENCE_NS not in ns:
            ns[EVIDENCE_NS] = (max(ns.values()) + 10000) if ns else 10000
            reg.write_text(json.dumps(ns, indent=2))
        nxt = ns[EVIDENCE_NS] + len(read_jsonl(paths.evidence_dir / f"{EVIDENCE_NS}.jsonl")) + 1
    else:
        nxt = max(used, default=0) + 1
    out = []
    while len(out) < n:
        if nxt not in used:
            out.append(f"ev_{nxt}")
        nxt += 1
    return out


def draft_files(paths: Paths) -> list[Path]:
    """Drafts in the order pipeline.build_register reads them."""
    d = paths.drafts
    if not d.exists():
        return []
    return sorted(d.glob("cluster_*.json")) + sorted(d.glob("lead_*.json")) + sorted(d.glob("complex_*.json"))


class Writer:
    """Applies changes to the register and to the research drafts that the register is built from."""

    def __init__(self, paths: Paths):
        self.paths = paths
        self.data = load_collections(paths.register)
        self.dirty: set = set()
        self.drafts = {f: load_json(f) for f in draft_files(paths)}
        self.dirty_drafts: set = set()
        self.financials_draft = paths.drafts / "nvidia_financials.json"
        self.notes: list[str] = []

    def _draft_targets(self, coll: str, rid: str) -> list[Path]:
        hits = [f for f, d in self.drafts.items() if any(r.get("id") == rid for r in d.get(coll, []))]
        if coll == "entities":
            return hits            # an entity is merged from every draft that carries it
        return hits[:1]            # build_register keeps the first copy of any other record

    def change(self, ch: dict) -> None:
        coll, rid = subject_of(ch["path"])
        set_path(self.data, ch["path"], copy.deepcopy(ch.get("new")))
        self.dirty.add(coll)
        if coll in DRAFT_COLLECTIONS and self.paths.drafts.exists():
            whole = len(ch["path"].strip("/").split("/")) == 2
            targets = self._draft_targets(coll, rid)
            if not targets and whole and ch.get("new") is not None:
                f = self.paths.drafts / ("complex_updates.json" if coll == "complex_links" else "cluster_updates.json")
                self.drafts.setdefault(f, {"entities": [], "relationships": [], "projects": [], "events": [], "complex_links": []})
                self.drafts[f].setdefault(coll, [])
                targets = [f]
            if not targets:
                self.notes.append(f"{ch['path']}: no research draft holds {rid}; changed in data/register only, which build_register may overwrite")
            for f in targets:
                try:
                    set_path(self.drafts[f], ch["path"], copy.deepcopy(ch.get("new")))
                    self.dirty_drafts.add(f)
                except DiffError:
                    if coll != "entities":
                        raise
        elif coll == "nvidia_financials" and self.financials_draft.exists():
            d = self.drafts.setdefault(self.financials_draft, {"nvidia_financials": load_json(self.financials_draft)})
            set_path(d, ch["path"], copy.deepcopy(ch.get("new")))
            self.dirty_drafts.add(self.financials_draft)
        elif coll == "evidence" and self.paths.evidence_dir.exists():
            self._patch_evidence_line(rid)

    def _patch_evidence_line(self, rid: str) -> None:
        rec = next((e for e in self.data["evidence"] if e["id"] == rid), None)
        for f in sorted(self.paths.evidence_dir.glob("*.jsonl")):
            rows = read_jsonl(f)
            if any(r.get("id") == rid for r in rows):
                rows = [rec if r.get("id") == rid else r for r in rows if not (r.get("id") == rid and rec is None)]
                f.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
                return

    def bump(self, coll: str, rid: str) -> None:
        for store in [self.data] + [self.drafts[f] for f in self._draft_targets(coll, rid)]:
            rec = next((r for r in store.get(coll, []) if r.get("id") == rid), None)
            if rec is not None and (coll == "relationships" or "version" in rec):
                rec["version"] = int(rec.get("version") or 0) + 1
        self.dirty.add(coll)
        self.dirty_drafts.update(self._draft_targets(coll, rid))

    def add_evidence(self, records: list[dict]) -> None:
        if not records:
            return
        self.data["evidence"] += records
        self.dirty.add("evidence")
        if self.paths.evidence_dir.exists():
            # records the extraction job made with `pipeline.evidence add` are already in research/evidence/
            have = {r.get("id") for f in self.paths.evidence_dir.glob("*.jsonl") for r in read_jsonl(f)}
            append_jsonl(self.paths.evidence_dir / f"{EVIDENCE_NS}.jsonl", [r for r in records if r["id"] not in have])

    def save(self) -> None:
        for coll in sorted(self.dirty):
            save_json(self.paths.register / f"{coll}.json", self.data[coll])
        for f in sorted(self.dirty_drafts):
            save_json(f, self.drafts[f]["nvidia_financials"] if f == self.financials_draft else self.drafts[f])


def changelog_entries(item: dict, diff: list[dict], before: dict, after: dict, new_ev_ids: list[str]) -> list[dict]:
    """One entry per changed amount or field. Changes inside one amount collapse into a single line."""
    ap = item["approval_record"]
    base = {"timestamp": ap.get("applied_at") or now_iso(), "change_type": item["change_type"],
            "approved_by": ap.get("by") if ap["mode"] == "human" else None, "auto_rule": ap.get("rule") if ap["mode"] == "auto" else None,
            "queue_id": item["id"]}
    out, seen = [], set()
    for ch in diff:
        coll, rid = subject_of(ch["path"])
        if coll == "evidence" and item["change_type"] != "link_repair":
            continue
        parts = ch["path"].strip("/").split("/")
        rest = parts[2:] if coll in LIST_COLLECTIONS else parts[1:]
        field = amount_field_of(ch["path"])
        if field:
            i = parts.index("amounts")
            amount_path = "/".join(parts[: i + 2])
            if amount_path in seen:
                continue
            seen.add(amount_path)
            old_a, new_a = get_path(before, amount_path) or {}, get_path(after, amount_path) or {}
            key = "value" if old_a.get("value") != new_a.get("value") else ("last_verified" if old_a.get("last_verified") != new_a.get("last_verified") else None)
            old_v, new_v = (old_a.get(key), new_a.get(key)) if key else (ch.get("old"), ch.get("new"))
            ev = [e for e in (new_a.get("evidence") or []) if isinstance(e, str)][:5]
            out.append({**base, "relationship": rid or coll, "field": "amounts." + field, "old": old_v, "new": new_v, "evidence": ev or new_ev_ids[:5]})
        elif not rest:
            new = ch.get("new")
            label = (new or {}).get("title") or (new or {}).get("name") or (new or {}).get("summary") or (new or {}).get("instrument") if isinstance(new, dict) else None
            out.append({**base, "relationship": rid, "field": None, "old": None if ch.get("old") is None else "removed", "new": label,
                        "evidence": ((new or {}).get("evidence") or [])[:5] if isinstance(new, dict) else []})
        else:
            if rest[-1] == "version":
                continue
            out.append({**base, "relationship": rid or coll, "field": ".".join(rest), "old": ch.get("old"), "new": ch.get("new"), "evidence": new_ev_ids[:5]})
    return out


def apply_item(item: dict, writer: Writer, paths: Paths, today: date | None) -> list[dict]:
    """Validate against the writer's current data, then apply. Returns the change log entries."""
    ready = prepare(item, paths, writer.data, today)
    new_ev = [e for e in ready.get("evidence") or [] if e.get("id") not in {x["id"] for x in writer.data["evidence"]}]
    placeholders = [e["id"] for e in new_ev if str(e["id"]).startswith("new:")]
    mapping = dict(zip(placeholders, _next_evidence_ids(paths, writer.data, len(placeholders))))
    diff = triage.resolve_ids(ready["diff"], mapping)
    new_ev = triage.resolve_ids(new_ev, mapping)
    before = copy.deepcopy(writer.data)
    writer.add_evidence(new_ev)
    touched = []
    for ch in diff:
        writer.change(ch)
        coll, rid = subject_of(ch["path"])
        whole = len(ch["path"].strip("/").split("/")) == 2
        if rid and coll != "evidence" and not whole and (coll, rid) not in touched:
            touched.append((coll, rid))
    for coll, rid in touched:
        writer.bump(coll, rid)
    item["approval_record"]["applied_at"] = now_iso()
    item["applied_diff"] = diff
    item["applied_evidence_ids"] = [e["id"] for e in new_ev]
    return changelog_entries(item, diff, before, writer.data, [e["id"] for e in new_ev])


# ---------------------------------------------------------------- the run

def run_step(module: str, paths: Paths) -> int:
    """Run one pipeline command. Separate so tests can replace it."""
    return subprocess.run([sys.executable, "-m", module], cwd=paths.root).returncode


class Backup:
    """Copies of everything a run may change, so a failed run can be undone."""

    def __init__(self, paths: Paths, with_published: bool):
        self.paths = paths
        self.tmp = Path(tempfile.mkdtemp(prefix="apply_backup_"))
        self.targets = [paths.register, paths.drafts, paths.changelog, paths.approved, paths.evidence_dir / f"{EVIDENCE_NS}.jsonl",
                        paths.evidence_dir / "_namespaces.json"]
        if with_published:
            self.targets += [paths.published, paths.root / "site"]
        self.history = paths.root / "data" / "history"
        self.history_before = {p.name for p in self.history.iterdir()} if self.history.exists() else set()
        self.existed = {}
        for i, t in enumerate(self.targets):
            self.existed[t] = t.exists()
            if t.is_dir():
                shutil.copytree(t, self.tmp / str(i))
            elif t.exists():
                shutil.copy2(t, self.tmp / str(i))

    def restore(self) -> None:
        for i, t in enumerate(self.targets):
            if t.is_dir():
                shutil.rmtree(t)
            elif t.exists():
                t.unlink()
            if self.existed[t]:
                src = self.tmp / str(i)
                if src.is_dir():
                    shutil.copytree(src, t)
                else:
                    shutil.copy2(src, t)
        if self.history.exists():
            for p in self.history.iterdir():
                if p.name not in self.history_before and p.is_dir():
                    shutil.rmtree(p)
        tmp_pub = self.paths.published.with_name("published.tmp")
        if tmp_pub.exists():
            shutil.rmtree(tmp_pub)

    def discard(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)


def approved_items(paths: Paths) -> list[dict]:
    if not paths.approved.exists():
        return []
    items = [load_json(f) for f in sorted(paths.approved.glob("*.json")) if not f.name.startswith("_")]
    return sorted(items, key=lambda i: ((i.get("approval_record") or {}).get("at") or "", i["id"]))


def apply_all(paths: Paths | None = None, publish: bool = True, dry_run: bool = False, publish_anyway: bool = False,
              today: date | None = None, step=run_step) -> int:
    paths = paths or Paths()
    items = approved_items(paths)
    if not items and not publish_anyway:
        print("Nothing approved to apply.")
        return 0
    if dry_run:
        data = load_collections(paths.register)
        rc = 0
        for it in items:
            try:
                prepare(it, paths, data, today)
                print(f"ok       {it['id']}")
            except Blocked as b:
                rc = 1
                print(f"BLOCKED  {b}")
        return rc
    backup = Backup(paths, with_published=publish)
    try:
        writer = Writer(paths)
        entries = []
        for it in items:
            entries += apply_item(it, writer, paths, today)
        writer.save()
        if entries:
            save_json(paths.changelog, load_json(paths.changelog, []) + entries)
        paths.applied.mkdir(parents=True, exist_ok=True)
        for it in items:
            save_item(paths.applied, it)
            (paths.approved / f"{it['id']}.json").unlink()
        for n in writer.notes:
            print(f"note: {n}")
        print(f"Applied {len(items)} approved item(s); {len(entries)} change log entr{'y' if len(entries) == 1 else 'ies'} added.")
        if publish:
            for mod in STEPS:
                print(f"== {mod}", flush=True)
                rc = step(mod, paths)
                if rc != 0:
                    raise Blocked(mod, f"exited with code {rc}")
    except (Blocked, DiffError) as err:
        backup.restore()
        backup.discard()
        print(f"\nSTOPPED: {err}\nNothing was applied or published. The register, change log, approved items and data/published/ are as they were.",
              file=sys.stderr)
        return 1
    except Exception:
        backup.restore()
        backup.discard()
        raise
    backup.discard()
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-publish", action="store_true")
    ap.add_argument("--publish-anyway", action="store_true")
    args = ap.parse_args(argv)
    return apply_all(publish=not args.no_publish, dry_run=args.dry_run, publish_anyway=args.publish_anyway)


if __name__ == "__main__":
    sys.exit(main())
