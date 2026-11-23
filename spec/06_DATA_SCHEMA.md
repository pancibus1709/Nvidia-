# 06 · Data Schema

All data lives in `data/` as JSON, validated against JSON Schema files in `schema/`. The front end reads only `data/published/`. Research and review work happens in `data/register/`, `data/inbox/` and `data/queue/`. History is append-only in `data/history/`.

Identifiers are stable slugs, never reused: `ent_<name>`, `rel_<counterparty>_<type>_<year>`, `ev_<number>`, `proj_<entity>_<site>`.

**Examples below use a fictional entity (`ent_example`) and placeholders on purpose.** Do not copy example values into real records.

---

## schema/enums.json (the only place enums are defined)

Every other file in this package refers to these lists. Validators, badges and filters read from this file.

```json
{
  "cluster": ["nvidia", "ai_lab", "neocloud", "hyperscaler", "semis_supply", "sovereign_project", "portfolio", "vehicle", "lender", "other"],
  "type": ["EQ", "EQ-SPV", "EQ-C", "BK", "LB", "GU", "RV", "FC", "LP", "PP", "LI", "CX"],
  "status": ["definitive", "loi_or_framework", "reported_unconfirmed", "restructured", "terminated", "completed"],
  "claim_basis": ["filed", "company_announced", "reported_corroborated", "reported_single_source"],
  "label": ["fact", "analysis"],
  "reconciliation": ["reconciled", "partial", "one_sided", "contradicted"],
  "seniority": ["common_equity", "preferred_equity", "warrants", "spv_equity", "lp_interest", "senior_secured_creditor", "unsecured_creditor", "guarantor", "contingent_buyer", "lessee", "prepaying_buyer", "licensee", "none"],
  "grade": ["Strong", "Adequate", "Watch", "Weak", "Distressed", "Insufficient information"],
  "wwr": ["specific", "general", "none"],
  "lens": ["revenue_quality", "lender_reliance", "collateral_loop", "contagion", "signaling"],
  "direction": ["negative", "positive", "mixed"],
  "evidence_kind": ["sec_filing", "company_release", "earnings_call", "regulator", "rating_agency", "lien_registry", "news", "market_data"],
  "sourcing": ["filing", "named", "documents_seen", "anonymous"],
  "change_type": ["added", "amount_changed", "status_changed", "reconciliation_changed", "dates_changed", "evidence_added", "market_value", "link_repair", "reverified", "corrected", "removed_from_display"],
  "project_role": ["covered", "context"],
  "event_kind": ["announcement", "signing", "filing", "closing", "amendment", "drawdown", "restructuring", "termination", "holding_change"]
}
```

Badge labels on screen map one to one: status `definitive` → "Definitive", `loi_or_framework` → "Letter of intent", `reported_unconfirmed` → "Reported, unconfirmed", `restructured` → "Restructured", `terminated` → "Terminated", `completed` → "Completed". Claim basis is shown separately as a small source-strength chip: "Filed", "Company announced", "Reported, two sources", "Reported, one source".

## The amount object (used for every amount)

```json
{
  "value": null,
  "as_of": "YYYY-MM-DD",
  "fiscal_period": "<e.g. Nvidia FY2026 Q3, or null>",
  "original_currency": "USD",
  "original_value": null,
  "fx_rate": null,
  "fx_date": null,
  "last_verified": "YYYY-MM-DD",
  "display_eligible": false,
  "lower_bound": false,
  "evidence": ["ev_0000"]
}
```

`value` is always USD. `display_eligible` is set by `checks.py`, never by hand.

**Not applicable versus unknown.** An amount that cannot exist for the deal type is stored as `0` with `"not_applicable": true`, not null: `contingent_max` for EQ, EQ-SPV, PP and LI unless a source shows a contingent term; `committed_total` for open-market or 13F stakes. Only true unknowns are null, and only they go into `gross_missing`. Grounding checks `original_value` when `original_currency` is not USD, and checks `fx_rate` against its own evidence. `last_verified` lives on each amount, not the record (see `11`).

## entities.json

```json
{
  "id": "ent_example",
  "name": "<legal name>",
  "short_name": "<display name>",
  "cluster": "<enum cluster>",
  "depth": 1,
  "public": true,
  "ticker": "<or null>",
  "cik": "<from EDGAR, or null>",
  "country": "<ISO code>",
  "credit": {
    "grade": "<enum grade>",
    "grade_reason": "<two sentences, analysis>",
    "public_ratings": [{"agency": "<agency>", "rating": "<rating>", "date": "YYYY-MM-DD", "evidence": []}],
    "debt_outstanding": "<amount object>",
    "maturities_24m": "<amount object>",
    "liquidity_months": {"value": null, "inputs": [], "label": "analysis"},
    "top_customer_share": "<amount-like object with value as a fraction>",
    "evidence": []
  }
}
```

Nvidia itself is `ent_nvidia`, cluster `nvidia`, depth 0, CIK `0001045810`.

## relationships.json

```json
{
  "id": "rel_example_bk_2025",
  "from": "ent_nvidia",
  "to": "ent_example",
  "type_primary": "<enum type>",
  "types_secondary": [],
  "title": "<short title>",
  "insight_template": "<sentence with {placeholders}, see rule below>",
  "definition": "<plain description, two to four sentences>",
  "status": "<enum status>",
  "claim_basis": "<enum claim_basis>",
  "amounts": {
    "headline": "<amount object>",
    "committed_total": "<amount object>",
    "funded": "<amount object>",
    "contingent_max": "<amount object plus a 'trigger' string>",
    "annual_obligation": "<amount object, optional>",
    "market_value": "<amount object plus 'price_source'>"
  },
  "dates": {"announced": null, "signed": null, "filed": null, "effective": null, "maturity": null},
  "seniority": "<enum seniority>",
  "reconciliation": {
    "result": "<enum reconciliation>",
    "nvidia_side": "<text with evidence ids>",
    "counterparty_side": "<text with evidence ids, or 'No disclosure found as of YYYY-MM-DD'>",
    "differences": [{"field": "", "nvidia_value": null, "counterparty_value": null, "evidence": []}]
  },
  "derived": {
    "committed_unfunded": null,
    "gross_exposure": null,
    "gross_missing": [],
    "ead_base": null, "ead_max": null,
    "loss_base": null, "loss_max": null,
    "circularity_ratio": {"value": null, "window": null, "inputs": []},
    "round_trip": {"nvidia_paid": null, "counterparty_nvidia_spend": null, "window": null, "inputs": []},
    "share_of_counterparty_capital": {"value": null, "inputs": []},
    "share_of_nvda_equity": {"value": null, "inputs": []},
    "share_of_nvda_fcf": {"value": null, "inputs": []},
    "backstop_coverage": {"value": null, "inputs": []}
  },
  "credit": {"wwr": "<enum wwr>", "wwr_reason": "", "collateral": "", "notes": ""},
  "consequences": {
    "first_order": [{"trigger": "", "mechanism": "", "affected": [], "direction": "<enum>", "text": ""}],
    "second_order": [{"lens": "<enum lens>", "trigger": "", "mechanism": "", "affected": [], "direction": "<enum>", "text": ""}]
  },
  "projects": [],
  "depth2_links": [],
  "aggregate_of": null,
  "significance": {"score": null, "components": {}},
  "version": 1,
  "evidence": []
}
```

All `derived` fields are written by `pipeline/measure.py` only, always labeled analysis. Consequences are always analysis.

`aggregate_of` is set on unattributed-remainder nodes (see `05` section 3); such records are excluded from every total. They use `to: "ent_nvidia_unattributed"` (a synthetic entity, cluster `other`) and the id pattern `rel_unattributed_<aggregate>_<balance sheet date>`.

### Insight rule

The insight is stored as a template. Numbers enter only through placeholders filled by a formatter from `amounts` or `derived` (for example `{funded}`, `{contingent_max}`, `{dates.maturity:year}`). Any digit or number word typed directly into the template fails the check. Maximum 25 words after rendering. No dashes of any kind.

### Significance score (sizing and sorting, analysis)

`score = 40 × gross exposure percentile + 25 × contingent share of gross + 15 × circularity percentile + 10 × counterparty weakness + 10 × lender reliance`, each component 0 to 1, weights in `config/significance.json`. Counterparty weakness is computed from the displayed indicators (liquidity months, maturities, concentration, public rating), never from the internal letter grade. A missing component scores 0.5 (neutral) and is listed, so an opaque private counterparty is not ranked as the safest. Formula shown on the Method view.

## evidence.json

```json
{
  "id": "ev_0000",
  "tier": "<1 | 2 | market>",
  "kind": "<enum evidence_kind>",
  "publisher": "",
  "title": "",
  "url": "",
  "accession": "<filings only>",
  "section": "<Item, Note or page>",
  "published": "YYYY-MM-DD",
  "retrieved": "YYYY-MM-DDThh:mm:ssZ",
  "quote": "<verbatim, under fifteen words>",
  "locator": "<character offset in the cached file, or XBRL fact id>",
  "unit_scale_locator": "<offset of a table header such as '(in millions)', or null>",
  "parent_company": "<from the allowlist, e.g. Dow Jones for WSJ and Barron's>",
  "cites_publisher": [],
  "cache_path": "research/cache/<file>",
  "content_hash": "<sha256 of the cached file>",
  "sourcing": "<enum sourcing>",
  "paywalled": false,
  "supports": ["rel_example_bk_2025.amounts.contingent_max"]
}
```

The grounding check in `09` uses `cache_path`, `content_hash`, `quote` and `locator`. For paywalled articles the cache holds what a human pasted in review, marked as such.

## projects.json

```json
{
  "id": "proj_example_site",
  "entity": "ent_example",
  "name": "", "location": "",
  "power_mw_contracted": "<amount-like>", "power_mw_energized": "<amount-like>",
  "gpu_generation": null, "gpu_count": null,
  "anchor_tenant": null, "contract_years": null,
  "financing": [{"facility": "", "lenders": [], "balance": "<amount object>", "secured_by": "", "covenant_ltv": null, "evidence": []}],
  "expected_completion": null,
  "nvidia_link": [],
  "role": "<enum project_role>",
  "evidence": []
}
```

## events.json (timeline)

`{id, date, relationship, kind, summary, evidence}`, with `kind` from `event_kind` in enums.

## scenarios.json

Generated from `config/scenarios.json` plus the register: parameters with their basis, affected node ids, stressed EAD and loss, not-computable list.

## Change log and history

- `data/changelog.json` is append-only and private: `{timestamp, relationship, change_type, field, old, new, evidence, approved_by, auto_rule}`.
- Each publish writes `data/published/changelog.json` for the What changed view, filtered so any `old` or `new` value that is not display eligible appears as "Not confirmed", and with `approved_by` removed.
- Each publish snapshots `published/` to `data/history/YYYY-MM-DDThhmmssZ/`, so two publishes on one day never collide.
- No record is deleted. Removal from display is a status change with history kept.
