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
        g = defaultdict(lambda: {"count": 0, "funded": 0.0, "committed_unfunded": 0.0, "contingent_max": 0.0, "gross": 0.0, "headline": 0.0, "lower_bound": 0})
        for r in core:
            k = keyfn(r)
            ig = independent_gross(r)
            row = g[k]
            row["count"] += 1
            for f in ("funded", "committed_unfunded", "contingent_max"):
                row[f] += ig[f] or 0
            row["gross"] += ig["gross"]
            row["lower_bound"] += bool(ig["missing"])
            h = elig_value(r["amounts"].get("headline"))
            if h and not r["amounts"]["headline"].get("not_applicable"):
                row["headline"] += h
        return dict(sorted(g.items(), key=lambda kv: -kv[1]["gross"]))

    by_cp = group(lambda r: r["to"])
    totals = independent_totals(reg)
    binding = totals["gross"]
    out = {
        "as_of": today.isoformat(), "label": "analysis",
        "totals": totals,
        "headline_binding_share": (min(binding, totals["headline"]) / totals["headline"]) if totals["headline"] else None,
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
    lines = [f"### {title}", "", "| Group | Relationships | Funded | Committed, not yet paid | Contingent maximum | Gross | Headline | Lower bounds |", "|---|---|---|---|---|---|---|---|"]
    for k, v in groups.items():
        lines.append(f"| {namefn(k)} | {v['count']} | {fmt.money(v['funded'])} | {fmt.money(v['committed_unfunded'])} | {fmt.money(v['contingent_max'])} | {fmt.money(v['gross'])} | {fmt.money(v['headline'])} | {v['lower_bound']} |")
    return "\n".join(lines) + "\n"


def main():
    reg = Register()
    sv = build(reg)
    reg.save()
    save_json(REGISTER / "system_view.json", sv)
    t = sv["totals"]
    md = ["# R9 system view", "", f"Computed {sv['as_of']} from display-eligible amounts only. Label: analysis. Unattributed remainders and context records are excluded.", "",
          "## Totals", "",
          f"- Relationships counted: {t['count']} ({t['lower_bound_count']} are lower bounds because at least one component is not disclosed or not confirmed)",
          f"- Funded: {fmt.money(t['funded'])} across {t['counts']['funded']} relationships",
          f"- Committed, not yet paid (or paid portion not disclosed): {fmt.money(t['committed_unfunded'])} across {t['counts']['committed_unfunded']}",
          f"- Contingent maximum: {fmt.money(t['contingent_max'])} across {t['counts']['contingent_max']}",
          f"- Gross exposure: at least {fmt.money(t['gross'])}",
          f"- Headline announced (never added to exposure): {fmt.money(t['headline'])} across {t['counts']['headline']}", ""]
    md.append(table("By exposure type", sv["by_type"], lambda k: f"{k} {TYPE_NAMES[k]}"))
    md.append(table("By cluster", sv["by_cluster"]))
    md.append(table("By status", sv["by_status"]))
    md.append(table("By counterparty grade (internal)", sv["by_grade"]))
    md.append(table("By tenor", sv["by_tenor"]))
    md.append(table("By wrong-way risk", sv["by_wwr"]))
    md.append(table("By reconciliation result", sv["by_reconciliation"]))
    md += ["### Top five concentrations by gross exposure", "", "| Counterparty | Gross | Share of gross | Relationships |", "|---|---|---|---|"]
    for c in sv["top_concentrations"]:
        md.append(f"| {c['name']} | {fmt.money(c['gross'])} | {fmt.pct(c['share_of_gross'])} | {c['count']} |")
    md += ["", "## Scenarios at default parameters", "", "These illustrate how losses would travel, not forecasts.", ""]
    s1 = sv["scenarios"]["S1"]
    md += [f"### S1 Demand pause", f"- Parameters: {s1['parameters']}", f"- Backstop draws computed: {len(s1['backstop_draws'])}; equity stakes haircut: {len(s1['equity_losses'])}",
           f"- Loss: {fmt.money(s1['loss'])} on exposure of {fmt.money(s1['ead'])}; share of Nvidia equity {fmt.pct(s1['loss_share_of_equity'])}",
           f"- Not computable: {len(s1['not_computable'])} items", ""]
    for lab, s2 in sv["scenarios"]["S2"].items():
        md += [f"### S2 Lab funding gap: {reg.ent.get(lab, {}).get('short_name', lab)}",
               f"- Nvidia equity loss after haircut: {fmt.money(s2['loss'])}; conditional commitments that lapse: {len(s2['lapsed_commitments'])}; at-risk compute commitments: {fmt.money(s2['at_risk_backlog_total'])} across {len(s2['at_risk_backlog'])} counterparties; not computable: {len(s2['not_computable'])}", ""]
    s3 = sv["scenarios"]["S3"]
    md += ["### S3 Collateral repricing", f"- Facilities computed: {len(s3['facilities'])}; not computable: {len(s3['not_computable'])}", ""]
    (ROOT / "research" / "reports" / "R9_system_view.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md[:14]))


if __name__ == "__main__":
    main()
