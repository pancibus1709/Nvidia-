"""Stress scenarios S1 to S3 (spec/05 section 7). Illustrations of how losses would travel, not forecasts.

Only display-eligible amounts are used. Anything whose inputs are not sourced is listed as not computable.
The page recomputes these with the same formulas when a slider moves; tests compare the two.
"""
from __future__ import annotations

from .checks import Register, elig_value
from .common import CONFIG, load_json

EQUITY_TYPES = ("EQ", "EQ-SPV")


def params(name: str, overrides: dict | None = None) -> dict:
    cfg = load_json(CONFIG / "scenarios.json")[name]["parameters"]
    p = {k: v["value"] for k, v in cfg.items()}
    p.update(overrides or {})
    return p


def equity_at_risk(r: dict):
    """Value of an equity stake for haircut purposes: market value if eligible, else carrying value, else funded cost."""
    if r["status"] == "terminated":
        return None, None
    for k in ("market_value", "carrying_value"):
        v = elig_value(r["amounts"].get(k)) if r["amounts"].get(k) else None
        if v:
            return v, k
    from .checks import funded_remaining
    v = funded_remaining(r)
    return (v, "funded_remaining") if v else (None, None)


def utilization(contracted_share, merchant_share, d, p, e):
    u = contracted_share + merchant_share * (1 + d) * (1 + e * p)
    return max(0.0, min(1.0, u))


def _shares(reg, base_ead, base_loss):
    fin = reg.financials or {}
    eq, fcf = elig_value(fin.get("shareholders_equity")), elig_value(fin.get("fcf_ttm"))
    return {"ead": base_ead, "loss": base_loss,
            "loss_share_of_equity": (base_loss / eq) if eq else None,
            "loss_share_of_fcf": (base_loss / fcf) if fcf else None}


def s1(reg: Register, overrides=None) -> dict:
    p = params("S1", overrides)
    draws, eq_losses, nc, affected = [], [], [], set()
    for r in reg.relationships:
        if r.get("aggregate_of"):
            continue
        ent = reg.ent.get(r["to"], {})
        if r["type_primary"] == "BK":
            si = r.get("stress_inputs") or {}
            vals = {k: (si.get(k) or {}).get("value") if isinstance(si.get(k), dict) else None
                    for k in ("contracted_share", "merchant_share", "contracted_floor", "capacity_value_per_quarter")}
            cmax = elig_value(r["amounts"].get("contingent_max"))
            if any(v is None for v in vals.values()):
                nc.append({"relationship": r["id"], "reason": "Backstop draw needs a sourced contracted floor, contracted and merchant shares, and the quarterly value of the capacity. Missing: "
                           + ", ".join(k for k, v in vals.items() if v is None)})
                affected.add(r["to"])
                continue
            u = utilization(vals["contracted_share"], vals["merchant_share"], p["d"], p["p"], p["e"])
            draw = max(0.0, vals["contracted_floor"] - u) * vals["capacity_value_per_quarter"] * p["quarters"]
            if cmax is not None:
                draw = min(draw, cmax)
            draws.append({"relationship": r["id"], "utilization": round(u, 4), "draw": draw})
            affected.add(r["to"])
        if r["type_primary"] in EQUITY_TYPES and ent.get("cluster") == "neocloud":
            v, basis = equity_at_risk(r)
            if v is None:
                nc.append({"relationship": r["id"], "reason": "No confirmed value for this stake."})
            else:
                eq_losses.append({"relationship": r["id"], "basis": basis, "value": v, "loss": v * p["h1"]})
            affected.add(r["to"])
    low_liq = [e["id"] for e in reg.entities if e.get("cluster") == "neocloud"
               and ((e.get("credit") or {}).get("liquidity_months") or {}).get("value") is not None
               and e["credit"]["liquidity_months"]["value"] < 12]
    loss = sum(x["draw"] for x in draws) + sum(x["loss"] for x in eq_losses)
    ead = sum(x["draw"] for x in draws) + sum(x["value"] for x in eq_losses)
    return {"id": "S1", "name": "Demand pause", "parameters": p, "backstop_draws": draws, "equity_losses": eq_losses,
            "liquidity_below_12_months": low_liq, "affected": sorted(affected), "not_computable": nc, **_shares(reg, ead, loss), "label": "analysis"}


def labs(reg: Register) -> list[str]:
    return sorted({r["to"] for r in reg.relationships if reg.ent.get(r["to"], {}).get("cluster") == "ai_lab" and not r.get("aggregate_of")})


def s2(reg: Register, overrides=None) -> dict:
    p = params("S2", overrides)
    lab_ids = labs(reg)
    lab = p.get("lab") or (lab_ids[0] if lab_ids else None)
    p["lab"] = lab
    eq_losses, lapsed, at_risk, nc, affected, guaranties = [], [], [], [], set(), []
    if lab:
        affected.add(lab)
        for r in reg.relationships:
            if r["to"] != lab or r.get("aggregate_of"):
                continue
            if r["type_primary"] in EQUITY_TYPES:
                v, basis = equity_at_risk(r)
                if v is None:
                    c = elig_value(r["amounts"].get("committed_total"))
                    nc.append({"relationship": r["id"], "reason": (f"Equity loss not computable: {c:,.0f} committed, paid amount not disclosed." if c else "No confirmed value for this stake.")})
                else:
                    eq_losses.append({"relationship": r["id"], "basis": basis, "value": v, "loss": v * p["h2"]})
            if r["type_primary"] in ("GU", "RV") and elig_value(r["amounts"].get("contingent_max")):
                cm = r["amounts"]["contingent_max"]
                guaranties.append({"relationship": r["id"], "cap": cm["value"], "in_force": cm.get("in_force", True), "effective_note": cm.get("effective_note", "")})
            if r["type_primary"] == "EQ-C":
                h = elig_value(r["amounts"].get("headline"))
                lapsed.append({"relationship": r["id"], "headline": h, "status": r["status"]})
        for cc in reg.ent.get(lab, {}).get("compute_commitments") or []:
            v = elig_value(cc["amount"])
            affected.add(cc["counterparty"])
            if v is None:
                nc.append({"entity": cc["counterparty"], "reason": f"Commitment amount not confirmed: {cc['description']}"})
            else:
                at_risk.append({"counterparty": cc["counterparty"], "description": cc["description"], "amount": v,
                                "as_of": cc["amount"].get("as_of"), "evidence": cc["amount"].get("evidence", [])})
    loss = sum(x["loss"] for x in eq_losses)
    ead = sum(x["value"] for x in eq_losses)
    return {"id": "S2", "name": "Lab funding gap", "parameters": p, "labs": lab_ids, "equity_losses": eq_losses, "lapsed_commitments": lapsed, "guaranties_triggered_by_lab_default": guaranties,
            "at_risk_backlog": at_risk, "at_risk_backlog_total": sum(x["amount"] for x in at_risk),
            "affected": sorted(affected), "not_computable": nc, **_shares(reg, ead, loss), "label": "analysis"}


def s3(reg: Register, overrides=None) -> dict:
    p = params("S3", overrides)
    rows, nc, affected = [], [], set()
    for pr in reg.projects:
        for f in pr.get("financing") or []:
            bal, col = elig_value(f.get("balance")), elig_value(f.get("collateral_value"))
            if bal is None or not col:
                nc.append({"project": pr["id"], "facility": f["facility"], "reason": "Needs both a sourced balance and a sourced collateral value."})
                continue
            ltv0, ltv1 = bal / col, bal / (col * (1 + p["v"])) if (1 + p["v"]) > 0 else None
            cov = f.get("covenant_ltv")
            rows.append({"project": pr["id"], "entity": pr["entity"], "facility": f["facility"], "ltv_before": ltv0, "ltv_after": ltv1,
                         "covenant_ltv": cov, "over_covenant": (ltv1 > cov) if (cov and ltv1 is not None) else None})
            affected.add(pr["entity"])
    return {"id": "S3", "name": "Collateral repricing", "parameters": p, "facilities": rows, "affected": sorted(affected),
            "not_computable": nc, **_shares(reg, 0.0, 0.0), "nvidia_loss_note": "Collateral repricing hits lenders first. Nvidia's loss is indirect and is not estimated here.", "label": "analysis"}


def run_all(reg: Register) -> dict:
    cfg = load_json(CONFIG / "scenarios.json")
    return {"note": "These illustrate how losses would travel, not forecasts.", "config": {k: v for k, v in cfg.items() if not k.startswith("_")},
            "S1": s1(reg), "S2": {lab: s2(reg, {"lab": lab}) for lab in labs(reg)} or {"none": s2(reg)}, "S3": s3(reg)}
