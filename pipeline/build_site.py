"""Write site/index.html from data/published/ (spec/07, spec/08, spec/10 B3 to B6).

  python3 -m pipeline.build_site

Everything a reader needs is rendered into the HTML at build time: summary, tiles, Ledger rows, every relationship's
full detail, the verdict, What changed and Method. Script adds the map, filters, sorting, the slide-in panel,
the timeline brush, the stress sliders and shareable URLs. Nothing loads from other websites.
"""
from __future__ import annotations

import html
import json
import math
import re
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
ROLE = {"co_investor": "Co-investor", "lender": "Lender", "offtaker": "Offtaker", "landlord": "Landlord", "bondholder": "Bondholder", "utility": "Utility"}
CHANGE_LABEL = {"added": "Added", "amount_changed": "Amount changed", "status_changed": "Status changed", "reconciliation_changed": "Reconciliation changed",
                "dates_changed": "Dates changed", "evidence_added": "Source added", "market_value": "Market value", "link_repair": "Link repaired",
                "reverified": "Re-verified", "corrected": "Corrected", "removed_from_display": "Removed from display"}


ISO_DATE = re.compile(r"\b((?:19|20)\d\d)-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\b")
PAREN_EV = re.compile(r"\s*\((ev_\d+(?:(?:,| and| or|;)\s*ev_\d+)*)\)")
BARE_EV = re.compile(r"\bev_\d+(?:(?:,| and| or|;)\s*ev_\d+)*")
ANY_EV = re.compile(PAREN_EV.pattern + "|" + BARE_EV.pattern)
UNITS = ("trillion", "billion", "million", "thousand")


def money(v):
    return fmt.money(v)


def money_s(v):
    """Short form for table cells: $30.2B, $860.3M. The key sits under the Ledger."""
    return fmt.money_short(v)


def short_text(t):
    return (t or "").replace(" trillion", "T").replace(" billion", "B").replace(" million", "M").replace(" thousand", "K")


def money_u(v):
    """Tile figure with its unit in a smaller span."""
    t = money(v)
    head, _, unit = t.rpartition(" ")
    return f'{E(head)} <span class="u">{E(unit)}</span>' if unit in UNITS else E(t)


def dl(d):
    return fmt.date_long(d) if d else "Not disclosed"


def ds(d):
    """Short reader date for tables: 17 Aug 2026."""
    if not d:
        return ""
    parts = d.split("-")
    if len(parts) == 1:
        return parts[0]
    mon = fmt.MONTHS[int(parts[1]) - 1][:3]
    return f"{mon} {parts[0]}" if len(parts) == 2 else f"{int(parts[2])} {mon} {parts[0]}"


def chip(ids, label="Source", rid=None, what=None):
    ids = list(dict.fromkeys(i for i in (ids or []) if i))
    if not ids:
        return ""
    href = f"#srcs-{rid}" if rid else "#sources"
    n = f" ({len(ids)})" if len(ids) > 1 else ""
    aria = f"{len(ids)} source{'s' if len(ids) > 1 else ''}" + (f" for {what}" if what else "")
    return f'<a class="chip" role="button" href="{href}" data-ev="{E(" ".join(ids))}" aria-label="{E(aria)}">{E(label)}{n}</a>'


def mchip(measure, what, rels=None, ev=None, scope="all", label="Sources"):
    """A chip that opens the largest relationships behind a total, each with its source."""
    extra = (f' data-rels="{E(" ".join(rels))}"' if rels else "") + (f' data-ev2="{E(" ".join(ev))}"' if ev else "")
    return (f'<a class="chip" role="button" href="#ledger-view" data-measure="{E(measure)}" data-scope="{scope}"{extra} '
            f'aria-label="Sources for {E(what)}">{E(label)}</a>')


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

    def prose(self, s, rid=None):
        """Reader copy from register text: escaped, dates in words, evidence ids turned into source chips,
        internal identifiers replaced by names. Never used on quotes or source titles."""
        if s is None:
            return ""
        t = E(s)
        t = ISO_DATE.sub(lambda m: fmt.date_long(m.group(0)), t)
        def evchip(m):
            ids = [i for i in re.findall(r"ev_\d+", m.group(0)) if i in self.ev]
            return (" " + chip(ids, "Source", rid)) if ids else ""
        t = ANY_EV.sub(evchip, t)
        t = re.sub(r"\brel_[a-z0-9_]+\b", lambda m: E(self.relmap[m.group(0)]["title"]) if m.group(0) in self.relmap else "another record", t)
        t = re.sub(r"\bent_[a-z0-9_]+\b", lambda m: E(self.name(m.group(0))), t)
        t = re.sub(r"\s+under spec/\d+", "", t)
        t = re.sub(r"\bspec/\d+\b", "the method", t)
        return t

    # ---------------------------------------------------------------- sources
    def source_li(self, i, with_id=False):
        e = self.ev.get(i)
        if not e:
            return ""
        idattr = f' id="src-{E(i)}"' if with_id else ""
        tier = {"1": "Primary", "2": "News", "market": "Market data"}.get(str(e.get("tier")), "")
        acc = f", accession {E(e['accession'])}" if e.get("accession") else ""
        sec = (", " + ISO_DATE.sub(lambda m: fmt.date_long(m.group(0)), E(e["section"]))) if e.get("section") else ""
        link = e.get("source_link") or e.get("url")
        return (f'<li{idattr}><span class="tier">{tier}</span><span class="pubd">{E(e["publisher"])}, {E(dl(e.get("published")))}</span>{acc}{sec}. '
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
        c = chip(a.get("evidence"), "Source", rid, label.lower()) if a.get("value") or a.get("status") == "not_confirmed" else ""
        return (f'<div class="amt"><span class="k">{E(label)}</span><span class="{cls}">{E(txt)}</span>'
                f'<span class="d">{" ".join(x if x.startswith("<") else E(x) for x in extra)} {c}</span></div>')

    def panel(self, r):
        rid = r["id"]
        ent = self.ents.get(r["to"], {})
        am, x = r["amounts"], r["exposure"]
        T = lambda s: self.prose(s, rid)
        sig = (r.get("significance") or {}).get("score")
        badges = (f'<span class="badge t b-{E(r["type_primary"])}">{E(r["labels"]["type"])}</span> '
                  f'<span class="badge">{E(r["labels"]["status"])}</span> <span class="badge">{E(r["labels"]["basis"])}</span> '
                  f'<span class="badge">{E(r["labels"]["cluster"])}</span>')
        if r["credit"].get("wwr") == "specific":
            badges += ' <span class="badge wwr">Specific wrong-way risk</span>'
        amts = "".join([self.amount_cell("Funded", am.get("funded"), rid), self.amount_cell("Committed", am.get("committed_total"), rid),
                        self.amount_cell("Contingent maximum", am.get("contingent_max"), rid), self.amount_cell("Headline", am.get("headline"), rid)])
        extra_amts = ""
        for k, lab in (("market_value", "Market value"), ("carrying_value", "Carrying value"), ("annual_obligation", "Annual obligation")):
            a = am.get(k)
            if a and (a.get("value") or a.get("status") == "not_confirmed"):
                extra_amts += self.amount_cell(lab, a, rid)
        if extra_amts:
            extra_amts = f'<div class="amts extra">{extra_amts}</div>'
        floor = (am.get("funded") or {}).get("floor")
        floor_html = (f'<p class="note"><span class="analysis">Analysis</span> At least {E(money(floor["value"]))} paid by {E(dl(floor.get("as_of")))}: '
                      f'{T(floor["note"].replace("Analysis: ", ""))}</p>') if floor else ""
        d = r["dates"]
        lv = max([a.get("last_verified") or "" for a in am.values() if isinstance(a, dict)] or [""])
        low = lambda dd: dl(dd) if dd else "not disclosed"
        dparts = [f"Announced: {low(d.get('announced'))}"]
        if d.get("signed"):
            dparts.append(f"Signed: {dl(d['signed'])}")
        cmax = am.get("contingent_max") or {}
        if cmax.get("in_force") is False:
            dparts.append("Not yet in force" + (f": {fmt.date_long(d['effective'])}" if d.get("effective") and d["effective"] > (d.get("signed") or "") else ""))
        elif d.get("effective"):
            dparts.append(f"Effective: {dl(d['effective'])}")
        dparts += [f"Matures: {low(d.get('maturity'))}", f"Last verified: {dl(lv) if lv else 'not recorded'}"]
        dates = '<p class="dates">' + " · ".join(E(x) for x in dparts) + "</p>"
        sigbar = ""
        if sig is not None:
            sigbar = (f'<div class="sig"><span>Significance</span><span class="bar" aria-hidden="true"><i style="width:{min(100, sig):.0f}%"></i></span>'
                      f'<span>{sig:.0f} of 100</span> <a href="#method-significance">why</a> <span class="analysis">Analysis</span></div>')

        sec = []
        sec.append(("what", "What the deal is", f"<p>{T(r['definition'])}</p>" + (f"<p>{T(r['inclusion_reason'])}</p>" if r.get("inclusion_reason") else "")
                    + (f'<p class="note">Seniority: {E(SENIORITY.get(r.get("seniority"), r.get("seniority")))}</p>')))
        rc = r["reconciliation"]
        diffs = "".join(f"<li><b>{T((df.get('field') or '').replace('amounts.', '').replace('_', ' ').replace('.', ' '))}</b>: Nvidia side {T(df.get('nvidia_value'))}; counterparty side {T(df.get('counterparty_value'))} {chip(df.get('evidence'), 'Source', rid)}</li>"
                        for df in rc.get("differences") or [])
        sec.append(("sides", "Both sides", f"<p><b>Result:</b> {E(RECON.get(rc['result'], rc['result']))}</p>"
                    f"<p><b>What Nvidia disclosed.</b> {T(rc.get('nvidia_side'))} {chip(rc.get('nvidia_evidence'), 'Source', rid)}</p>"
                    f"<p><b>What {E(self.name(r['to']))} disclosed.</b> {T(rc.get('counterparty_side'))} {chip(rc.get('counterparty_evidence'), 'Source', rid)}</p>"
                    + (f"<ul>{diffs}</ul>" if diffs else "")))
        projs = [self.projects[p] for p in r.get("projects") or [] if p in self.projects]
        projs += [p for p in self.projects.values() if rid in (p.get("nvidia_link") or []) and p not in projs]
        if projs:
            rows = ""
            for p in projs:
                fin = "; ".join(f"{T(f.get('facility'))}" + (f" ({E(', '.join(self.name(x) for x in f.get('lenders') or []))})" if f.get("lenders") else "") +
                                (f": {E(fmt.amount_text(f.get('balance')))}" if f.get("balance") else "") for f in p.get("financing") or [])
                mw = (p.get("power_mw_contracted") or {}).get("value")
                rows += (f"<tr><td>{E(p['name'])} {chip(p.get('evidence'), 'Source', rid)}</td><td>{E(p.get('location'))}</td><td class='num'>{E(f'{mw:,.0f} MW' if mw else '')}</td>"
                         f"<td>{E(p.get('anchor_tenant') or '')}</td><td>{fin}</td><td>{E('Covered' if p.get('role') == 'covered' else 'Context')}</td></tr>")
            sec.append(("projects", "Project basis", f"<div class='tbl-wrap'><table class='stack'><thead><tr><th scope='col'>Site</th><th scope='col'>Location</th><th scope='col' class='num'>Contracted</th><th scope='col'>Anchor tenant</th><th scope='col'>Financing</th><th scope='col'>Role</th></tr></thead><tbody>{rows}</tbody></table></div>"))
        c = ent.get("credit") or {}
        credit = [f"<dt>Wrong-way risk</dt><dd>{E(WWR_LABEL.get(r['credit'].get('wwr'), ''))}. {T(r['credit'].get('wwr_reason'))}</dd>"]
        if r["credit"].get("collateral"):
            credit.append(f"<dt>Collateral</dt><dd>{T(r['credit']['collateral'])}</dd>")
        if r["credit"].get("tenor"):
            credit.append(f"<dt>Tenor</dt><dd>{T(r['credit']['tenor'])}</dd>")
        for k, lab in (("debt_outstanding", "Debt outstanding"), ("maturities_24m", "Debt due within 24 months"), ("cash_and_undrawn", "Cash and undrawn facilities"),
                       ("committed_spend_12m", "Committed spending, next 12 months")):
            a = c.get(k)
            if a and a.get("text"):
                credit.append(f"<dt>{lab}</dt><dd>{E(a['text'])}{' (at least)' if a.get('lower_bound') else ''}, {E(dl(a.get('as_of')))} {chip(a.get('evidence'), 'Source', rid, lab.lower())}</dd>")
        lm = (c.get("liquidity_months") or {}).get("value")
        if lm is not None:
            credit.append(f"<dt>Liquidity</dt><dd>{lm:.1f} months of committed spending <span class='analysis'>Analysis</span></dd>")
        for k, lab in (("top_customer_share", "Largest customer"), ("top3_customer_share", "Top three customers")):
            a = c.get(k)
            if a and a.get("value") is not None:
                credit.append(f"<dt>{lab}</dt><dd>{a['value'] * 100:.0f}% of revenue, {E(dl(a.get('as_of')))} {chip(a.get('evidence'), 'Source', rid, lab.lower())}</dd>")
        for pr in c.get("public_ratings") or []:
            credit.append(f"<dt>Rating</dt><dd>{E(pr.get('agency'))} {E(pr.get('rating'))}, {E(dl(pr.get('date')))} {chip(pr.get('evidence'), 'Source', rid, 'rating')}</dd>")
        if c.get("collateral_note"):
            credit.append(f"<dt>GPU collateral</dt><dd>{T(c['collateral_note'])}</dd>")
        if self.show_grades and c.get("grade"):
            credit.append(f"<dt>Grade</dt><dd>{E(c['grade'])}. {T(c.get('grade_reason'))} <span class='analysis'>Analysis</span></dd>")
        sec.append(("credit", "Credit read", f"<dl>{''.join(credit)}</dl>"))
        dv = r.get("derived") or {}
        gross_ids = [i for k in ("funded", "committed_total", "contingent_max") for i in ((am.get(k) or {}).get("evidence") or [])]
        meas = [f"<dt>Gross exposure</dt><dd>{E(('at least ' if x['lower_bound'] else '') + money(x['gross']) if x['gross'] else 'Not sized')}"
                f"{(' (missing: ' + E(', '.join(m.replace('_', ' ') for m in x['missing'])) + ')') if x['missing'] else ''} {chip(gross_ids if x['gross'] else [], 'Source', rid, 'gross exposure')}</dd>"]
        if dv.get("ead_max") is not None:
            meas.append(f"<dt>Exposure at default, worst case</dt><dd>{E(money(dv['ead_max']))}; loss up to {E(money(dv.get('loss_max')))}. {T(dv.get('loss_max_note', ''))} {chip(gross_ids, 'Source', rid, 'exposure at default')}</dd>")
        meas.append(f"<dt>Base case</dt><dd>{E(money(dv['ead_base']) if dv.get('ead_base') is not None else 'Not estimated')}. {T(dv.get('loss_base_note', ''))}</dd>")
        for k, lab in (("circularity_ratio", "Circularity ratio"), ("share_of_counterparty_capital", "Share of counterparty's equity raised"),
                       ("share_of_nvda_equity", "Share of Nvidia's equity"), ("share_of_nvda_fcf", "Share of Nvidia's free cash flow"), ("backstop_coverage", "Backstop coverage")):
            v = (dv.get(k) or {}).get("value")
            meas.append(f"<dt>{lab}</dt><dd>{E(fmt.pct(v, 2) if v is not None else 'Not computable: inputs not sourced')}</dd>")
        sec.append(("measures", "Exposure and derived measures", f"<p><span class='analysis'>Analysis</span> Formulas are on the Method view.</p><dl>{''.join(meas)}</dl>"))
        fo = r["consequences"].get("first_order") or []
        so = r["consequences"].get("second_order") or []
        if fo:
            sec.append(("first", "First order consequences", "<p><span class='analysis'>Analysis</span></p><ul class='cons'>" +
                        "".join(f"<li>{T(cq['text'])} {chip(cq.get('evidence'), 'Source', rid)}</li>" for cq in fo) + "</ul>"))
        if so:
            sec.append(("second", "Second order consequences", "<p><span class='analysis'>Analysis</span></p><ul class='cons'>" +
                        "".join(f"<li><span class='lens'>{E(LENS.get(cq.get('lens'), ''))}</span>{T(cq['text'])} {chip(cq.get('evidence'), 'Source', rid)}</li>" for cq in so) + "</ul>"))
        d2 = r.get("depth2_links") or []
        if d2:
            sec.append(("parties", "Lenders, co-investors and offtakers", "<ul class='cons'>" + "".join(
                f"<li><span class='lens'>{E(ROLE.get(l2.get('role'), l2.get('role') or ''))}</span><b>{E(self.name(l2['entity']))}</b>: {T(l2.get('description'))} "
                f"{chip(l2.get('evidence'), 'Source', rid)}</li>" for l2 in d2) + "</ul>"))
        evs = sorted(self.events_by_rel.get(rid, []), key=lambda e: e["date"])
        if evs:
            sec.append(("timeline", "Timeline", "<ul class='cons'>" + "".join(f"<li><b>{E(dl(ev['date']))}</b>: {T(ev['summary'])} {chip(ev.get('evidence'), 'Source', rid)}</li>" for ev in evs) + "</ul>"))
        srcs = "".join(self.source_li(i) for i in dict.fromkeys(r["evidence"] + self.amount_ids(r)))
        sec.append(("sources", "Sources", f"<ol class='srcs' id='srcs-{E(rid)}'>{srcs}</ol>"))
        body = "".join(f"<details data-sec='{k}'><summary>{E(t)}</summary>{h}</details>" for k, t, h in sec)
        return (f'<div class="pb" id="p-{E(rid)}"><button type="button" class="btn xall" data-mode="expand">Expand all</button>'
                f'<h4 class="cp">{E(self.ents.get(r["to"], {}).get("name") or self.name(r["to"]))}</h4><div class="meta">{badges}</div>'
                f'<p class="note">{E(r["title"])}</p><p class="insight">{E(r["insight"])} <span class="analysis">Analysis</span></p>'
                f'<div class="amts">{amts}</div>{extra_amts}{floor_html}{dates}{sigbar}{body}</div>')

    def amount_ids(self, r):
        out = []
        for a in r["amounts"].values():
            if isinstance(a, dict):
                out += a.get("evidence") or []
        return out

    # ---------------------------------------------------------------- ledger
    def num_link(self, text, ids, rid, what):
        ids = list(dict.fromkeys(i for i in ids or [] if i))
        if not ids:
            return E(text)
        return (f'<a class="ns" role="button" href="#srcs-{E(rid)}" data-ev="{E(" ".join(ids))}" '
                f'aria-label="{E(text)}, {E(what)}: {len(ids)} source{"s" if len(ids) > 1 else ""}">{E(text)}</a>')

    def ledger_row(self, r, ncols):
        x, am, rid = r["exposure"], r["amounts"], r["id"]
        ent = self.ents.get(r["to"], {})
        evs = lambda k: (am.get(k) or {}).get("evidence") or []

        def cell(v, key, what, missing=False):
            if v:
                return f'<td class="num">{self.num_link(money_s(v), evs(key), rid, what)}</td>'
            if missing:
                return '<td class="num"><span class="nc nd">Not disclosed</span></td>'
            if (am.get(key) or {}).get("not_applicable"):
                return '<td class="num"><span class="nc">Not applicable</span></td>'
            return '<td class="num"><span class="nc">None</span></td>'
        committed = (x["committed_unfunded"] or 0) + (x["committed_split_unknown"] or 0)
        h = (am.get("headline") or {})
        lv = max([a.get("last_verified") or "" for a in am.values() if isinstance(a, dict)] or [""])
        sig = (r.get("significance") or {}).get("score")
        term = r["status"] == "terminated"
        cls = "row" + (" terminated" if term else "")
        nm = self.name(r["to"])
        attrs = (f'data-id="{E(rid)}" data-cp="{E(nm)}" data-gross="{x["gross"] or 0}" data-funded="{x["funded"] or 0}" '
                 f'data-committed="{committed}" data-cont="{x["contingent_max"] or 0}" data-headline="{h.get("value") or 0}" '
                 f'data-ann="{E(r["dates"].get("announced") or "")}" data-lv="{E(lv)}" data-sig="{sig or 0}" data-cl="{E(r["labels"]["cluster"])}" '
                 f'data-type="{E(r["labels"]["type"])}" data-st="{E(r["labels"]["status"])}" data-rc="{E(RECON.get(r["reconciliation"]["result"]))}"')
        grade = f"<td>{E((ent.get('credit') or {}).get('grade') or '')}</td>" if self.show_grades else ""
        gross_ids = evs("funded") + evs("committed_total") + evs("contingent_max")
        gross = (('<span class="lb">at least</span> ' if x["lower_bound"] else "") + self.num_link(money_s(x["gross"]), gross_ids, rid, "gross exposure")) if x["gross"] else '<span class="nc">Not sized</span>'
        htxt = short_text(h.get("text") or "")
        hcell = self.num_link(htxt, h.get("evidence"), rid, "headline") if h.get("value") else f'<span class="nc">{E(htxt)}</span>'
        status = f'<span class="badge ended">{E(r["labels"]["status"])}</span>' if term else E(r["labels"]["status"])
        row = (f'<tr class="{cls}" id="row-{E(rid)}" {attrs}><th scope="row"><button type="button" class="rowbtn" aria-label="Open detail for {E(nm)}: {E(r["title"])}">{E(nm)}</button>'
               f'<button type="button" class="disc" hidden aria-expanded="false" aria-controls="det-{E(rid)}" aria-label="Show full detail for {E(nm)} in the table">▸</button>'
               f'<span class="note rt">{E(r["title"])}</span></th>'
               f'<td>{E(r["labels"]["cluster"])}</td><td><span class="badge t b-{E(r["type_primary"])}">{E(r["labels"]["type"])}</span></td><td>{status}</td>'
               f'{cell(x["funded"], "funded", "funded", "funded" in x["missing"])}{cell(committed, "committed_total", "committed")}'
               f'{cell(x["contingent_max"], "contingent_max", "contingent maximum", "contingent_max" in x["missing"])}'
               f'<td class="num">{gross}</td><td class="num">{hcell}</td><td class="dt">{E(ds(r["dates"].get("announced")))}</td><td class="dt">{E(ds(lv))}</td>'
               f'<td>{E(RECON.get(r["reconciliation"]["result"]))}</td><td class="num">{"" if sig is None else f"{sig:.0f}"}</td>{grade}</tr>')
        det = f'<tr class="detail" id="det-{E(rid)}"><td colspan="{ncols}"><details><summary>Full detail for {E(nm)}</summary>{self.panel(r)}</details></td></tr>'
        return row + det

    def ledger(self):
        cols = ["Counterparty", "Cluster", "Type", "Status", "Funded", "Committed", "Contingent max", "Gross", "Headline", "Announced", "Verified", "Both sides", "Score"]
        keys = ["cp", "cl", "type", "st", "funded", "committed", "cont", "gross", "headline", "ann", "lv", "rc", "sig"]
        tips = {"Funded": "Funded and still held: cost of stakes Nvidia still holds", "Committed": "Binding amounts, counted once", "Contingent max": "Contingent maximum: the most Nvidia could be made to pay",
                "Gross": "Gross exposure: funded plus committed plus contingent maximum", "Headline": "Announced figure, never added", "Verified": "Last verified", "Both sides": "Whether both companies describe the deal the same way",
                "Score": "Significance score, 0 to 100"}
        if self.show_grades:
            cols.append("Grade"); keys.append("")
        num = {"funded", "committed", "cont", "gross", "headline", "sig"}
        th = "".join((f'<th scope="col" data-sort="{k}" class="{"num" if k in num else ""}"><button type="button"{(" title=" + chr(34) + E(tips[c]) + chr(34)) if c in tips else ""}>{E(c)}</button><span class="pth">{E(c)}</span></th>' if k else f'<th scope="col">{E(c)}</th>') for c, k in zip(cols, keys))
        core = [r for r in self.rels if not r.get("aggregate_of") and r["type_primary"] != "CX"]
        core.sort(key=lambda r: -(r["exposure"]["gross"] or 0))
        body = "".join(self.ledger_row(r, len(cols)) for r in core)
        t = self.s["totals"]
        tl = lambda k, v, what: f'<td class="num" data-k="{k}"><a class="ns" role="button" href="#ledger-view" data-measure="{what[0]}" data-scope="filtered" aria-label="{E(money(v))}, total {E(what[1])}: sources">{E(money_s(v))}</a></td>'
        foot = (f'<tfoot><tr><th scope="row" data-k="n">{t["count"]} relationships</th><td colspan="3">Totals, confirmed amounts only</td>'
                + tl("funded", t["funded"], ("funded", "funded")) + tl("cu", t["committed_unfunded"] + t["committed_split_unknown"], ("committed", "committed"))
                + tl("cont", t["contingent_max"], ("contingent", "contingent maximum")) + tl("gross", t["gross"], ("gross", "gross exposure"))
                + tl("h", t["headline"], ("headline", "headline")) + f'<td colspan="{len(cols) - 9}"></td></tr></tfoot>')
        opts = lambda name, pairs: f'<label>{name} <select name="{name.lower().replace(" ", "")}"><option value="">All</option>' + "".join(f'<option value="{E(v)}">{E(l)}</option>' for v, l in pairs) + "</select></label>"
        clusters = sorted({(r["to_cluster"], r["labels"]["cluster"]) for r in core}, key=lambda p: p[1])
        filters = ('<div class="controls" id="ledger-filters">'
                   + opts("Cluster", clusters)
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
                amt = self.num_link(a["text"], a.get("evidence"), r["id"], "amount") if a else "Not computable"
                b += (f'<tr class="row" data-id="{E(r["id"])}"><th scope="row"><button type="button" class="rowbtn" aria-label="Open detail for {E(r["title"])}">{E(r["title"])}</button>'
                      f'<span class="note rt">{E(r["insight"])}</span></th><td class="num">{amt}</td>'
                      f'<td>{chip(a.get("evidence") if a else r["evidence"], "Source", r["id"], r["title"])}</td></tr>'
                      f'<tr class="detail"><td colspan="3"><details><summary>Full detail</summary>{self.panel(r)}</details></td></tr>')
            return (f'<h3>{E(title)}</h3><p class="note">{E(note)}</p><div class="tbl-wrap"><table class="sub" aria-label="{E(title)}: record, amount, sources"><tbody>{b}</tbody></table></div>')
        return (filters + '<p class="note" id="filtered-note" role="status" hidden>Filters are on. Tiles, the map and the totals row show the filtered set.</p>'
                '<p class="sr" id="ledger-status" role="status"></p>'
                f'<div class="tbl-wrap ledger-wrap" id="ledger-wrap" tabindex="-1"><table id="ledger"><caption class="sr">Every relationship, sortable. Each amount opens its sources.</caption>'
                f'<thead><tr>{th}</tr></thead><tbody>{body}</tbody>{foot}</table></div>'
                '<p class="note scroll-hint" id="scroll-hint" hidden>More columns to the right: scroll the table sideways.</p>'
                '<p class="note">B is billion, M is million. Funded counts the cost of shares still held. Committed includes amounts whose paid portion is not disclosed; they are counted once and never called unpaid. '
                'Headline is what was announced and is never added. Each amount opens its sources. <span class="noprint">Select a counterparty or click a row for the full detail.</span></p>'
                + sub(other, "Unattributed remainders of Nvidia's own totals", "What Nvidia reports in total, less what this register can name and size. Upper bounds where named stakes have no stated amount. Excluded from every total above. Label: analysis.")
                + sub(cx, "Context records", "Parties that matter to the analysis but where no Nvidia capital is involved. Excluded from every total."))

    # ---------------------------------------------------------------- data for script
    def data(self):
        rels = []
        for r in self.rels:
            x, am = r["exposure"], r["amounts"]
            h = am.get("headline") or {}
            lv = max([a.get("last_verified") or "" for a in am.values() if isinstance(a, dict)] or [""])
            ev0 = (r["evidence"] or [None])[0]
            evs = lambda k: [i for i in ((am.get(k) or {}).get("evidence") or []) if i in self.ev]
            rels.append({"id": r["id"], "to": r["to"], "ti": r["title"], "t": r["type_primary"], "tl": r["labels"]["type"], "s": r["status"], "sl": r["labels"]["status"],
                         "b": r["claim_basis"], "bl": r["labels"]["basis"], "cl": r["to_cluster"], "cll": r["labels"]["cluster"], "w": r["credit"].get("wwr"),
                         "d": r["dates"].get("announced"), "lv": lv, "rc": r["reconciliation"]["result"], "sig": (r.get("significance") or {}).get("score"),
                         "agg": bool(r.get("aggregate_of")), "lb": bool(x["lower_bound"]), "h": h.get("value") if h.get("value") and not h.get("not_applicable") else 0,
                         "x": {"funded": x["funded"] or 0, "cu": x["committed_unfunded"] or 0, "csu": x["committed_split_unknown"] or 0, "cont": x["contingent_max"] or 0, "gross": x["gross"] or 0},
                         "e": {"f": evs("funded"), "c": evs("committed_total"), "k": evs("contingent_max"), "h": evs("headline"), "mv": evs("market_value"), "cv": evs("carrying_value"),
                               "a": [i for i in r["evidence"] if i in self.ev][:4]},
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
            sat = {}
            for r in n["rels"]:
                for l2 in r.get("depth2_links") or []:
                    if l2["entity"] != n["id"]:
                        sat.setdefault(l2["entity"], {"n": self.name(l2["entity"]), "r": ROLE.get(l2.get("role"), l2.get("role") or "").lower()})
            out_nodes.append({"id": n["id"], "name": n["name"], "ring": n["ring"], "gross": n["gross"], "headline": n["headline"], "type": top["type_primary"],
                              "typeLabel": ", ".join(sorted({TYPE_NAMES[r["type_primary"]] for r in n["rels"]})), "rel": top["id"], "wwr": n["wwr"], "lb": n["lb"],
                              "date": ("First announced " + dl(n["date"])) if n["date"] else None, "sat": list(sat.values())})
        out_nodes.sort(key=lambda n: (n["ring"], -n["gross"]))
        loop_ents = [[l2["from"] for l2 in lp["legs"]] + [lp["legs"][-1]["to"]] for lp in self.loops if lp.get("legs")]
        lanes = [{"key": k, "label": lab} for k, lab in RINGS]
        evs = []
        for ev in sorted(self.events, key=lambda e: e["date"]):
            r = self.relmap.get(ev["relationship"])
            if not r:
                continue
            lane = RINGS[RING_OF.get(r["to_cluster"], 6)][0]
            evs.append({"date": ev["date"], "rel": ev["relationship"], "kind": ev["kind"], "summary": ev["summary"], "lane": lane})
        fin = self.s.get("financials", {})
        sc = {k: v for k, v in self.scen.items() if k in ("S1", "S2", "S3", "config")}
        sc["config"] = {k: v for k, v in sc["config"].items() if not k.startswith("_")}
        proj_ev = {f["project"]: [i for i in (self.projects.get(f["project"], {}).get("evidence") or []) if i in self.ev] for f in (sc.get("S3") or {}).get("facilities", [])}
        return {"rels": rels, "ents": {k: {"n": v.get("short_name"), "g": (v.get("credit") or {}).get("grade") if self.show_grades else None} for k, v in self.ents.items()},
                "relEnt": {r["id"]: r["to"] for r in self.rels}, "nodes": out_nodes, "rings": [{"key": k, "label": l} for k, l in RINGS],
                "loopEnts": loop_ents, "lanes": lanes, "events": evs, "tlStart": "2023-01-01", "tlEnd": self.s["data_as_of"], "scen": sc, "projEv": proj_ev,
                "fin": {"equity": (fin.get("shareholders_equity") or {}).get("value"), "fcf": (fin.get("fcf_ttm") or {}).get("value"),
                        "equityEv": (fin.get("shareholders_equity") or {}).get("evidence") or [], "fcfEv": (fin.get("fcf_ttm") or {}).get("evidence") or []},
                "count": self.s["totals"]["count"], "showGrades": self.show_grades}

    # ---------------------------------------------------------------- page sections
    def sentence(self, x):
        """A summary sentence with a source chip after each figure."""
        text, out, pos = x["text"], "", 0
        for f in x.get("figures", []):
            t = f.get("text")
            i = text.find(t, pos) if t else -1
            if i < 0:
                continue
            if f.get("measure"):
                c = mchip(f["measure"], t, rels=f.get("rels"), ev=f.get("evidence"))
            else:
                c = chip([i2 for i2 in f.get("evidence") or [] if i2 in self.ev], "Source", None, t)
            out += E(text[pos:i + len(t)]) + ((" " + c) if c else "")
            pos = i + len(t)
        return f"<p>{out}{E(text[pos:])}</p>"

    def summary(self):
        ps = [self.sentence(x) for x in self.s["sentences"]]
        more = f'<details class="more" open><summary>More of the summary</summary>{"".join(ps[2:])}</details>' if len(ps) > 2 else ""
        return f'<div class="lede">{"".join(ps[:2])}{more}</div>'

    def tiles(self):
        t = self.s["totals"]
        c = t["counts"]
        committed = t["committed_unfunded"] + t["committed_split_unknown"]
        lb = t["lower_bound_count"]
        tl = [("funded", "Funded and still held", t["funded"], c["funded"], "Cost of stakes Nvidia still holds, where a source states the cost."),
              ("committed", "Committed", committed, c["committed_unfunded"] + c["committed_split_unknown"],
               f"Binding amounts. {money(t['committed_unfunded'])} is confirmed unpaid; for {money(t['committed_split_unknown'])} the paid portion is not disclosed."),
              ("contingent", "Contingent maximum", t["contingent_max"], c["contingent_max"],
               f"The most Nvidia could be made to pay. {money(t['contingent_not_in_force'])} of it is signed but not yet in force."),
              ("headline", "Headline announced, never added", t["headline"], c["headline"],
               f"{money(t['headline_groups']['not_binding'])} of it is letters of intent or has no disclosed agreement.")]
        out = '<div class="tiles" role="group" aria-label="Exposure totals. Each filters the map and Ledger.">'
        for k, lab, v, n, note in tl:
            out += (f'<div class="tilew{" apart" if k == "headline" else ""}"><button type="button" class="tile" data-k="{k}" aria-pressed="false"><span class="k">{E(lab)}</span>'
                    f'<span class="v">{money_u(v)}</span><span class="n cnt">{n} relationship{"" if n == 1 else "s"}</span></button>'
                    f'<p class="tn"><span class="tnote">{E(note)}</span> {mchip(k, lab.lower(), scope="filtered")}</p></div>')
        out += "</div>"
        out += (f'<p class="note" id="tile-note"><span id="tile-note-text" role="status">Funded, committed and contingent add up to gross exposure of at least {E(money(t["gross"]))}. It is a lower bound: '
                f'{lb} of {t["count"]} relationships have a part that is not disclosed. No filter is on.</span> {mchip("gross", "gross exposure", scope="filtered")} '
                f'<span class="noprint">Select a tile to filter the map and the Ledger.</span> '
                f'<button type="button" class="btn" id="clear-filters-2" hidden>Clear filters</button></p>')
        return out

    def ranked(self, d):
        by = defaultdict(list)
        for n in d["nodes"]:
            by[n["ring"]].append(n)
        out = ('<div class="ranked" id="ranked"><p class="note">This list is the map in text, largest first within each group. '
               '<button type="button" class="btn full-map-btn" id="full-map">Open the radial map</button></p>')
        for i, (k, lab) in enumerate(RINGS):
            if not by.get(i):
                continue
            out += f'<div class="rgroup"><h3>{E(lab)}</h3><ol>' + "".join(
                f'<li data-ent="{E(n["id"])}"><a href="#row-{E(n["rel"])}" data-open="{E(n["rel"])}"><b>{E(n["name"])}</b>: {E(n["typeLabel"])}; '
                f'{E((("at least " if n["lb"] else "") + money(n["gross"])) if n["gross"] else "not sized")}</a></li>' for n in sorted(by[i], key=lambda n: -n["gross"])) + "</ol></div>"
        return out + "</div>"

    def legend(self):
        sw = lambda inner, h=12: f'<svg width="38" height="{h}" viewBox="0 0 38 {h}" aria-hidden="true">{inner}</svg>'
        ln = lambda c, d="", w=3: f'<line x1="1" y1="6" x2="37" y2="6" stroke="{c}" stroke-width="{w}" stroke-dasharray="{d}"/>'
        rows = [(sw(ln("var(--cobalt)")), "Equity: solid line"),
                (sw(ln("#6F8BC8", w=5) + '<line x1="1" y1="6" x2="37" y2="6" stroke="#fff" stroke-width="2"/>'), "Conditional equity: hollow line"),
                (sw(ln("var(--cochineal)", "6 4")), "Backstop or guarantee: dashed"),
                (sw(ln("var(--cochineal)", "8 3 2 3")), "Residual value support: dash and dot"),
                (sw('<line x1="2" y1="6" x2="37" y2="6" stroke="var(--rosa)" stroke-width="3" stroke-dasharray="0.1 5" stroke-linecap="round"/>'), "Capacity rental: dotted"),
                (sw(ln("var(--cobalt-deep)").replace('x2="37"', 'x2="30"') + '<path d="M38,6 l-9,-5 v10 z" fill="var(--cobalt-deep)"/>'), "Financing: line with arrowhead"),
                (sw('<line x1="1" y1="4" x2="37" y2="4" stroke="var(--ochre)" stroke-width="1.6"/><line x1="1" y1="8.5" x2="37" y2="8.5" stroke="var(--ochre)" stroke-width="1.6"/>'), "Supply prepayment: double line"),
                (sw(ln("#4F6DB0", w=2) + '<line x1="5" y1="6" x2="37" y2="6" stroke="#4F6DB0" stroke-width="9" stroke-dasharray="1.6 8"/>'), "Fund commitment: line with cross ticks"),
                (sw(ln("var(--leaf)", w=1.5)), "License: thin line"),
                (sw(ln("var(--ink-3)", w=1)), "Context: hairline"),
                (sw('<line x1="1" y1="6" x2="37" y2="6" stroke="var(--cobalt)" stroke-width="11" opacity=".18"/>'), "Wide faint band: headline beyond what is binding"),
                (sw('<circle cx="14" cy="8" r="5" fill="#fff" stroke="var(--ink-2)" stroke-width="1.5"/><path d="M17,5 l7,-5 l1,9 z" fill="var(--cochineal)"/>', 14), "Notch: specific wrong-way risk"),
                (sw('<line x1="6" y1="7" x2="26" y2="7" stroke="var(--ink-2)" stroke-width="1"/><circle cx="29" cy="7" r="3.5" fill="#fff" stroke="var(--ink-2)" stroke-width="1.2"/>', 14), "Small satellite: a lender, co-investor or offtaker")]
        li = "".join(f"<li>{svg}<span>{E(t)}</span></li>" for svg, t in rows)
        li += ('<li id="legend-stress" hidden>' + sw('<circle cx="19" cy="7" r="5" fill="#fff" stroke="var(--cochineal)" stroke-width="3"/>', 14)
               + '<span>Red ring: touched by the selected stress scenario <button type="button" class="btn sm" id="clear-hit">Clear highlight</button></span></li>')
        return (f'<div class="legend"><p><b>How to read it.</b> Nvidia sits at the center. Each ring is a kind of counterparty. Node and line size show gross exposure. '
                f'Line style and color show the kind of deal. A node with several deals shows its largest; the hover lists all.</p><ul>{li}</ul>'
                '<p class="note">Satellites appear when you point at, focus or open a node. Every lender, co-investor and offtaker is also listed in that node\'s panel.</p>'
                '<p><button type="button" class="btn" id="show-loops" aria-pressed="false">Show circular flows</button> '
                '<button type="button" class="btn" id="view-list" aria-pressed="false" aria-controls="ranked">View as list</button></p>'
                '<p class="note">Keyboard: Tab to the map, arrow keys move around a ring or between rings, Enter opens the node.</p></div>')

    def loop_svg(self, lp):
        """Small flow diagram: Nvidia on the left, the other parties in a column, one numbered arrow per leg.
        Out and back between the same pair run as paired arrows. The numbered list below is the text equivalent."""
        ents = ["ent_nvidia"] + [e for e in dict.fromkeys(x for l2 in lp["legs"] for x in (l2["from"], l2["to"])) if e != "ent_nvidia"]
        others = ents[1:]
        gap = 46
        H = max(96, gap * (len(others) - 1) + 56)
        pos = {"ent_nvidia": (58, H / 2)}
        for i, e in enumerate(others):
            pos[e] = (250, 28 + i * gap if len(others) > 1 else H / 2)
        out = [f'<svg class="loopsvg" viewBox="0 0 360 {H:.0f}" role="img" aria-label="Flow diagram for this loop. The numbered legs below say the same in text.">']
        seen = defaultdict(int)
        for i, l2 in enumerate(lp["legs"], 1):
            a, b = l2["from"], l2["to"]
            if a not in pos or b not in pos:
                continue
            col = "var(--cobalt)" if a == "ent_nvidia" else ("var(--rosa)" if l2["kind"] in ("rent", "lease") else "var(--ochre)" if b == "ent_nvidia" else "var(--ink-2)")
            (x1, y1), (x2, y2) = pos[a], pos[b]
            key = tuple(sorted((a, b)))
            k = seen[key]
            seen[key] += 1
            if "ent_nvidia" in (a, b):
                off = (k - (sum(1 for q in lp["legs"] if tuple(sorted((q["from"], q["to"]))) == key) - 1) / 2) * 11
                sx, ex = (x1 + 44, x2 - 52) if a == "ent_nvidia" else (x1 - 52, x2 + 44)
                sy, ey = y1 + off * 0.5, y2 + off
                if a != "ent_nvidia":
                    sy, ey = y1 + off, y2 + off * 0.5
                d = f"M{sx:.1f},{sy:.1f} L{ex:.1f},{ey:.1f}"
                ang = math.atan2(ey - sy, ex - sx)
                mx, my = sx + (ex - sx) * (0.38 + 0.12 * (k % 3)), sy + (ey - sy) * (0.38 + 0.12 * (k % 3))
            else:
                bulge = 300 + 18 * k
                sx, ex = x1 + 52, x2 + 52
                d = f"M{sx:.1f},{y1:.1f} Q{bulge + 30},{(y1 + y2) / 2:.1f} {ex + 5:.1f},{y2:.1f}"
                ang = math.atan2(y2 - (y1 + y2) / 2, ex + 5 - (bulge + 30))
                mx, my, ey = (sx + ex + 5) / 4 + (bulge + 30) / 2, (y1 + y2) / 2, y2
                ex = ex + 5
            hx, hy = ex, ey
            p1 = (hx - 8 * math.cos(ang - 0.45), hy - 8 * math.sin(ang - 0.45))
            p2 = (hx - 8 * math.cos(ang + 0.45), hy - 8 * math.sin(ang + 0.45))
            out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.6"/><path d="M{hx:.1f},{hy:.1f} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} z" fill="{col}"/>'
                       f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="8" fill="#fff" stroke="{col}" stroke-width="1.2"/><text x="{mx:.1f}" y="{my + 3.6:.1f}" text-anchor="middle" class="ln">{i}</text>')
        for e, (x, y) in pos.items():
            nm = self.name(e)
            core = e == "ent_nvidia"
            w = 88 if core else 104
            out.append(f'<rect x="{x - w / 2:.0f}" y="{y - 13:.0f}" width="{w}" height="26" rx="4" fill="{"var(--ink)" if core else "#fff"}" stroke="{"var(--marigold)" if core else "var(--ink-2)"}" stroke-width="{2 if core else 1}"/>'
                       f'<text x="{x:.0f}" y="{y + 4:.0f}" text-anchor="middle" class="{"lc" if core else "le"}">{E(nm if len(nm) <= 15 else nm[:14].rstrip() + ".")}</text>')
        return "".join(out) + "</svg>"

    def loops_html(self):
        out = '<div class="loops">'
        for lp in self.loops:
            legs = ""
            for l2 in lp["legs"]:
                out_leg, back = l2["from"] == "ent_nvidia", l2["to"] == "ent_nvidia"
                cls = "out" if out_leg else ("rent" if l2["kind"] in ("rent", "lease") else "back" if back else "on")
                if l2["kind"] in ("rent", "lease") and out_leg:
                    cls = "rent"
                word = "Out" if out_leg else "Back" if back else "Onward"
                if l2.get("amount"):
                    amt = f'<span class="amtl">{E(money(l2["amount"]))}' + (f' <span class="al">{self.prose(l2.get("amount_label"))}</span>' if l2.get("amount_label") else "") + "</span>"
                else:
                    amt = f'<span class="amtl none">Amount: {self.prose(l2.get("amount_label") or "not disclosed")}</span>'
                legs += (f'<li class="leg-{cls}"><span class="dir">{word}:</span> <b>{E(self.name(l2["from"]))}</b> to <b>{E(self.name(l2["to"]))}</b>. {self.prose(l2["description"])} '
                         f'{chip(l2.get("evidence"), "Source", None, "this leg")}{amt}</li>')
            status = "Closed loop" if lp.get("closed") else "Open at the closing leg"
            out += (f'<article class="loop"><h3>{E(lp["title"])}</h3><p class="note">{E(status)} · <span class="analysis">Analysis</span></p>'
                    f'{self.loop_svg(lp)}<p>{self.prose(lp["summary"])}</p><ol>{legs}</ol><p class="note">{self.prose(lp.get("circularity_note"))}</p></article>')
        return out + '</div><p class="note">Blue legs are money out from Nvidia, ochre legs are purchases or payments back to Nvidia, pink legs are rent, gray legs run between other companies. Each leg says Out, Back or Onward in words.</p>'

    def guarantees_html(self):
        by = defaultdict(list)
        for c in self.cx:
            if not c.get("same_obligation_as"):
                by[c["provider"]].append(c)
        def best(cs):
            vals = [(a.get("value"), a.get("text"), k, c) for c in cs for k, a in c["amounts"].items() if a.get("value")]
            return max(vals, key=lambda v: v[0]) if vals else None
        def fold(text):
            m = re.match(r"(.{60,}?(?<!Inc)(?<!Corp)(?<!Ltd)(?<!Co)(?<!No)(?<!U\.S)[.!?])\s+(?=[A-Z])(.+)$", text or "", re.S)
            if not m or len(text) < 160:
                return self.prose(text)
            return f'<details class="inl"><summary>{self.prose(m.group(1))}</summary><p>{self.prose(m.group(2))}</p></details>'
        rows = sorted(by.items(), key=lambda kv: -((best(kv[1]) or (0,))[0] or 0))
        t = self.s["totals"]
        nv = (self.s.get("financials", {}).get("total_guarantees_max") or {})
        body = (f'<tr><th scope="row">Nvidia</th><td class="num">{E(nv.get("text") or "")} {chip(nv.get("evidence"), "Source", None, "Nvidia guarantees")}</td><td>Guarantees of leases and other obligations, mostly OpenAI\'s rent in Ohio; '
                f'{E(money(t["contingent_not_in_force"]))} is signed but not yet in force</td></tr>')
        for prov, cs in rows:
            b = best(cs)
            if not b or b[0] < 1e9:
                continue
            kinds = ", ".join(sorted({KIND_LABEL.get(c["kind"], c["kind"]) for c in cs}))
            a = b[3]["amounts"][b[2]]
            body += (f'<tr><th scope="row">{E(self.name(prov))}</th><td class="num">{E(b[1])} {chip(a.get("evidence") or b[3]["evidence"], "Source", None, self.name(prov))}</td><td>{fold(b[3]["description"])}'
                     f'<span class="note blk">{len(cs)} arrangement{"s" if len(cs) > 1 else ""}: {E(kinds)} {chip(b[3]["evidence"], "Sources", None, "this arrangement")}</span></td></tr>')
        same = [c for c in self.cx if c.get("same_capacity_as_nvidia") and not c.get("same_obligation_as")]
        by_obl = defaultdict(list)
        for c in same:
            key = self.relmap[c["nvidia_links"][0]]["to"] if c.get("nvidia_links") and c["nvidia_links"][0] in self.relmap else c["obligor"]
            by_obl[key].append(c)
        srows = ""
        for k, cs in sorted(by_obl.items(), key=lambda kv: -len(kv[1])):
            def one(c):
                a = next((a for a in c["amounts"].values() if a.get("value")), None)
                return (f"{E(self.name(c['provider']))}: {E(KIND_LABEL.get(c['kind'], c['kind']).lower())}" + (f" ({E(a['text'])})" if a else "")
                        + " " + chip((a or {}).get("evidence") or c["evidence"][:3], "Source", None, self.name(c["provider"])))
            srows += f'<tr><th scope="row">{E(self.name(k))}</th><td><ul class="plain">{"".join("<li>" + one(c) + "</li>" for c in cs)}</ul></td></tr>'
        return (f'<p class="lede">Nvidia is the largest underwriter of AI capacity, but not the only one. Google, Broadcom and AMD stand behind demand for their own chips '
                f'with the same tools, and Meta stands behind capacity it will use. Each figure below is that company\'s largest disclosed amount, so they cannot be added across companies. <span class="analysis">Analysis</span></p>'
                f'<div class="tbl-wrap"><table class="stack"><thead><tr><th scope="col">Provider</th><th scope="col" class="num">Largest disclosed figure</th><th scope="col">What it stands behind</th></tr></thead><tbody>{body}</tbody></table></div>'
                f'<h3>Where others stand behind the same companies as Nvidia</h3>'
                f'<p class="note">{len(same)} of {len([c for c in self.cx if not c.get("same_obligation_as")])} arrangements sit on a company or site that also carries Nvidia support.</p>'
                f'<div class="tbl-wrap"><table class="stack"><thead><tr><th scope="col">Company</th><th scope="col">Who else stands behind it</th></tr></thead><tbody>{srows}</tbody></table></div>')

    def central_bank_html(self):
        rows = ""
        for f in self.cb.get("functions", []):
            v = f["verdict"]
            cls = "v-" + ("Nottest" if v.lower().startswith("not test") else v.split()[0])
            def lis(items):
                return "".join(f"<li>{self.prose(i['text'])} {chip(i.get('evidence'), 'Source')}</li>" for i in items)
            rows += (f'<div class="card"><h3>{E(f["name"])}</h3><p class="note">{self.prose(f.get("analogue"))}</p><p class="verdict {cls}"><span class="vm" aria-hidden="true"></span>{E(v)} <span class="analysis">Analysis</span></p><p>{self.prose(f.get("verdict_reason"))}</p>'
                     f'<p><b>For</b></p><ul>{lis(f.get("evidence_for", []))}</ul><p><b>Against</b></p><ul>{lis(f.get("evidence_against", []))}</ul></div>')
        return (f'<div class="cards2">{rows}</div><h3>Where the analogy breaks</h3><p class="lede">{self.prose(self.cb.get("where_the_analogy_breaks"))} '
                f'{chip(self.cb.get("where_the_analogy_breaks_evidence"), "Sources")}</p><p class="lede"><b>{self.prose(self.cb.get("overall"))}</b></p>'
                '<p class="note"><span class="analysis">Analysis</span> The verdicts are judgments on the evidence shown, not facts reported by any company.</p>')

    def changes_html(self):
        types = sorted({e["change_type"] for e in self.log})
        sel = '<label>Type of change <select id="change-filter"><option value="">All</option>' + "".join(f'<option value="{t}">{E(CHANGE_LABEL.get(t, t))}</option>' for t in types) + "</select></label>"
        def one(e, with_date=True):
            rel = e.get("relationship")
            what = CHANGE_LABEL.get(e["change_type"], e["change_type"])
            cp, title = e.get("counterparty") or "", ISO_DATE.sub(lambda m: fmt.date_long(m.group(0)), e.get("title") or rel or "")
            label = title if (not cp or title.lower().startswith(cp.lower())) else f"{cp}: {title}"
            delta = ""
            if e["change_type"] != "added" and (e.get("field") or e.get("old") is not None or e.get("new") is not None):
                field = re.sub(r"^(entities|relationships|projects)\.[^.]+\.", "", e.get("field") or "").replace(".", " ").replace("_", " ")
                delta = f" {self.prose(field.capitalize())}: {self.prose(e.get('old'))} to {self.prose(e.get('new'))}."
            head = f'<b>{E(dl((e.get("timestamp") or "")[:10]))}</b> · {E(what)} · ' if with_date else ""
            link = f'<a href="#row-{E(rel)}" data-open="{E(rel)}">{E(label)}</a>' if rel in self.relmap else E(label)
            return f'<li data-type="{E(e["change_type"])}">{head}{link}.{delta} {chip(e.get("evidence"), "Source", None, label)}</li>'
        groups = defaultdict(list)
        for e in self.log[:400]:
            if e["change_type"] in ("added", "reverified"):
                groups[((e.get("timestamp") or "")[:10], e["change_type"])].append(e)
        items, done = "", set()
        for e in self.log[:400]:
            key = ((e.get("timestamp") or "")[:10], e["change_type"])
            if key in groups and len(groups[key]) > 5:
                if key in done:
                    continue
                done.add(key)
                g = groups[key]
                n = len(g)
                if key[1] == "added":
                    head = f"register published with {n} records: {self.s['totals']['count']} relationships in the totals, plus unattributed remainders and context records" if n > self.s["totals"]["count"] else f"{n} records added"
                else:
                    head = f"{n} records checked again against their sources, with no change"
                items += (f'<li data-type="{E(key[1])}" class="bulk"><b>{E(dl(key[0]))}</b>: {E(head)}.'
                          f'<details><summary>List all {n}</summary><ul class="changes sub">{"".join(one(x, False) for x in g)}</ul></details></li>')
            else:
                items += one(e)
        return f'<div class="controls">{sel}</div><ul class="changes" id="changes-list">{items}</ul>'

    def timeline_list(self):
        by = defaultdict(list)
        for ev in sorted(self.events, key=lambda e: e["date"]):
            r = self.relmap.get(ev["relationship"])
            if r:
                by[ev["date"][:4]].append((ev, r))
        n = sum(len(v) for v in by.values())
        out = f'<details class="tl-list" id="tl-list"><summary>All {n} events as a list</summary>'
        for y in sorted(by):
            out += f'<h3>{E(y)}</h3><ol>' + "".join(
                f'<li data-date="{E(ev["date"])}" data-rel="{E(r["id"])}"><a href="#row-{E(r["id"])}" data-open="{E(r["id"])}"><b>{E(ds(ev["date"]))}</b> · {E(self.name(r["to"]))}'
                f'{" · restructured or ended" if ev["kind"] in ("restructuring", "termination") else ""}</a>: {self.prose(ev["summary"])}</li>' for ev, r in by[y]) + "</ol>"
        return out + "</details>"

    def method_html(self):
        s = self.s
        sm = s["source_mix"]
        okev = lambda ids: [i for i in ids or [] if i in self.ev]
        def named(b):
            txt = b.get("named_text") or (money(b["named"]) if b.get("named") is not None else "")
            if b.get("named") == 0:
                return "None"
            if not b.get("named"):
                return E(txt)
            if b.get("named_rels"):
                return E(txt) + " " + mchip("funded", "named equity purchases", rels=b["named_rels"], ev=okev(b.get("named_evidence")))
            return E(txt) + " " + chip(okev(b.get("named_evidence")), "Source", None, "named amount")
        bridge = "".join(f'<tr><th scope="row">{E(b["line"])}</th><td class="num">{E(money(b["nvidia"]) if b.get("nvidia") is not None else "Not disclosed")} {chip(okev(b.get("evidence")), "Source", None, b["line"])}</td>'
                         f'<td class="num">{named(b)}</td><td class="note">{self.prose(b["note"])}</td></tr>' for b in s["bridge"])
        mv = lambda rid, k: ((self.relmap.get(rid) or {}).get("amounts", {}).get(k) or {}).get("evidence")
        pos = "".join(f'<tr><th scope="row">{E(p["name"])}</th><td class="num">{E(money(p["value"]))} {chip(mv(p["relationship"], "market_value"), "Source", p["relationship"], p["name"])}</td><td>{E(dl(p.get("as_of")))}</td><td>{"Yes" if p.get("cost_known") else "No"}</td></tr>' for p in s["positions_by_value"])
        pos += "".join(f'<tr><th scope="row">{E(p["name"])}</th><td class="num">not valued (cost {E(money(p["cost"]))}) {chip(mv(p["relationship"], "funded"), "Source", p["relationship"], p["name"])}</td><td>{E(p["reason"])}</td><td>Yes</td></tr>' for p in s.get("positions_not_yet_valued", []))
        return f"""
<h3>What Nvidia reports, beside what can be named</h3>
<p>Nvidia's own accounts show far more than any outsider can tie to named deals. <span class="analysis">Analysis</span></p>
<div class="tbl-wrap"><table class="stack"><thead><tr><th scope="col">Line</th><th scope="col" class="num">Nvidia reports</th><th scope="col" class="num">Named and sized here</th><th scope="col">Note</th></tr></thead><tbody>{bridge}</tbody></table></div>
<h3>Largest positions by value</h3>
<p class="note">Values from Nvidia's holdings report of 30 September 2026. A position whose cost is not disclosed adds nothing to gross exposure, so it is shown here.</p>
<div class="tbl-wrap"><table class="stack"><thead><tr><th scope="col">Counterparty</th><th scope="col" class="num">Value</th><th scope="col">As of or reason</th><th scope="col">Cost disclosed</th></tr></thead><tbody>{pos}</tbody></table></div>
<h3>How the data was gathered</h3>
<p>Every relationship starts from what Nvidia was legally required to disclose: its annual and quarterly reports, current reports, holdings reports and ownership filings since January 2023. Then the same deal was traced in what the other company filed: its annual and quarterly reports, prospectuses, credit agreements and indentures, newest first. Company releases fill deals that never reached a filing. A sweep of every company's filings for Nvidia near words such as backstop, guarantee, warrant and lease found the rest.</p>
<p>{E(sm["note"])} The register holds {sum(sm["evidence_by_tier"].values()):,} citations: {sm["evidence_by_tier"].get("1", 0):,} primary and {sm["evidence_by_tier"].get("2", 0)} from news. {sm["one_sided_relationships"]} of {sm["relationships"]} relationships are disclosed by one side only.</p>
<h3>Source policy</h3>
<p>A figure is shown only if a primary source (a filing, the company's own release, a regulator, a court, a lien registry or a rating agency's public release) or two independent named publications (Bloomberg, Reuters, The Wall Street Journal, the Financial Times, The Information, CNBC, Barron's, The Economist, Nikkei Asia, Axios) contain it. Otherwise it reads "Not confirmed". Blogs, social posts, aggregators and sell-side notes are never used. Every quote was found word for word in a saved copy of its source, and every number sits in or beside that quote.</p>
<h3>Definitions</h3>
<dl class="pb defs">
<dt><dfn id="def-funded">Funded</dfn></dt><dd>Cash Nvidia has paid. On the page it counts the cost of shares still held: a stake partly sold counts only the part still reported.</dd>
<dt><dfn id="def-committed">Committed</dfn></dt><dd>A legally binding amount under a definitive agreement. Where no source says how much has been paid, it is counted once and never called unpaid.</dd>
<dt><dfn id="def-contingent">Contingent maximum</dfn></dt><dd>The most Nvidia could be required to pay under a guarantee, backstop or similar promise, with the trigger stated. A guaranty that cannot yet be called is labeled not yet in force.</dd>
<dt><dfn id="def-headline">Headline</dfn></dt><dd>The largest figure announced, often "up to". Shown, never added to exposure.</dd>
<dt><dfn id="def-gross">Gross exposure</dfn></dt><dd>Funded plus committed plus contingent maximum, using confirmed amounts only. If any part is not disclosed it is a lower bound and reads "at least".</dd>
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
            for k in ("title", "insight"):          # reader dates in words, as everywhere else on the page
                r[k] = ISO_DATE.sub(lambda m: fmt.date_long(m.group(0)), r.get(k) or "")
        d = self.data()
        disp = s["display"]
        lib = "".join(self.source_li(i, True) for i in self.ev)
        first_note = ("<p class='lede'>These illustrate how losses would travel, not forecasts.</p>"
                      "<div class='scen' role='group' aria-label='Scenarios'><button class='btn' type='button' data-s='S1' aria-pressed='false'>Demand pause</button>"
                      "<button class='btn' type='button' data-s='S2' aria-pressed='false'>Lab funding gap</button><button class='btn' type='button' data-s='S3' aria-pressed='false'>Collateral repricing</button></div>"
                      "<div class='sliders' id='sliders'></div><div class='out' id='stress-out' aria-live='polite'><noscript>Scenario sliders need script. Results at default settings are in the research files.</noscript></div>"
                      "<p class='note'>Defaults are illustrative, not anchored to an observed move. Choosing a scenario rings the companies it touches on the map; the map legend has a control to clear the rings.</p>")
        views = [("constellation", "Map"), ("ledger-view", "Ledger"), ("timeline", "Timeline"), ("loops", "Loops"), ("stress", "Stress"),
                 ("others", "Who else guarantees"), ("verdict", "Central bank?"), ("changes-view", "What changed"), ("method", "Method")]
        nav = "".join(f'<li><a href="#{k}">{E(v)}</a></li>' for k, v in views)
        last = s.get("last_change") or s["data_as_of"]
        sec = lambda i, title, body, extra="": f'<section class="view" id="{i}" aria-labelledby="h-{i}" tabindex="-1"><h2 id="h-{i}">{E(title)}</h2>{body}</section>'
        page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Is Nvidia the Central Bank of AI?</title>
<meta name="description" content="{E(disp.get('subtitle'))}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='10' fill='%231B1D26' stroke='%23F0B429' stroke-width='4'/%3E%3C/svg%3E">
<script>document.documentElement.className='js'</script>
<style>{CSS}</style><noscript><style>.ranked{{display:block}}.map-box,.legend button,.tl-box,.tl-legend,.scen,.sliders,.skip-in{{display:none}}</style></noscript></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="site wrap"><a class="builtby" href="{E(disp.get('built_by_url'))}">Built By <strong>Resolute Business Development</strong></a>
<h1>{E(disp.get('site_title'))}</h1><p class="sub">{E(disp.get('subtitle'))}</p>
<div class="pills"><span class="pill">Data as of <b>{E(dl(s['data_as_of']))}</b></span><a class="pill" href="#changes-view">Last change <b>{E(dl(last[:10]))}</b></a></div></header>
<nav class="views" aria-label="Views"><div class="wrap"><ul>{nav}</ul></div></nav>
<main id="main" class="wrap">
<section class="summary" aria-labelledby="h-summary"><h2 class="sr" id="h-summary">Summary</h2>{self.tiles()}{self.summary()}</section>
{sec("constellation", "The map", f'<a class="skip-in" href="#ledger-view">Skip the map</a><div class="map-wrap"><div class="map-box" id="map-box"><button type="button" class="btn map-close" id="map-close" aria-label="Close map">Close map</button><svg id="map" role="group" aria-label="Radial map of Nvidia\'s relationships. Arrow keys move between nodes. Each node opens its detail." aria-describedby="ranked"></svg><div class="tip" id="tip"></div></div>{self.legend()}</div>{self.ranked(d)}')}
{sec("ledger-view", "The Ledger", self.ledger())}
{sec("timeline", "Timeline", f'<p class="note tl-help">Each mark is a dated event. Drag across the track to filter the map and Ledger to that period, or use the dates. Click empty track to clear.</p><a class="skip-in" href="#loops">Skip the timeline</a>'
     f'<div class="controls"><label>From <input type="date" id="tl-from" min="2023-01-01" max="{E(s["data_as_of"])}"></label><label>To <input type="date" id="tl-to" min="2023-01-01" max="{E(s["data_as_of"])}"></label><button type="button" class="btn" id="tl-clear">Clear dates</button><span class="note" id="tl-range" role="status"></span></div>'
     '<p class="note tl-legend"><svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><circle cx="7" cy="7" r="5" fill="var(--cobalt)"/></svg> Event '
     '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M7,1 L13,7 L7,13 L1,7 z" fill="var(--cochineal)"/></svg> Restructured or ended (diamond)</p>'
     f'<div class="tl-box" id="tl-box"><svg id="tl" role="group" aria-label="Timeline of events by cluster. Left and right arrow keys move between events."></svg></div>{self.timeline_list()}')}
{sec("loops", "Circular flows", '<p class="lede">Where Nvidia money goes out and comes back as demand for Nvidia systems. No loop has a disclosed dollar value on its return leg, so no circularity ratio can be computed.</p>' + self.loops_html())}
{sec("stress", "Stress", first_note)}
{sec("others", "Who else guarantees AI capacity", self.guarantees_html())}
{sec("verdict", "Is Nvidia a central bank?", self.central_bank_html())}
{sec("changes-view", "What changed", self.changes_html())}
{sec("method", "Method and sources", self.method_html())}
</main>
<footer class="wrap"><p><a class="builtby" href="{E(disp.get('built_by_url'))}">Built By <strong>Resolute Business Development</strong></a></p>
<p>Not investment advice. This page describes exposure from public filings and company releases; it never recommends a trade. Data as of {E(dl(s['data_as_of']))}.</p></footer>
<div id="scrim" hidden></div>
<aside id="panel" hidden aria-hidden="true" role="dialog" aria-modal="true" aria-label="Relationship detail"><button class="close" type="button" aria-label="Close detail">×</button><div id="panel-body"></div></aside>
<div id="sources-lib" hidden><ol id="sources">{lib}</ol></div>
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
