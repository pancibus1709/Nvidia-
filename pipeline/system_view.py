"""R9 system-level view: totals by type, cluster, status, grade and tenor; top concentrations; scenarios.

  python3 -m pipeline.system_view     writes research/reports/R9_system_view.md and data/register/system_view.json
Only display-eligible amounts are used. Unattributed remainders and context records are excluded from totals.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import date

from . import fmt, measure, scenarios
from .checks import Register, elig_value, independent_gross, independent_totals
from .common import REGISTER, ROOT, save_json

TYPE_NAMES = {"EQ": "Direct equity", "EQ-SPV": "Vehicle equity", "EQ-C": "Conditional equity commitment", "BK": "Capacity backstop",
              "LB": "Leaseback or capacity rental", "GU": "Guarantee", "RV": "Residual value or repurchase", "FC": "Financing commitment",
              "LP": "Fund commitment", "PP": "Supply prepayment", "LI": "License or acqui-hire", "CX": "Context"}


def tenor_bucket(r, today):
    m = r["dates"].get("maturity")
    if not m:
        return "No stated maturity"
    yrs = int(m[:4]) - today.year + ((int(m[5:7]) if len(m) >= 7 else 12) - today.month) / 12
    return "Under 2 years" if yrs < 2 else "2 to 5 years" if yrs < 5 else "5 to 10 years" if yrs < 10 else "Over 10 years"


def build(reg: Register, today: date | None = None) -> dict:
    today = today or date.today()
    measure.run(reg, today)
    core = [r for r in reg.relationships if not r.get("aggregate_of") and r["type_primary"] != "CX"]

    def group(keyfn):
        g = defaultdict(lambda: {"count": 0, "funded": 0.0, "committed_unfunded": 0.0, "committed_split_unknown": 0.0, "contingent_max": 0.0,
                                 "contingent_not_in_force": 0.0, "gross": 0.0, "headline": 0.0, "lower_bound": 0, "funded_known": 0})
        for r in core:
            k = keyfn(r)
            ig = independent_gross(r)
            row = g[k]
            row["count"] += 1
            for f in ("funded", "committed_unfunded", "committed_split_unknown", "contingent_max", "contingent_not_in_force"):
                row[f] += ig[f] or 0
            row["funded_known"] += ig["funded"] is not None
            row["gross"] += ig["gross"]
            row["lower_bound"] += bool(ig["lower_bound"])
            h = elig_value(r["amounts"].get("headline"))
            if h and not r["amounts"]["headline"].get("not_applicable"):
                row["headline"] += h
        return dict(sorted(g.items(), key=lambda kv: -kv[1]["gross"]))

    by_cp = group(lambda r: r["to"])
    totals = independent_totals(reg)
    fin = reg.financials or {}

    def f(key):
        a = fin.get(key)
        return elig_value(a) if isinstance(a, dict) else None

    def named(pred, field):
        return sum((independent_gross(r)[field] or 0) for r in core if pred(r))

    public_named = sum(elig_value(r["amounts"].get("market_value")) or 0 for r in core if r["amounts"].get("market_value"))
    bridge = [
        {"line": "Private stakes, carrying value", "nvidia": f("non_marketable_equity_carrying_value"), "named": None, "key": "non_marketable_equity_carrying_value",
         "note": "The register sizes private stakes at cost only where a source states the cost; see the unattributed remainder."},
        {"line": "Public equity, fair value", "nvidia": f("marketable_equity_fair_value"), "named": public_named, "key": "marketable_equity_fair_value",
         "note": "Named column is the value in Nvidia's holdings report of 30 September 2026."},
        {"line": "Guarantees, maximum", "nvidia": f("total_guarantees_max"), "named": named(lambda r: r["type_primary"] in ("GU", "RV"), "contingent_max"), "key": "total_guarantees_max", "note": ""},
        {"line": "Neocloud agreements, maximum", "nvidia": f("neocloud_agreements_max"), "named": named(lambda r: r["type_primary"] == "BK", "contingent_max"), "key": "neocloud_agreements_max",
         "note": "No counterparty states its share of this maximum."},
        {"line": "Cloud service agreements", "nvidia": f("cloud_service_agreements"), "named": named(lambda r: r["type_primary"] == "LB", "committed_split_unknown") + named(lambda r: r["type_primary"] == "LB", "committed_unfunded"), "key": "cloud_service_agreements",
         "note": "Named column is contract value at signing, not the balance still owed."},
        {"line": "Unfunded equity commitments", "nvidia": f("unfunded_equity_commitments"), "named": named(lambda r: r["type_primary"] in ("EQ", "EQ-SPV", "EQ-C", "FC"), "committed_unfunded"), "key": "unfunded_equity_commitments",
         "note": "Named column counts only amounts confirmed not yet paid."},
        {"line": "Equity purchases, nine months", "nvidia": f("equity_purchases_9m"), "named": None, "key": "equity_purchases_9m", "note": "Cash Nvidia paid for equity securities in the period."},
        {"line": "Data center leases signed, not commenced", "nvidia": f("data_center_leases_not_commenced"), "named": None, "key": "data_center_leases_not_commenced", "note": "Nvidia says it may assign some of these leases to third parties."},
    ]
    positions = sorted(({"relationship": r["id"], "name": reg.ent[r["to"]]["short_name"], "value": elig_value(r["amounts"]["market_value"]),
                         "as_of": r["amounts"]["market_value"].get("as_of"), "cost_known": elig_value(r["amounts"].get("funded")) is not None}
                        for r in core if r["amounts"].get("market_value") and elig_value(r["amounts"]["market_value"])), key=lambda x: -x["value"])
    tiers = defaultdict(int)
    for e in reg.evidence:
        tiers[e["tier"]] += 1
    out = {
        "as_of": today.isoformat(), "label": "analysis",
        "totals": totals,
        "bridge": bridge,
        "positions_by_value": positions[:8],
        "source_mix": {"evidence_by_tier": dict(tiers), "one_sided_relationships": sum(1 for r in core if r["reconciliation"]["result"] == "one_sided"), "relationships": len(core),
                       "note": "Pages from the named news publications could not be read when this register was compiled, so almost every figure rests on filings and company releases. Reported figures that could not be read are listed as needing a quote and are not shown."},
        "by_type": group(lambda r: r["type_primary"]),
        "by_cluster": group(lambda r: reg.ent[r["to"]]["cluster"]),
        "by_status": group(lambda r: r["status"]),
        "by_grade": group(lambda r: (reg.ent[r["to"]].get("credit") or {}).get("grade") or "Insufficient information"),
        "by_tenor": group(lambda r: tenor_bucket(r, today)),
        "by_wwr": group(lambda r: r["credit"]["wwr"]),
        "by_reconciliation": group(lambda r: r["reconciliation"]["result"]),
        "top_concentrations": [{"entity": k, "name": reg.ent[k]["short_name"], **v, "share_of_gross": (v["gross"] / totals["gross"]) if totals["gross"] else None}
                               for k, v in list(by_cp.items())[:5]],
        "scenarios": scenarios.run_all(reg),
    }
    return out


def table(title, groups, namefn=lambda k: k):
    lines = [f"### {title}", "", "| Group | Relationships | Funded and still held (cost) | Committed, confirmed not yet paid | Committed, paid portion not disclosed | Contingent maximum | of which not yet in force | Gross | Headline | Lower bounds |", "|---|---|---|---|---|---|---|---|---|---|"]
    for k, v in groups.items():
        lines.append(f"| {namefn(k)} | {v['count']} | {fmt.money(v['funded'])} | {fmt.money(v['committed_unfunded'])} | {fmt.money(v['committed_split_unknown'])} | {fmt.money(v['contingent_max'])} | {fmt.money(v['contingent_not_in_force'])} | {fmt.money(v['gross'])} | {fmt.money(v['headline'])} | {v['lower_bound']} |")
    return "\n".join(lines) + "\n"


def m(v):
    return "Not disclosed" if v is None else fmt.money(v)


def main():
    reg = Register()
    sv = build(reg)
    reg.save()
    save_json(REGISTER / "system_view.json", sv)
    t, c = sv["totals"], sv["totals"]["counts"]
    sm = sv["source_mix"]
    hg = t["headline_groups"]
    md = ["# R9 system view", "",
          f"Computed {sv['as_of']} from display-eligible amounts only. Label: analysis. Unattributed remainders and context records are excluded.", "",
          f"**How far the sources reach.** {sm['note']} The register holds {sum(sm['evidence_by_tier'].values())} citations: {sm['evidence_by_tier'].get('1', 0)} from filings, company releases and other primary sources, {sm['evidence_by_tier'].get('2', 0)} from news publications. {sm['one_sided_relationships']} of {sm['relationships']} relationships are disclosed by one side only.", "",
          "## Totals", "",
          f"- Relationships counted: {t['count']} ({t['lower_bound_count']} are lower bounds because at least one component is not disclosed or not confirmed)",
          f"- Funded and still held, at cost: {fmt.money(t['funded'])} across {c['funded']} relationships. Cash paid to date including shares since sold: {fmt.money(t['funded_cash'])}. Funded counts only stakes whose cost a source states; Nvidia's own accounts show far more (see the bridge below).",
          f"- Committed, confirmed not yet paid: {fmt.money(t['committed_unfunded'])} across {c['committed_unfunded']}",
          f"- Committed, paid portion not disclosed: {fmt.money(t['committed_split_unknown'])} across {c['committed_split_unknown']}. These are binding amounts where no source says how much has been paid, so they are not called unpaid.",
          f"- Contingent maximum: {fmt.money(t['contingent_max'])} across {c['contingent_max']}, of which signed but not yet in force: {fmt.money(t['contingent_not_in_force'])}; in force today: {fmt.money(t['contingent_in_force'])}",
          f"- Gross exposure: at least {fmt.money(t['gross'])}",
          f"- Headline announced (never added to exposure): {fmt.money(t['headline'])} across {c['headline']}, in three unlike groups: guaranty and backstop figures {fmt.money(hg['guaranty_backstop'])}; announced but not binding or not followed by a disclosed agreement {fmt.money(hg['not_binding'])}; other announced amounts (equity, rentals, prepayments, options Nvidia holds) {fmt.money(hg['other'])}"
          + ("; excludes " + ", ".join(f"{x['currency']} {x['value'] / 1e9:g} billion ({x['relationship']})" for x in t["headline_not_converted"]) + ", not converted" if t["headline_not_converted"] else ""), ""]
    md += ["## Bridge to Nvidia's own disclosures", "", "What Nvidia reports in total, beside what this register can name and size. Label: analysis.", "",
           "| Line | Nvidia reports | Named and sized in this register | Note |", "|---|---|---|---|"]
    for b in sv["bridge"]:
        md.append(f"| {b['line']} | {m(b['nvidia'])} | {'' if b['named'] is None else fmt.money(b['named'])} | {b['note']} |")
    md += ["", "## Largest positions by current value where known", "", "Value in Nvidia's holdings report. A position whose cost is not disclosed adds nothing to gross exposure above, so it is shown here.", "",
           "| Counterparty | Value | As of | Cost disclosed |", "|---|---|---|---|"]
    for p in sv["positions_by_value"]:
        md.append(f"| {p['name']} | {fmt.money(p['value'])} | {p['as_of']} | {'Yes' if p['cost_known'] else 'No'} |")
    md.append("")
    md.append(table("By exposure type", sv["by_type"], lambda k: f"{k} {TYPE_NAMES[k]}"))
    md.append(table("By cluster", sv["by_cluster"]))
    md.append(table("By status", sv["by_status"]))
    md.append(table("By counterparty grade (internal)", sv["by_grade"]))
    md.append(table("By tenor", sv["by_tenor"]))
    md.append(table("By wrong-way risk", sv["by_wwr"]))
    md.append(table("By reconciliation result", sv["by_reconciliation"]))
    md += ["### Top five concentrations by gross exposure", "", "| Counterparty | Gross | Share of gross | Funded and still held | Relationships |", "|---|---|---|---|---|"]
    for x in sv["top_concentrations"]:
        md.append(f"| {x['name']} | {fmt.money(x['gross'])} | {fmt.pct(x['share_of_gross'])} | {fmt.money(x['funded']) if (x['funded_known'] and not (x['funded'] == 0 and x['committed_split_unknown'])) else 'Not disclosed'} | {x['count']} |")
    md += ["", "## Scenarios at default parameters", "", "These illustrate how losses would travel, not forecasts.", ""]
    s1 = sv["scenarios"]["S1"]
    md += ["### S1 Demand pause", f"- Parameters: {s1['parameters']}",
           f"- Loss on {len(s1['equity_losses'])} neocloud equity stakes only: {fmt.money(s1['loss'])}. " + ("No backstop draw is computable: the contracted floors are not disclosed. " if not s1["backstop_draws"] else f"Backstop draws computed: {len(s1['backstop_draws'])}. ") + "Guaranties of leases sit outside this scenario.",
           f"- Not computable: {len(s1['not_computable'])} items", ""]
    for lab, s2 in sv["scenarios"]["S2"].items():
        nc_eq = [x for x in s2["not_computable"] if "relationship" in x]
        line = f"- Equity loss after haircut: {fmt.money(s2['loss'])} on stakes with a confirmed value" if s2["equity_losses"] else "- Equity loss: not computable"
        if nc_eq:
            line += "; not computable for " + ", ".join(x["relationship"] for x in nc_eq)
        g = s2.get("guaranties_triggered_by_lab_default") or []
        if g:
            line += ". Guaranties that this lab's default would trigger: " + "; ".join(f"{fmt.money(x['cap'])} cap" + ("" if x["in_force"] else ", not yet in force") for x in g)
        md += [f"### S2 Lab funding gap: {reg.ent.get(lab, {}).get('short_name', lab)}", line,
               f"- Conditional commitments or letters of intent to this lab: {len(s2['lapsed_commitments'])}; compute commitments at risk: {fmt.money(s2['at_risk_backlog_total'])} across {len(s2['at_risk_backlog'])} counterparties", ""]
    s3 = sv["scenarios"]["S3"]
    md += ["### S3 Collateral repricing", f"- Facilities computed: {len(s3['facilities'])}; not computable: {len(s3['not_computable'])} (needs both a sourced balance and a sourced collateral value)", ""]
    (ROOT / "research" / "reports" / "R9_system_view.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md[4:16]))


if __name__ == "__main__":
    main()
