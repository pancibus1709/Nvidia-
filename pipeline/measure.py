"""Derived measures (spec/05 sections 3 and 4) and the significance score (spec/06).

Everything written here is labeled analysis. Only display-eligible amounts are used.
A measure whose inputs are not sourced is left blank.

  python3 -m pipeline.measure      recompute `derived` and `significance` on every relationship in the register
"""
from __future__ import annotations

from datetime import date

from .checks import Register, elig_value, set_eligibility
from .common import CONFIG, load_json


def _ref(path, a):
    return {"field": path, "value": a.get("value"), "as_of": a.get("as_of"), "evidence": a.get("evidence", [])}


def committed_unfunded(r: dict):
    am = r["amounts"]
    funded, committed = elig_value(am.get("funded")), elig_value(am.get("committed_total"))
    na = am["committed_total"].get("not_applicable")
    if committed is not None and funded is not None and not na:
        return max(0.0, committed - funded)
    if funded is not None and (r["status"] == "completed" or na):
        return 0.0
    if committed is not None and funded is None and not na:
        # Paid portion not disclosed. Funded plus unfunded equals the committed total whatever the split,
        # so the whole committed total counts once, here, and the record is flagged.
        return committed
    return None


def funded_split_unknown(r: dict) -> bool:
    am = r["amounts"]
    return (elig_value(am.get("committed_total")) is not None and not am["committed_total"].get("not_applicable")
            and elig_value(am.get("funded")) is None)


def gross(r: dict):
    parts = {"funded": elig_value(r["amounts"].get("funded")), "committed_unfunded": committed_unfunded(r),
             "contingent_max": elig_value(r["amounts"].get("contingent_max"))}
    split_unknown = funded_split_unknown(r)
    missing = [k for k, v in parts.items() if v is None and not (k == "funded" and split_unknown)]
    return sum(v for v in parts.values() if v is not None), missing, parts


def remaining_years(r: dict, today: date) -> float | None:
    m = r["dates"].get("maturity")
    if not m:
        return None
    y, mo = int(m[:4]), int(m[5:7]) if len(m) >= 7 else 12
    yrs = (y - today.year) + (mo - today.month) / 12
    return yrs if yrs > 0 else None


def percentile(value, population):
    pop = sorted(p for p in population if p is not None)
    if value is None or not pop:
        return None
    if len(pop) == 1:
        return 1.0
    below = sum(1 for p in pop if p < value)
    equal = sum(1 for p in pop if p == value)
    return (below + 0.5 * (equal - 1)) / (len(pop) - 1) if len(pop) > 1 else 1.0


def weakness(ent: dict, rubric: dict):
    """0 (strong) to 1 (weak) from the displayed indicators only. None when fewer than two are sourced."""
    c = ent.get("credit") or {}
    scores = []
    lm = (c.get("liquidity_months") or {}).get("value")
    if lm is not None:
        scores.append(0.0 if lm >= 24 else 0.33 if lm >= 12 else 0.66 if lm >= 6 else 1.0)
    mat, cash = elig_value(c.get("maturities_24m")), elig_value(c.get("cash_and_undrawn"))
    if mat is not None and cash:
        x = mat / cash
        scores.append(0.0 if x < 0.5 else 0.33 if x < 1.0 else 0.66 if x < 1.5 else 1.0)
    tc = (c.get("top_customer_share") or {}).get("value")
    if tc is not None:
        scores.append(0.0 if tc < 0.25 else 0.33 if tc < 0.5 else 0.66 if tc < 0.7 else 1.0)
    for pr in c.get("public_ratings") or []:
        rt = pr["rating"].upper().replace("+", "").replace("-", "").strip()
        rt = {"AAA": "A", "AA": "A", "AA1": "A", "AA2": "A", "AA3": "A", "A1": "A", "A2": "A", "A3": "A", "BAA1": "BBB", "BAA2": "BBB", "BAA3": "BBB",
              "BA1": "BB", "BA2": "BB", "BA3": "BB", "B1": "B", "B2": "B", "B3": "B", "CAA1": "CCC", "CAA2": "CCC", "CAA3": "CCC", "CA": "CC"}.get(rt, rt)
        scores.append({"A": 0.0, "BBB": 0.0, "BB": 0.33, "B": 0.66, "CCC": 1.0}.get(rt, 1.0 if rt in ("CC", "C", "D", "SD") else 0.5))
        break
    if len(scores) < rubric.get("min_columns_sourced", 2):
        return None
    return max(scores)


def liquidity_months(ent: dict):
    c = ent.get("credit") or {}
    cash, spend = elig_value(c.get("cash_and_undrawn")), elig_value(c.get("committed_spend_12m"))
    if cash is None or not spend:
        return {"value": None, "inputs": [], "label": "analysis"}
    return {"value": round(cash / (spend / 12), 1), "label": "analysis",
            "inputs": [_ref("credit.cash_and_undrawn", c["cash_and_undrawn"]), _ref("credit.committed_spend_12m", c["committed_spend_12m"])]}


def run(reg: Register, today: date | None = None) -> Register:
    today = today or date.today()
    set_eligibility(reg)
    draw = load_json(CONFIG / "draw_rates.json")
    sig_cfg = load_json(CONFIG / "significance.json")
    rubric = load_json(CONFIG / "grade_rubric.json")
    fin = reg.financials or {}
    equity = elig_value(fin.get("shareholders_equity"))
    fcf = elig_value(fin.get("fcf_ttm"))

    for e in reg.entities:
        if e.get("credit") is not None:
            e["credit"]["liquidity_months"] = liquidity_months(e)

    for r in reg.relationships:
        am = r["amounts"]
        g, missing, parts = gross(r)
        cu = parts["committed_unfunded"]
        cont = parts["contingent_max"]
        funded = parts["funded"]
        d = {"label": "analysis", "committed_unfunded": cu, "gross_exposure": g if (g or not missing) else None,
             "gross_missing": missing, "gross_lower_bound": bool(missing),
             "funded_split_unknown": funded_split_unknown(r)}
        if g == 0 and missing:
            d["gross_exposure"] = None
        rate = (draw["base"].get(r["type_primary"]) or {}).get("rate")
        base_known = (funded or 0) + (cu or 0)
        if cont:
            d["ead_base"] = base_known + cont * rate if rate is not None else None
            d["ead_base_note"] = (draw["base"].get(r["type_primary"]) or {}).get("basis", "Not estimated.")
        else:
            d["ead_base"] = base_known if d["gross_exposure"] is not None else None
        d["ead_max"] = (base_known + (cont or 0)) if d["gross_exposure"] is not None else None
        # worst case for one relationship on its own: everything drawn, nothing recovered
        d["loss_max"] = d["ead_max"]
        d["loss_max_note"] = "Upper bound. Assumes every contingent amount is drawn and no value is received or recovered."
        d["loss_base"] = None
        d["loss_base_note"] = "Not estimated. A base case loss needs a sourced value for what Nvidia receives or recovers."

        mi = r.get("measure_inputs") or {}
        spend, raised, paid, debt = (elig_value(mi.get(k)) for k in ("counterparty_nvidia_spend", "counterparty_equity_raised", "nvidia_paid", "covered_project_debt"))
        nv_in = (funded or 0) + (cu or 0) if (funded is not None or cu is not None) else None
        d["circularity_ratio"] = {"value": None, "window": mi.get("window"), "inputs": []}
        if spend and nv_in:
            d["circularity_ratio"] = {"value": nv_in / spend, "window": mi.get("window"),
                                      "inputs": [{"field": "funded + committed not yet paid", "value": nv_in}, _ref("counterparty_nvidia_spend", mi["counterparty_nvidia_spend"])]}
        d["round_trip"] = {"nvidia_paid": paid, "counterparty_nvidia_spend": spend, "window": mi.get("window"), "inputs": []}
        if paid is not None and spend is not None:
            d["round_trip"]["inputs"] = [_ref("nvidia_paid", mi["nvidia_paid"]), _ref("counterparty_nvidia_spend", mi["counterparty_nvidia_spend"])]
        else:
            d["round_trip"]["nvidia_paid"] = d["round_trip"]["counterparty_nvidia_spend"] = None
        d["share_of_counterparty_capital"] = {"value": None, "inputs": []}
        if funded and raised and r["type_primary"] in ("EQ", "EQ-SPV", "EQ-C"):
            d["share_of_counterparty_capital"] = {"value": funded / raised, "inputs": [_ref("funded", am["funded"]), _ref("counterparty_equity_raised", mi["counterparty_equity_raised"])]}
        d["share_of_nvda_equity"] = {"value": None, "inputs": []}
        if equity and d["gross_exposure"] is not None:
            d["share_of_nvda_equity"] = {"value": d["gross_exposure"] / equity, "inputs": [{"field": "gross_exposure", "value": d["gross_exposure"]}, _ref("nvidia_financials.shareholders_equity", fin["shareholders_equity"])]}
        d["share_of_nvda_fcf"] = {"value": None, "inputs": []}
        annual = elig_value(am.get("annual_obligation")) if am.get("annual_obligation") else None
        annual_src = "sourced"
        if not annual and cu and remaining_years(r, today):
            annual, annual_src = cu / remaining_years(r, today), "derived: committed not yet paid divided by remaining years"
        d["annual_obligation"] = {"value": annual, "basis": annual_src if annual else None}
        if annual and fcf:
            d["share_of_nvda_fcf"] = {"value": annual / fcf, "inputs": [{"field": "annual_obligation", "value": annual, "basis": annual_src}, _ref("nvidia_financials.fcf_ttm", fin["fcf_ttm"])]}
        d["backstop_coverage"] = {"value": None, "inputs": []}
        if cont and debt and r["type_primary"] in ("BK", "GU", "RV"):
            d["backstop_coverage"] = {"value": cont / debt, "inputs": [_ref("contingent_max", am["contingent_max"]), _ref("covered_project_debt", mi["covered_project_debt"])]}
        r["derived"] = d

    scored = [r for r in reg.relationships if not r.get("aggregate_of") and r["type_primary"] != "CX"]
    gross_pop = [r["derived"]["gross_exposure"] for r in scored]
    circ_pop = [r["derived"]["circularity_ratio"]["value"] for r in scored]
    w, neutral = sig_cfg["weights"], sig_cfg["missing_component_score"]
    for r in reg.relationships:
        if r not in scored:
            r["significance"] = {"score": None, "components": {}, "missing": []}
            continue
        d = r["derived"]
        g = d["gross_exposure"]
        cont = elig_value(r["amounts"].get("contingent_max"))
        comp = {
            "gross_percentile": percentile(g, gross_pop),
            "contingent_share": (cont / g) if (g and cont is not None) else (0.0 if g else None),
            "circularity_percentile": percentile(d["circularity_ratio"]["value"], circ_pop),
            "counterparty_weakness": weakness(reg.ent.get(r["to"], {}), rubric),
            "lender_reliance": 1.0 if any(c.get("lens") == "lender_reliance" for c in r["consequences"]["second_order"]) and any(
                reg.ent.get(l["entity"], {}).get("cluster") == "lender" for l in r.get("depth2_links") or []) else
                0.5 if any(c.get("lens") == "lender_reliance" for c in r["consequences"]["second_order"]) else 0.0,
        }
        missing = [k for k, v in comp.items() if v is None]
        score = sum(w[k] * (neutral if v is None else v) for k, v in comp.items())
        r["significance"] = {"score": round(score, 1), "components": {k: (None if v is None else round(v, 3)) for k, v in comp.items()}, "missing": missing, "label": "analysis"}
    return reg


def main():
    reg = Register()
    run(reg)
    reg.save()
    print(f"derived measures written for {len(reg.relationships)} relationships")


if __name__ == "__main__":
    main()
