"""Write site/index.html from data/published/ (spec/07, spec/08, spec/10 B3 to B6).

  python3 -m pipeline.build_site

Everything a reader needs is rendered into the HTML at build time: summary, tiles, Ledger rows, every relationship's
full detail, the verdict, What changed and Method. Script adds the map, filters, sorting, the slide-in panel,
the timeline brush, the stress sliders and shareable URLs. Nothing loads from other websites.
"""
from __future__ import annotations

import html
import json
from collections import defaultdict
from datetime import date

from . import fmt
from .common import PUBLISHED, ROOT, load_json
from .site_assets import CSS, JS

SITE = ROOT / "site"
E = lambda s: html.escape("" if s is None else str(s), quote=True)
RINGS = [("ai_lab", "AI labs"), ("neocloud", "Neoclouds"), ("hyperscaler", "Hyperscalers and offtakers"), ("semis_supply", "Semis and supply"),
         ("sovereign", "Sovereign and projects"), ("portfolio", "Portfolio"), ("other", "Other and unattributed")]
RING_OF = {"ai_lab": 0, "neocloud": 1, "hyperscaler": 2, "semis_supply": 3, "sovereign_project": 4, "vehicle": 4, "portfolio": 5, "lender": 6, "other": 6}
TYPE_ORDER = ["EQ", "EQ-SPV", "EQ-C", "BK", "LB", "GU", "RV", "FC", "LP", "PP", "LI", "CX"]
TYPE_NAMES = {"EQ": "Equity", "EQ-SPV": "Vehicle equity", "EQ-C": "Conditional equity", "BK": "Capacity backstop", "LB": "Capacity rental",
              "GU": "Guarantee", "RV": "Residual value support", "FC": "Financing", "LP": "Fund commitment", "PP": "Supply prepayment", "LI": "License", "CX": "Context"}
WWR_LABEL = {"specific": "Specific: exposure grows as the counterparty weakens", "general": "General: moves with the AI cycle", "none": "None"}
LENS = {"revenue_quality": "Revenue quality", "lender_reliance": "Lender reliance", "collateral_loop": "Collateral loop", "contagion": "Contagion", "signaling": "Signaling"}
RECON = {"reconciled": "Reconciled", "partial": "Partly reconciled", "one_sided": "One side only", "contradicted": "Contradicted"}
SENIORITY = {"common_equity": "Common equity", "preferred_equity": "Preferred equity", "warrants": "Warrants", "spv_equity": "Vehicle equity",
             "lp_interest": "Fund interest", "senior_secured_creditor": "Senior secured creditor", "unsecured_creditor": "Unsecured creditor",
             "guarantor": "Guarantor", "contingent_buyer": "Buyer of last resort", "lessee": "Renter", "prepaying_buyer": "Prepaying buyer",
             "licensee": "Licensee", "none": "None"}
KIND_LABEL = {"guarantee": "Guarantee", "backstop": "Backstop", "residual_value_guarantee": "Residual value guarantee", "lease_guarantee": "Lease guarantee",
              "parent_guarantee": "Parent guarantee", "credit_support": "Credit support", "vendor_financing": "Vendor financing",
              "share_option_or_warrant": "Warrant to a customer", "minimum_revenue": "Minimum commitment", "compute_contract": "Contract lenders rely on"}
CHANGE_LABEL = {"added": "Added", "amount_changed": "Amount changed", "status_changed": "Status changed", "reconciliation_changed": "Reconciliation changed",
                "dates_changed": "Dates changed", "evidence_added": "Source added", "market_value": "Market value", "link_repair": "Link repaired",
                "reverified": "Re-verified", "corrected": "Corrected", "removed_from_display": "Removed from display"}


def money(v):
    return fmt.money(v)


def dl(d):
    return fmt.date_long(d) if d else "Not disclosed"


def chip(ids, label="Source", rid=None):
    ids = [i for i in (ids or []) if i]
    if not ids:
        return ""
    href = f"#srcs-{rid}" if rid else "#sources"
    n = f" ({len(ids)})" if len(ids) > 1 else ""
    return f'<a class="chip" href="{href}" data-ev="{E(" ".join(dict.fromkeys(ids)))}" aria-label="{E(label)}: open citations">{E(label)}{n}</a>'


class Site:
    def __init__(self):
        P = lambda n, d=None: load_json(PUBLISHED / n, d)
        self.rels = P("relationships.json")
        self.ents = {e["id"]: e for e in P("entities.json")}
        self.ev = {e["id"]: e for e in P("evidence.json")}
        self.projects = {p["id"]: p for p in P("projects.json", [])}
        self.events = P("events.json", [])
        self.cx = P("complex_links.json", [])
        self.loops = P("loops.json", [])
        self.cb = P("central_bank.json", {})
        self.scen = P("scenarios.json", {})
        self.s = P("summary.json")
        self.log = P("changelog.json", [])
        self.show_grades = bool(self.s.get("display", {}).get("show_grades"))
        self.relmap = {r["id"]: r for r in self.rels}
        self.events_by_rel = defaultdict(list)
        for ev in self.events:
            self.events_by_rel[ev["relationship"]].append(ev)

    def name(self, eid):
        return (self.ents.get(eid) or {}).get("short_name") or eid

    # ---------------------------------------------------------------- sources
    def source_li(self, i, with_id=False):
        e = self.ev.get(i)
        if not e:
            return ""
        idattr = f' id="src-{E(i)}"' if with_id else ""
        tier = {"1": "Primary", "2": "News", "market": "Market data"}.get(str(e.get("tier")), "")
        acc = f", accession {E(e['accession'])}" if e.get("accession") else ""
        sec = f", {E(e['section'])}" if e.get("section") else ""
        link = e.get("source_link") or e.get("url")
        return (f'<li{idattr}><span class="tier">{tier}</span>{E(e["publisher"])}, {E(dl(e.get("published")))}{acc}{sec}. '
                f'<cite>{E(e["title"])}</cite>. <q>{E(e["quote"])}</q> <a href="{E(link)}" rel="noopener" target="_blank">Open source</a></li>')

    # ---------------------------------------------------------------- panel
    def amount_cell(self, label, a, rid):
        if a is None:
            return f'<div class="amt"><span class="k">{E(label)}</span><span class="v nc">Not disclosed</span></div>'
        txt = a.get("text") or "Not disclosed"
        cls = "v" + ("" if a.get("value") else " nc")
        extra = []
        if a.get("as_of") and a.get("value"):
            extra.append(f"as of {dl(a['as_of'])}")
        if a.get("in_force") is False:
            extra.append("not yet in force")
        if a.get("stale"):
            extra.append(f'<span class="stale">Not re-verified since {E(dl(a.get("last_verified")))}</span>')
        c = chip(a.get("evidence"), "Source", rid) if a.get("value") or a.get("status") == "not_confirmed" else ""
        return (f'<div class="amt"><span class="k">{E(label)}</span><span class="{cls}">{E(txt)}</span>'
                f'<span class="d">{" ".join(x if x.startswith("<") else E(x) for x in extra)} {c}</span></div>')

    def panel(self, r):
        rid = r["id"]
        ent = self.ents.get(r["to"], {})
        am, x = r["amounts"], r["exposure"]
        sig = (r.get("significance") or {}).get("score")
        badges = (f'<span class="badge t b-{E(r["type_primary"])}">{E(r["labels"]["type"])}</span> '
                  f'<span class="badge">{E(r["labels"]["status"])}</span> <span class="badge">{E(r["labels"]["basis"])}</span> '
                  f'<span class="badge">{E(r["labels"]["cluster"])}</span>')
        if r["credit"].get("wwr") == "specific":
            badges += ' <span class="badge" style="color:var(--cochineal)">Specific wrong-way risk</span>'
        amts = "".join([self.amount_cell("Funded", am.get("funded"), rid), self.amount_cell("Committed", am.get("committed_total"), rid),
                        self.amount_cell("Contingent maximum", am.get("contingent_max"), rid), self.amount_cell("Headline", am.get("headline"), rid)])
        extra_amts = ""
        for k, lab in (("market_value", "Market value"), ("carrying_value", "Carrying value"), ("annual_obligation", "Annual obligation")):
            a = am.get(k)
            if a and (a.get("value") or a.get("status") == "not_confirmed"):
                extra_amts += self.amount_cell(lab, a, rid)
        floor = (am.get("funded") or {}).get("floor")
        floor_html = (f'<p class="note"><span class="analysis">Analysis</span> At least {E(money(floor["value"]))} paid by {E(dl(floor.get("as_of")))}: '
                      f'{E(floor["note"].replace("Analysis: ", ""))}</p>') if floor else ""
        d = r["dates"]
        lv = max([a.get("last_verified") or "" for a in am.values() if isinstance(a, dict)] or [""])
        dparts = [f"Announced {dl(d.get('announced'))}"]
        if d.get("signed"):
            dparts.append(f"Signed {dl(d['signed'])}")
        cmax = am.get("contingent_max") or {}
        if cmax.get("in_force") is False:
            dparts.append("Not yet in force" + (f": {fmt.date_long(d['effective'])}" if d.get("effective") and d["effective"] > (d.get("signed") or "") else ""))
        elif d.get("effective"):
            dparts.append(f"Effective {dl(d['effective'])}")
        dparts += [f"Matures {dl(d.get('maturity'))}", f"Last verified {dl(lv) if lv else 'Not recorded'}"]
        dates = '<p class="dates">' + " · ".join(E(x) for x in dparts) + "</p>"
        sigbar = ""
        if sig is not None:
            sigbar = (f'<div class="sig"><span>Significance</span><span class="bar"><i style="width:{min(100, sig):.0f}%"></i></span>'
                      f'<span>{sig:.0f} of 100</span> <a href="#method-significance">why</a> <span class="analysis">Analysis</span></div>')

        sec = []
        sec.append(("what", "What the deal is", f"<p>{E(r['definition'])}</p>" + (f"<p>{E(r['inclusion_reason'])}</p>" if r.get("inclusion_reason") else "")
                    + (f'<p class="note">Seniority: {E(SENIORITY.get(r.get("seniority"), r.get("seniority")))}</p>')))
        rc = r["reconciliation"]
        diffs = "".join(f"<li><b>{E(df.get('field'))}</b>: Nvidia side {E(df.get('nvidia_value'))}; counterparty side {E(df.get('counterparty_value'))} {chip(df.get('evidence'), 'Source', rid)}</li>"
                        for df in rc.get("differences") or [])
        sec.append(("sides", "Both sides", f"<p><b>Result:</b> {E(RECON.get(rc['result'], rc['result']))}</p>"
                    f"<p><b>What Nvidia disclosed.</b> {E(rc.get('nvidia_side'))} {chip(rc.get('nvidia_evidence'), 'Source', rid)}</p>"
                    f"<p><b>What {E(self.name(r['to']))} disclosed.</b> {E(rc.get('counterparty_side'))} {chip(rc.get('counterparty_evidence'), 'Source', rid)}</p>"
                    + (f"<ul>{diffs}</ul>" if diffs else "")))
        projs = [self.projects[p] for p in r.get("projects") or [] if p in self.projects]
        projs += [p for p in self.projects.values() if rid in (p.get("nvidia_link") or []) and p not in projs]
        if projs:
            rows = ""
            for p in projs:
                fin = "; ".join(f"{E(f.get('facility'))}" + (f" ({E(', '.join(f.get('lenders') or []))})" if f.get("lenders") else "") +
                                (f": {E(fmt.amount_text(f.get('balance')))}" if f.get("balance") else "") for f in p.get("financing") or [])
                mw = (p.get("power_mw_contracted") or {}).get("value")
                rows += (f"<tr><td>{E(p['name'])}</td><td>{E(p.get('location'))}</td><td class='num'>{E(f'{mw:,.0f} MW' if mw else '')}</td>"
                         f"<td>{E(p.get('anchor_tenant') or '')}</td><td>{fin}</td><td>{E('Covered' if p.get('role') == 'covered' else 'Context')}</td></tr>")
            sec.append(("projects", "Project basis", f"<div class='tbl-wrap'><table><thead><tr><th>Site</th><th>Location</th><th class='num'>Contracted</th><th>Anchor tenant</th><th>Financing</th><th>Role</th></tr></thead><tbody>{rows}</tbody></table></div>"))
        c = ent.get("credit") or {}
        credit = [f"<dt>Wrong-way risk</dt><dd>{E(WWR_LABEL.get(r['credit'].get('wwr'), ''))}. {E(r['credit'].get('wwr_reason'))}</dd>"]
        if r["credit"].get("collateral"):
            credit.append(f"<dt>Collateral</dt><dd>{E(r['credit']['collateral'])}</dd>")
        if r["credit"].get("tenor"):
            credit.append(f"<dt>Tenor</dt><dd>{E(r['credit']['tenor'])}</dd>")
        for k, lab in (("debt_outstanding", "Debt outstanding"), ("maturities_24m", "Debt due within 24 months"), ("cash_and_undrawn", "Cash and undrawn facilities"),
                       ("committed_spend_12m", "Committed spending, next 12 months")):
            a = c.get(k)
            if a and a.get("text"):
                credit.append(f"<dt>{lab}</dt><dd>{E(a['text'])}{' (at least)' if a.get('lower_bound') else ''}, {E(dl(a.get('as_of')))} {chip(a.get('evidence'), 'Source', rid)}</dd>")
        lm = (c.get("liquidity_months") or {}).get("value")
        if lm is not None:
            credit.append(f"<dt>Liquidity</dt><dd>{lm:.1f} months of committed spending <span class='analysis'>Analysis</span></dd>")
        for k, lab in (("top_customer_share", "Largest customer"), ("top3_customer_share", "Top three customers")):
            a = c.get(k)
            if a and a.get("value") is not None:
                credit.append(f"<dt>{lab}</dt><dd>{a['value'] * 100:.0f}% of revenue, {E(dl(a.get('as_of')))} {chip(a.get('evidence'), 'Source', rid)}</dd>")
        for pr in c.get("public_ratings") or []:
            credit.append(f"<dt>Rating</dt><dd>{E(pr.get('agency'))} {E(pr.get('rating'))}, {E(dl(pr.get('date')))} {chip(pr.get('evidence'), 'Source', rid)}</dd>")
        if c.get("collateral_note"):
            credit.append(f"<dt>GPU collateral</dt><dd>{E(c['collateral_note'])}</dd>")
        if self.show_grades and c.get("grade"):
            credit.append(f"<dt>Grade</dt><dd>{E(c['grade'])}. {E(c.get('grade_reason'))} <span class='analysis'>Analysis</span></dd>")
        sec.append(("credit", "Credit read", f"<dl>{''.join(credit)}</dl>"))
        dv = r.get("derived") or {}
        meas = [f"<dt>Gross exposure</dt><dd>{E(('at least ' if x['lower_bound'] else '') + money(x['gross']) if x['gross'] else 'Not sized')}"
                f"{(' (missing: ' + E(', '.join(m.replace('_', ' ') for m in x['missing'])) + ')') if x['missing'] else ''}</dd>"]
        if dv.get("ead_max") is not None:
            meas.append(f"<dt>Exposure at default, worst case</dt><dd>{E(money(dv['ead_max']))}; loss up to {E(money(dv.get('loss_max')))}. {E(dv.get('loss_max_note', ''))}</dd>")
        meas.append(f"<dt>Base case</dt><dd>{E(money(dv['ead_base']) if dv.get('ead_base') is not None else 'Not estimated')}. {E(dv.get('loss_base_note', ''))}</dd>")
        for k, lab in (("circularity_ratio", "Circularity ratio"), ("share_of_counterparty_capital", "Share of counterparty's equity raised"),
                       ("share_of_nvda_equity", "Share of Nvidia's equity"), ("share_of_nvda_fcf", "Share of Nvidia's free cash flow"), ("backstop_coverage", "Backstop coverage")):
            v = (dv.get(k) or {}).get("value")
            meas.append(f"<dt>{lab}</dt><dd>{E(fmt.pct(v, 2) if v is not None else 'Not computable: inputs not sourced')}</dd>")
        sec.append(("measures", "Exposure and derived measures", f"<p><span class='analysis'>Analysis</span> Formulas are on the Method view.</p><dl>{''.join(meas)}</dl>"))
        fo = r["consequences"].get("first_order") or []
        so = r["consequences"].get("second_order") or []
        if fo:
            sec.append(("first", "First order consequences", "<p><span class='analysis'>Analysis</span></p><ul class='cons'>" +
                        "".join(f"<li>{E(cq['text'])} {chip(cq.get('evidence'), 'Source', rid)}</li>" for cq in fo) + "</ul>"))
        if so:
            sec.append(("second", "Second order consequences", "<p><span class='analysis'>Analysis</span></p><ul class='cons'>" +
                        "".join(f"<li><span class='lens'>{E(LENS.get(cq.get('lens'), ''))}</span>{E(cq['text'])} {chip(cq.get('evidence'), 'Source', rid)}</li>" for cq in so) + "</ul>"))
        evs = sorted(self.events_by_rel.get(rid, []), key=lambda e: e["date"])
        if evs:
            sec.append(("timeline", "Timeline", "<ul class='cons'>" + "".join(f"<li><b>{E(dl(ev['date']))}</b>: {E(ev['summary'])} {chip(ev.get('evidence'), 'Source', rid)}</li>" for ev in evs) + "</ul>"))
        if r.get("notes"):
            sec.append(("notes", "Research notes", f"<p class='note'>{E(r['notes'])}</p>"))
        srcs = "".join(self.source_li(i) for i in dict.fromkeys(r["evidence"] + self.amount_ids(r)))
        sec.append(("sources", "Sources", f"<ol class='srcs' id='srcs-{E(rid)}'>{srcs}</ol>"))
        body = "".join(f"<details data-sec='{k}'><summary>{E(t)}</summary>{h}</details>" for k, t, h in sec)
        return (f'<div class="pb" id="p-{E(rid)}"><a href="#" class="xall" data-mode="expand">Expand all</a>'
                f'<h3 class="cp">{E(self.ents.get(r["to"], {}).get("name") or self.name(r["to"]))}</h3><div class="meta">{badges}</div>'
                f'<p class="note">{E(r["title"])}</p><p class="insight">{E(r["insight"])}</p>'
                f'<div class="amts">{amts}{extra_amts}</div>{floor_html}{dates}{sigbar}{body}</div>')

    def amount_ids(self, r):
        out = []
        for a in r["amounts"].values():
            if isinstance(a, dict):
                out += a.get("evidence") or []
        return out

    # ---------------------------------------------------------------- ledger
    def ledger_row(self, r, ncols):
        x = r["exposure"]
        ent = self.ents.get(r["to"], {})
        cell = lambda v, missing=False: f'<td class="num">{E(money(v)) if v else ("<span class=nc>Not disclosed</span>" if missing else "<span class=nc>0</span>")}</td>'
        committed = (x["committed_unfunded"] or 0) + (x["committed_split_unknown"] or 0)
        h = (r["amounts"].get("headline") or {})
        lv = max([a.get("last_verified") or "" for a in r["amounts"].values() if isinstance(a, dict)] or [""])
        sig = (r.get("significance") or {}).get("score")
        cls = "row" + (" terminated" if r["status"] == "terminated" else "")
        attrs = (f'data-id="{E(r["id"])}" data-cp="{E(self.name(r["to"]))}" data-gross="{x["gross"] or 0}" data-funded="{x["funded"] or 0}" '
                 f'data-committed="{committed}" data-cont="{x["contingent_max"] or 0}" data-headline="{h.get("value") or 0}" '
                 f'data-ann="{E(r["dates"].get("announced") or "")}" data-lv="{E(lv)}" data-sig="{sig or 0}"')
        grade = f"<td>{E((ent.get('credit') or {}).get('grade') or '')}</td>" if self.show_grades else ""
        row = (f'<tr class="{cls}" id="row-{E(r["id"])}" {attrs}><td><b>{E(self.name(r["to"]))}</b><br><span class="note">{E(r["title"])}</span></td>'
               f'<td>{E(r["labels"]["cluster"])}</td><td><span class="badge t b-{E(r["type_primary"])}">{E(r["type_primary"])}</span></td><td>{E(r["labels"]["status"])}</td>'
               f'{cell(x["funded"], "funded" in x["missing"])}{cell(committed)}{cell(x["contingent_max"], "contingent_max" in x["missing"])}'
               f'<td class="num">{E(("at least " if x["lower_bound"] and x["gross"] else "") + money(x["gross"])) if x["gross"] else "<span class=nc>Not sized</span>"}</td>'
               f'<td class="num">{E(h.get("text") or "")}</td><td class="dt">{E(r["dates"].get("announced") or "")}</td><td class="dt">{E(lv)}</td>'
               f'<td>{E(RECON.get(r["reconciliation"]["result"]))}</td><td class="num">{"" if sig is None else f"{sig:.0f}"}</td>{grade}</tr>')
        det = f'<tr class="detail"><td colspan="{ncols}"><details><summary>Full detail for {E(self.name(r["to"]))}</summary>{self.panel(r)}</details></td></tr>'
        return row + det

    def ledger(self):
        cols = ["Counterparty", "Cluster", "Type", "Status", "Funded and still held", "Committed", "Contingent maximum", "Gross exposure", "Headline", "Announced", "Last verified", "Both sides", "Significance"]
        keys = ["cp", "", "", "", "funded", "committed", "cont", "gross", "headline", "ann", "lv", "", "sig"]
        if self.show_grades:
            cols.append("Grade"); keys.append("")
        num = {"funded", "committed", "cont", "gross", "headline", "sig"}
        th = "".join((f'<th data-sort="{k}" class="{"num" if k in num else ""}"><button type="button">{E(c)}</button></th>' if k else f"<th>{E(c)}</th>") for c, k in zip(cols, keys))
        core = [r for r in self.rels if not r.get("aggregate_of") and r["type_primary"] != "CX"]
        core.sort(key=lambda r: -(r["exposure"]["gross"] or 0))
        body = "".join(self.ledger_row(r, len(cols)) for r in core)
        t = self.s["totals"]
        foot = (f'<tfoot><tr><td data-k="n">{t["count"]} relationships</td><td colspan="3">Totals, confirmed amounts only</td>'
                f'<td class="num" data-k="funded">{E(money(t["funded"]))}</td><td class="num" data-k="cu">{E(money(t["committed_unfunded"] + t["committed_split_unknown"]))}</td>'
                f'<td class="num" data-k="cont">{E(money(t["contingent_max"]))}</td><td class="num" data-k="gross">{E(money(t["gross"]))}</td>'
                f'<td class="num" data-k="h">{E(money(t["headline"]))}</td><td colspan="{len(cols) - 9}"></td></tr></tfoot>')
        opts = lambda name, pairs: f'<label>{name} <select name="{name.lower().replace(" ", "")}"><option value="">All</option>' + "".join(f'<option value="{E(v)}">{E(l)}</option>' for v, l in pairs) + "</select></label>"
        clusters = sorted({(r["to_cluster"], r["labels"]["cluster"]) for r in core}, key=lambda p: p[1])
        filters = ('<div class="controls" id="ledger-filters">'
                   + opts("Cluster", clusters).replace('name="cluster"', 'name="cluster"')
                   + opts("Type", [(t_, TYPE_NAMES[t_]) for t_ in TYPE_ORDER if any(r["type_primary"] == t_ for r in core)])
                   + opts("Status", sorted({(r["status"], r["labels"]["status"]) for r in core}))
                   + opts("Wrong way risk", [("specific", "Specific"), ("general", "General"), ("none", "None")]).replace('name="wrongwayrisk"', 'name="wwr"')
                   + opts("Source strength", sorted({(r["claim_basis"], r["labels"]["basis"]) for r in core})).replace('name="sourcestrength"', 'name="basis"')
                   + '<button class="btn" type="button" id="clear-filters">Clear filters</button><button class="btn" type="button" id="csv">Download CSV</button></div>')
        other = [r for r in self.rels if r.get("aggregate_of")]
        cx = [r for r in self.rels if r["type_primary"] == "CX" and not r.get("aggregate_of")]
        def sub(rows, title, note):
            if not rows:
                return ""
            b = ""
            for r in rows:
                a = next((r["amounts"][k] for k in ("funded", "committed_total", "contingent_max") if (r["amounts"].get(k) or {}).get("value")), None)
                b += (f'<tr><td><b>{E(r["title"])}</b><br><span class="note">{E(r["insight"])}</span></td><td class="num">{E(a["text"]) if a else "Not computable"}</td>'
                      f'<td>{chip(a.get("evidence") if a else r["evidence"], "Source", r["id"])}</td></tr>'
                      f'<tr class="detail"><td colspan="3"><details><summary>Full detail</summary>{self.panel(r)}</details></td></tr>')
            return f'<h3>{E(title)}</h3><p class="note">{E(note)}</p><div class="tbl-wrap"><table><tbody>{b}</tbody></table></div>'
        return (filters + '<p class="note" id="filtered-note" hidden>Filters are on. Tiles, the map and the totals row show the filtered set.</p>'
                f'<div class="tbl-wrap"><table id="ledger"><thead><tr>{th}</tr></thead><tbody>{body}</tbody>{foot}</table></div>'
                '<p class="note">Funded counts the cost of shares still held. Committed includes amounts whose paid portion is not disclosed; they are counted once and never called unpaid. Headline is what was announced and is never added. Click any row for the full detail.</p>'
                + sub(other, "Unattributed remainders of Nvidia's own totals", "What Nvidia reports in total, less what this register can name and size. Upper bounds where named stakes have no stated amount. Excluded from every total above. Label: analysis.")
                + sub(cx, "Context records", "Parties that matter to the analysis but where no Nvidia capital is involved. Excluded from every total."))

    # ---------------------------------------------------------------- data for script
    def data(self):
        rels = []
        for r in self.rels:
            x = r["exposure"]
            h = r["amounts"].get("headline") or {}
            lv = max([a.get("last_verified") or "" for a in r["amounts"].values() if isinstance(a, dict)] or [""])
            ev0 = (r["evidence"] or [None])[0]
            rels.append({"id": r["id"], "to": r["to"], "t": r["type_primary"], "tl": r["labels"]["type"], "s": r["status"], "sl": r["labels"]["status"],
                         "b": r["claim_basis"], "bl": r["labels"]["basis"], "cl": r["to_cluster"], "cll": r["labels"]["cluster"], "w": r["credit"].get("wwr"),
                         "d": r["dates"].get("announced"), "lv": lv, "rc": r["reconciliation"]["result"], "sig": (r.get("significance") or {}).get("score"),
                         "agg": bool(r.get("aggregate_of")), "h": h.get("value") if h.get("value") and not h.get("not_applicable") else 0,
                         "x": {"funded": x["funded"] or 0, "cu": x["committed_unfunded"] or 0, "csu": x["committed_split_unknown"] or 0, "cont": x["contingent_max"] or 0, "gross": x["gross"] or 0},
                         "src": (self.ev.get(ev0) or {}).get("url")})
        nodes = {}
        for r in self.rels:
            if r.get("aggregate_of") and r["to"] != "ent_nvidia_unattributed":
                continue
            eid = r["to"]
            n = nodes.setdefault(eid, {"id": eid, "name": self.name(eid), "ring": RING_OF.get(self.ents.get(eid, {}).get("cluster"), 6), "gross": 0, "headline": 0,
                                       "rels": [], "wwr": False, "lb": False, "date": None})
            if r.get("aggregate_of"):
                continue
            n["gross"] += r["exposure"]["gross"] or 0
            n["headline"] += (r["amounts"].get("headline") or {}).get("value") or 0
            n["rels"].append(r)
            n["wwr"] |= r["credit"].get("wwr") == "specific"
            n["lb"] |= r["exposure"]["lower_bound"]
            if r["dates"].get("announced") and (not n["date"] or r["dates"]["announced"] < n["date"]):
                n["date"] = r["dates"]["announced"]
        out_nodes = []
        for n in nodes.values():
            if not n["rels"]:
                continue
            top = max(n["rels"], key=lambda r: (r["exposure"]["gross"] or 0, (r["amounts"].get("headline") or {}).get("value") or 0))
            out_nodes.append({"id": n["id"], "name": n["name"], "ring": n["ring"], "gross": n["gross"], "headline": n["headline"], "type": top["type_primary"],
                              "typeLabel": ", ".join(sorted({TYPE_NAMES[r["type_primary"]] for r in n["rels"]})), "rel": top["id"], "wwr": n["wwr"], "lb": n["lb"],
                              "date": ("First announced " + dl(n["date"])) if n["date"] else None})
        out_nodes.sort(key=lambda n: (n["ring"], -n["gross"]))
        loop_ents = [[l2["from"] for l2 in lp["legs"]] + [lp["legs"][-1]["to"]] for lp in self.loops if lp.get("legs")]
        lanes = [{"key": k, "label": lab} for k, lab in RINGS]
        evs = []
        for ev in self.events:
            r = self.relmap.get(ev["relationship"])
            if not r:
                continue
            lane = RINGS[RING_OF.get(r["to_cluster"], 6)][0]
            evs.append({"date": ev["date"], "rel": ev["relationship"], "kind": ev["kind"], "summary": ev["summary"], "lane": lane})
        fin = self.s.get("financials", {})
        sc = {k: v for k, v in self.scen.items() if k in ("S1", "S2", "S3", "config")}
        sc["config"] = {k: v for k, v in sc["config"].items() if not k.startswith("_")}
        return {"rels": rels, "ents": {k: {"n": v.get("short_name"), "g": (v.get("credit") or {}).get("grade") if self.show_grades else None} for k, v in self.ents.items()},
                "relEnt": {r["id"]: r["to"] for r in self.rels}, "nodes": out_nodes, "rings": [{"key": k, "label": l} for k, l in RINGS],
                "loopEnts": loop_ents, "lanes": lanes, "events": evs, "tlStart": "2023-01-01", "tlEnd": self.s["data_as_of"], "scen": sc,
                "fin": {"equity": (fin.get("shareholders_equity") or {}).get("value"), "fcf": (fin.get("fcf_ttm") or {}).get("value")}, "showGrades": self.show_grades}

    # ---------------------------------------------------------------- page sections
    def tiles(self):
        t = self.s["totals"]
        c = t["counts"]
        committed = t["committed_unfunded"] + t["committed_split_unknown"]
        lb = t["lower_bound_count"]
        tl = [("funded", "Funded and still held", t["funded"], f"{c['funded']} relationships", "Cost of stakes Nvidia still holds, where a source states the cost."),
              ("committed", "Committed", committed, f"{c['committed_unfunded'] + c['committed_split_unknown']} relationships",
               f"Binding amounts. {money(t['committed_unfunded'])} is confirmed unpaid; for {money(t['committed_split_unknown'])} the paid portion is not disclosed."),
              ("contingent", "Contingent maximum", t["contingent_max"], f"{c['contingent_max']} relationships",
               f"The most Nvidia could be made to pay. {money(t['contingent_not_in_force'])} of it is signed but not yet in force.")]
        out = '<div class="tiles" role="group" aria-label="Exposure totals. Each filters the map and Ledger.">'
        for k, lab, v, n, note in tl:
            out += f'<button type="button" class="tile" data-k="{k}" aria-pressed="false"><span class="k">{E(lab)}</span><span class="v">{E(money(v))}</span><span class="n">{E(n)}</span><span class="n">{E(note)}</span></button>'
        out += (f'<button type="button" class="tile apart" data-k="headline" aria-pressed="false"><span class="k">Headline announced, never added</span><span class="v">{E(money(t["headline"]))}</span>'
                f'<span class="n">{c["headline"]} relationships</span><span class="n">{E(money(t["headline_groups"]["not_binding"]))} of it is letters of intent or has no disclosed agreement.</span></button></div>')
        out += (f'<p class="note">Funded, committed and contingent add up to gross exposure of at least {E(money(t["gross"]))}. It is a lower bound: '
                f'{lb} of {t["count"]} relationships have a part that is not disclosed. Click a tile to filter.</p>')
        return out

    def ranked(self, d):
        by = defaultdict(list)
        for n in d["nodes"]:
            by[n["ring"]].append(n)
        out = '<div class="ranked"><p class="note">The ranked list below is the map in text. <button type="button" class="btn full-map-btn" id="full-map">Open the radial map</button></p>'
        for i, (k, lab) in enumerate(RINGS):
            if not by.get(i):
                continue
            out += f"<h3>{E(lab)}</h3><ol>" + "".join(
                f'<li><a href="#row-{E(n["rel"])}" data-open="{E(n["rel"])}">{E(n["name"])}</a>: {E(n["typeLabel"])}; '
                f'{E((("at least " if n["lb"] else "") + money(n["gross"])) if n["gross"] else "not sized")}</li>' for n in sorted(by[i], key=lambda n: -n["gross"])) + "</ol>"
        return out + "</div>"

    def legend(self):
        rows = [("var(--cobalt)", "", "Equity"), ("#8FA6D6", "", "Conditional equity"), ("var(--cochineal)", "6 4", "Backstop or guarantee"),
                ("var(--cochineal)", "8 3 2 3", "Residual value support"), ("var(--rosa)", "1 4", "Capacity rental"), ("var(--cobalt-deep)", "", "Financing"),
                ("var(--ochre)", "", "Supply prepayment"), ("#5876B8", "3 2", "Fund commitment"), ("var(--ink-3)", "", "Context")]
        li = "".join(f'<li><svg width="34" height="10" aria-hidden="true"><line x1="0" y1="5" x2="34" y2="5" stroke="{c}" stroke-width="3" stroke-dasharray="{d}"/></svg>{E(t)}</li>' for c, d, t in rows)
        li += '<li><svg width="34" height="12" aria-hidden="true"><line x1="0" y1="6" x2="34" y2="6" stroke="var(--cobalt)" stroke-width="10" opacity=".18"/></svg>Headline beyond what is binding</li>'
        li += '<li><svg width="34" height="14" aria-hidden="true"><path d="M12,10 l7,-7 l3,10 z" fill="var(--cochineal)"/></svg>Specific wrong-way risk</li>'
        return (f'<div class="legend"><p><b>How to read it.</b> Nvidia sits at the center. Each ring is a kind of counterparty. Node and line size show gross exposure; '
                f'a faint wide halo shows the headline beyond it. Line style and color show the kind of deal.</p><ul>{li}</ul>'
                '<button type="button" class="btn" id="show-loops" aria-pressed="false">Show circular flows</button>'
                '<p class="note">Keyboard: Tab to a node, arrow keys move around a ring or between rings, Enter opens it.</p></div>')

    def loops_html(self):
        out = '<div class="loops">'
        for lp in self.loops:
            legs = "".join(
                f'<li><b>{E(self.name(l2["from"]))}</b> to <b>{E(self.name(l2["to"]))}</b>: {E(l2["description"])}'
                + (f' <span class="amtl">{E(money(l2["amount"]))}</span>' + (f' ({E(l2.get("amount_label"))})' if l2.get("amount_label") else "") if l2.get("amount") else "")
                + f' {chip(l2.get("evidence"), "Source")}</li>' for l2 in lp["legs"])
            status = "Closed loop" if lp.get("closed") else "Open at the closing leg"
            out += (f'<article class="loop"><h3>{E(lp["title"])}</h3><p class="note">{E(status)} · <span class="analysis">Analysis</span></p>'
                    f'<p>{E(lp["summary"])}</p><ol>{legs}</ol><p class="note">{E(lp.get("circularity_note"))}</p></article>')
        return out + "</div>"

    def guarantees_html(self):
        by = defaultdict(list)
        for c in self.cx:
            if not c.get("same_obligation_as"):
                by[c["provider"]].append(c)
        def best(cs):
            vals = [(a.get("value"), a.get("text"), k, c) for c in cs for k, a in c["amounts"].items() if a.get("value")]
            return max(vals, key=lambda v: v[0]) if vals else None
        rows = sorted(by.items(), key=lambda kv: -((best(kv[1]) or (0,))[0] or 0))
        t = self.s["totals"]
        nv = (self.s.get("financials", {}).get("total_guarantees_max") or {})
        body = (f'<tr><td><b>Nvidia</b></td><td class="num">{E(nv.get("text") or "")}</td><td>Guarantees of leases and other obligations, mostly OpenAI\'s rent in Ohio; '
                f'{E(money(t["contingent_not_in_force"]))} is signed but not yet in force</td><td>{chip(nv.get("evidence"), "Source")}</td></tr>')
        for prov, cs in rows:
            b = best(cs)
            if not b or b[0] < 1e9:
                continue
            kinds = ", ".join(sorted({KIND_LABEL.get(c["kind"], c["kind"]) for c in cs}))
            body += (f'<tr><td><b>{E(self.name(prov))}</b></td><td class="num">{E(b[1])}</td><td>{E(b[3]["description"][:240])}{"..." if len(b[3]["description"]) > 240 else ""}'
                     f'<br><span class="note">{len(cs)} arrangement{"s" if len(cs) > 1 else ""}: {E(kinds)}</span></td><td>{chip(b[3]["evidence"], "Source")}</td></tr>')
        same = [c for c in self.cx if c.get("same_capacity_as_nvidia") and not c.get("same_obligation_as")]
        by_obl = defaultdict(list)
        for c in same:
            key = self.relmap[c["nvidia_links"][0]]["to"] if c.get("nvidia_links") and c["nvidia_links"][0] in self.relmap else c["obligor"]
            by_obl[key].append(c)
        srows = ""
        for k, cs in sorted(by_obl.items(), key=lambda kv: -len(kv[1])):
            items = "; ".join(f"{E(self.name(c['provider']))}: {E(KIND_LABEL.get(c['kind'], c['kind']).lower())}"
                              + (f" ({E(next((a['text'] for a in c['amounts'].values() if a.get('value')), ''))})" if any(a.get("value") for a in c["amounts"].values()) else "")
                              for c in cs)
            srows += f'<tr><td><b>{E(self.name(k))}</b></td><td>{items}</td><td>{chip([i for c in cs for i in c["evidence"]][:6], "Sources")}</td></tr>'
        return (f'<p class="lede">Nvidia is the largest underwriter of AI capacity, but not the only one. Google, Broadcom and AMD stand behind demand for their own chips '
                f'with the same tools, and Meta stands behind capacity it will use. Each figure below is that company\'s largest disclosed amount, so they cannot be added across companies.</p>'
                f'<div class="tbl-wrap"><table><thead><tr><th>Provider</th><th class="num">Largest disclosed figure</th><th>What it stands behind</th><th></th></tr></thead><tbody>{body}</tbody></table></div>'
                f'<h3>Where others stand behind the same companies as Nvidia</h3>'
                f'<p class="note">{len(same)} of {len([c for c in self.cx if not c.get("same_obligation_as")])} arrangements sit on a company or site that also carries Nvidia support.</p>'
                f'<div class="tbl-wrap"><table><thead><tr><th>Company</th><th>Who else stands behind it</th><th></th></tr></thead><tbody>{srows}</tbody></table></div>')

    def central_bank_html(self):
        rows = ""
        for f in self.cb.get("functions", []):
            v = f["verdict"]
            cls = "v-" + v.split()[0]
            def lis(items):
                return "".join(f"<li>{E(i['text'])} {chip(i.get('evidence'), 'Source')}</li>" for i in items)
            rows += (f'<div class="card"><h3>{E(f["name"])}</h3><p class="note">{E(f.get("analogue"))}</p><p class="verdict {cls}">{E(v)}</p><p>{E(f.get("verdict_reason"))}</p>'
                     f'<p><b>For</b></p><ul>{lis(f.get("evidence_for", []))}</ul><p><b>Against</b></p><ul>{lis(f.get("evidence_against", []))}</ul></div>')
        return (f'<div class="cards2">{rows}</div><h3>Where the analogy breaks</h3><p class="lede">{E(self.cb.get("where_the_analogy_breaks"))} '
                f'{chip(self.cb.get("where_the_analogy_breaks_evidence"), "Sources")}</p><p class="lede"><b>{E(self.cb.get("overall"))}</b></p>'
                '<p class="note"><span class="analysis">Analysis</span> The verdicts are judgments on the evidence shown, not facts reported by any company.</p>')

    def changes_html(self):
        types = sorted({e["change_type"] for e in self.log})
        sel = '<label>Type of change <select id="change-filter"><option value="">All</option>' + "".join(f'<option value="{t}">{E(CHANGE_LABEL.get(t, t))}</option>' for t in types) + "</select></label>"
        items = ""
        for e in self.log[:400]:
            rel = e.get("relationship")
            what = CHANGE_LABEL.get(e["change_type"], e["change_type"])
            delta = ""
            if e["change_type"] != "added":
                delta = f" {E(e.get('field') or '')}: {E(e.get('old'))} to {E(e.get('new'))}."
            items += (f'<li data-type="{E(e["change_type"])}"><b>{E(dl((e.get("timestamp") or "")[:10]))}</b> · {E(what)} · '
                      f'<a href="#row-{E(rel)}" data-open="{E(rel)}">{E(e.get("counterparty") or "")}: {E(e.get("title") or rel)}</a>.{delta} {chip(e.get("evidence"), "Source")}</li>')
        return f'<div class="controls">{sel}</div><ul class="changes" id="changes">{items}</ul>'

    def method_html(self):
        s = self.s
        sm = s["source_mix"]
        bridge = "".join(f'<tr><td>{E(b["line"])}</td><td class="num">{E(money(b["nvidia"]) if b.get("nvidia") is not None else "Not disclosed")}</td>'
                         f'<td class="num">{E(b.get("named_text") or (money(b["named"]) if b.get("named") is not None else ""))}</td><td class="note">{E(b["note"])}</td></tr>' for b in s["bridge"])
        pos = "".join(f'<tr><td>{E(p["name"])}</td><td class="num">{E(money(p["value"]))}</td><td>{E(dl(p.get("as_of")))}</td><td>{"Yes" if p.get("cost_known") else "No"}</td></tr>' for p in s["positions_by_value"])
        pos += "".join(f'<tr><td>{E(p["name"])}</td><td class="num">not valued (cost {E(money(p["cost"]))})</td><td>{E(p["reason"])}</td><td>Yes</td></tr>' for p in s.get("positions_not_yet_valued", []))
        return f"""
<h3>What Nvidia reports, beside what can be named</h3>
<p>Nvidia's own accounts show far more than any outsider can tie to named deals. <span class="analysis">Analysis</span></p>
<div class="tbl-wrap"><table><thead><tr><th>Line</th><th class="num">Nvidia reports</th><th class="num">Named and sized here</th><th>Note</th></tr></thead><tbody>{bridge}</tbody></table></div>
<h3>Largest positions by value</h3>
<p class="note">Values from Nvidia's holdings report of 30 September 2026. A position whose cost is not disclosed adds nothing to gross exposure, so it is shown here.</p>
<div class="tbl-wrap"><table><thead><tr><th>Counterparty</th><th class="num">Value</th><th>As of or reason</th><th>Cost disclosed</th></tr></thead><tbody>{pos}</tbody></table></div>
<h3>How the data was gathered</h3>
<p>Every relationship starts from what Nvidia was legally required to disclose: its annual and quarterly reports, current reports, holdings reports and ownership filings since January 2023. Then the same deal was traced in what the other company filed: its annual and quarterly reports, prospectuses, credit agreements and indentures, newest first. Company releases fill deals that never reached a filing. A sweep of every company's filings for Nvidia near words such as backstop, guarantee, warrant and lease found the rest.</p>
<p>{E(sm["note"])} The register holds {sum(sm["evidence_by_tier"].values()):,} citations: {sm["evidence_by_tier"].get("1", 0):,} primary and {sm["evidence_by_tier"].get("2", 0)} from news. {sm["one_sided_relationships"]} of {sm["relationships"]} relationships are disclosed by one side only.</p>
<h3>Source policy</h3>
<p>A figure is shown only if a primary source (a filing, the company's own release, a regulator, a court, a lien registry or a rating agency's public release) or two independent named publications (Bloomberg, Reuters, The Wall Street Journal, the Financial Times, The Information, CNBC, Barron's, The Economist, Nikkei Asia, Axios) contain it. Otherwise it reads "Not confirmed". Blogs, social posts, aggregators and sell-side notes are never used. Every quote was found word for word in a saved copy of its source, and every number sits in or beside that quote.</p>
<h3>Definitions</h3>
<dl class="pb">
<dt><dfn>Funded</dfn></dt><dd>Cash Nvidia has paid. On the page it counts the cost of shares still held: a stake partly sold counts only the part still reported.</dd>
<dt><dfn>Committed</dfn></dt><dd>A legally binding amount under a definitive agreement. Where no source says how much has been paid, it is counted once and never called unpaid.</dd>
<dt><dfn>Contingent maximum</dfn></dt><dd>The most Nvidia could be required to pay under a guarantee, backstop or similar promise, with the trigger stated. A guaranty that cannot yet be called is labeled not yet in force.</dd>
<dt><dfn>Headline</dfn></dt><dd>The largest figure announced, often "up to". Shown, never added to exposure.</dd>
<dt><dfn>Gross exposure</dfn></dt><dd>Funded plus committed plus contingent maximum, using confirmed amounts only. If any part is not disclosed it is a lower bound and reads "at least".</dd>
<dt><dfn>Capacity backstop</dfn></dt><dd>A promise to buy computing capacity that a cloud provider cannot sell to anyone else.</dd>
<dt><dfn>Residual value guarantee</dfn></dt><dd>A promise to cover the gap between an asset's guaranteed value and what it fetches when a lease ends or fails.</dd>
<dt><dfn>Wrong-way risk</dfn></dt><dd>Specific: Nvidia's exposure grows as the other company weakens. General: both move with AI demand. None: neither.</dd>
<dt><dfn>Both sides</dfn></dt><dd>Reconciled: both companies describe the deal the same way. Partly: they agree it exists but differ on terms. One side only: the other company has said nothing. Contradicted: they disagree on whether it exists or binds.</dd>
<dt><dfn>Exposure at default</dfn></dt><dd>Funded plus committed not yet paid plus the contingent maximum times a draw rate. The worst case draws everything; the base case is "not estimated" unless the draw is sourced. Loss is exposure less what Nvidia would receive or recover. <span class="analysis">Analysis</span></dd>
</dl>
<h3 id="method-significance">Significance score</h3>
<p>score = 40 x gross exposure percentile + 25 x contingent share of gross + 15 x circularity percentile + 10 x counterparty weakness + 10 x lender reliance. Each part runs from 0 to 1. A part that cannot be computed scores 0.5, so an opaque private company is not ranked as the safest. Weakness comes from the indicators shown in each credit read, never from a letter grade. <span class="analysis">Analysis</span></p>
<h3>Staying current</h3>
<p>Watchers check Nvidia's filings every two hours on weekdays, every counterparty's filings every four hours, holdings and ownership filings daily, and named publications twice a day. Anything new goes to a review queue; nothing reaches this page until a person approves it. An amount of $1 billion or more, or any letter of intent, is re-verified every 30 days; other definitive deals every 90 days; completed or ended deals every year. Past its limit an amount shows "Not re-verified since" its date.</p>
<h3>Not investment advice</h3>
<p>This page describes financial exposure from public sources. It does not recommend buying or selling any security. Figures can be wrong or out of date; every one links to its source so you can check it.</p>"""

    # ---------------------------------------------------------------- page
    def build(self):
        s, d = self.s, None
        for r in self.rels:
            r["to_cluster"] = self.ents.get(r["to"], {}).get("cluster", "other")
        d = self.data()
        disp = s["display"]
        lib = "".join(self.source_li(i, True) for i in self.ev)
        summary = "".join(f"<p>{E(x['text'])}</p>" for x in s["sentences"])
        first_note = ("<p class='lede'>These illustrate how losses would travel, not forecasts.</p>"
                      "<div class='scen' role='group' aria-label='Scenarios'><button class='btn' type='button' data-s='S1' aria-pressed='false'>Demand pause</button>"
                      "<button class='btn' type='button' data-s='S2' aria-pressed='false'>Lab funding gap</button><button class='btn' type='button' data-s='S3' aria-pressed='false'>Collateral repricing</button></div>"
                      "<div class='sliders' id='sliders'></div><div class='out' id='stress-out' aria-live='polite'><noscript>Scenario sliders need script. Results at default settings are in the research files.</noscript></div>"
                      "<p class='note'>Defaults are illustrative, not anchored to an observed move. Highlighted nodes on the map are the companies a scenario touches.</p>")
        views = [("constellation", "Map"), ("ledger-view", "Ledger"), ("timeline", "Timeline"), ("loops", "Loops"), ("stress", "Stress"),
                 ("others", "Who else guarantees"), ("verdict", "Central bank?"), ("changes", "What changed"), ("method", "Method")]
        nav = "".join(f'<li><a href="#{k}">{E(v)}</a></li>' for k, v in views)
        last = s.get("last_change") or s["data_as_of"]
        page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Is Nvidia the Central Bank of AI?</title>
<meta name="description" content="{E(disp.get('subtitle'))}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='10' fill='%231B1D26' stroke='%23F0B429' stroke-width='4'/%3E%3C/svg%3E">
<style>{CSS}</style><noscript><style>.ranked{{display:block}}.map-box,.legend button,#tl,.scen,.sliders{{display:none}}</style></noscript></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="site wrap"><a class="builtby" href="{E(disp.get('built_by_url'))}">Built By <strong>Resolute Business Development</strong></a>
<h1>{E(disp.get('site_title'))}</h1><p class="sub">{E(disp.get('subtitle'))}</p>
<div class="pills"><span class="pill">Data as of <b>{E(dl(s['data_as_of']))}</b></span><a class="pill" href="#changes">Last change <b>{E(dl(last[:10]))}</b></a></div></header>
<nav class="views" aria-label="Views"><div class="wrap"><ul>{nav}</ul></div></nav>
<main id="main" class="wrap">
<section class="summary" aria-label="Summary"><div class="lede">{summary}</div>{self.tiles()}</section>
<section class="view" id="constellation"><h2>The map</h2><div class="map-wrap"><div class="map-box"><svg id="map" role="group" aria-label="Radial map of Nvidia's relationships. Each node opens its detail."></svg><div class="tip" id="tip" role="status"></div></div>{self.legend()}</div>{self.ranked(d)}</section>
<section class="view" id="ledger-view"><h2>The Ledger</h2>{self.ledger()}</section>
<section class="view" id="timeline"><h2>Timeline</h2><p class="note">Each mark is a dated event. Drag across the track to filter the map and Ledger to that period, or use the dates. Click empty track to clear.</p>
<div class="controls"><label>From <input type="date" id="tl-from" min="2023-01-01"></label><label>To <input type="date" id="tl-to"></label><span class="note" id="tl-range" aria-live="polite"></span></div>
<svg id="tl" role="group" aria-label="Timeline of events by cluster"></svg></section>
<section class="view" id="loops"><h2>Circular flows</h2><p class="lede">Where Nvidia money goes out and comes back as demand for Nvidia systems. No loop has a disclosed dollar value on its return leg, so no circularity ratio can be computed.</p>{self.loops_html()}</section>
<section class="view" id="stress"><h2>Stress</h2>{first_note}</section>
<section class="view" id="others"><h2>Who else guarantees AI capacity</h2>{self.guarantees_html()}</section>
<section class="view" id="verdict"><h2>Is Nvidia a central bank?</h2>{self.central_bank_html()}</section>
<section class="view" id="changes-view"><h2 id="changes">What changed</h2>{self.changes_html()}</section>
<section class="view" id="method"><h2>Method and sources</h2>{self.method_html()}</section>
</main>
<aside id="panel" hidden aria-hidden="true" role="dialog" aria-modal="true" aria-label="Relationship detail"><button class="close" type="button" aria-label="Close detail">×</button><div id="panel-body"></div></aside>
<div id="sources-lib" hidden><ol id="sources">{lib}</ol></div>
<footer class="wrap"><p><a class="builtby" href="{E(disp.get('built_by_url'))}">Built By <strong>Resolute Business Development</strong></a></p>
<p>Not investment advice. This page describes exposure from public filings and company releases; it never recommends a trade. Data as of {E(dl(s['data_as_of']))}.</p></footer>
<script type="application/json" id="data">{json.dumps(d, separators=(",", ":")).replace("</", "<\\/")}</script>
<script>{JS}</script>
</body></html>"""
        SITE.mkdir(exist_ok=True)
        (SITE / "index.html").write_text(page, encoding="utf-8")
        return len(page.encode())


def main():
    n = Site().build()
    print(f"wrote site/index.html ({n / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
