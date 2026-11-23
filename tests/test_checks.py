import copy

from pipeline import checks, fmt, measure, scenarios
from pipeline.common import value_in_text


def fails(reg, prefix):
    return [p for p in checks.run_all(reg) if p.startswith(prefix)]


def test_clean_fixture_passes(reg):
    assert checks.run_all(reg) == []


def test_units_normalised():
    assert value_in_text(6.3e9, "initial order value of $6.3 billion")
    assert value_in_text(3.387e9, "Non-marketable equity securities 3,387", 1e6)
    assert not value_in_text(3.387e9, "Non-marketable equity securities 3,387")
    assert not value_in_text(6.3e9, "about $6.4 billion")


def test_5a_quote_absent_from_cache_fails_grounding(reg):
    reg.ev["ev_1"]["quote"] = "agreed to purchase all capacity forever"
    assert any("quote not found" in p for p in fails(reg, "grounding"))


def test_hash_mismatch_fails_grounding(reg):
    reg.ev["ev_2"]["content_hash"] = "0" * 64
    assert any("hash differs" in p for p in fails(reg, "grounding"))


def test_amount_not_near_quote_fails_grounding(reg):
    reg.rel["rel_example_eq_2025"]["amounts"]["funded"]["value"] = 900e6
    assert any("does not appear" in p for p in fails(reg, "grounding"))


def test_seed_style_anchor_number_without_quote_is_never_eligible(reg):
    a = reg.rel["rel_example_eq_2025"]["amounts"]["funded"]
    a["value"] = 900e6
    assert checks.eligible(reg, "funded", a) is False


def test_5b_single_tier2_is_not_confirmed_and_absent_from_totals(reg, helpers):
    r = helpers.rel("rel_examplelab_eq_2025", to="ent_examplelab", type_primary="EQ", status="reported_unconfirmed", claim_basis="reported_single_source",
                    evidence=["ev_3"], funded=helpers.amt(2e9, ["ev_3"]), contingent_max=helpers.amt(na=True), committed_total=helpers.amt(2e9, ["ev_3"]))
    r["consequences"]["first_order"][0]["text"] = "If Example Lab cannot raise again, Nvidia writes down the stake."
    r["consequences"]["second_order"][0]["text"] = "Example Lab buys compute from others, who lose a customer."
    before = checks.independent_totals(reg)
    reg.relationships.append(r); reg.index()
    checks.set_eligibility(reg)
    assert r["amounts"]["funded"]["display_eligible"] is False
    assert fmt.amount_text(r["amounts"]["funded"]) == "Not confirmed"
    after = checks.independent_totals(reg)
    assert after["funded"] == before["funded"] and after["gross"] == before["gross"]
    measure.run(reg)
    assert r["derived"]["gross_exposure"] is None and "funded" in r["derived"]["gross_missing"]
    s = scenarios.s2(reg, {"lab": "ent_examplelab"})
    assert s["loss"] == 0 and s["not_computable"]
    assert "unconfirmed amount" in fmt.render_insight("Nvidia put {funded} into {counterparty}.", r, reg.ent)[0]


def test_two_independent_tier2_are_eligible(reg, helpers):
    a = helpers.amt(2e9, ["ev_3", "ev_4"])
    assert checks.eligible(reg, "headline", a) is True


def test_independence_same_parent_or_citation(reg, helpers):
    reg.ev["ev_4"]["parent_company"] = "Dow Jones"
    a = helpers.amt(2e9, ["ev_3", "ev_4"])
    assert checks.eligible(reg, "headline", a) is False
    reg.ev["ev_4"]["parent_company"] = "Thomson Reuters"
    reg.ev["ev_4"]["cites_publisher"] = ["The Wall Street Journal"]
    assert checks.eligible(reg, "headline", a) is False


def test_5c_filing_quote_with_en_dash_passes_grounding_and_copy_scan(reg):
    reg.rel["rel_example_bk_2025"]["evidence"].append("ev_5")
    assert "–" in reg.ev["ev_5"]["quote"]
    assert checks.run_all(reg) == []


def test_12_dash_in_text_we_write_fails_copy_scan(reg):
    reg.rel["rel_example_bk_2025"]["definition"] += " It runs 2025–2032."
    assert fails(reg, "copy")
    reg.rel["rel_example_bk_2025"]["definition"] = "A fictional agreement — used only to test the checks, nothing real."
    assert fails(reg, "copy")


def test_banned_word_fails_copy_scan(reg):
    reg.rel["rel_example_bk_2025"]["title"] = "A massive backstop"
    assert any("massive" in p for p in fails(reg, "copy"))


def test_10_excluded_domain_fails(reg):
    reg.ev["ev_2"]["url"] = "https://seekingalpha.com/article/example"
    assert any("not an allowed source" in p for p in fails(reg, "allowlist"))


def test_unlisted_domain_fails(reg):
    reg.ev["ev_2"]["url"] = "https://some-blog.example.org/post"
    assert fails(reg, "allowlist")


def test_market_data_supports_only_market_value(reg, helpers):
    reg.ev["ev_2"]["tier"] = "market"
    reg.ev["ev_2"]["url"] = "https://finance.yahoo.com/quote/EX"
    assert any("market data" in p for p in fails(reg, "allowlist"))


def test_5_headline_never_in_totals(reg, helpers):
    r = helpers.rel("rel_examplelab_eqc_2025", to="ent_examplelab", type_primary="EQ-C", status="loi_or_framework", claim_basis="reported_corroborated",
                    evidence=["ev_3", "ev_4"], headline=helpers.amt(2e9, ["ev_3", "ev_4"]), committed_total=helpers.amt(na=True),
                    funded=helpers.amt(na=True), contingent_max=helpers.amt(na=True))
    before = checks.independent_totals(reg)
    reg.relationships.append(r); reg.index(); checks.set_eligibility(reg)
    after = checks.independent_totals(reg)
    assert r["amounts"]["headline"]["display_eligible"] is True
    assert after["headline"] == before["headline"] + 2e9
    for k in ("funded", "committed_unfunded", "contingent_max", "gross"):
        assert after[k] == before[k]
    measure.run(reg)
    assert r["derived"]["gross_exposure"] == 0


def test_loi_with_committed_amount_fails(reg):
    r = reg.rel["rel_example_bk_2025"]
    r["status"] = "loi_or_framework"
    assert any("letter of intent" in p for p in fails(reg, "order"))


def test_5_unattributed_remainder_never_in_totals(reg, helpers):
    reg.entities.append({"id": "ent_nvidia_unattributed", "name": "Unattributed", "short_name": "Unattributed", "cluster": "other", "depth": 1, "public": False, "ticker": None, "cik": None, "country": None})
    r = helpers.rel("rel_unattributed_nonmarketable_2025_01_26", to="ent_nvidia_unattributed", type_primary="EQ", evidence=["ev_2"], funded=helpers.amt(250e6, ["ev_2"]))
    r["aggregate_of"] = "non_marketable_equity"
    before = checks.independent_totals(reg)
    reg.relationships.append(r); reg.index(); checks.set_eligibility(reg)
    assert checks.independent_totals(reg) == before


def test_amount_order(reg):
    reg.rel["rel_example_eq_2025"]["amounts"]["committed_total"]["value"] = 100e6
    assert fails(reg, "order")


def test_insight_rules(reg):
    r = reg.rel["rel_example_bk_2025"]
    r["insight_template"] = "Nvidia backs {counterparty} with $6.3 billion."
    assert any("typed number" in p for p in fails(reg, "insight"))
    r["insight_template"] = "Nvidia backs {counterparty} with two deals."
    assert any("typed number" in p for p in fails(reg, "insight"))
    r["insight_template"] = "Nvidia backs {counterparty} with {nonsense}."
    assert any("unresolved" in p for p in fails(reg, "insight"))
    r["insight_template"] = "Nvidia backs {counterparty} " + "and then some more words " * 6
    assert any("words" in p for p in fails(reg, "insight"))


def test_quote_length(reg):
    reg.ev["ev_1"]["quote"] = "the Chip Vendor agreed to purchase residual unsold capacity through April 13, 2032, with an initial order"
    assert fails(reg, "quotes")


def test_reconciliation_rules(reg):
    reg.rel["rel_example_bk_2025"]["reconciliation"]["result"] = "partial"
    assert fails(reg, "reconciliation")
    reg.rel["rel_example_bk_2025"]["reconciliation"]["result"] = "reconciled"
    assert any("both sides" in p for p in fails(reg, "reconciliation"))


def test_generic_consequence_fails(reg):
    reg.rel["rel_example_bk_2025"]["consequences"]["first_order"][0].update(text="If demand falls, the company loses money.", mechanism="Demand falls and revenue declines")
    assert fails(reg, "consequences")


def test_unresolved_evidence_and_amount_without_evidence(reg):
    reg.rel["rel_example_eq_2025"]["amounts"]["funded"]["evidence"] = []
    assert any("no evidence" in p for p in fails(reg, "evidence"))
    reg.rel["rel_example_eq_2025"]["evidence"] = ["ev_999"]
    assert any("does not resolve" in p for p in fails(reg, "evidence"))


def test_schema_enum(reg):
    reg.rel["rel_example_eq_2025"]["status"] = "rumoured"
    assert fails(reg, "schema")


def test_measures(reg):
    measure.run(reg)
    bk, eq = reg.rel["rel_example_bk_2025"]["derived"], reg.rel["rel_example_eq_2025"]["derived"]
    assert bk["gross_exposure"] == 6.3e9 and bk["gross_missing"] == []
    assert bk["ead_max"] == 6.3e9 and bk["ead_base"] is None
    assert eq["committed_unfunded"] == 0 and eq["gross_exposure"] == 250e6
    assert reg.rel["rel_example_bk_2025"]["significance"]["score"] > reg.rel["rel_example_eq_2025"]["significance"]["score"]
    assert "counterparty_weakness" in reg.rel["rel_example_bk_2025"]["significance"]["missing"]


def test_7_s1_negative_shock_draws_backstop_and_matches_independent_calc(reg):
    r = reg.rel["rel_example_bk_2025"]
    r["stress_inputs"] = {"contracted_share": {"value": 0.5}, "merchant_share": {"value": 0.5}, "contracted_floor": {"value": 0.9}, "capacity_value_per_quarter": {"value": 400e6}}
    s = scenarios.s1(reg, {"d": -0.3, "p": -0.2, "e": -0.5, "quarters": 4, "h1": 0.5})
    u = 0.5 + 0.5 * (1 - 0.3) * (1 + (-0.5) * (-0.2))
    expect = (0.9 - u) * 400e6 * 4
    assert s["backstop_draws"][0]["draw"] > 0
    assert abs(s["backstop_draws"][0]["draw"] - expect) < 1
    eq_loss = 0.5 * 250e6
    assert abs(s["loss"] - (expect + eq_loss)) < 1
    assert "ent_example" in s["affected"]
    flat = scenarios.s1(reg, {"d": 0.0, "p": 0.0, "e": -0.5, "quarters": 4, "h1": 0.0})
    assert flat["backstop_draws"][0]["draw"] == 0
    assert s["loss"] != reg.rel["rel_example_bk_2025"].get("derived", {}).get("loss_max")


def test_s1_without_sourced_inputs_is_not_computable(reg):
    s = scenarios.s1(reg)
    assert s["backstop_draws"] == [] and s["not_computable"]


def test_staleness_rule():
    from datetime import date
    cfg = {"large_threshold_usd": 1e9, "large_days": 30, "unsettled_statuses": ["loi_or_framework"], "unsettled_days": 30, "definitive_days": 90, "closed_statuses": ["completed"], "closed_days": 365}
    a = {"last_verified": "2025-01-01"}
    big = {"status": "definitive", "amounts": {"headline": {"value": 5e9}}}
    small = {"status": "definitive", "amounts": {"headline": {"value": 5e6}}}
    done = {"status": "completed", "amounts": {"headline": {"value": 5e9}}}
    assert checks.is_stale(a, big, cfg, date(2025, 2, 15)) and not checks.is_stale(a, small, cfg, date(2025, 2, 15))
    assert not checks.is_stale(a, done, cfg, date(2025, 6, 1)) and checks.is_stale(a, done, cfg, date(2026, 2, 1))


def test_committed_with_undisclosed_paid_portion_counts_once_and_is_never_called_unpaid(reg, helpers):
    r = helpers.rel("rel_example_eq_2026", type_primary="EQ", evidence=["ev_2"], committed_total=helpers.amt(250e6, ["ev_2"]),
                    headline=helpers.amt(250e6, ["ev_2"]), contingent_max=helpers.amt(na=True))
    before = checks.independent_totals(reg)
    reg.relationships.append(r); reg.index(); measure.run(reg)
    after = checks.independent_totals(reg)
    d = r["derived"]
    assert d["committed_unfunded"] is None and d["committed_split_unknown"] == 250e6 and d["funded_split_unknown"] is True
    assert d["gross_exposure"] == 250e6 and d["gross_lower_bound"] is False
    assert after["gross"] == before["gross"] + 250e6
    assert after["committed_unfunded"] == before["committed_unfunded"] and after["funded"] == before["funded"]
    assert after["committed_split_unknown"] == before["committed_split_unknown"] + 250e6


def test_cost_counts_only_for_shares_still_held(reg):
    r = reg.rel["rel_example_eq_2025"]
    r["holding"] = {"shares": 75, "shares_acquired": 100}
    measure.run(reg)
    assert r["derived"]["funded_remaining"] == 0.75 * 250e6 and r["derived"]["funded_cash"] == 250e6
    assert r["derived"]["gross_exposure"] == 0.75 * 250e6
    r["status"] = "terminated"
    measure.run(reg)
    assert r["derived"]["gross_exposure"] == 0 and checks.independent_totals(reg)["funded"] == 0


def test_guaranty_not_yet_in_force_is_reported_apart(reg):
    reg.rel["rel_example_bk_2025"]["amounts"]["contingent_max"]["in_force"] = False
    t = checks.independent_totals(reg)
    assert t["contingent_not_in_force"] == 6.3e9 and t["contingent_in_force"] == 0 and t["contingent_max"] == 6.3e9


def test_headline_is_grouped_by_what_it_is(reg):
    t = checks.independent_totals(reg)
    assert t["headline_groups"]["guaranty_backstop"] == 6.3e9 and t["headline_groups"]["other"] == 250e6
    assert abs(sum(t["headline_groups"].values()) - t["headline"]) < 1


def test_evidence_id_cited_in_text_must_exist(reg, tmp_path):
    reg.rel["rel_example_bk_2025"]["notes"] = "See ev_999 for the figure."
    reg.save()
    assert any("ev_999" in p for p in checks.check_text_citations(reg))
    reg.rel["rel_example_bk_2025"]["consequences"]["first_order"][0]["text"] = "If Example sells less (ev_1), Nvidia pays."
    assert checks.check_no_ids_in_copy(reg)


def test_non_usd_amount_without_fx_shows_in_own_currency_and_stays_out_of_totals(reg, helpers):
    a = helpers.amt(None, ["ev_2"], original_currency="GBP", original_value=250e6, as_of="2025-03-03", last_verified="2025-03-04")
    assert checks.eligible(reg, "headline", a) is True
    a["display_eligible"] = True
    assert fmt.amount_text(a) == "£250 million"
    assert checks.elig_value(a) is None


def test_lab_commitments_are_classified_by_field_never_by_wording(reg, helpers):
    lab = reg.ent["ent_examplelab"]
    lab["compute_commitments"] = [
        {"counterparty": "ent_example", "description": "Cloud services contract; early release terms apply", "kind": "contract", "soft_amount": 0, "amount": helpers.amt(250e6, ["ev_2"])},
        {"counterparty": "ent_example", "description": "Equipment arrangement", "kind": "lease", "soft_amount": 0, "amount": helpers.amt(250e6, ["ev_2"])},
    ]
    r = helpers.rel("rel_examplelab_eq_2025", to="ent_examplelab", type_primary="EQ", status="completed", evidence=["ev_2"], funded=helpers.amt(250e6, ["ev_2"]),
                    committed_total=helpers.amt(250e6, ["ev_2"]), contingent_max=helpers.amt(na=True))
    reg.relationships.append(r); reg.index(); checks.set_eligibility(reg)
    s = scenarios.s2(reg, {"lab": "ent_examplelab"})
    kinds = [x["kind"] for x in s["at_risk_backlog"]]
    assert kinds == ["contract", "lease"]          # "release" in a description does not make a lease
    assert all(x["soft_amount"] == 0 for x in s["at_risk_backlog"])
    del lab["compute_commitments"][0]["kind"]
    assert scenarios.s2(reg, {"lab": "ent_examplelab"})["at_risk_backlog"][0]["kind"] == "unclassified"


def test_money_style_check(reg):
    c = reg.rel["rel_example_bk_2025"]["consequences"]["first_order"][0]
    c["text"] = "If Example sells less, Nvidia pays up to $6.3B."
    assert checks.check_money_style(reg)
    c["text"] = "If Example sells less, Nvidia pays up to $6.3 billion."
    assert not checks.check_money_style(reg)
    c["text"] = "If Example sells less, Nvidia pays USD 30 million."
    assert checks.check_money_style(reg)
