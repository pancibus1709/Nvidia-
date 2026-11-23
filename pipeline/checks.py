"""Every automated check in spec/09. `make check` runs this over data/register and data/published.

  python3 -m pipeline.checks                 check the register (and the published build if present)
  python3 -m pipeline.checks draft <file>    check a research draft {entities, relationships, projects, events}
  python3 -m pipeline.checks eligibility     write display_eligible on every amount in the register
  python3 -m pipeline.checks links           weekly link check (network)

Display eligibility is computed here and nowhere else: an amount is eligible only if a tier 1
source or two independent tier 2 sources contain the number (grounded in the cached copy).
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

import jsonschema

from . import fmt, xbrl
from .common import (BANNED_DASHES, CONFIG, PUBLISHED, REGISTER, ROOT, SCHEMA, allowlist, classify_domain, doc_text,
                     enums, load_json, norm, save_json, sha256_file, table_scale, value_in_text, word_count)

WINDOW = 300
AMOUNT_FIELDS = ("headline", "committed_total", "funded", "contingent_max", "annual_obligation", "market_value", "carrying_value")
GROSS_FIELDS = ("funded", "committed_unfunded", "contingent_max")


# ------------------------------------------------------------------ loading

def _expand(node):
    if isinstance(node, dict):
        if "$enum" in node:
            return {"enum": enums()[node["$enum"]]}
        return {k: _expand(v) for k, v in node.items()}
    if isinstance(node, list):
        return [_expand(v) for v in node]
    return node


_schemas: dict = {}


def schema(name: str) -> dict:
    if name not in _schemas:
        _schemas[name] = _expand(load_json(SCHEMA / f"{name}.schema.json"))
    return _schemas[name]


class Register:
    def __init__(self, directory=REGISTER, extra_evidence=None):
        d = Path(directory)
        self.dir = d
        self.entities = load_json(d / "entities.json", [])
        self.relationships = load_json(d / "relationships.json", [])
        self.evidence = load_json(d / "evidence.json", [])
        self.projects = load_json(d / "projects.json", [])
        self.events = load_json(d / "events.json", [])
        self.financials = load_json(d / "nvidia_financials.json", {})
        if extra_evidence:
            self.evidence = self.evidence + extra_evidence
        self.index()

    def index(self):
        self.ev = {e["id"]: e for e in self.evidence}
        self.ent = {e["id"]: e for e in self.entities}
        self.rel = {r["id"]: r for r in self.relationships}

    def save(self):
        save_json(self.dir / "relationships.json", self.relationships)
        save_json(self.dir / "entities.json", self.entities)
        save_json(self.dir / "projects.json", self.projects)
        if self.financials:
            save_json(self.dir / "nvidia_financials.json", self.financials)


def iter_amounts(reg: Register):
    """Yield (path, field, amount, owner_record) for every amount object in the register."""
    for r in reg.relationships:
        for k, a in (r.get("amounts") or {}).items():
            if isinstance(a, dict):
                yield f"{r['id']}.amounts.{k}", k, a, r
        for k, a in (r.get("measure_inputs") or {}).items():
            if isinstance(a, dict) and "value" in a:
                yield f"{r['id']}.measure_inputs.{k}", k, a, r
        for i, l in enumerate(r.get("depth2_links") or []):
            if isinstance(l.get("amount"), dict):
                yield f"{r['id']}.depth2_links[{i}].amount", "depth2", l["amount"], r
    for e in reg.entities:
        c = e.get("credit") or {}
        for k in ("debt_outstanding", "maturities_24m", "cash_and_undrawn", "committed_spend_12m"):
            if isinstance(c.get(k), dict):
                yield f"{e['id']}.credit.{k}", k, c[k], e
        for i, cc in enumerate(e.get("compute_commitments") or []):
            yield f"{e['id']}.compute_commitments[{i}].amount", "compute_commitment", cc["amount"], e
    for p in reg.projects:
        for i, f in enumerate(p.get("financing") or []):
            for k in ("balance", "collateral_value"):
                if isinstance(f.get(k), dict):
                    yield f"{p['id']}.financing[{i}].{k}", k, f[k], p
    for k, a in (reg.financials or {}).items():
        if isinstance(a, dict) and "value" in a and "evidence" in a:
            yield f"nvidia_financials.{k}", k, a, reg.financials


# ------------------------------------------------------------------ grounding

_ground_cache: dict = {}


def ground_evidence(ev: dict) -> list[str]:
    """Problems with one evidence record's grounding. Empty list = grounded."""
    key = (ev["id"], ev.get("content_hash"), ev.get("quote"), ev.get("locator"))
    if key in _ground_cache:
        return _ground_cache[key]
    probs = []
    path = ROOT / ev["cache_path"]
    if not path.exists():
        probs.append(f"cached file missing: {ev['cache_path']}")
    elif sha256_file(path) != ev["content_hash"]:
        probs.append("cached file hash differs from content_hash")
    elif str(ev["locator"]).startswith("xbrl:"):
        if xbrl.lookup(path, ev["locator"]) is None:
            probs.append("XBRL fact id does not resolve in the cached company facts")
    else:
        text = doc_text(path)
        if norm(ev["quote"]) not in text:
            probs.append("quote not found verbatim in the cached source")
    _ground_cache[key] = probs
    return probs


def evidence_contains(ev: dict, value: float) -> bool:
    """True if the number appears in the quote or within 300 characters of the locator.

    A negative value is a component being subtracted (unattributed remainders): the source states it as a positive figure.
    """
    value = abs(value)
    path = ROOT / ev["cache_path"]
    if not path.exists():
        return False
    if str(ev["locator"]).startswith("xbrl:"):
        v = xbrl.lookup(path, ev["locator"])
        return v is not None and abs(v - value) <= 5e-4 * max(abs(value), 1)
    text = doc_text(path)
    q = norm(ev["quote"])
    try:
        loc = int(ev["locator"])
    except (TypeError, ValueError):
        loc = text.find(q)
    if text[loc: loc + len(q)] != q:
        loc = text.find(q)
        if loc < 0:
            return False
    scale = None
    usl = ev.get("unit_scale_locator")
    if usl is not None:
        scale = table_scale(text[usl: usl + 80])
    window = text[max(0, loc - WINDOW): loc + len(q) + WINDOW]
    return value_in_text(value, window, scale)


def amount_parts(a: dict) -> list[tuple[float, list[str]]]:
    """(value, evidence ids) pairs that must each be grounded. Components if present, else the amount itself."""
    if a.get("components"):
        return [(c["value"], c["evidence"]) for c in a["components"]]
    v = a.get("original_value") if a.get("original_currency", "USD") != "USD" and a.get("original_value") is not None else a.get("value")
    return [(v, a.get("evidence") or [])]


def native_only(a: dict) -> bool:
    """A non-USD amount with no sourced exchange rate: shown in its own currency, never added to a USD total."""
    return a.get("value") is None and a.get("original_value") is not None and a.get("original_currency", "USD") != "USD"


def supporting(reg: Register, value, ids) -> list[dict]:
    """Evidence records among `ids` that are grounded and contain the value."""
    out = []
    for i in ids:
        ev = reg.ev.get(i)
        if ev and not ground_evidence(ev) and evidence_contains(ev, value):
            out.append(ev)
    return out


def _independent_pair(evs: list[dict]) -> bool:
    for i, a in enumerate(evs):
        for b in evs[i + 1:]:
            if a.get("parent_company") and a.get("parent_company") == b.get("parent_company"):
                continue
            if a["publisher"] in (b.get("cites_publisher") or []) or b["publisher"] in (a.get("cites_publisher") or []):
                continue
            return True
    return False


def eligible(reg: Register, field: str, a: dict) -> bool:
    """The display rule (spec/04). Tier 1, or two independent tier 2, or market data for market_value only."""
    if a.get("not_applicable"):
        return False
    if a.get("value") is None and not native_only(a):
        return False
    if not a.get("as_of"):
        return False
    for value, ids in amount_parts(a):
        evs = supporting(reg, value, ids)
        t1 = [e for e in evs if e["tier"] == "1"]
        t2 = [e for e in evs if e["tier"] == "2" and not (e.get("paywalled") and not e.get("pasted_by_reviewer"))]
        mk = [e for e in evs if e["tier"] == "market"]
        ok = bool(t1) or _independent_pair(t2) or (field == "market_value" and bool(mk) and bool(a.get("price_timestamp")) and bool(a.get("price_source")))
        if not ok:
            return False
    return True


def set_eligibility(reg: Register) -> int:
    n = 0
    for path, field, a, _ in iter_amounts(reg):
        e = eligible(reg, field, a)
        if a.get("display_eligible") != e:
            a["display_eligible"] = e
            n += 1
    return n


# ------------------------------------------------------------------ independent arithmetic

def elig_value(a):
    if not isinstance(a, dict):
        return None
    if a.get("not_applicable"):
        return 0.0
    if a.get("value") is None or not a.get("display_eligible"):
        return None
    return float(a["value"])


def independent_gross(r: dict) -> dict:
    """Recompute committed_unfunded and gross from eligible amounts only. Deliberately separate from measure.py."""
    am = r["amounts"]
    funded, committed, cont = elig_value(am.get("funded")), elig_value(am.get("committed_total")), elig_value(am.get("contingent_max"))
    if committed is not None and funded is not None and not am["committed_total"].get("not_applicable"):
        unfunded = max(0.0, committed - funded)
    elif r["status"] == "completed" and funded is not None:
        unfunded = 0.0
    elif am["committed_total"].get("not_applicable") and funded is not None:
        unfunded = 0.0
    elif committed is not None and funded is None and not am["committed_total"].get("not_applicable"):
        unfunded = committed   # paid portion not disclosed: the committed total counts once, as not yet confirmed paid
    else:
        unfunded = None
    split_unknown = unfunded is not None and funded is None
    parts = {"funded": funded, "committed_unfunded": unfunded, "contingent_max": cont}
    return {**parts, "gross": sum(v for v in parts.values() if v is not None),
            "missing": [k for k, v in parts.items() if v is None and not (k == "funded" and split_unknown)]}


def independent_totals(reg: Register, rel_filter=None) -> dict:
    t = {"funded": 0.0, "committed_unfunded": 0.0, "contingent_max": 0.0, "headline": 0.0, "gross": 0.0,
         "count": 0, "lower_bound_count": 0, "counts": {"funded": 0, "committed_unfunded": 0, "contingent_max": 0, "headline": 0}}
    for r in reg.relationships:
        if r.get("aggregate_of") or r["type_primary"] == "CX":
            continue
        if rel_filter and not rel_filter(r):
            continue
        g = independent_gross(r)
        t["count"] += 1
        for k in GROSS_FIELDS:
            if g[k]:
                t[k] += g[k]
                t["counts"][k] += 1
        t["gross"] += g["gross"]
        if g["missing"]:
            t["lower_bound_count"] += 1
        h = elig_value(r["amounts"].get("headline"))
        if h and not r["amounts"]["headline"].get("not_applicable"):
            t["headline"] += h
            t["counts"]["headline"] += 1
    return t


# ------------------------------------------------------------------ the checks

def check_schema(reg):
    out = []
    for name, rows in (("entity", reg.entities), ("relationship", reg.relationships), ("evidence", reg.evidence), ("project", reg.projects), ("event", reg.events)):
        v = jsonschema.Draft202012Validator(schema(name))
        seen = set()
        for row in rows:
            rid = row.get("id", "?")
            if rid in seen:
                out.append(f"schema: duplicate id {rid}")
            seen.add(rid)
            for err in v.iter_errors(row):
                out.append(f"schema: {rid}: {'/'.join(str(p) for p in err.absolute_path)}: {err.message[:160]}")
    for r in reg.relationships:
        for end in ("from", "to"):
            if r[end] not in reg.ent:
                out.append(f"schema: {r['id']}: {end} entity {r[end]} does not exist")
        if r["type_primary"] == "LI" and not r.get("inclusion_reason"):
            out.append(f"schema: {r['id']}: a license record needs inclusion_reason")
        for l in r.get("depth2_links") or []:
            if l["entity"] not in reg.ent:
                out.append(f"schema: {r['id']}: depth-2 entity {l['entity']} does not exist")
    for p in reg.projects:
        if p["entity"] not in reg.ent:
            out.append(f"schema: {p['id']}: entity {p['entity']} does not exist")
    for e in reg.events:
        if e["relationship"] not in reg.rel:
            out.append(f"schema: event {e['id']}: relationship {e['relationship']} does not exist")
    return out


def _ev_ids(node):
    """Every evidence id referenced anywhere inside a record."""
    found = []
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ("evidence", "nvidia_evidence", "counterparty_evidence", "fx_evidence") and isinstance(v, list):
                found += [x for x in v if isinstance(x, str)]
            else:
                found += _ev_ids(v)
    elif isinstance(node, list):
        for v in node:
            found += _ev_ids(v)
    return found


def check_evidence_resolution(reg):
    out = []
    for coll in (reg.relationships, reg.entities, reg.projects, reg.events):
        for row in coll:
            for i in _ev_ids(row):
                if i not in reg.ev:
                    out.append(f"evidence: {row['id']}: evidence id {i} does not resolve")
    for path, field, a, _ in iter_amounts(reg):
        if a.get("value") is not None and not a.get("not_applicable"):
            if not any(ids for _, ids in amount_parts(a)):
                out.append(f"evidence: {path}: non-null amount has no evidence")
    for r in reg.relationships:
        if not r.get("evidence") and not r.get("aggregate_of"):
            out.append(f"evidence: {r['id']}: relationship has no evidence")
    return out


def check_grounding(reg):
    out = []
    for ev in reg.evidence:
        for p in ground_evidence(ev):
            out.append(f"grounding: {ev['id']}: {p}")
    for path, field, a, _ in iter_amounts(reg):
        if a.get("not_applicable") or (a.get("value") is None and not native_only(a)):
            continue
        parts = amount_parts(a)
        if a.get("components"):
            total = sum(c["value"] for c in a["components"])
            if a.get("value") is not None and abs(total - a["value"]) > 5e-4 * max(abs(a["value"]), 1):
                out.append(f"grounding: {path}: components sum to {total}, value is {a['value']}")
        for value, ids in parts:
            for i in ids:
                ev = reg.ev.get(i)
                if ev and not ground_evidence(ev) and not evidence_contains(ev, value):
                    out.append(f"grounding: {path}: {value:,.6g} does not appear in the quote or within {WINDOW} characters of the locator of {i}")
        if a.get("original_currency", "USD") != "USD" and a.get("fx_rate"):
            if not a.get("fx_evidence"):
                out.append(f"grounding: {path}: fx_rate has no evidence")
            elif not supporting(reg, a["fx_rate"], a["fx_evidence"]):
                out.append(f"grounding: {path}: fx_rate {a['fx_rate']} not found in its evidence")
    return out


def check_display_rule(reg):
    out = []
    for path, field, a, _ in iter_amounts(reg):
        want = eligible(reg, field, a)
        if bool(a.get("display_eligible")) != want:
            out.append(f"display: {path}: display_eligible is {a.get('display_eligible')} but the rule gives {want}. Run `python3 -m pipeline.checks eligibility`.")
    for r in reg.relationships:
        if r["claim_basis"] == "reported_single_source":
            if r["status"] != "reported_unconfirmed":
                out.append(f"display: {r['id']}: single-source claim must have status reported_unconfirmed")
            for k in AMOUNT_FIELDS:
                a = r["amounts"].get(k)
                if a and a.get("display_eligible"):
                    out.append(f"display: {r['id']}.{k}: single-source relationship shows an amount")
    return out


def check_independence(reg):
    out = []
    for path, field, a, _ in iter_amounts(reg):
        if not a.get("display_eligible"):
            continue
        for value, ids in amount_parts(a):
            evs = [reg.ev[i] for i in ids if i in reg.ev]
            if any(e["tier"] in ("1", "market") for e in evs):
                continue
            t2 = [e for e in evs if e["tier"] == "2"]
            if len(t2) >= 2 and not _independent_pair(t2):
                out.append(f"independence: {path}: its tier 2 sources share a parent company or cite each other")
    return out


def check_allowlist(reg):
    out = []
    al = allowlist()
    for ev in reg.evidence:
        info = classify_domain(ev["url"], al)
        if info["tier"] is None:
            out.append(f"allowlist: {ev['id']}: domain {info['domain']} is not an allowed source ({info.get('reason')})")
        elif info["tier"] != ev["tier"]:
            out.append(f"allowlist: {ev['id']}: tier recorded as {ev['tier']} but {info['domain']} is tier {info['tier']}")
        if ev["tier"] == "market":
            bad = [s for s in ev.get("supports", []) if not s.endswith("market_value")]
            if bad:
                out.append(f"allowlist: {ev['id']}: market data supports a field other than market_value: {bad}")
    for path, field, a, _ in iter_amounts(reg):
        if field != "market_value":
            for _, ids in amount_parts(a):
                for i in ids:
                    if reg.ev.get(i, {}).get("tier") == "market":
                        out.append(f"allowlist: {path}: market data evidence {i} used for a field other than market_value")
    return out


def stale_limit_days(r: dict | None, cfg: dict) -> int:
    if r is None or "amounts" not in r:
        return cfg["definitive_days"]
    big = any((r["amounts"].get(k) or {}).get("value") and r["amounts"][k]["value"] >= cfg["large_threshold_usd"]
              for k in ("headline", "committed_total", "contingent_max"))
    if r["status"] in cfg["closed_statuses"]:
        return cfg["closed_days"]
    if big:
        return cfg["large_days"]
    if r["status"] in cfg["unsettled_statuses"]:
        return cfg["unsettled_days"]
    return cfg["definitive_days"]


def is_stale(a: dict, r: dict | None, cfg: dict, today: date | None = None) -> bool:
    lv = a.get("last_verified")
    if not lv:
        return True
    today = today or date.today()
    return (today - date.fromisoformat(lv)).days > stale_limit_days(r, cfg)


def check_dates(reg, published=None, today=None):
    out = []
    cfg = load_json(CONFIG / "staleness.json")
    for path, field, a, owner in iter_amounts(reg):
        if a.get("value") is None or a.get("not_applicable"):
            continue
        if not a.get("as_of"):
            out.append(f"dates: {path}: amount has no as_of date")
        if not a.get("last_verified"):
            out.append(f"dates: {path}: amount has no last_verified date")
    if published:
        for r in published.get("relationships", []):
            src = reg.rel.get(r["id"])
            for k, a in r["amounts"].items():
                if isinstance(a, dict) and a.get("display_eligible") and is_stale(a, src, cfg, today) and not a.get("stale"):
                    out.append(f"dates: published {r['id']}.{k}: past its re-verification limit without a stale badge")
    return out


def check_amount_order(reg):
    out = []
    for r in reg.relationships:
        am = r["amounts"]

        def v(k):
            a = am.get(k) or {}
            return None if a.get("not_applicable") else a.get("value")
        f, c, h = v("funded"), v("committed_total"), v("headline")
        tol = lambda x: 1.0005 * x
        if f is not None and c is not None and f > tol(c):
            out.append(f"order: {r['id']}: funded {f:,.0f} exceeds committed_total {c:,.0f}")
        if c is not None and h is not None and c > tol(h):
            out.append(f"order: {r['id']}: committed_total {c:,.0f} exceeds headline {h:,.0f}")
        if f is not None and h is not None and f > tol(h):
            out.append(f"order: {r['id']}: funded {f:,.0f} exceeds headline {h:,.0f}")
        if r["status"] == "loi_or_framework":
            for k in ("committed_total", "funded", "contingent_max"):
                if (am.get(k) or {}).get("value") and not am[k].get("not_applicable"):
                    out.append(f"order: {r['id']}: a letter of intent carries headline only, but {k} has a value")
    return out


def check_insights(reg):
    out = []
    for r in reg.relationships:
        t = r["insight_template"]
        bad = fmt.template_number_violations(t)
        if bad:
            out.append(f"insight: {r['id']}: template contains a typed number ({', '.join(bad[:4])})")
        if any(ch in t for ch in BANNED_DASHES) or " - " in t or "--" in t:
            out.append(f"insight: {r['id']}: template contains a dash")
        text, unresolved = fmt.render_insight(t, r, reg.ent)
        if unresolved:
            out.append(f"insight: {r['id']}: unresolved placeholder {unresolved}")
        if word_count(text) > 25:
            out.append(f"insight: {r['id']}: rendered insight has {word_count(text)} words (limit 25)")
    return out


_EXEMPT_KEYS = {"quote", "title", "url", "source_link", "cache_path", "id", "locator"}


def _walk_strings(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in _EXEMPT_KEYS and path.startswith("evidence") or k in ("url", "source_link"):
                continue
            yield from _walk_strings(v, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _walk_strings(v, f"{path}[{i}]")
    elif isinstance(node, str):
        yield path, node


def copy_problems(text: str, banned: list[str]) -> list[str]:
    probs = [f"dash U+{ord(ch):04X}" for ch in BANNED_DASHES if ch in text]
    low = text.lower()
    probs += [f"banned word '{w}'" for w in banned if re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", low)]
    return probs


def check_copy(reg, published_dir=None, site_dir=None):
    out = []
    banned = load_json(CONFIG / "banned_words.json")["words"]
    for name, coll in (("relationships", reg.relationships), ("entities", reg.entities), ("projects", reg.projects), ("events", reg.events)):
        for row in coll:
            for path, s in _walk_strings(row):
                for p in copy_problems(s, banned):
                    out.append(f"copy: {row['id']}.{path}: {p}")
    if published_dir and Path(published_dir).exists():
        for f in sorted(Path(published_dir).glob("*.json")):
            data = load_json(f)
            top = "evidence" if f.name == "evidence.json" else ""
            for path, s in _walk_strings(data, top):
                for p in copy_problems(s, banned):
                    out.append(f"copy: published/{f.name}:{path}: {p}")
    if site_dir and (Path(site_dir) / "index.html").exists():
        html = (Path(site_dir) / "index.html").read_text(encoding="utf-8")
        # verbatim quotes and source titles render inside <q> or <cite>; embedded data is checked via published/
        stripped = re.sub(r"(?s)<(q|cite)\b[^>]*>.*?</\1>", " ", html)
        stripped = re.sub(r"(?s)<script\b[^>]*type=\"application/json\"[^>]*>.*?</script>", " ", stripped)
        stripped = re.sub(r"(?s)(href|data-src|title)=\"[^\"]*\"", " ", stripped)
        for ch in BANNED_DASHES:
            if ch in stripped:
                i = stripped.index(ch)
                out.append(f"copy: site/index.html: dash U+{ord(ch):04X} near '{stripped[max(0, i - 40): i + 40]!r}'")
    return out


def check_quotes(reg):
    return [f"quotes: {e['id']}: quote has {word_count(e['quote'])} words (limit under fifteen)"
            for e in reg.evidence if not str(e["locator"]).startswith("xbrl:") and word_count(e["quote"]) >= 15]


def check_reconciliation(reg):
    out = []
    for r in reg.relationships:
        rc = r["reconciliation"]
        if rc["result"] in ("contradicted", "partial") and not rc["differences"]:
            out.append(f"reconciliation: {r['id']}: {rc['result']} without a differences list")
        if rc["result"] == "reconciled" and not (rc.get("nvidia_evidence") and rc.get("counterparty_evidence")):
            out.append(f"reconciliation: {r['id']}: reconciled needs evidence from both sides (nvidia_evidence and counterparty_evidence)")
        if rc["result"] == "one_sided" and rc.get("nvidia_evidence") and rc.get("counterparty_evidence"):
            out.append(f"reconciliation: {r['id']}: marked one_sided but both sides have evidence")
    return out


def check_consequences(reg):
    out = []
    for r in reg.relationships:
        if r.get("aggregate_of") or r["type_primary"] == "CX":
            continue
        c = r["consequences"]
        n1, n2 = len(c["first_order"]), len(c["second_order"])
        if not (1 <= n1 <= 4) or not (1 <= n2 <= 4) or not (2 <= n1 + n2 <= 8):
            out.append(f"consequences: {r['id']}: needs one to four first order and one to four second order consequences (has {n1} and {n2})")
        name = (reg.ent.get(r["to"], {}).get("short_name") or "").lower()
        for item in c["first_order"] + c["second_order"]:
            if name and name not in item["text"].lower() and name not in item["mechanism"].lower():
                out.append(f"consequences: {r['id']}: a consequence does not name the counterparty, so it could describe any company: '{item['text'][:60]}'")
    return out


def check_published(reg, published_dir):
    """Headline leakage, aggregate exclusion, arithmetic and the display rule on the published build."""
    out = []
    pd = Path(published_dir)
    if not (pd / "summary.json").exists():
        return out
    summary = load_json(pd / "summary.json")
    pub_rels = load_json(pd / "relationships.json")
    ind = independent_totals(reg)
    t = summary["totals"]
    for k in ("funded", "committed_unfunded", "contingent_max", "headline", "gross"):
        if abs(t[k] - ind[k]) > 1.0:
            out.append(f"arithmetic: published total {k} = {t[k]:,.0f}, independent recomputation = {ind[k]:,.0f}")
    if t.get("count") != ind["count"]:
        out.append(f"arithmetic: published relationship count {t.get('count')} differs from {ind['count']}")
    if abs(t["gross"] - (t["funded"] + t["committed_unfunded"] + t["contingent_max"])) > 1.0:
        out.append("headline leakage: gross is not the sum of funded, committed not yet paid and contingent")
    # headline leakage test: totals recomputed with every headline set to zero must be unchanged
    reg2 = copy.deepcopy(reg)
    for r in reg2.relationships:
        r["amounts"]["headline"]["value"] = None
    ind2 = independent_totals(reg2)
    for k in ("funded", "committed_unfunded", "contingent_max", "gross"):
        if abs(ind2[k] - t[k]) > 1.0:
            out.append(f"headline leakage: total {k} changes when headline amounts are removed")
    agg_ids = {r["id"] for r in reg.relationships if r.get("aggregate_of")}
    for rid in summary.get("included_ids", []):
        if rid in agg_ids:
            out.append(f"aggregate exclusion: {rid} is an unattributed remainder but is included in totals")
    for r in pub_rels:
        for k, a in r["amounts"].items():
            if isinstance(a, dict) and not a.get("display_eligible") and not a.get("not_applicable") and a.get("value") is not None:
                out.append(f"display: published {r['id']}.{k}: ineligible amount is published as a number")
    for s in summary.get("sentences", []):
        for ref in s.get("figures", []):
            if ref.get("value") is not None and not ref.get("eligible_only", True):
                out.append("display: summary sentence uses a figure that is not built from eligible amounts")
    return out


CHECKS = [check_schema, check_evidence_resolution, check_grounding, check_display_rule, check_independence, check_allowlist,
          check_amount_order, check_insights, check_quotes, check_reconciliation, check_consequences]


def run_all(reg: Register, published_dir=None, site_dir=None, today=None) -> list[str]:
    out = []
    for fn in CHECKS:
        out += fn(reg)
    published = None
    if published_dir and (Path(published_dir) / "relationships.json").exists():
        published = {"relationships": load_json(Path(published_dir) / "relationships.json")}
        out += check_published(reg, published_dir)
    out += check_dates(reg, published, today)
    out += check_copy(reg, published_dir, site_dir)
    return out


def check_links(reg) -> list[str]:
    import requests
    from .cache import GENERIC_UA
    from . import edgar
    out = []
    seen = set()
    for ev in reg.evidence:
        url = ev["url"]
        if url in seen or ev.get("paywalled"):
            continue
        seen.add(url)
        try:
            if "sec.gov" in url:
                edgar._throttle()
                code = requests.head(url, headers={"User-Agent": edgar.user_agent()}, timeout=30, allow_redirects=True).status_code
            else:
                code = requests.get(url, headers={"User-Agent": GENERIC_UA}, timeout=30, stream=True).status_code
        except Exception as e:  # noqa: BLE001
            code = str(e)[:60]
        if code != 200:
            out.append(f"links: {ev['id']}: {url} returned {code}")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", nargs="?", default="all", choices=["all", "draft", "eligibility", "links"])
    ap.add_argument("file", nargs="?")
    ap.add_argument("--register", default=str(REGISTER))
    ap.add_argument("--published", default=str(PUBLISHED))
    ap.add_argument("--site", default=str(ROOT / "site"))
    args = ap.parse_args(argv)
    if args.cmd == "draft":
        from .evidence import EV_DIR
        extra = []
        for f in sorted(EV_DIR.glob("*.jsonl")):
            extra += [r for r in (json.loads(l) for l in open(f, encoding="utf-8")) if str(r.get("id", "")).startswith("ev_")]
        reg = Register(args.register)
        known = set(reg.ev)
        reg.evidence += [e for e in extra if e["id"] not in known]
        d = load_json(args.file)
        ids = {e["id"] for e in d.get("entities", [])}
        reg.entities = [e for e in reg.entities if e["id"] not in ids] + d.get("entities", [])
        reg.relationships = d.get("relationships", [])
        reg.projects = d.get("projects", [])
        reg.events = d.get("events", [])
        used = set()
        for coll in (reg.relationships, reg.entities, reg.projects, reg.events):
            for row in coll:
                used |= set(_ev_ids(row))
        reg.evidence = [e for e in reg.evidence if e["id"] in used]
        reg.index()
        set_eligibility(reg)
        d["relationships"], d["projects"] = reg.relationships, reg.projects
        d["entities"] = [e for e in reg.entities if e["id"] in ids]
        save_json(args.file, d)
        probs = run_all(reg)
        print("Display eligibility written to the draft.")
        for r in reg.relationships:
            shown = {k: fmt.amount_text(a) for k, a in r["amounts"].items()}
            print(f"  {r['id']}: {shown}")
            print(f"    insight: {fmt.render_insight(r['insight_template'], r, reg.ent)[0]}")
    elif args.cmd == "eligibility":
        reg = Register(args.register)
        n = set_eligibility(reg)
        reg.save()
        print(f"display_eligible updated on {n} amounts")
        return 0
    elif args.cmd == "links":
        probs = check_links(Register(args.register))
    else:
        probs = run_all(Register(args.register), args.published, args.site)
    for p in probs:
        print("FAIL", p)
    print(f"\n{len(probs)} problem(s)" if probs else "All checks passed")
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
