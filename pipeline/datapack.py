"""Evidence pack for audit: research/Nvidia_Exposure_Datapack.xlsx

  python3 -m pipeline.datapack

One tab per exposure type, one row per relationship. Every amount sits beside its as-of date and its source
(evidence id linked to the source document, quote in the cell note). Blue = sourced input, black = formula.
Amounts that fail the display rule appear as "Not confirmed" text and so cannot enter a total.
The Summary tab adds the type tabs by formula and ties the result to the register's independent totals.
"""
from __future__ import annotations

from datetime import date

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L

from . import fmt
from .checks import Register, independent_totals
from .common import REGISTER, ROOT, load_json
from .system_view import TYPE_NAMES

OUT = ROOT / "research" / "Nvidia_Exposure_Datapack.xlsx"
BLUE, BLACK, GREEN = Font(name="Arial", size=10, color="0000FF"), Font(name="Arial", size=10, color="000000"), Font(name="Arial", size=10, color="008000")
BOLD = Font(name="Arial", size=10, bold=True)
HEAD_FILL = PatternFill("solid", fgColor="D9E1F2")
TITLE = Font(name="Arial", size=14, bold=True)
MONEY = '$#,##0.0;$(#,##0.0);"-"'
THIN, DOUBLE = Side(style="thin"), Side(style="double")
AMOUNTS = [("headline", "Headline announced"), ("committed_total", "Committed total (incl. funded)"), ("funded", "Funded"), ("contingent_max", "Contingent maximum")]


def header(ws, row, labels, widths=None):
    for i, lab in enumerate(labels, 1):
        c = ws.cell(row=row, column=i, value=lab)
        c.font, c.fill, c.alignment = BOLD, HEAD_FILL, Alignment(wrap_text=True, vertical="top", horizontal="left")
        if widths:
            ws.column_dimensions[L(i)].width = widths[i - 1]
    ws.row_dimensions[row].height = 44


def put_amount(ws, row, col, a, reg):
    """Writes value | as of | source into three columns. Returns nothing."""
    cell = ws.cell(row=row, column=col)
    qual = ""
    text = fmt.amount_text(a)
    if a and a.get("value") is not None and a.get("display_eligible") and not a.get("not_applicable"):
        cell.value, cell.number_format, cell.font = a["value"] / 1e6, MONEY, BLUE
        if a.get("qualifier"):
            qual = f'Source states this figure as "{a["qualifier"]}".\n'

    else:
        cell.value, cell.font = text, BLACK
    cell.alignment = Alignment(horizontal="right")
    ws.cell(row=row, column=col + 1, value=(a or {}).get("as_of") or "").font = BLUE
    ids = list((a or {}).get("evidence") or [])
    for comp in (a or {}).get("components") or []:
        ids += comp["evidence"]
    src = ws.cell(row=row, column=col + 2, value=", ".join(dict.fromkeys(ids)))
    src.font = GREEN
    if ids and ids[0] in reg.ev:
        ev = reg.ev[ids[0]]
        src.hyperlink = ev.get("source_link") or ev["url"]
        note = "\n".join(f"{i}: \"{reg.ev[i]['quote']}\" ({reg.ev[i]['publisher']}, {reg.ev[i]['published']})" for i in dict.fromkeys(ids) if i in reg.ev)
        cell.comment = Comment((qual + note)[:1500], "Register")


def type_tab(wb, code, rels, reg):
    ws = wb.create_sheet(code)
    ws["A1"].value, ws["A1"].font = f"{code}  {TYPE_NAMES[code]}", TITLE
    ws["A2"].value = "USD millions. Blue = sourced input. Black = formula. \"Not confirmed\" = fails the display rule, never summed. Hover an amount for the quote; the source column links to the document."
    ws["A2"].font = BLACK
    labels = ["Relationship id", "Counterparty", "Title", "Status", "Source strength", "Announced", "Matures"]
    widths = [30, 22, 46, 14, 16, 12, 12]
    for _, lab in AMOUNTS:
        labels += [lab, "As of", "Source"]
        widths += [16, 11, 18]
    labels += ["Share of purchase still held", "Funded and still held (cost)", "Committed, confirmed not yet paid", "Committed, paid portion not disclosed", "Gross exposure",
               "Lower bound?", "Contingent in force?", "Reconciliation", "Wrong-way risk", "Last verified", "Contingent not yet in force"]
    widths += [14, 16, 16, 16, 16, 12, 12, 14, 14, 12, 16]
    header(ws, 4, labels, widths)
    first = 5
    col = {k: 8 + 3 * i for i, (k, _) in enumerate(AMOUNTS)}   # value columns
    base = 8 + 3 * len(AMOUNTS)
    c_share, c_held, c_unf, c_split, c_gross = base, base + 1, base + 2, base + 3, base + 4
    row = first
    for r in sorted(rels, key=lambda r: -((r.get("derived") or {}).get("gross_exposure") or 0)):
        ent = reg.ent[r["to"]]
        vals = [r["id"], ent["short_name"], r["title"], r["status"], r["claim_basis"], r["dates"].get("announced") or "", r["dates"].get("maturity") or ""]
        for i, v in enumerate(vals, 1):
            ws.cell(row=row, column=i, value=v).font = BLUE
        for k, _ in AMOUNTS:
            put_amount(ws, row, col[k], r["amounts"].get(k), reg)
        f, c, g = L(col["funded"]), L(col["committed_total"]), L(col["contingent_max"])
        h = r.get("holding") or {}
        share = 0.0 if r["status"] == "terminated" else (min(1.0, h["shares"] / h["shares_acquired"]) if h.get("shares") is not None and h.get("shares_acquired") else 1.0)
        sc = ws.cell(row=row, column=c_share, value=share)
        sc.number_format, sc.font = "0.0%", BLUE
        ws.cell(row=row, column=c_held, value=f'=IF(ISNUMBER({f}{row}),{f}{row}*{L(c_share)}{row},0)')
        ws.cell(row=row, column=c_unf, value=f'=IF(AND(ISNUMBER({c}{row}),ISNUMBER({f}{row})),MAX(0,{c}{row}-{f}{row}),0)')
        ws.cell(row=row, column=c_split, value=f'=IF(AND(ISNUMBER({c}{row}),NOT(ISNUMBER({f}{row}))),{c}{row},0)')
        ws.cell(row=row, column=c_gross, value=f'={L(c_held)}{row}+{L(c_unf)}{row}+{L(c_split)}{row}+IF(ISNUMBER({g}{row}),{g}{row},0)')
        d = r.get("derived") or {}
        cm = r["amounts"]["contingent_max"]
        c_nif = c_gross + 6
        ws.cell(row=row, column=c_nif, value=f'=IF(AND(ISNUMBER({g}{row}),LEFT({L(c_gross + 2)}{row},2)="No"),{g}{row},0)')
        for cc in (c_held, c_unf, c_split, c_gross, c_nif):
            ws.cell(row=row, column=cc).number_format, ws.cell(row=row, column=cc).font = MONEY, BLACK
        tail = ["Yes" if d.get("gross_lower_bound") else "No", ("" if not cm.get("value") else "Yes" if cm.get("in_force", True) else "No: " + cm.get("effective_note", "")),
                r["reconciliation"]["result"], r["credit"]["wwr"],
                max([a.get("last_verified") or "" for a in r["amounts"].values() if isinstance(a, dict)] or [""])]
        for i, v in enumerate(tail):
            ws.cell(row=row, column=c_gross + 1 + i, value=v).font = BLUE
        row += 1
    last = row - 1
    total = row + 1
    ws.cell(row=total, column=1, value="Total (confirmed amounts only)").font = BOLD
    for cc in [col[k] for k, _ in AMOUNTS] + [c_held, c_unf, c_split, c_gross, c_gross + 6]:
        c = ws.cell(row=total, column=cc, value=f"=SUM({L(cc)}{first}:{L(cc)}{last})" if last >= first else 0)
        c.number_format, c.font, c.border = MONEY, BOLD, Border(top=THIN, bottom=DOUBLE)
    ws.freeze_panes = "C5"
    return {"sheet": code, "total_row": total, "cols": {**{k: L(v) for k, v in col.items()}, "funded_held": L(c_held), "committed_unfunded": L(c_unf), "committed_split_unknown": L(c_split), "gross": L(c_gross), "not_in_force": L(c_gross + 6)}, "count": len(rels)}


def build():
    reg = Register()
    wb = Workbook()
    summ = wb.active
    summ.title = "Summary"
    core = [r for r in reg.relationships if not r.get("aggregate_of") and r["type_primary"] != "CX"]
    refs = []
    for code in TYPE_NAMES:
        rels = [r for r in core if r["type_primary"] == code]
        if rels:
            refs.append(type_tab(wb, code, rels, reg))

    # context and unattributed remainders: shown, never summed
    for name, rels, title in (("Context", [r for r in reg.relationships if r["type_primary"] == "CX" and not r.get("aggregate_of")], "Context records (no Nvidia capital; excluded from totals)"),
                              ("Unattributed", [r for r in reg.relationships if r.get("aggregate_of")], "Unattributed remainders of Nvidia's disclosed aggregates (analysis; excluded from every total)")):
        ws = wb.create_sheet(name)
        ws["A1"].value, ws["A1"].font = title, TITLE
        labels, widths = ["Relationship id", "Aggregate / counterparty", "Title", "Status"], [44, 26, 60, 14]
        for _, lab in AMOUNTS:
            labels += [lab, "As of", "Source"]
            widths += [16, 11, 22]
        labels.append("Notes"); widths.append(90)
        header(ws, 3, labels, widths)
        for i, r in enumerate(rels, 4):
            for j, v in enumerate([r["id"], r.get("aggregate_of") or reg.ent[r["to"]]["short_name"], r["title"], r["status"]], 1):
                ws.cell(row=i, column=j, value=v).font = BLUE
            for n, (k, _) in enumerate(AMOUNTS):
                put_amount(ws, i, 5 + 3 * n, r["amounts"].get(k), reg)
            ws.cell(row=i, column=5 + 3 * len(AMOUNTS), value=(r.get("notes") or "")[:900]).font = BLUE
        ws.freeze_panes = "C4"

    # reconciliation
    ws = wb.create_sheet("Reconciliation")
    ws["A1"].value, ws["A1"].font = "Both sides: what Nvidia disclosed, what the counterparty disclosed", TITLE
    header(ws, 3, ["Relationship id", "Counterparty", "Type", "Result", "Nvidia side", "Nvidia evidence", "Counterparty side", "Counterparty evidence", "Differences"], [30, 20, 8, 13, 70, 22, 70, 22, 70])
    for i, r in enumerate(sorted(reg.relationships, key=lambda r: r["reconciliation"]["result"]), 4):
        rc = r["reconciliation"]
        diffs = "; ".join(f"{d['field']}: Nvidia {d['nvidia_value']} vs counterparty {d['counterparty_value']}" for d in rc["differences"])
        for j, v in enumerate([r["id"], reg.ent[r["to"]]["short_name"], r["type_primary"], rc["result"], rc["nvidia_side"][:900], ", ".join(rc.get("nvidia_evidence") or []),
                               rc["counterparty_side"][:900], ", ".join(rc.get("counterparty_evidence") or []), diffs[:900]], 1):
            c = ws.cell(row=i, column=j, value=v)
            c.font, c.alignment = BLUE, Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "C4"

    # Nvidia financials
    ws = wb.create_sheet("Nvidia financials")
    ws["A1"].value, ws["A1"].font = "Nvidia figures used as denominators (USD millions)", TITLE
    header(ws, 3, ["Measure", "Value", "As of", "Source", "Note"], [34, 16, 12, 26, 100])
    i = 4
    for k, a in reg.financials.items():
        if isinstance(a, dict) and "value" in a:
            ws.cell(row=i, column=1, value=k).font = BLUE
            put_amount(ws, i, 2, a, reg)
            ws.cell(row=i, column=5, value=a.get("note", "")).font = BLUE
            i += 1

    # sources
    ws = wb.create_sheet("Sources")
    ws["A1"].value, ws["A1"].font = "Every citation in the register", TITLE
    header(ws, 3, ["Evidence id", "Tier", "Kind", "Publisher", "Published", "Title", "Section", "Quote (verbatim)", "Accession", "Open source", "Retrieved"], [12, 6, 16, 24, 12, 50, 34, 70, 22, 60, 20])
    for i, e in enumerate(reg.evidence, 4):
        for j, v in enumerate([e["id"], e["tier"], e["kind"], e["publisher"], e["published"], e["title"], e.get("section", ""), e["quote"], e.get("accession") or "", e.get("source_link") or e["url"], e["retrieved"]], 1):
            c = ws.cell(row=i, column=j, value=v)
            c.font = BLUE
        ws.cell(row=i, column=10).hyperlink = e.get("source_link") or e["url"]
        ws.cell(row=i, column=10).font = GREEN
    ws.freeze_panes = "B4"

    # seeds
    import csv
    ws = wb.create_sheet("Seeds")
    ws["A1"].value, ws["A1"].font = "Seed hypotheses and how each ended", TITLE
    rows = list(csv.reader(open(ROOT / "research" / "seed_status.csv", encoding="utf-8")))
    header(ws, 3, rows[0], [8, 34, 80, 12, 90, 50])
    for i, r in enumerate(rows[1:], 4):
        for j, v in enumerate(r, 1):
            ws.cell(row=i, column=j, value=v).font = BLUE

    # summary with tie-out
    t = independent_totals(reg)
    summ["A1"].value, summ["A1"].font = "Is Nvidia the Central Bank of AI?  Exposure evidence pack", TITLE
    summ["A2"].value = f"Prepared {date.today().isoformat()} by Resolute Business Development. USD millions. Confirmed amounts only: a figure counts only if a primary source or two independent named publications contain it. Not investment advice."
    cols = [("funded_held", "Funded and still held (cost)", "funded"), ("committed_unfunded", "Committed, confirmed not yet paid", "committed_unfunded"),
            ("committed_split_unknown", "Committed, paid portion not disclosed", "committed_split_unknown"), ("contingent_max", "Contingent maximum", "contingent_max"),
            ("not_in_force", "of which not yet in force", "contingent_not_in_force"), ("gross", "Gross exposure", "gross"), ("headline", "Headline announced (never added)", "headline")]
    header(summ, 4, ["Exposure type", "Relationships"] + [c[1] for c in cols], [38, 14, 18, 18, 18, 18, 18, 16, 20])
    row = 5
    for ref in refs:
        summ.cell(row=row, column=1, value=f"{ref['sheet']}  {TYPE_NAMES[ref['sheet']]}").font = BLACK
        summ.cell(row=row, column=2, value=ref["count"]).font = BLUE
        for j, (k, _, _) in enumerate(cols, 3):
            c = summ.cell(row=row, column=j, value=f"='{ref['sheet']}'!{ref['cols'][k]}{ref['total_row']}")
            c.number_format, c.font = MONEY, GREEN
        row += 1
    tot = row
    ncol = 2 + len(cols)
    summ.cell(row=tot, column=1, value="Total").font = BOLD
    for j in range(2, ncol + 1):
        c = summ.cell(row=tot, column=j, value=f"=SUM({L(j)}5:{L(j)}{tot - 1})")
        c.font, c.border = BOLD, Border(top=THIN, bottom=DOUBLE)
        if j > 2:
            c.number_format = MONEY
    summ.cell(row=tot + 2, column=1, value="Register totals (independent recomputation)").font = BOLD
    for j, k in enumerate(["count"] + [c[2] for c in cols], 2):
        c = summ.cell(row=tot + 2, column=j, value=t[k] if k == "count" else t[k] / 1e6)
        c.font = BLUE
        if j > 2:
            c.number_format = MONEY
    summ.cell(row=tot + 3, column=1, value="Difference (must be zero)").font = BOLD
    for j in range(2, ncol + 1):
        c = summ.cell(row=tot + 3, column=j, value=f"=ROUND({L(j)}{tot}-{L(j)}{tot + 2},3)")
        c.font = BLACK
        if j > 2:
            c.number_format = '$#,##0.000;$(#,##0.000);"0"'
    sv = load_json(REGISTER / "system_view.json", {})
    brow = tot + 15
    summ.cell(row=brow - 1, column=1, value="Bridge to Nvidia's own disclosures at 25 October 2026 (USD millions; analysis)").font = BOLD
    for j, lab in enumerate(["Line", "Nvidia reports", "Named and sized in this register", "Note"], 1):
        c = summ.cell(row=brow, column=j, value=lab)
        c.font, c.fill = BOLD, HEAD_FILL
    for i, b in enumerate(sv.get("bridge", []), brow + 1):
        summ.cell(row=i, column=1, value=b["line"]).font = BLACK
        for j, k in ((2, "nvidia"), (3, "named")):
            c = summ.cell(row=i, column=j, value=(b[k] / 1e6 if b[k] is not None else (b.get("named_text") or "") if k == "named" else "Not disclosed"))
            c.font, c.number_format = BLUE, MONEY
        summ.cell(row=i, column=4, value=b["note"]).font = BLACK
    notes = [
        "How to read this pack",
        "Funded and still held = cash paid, scaled to the share of the purchase Nvidia still reports holding. Committed, confirmed not yet paid = binding amount less what is funded, both sourced.",
        "Committed, paid portion not disclosed = binding amounts where no source says how much has been paid; counted once and never called unpaid.",
        "Contingent maximum = the most Nvidia could be required to pay under a guarantee or backstop; the type tabs say whether each is in force yet. Gross = the four added together. Headline is what was announced and is never added.",
        f"{t['lower_bound_count']} of {t['count']} relationships are lower bounds because at least one component is not disclosed or not confirmed.",
        "Tabs: one per exposure type, then Context, Unattributed (remainders of Nvidia's disclosed aggregates, excluded from totals), Reconciliation, Nvidia financials, Sources, Seeds.",
        "Every amount has its as-of date and source beside it. Hover the amount for the verbatim quote. The source cell opens the document at the passage.",
        (sv.get("source_mix", {}).get("note", "") + f" {sv.get('source_mix', {}).get('one_sided_relationships', '')} of {sv.get('source_mix', {}).get('relationships', '')} relationships are disclosed by one side only."),
    ]
    for i, n in enumerate(notes):
        c = summ.cell(row=tot + 5 + i, column=1, value=n)
        c.font = BOLD if i == 0 else BLACK
    summ.freeze_panes = "B5"
    wb.save(OUT)
    return OUT, t


if __name__ == "__main__":
    out, t = build()
    print("wrote", out.relative_to(ROOT), "| register gross", fmt.money(t["gross"]))
