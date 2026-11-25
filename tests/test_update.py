"""Gate U: the continuous update loop on fixtures (spec/09, spec/11).

Everything runs in a temporary directory. No test touches the real register, the real published
build or the network: sources are fixture files and every fetch is replaced.
"""
import json
import shutil
from datetime import date, datetime, timezone
from pathlib import Path

import pytest

from pipeline import apply_approved, checks, review, triage
from pipeline.common import load_json, save_json
from pipeline.update_common import Paths, apply_diff, get_path, load_collections, needs_human, write_hits
from pipeline.watchers import base, market_values, run as watch_run, staleness

ROOT = Path(__file__).resolve().parent.parent
SEC = "https://www.sec.gov/Archives/edgar/data/1/000000000025000001/example.htm"
TODAY = date(2025, 3, 10)
PUBLISHED_SENTINEL = {"data_as_of": "2025-03-04", "note": "the last good publish"}


@pytest.fixture
def root(tmp_path, reg, helpers):
    """A whole temporary project: register, published build, inbox, queue, approved."""
    r = tmp_path / "project"
    eq = reg.rel["rel_example_eq_2025"]
    eq["amounts"]["funded"] = helpers.amt()                      # paid amount not yet known: the fixture filing will supply it
    eq["amounts"]["market_value"] = helpers.amt(250e6, ["ev_2"], price_source="Example filing", price_timestamp="2025-03-03")
    eq["holding"] = {"shares": 20000000, "as_of": "2025-03-03", "ticker": "EXMP", "instrument": "common", "evidence": ["ev_2"]}
    checks.set_eligibility(reg)
    (r / "data" / "register").mkdir(parents=True)
    for name, rows in (("entities", reg.entities), ("relationships", reg.relationships), ("evidence", reg.evidence), ("projects", []),
                       ("events", []), ("complex_links", [])):
        save_json(r / "data" / "register" / f"{name}.json", rows)
    save_json(r / "data" / "published" / "summary.json", PUBLISHED_SENTINEL)
    save_json(r / "data" / "changelog.json", [])
    for d in ("inbox", "queue", "approved"):
        (r / "data" / d).mkdir()
    assert checks.run_all(checks.Register(r / "data" / "register"), today=TODAY) == []
    return Paths(r)


def filing_hit():
    return {"hash": "h" * 64, "watcher": "counterparty_filings", "kind": "filing", "key": "0000000000-25-000001", "entity": "ent_example",
            "entity_name": "Example", "cik": "0000000001", "form": "8-K", "accession": "0000000000-25-000001", "date": "2025-03-03",
            "title": "Example 8-K: entry into a material definitive agreement", "source_url": SEC, "found_at": "2025-03-05T12:00:00Z"}


def drop(paths, watcher, hit, day="2025-03-05"):
    f = paths.inbox / day / f"{watcher}.jsonl"
    f.parent.mkdir(parents=True, exist_ok=True)
    with open(f, "a") as fh:
        fh.write(json.dumps(hit) + "\n")


def extracted(helpers, quote="for an aggregate purchase price of $250 million", value=250e6, status=None):
    ev = helpers.ev(0, f"{helpers.FX}/example_filing.html", quote, SEC)
    ev["id"] = "new:1"
    base_path = "relationships/rel_example_eq_2025"
    diff = [{"path": f"{base_path}/amounts/funded/value", "old": None, "new": value},
            {"path": f"{base_path}/amounts/funded/as_of", "old": None, "new": "2025-03-03"},
            {"path": f"{base_path}/amounts/funded/evidence", "old": [], "new": ["new:1"]}]
    if status:
        diff.append({"path": f"{base_path}/status", "old": "completed", "new": status})
    return {"summary": "Example's 8-K states the price paid for the shares.", "change_type": "amount_changed", "diff": diff, "evidence": [ev],
            "critic_notes": "No insight or consequence text changes.", "counterparty_silence": "Not applicable: this is the other party's filing."}


def queue_one(paths, monkeypatch, helpers, **kw):
    monkeypatch.setattr(triage, "fetch_text", lambda hit: "Example Corp sold shares to NVIDIA for $250 million.")
    drop(paths, "counterparty_filings", filing_hit())
    res = triage.run(paths, today=TODAY)
    assert res["queued"] == 1
    item = triage.queue_items(paths)[0]
    save_json(paths.queue / "_extracted" / f"{item['id']}.json", extracted(helpers, **kw))
    assert triage.merge_extracted(paths, TODAY) == 1
    return load_json(paths.queue / f"{item['id']}.json")


def steps_recorder(fail_at=None, scribble=None):
    calls = []

    def step(module, paths):
        calls.append(module)
        if scribble:
            scribble(module, paths)
        return 1 if module == fail_at else 0
    return calls, step


def snapshot(paths):
    """Bytes of everything a failed run must leave alone."""
    out = {}
    for d in (paths.published, paths.register, paths.approved):
        for f in sorted(d.rglob("*")):
            if f.is_file():
                out[str(f.relative_to(paths.root))] = f.read_bytes()
    out["changelog"] = paths.changelog.read_bytes()
    return out


# ------------------------------------------------------------------ Gate U 1: inbox to queue to register to change log

def test_fixture_filing_becomes_queue_item_without_an_api_key(root, monkeypatch):
    monkeypatch.setattr(triage, "fetch_text", lambda hit: "Example Corp sold shares to NVIDIA for $250 million.")
    drop(root, "counterparty_filings", filing_hit())
    res = triage.run(root, today=TODAY)
    assert (res["queued"], res["discarded"]) == (1, 0)
    [item] = triage.queue_items(root)
    assert item["state"] == "needs extraction" and item["diff"] == []
    assert item["hits"][0]["accession"] == "0000000000-25-000001"
    assert item["match"]["kind"] == "existing" and "rel_example_eq_2025" in item["match"]["relationships"]
    assert item["needs_human"] is True and item["approval"] == "human"
    assert item["summary"] and item["change_type"] == "evidence_added" and item["checks"][0]["result"] == "pending"
    # the same hit is never processed twice
    assert triage.run(root, today=TODAY)["hits"] == 0
    assert len(triage.queue_items(root)) == 1
    with pytest.raises(ValueError):
        review.approve(item["id"], root, by="Tester")      # nothing to approve until a change is drafted


def test_hits_with_no_money_or_no_nvidia_are_discarded_with_a_logged_reason(root, monkeypatch):
    monkeypatch.setattr(triage, "fetch_text", lambda hit: "Example Corp reports quarterly results. No chip vendor is named.")
    drop(root, "counterparty_filings", filing_hit())
    drop(root, "ownership_filings", {"hash": "o" * 64, "watcher": "ownership_filings", "kind": "ownership", "role": "issuer", "form": "4",
                                     "title": "4 on Nvidia's filing list", "source_url": SEC})
    drop(root, "fulltext_nvidia", {"hash": "f" * 64, "watcher": "fulltext_nvidia", "kind": "fulltext", "has_money": False, "title": "x", "source_url": SEC})
    drop(root, "news", {"hash": "n" * 64, "watcher": "news", "kind": "news", "title": "Nvidia to invest $1 billion", "source_url": "https://example-blog.substack.com/p/x"})
    res = triage.run(root, today=TODAY)
    assert res["discarded"] == 4 and res["queued"] == 0 and triage.queue_items(root) == []
    log = [json.loads(l) for l in open(root.triaged)]
    assert all(r["outcome"] == "discarded" and r["reason"] for r in log)
    assert any("does not mention Nvidia" in r["reason"] for r in log) and any("tier 2" in r["reason"] for r in log)


def test_approval_applies_diff_and_appends_changelog(root, monkeypatch, helpers):
    item = queue_one(root, monkeypatch, helpers)
    assert item["state"] == "ready", [c for c in item["checks"] if c["result"] != "pass"]
    assert all(c["result"] == "pass" for c in item["checks"])
    assert item["needs_human"] is True                       # funded changes at any size, null to a value included
    assert review.auto_approve(root) == []
    approved = review.approve(item["id"], root, by="Tester")
    assert (root.approved / f"{item['id']}.json").exists() and not (root.queue / f"{item['id']}.json").exists()
    assert approved["approval_record"]["rechecked"] == ["relationships/rel_example_eq_2025/amounts/funded"]

    calls, step = steps_recorder()
    assert apply_approved.apply_all(root, today=TODAY, step=step) == 0
    assert calls == ["pipeline.build_register", "pipeline.system_view", "pipeline.publish", "pipeline.build_site"]

    reg = checks.Register(root.register)
    rel = reg.rel["rel_example_eq_2025"]
    funded = rel["amounts"]["funded"]
    assert funded["value"] == 250e6 and funded["as_of"] == "2025-03-03"
    assert funded["last_verified"] == approved["approval_record"]["at"][:10]      # a person re-checked this amount
    assert rel["amounts"]["committed_total"]["last_verified"] == "2025-03-04"     # not re-checked, so untouched
    assert rel["version"] == 2 and reg.rel["rel_example_bk_2025"]["version"] == 1
    [new_id] = funded["evidence"]
    assert new_id.startswith("ev_") and reg.ev[new_id]["quote"] == "for an aggregate purchase price of $250 million"
    checks.set_eligibility(reg)
    assert funded["display_eligible"] is True
    assert checks.run_all(reg, today=TODAY) == []

    log = load_json(root.changelog)
    assert len(log) == 1
    e = log[0]
    assert set(e) >= {"timestamp", "relationship", "change_type", "field", "old", "new", "evidence", "approved_by", "auto_rule"}
    assert (e["relationship"], e["change_type"], e["field"], e["old"], e["new"]) == ("rel_example_eq_2025", "amount_changed", "amounts.funded", None, 250e6)
    assert e["approved_by"] == "Tester" and e["auto_rule"] is None and e["evidence"] == [new_id]
    import jsonschema
    jsonschema.Draft202012Validator(checks.schema("changelog_entry")).validate(e)
    assert (root.applied / f"{item['id']}.json").exists() and not list(root.approved.glob("*.json"))


def test_edit_then_approve_rechecks_the_edited_change(root, monkeypatch, helpers):
    item = queue_one(root, monkeypatch, helpers)
    bad = [dict(c) for c in item["diff"]]
    bad[0]["new"] = 999e6                                   # a figure the quote does not contain
    with pytest.raises(ValueError):
        review.approve(item["id"], root, by="Tester", edited_diff=bad)
    assert load_json(root.queue / f"{item['id']}.json")["state"] == "failed grounding"
    ok = review.approve(item["id"], root, by="Tester", edited_diff=item["diff"])
    assert ok["approval_record"]["edited"] is True


def test_reject_needs_a_reason_and_hold_keeps_the_item(root, monkeypatch, helpers):
    item = queue_one(root, monkeypatch, helpers)
    with pytest.raises(ValueError):
        review.reject(item["id"], " ", root)
    assert review.hold(item["id"], root)["state"] == "hold"
    with pytest.raises(ValueError):
        review.approve(item["id"], root, by="Tester")
    assert review.hold(item["id"], root, release=True)["state"] == "ready"
    review.reject(item["id"], "Duplicate of an earlier filing", root, by="Tester")
    assert (root.rejected / f"{item['id']}.json").exists() and triage.queue_items(root) == []


def market_hit(root, helpers, price=13.25):
    rel = next(r for r in load_json(root.register / "relationships.json") if r["id"] == "rel_example_eq_2025")
    q = {"price": price, "currency": "USD", "timestamp": datetime(2025, 3, 3, 21, 0, tzinfo=timezone.utc), "name": "Example Corp",
         "path": ROOT / helpers.FX / "example_quote.json", "url": "https://query2.finance.yahoo.com/v8/finance/chart/EXMP?interval=1d&range=5d"}
    ctx = base.Context("market_values", "2025-03-01", Paths(ROOT), TODAY)
    ev = market_values.evidence_for(ctx, q, "EXMP", rel["id"])
    return ctx.hit("market_value", f"{rel['id']}|2025-03-03T21:00:00Z", entity="ent_example", relationship=rel["id"], ticker="EXMP", date="2025-03-03",
                   source_url=q["url"], price=price, currency="USD", price_timestamp="2025-03-03T21:00:00Z", price_source="Yahoo Finance",
                   shares=20000000, value=20000000 * price, title="EXMP", evidence=[ev], diff=market_values.proposal(rel, q, ev))


def test_market_value_is_auto_approved_and_never_touches_last_verified(root, helpers):
    assert write_hits(root, "market_values", [market_hit(root, helpers)], TODAY) == 1
    assert write_hits(root, "market_values", [market_hit(root, helpers)], TODAY) == 0         # content hash: not written twice
    assert triage.run(root, today=TODAY)["queued"] == 1
    [item] = triage.queue_items(root)
    assert item["state"] == "ready", [c for c in item["checks"] if c["result"] != "pass"]
    assert item["needs_human"] is False and item["approval_reason"] == "auto rule: market_value"
    assert review.auto_approve(root) == [item["id"]]
    calls, step = steps_recorder()
    assert apply_approved.apply_all(root, today=TODAY, step=step) == 0
    reg = checks.Register(root.register)
    mv = reg.rel["rel_example_eq_2025"]["amounts"]["market_value"]
    assert mv["value"] == 265e6 and mv["price"] == 13.25 and mv["price_source"] == "Yahoo Finance" and mv["price_timestamp"] == "2025-03-03T21:00:00Z"
    assert mv["last_verified"] == "2025-03-04"                                               # no person re-checked anything
    assert reg.ev[mv["evidence"][0]]["tier"] == "market"
    checks.set_eligibility(reg)
    assert mv["display_eligible"] is True and checks.run_all(reg, today=TODAY) == []
    [e] = load_json(root.changelog)
    assert e["change_type"] == "market_value" and e["auto_rule"] == "market_value" and e["approved_by"] is None
    assert (e["old"], e["new"]) == (250e6, 265e6)


def test_review_page_lists_items_and_approves_only_with_the_session_token(root, monkeypatch, helpers):
    import threading
    import urllib.error
    import urllib.parse
    import urllib.request
    from http.server import ThreadingHTTPServer
    item = queue_one(root, monkeypatch, helpers)
    save_json(root.queue / "_spend.json", {"2025-03": 1.0})                 # bookkeeping, not a queue item
    srv = ThreadingHTTPServer(("127.0.0.1", 0), review.make_handler(root, "Tester", False, "tok123"))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{srv.server_address[1]}"
    try:
        page = urllib.request.urlopen(url + "/").read().decode()
        for text in ("Approve", "Edit then approve", "Reject", "Hold", "Batch confirm", "Now in the register", "Proposed",
                     "for an aggregate purchase price of $250 million", "Checks", "Critic notes", item["id"]):
            assert text in page
        assert "Nothing to confirm" in urllib.request.urlopen(url + "/batch").read().decode()
        post = lambda tok: urllib.request.urlopen(urllib.request.Request(url + "/approve", urllib.parse.urlencode({"id": item["id"], "token": tok}).encode()))
        with pytest.raises(urllib.error.HTTPError):
            post("wrong")
        assert not list(root.approved.glob("*.json"))
        post("tok123")
        assert load_json(root.approved / f"{item['id']}.json")["approval_record"]["by"] == "Tester"
    finally:
        srv.shutdown()
        srv.server_close()


def test_news_hits_are_ingested_only_from_tier_2_domains(root):
    from pipeline import ingest_news
    f = root.root / "hits.jsonl"
    good = {"url": "https://www.reuters.com/technology/example-2025-03-04/", "title": "Chip Vendor to invest $2 billion in Example Lab", "publisher": "Reuters",
            "published": "2025-03-04", "counterparty": "ent_examplelab", "keywords": ["invest"], "claim": "Reuters reports a $2 billion investment in Example Lab.",
            "sourcing": "anonymous", "cites_publisher": [], "paywalled": True, "search": "x"}
    f.write_text("\n".join([json.dumps(good), json.dumps({**good, "url": "https://medium.com/@x/y"}), "not json", json.dumps({"url": "https://www.ft.com/a"})]))
    res = ingest_news.ingest(f, root, TODAY)
    assert (res["accepted"], res["new"], len(res["refused"])) == (1, 1, 3)
    assert ingest_news.ingest(f, root, TODAY)["new"] == 0
    assert triage.run(root, today=TODAY)["queued"] == 1
    [item] = triage.queue_items(root)
    assert item["state"] == "needs quote" and item["match"]["entities"] == ["ent_examplelab"] and item["needs_human"] is True


def test_only_market_value_and_link_repair_can_skip_a_person():
    cfg = {"auto": ["market_value", "link_repair"]}
    ok = {"state": "ready", "checks": [], "change_type": "market_value", "diff": [{"path": "relationships/r/amounts/market_value/value", "old": 1, "new": 2}]}
    assert needs_human(ok, cfg)[0] is False
    for ct in ("added", "status_changed", "reconciliation_changed", "dates_changed", "corrected", "reverified", "evidence_added", "amount_changed"):
        assert needs_human({**ok, "change_type": ct}, cfg)[0] is True
    for field in ("headline", "committed_total", "funded", "contingent_max"):
        sneaky = {**ok, "diff": ok["diff"] + [{"path": f"relationships/r/amounts/{field}/value", "old": None, "new": 5}]}
        assert needs_human(sneaky, cfg)[0] is True
    assert needs_human({**ok, "diff": [{"path": "relationships/r/amounts/market_value/last_verified", "old": "a", "new": "b"}]}, cfg)[0] is True
    assert needs_human({**ok, "checks": [{"check": "grounding", "result": "fail"}]}, cfg)[0] is True
    assert needs_human({**ok, "state": "failed grounding"}, cfg)[0] is True
    link = {"state": "ready", "checks": [], "change_type": "link_repair", "diff": [{"path": "evidence/ev_1/url", "old": "https://a", "new": "https://b"}]}
    assert needs_human(link, cfg)[0] is False
    assert needs_human({**link, "diff": [{"path": "evidence/ev_1/quote", "old": "a", "new": "b"}]}, cfg)[0] is True


# ------------------------------------------------------------------ Gate U 2: a failure blocks publishing

def approve_directly(paths, item):
    """Put an item in data/approved/ as a commit would, bypassing the review page's own refusal."""
    item = {**item, "state": "ready", "approval_record": {"mode": "human", "by": "Tester", "rule": None, "at": "2025-03-10T12:00:00Z",
                                                            "rechecked": review.rechecked_amounts(item)}}
    (paths.queue / f"{item['id']}.json").unlink(missing_ok=True)
    save_json(paths.approved / f"{item['id']}.json", item)
    return item


def assert_blocked(paths, capsys, expect, **kw):
    before = snapshot(paths)
    calls, step = steps_recorder(**kw)
    assert apply_approved.apply_all(paths, today=TODAY, step=step) == 1
    assert expect in capsys.readouterr().err
    assert snapshot(paths) == before                       # published build, register, change log and approved items untouched
    assert load_json(paths.published / "summary.json") == PUBLISHED_SENTINEL
    assert not paths.applied.exists() or not list(paths.applied.glob("*.json"))
    return calls


def test_unreachable_source_blocks_apply(root, monkeypatch, helpers, capsys):
    item = queue_one(root, monkeypatch, helpers)
    item["evidence"][0]["cache_path"] = "research/cache/sec/1/000000000025000001/missing.htm"

    def unreachable(url):
        raise ConnectionError("simulated: sec.gov cannot be reached")
    monkeypatch.setattr(apply_approved, "fetch_source", unreachable)
    approve_directly(root, item)
    assert assert_blocked(root, capsys, "source unreachable") == []          # no pipeline step ran


def test_schema_failure_blocks_apply(root, monkeypatch, helpers, capsys):
    item = queue_one(root, monkeypatch, helpers, status="not_a_status")
    assert item["state"] == "failed checks" and any(c["check"] == "schema" and c["result"] == "fail" for c in item["checks"])
    with pytest.raises(ValueError):
        review.approve(item["id"], root, by="Tester")
    approve_directly(root, item)
    assert assert_blocked(root, capsys, "schema failure") == []


def test_grounding_failure_blocks_apply(root, monkeypatch, helpers, capsys):
    item = queue_one(root, monkeypatch, helpers, value=400e6)                # the quote says $250 million
    assert item["state"] == "failed grounding"
    with pytest.raises(ValueError):
        review.approve(item["id"], root, by="Tester")
    assert review.auto_approve(root) == []
    approve_directly(root, item)
    assert assert_blocked(root, capsys, "grounding failure") == []


def test_quote_missing_from_cached_source_blocks_apply(root, monkeypatch, helpers, capsys):
    item = queue_one(root, monkeypatch, helpers)
    item["evidence"][0]["quote"] = "for an aggregate purchase price of $251 million"
    item["diff"][0]["new"] = 251e6
    approve_directly(root, item)
    assert_blocked(root, capsys, "grounding failure")


def test_failed_publish_step_rolls_everything_back(root, monkeypatch, helpers, capsys):
    item = queue_one(root, monkeypatch, helpers)
    review.approve(item["id"], root, by="Tester")

    def scribble(module, paths):
        if module == "pipeline.publish":                   # a half-finished publish must not survive
            save_json(paths.published / "summary.json", {"data_as_of": "broken"})
            (paths.root / "data" / "history" / "2025-03-10T120000Z").mkdir(parents=True)
    calls = assert_blocked(root, capsys, "pipeline.publish", fail_at="pipeline.publish", scribble=scribble)
    assert calls == ["pipeline.build_register", "pipeline.system_view", "pipeline.publish"]      # build_site never ran
    assert not (root.root / "data" / "history" / "2025-03-10T120000Z").exists()
    assert (root.approved / f"{item['id']}.json").exists()                                       # still approved, ready to retry


def test_stale_register_value_blocks_apply(root, monkeypatch, helpers, capsys):
    item = queue_one(root, monkeypatch, helpers)
    review.approve(item["id"], root, by="Tester")
    rels = load_json(root.register / "relationships.json")
    next(r for r in rels if r["id"] == "rel_example_eq_2025")["amounts"]["funded"]["value"] = 1.0     # the register moved after drafting
    save_json(root.register / "relationships.json", rels)
    assert_blocked(root, capsys, "no longer holds the value")


def test_auto_approval_cannot_carry_a_human_only_change(root, monkeypatch, helpers, capsys):
    item = queue_one(root, monkeypatch, helpers)
    item = {**item, "approval_record": {"mode": "auto", "by": None, "rule": "market_value", "at": "2025-03-10T12:00:00Z", "rechecked": []}}
    (root.queue / f"{item['id']}.json").unlink()
    save_json(root.approved / f"{item['id']}.json", item)
    assert_blocked(root, capsys, "needs a person")


# ------------------------------------------------------------------ changes land in the research drafts the register is built from

def test_changes_are_written_to_the_draft_that_holds_the_record(root, monkeypatch, helpers):
    data = load_collections(root.register)
    save_json(root.drafts / "cluster_x.json", {"entities": data["entities"], "relationships": data["relationships"], "projects": [], "events": []})
    (root.evidence_dir).mkdir(parents=True)
    (root.evidence_dir / "_namespaces.json").write_text(json.dumps({"r1": 10000}))
    item = queue_one(root, monkeypatch, helpers)
    review.approve(item["id"], root, by="Tester")
    assert apply_approved.apply_all(root, today=TODAY, publish=False) == 0
    draft = load_json(root.drafts / "cluster_x.json")
    rel = next(r for r in draft["relationships"] if r["id"] == "rel_example_eq_2025")
    assert rel["amounts"]["funded"]["value"] == 250e6 and rel["version"] == 2
    assert rel["amounts"]["funded"]["evidence"] == ["ev_20001"]                 # a new namespace, clear of every research id
    [line] = [json.loads(l) for l in open(root.evidence_dir / "upd.jsonl")]
    assert line["id"] == "ev_20001"


# ------------------------------------------------------------------ staleness and batch confirm

def test_stale_amounts_queue_for_batch_confirm(root):
    later = date(2025, 5, 1)                                # the backstop is over $1 billion: 30 day limit
    res = base.execute(staleness, None, root, later)
    assert res["new"] >= 1
    hits = [json.loads(l) for l in open(root.inbox / later.isoformat() / "staleness.jsonl")]
    assert any(h["amount_path"] == "rel_example_bk_2025.amounts.contingent_max" and h["limit_days"] == 30 for h in hits)
    assert base.execute(staleness, None, root, later)["new"] == 0
    assert triage.run(root, today=later)["stale_items"] >= 1
    item = load_json(root.queue / "q_stale_rel_example_bk_2025.json")
    assert item["change_type"] == "reverified" and item["needs_human"] is True and item["batch_confirm"] is True
    assert review.auto_approve(root) == []                  # every re-verification needs a person
    done = review.batch_confirm(root, by="Tester")
    assert "q_stale_rel_example_bk_2025" in done
    calls, step = steps_recorder()
    assert apply_approved.apply_all(root, today=later, step=step) == 0
    rel = checks.Register(root.register).rel["rel_example_bk_2025"]
    confirmed = load_json(root.applied / "q_stale_rel_example_bk_2025.json")["approval_record"]["at"][:10]
    assert rel["amounts"]["contingent_max"]["last_verified"] == confirmed
    assert all(e["change_type"] == "reverified" and e["approved_by"] == "Tester" for e in load_json(root.changelog))


# ------------------------------------------------------------------ watchers: failures, timetable, never the register

def test_three_consecutive_failures_raise_an_alert_and_write_nothing(root, monkeypatch):
    def boom(ctx):
        raise ConnectionError("simulated: source unreachable")
    monkeypatch.setattr(staleness, "run", boom)
    before = snapshot(root)
    for n in (1, 2, 3):
        res = watch_run.run_watchers(["staleness"], paths=root, today=TODAY)
        assert res["failed"] == ["staleness"]
        st = load_json(root.status)["staleness"]
        assert st["consecutive_failures"] == n and st["alert"] is (n >= 3)
    assert watch_run.alerts(root) and "ALERT" in triage.pending_summary(root)
    assert snapshot(root) == before
    monkeypatch.undo()
    assert watch_run.run_watchers(["staleness"], paths=root, today=TODAY)["failed"] == []
    assert load_json(root.status)["staleness"]["alert"] is False


def test_timetable(root):
    et = lambda y, m, d, hh, mm: datetime(y, m, d, hh, mm, tzinfo=watch_run.ET)
    mon_0710 = et(2026, 11, 30, 7, 10)
    assert watch_run.is_due("fulltext_nvidia", mon_0710, {}, root)
    assert not watch_run.is_due("fulltext_nvidia", et(2026, 11, 30, 7, 5), {}, root)
    ran = {"fulltext_nvidia": {"last_run": "2026-11-30T12:10:30Z"}, "nvda_filings": {"last_run": "2026-11-30T12:10:30Z"}}
    assert not watch_run.is_due("fulltext_nvidia", et(2026, 11, 30, 18, 0), ran, root)
    assert not watch_run.is_due("nvda_filings", et(2026, 11, 30, 8, 10), ran, root)          # every 2 hours
    assert watch_run.is_due("nvda_filings", et(2026, 11, 30, 9, 10), ran, root)
    assert not watch_run.is_due("nvda_filings", et(2026, 11, 28, 9, 10), {}, root)            # Saturday
    assert not watch_run.is_due("nvda_filings", et(2026, 11, 30, 23, 30), {}, root)           # after 10 pm
    save_json(root.inbox / "_earnings.json", {"nvidia_last": "2026-11-25"})
    assert watch_run.is_due("nvda_filings", et(2026, 11, 30, 8, 10), ran, root)               # hourly for ten days after earnings
    assert not watch_run.is_due("market_values", et(2026, 11, 30, 15, 0), {}, root)
    assert watch_run.is_due("market_values", et(2026, 11, 30, 16, 40), {}, root)
    assert set(watch_run.SCHEDULE) == set(watch_run.WATCHERS)


def test_every_watcher_module_has_the_shared_shape():
    for name in watch_run.WATCHERS:
        m = watch_run.module(name)
        assert m.NAME == name and m.LOOKBACK_DAYS >= 1 and callable(m.run)
        src = (ROOT / "pipeline" / "watchers" / f"{name}.py").read_text()
        assert "import requests" not in src and "requests.get" not in src       # SEC and web pages only through edgar and cache
        assert "save_json(REGISTER" not in src and "PUBLISHED" not in src


def test_diff_refuses_a_change_drafted_against_an_older_value(root):
    data = load_collections(root.register)
    p = "relationships/rel_example_bk_2025/status"
    assert get_path(apply_diff(data, [{"path": p, "old": "definitive", "new": "terminated"}]), p) == "terminated"
    assert get_path(data, p) == "definitive"                # the original is never changed in place
    with pytest.raises(ValueError):
        apply_diff(data, [{"path": p, "old": "restructured", "new": "terminated"}])


def test_spend_cap_null_means_the_paid_step_does_not_run(root):
    save_json(root.config / "limits.json", {"monthly_usd_cap": None})
    assert triage.budget(root, TODAY)["may_run"] is False
    save_json(root.config / "limits.json", {"monthly_usd_cap": 20})
    assert triage.budget(root, TODAY)["remaining"] == 20
    f = root.root / "result.json"
    f.write_text(json.dumps({"total_cost_usd": 20.5}))
    triage.record_spend(f, root, TODAY)
    b = triage.budget(root, TODAY)
    assert b["may_run"] is False and "ALERT" in b["message"]


def test_workflows_share_one_concurrency_group_and_commit_no_secret():
    import re
    wf = sorted((ROOT / ".github" / "workflows").glob("*.yml"))
    assert {f.name for f in wf} >= {"watch.yml", "triage.yml", "publish.yml", "checks.yml", "ingest_news.yml"}
    groups = set()
    for f in wf:
        text = f.read_text()
        assert "workflow_dispatch:" in text and "schedule:" in text and "cron:" in text, f.name
        m = re.search(r"concurrency:\s*\n\s+group:\s*(\S+)", text)
        assert m, f.name
        groups.add(m.group(1))
        assert "cancel-in-progress: false" in text
        for name in re.findall(r"(SEC_USER_AGENT|ANTHROPIC_API_KEY|PUBLIC_REPO_TOKEN):\s*(\S+)", text):
            assert name[1].startswith("${{"), f"{f.name}: {name[0]} must come from repository secrets"
    assert len(groups) == 1
