"""Fixtures use a fictional counterparty (ent_example) on purpose. No real figures appear here."""
import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline import checks  # noqa: E402
from pipeline.common import sha256_file  # noqa: E402

FX = "tests/fixtures/cache"


def ev(i, path, quote, url, tier="1", kind="sec_filing", publisher="SEC EDGAR", parent="SEC", scale_loc=None, cites=None, locator=None):
    from pipeline.common import doc_text, norm
    text = doc_text(ROOT / path)
    return {"id": f"ev_{i}", "tier": tier, "kind": kind, "publisher": publisher, "title": "Example source", "url": url, "accession": None,
            "section": "Item 1.01", "published": "2025-03-03", "retrieved": "2025-03-04T00:00:00Z", "quote": quote,
            "locator": str(text.find(norm(quote)) if locator is None else locator), "unit_scale_locator": scale_loc, "parent_company": parent,
            "cites_publisher": cites or [], "cache_path": path, "content_hash": sha256_file(ROOT / path), "sourcing": "filing" if tier == "1" else "anonymous",
            "paywalled": False, "supports": []}


def amt(value=None, evidence=None, na=False, **kw):
    a = {"value": value, "as_of": "2025-03-03" if value is not None or na else None, "fiscal_period": None, "original_currency": "USD",
         "original_value": None, "fx_rate": None, "fx_date": None, "last_verified": "2025-03-04" if value is not None or na else None,
         "display_eligible": False, "lower_bound": False, "evidence": evidence or []}
    if na:
        a["value"], a["not_applicable"] = 0, True
    a.update(kw)
    return a


def rel(rid, to="ent_example", type_primary="BK", status="definitive", claim_basis="filed", evidence=None, **amounts):
    base = {"headline": amt(), "committed_total": amt(), "funded": amt(), "contingent_max": amt()}
    base.update(amounts)
    return {"id": rid, "from": "ent_nvidia", "to": to, "type_primary": type_primary, "types_secondary": [], "title": "Example relationship",
            "insight_template": "Nvidia has agreed to buy whatever capacity {counterparty} cannot sell through {dates.maturity:year}, so its exposure grows when demand weakens.",
            "definition": "A fictional agreement used only to test the checks. It describes nothing real.", "status": status, "claim_basis": claim_basis,
            "amounts": base, "dates": {"announced": "2025-03-03", "signed": None, "filed": "2025-03-03", "effective": None, "maturity": "2032-04-13"},
            "seniority": "contingent_buyer",
            "reconciliation": {"result": "one_sided", "nvidia_side": "No disclosure found as of 2025-03-04", "counterparty_side": "Disclosed in a filing.", "differences": [], "counterparty_evidence": evidence or []},
            "credit": {"wwr": "specific", "wwr_reason": "Exposure grows as the counterparty sells less capacity.", "collateral": "", "notes": ""},
            "consequences": {"first_order": [{"trigger": "Example sells less capacity than contracted", "mechanism": "Nvidia pays Example for the unsold capacity", "affected": ["ent_nvidia"], "direction": "negative", "text": "If Example sells less capacity than contracted, Nvidia pays for the remainder."}],
                             "second_order": [{"lens": "lender_reliance", "trigger": "Nvidia does not renew", "mechanism": "Lenders to Example lose a contracted revenue floor", "affected": ["ent_example"], "direction": "negative", "text": "Lenders to Example sized loans against revenue that includes the Nvidia floor."}]},
            "projects": [], "depth2_links": [], "aggregate_of": None, "significance": {}, "version": 1, "evidence": evidence or []}


@pytest.fixture
def reg(tmp_path):
    sec = "https://www.sec.gov/Archives/edgar/data/1/000000000025000001/example.htm"
    evidence = [
        ev(1, f"{FX}/example_filing.html", "agreed to purchase residual unsold capacity through April 13, 2032", sec),
        ev(2, f"{FX}/example_filing.html", "for an aggregate purchase price of $250 million", sec),
        ev(3, f"{FX}/example_news_a.txt", "agreed to invest as much as $2 billion in Example Lab", "https://www.wsj.com/articles/example", tier="2", kind="news", publisher="The Wall Street Journal", parent="Dow Jones"),
        ev(4, f"{FX}/example_news_b.txt", "will put up to $2 billion into Example Lab", "https://www.reuters.com/technology/example", tier="2", kind="news", publisher="Reuters", parent="Thomson Reuters"),
        ev(5, f"{FX}/example_filing.html", "The term runs from 2025–2032 under the master agreement", sec),
    ]
    entities = [
        {"id": "ent_nvidia", "name": "NVIDIA Corporation", "short_name": "Nvidia", "cluster": "nvidia", "depth": 0, "public": True, "ticker": "NVDA", "cik": "0001045810", "country": "US"},
        {"id": "ent_example", "name": "Example Corp", "short_name": "Example", "cluster": "neocloud", "depth": 1, "public": True, "ticker": None, "cik": None, "country": "US", "credit": {}},
        {"id": "ent_examplelab", "name": "Example Lab Inc", "short_name": "Example Lab", "cluster": "ai_lab", "depth": 1, "public": False, "ticker": None, "cik": None, "country": "US"},
    ]
    rels = [
        rel("rel_example_bk_2025", evidence=["ev_1"], contingent_max=amt(6.3e9, ["ev_1"], trigger="Capacity not sold to other customers"),
            committed_total=amt(na=True), funded=amt(na=True), headline=amt(6.3e9, ["ev_1"])),
        rel("rel_example_eq_2025", type_primary="EQ", status="completed", evidence=["ev_2"], funded=amt(250e6, ["ev_2"]),
            committed_total=amt(250e6, ["ev_2"]), contingent_max=amt(na=True), headline=amt(250e6, ["ev_2"])),
    ]
    rels[1]["credit"]["wwr"] = "general"
    rels[1]["seniority"] = "common_equity"
    d = tmp_path / "register"
    d.mkdir()
    for name, rows in (("entities", entities), ("relationships", rels), ("evidence", evidence), ("projects", []), ("events", [])):
        (d / f"{name}.json").write_text(json.dumps(rows))
    r = checks.Register(d)
    checks.set_eligibility(r)
    return r


@pytest.fixture
def helpers():
    return type("H", (), {"ev": staticmethod(ev), "amt": staticmethod(amt), "rel": staticmethod(rel), "FX": FX})
