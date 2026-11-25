"""Build data/published/ from data/register/ (spec/11 U4 steps 4 to 7).

  python3 -m pipeline.publish            rebuild, check, snapshot, swap in
  python3 -m pipeline.publish --dry-run  rebuild and check into data/published.tmp only

Rules:
- Totals, derived measures, scenarios and summary sentences are recomputed from the register, never patched.
- An amount that fails the display rule is published without its number ("Not confirmed").
- The public change log never shows an ineligible value and never names the approver.
- Every check runs against the new build first. Any failure stops the publish and leaves the live data unchanged.
- Each publish is snapshotted to data/history/<UTC timestamp>/.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import date, datetime, timezone
from pathlib import Path

from . import checks, fmt, measure
from .checks import Register, elig_value, independent_gross, independent_totals, is_stale, set_eligibility
from .common import CONFIG, PUBLISHED, REGISTER, ROOT, load_json, save_json

HISTORY = ROOT / "data" / "history"
CHANGELOG = ROOT / "data" / "changelog.json"
EV_PUBLIC = ("id", "tier", "kind", "publisher", "title", "url", "source_link", "accession", "section", "published", "retrieved", "quote", "sourcing", "paywalled")
ENTITY_PUBLIC = ("id", "name", "short_name", "cluster", "depth", "public", "ticker", "country", "description")
TYPE_LABELS = {"EQ": "Equity", "EQ-SPV": "Vehicle equity", "EQ-C": "Conditional equity", "BK": "Capacity backstop", "LB": "Capacity rental",
               "GU": "Guarantee", "RV": "Residual value support", "FC": "Financing", "LP": "Fund commitment", "PP": "Supply prepayment",
               "LI": "License", "CX": "Context"}
STATUS_LABELS = {"definitive": "Definitive", "loi_or_framework": "Letter of intent", "reported_unconfirmed": "Reported, unconfirmed",
                 "restructured": "Restructured", "terminated": "Terminated", "completed": "Completed"}
BASIS_LABELS = {"filed": "Filed", "company_announced": "Company announced", "reported_corroborated": "Reported, two sources",
                "reported_single_source": "Reported, one source"}
CLUSTER_LABELS = {"ai_lab": "AI labs", "neocloud": "Neoclouds", "hyperscaler": "Hyperscalers and offtakers", "semis_supply": "Semis and supply",
                  "sovereign_project": "Sovereign and projects", "vehicle": "Sovereign and projects", "portfolio": "Portfolio",
                  "lender": "Lenders", "other": "Other and unattributed", "nvidia": "Nvidia"}


def public_amount(a: dict | None, field: str, rel: dict, cfg_stale: dict, today: date) -> dict | None:
    if not isinstance(a, dict):
        return None
    out = {k: a.get(k) for k in ("as_of", "fiscal_period", "original_currency", "last_verified", "display_eligible", "not_applicable",
                                 "trigger", "price_source", "price_timestamp", "qualifier", "in_force", "effective_note", "lower_bound")
           if a.get(k) is not None}
    out["evidence"] = list(dict.fromkeys((a.get("evidence") or []) + [i for c in a.get("components") or [] for i in c["evidence"]]))
    out["text"] = fmt.amount_text(a)
    if a.get("not_applicable"):
        out["value"] = 0
    elif a.get("display_eligible"):
        out["value"] = a.get("value")
        if a.get("original_currency", "USD") != "USD":
            out["original_value"] = a.get("original_value")
    else:
        out["value"] = None
        out["status"] = "not_disclosed" if a.get("value") is None and a.get("original_value") is None else "not_confirmed"
    if out.get("value") and a.get("display_eligible") and is_stale(a, rel, cfg_stale, today):
        out["stale"] = True
    if a.get("note") and a.get("display_eligible"):
        out["note"] = a["note"]
    if a.get("floor") and a.get("floor_note"):
        out["floor"] = {"value": a["floor"], "as_of": a.get("floor_as_of"), "note": a["floor_note"]}
    return out


def public_relationship(r: dict, reg: Register, show_grades: bool, cfg_stale: dict, today: date) -> dict:
    g = independent_gross(r)
    d = r.get("derived") or {}
    text, _ = fmt.render_insight(r["insight_template"], r, reg.ent)
    out = {k: r.get(k) for k in ("id", "to", "type_primary", "types_secondary", "title", "definition", "status", "claim_basis", "dates",
                                 "seniority", "reconciliation", "consequences", "projects", "depth2_links", "aggregate_of", "version",
                                 "evidence", "holding", "inclusion_reason")}
    out["insight"] = text
    out["labels"] = {"type": TYPE_LABELS[r["type_primary"]], "status": STATUS_LABELS[r["status"]], "basis": BASIS_LABELS[r["claim_basis"]],
                     "cluster": CLUSTER_LABELS.get(reg.ent[r["to"]]["cluster"], "Other and unattributed")}
    out["amounts"] = {k: public_amount(a, k, r, cfg_stale, today) for k, a in r["amounts"].items()}
    out["credit"] = {k: r["credit"].get(k) for k in ("wwr", "wwr_reason", "collateral", "tenor", "notes", "tenor_bucket") if r["credit"].get(k)}
    out["notes"] = r.get("notes")
    out["exposure"] = {"funded": g["funded"], "funded_cash": g["funded_cash"], "committed_unfunded": g["committed_unfunded"],
                       "committed_split_unknown": g["committed_split_unknown"], "contingent_max": g["contingent_max"],
                       "contingent_in_force": g["contingent_in_force"], "contingent_not_in_force": g["contingent_not_in_force"],
                       "gross": g["gross"], "missing": g["missing"], "lower_bound": g["lower_bound"]}
    keep = ("ead_base", "ead_base_note", "ead_max", "loss_max", "loss_max_note", "loss_base", "loss_base_note", "circularity_ratio",
            "round_trip", "share_of_counterparty_capital", "share_of_nvda_equity", "share_of_nvda_fcf", "annual_obligation", "backstop_coverage")
    out["derived"] = {k: d.get(k) for k in keep if k in d}
    out["significance"] = r.get("significance")
    if not show_grades:
        pass   # grades live on entities and are dropped there
    return out


def public_entity(e: dict, show_grades: bool) -> dict:
    out = {k: e.get(k) for k in ENTITY_PUBLIC}
    c = e.get("credit") or {}
    if c:
        cp = {k: c.get(k) for k in ("public_ratings", "debt_outstanding", "maturities_24m", "cash_and_undrawn", "committed_spend_12m",
                                    "liquidity_months", "top_customer_share", "top3_customer_share", "collateral_note", "market_signals", "notes") if c.get(k)}
        for k in ("debt_outstanding", "maturities_24m", "cash_and_undrawn", "committed_spend_12m"):
            a = cp.get(k)
            if isinstance(a, dict):
                cp[k] = {"value": a.get("value") if a.get("display_eligible") else None, "text": fmt.amount_text(a), "as_of": a.get("as_of"),
                         "evidence": a.get("evidence") or [i for x in a.get("components") or [] for i in x["evidence"]],
                         "lower_bound": a.get("lower_bound"), "note": a.get("note") if a.get("display_eligible") else None}
        if show_grades:
            cp["grade"], cp["grade_reason"] = c.get("grade"), c.get("grade_reason")
        out["credit"] = cp
    if e.get("compute_commitments"):
        out["compute_commitments"] = [{"counterparty": x["counterparty"], "description": x["description"], "kind": x.get("kind"),
                                       "amount": {"text": fmt.amount_text(x["amount"]), "as_of": x["amount"].get("as_of"), "evidence": x["amount"].get("evidence") or []}}
                                      for x in e["compute_commitments"]]
    return out


def public_complex(c: dict, reg: Register) -> dict:
    out = {k: c.get(k) for k in ("id", "kind", "provider", "beneficiary", "obligor", "instrument", "description", "status", "claim_basis",
                                 "trigger", "dates", "same_capacity_as_nvidia", "nvidia_links", "same_obligation_as", "evidence")}
    out["amounts"] = {k: {"text": fmt.amount_text(a), "value": a.get("value") if a.get("display_eligible") else None, "as_of": a.get("as_of"),
                          "evidence": a.get("evidence") or []} for k, a in (c.get("amounts") or {}).items() if isinstance(a, dict)}
    return out


def summary_sentences(reg: Register, t: dict, sv: dict) -> list[dict]:
    m = fmt.money
    hg = t["headline_groups"]
    s = []
    s.append({"text": f"This register finds {t['count']} financial relationships in which Nvidia has put money, credit or demand behind companies in the AI buildout, and every number on this page links to its source.",
              "figures": [{"value": t["count"], "eligible_only": True}]})
    s.append({"text": f"Of the amounts that can be confirmed, {m(t['funded'])} is invested and still held, {m(t['committed_unfunded'] + t['committed_split_unknown'])} is committed, and {m(t['contingent_max'])} is contingent on events such as a tenant's default.",
              "figures": [{"value": t["funded"], "eligible_only": True}, {"value": t["committed_unfunded"] + t["committed_split_unknown"], "eligible_only": True}, {"value": t["contingent_max"], "eligible_only": True}]})
    nif = [r for r in reg.relationships if not r.get("aggregate_of") and independent_gross(r)["contingent_not_in_force"]]
    if nif:
        big = max(nif, key=lambda r: independent_gross(r)["contingent_not_in_force"])
        s.append({"text": f"{m(t['contingent_not_in_force'])} of the contingent amount is a guaranty of {reg.ent[big['to']]['short_name']}'s rent that is signed but not yet in force.",
                  "figures": [{"value": t["contingent_not_in_force"], "eligible_only": True}]})
    s.append({"text": f"Announcements add up to {m(t['headline'])}, which is never counted as exposure; {m(hg['not_binding'])} of it is letters of intent or deals with no disclosed agreement.",
              "figures": [{"value": t["headline"], "eligible_only": True}, {"value": hg["not_binding"], "eligible_only": True}]})
    eqrow = next((b for b in sv.get("bridge", []) if b["line"].startswith("Equity purchases")), None)
    if eqrow and eqrow.get("nvidia"):
        s.append({"text": f"Nvidia's own accounts show more than any outsider can name: it paid {m(eqrow['nvidia'])} for equity in the nine months to 25 October 2026, and this register can tie {m(eqrow['named'])} of that to named deals.",
                  "figures": [{"value": eqrow["nvidia"], "eligible_only": True}, {"value": eqrow["named"], "eligible_only": True}]})
    return s


def public_changelog(entries: list[dict], reg: Register) -> list[dict]:
    out = []
    for e in entries:
        x = {k: e.get(k) for k in ("timestamp", "relationship", "change_type", "field", "old", "new", "evidence")}
        rel = reg.rel.get(e.get("relationship"))
        if rel:
            x["title"] = rel["title"]
            x["counterparty"] = reg.ent[rel["to"]]["short_name"]
        field = (e.get("field") or "").split(".")[-1]
        if rel and field in rel["amounts"]:
            a = rel["amounts"][field]
            if not a.get("display_eligible"):
                x["old"] = x["new"] = "Not confirmed"
        for k in ("old", "new"):
            if isinstance(x[k], (int, float)) and not isinstance(x[k], bool) and abs(x[k]) >= 1000:
                x[k] = fmt.money(x[k])
            elif isinstance(x[k], (dict, list)):
                x[k] = json.dumps(x[k])[:200]
        out.append(x)
    return sorted(out, key=lambda x: x["timestamp"] or "", reverse=True)


def seed_changelog(reg: Register) -> list[dict]:
    """First publish: one 'added' entry per relationship, plus any refresh changes logged before launch."""
    log = load_json(CHANGELOG, [])
    if log:
        seen = {(e["timestamp"], e["relationship"], e.get("field"), e["change_type"]) for e in log}
        added = [e for f in sorted((ROOT / "research" / "refresh").glob("changes_*.json")) for e in load_json(f, [])
                 if (e["timestamp"], e["relationship"], e.get("field"), e["change_type"]) not in seen]
        if added:
            log += added
            save_json(CHANGELOG, log)
        return log
    ts = "2026-11-25T00:00:00Z"
    for r in reg.relationships:
        log.append({"timestamp": ts, "relationship": r["id"], "change_type": "added", "field": None, "old": None, "new": r["title"],
                    "evidence": r["evidence"][:3], "approved_by": "Thomas (Gate R approval, 2026-11-25)", "auto_rule": None})
    for f in sorted((ROOT / "research" / "refresh").glob("changes_*.json")):
        log += load_json(f, [])
    save_json(CHANGELOG, log)
    return log


def build(out_dir: Path, today: date | None = None) -> dict:
    today = today or date.today()
    reg = Register()
    set_eligibility(reg)
    measure.run(reg, today)
    reg.save()
    from . import system_view
    sv = system_view.build(reg, today)
    save_json(REGISTER / "system_view.json", sv)
    display = load_json(CONFIG / "display.json")
    show_grades = bool(display.get("show_grades"))
    cfg_stale = load_json(CONFIG / "staleness.json")
    t = independent_totals(reg)
    core = [r for r in reg.relationships if not r.get("aggregate_of") and r["type_primary"] != "CX"]

    rels = [public_relationship(r, reg, show_grades, cfg_stale, today) for r in reg.relationships]
    used_ents = {r["to"] for r in reg.relationships} | {"ent_nvidia"} | {l["entity"] for r in reg.relationships for l in r.get("depth2_links") or []}
    used_ents |= {e for c in reg.complex for e in (c["provider"], c["beneficiary"], c["obligor"])}
    used_ents |= {x["counterparty"] for e in reg.entities for x in e.get("compute_commitments") or []}
    ents = [public_entity(e, show_grades) for e in reg.entities if e["id"] in used_ents]
    cx = [public_complex(c, reg) for c in reg.complex]
    loops = load_json(REGISTER / "loops.json", [])
    cb = load_json(REGISTER / "central_bank.json", {})

    cited = set()
    for coll in (rels, ents, reg.projects, reg.events, cx, loops, [cb]):
        cited |= set(checks._ev_ids(coll))
    cited |= set(__import__("re").findall(r"ev_\d+", json.dumps([loops, cb, rels])))
    evid = [{k: e.get(k) for k in EV_PUBLIC} for e in reg.evidence if e["id"] in cited]

    log = seed_changelog(reg)
    pub_log = public_changelog(log, reg)
    sentences = summary_sentences(reg, t, sv)
    last_change = max((e["timestamp"] for e in log), default=None)
    totals_pub = {k: t[k] for k in ("funded", "funded_cash", "committed_unfunded", "committed_split_unknown", "contingent_max",
                                    "contingent_in_force", "contingent_not_in_force", "headline", "gross", "count", "lower_bound_count",
                                    "counts", "headline_groups", "headline_not_converted")}
    summary = {"data_as_of": today.isoformat(), "last_change": last_change, "totals": totals_pub, "sentences": sentences,
               "included_ids": [r["id"] for r in core], "bridge": sv["bridge"], "positions_by_value": sv["positions_by_value"],
               "positions_not_yet_valued": sv["positions_not_yet_valued"], "source_mix": sv["source_mix"],
               "top_concentrations": sv["top_concentrations"], "by_type": sv["by_type"], "by_cluster": sv["by_cluster"],
               "financials": {k: public_amount(a, k, {}, cfg_stale, today) for k, a in reg.financials.items() if isinstance(a, dict) and "value" in a},
               "display": display}
    if show_grades:
        summary["by_grade"] = sv["by_grade"]
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, obj in (("relationships.json", rels), ("entities.json", ents), ("evidence.json", evid), ("projects.json", reg.projects),
                      ("events.json", reg.events), ("complex_links.json", cx), ("loops.json", loops), ("central_bank.json", cb),
                      ("scenarios.json", {**sv["scenarios"], "config": load_json(CONFIG / "scenarios.json")}), ("summary.json", summary),
                      ("changelog.json", pub_log)):
        save_json(out_dir / name, obj)
    return {"reg": reg, "totals": t}


def publish(dry_run=False, today=None) -> int:
    tmp = PUBLISHED.with_name("published.tmp")
    if tmp.exists():
        shutil.rmtree(tmp)
    b = build(tmp, today)
    probs = checks.run_all(Register(), tmp, None)
    for p in probs:
        print("FAIL", p)
    if probs:
        print(f"\nPublish stopped: {len(probs)} problem(s). data/published/ is unchanged.")
        return 1
    if dry_run:
        print(f"Dry run passed. Build left in {tmp.relative_to(ROOT)}.")
        return 0
    if PUBLISHED.exists():
        shutil.rmtree(PUBLISHED)
    tmp.rename(PUBLISHED)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    shutil.copytree(PUBLISHED, HISTORY / stamp)
    t = b["totals"]
    print(f"Published {t['count']} counted relationships; gross at least {fmt.money(t['gross'])}. Snapshot data/history/{stamp}/")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    sys.exit(publish(args.dry_run))


if __name__ == "__main__":
    main()
