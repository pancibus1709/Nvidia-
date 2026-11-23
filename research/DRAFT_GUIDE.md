# How to write register drafts (cluster researchers)

Write one file per cluster: `research/drafts/<cluster>.json` with this shape:

```json
{"entities": [...], "relationships": [...], "projects": [...], "events": [...]}
```

Validate until clean, every time you change it:

```
python3 -m pipeline.checks draft research/drafts/<cluster>.json
```

The command also writes `display_eligible` on each amount for you (never set it by hand) and prints how each
amount will display and how each insight renders. "Not confirmed" means the amount is not supported by a
tier 1 source or two independent tier 2 sources that contain the number. Fix by finding a better source,
or accept it: do not weaken the rule.

Schemas: `schema/relationship.schema.json`, `entity.schema.json`, `project.schema.json`, `event.schema.json`.
Enumerations: `schema/enums.json`. A complete fictional example of every record is in `tests/conftest.py`
(functions `amt`, `rel`, and the entity list). Do not copy its values.

## Entities

`{"id": "ent_<slug>", "name": "<legal name>", "short_name": "<display>", "cluster": "ai_lab|neocloud|hyperscaler|semis_supply|sovereign_project|portfolio|vehicle|lender|other", "depth": 1 or 2, "public": true|false, "ticker": .., "cik": "<10 digits or null>", "country": "US", "description": "<one sentence>", "domains": ["<company's own web domains>"], "credit": {...}, "compute_commitments": [...]}`

- Depth 1 = direct relationship with Nvidia. Depth 2 = a party whose position relies on one (lender, offtaker, co-investor).
- Do not create `ent_nvidia`; it exists.
- `credit` (depth 1 entities, where sourced; every figure is an amount object with evidence):
  `public_ratings` [{agency, rating, date, evidence}], `debt_outstanding`, `maturities_24m` (debt due within 24 months),
  `cash_and_undrawn` (cash plus undrawn committed facilities), `committed_spend_12m` (committed capex and purchase
  obligations due in the next 12 months), `top_customer_share` {value as a fraction, as_of, evidence},
  `top3_customer_share`, `collateral_note` (GPU generation, depreciation life used in the accounts),
  `market_signals` [], `grade` and `grade_reason` (internal, by the rubric in spec/05 section 5: weakest sourced column;
  "Insufficient information" if fewer than two columns are sourced), `notes`.
- `compute_commitments` (AI labs and other buyers): what the entity has committed to spend on compute with third parties:
  [{"counterparty": "ent_x", "description": "...", "amount": <amount object>}].

## Amount object

```json
{"value": 6300000000, "as_of": "2025-09-15", "fiscal_period": null, "original_currency": "USD", "original_value": null,
 "fx_rate": null, "fx_date": null, "last_verified": "2026-11-23", "display_eligible": false, "lower_bound": false,
 "evidence": ["ev_30007"]}
```

- `value` is always USD. Every evidence id listed must contain that number in or near its quote (the check enforces it),
  so list only evidence that states this exact figure. Cite other supporting documents in the relationship's `evidence` list.
- Unknown = `"value": null, "as_of": null, "last_verified": null, "evidence": []`.
- Cannot exist for this deal type = `"value": 0, "not_applicable": true, "as_of": "<date>", "last_verified": "2026-11-23"`.
  Use it for `contingent_max` on plain equity (EQ, EQ-SPV, PP, LI) unless a source shows a contingent term; for
  `committed_total` on stakes bought in the open market or known only from 13F; and for `committed_total`, `funded`
  and `contingent_max` on anything whose status is `loi_or_framework` (a letter of intent is headline only).
- A figure that is the sum of disclosed pieces: add `"components": [{"value": .., "evidence": ["ev_.."], "note": ".."}]`.
- `contingent_max` carries `"trigger": "<what makes Nvidia pay>"`.
- `market_value` (public stakes) needs `price_source` and `price_timestamp`; a 13F reported value is a tier 1 figure as of
  the 13F report date: use it with `"price_source": "Nvidia Form 13F-HR"`.
- `carrying_value` (optional): what Nvidia carries the stake at, if disclosed.
- Integrity: funded <= committed_total <= headline.

## Relationship

Required: `id` (`rel_<counterparty>_<type lower>_<year>`), `from` "ent_nvidia", `to`, `type_primary`, `types_secondary`,
`title`, `insight_template`, `definition`, `status`, `claim_basis`, `amounts` {headline, committed_total, funded,
contingent_max, optional annual_obligation, market_value, carrying_value}, `dates` {announced, signed, filed, effective,
maturity}, `seniority`, `reconciliation`, `credit`, `consequences`, `projects` [], `depth2_links` [], `aggregate_of` null,
`significance` {}, `version` 1, `evidence` [all evidence ids used], optional `measure_inputs`, `stress_inputs`, `notes`,
`holding` {shares, as_of, ticker, evidence}.

- One relationship per distinct transaction (an equity stake and a capacity backstop with the same company are two records).
- `status`: definitive | loi_or_framework | reported_unconfirmed | restructured | terminated | completed.
  `claim_basis`: filed | company_announced | reported_corroborated | reported_single_source. A single tier 2 report means
  status `reported_unconfirmed`, basis `reported_single_source`, and no displayed amounts.
- `insight_template`: one sentence, at most 25 words once rendered, stating the risk plainly. No digits and no number
  words typed in (not even "one" or "half"): numbers and names enter only through placeholders `{counterparty}`,
  `{funded}`, `{committed_total}`, `{headline}`, `{contingent_max}`, `{market_value}`, `{carrying_value}`,
  `{committed_unfunded}`, `{gross_exposure}`, `{dates.maturity:year}`, `{dates.announced:year}`, `{dates.announced:month_year}`.
  No dashes. Example form: "Nvidia has agreed to buy whatever capacity {counterparty} cannot sell through {dates.maturity:year}, so its exposure grows exactly when demand weakens."
- `definition`: two to four plain sentences saying what the transaction is.
- `reconciliation`: `result` reconciled | partial | one_sided | contradicted; `nvidia_side` and `counterparty_side` text;
  `nvidia_evidence` [], `counterparty_evidence` []; `differences` [{field, nvidia_value, counterparty_value, evidence}].
  "reconciled" needs evidence from both sides. Silence is a result: write "No disclosure found as of 2026-11-23" and use one_sided.
- `credit`: `wwr` specific | general | none with `wwr_reason`; `collateral`; `tenor`; `notes`.
  Specific = Nvidia's exposure grows as the counterparty weakens (backstops, guarantees). General = both move with AI demand.
- `consequences`: `first_order` 1 to 4 items {trigger, mechanism, affected [entity ids], direction, text};
  `second_order` 1 to 4 items, same plus `lens` (revenue_quality | lender_reliance | collateral_loop | contagion | signaling).
  Each `text` is one sentence and must name the counterparty. A consequence that would read the same for any company fails.
- `measure_inputs` (optional, each an amount object, only when sourced): `counterparty_nvidia_spend` (what the counterparty
  has disclosed it spent or committed on Nvidia hardware; indirect purchases count only if a filing names Nvidia hardware),
  `counterparty_equity_raised` (total equity raised), `nvidia_paid` (rent or backstop payments Nvidia has made),
  `covered_project_debt` (debt on the projects a backstop covers), `window` (text).
- `stress_inputs` (backstops only, when sourced): `contracted_share`, `merchant_share`, `contracted_floor`,
  `capacity_value_per_quarter`, each `{"value": .., "evidence": [..]}`.
- `depth2_links`: [{"entity": "ent_x", "role": "lender|offtaker|co_investor|bondholder|landlord|utility", "description": "...", "amount": <amount object or null>, "evidence": [...]}].
- Text rules for everything you write: plain English, no em dashes or en dashes, no hype words.

## Projects (neoclouds and vehicles)

`{"id": "proj_<entity>_<site>", "entity": "ent_x", "name", "location", "power_mw_contracted": {"value", "as_of", "evidence"}, "power_mw_energized": {...}, "gpu_generation", "gpu_count", "anchor_tenant", "contract_years", "financing": [{"facility", "lenders": [], "balance": <amount>, "collateral_value": <amount or null>, "secured_by", "covenant_ltv", "evidence": []}], "expected_completion", "nvidia_link": ["rel_.."], "role": "covered|context", "notes", "evidence": []}`

## Events (timeline)

`{"id": "evt_<slug>", "date": "YYYY-MM-DD", "relationship": "rel_..", "kind": "announcement|signing|filing|closing|amendment|drawdown|restructuring|termination|holding_change", "summary": "<one sentence>", "evidence": ["ev_.."]}`

## Additions after the Gate R critic review (23 November 2026)

- `amounts.contingent_max.in_force` (boolean, default true) and `effective_note` (text): set `in_force` false when a signed
  guaranty or backstop cannot yet be called (for example it takes effect only when a building is ready), and say when it starts.
- `holding.shares_acquired`: the number of shares the funded amount bought, when a source states it. With `holding.shares`
  (the current count) the pipeline works out how much of the cost relates to shares still held.
- Evidence ids belong in `evidence` lists. If a note or reconciliation text mentions an id, that id must exist in
  research/evidence/*.jsonl; the checks now fail on any id that does not resolve.
- No "ev_" ids and no bracketed citations inside insight, definition or consequence text.
- `amounts.<field>.qualifier`: "nearly", "about", "more than" or "up to", when the source states the figure that way. It is shown before the number.
- `credit.tenor_bucket`: "Under 2 years", "2 to 5 years", "5 to 10 years", "Over 10 years" or "Equity or no stated maturity", when a source states the term.

## Additions after critic round 3 (explicit fields; nothing is classified by searching text)

- `compute_commitments[].kind`: "contract" or "lease". `compute_commitments[].soft_amount`: the USD part of the amount that the
  source states as "up to", cancellable or terminable (0 if none).
- `amounts.funded.components[].paid_on`: the date that piece of cash was paid ("YYYY-MM-DD"), when a source states it; null if not.
  A single-payment funded amount with no components uses `amounts.funded.as_of` as its payment date only if `paid_on_is_as_of` is true... do not rely on that: give it one component with `paid_on`.
- `amounts.funded.floor`, `floor_as_of`, `floor_note`: a sourced lower bound when the value itself is not disclosed. Never display eligible, never in a total; `floor_note` says what it rests on and is labeled analysis.
- `holding.instrument`: "common", "preferred", "warrant", "convertible note", for positions in listed companies.
