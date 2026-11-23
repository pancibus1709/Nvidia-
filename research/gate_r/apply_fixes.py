"""Gate R fixes applied to the research drafts after independent re-sourcing (23 November 2026).
Each change is listed in research/gate_r/FIXES.md. Run once: python3 research/gate_r/apply_fixes.py"""
import json, glob, sys
sys.path.insert(0, ".")
TODAY = "2026-11-23"
files = {f: json.load(open(f)) for f in glob.glob("research/drafts/cluster_*.json")}
def rel(i):
    for f, d in files.items():
        for r in d["relationships"]:
            if r["id"] == i:
                return r, d
    raise KeyError(i)
log = []
def note(r, text):
    r["notes"] = ((r.get("notes") or "").rstrip() + " " + text).strip()

r, d = rel("rel_openai_eqc_2025")
r["status"] = "restructured"
r["insight_template"] = "Nvidia's {headline} letter of intent with {counterparty} produced no disclosed definitive agreement; a separate equity purchase followed, so the headline adds no binding exposure."
note(r, "Gate R: status changed from letter of intent to restructured. Nvidia's annual report filed 2026-02-25 says it was finalizing an investment and partnership agreement with OpenAI (ev_140027); OpenAI's round naming Nvidia followed (rel_openai_eq_2026); Nvidia's two later quarterly reports do not mention the letter of intent. Analysis: no source says the letter of intent was terminated or that the later purchase counts against it.")
r["evidence"] = sorted(set(r["evidence"] + ["ev_140027"]))
d["events"].append({"id": "evt_openai_loi_finalizing_2026", "date": "2026-02-25", "relationship": "rel_openai_eqc_2025", "kind": "restructuring",
                    "summary": "Nvidia's annual report says it is finalizing an investment and partnership agreement with OpenAI, in place of the letter of intent wording.", "evidence": ["ev_140027"]})
log.append("rel_openai_eqc_2025: status loi_or_framework to restructured; insight rewritten; event added (verifier 1, n=1)")

r, d = rel("rel_wayve_eqc_2025")
r["status"] = "restructured"
note(r, "Gate R: status changed to restructured. Wayve closed its Series D on 2026-02-25 with Nvidia participating (ev_140022); Nvidia's amount is not disclosed, so the letter of intent figure stays a headline only.")
r["evidence"] = sorted(set(r["evidence"] + ["ev_140022"]))
d["events"].append({"id": "evt_wayve_series_d_close_2026", "date": "2026-02-25", "relationship": "rel_wayve_eqc_2025", "kind": "restructuring",
                    "summary": "Wayve closes its Series D with Nvidia participating; the amount Nvidia invested is not stated.", "evidence": ["ev_140022"]})
log.append("rel_wayve_eqc_2025: status to restructured; closing event added (verifier 1, n=14)")

r, d = rel("rel_uk_ai_startup_program_eqc_2025")
h = r["amounts"]["headline"]
h.update({"as_of": "2025-09-18", "last_verified": TODAY, "evidence": sorted(set(h["evidence"] + ["ev_140020"]))})
r["evidence"] = sorted(set(r["evidence"] + ["ev_140020"]))
log.append("rel_uk_ai_startup_program_eqc_2025: sterling headline now dated and shown in pounds, not converted (verifier 1, n=12)")

r, d = rel("rel_tusimple_eq_2023")
r["status"] = "completed"
r["insight_template"] = "Nvidia reported {counterparty} shares until the company left the exchange; whether Nvidia still holds them is not disclosed."
note(r, "Gate R: status changed from terminated to completed. The position leaves Nvidia's holdings report after TuSimple delisted and deregistered in early 2024 (ev_150020, ev_150021), which by itself removes it from that report, so no sale is shown.")
r["evidence"] = sorted(set(r["evidence"] + ["ev_150020", "ev_150021"]))
log.append("rel_tusimple_eq_2023: status terminated to completed; insight no longer claims the position is closed (verifier 2, n=18)")

r, d = rel("rel_coreweave_gu_2026")
r["type_primary"], r["types_secondary"] = "CX", ["GU", "FC"]
note(r, "Gate R: reclassified from guarantee to context. The January 2026 release states an intent only; no guarantee, instrument or amount exists (ev_150004).")
r["evidence"] = sorted(set(r["evidence"] + ["ev_150004"]))
log.append("rel_coreweave_gu_2026: type GU to CX because no guarantee exists, only a stated intent (verifier 2, n=22)")

r, d = rel("rel_meta_eq_2026")
note(r, "Gate R: Meta's offering has priced and its prospectus still calls the interest not binding. No filing yet shows whether Nvidia bought shares. Status stays a framework until one does.")
log.append("rel_meta_eq_2026: note added that the offering priced and Nvidia's purchase is unconfirmed (verifier 3, n=43)")

r, d = rel("rel_corning_pp_2026")
r["dates"]["announced"] = "2026-05-06"
log.append("rel_corning_pp_2026: announced date set to 2026-05-06 (verifier 3, n=38). Funded stays undisclosed because Corning does not name the depositor.")

# new facts from the filings sweep (R2)
r, d = rel("rel_coreweave_bk_2025")
if not any(e["id"] == "ent_galaxy_digital" for e in d["entities"]):
    d["entities"].append({"id": "ent_galaxy_digital", "name": "Galaxy Digital Inc.", "short_name": "Galaxy Digital", "cluster": "lender", "depth": 2, "public": True,
                          "ticker": "GLXY", "cik": None, "country": "US", "description": "Owner of a data center campus leased to CoreWeave and issuer of notes secured on it."})
r["depth2_links"].append({"entity": "ent_galaxy_digital", "role": "bondholder",
                          "description": "Galaxy Digital's presentation for notes secured on a CoreWeave leased campus cites Nvidia's obligation to buy CoreWeave's residual capacity.",
                          "amount": None, "evidence": ["ev_170016"]})
r["evidence"] = sorted(set(r["evidence"] + ["ev_170016"]))
log.append("rel_coreweave_bk_2025: depth 2 link to Galaxy Digital added, the first sourced case of a financing document citing the order (R2)")

r, d = rel("rel_nscale_gu_2025")
if not any(e["id"] == "ent_ionic_digital" for e in d["entities"]):
    d["entities"].append({"id": "ent_ionic_digital", "name": "Ionic Digital Inc.", "short_name": "Ionic Digital", "cluster": "other", "depth": 2, "public": True,
                          "ticker": "IOND", "cik": "0002007691", "country": "US", "description": "Landlord of Nscale's Ward County, Texas site, whose rent Nvidia guarantees."})
r["depth2_links"].append({"entity": "ent_ionic_digital", "role": "landlord",
                          "description": "Ionic Digital is the landlord of the Ward County lease to Nscale; its filing describes Nvidia's guarantee of the early rent.",
                          "amount": None, "evidence": ["ev_170012"]})
r["evidence"] = sorted(set(r["evidence"] + ["ev_170012"]))
log.append("rel_nscale_gu_2025: depth 2 link to the landlord, Ionic Digital, added (R2)")

for f, d in files.items():
    json.dump(d, open(f, "w"), indent=2, ensure_ascii=False)
open("research/gate_r/FIXES.md", "w").write("# Gate R fixes applied after independent re-sourcing\n\n" + "\n".join(f"- {l}" for l in log) + """

## Verifier findings not acted on, with reasons

- n=5 Anthropic, n=24 Nscale equity, n=27 Nebius warrant: the verifiers read the claims file as showing a contingent amount equal to the funded amount. The register records contingent as not applicable on all three. No change needed.
- n=3 OpenAI lease guaranties: the filing calls them residual value guaranties. The record keeps guarantee as the primary type because the trigger is the tenant's default, and already lists residual value as a secondary type.
- n=21 CoreWeave: the filing calls $6.3 billion the initial value of the order, not a cap. The record already says so in the amount note.
- n=31 to 33 Intel, Nokia, Synopsys: funded is the cash Nvidia paid, which does not change when shares are later sold. The holdings, market values and notes already show the reduced positions at 30 September 2026.
- n=38 Corning: the $1.0 billion deposit is not entered as funded by Nvidia because Corning does not name the depositor. The link is labeled analysis.
- n=25 Nscale notes: no filing confirms the second $1.0 billion closed, so funded stays at $1.0 billion.
""")
print("\n".join(log))
