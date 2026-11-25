"""Inbox to review queue (spec/11 U2).

  python3 -m pipeline.triage                  triage new inbox hits, then merge any extracted diffs
  python3 -m pipeline.triage --offline        the same without fetching any source
  python3 -m pipeline.triage --merge          only merge extracted diffs from data/queue/_extracted/
  python3 -m pipeline.triage --pending        list items waiting for extraction (the headless job reads this)
  python3 -m pipeline.triage --summary        the pending items summary, watcher alerts first; prints nothing if there is nothing
  python3 -m pipeline.triage --budget         exit 0 if the paid extraction step may run, 3 if the cap is unset or reached
  python3 -m pipeline.triage --record-spend <claude result json>
  python3 -m pipeline.triage --cited-cache    cached files that evidence cites (the workflows commit these by name)

What this module does without any API key:
1. Discards hits that show no money, commitment or credit support between Nvidia and another party.
   Every discard is logged with its reason in data/inbox/_triaged.jsonl.
2. Matches each remaining hit to an existing relationship or complex link, or marks it new.
3. Writes data/queue/<id>.json: summary, the raw hit, an empty diff marked "needs extraction"
   (or "needs quote" for a paywalled article), check results, proposed change type, and whether a
   person must approve it (config/auto_approve.json).
4. Market value hits arrive with their diff, so they are checked here and can be approved by rule.
5. Stale amounts are grouped per record, their evidence is grounded again, and those where nothing
   moved are marked for the batch confirm screen.

Extraction itself (reading the source, drafting the diff with a verbatim quote for every new figure,
searching the other party's filings, critic notes) is done by the headless Claude job following
pipeline/tasks/triage_extract.md. It writes data/queue/_extracted/<id>.json; this module validates
that file, runs every check on the proposed change and updates the queue item. A proposal that fails
grounding stays in the queue marked "failed grounding" and can never be published.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path

from . import checks
from .common import classify_domain, load_json, save_json
from .update_common import (DiffError, Paths, amount_field_of, append_jsonl, apply_diff, get_path, inbox_hits, load_collections,
                            needs_human, now_iso, queue_items, read_jsonl, save_item, sha, subject_of, touched_amounts)

STATES = ("needs extraction", "needs quote", "ready", "failed grounding", "failed checks", "hold")
MONEY = re.compile(r"\$\s?\d|\b(?:million|billion|trillion)\b|\bshares\b|\bcommit|\bwarrants?\b", re.I)
EXPOSURE = re.compile(r"(?i)\b(invest\w*|stake|equity|backstop|guarant\w+|financ\w+|loan|lease\w*|credit facility|prepa\w+|deposit|commit\w+|"
                      r"warrant\w*|acqui\w+|purchase agreement|letter of intent|collateral|offtake|capacity)\b")
NVDA_FORMS = ("10-K", "10-Q", "8-K", "S-1", "S-3", "S-4", "424B", "DEF 14A", "DEFA14A", "SC TO", "425")
TEMP_EV_BASE = 990000000


# ---------------------------------------------------------------- source text

def fetch_text(hit: dict) -> str | None:
    """Text of the hit's source, or None if it cannot be read. Filings come through the SEC client and are cached in full.
    News is never fetched here: the article is read by the extraction job into a temporary file only."""
    url = hit.get("source_url")
    if not url:
        return None
    info = classify_domain(url)
    if info.get("group") != "sec":
        return None
    from . import edgar
    from .common import html_to_text
    try:
        return html_to_text(edgar.fetch_text(url))
    except Exception:  # noqa: BLE001
        return None


# ---------------------------------------------------------------- step 1: discard

def discard_reason(hit: dict, text: str | None, names: list[str]) -> str | None:
    """Why a hit shows no money, commitment or credit support between Nvidia and another party. None = keep."""
    kind = hit.get("kind")
    blob = " ".join(str(hit.get(k) or "") for k in ("title", "snippet", "summary"))
    if kind in ("earnings_release", "earnings_date"):
        return "calendar entry only: an earnings date carries no money, commitment or credit support"
    if kind == "ownership" and hit.get("role") == "issuer":
        return "insider or holder report on Nvidia's own shares: no counterparty"
    if kind == "fulltext" and not hit.get("has_money"):
        return "the passage naming Nvidia has no amount, share count or commitment"
    if kind == "filing" and hit.get("watcher") == "nvda_filings":
        if not any((hit.get("form") or "").startswith(f) for f in NVDA_FORMS):
            return f"form {hit.get('form')} does not carry deal terms"
        if text is not None and not MONEY.search(text):
            return "the filing text has no amount, share count or commitment"
    if kind == "filing" and hit.get("watcher") == "counterparty_filings":
        if text is not None and "nvidia" not in text.lower():
            return "the filing does not mention Nvidia"
    if kind == "release":
        low = blob.lower()
        if hit.get("entity") == "ent_nvidia":
            named = any(re.search(rf"(?<!\w){re.escape(n.lower())}(?!\w)", low) for n in names)
            if not (MONEY.search(blob) or (named and EXPOSURE.search(blob))):
                return "the release summary shows no money, commitment or credit support"
        elif "nvidia" not in low:
            return "the release does not mention Nvidia"
    if kind == "news":
        info = classify_domain(hit.get("source_url") or "")
        if info.get("tier") != "2":
            return f"source {info.get('domain')} is not a tier 2 publication"
        if not (MONEY.search(blob) or EXPOSURE.search(blob)):
            return "the report shows no money, commitment or credit support"
    return None


# ---------------------------------------------------------------- step 2: match

def match(hit: dict, data: dict) -> dict:
    """Existing relationships and complex links the hit could change, or 'new'."""
    ents = {e["id"]: e for e in data["entities"]}
    found = []
    for k in ("counterparty", "entity"):
        if hit.get(k) and hit[k] != "ent_nvidia" and hit[k] in ents:
            found.append(hit[k])
    if hit.get("relationship"):
        r = next((r for r in data["relationships"] if r["id"] == hit["relationship"]), None)
        if r:
            return {"kind": "existing", "entities": [r["to"]], "relationships": [r["id"]], "complex_links": []}
    if not found:
        blob = " ".join(str(hit.get(k) or "") for k in ("title", "snippet", "summary", "issuer_name", "entity_name")).lower()
        for e in data["entities"]:
            if e["id"] in ("ent_nvidia", "ent_nvidia_unattributed"):
                continue
            for n in {e.get("short_name"), e.get("name")}:
                if n and len(n) >= 4 and re.search(rf"(?<!\w){re.escape(n.lower())}(?!\w)", blob):
                    found.append(e["id"])
                    break
    found = list(dict.fromkeys(found))
    rels = [r["id"] for r in data["relationships"] if r["to"] in found]
    cx = [c["id"] for c in data["complex_links"] if any(c.get(k) in found for k in ("provider", "beneficiary", "obligor"))]
    return {"kind": "existing" if rels or cx else "new", "entities": found, "relationships": rels, "complex_links": cx}


# ---------------------------------------------------------------- checks on a proposed change

def _temp_ids(item: dict) -> dict:
    """Placeholder evidence ids (new:1) mapped to ids that cannot collide, for checking only."""
    return {ev["id"]: f"ev_{TEMP_EV_BASE + i}" for i, ev in enumerate(item.get("evidence") or [], 1) if str(ev.get("id", "")).startswith("new:")}


def resolve_ids(obj, mapping: dict):
    """Replace placeholder evidence ids everywhere in a diff or an evidence list."""
    if not mapping:
        return obj
    raw = json.dumps(obj, ensure_ascii=False)
    for old, new in sorted(mapping.items(), key=lambda kv: -len(kv[0])):
        raw = raw.replace(json.dumps(old), json.dumps(new))
    return json.loads(raw)


def _subset(data: dict, touched: dict, extra_evidence: list[dict]) -> dict:
    """The touched records plus what they point at: small enough to check quickly, complete enough for every check."""
    rel_ids = set(touched.get("relationships", ()))
    for c in data["complex_links"]:
        if c["id"] in touched.get("complex_links", ()):
            rel_ids |= set(c.get("nvidia_links") or [])
    for e in data["events"]:
        if e["id"] in touched.get("events", ()):
            rel_ids.add(e.get("relationship"))
    out = {"entities": data["entities"],
           "relationships": [r for r in data["relationships"] if r["id"] in rel_ids],
           "projects": [p for p in data["projects"] if p["id"] in touched.get("projects", ())],
           "events": [e for e in data["events"] if e["id"] in touched.get("events", ())],
           "complex_links": [c for c in data["complex_links"] if c["id"] in touched.get("complex_links", ())],
           "nvidia_financials": data.get("nvidia_financials") or {}}
    ent_ids = set(touched.get("entities", ()))
    used = set()
    for coll in (out["relationships"], out["projects"], out["events"], out["complex_links"], [e for e in data["entities"] if e["id"] in ent_ids]):
        for row in coll:
            used |= set(checks._ev_ids(row))
    used |= set(touched.get("evidence", ()))
    pool = {e["id"]: e for e in data["evidence"]}
    pool.update({e["id"]: e for e in extra_evidence})
    out["evidence"] = [pool[i] for i in sorted(used) if i in pool] + [e for e in extra_evidence if e["id"] not in used]
    # entities other than the touched ones are present so references resolve, but their own amounts are not this item's business
    out["_quiet_entities"] = [e["id"] for e in data["entities"] if e["id"] not in ent_ids]
    return out


def _problems(sub: dict, today: date | None) -> set[str]:
    quiet = set(sub.pop("_quiet_entities", []))
    with tempfile.TemporaryDirectory() as tmp:
        for name in ("entities", "relationships", "projects", "events", "complex_links", "evidence", "nvidia_financials"):
            save_json(Path(tmp) / f"{name}.json", sub[name])
        reg = checks.Register(tmp)
        checks.set_eligibility(reg)
        probs = checks.run_all(reg, today=today, draft=True)
    out = set()
    for p in probs:
        m = re.match(r"[a-z ]+: (?:event )?((?:ent|rel|proj|cx|evt)_[A-Za-z0-9_]+)", p)
        if m and m.group(1) in quiet:
            continue
        if p.startswith(("nvidia_financials", "dates: nvidia_financials", "grounding: nvidia_financials", "evidence: nvidia_financials")):
            continue
        out.add(p)
    return out


def evaluate(item: dict, paths: Paths, today: date | None = None, data: dict | None = None) -> list[dict]:
    """Run the automated checks of spec/09 on the item's proposed change. Returns [{check, result, detail}].

    The change is applied to a copy of the touched records and checked beside the same records unchanged;
    only problems the change introduces count against it.
    """
    data = data or load_collections(paths.register)
    diff = item.get("diff") or []
    results = []
    if not diff:
        return [{"check": "proposal", "result": "pending", "detail": "no proposed change yet"}]
    mapping = _temp_ids(item)
    diff_r = resolve_ids(diff, mapping)
    new_ev = resolve_ids(item.get("evidence") or [], mapping)
    known = {e["id"] for e in data["evidence"]}
    new_ev = [e for e in new_ev if e.get("id") not in known]
    try:
        patched = apply_diff(data, diff_r)
    except DiffError as err:
        return [{"check": "applies", "result": "fail", "detail": str(err)}]
    except (KeyError, TypeError, ValueError) as err:
        return [{"check": "applies", "result": "fail", "detail": f"malformed change: {err}"}]
    results.append({"check": "applies", "result": "pass", "detail": f"{len(diff)} change(s) apply to the register as it stands"})
    day = (today or datetime.now(timezone.utc).date()).isoformat()
    for p in touched_amounts(diff_r):
        # an amount that gains its first value is dated by the person who approves it (apply_approved sets last_verified,
        # and the approval rule sends every such change to a person); check it as it will be applied
        a = get_path(patched, p)
        if isinstance(a, dict) and a.get("value") is not None and a.get("last_verified") is None and "last_verified" in a:
            a["last_verified"] = day
    touched: dict = {}
    for ch in diff_r:
        coll, rid = subject_of(ch["path"])
        if rid:
            touched.setdefault(coll, set()).add(rid)
    touched.setdefault("evidence", set()).update(e["id"] for e in new_ev)
    before = _problems(_subset(data, touched, []), today)
    try:
        after = _problems(_subset(patched, touched, new_ev), today)
    except Exception as err:  # noqa: BLE001  a record so malformed the checks cannot read it
        return results + [{"check": "schema", "result": "fail", "detail": f"the changed record cannot be checked: {type(err).__name__}: {err}"}]
    new = sorted(after - before)
    groups: dict = {}
    for p in new:
        groups.setdefault(p.split(":", 1)[0].strip(), []).append(p.split(":", 1)[1].strip())
    for name in ("schema", "evidence", "grounding", "display", "independence", "allowlist", "dates", "amount order", "insight", "copy",
                 "quotes", "reconciliation", "consequences"):
        if name in groups:
            results.append({"check": name, "result": "fail", "detail": "; ".join(groups.pop(name))[:1200]})
        else:
            results.append({"check": name, "result": "pass", "detail": ""})
    for name, msgs in groups.items():
        results.append({"check": name, "result": "fail", "detail": "; ".join(msgs)[:1200]})
    # every new figure needs a quote that contains it: a changed amount with no evidence at all is a grounding failure
    for ch in diff_r:
        field = amount_field_of(ch["path"])
        if field and ch["path"].endswith("/value") and ch.get("new") is not None:
            amount = get_path(patched, ch["path"].rsplit("/", 1)[0]) or {}
            if not amount.get("not_applicable") and not (amount.get("evidence") or amount.get("components")):
                results.append({"check": "grounding", "result": "fail", "detail": f"{ch['path']}: new figure has no quote"})
    return results


def state_from(results: list[dict], fallback: str = "ready") -> str:
    failed = [r["check"] for r in results if r["result"] == "fail"]
    if "grounding" in failed:
        return "failed grounding"
    if failed:
        return "failed checks"
    return fallback


def finalize(item: dict, paths: Paths, today: date | None = None, data: dict | None = None) -> dict:
    """Run the checks, set the state and decide who may approve."""
    if item.get("diff"):
        item["checks"] = evaluate(item, paths, today, data)
        if item.get("state") != "hold":
            item["state"] = state_from(item["checks"])
    human, why = needs_human(item, paths.cfg("auto_approve.json", {"auto": []}))
    item["needs_human"] = human
    item["approval"] = "human" if human else "auto"
    item["approval_reason"] = why
    return item


# ---------------------------------------------------------------- queue items

def source_key(hit: dict) -> str:
    return hit.get("accession") or hit.get("source_url") or hit["hash"]


def guess_change_type(hit: dict, m: dict) -> str:
    if hit.get("kind") == "market_value":
        return "market_value"
    if hit.get("kind") == "stale_amount":
        return "reverified"
    return "added" if m["kind"] == "new" else "evidence_added"


def summarize(hit: dict, m: dict, names: dict) -> str:
    who = ", ".join(names.get(e, e) for e in m["entities"]) or hit.get("entity_name") or "an unmatched party"
    what = hit.get("title") or hit.get("kind")
    tail = (f"Could change {len(m['relationships'])} relationship(s) and {len(m['complex_links'])} link(s) with {who}."
            if m["kind"] == "existing" else f"No existing record matches; possible new relationship with {who}.")
    return f"{what} ({hit.get('date') or 'undated'}). {tail}"


def new_item(hit: dict, m: dict, names: dict, state: str) -> dict:
    return {"id": f"q_{(hit.get('found_at') or now_iso())[:10].replace('-', '')}_{sha(source_key(hit))[:10]}",
            "created": now_iso(), "state": state, "change_type": guess_change_type(hit, m), "summary": summarize(hit, m, names),
            "source": {"key": source_key(hit), "url": hit.get("source_url"), "title": hit.get("title"), "date": hit.get("date"),
                       "form": hit.get("form"), "accession": hit.get("accession"), "watcher": hit.get("watcher")},
            "match": m, "hits": [hit], "diff": [], "evidence": [],
            "checks": [{"check": "proposal", "result": "pending", "detail": "needs extraction" if state == "needs extraction" else state}],
            "critic_notes": None, "counterparty_silence": None, "batch_confirm": False}


def _clean(hit: dict) -> dict:
    return {k: v for k, v in hit.items() if not k.startswith("_")}


def triage_hit(hit: dict, data: dict, open_items: dict, paths: Paths, offline: bool, today: date | None) -> tuple[str, str | None, str | None]:
    """Returns (outcome, reason, queue id). Outcome: discarded, queued or merged."""
    names = {e["id"]: e.get("short_name") or e["name"] for e in data["entities"]}
    text = None if (offline or hit.get("kind") != "filing") else fetch_text(hit)
    reason = discard_reason(hit, text, [n for i, n in names.items() if i not in ("ent_nvidia", "ent_nvidia_unattributed") and len(n) >= 4])
    if reason:
        return "discarded", reason, None
    m = match(hit, data)
    key = source_key(hit)
    existing = open_items.get(key)
    if existing and hit.get("kind") not in ("market_value",):
        existing["hits"].append(_clean(hit))
        for k in ("entities", "relationships", "complex_links"):
            existing["match"][k] = list(dict.fromkeys(existing["match"][k] + m[k]))
        if existing["match"]["relationships"] or existing["match"]["complex_links"]:
            existing["match"]["kind"] = "existing"
        save_item(paths.queue, existing)
        return "merged", None, existing["id"]
    state = "needs extraction"
    if hit.get("kind") == "news" and hit.get("paywalled"):
        state = "needs quote"
    item = new_item(_clean(hit), m, names, state)
    if hit.get("kind") == "market_value":
        item["id"] = f"q_{(hit.get('date') or '')[:10].replace('-', '')}_mv_{sha(hit['hash'])[:10]}"
        item["diff"], item["evidence"], item["state"] = hit.get("diff") or [], hit.get("evidence") or [], "ready"
        item["hits"] = [{k: v for k, v in _clean(hit).items() if k not in ("diff", "evidence")}]
        item["summary"] = (f"{names.get(hit.get('entity'), hit.get('ticker'))}: market value of {hit['shares']:,.0f} shares at "
                           f"{hit['price']:,.2f} ({hit['price_source']}, {hit['price_timestamp']}).")
    finalize(item, paths, today, data)
    save_item(paths.queue, item)
    open_items[key] = item
    return "queued", None, item["id"]


def triage_stale(hits: list[dict], data: dict, paths: Paths, today: date, all_hits: list[dict]) -> list[str]:
    """One queue item per record with stale amounts. Evidence is grounded again; unchanged items go to batch confirm."""
    by_record: dict = {}
    for h in hits:
        by_record.setdefault(h["record"], []).append(h)
    ev_by_id = {e["id"]: e for e in data["evidence"]}
    names = {e["id"]: e.get("short_name") or e["name"] for e in data["entities"]}
    ids = []
    for record, group in by_record.items():
        qid = f"q_stale_{re.sub(r'[^A-Za-z0-9_]+', '_', record)}"
        f = paths.queue / f"{qid}.json"
        item = load_json(f) if f.exists() else None
        diff, results, moved = [], [], []
        for h in group:
            p = h["path"] + "/last_verified"
            current = get_path(data, p)
            if current != h["last_verified"]:
                continue    # verified again since the watcher ran
            diff.append({"path": p, "old": current, "new": today.isoformat()})
            amount = get_path(data, h["path"]) or {}
            for value, ev_ids in checks.amount_parts(amount):
                for i in ev_ids:
                    ev = ev_by_id.get(i)
                    probs = ["evidence record missing"] if ev is None else checks.ground_evidence(ev)
                    if not probs and value is not None and not checks.evidence_contains(ev, value):
                        probs = ["the figure is no longer found beside the quote"]
                    if probs:
                        moved.append(f"{h['amount_path']}: {i}: {probs[0]}")
        if not diff:
            continue
        results.append({"check": "grounding", "result": "fail" if moved else "pass",
                        "detail": "; ".join(moved) if moved else "every quote still found in its cached source, with its figure"})
        ent = group[0].get("entity")
        since = min(h["last_verified"] for h in group)
        newer = [x for x in all_hits if x.get("kind") not in ("stale_amount", "market_value", "earnings_release", "earnings_date")
                 and ent and ent in (x.get("entity"), x.get("counterparty")) and (x.get("date") or "") > since]
        results.append({"check": "newer sources", "result": "review" if newer else "pass",
                        "detail": (f"{len(newer)} newer hit(s) on {names.get(ent, ent)} since {since}: " + "; ".join((x.get('title') or '')[:80] for x in newer[:5]))
                        if newer else f"no newer filing, release or report on {names.get(ent, ent) if ent else record} in the inbox since {since}"})
        results.append({"check": "source re-fetch", "result": "pending", "detail": "done by the extraction job when it runs; not done offline"})
        nothing_changed = not moved and not newer
        new = {"id": qid, "created": (item or {}).get("created") or now_iso(), "state": (item or {}).get("state") if (item or {}).get("state") == "hold" else ("ready" if not moved else "failed grounding"),
               "change_type": "reverified",
               "summary": f"{record}: {len(diff)} amount(s) past the re-verification limit, last verified {since}. "
                          + ("Nothing has moved: confirm in the batch screen." if nothing_changed else "Something may have moved: review individually."),
               "source": {"key": qid, "url": None, "title": "Re-verification", "date": today.isoformat(), "form": None, "accession": None, "watcher": "staleness"},
               "match": {"kind": "existing", "entities": [ent] if ent else [], "relationships": [record] if record.startswith("rel_") else [], "complex_links": [record] if record.startswith("cx_") else []},
               "hits": [_clean(h) for h in group], "diff": diff, "evidence": [], "checks": results, "critic_notes": None,
               "counterparty_silence": None, "batch_confirm": nothing_changed, "reverified_fields": [d["path"] for d in diff]}
        human, why = needs_human(new, paths.cfg("auto_approve.json", {"auto": []}))
        new.update({"needs_human": True, "approval": "human", "approval_reason": why if human else "every re-verification needs a person"})
        save_item(paths.queue, new)
        ids.append(qid)
    return ids


def run(paths: Paths | None = None, offline: bool = False, today: date | None = None) -> dict:
    paths = paths or Paths()
    today = today or datetime.now(timezone.utc).date()
    data = load_collections(paths.register)
    done = {r["hash"] for r in read_jsonl(paths.triaged)}
    hits = inbox_hits(paths)
    todo = [h for h in hits if h["hash"] not in done]
    open_items = {it["source"]["key"]: it for it in queue_items(paths) if it.get("source")}
    limit = (paths.cfg("limits.json", {}) or {}).get("max_queue_items_per_run") or 10 ** 9
    out = {"hits": len(todo), "discarded": 0, "queued": 0, "merged": 0, "stale_items": 0, "left_for_next_run": 0}
    log, stale = [], []
    for h in todo:
        if h.get("kind") == "stale_amount":
            stale.append(h)
            continue
        if out["queued"] >= limit and h.get("kind") != "market_value":
            out["left_for_next_run"] += 1
            continue
        outcome, reason, qid = triage_hit(h, data, open_items, paths, offline, today)
        out[outcome] += 1
        log.append({"hash": h["hash"], "watcher": h.get("watcher"), "outcome": outcome, "reason": reason, "queue_id": qid,
                    "title": (h.get("title") or "")[:160], "source_url": h.get("source_url"), "at": now_iso()})
    if stale:
        ids = triage_stale(stale, data, paths, today, hits)
        out["stale_items"] = len(ids)
        log += [{"hash": h["hash"], "watcher": "staleness", "outcome": "queued", "reason": None,
                 "queue_id": f"q_stale_{re.sub(r'[^A-Za-z0-9_]+', '_', h['record'])}", "title": h.get("title"), "source_url": None, "at": now_iso()} for h in stale]
    if log:
        append_jsonl(paths.triaged, log)
    out["extracted_merged"] = merge_extracted(paths, today)
    return out


# ---------------------------------------------------------------- extracted diffs from the headless job

def merge_extracted(paths: Paths | None = None, today: date | None = None) -> int:
    """Fold data/queue/_extracted/<id>.json into its queue item and check it. Returns how many were merged."""
    paths = paths or Paths()
    d = paths.queue / "_extracted"
    n = 0
    if not d.exists():
        return 0
    data = load_collections(paths.register)
    for f in sorted(d.glob("*.json")):
        qf = paths.queue / f.name
        if not qf.exists():
            print(f"extracted file {f.name} has no queue item; left in place", file=sys.stderr)
            continue
        try:
            ex = load_json(f)
        except json.JSONDecodeError as err:
            print(f"extracted file {f.name} is not valid JSON ({err}); left in place", file=sys.stderr)
            continue
        item = load_json(qf)
        if ex.get("discard"):
            append_jsonl(paths.triaged, [{"hash": h["hash"], "watcher": h.get("watcher"), "outcome": "discarded", "reason": str(ex["discard"]),
                                          "queue_id": item["id"], "title": (h.get("title") or "")[:160], "source_url": h.get("source_url"),
                                          "at": now_iso(), "by": "extraction"} for h in item.get("hits", [])])
            qf.unlink()
            f.unlink()
            n += 1
            continue
        if ex.get("needs_quote"):
            item["state"] = "needs quote"
            item["checks"] = [{"check": "proposal", "result": "pending", "detail": "paywalled: a reviewer must paste the sentence"}]
        for k in ("summary", "change_type", "critic_notes", "counterparty_silence", "notes"):
            if ex.get(k) is not None:
                item[k] = ex[k]
        if isinstance(ex.get("diff"), list):
            item["diff"] = ex["diff"]
            item["evidence"] = ex.get("evidence") or []
            if item.get("state") != "hold":
                item["state"] = "ready"
        item["extracted_at"] = now_iso()
        finalize(item, paths, today, data)
        save_item(paths.queue, item)
        f.unlink()
        n += 1
    return n


# ---------------------------------------------------------------- summary, budget

def pending_summary(paths: Paths | None = None) -> str:
    """Short text for Thomas: watcher alerts first, then the queue. Empty when there is nothing to say."""
    paths = paths or Paths()
    from .watchers.run import alerts
    items = [i for i in queue_items(paths) if i.get("state") != "hold"]
    lines = [f"ALERT: watcher {a}" for a in alerts(paths)]
    if not items and not lines:
        return ""
    by_state: dict = {}
    for i in items:
        by_state.setdefault(i["state"], []).append(i)
    batch = [i for i in items if i.get("batch_confirm")]
    auto = [i for i in items if not i.get("needs_human")]
    lines.append(f"{len(items)} item(s) in the review queue" + (f", {len(batch)} for batch confirm" if batch else "")
                 + (f", {len(auto)} that the auto rule will publish" if auto else "") + ".")
    for state in STATES:
        for i in by_state.get(state, [])[:12]:
            if i in batch or i in auto:
                continue
            lines.append(f"- [{state}] {i['summary'][:200]}")
    held = len(queue_items(paths)) - len(items)
    if held:
        lines.append(f"{held} item(s) on hold.")
    lines.append("Run `make review` to open the review page.")
    return "\n".join(lines)


def cited_cache(paths: Paths | None = None) -> list[str]:
    """Cached files cited by evidence in the queue, the approved items, the register and research/evidence/upd.jsonl.
    The cache directories are ignored by git, so the workflows add these files by name: CI needs them to ground quotes."""
    paths = paths or Paths()
    evs = list(load_json(paths.register / "evidence.json", []))
    evs += read_jsonl(paths.evidence_dir / "upd.jsonl")
    for d in (paths.queue, paths.approved):
        if d.exists():
            for f in d.glob("q_*.json"):
                evs += load_json(f).get("evidence") or []
    out = sorted({e["cache_path"] for e in evs if e.get("cache_path") and "/_tmp/" not in e["cache_path"] and (paths.root / e["cache_path"]).exists()})
    return out + [p + ".meta.json" for p in out if (paths.root / (p + ".meta.json")).exists()]


def spend_file(paths: Paths) -> Path:
    return paths.queue / "_spend.json"


def budget(paths: Paths | None = None, today: date | None = None) -> dict:
    """Whether the paid extraction step may run, per config/limits.json. A null cap means it does not run."""
    paths = paths or Paths()
    month = (today or datetime.now(timezone.utc).date()).strftime("%Y-%m")
    cap = (paths.cfg("limits.json", {}) or {}).get("monthly_usd_cap")
    spent = float(load_json(spend_file(paths), {}).get(month, 0))
    if cap is None:
        return {"may_run": False, "month": month, "cap": None, "spent": spent, "remaining": 0.0,
                "message": "No monthly spend cap is set in config/limits.json, so the paid extraction step does not run."}
    remaining = round(float(cap) - spent, 2)
    if remaining <= 0:
        return {"may_run": False, "month": month, "cap": cap, "spent": spent, "remaining": 0.0,
                "message": f"ALERT: the monthly spend cap of ${cap:,.2f} is reached (${spent:,.2f} spent in {month}). Extraction is stopped until next month or a higher cap."}
    return {"may_run": True, "month": month, "cap": cap, "spent": spent, "remaining": remaining,
            "message": f"${spent:,.2f} of ${cap:,.2f} spent in {month}; ${remaining:,.2f} left."}


def record_spend(result_file, paths: Paths | None = None, today: date | None = None) -> float:
    """Add the cost reported by `claude -p --output-format json` to this month's total."""
    paths = paths or Paths()
    month = (today or datetime.now(timezone.utc).date()).strftime("%Y-%m")
    try:
        res = json.loads(Path(result_file).read_text())
    except (OSError, json.JSONDecodeError):
        res = {}
    if isinstance(res, list):    # stream of events: the result event carries the total
        res = next((r for r in reversed(res) if isinstance(r, dict) and "total_cost_usd" in r), {})
    cost = float(res.get("total_cost_usd") or 0)
    spend = load_json(spend_file(paths), {})
    spend[month] = round(float(spend.get(month, 0)) + cost, 4)
    save_json(spend_file(paths), spend)
    return cost


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--merge", action="store_true")
    ap.add_argument("--pending", action="store_true")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--budget", action="store_true")
    ap.add_argument("--record-spend", metavar="FILE")
    ap.add_argument("--cited-cache", action="store_true", help="print the cached files that evidence cites, for `git add -f`")
    args = ap.parse_args(argv)
    paths = Paths()
    if args.cited_cache:
        print("\n".join(cited_cache(paths)))
        return 0
    if args.summary:
        s = pending_summary(paths)
        if s:
            print(s)
        return 0
    if args.budget:
        b = budget(paths)
        print(b["message"])
        if b["may_run"]:
            print(f"remaining_usd={b['remaining']}")
        return 0 if b["may_run"] else 3
    if args.record_spend:
        print(f"recorded ${record_spend(args.record_spend, paths):.4f}")
        return 0
    if args.pending:
        for i in queue_items(paths):
            if i["state"] in ("needs extraction",):
                print(f"{i['id']}\t{i['change_type']}\t{i['source'].get('url') or ''}\t{i['summary'][:140]}")
        return 0
    if args.merge:
        print(f"{merge_extracted(paths)} extracted proposal(s) merged")
        return 0
    res = run(paths, offline=args.offline)
    print(f"{res['hits']} new hit(s): {res['queued']} queued, {res['merged']} added to an open item, {res['discarded']} discarded, "
          f"{res['stale_items']} re-verification item(s), {res['extracted_merged']} extracted proposal(s) merged"
          + (f", {res['left_for_next_run']} left for the next run (limit in config/limits.json)" if res["left_for_next_run"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
