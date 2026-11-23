# R5/R6 report: clusters D and E (project vehicles, financing platforms, hyperscalers, sovereign programs)

**Date:** 23 November 2026. **Namespace:** veh (evidence ev_100001 to ev_100055). Reused: ev_30001 to ev_30028, ev_30074, ev_30076, ev_30077 (R3), ev_10040 to ev_10046 (R1), ev_40086 to ev_40107 (SB Energy, neocloud colleague, verified against the S-1/A text).
**Draft:** `research/drafts/cluster_de.json`: 21 entities, 7 relationships (5 exposure, 2 context), 2 projects, 9 events.
**Validation:** the draft passes every check ("All checks passed") when run with two in-memory workarounds, neither of which changes the draft: (1) `python3 -m pipeline.checks draft` currently crashes with `KeyError: 'id'` because `research/evidence/fulltext_hits.jsonl` (another sequence's working file) sits in the evidence directory with rows that have no `id`; (2) `data/register/entities.json` does not exist yet, so `ent_nvidia` is missing from the register and every relationship fails "from entity ent_nvidia does not exist". I did not create `ent_nvidia`. Both need a fix by the lead (see Open questions).

**Documents read (newest and fullest first).** SB Energy: S-1/A Amendment No. 3 filed 19 Nov 2026 (0001628280-26-075026; no 424B4 exists yet; it supersedes the S-1 of 1 Sept and the amendments of 4 and 21 Sept), its Exhibit 10.31 (executed Residual Value Guaranty, Building 1), 10.49, 10.50 and 10.51 (schedules of identical leases and guaranties). Nvidia: 8-K of 17 Aug 2026 and Ex. 99.1; 10-Q for the quarter ended 26 Jul 2026 and its **Exhibit 10.1, Form of Residual Value Guaranty**; Q2 and Q3 FY2027 CFO commentaries. Meta: final 424B5 of 28 Oct 2026, 8-K of 29 Oct 2026, 10-Q Q3 2026. KKR 10-Q Q3 2026 and Helix launch release (kkr.com); Vistra 10-Qs Q2 and Q3 2026; Brookfield Asset Management 10-K 2025, 8-Ks of 4 Feb, 2 Apr, 27 Jul and 6 Nov 2026; TeraWulf 8-K 14 Aug 2025; Oracle 10-Q Aug 2026.

---

## Guaranty terms (for the OpenAI-side record `rel_openai_gu_2026`)

Nvidia's 8-K said the agreement form would be filed with the July 2026 10-Q. It was: Exhibit 10.1 to the 10-Q (form, ev_100001 to ev_100004, ev_100049, ev_100050). SB Energy filed the **executed** Building 1 guaranty as Exhibit 10.31 to S-1/A No. 3 (ev_100008 to ev_100012) and a schedule of the eight identical ones (ev_100013). Schedules with the guaranteed minimum value (GMV) amounts are redacted in both.

| Term | What the documents say | Evidence |
|---|---|---|
| Parties | Guarantor NVIDIA Corporation; beneficiaries PORTS Building 1, LLC to PORTS Building 9, LLC (SB Energy subsidiaries, Delaware LLCs). Nine guaranties: Building 1 filed, Buildings 2 to 9 "substantially identical" except landlord, building, GMV schedule and GMV threshold | ev_100013, Ex. 10.31 |
| Tenant | VELA I Holdings, LLC (OpenAI affiliate). Tenant parent OpenAI Global, LLC has signed a joinder guaranteeing all tenant obligations | ev_100008, ev_100009 |
| Why Nvidia signs | Under a separate Letter Agreement between OpenAI OpCo, LLC and Nvidia. SB Energy: "We did not offer and do not owe any compensation to NVIDIA"; compensation is paid by OpenAI under a separate agreement, amount not disclosed | ev_100010, ev_40094 |
| What is covered | Lease plus the Power Affiliate's power purchase agreement and transmission commitment ("Project Agreements"). Nvidia: "limited to defined portions of lease and power payments and not the full cost of the site". SB Energy: GMV "is intended to cover debt principal, accrued interest, invested equity, targeted equity returns and committed transmission payments to AEP Ohio" | ev_100005, ev_40093 |
| Capacity | About 4.25 GW-IT across nine buildings of about 472 MW-IT each, out of 17 buildings and about 8.0 GW-IT on the campus | ev_30003, ev_30027, ev_100016, ev_100029 |
| Cap | Total liability across all Related Guaranties "shall not exceed $105,000,000,000" (form, ev_100001); "aggregate remedy cap is $105 billion" (ev_40090). SB Energy notes: guaranteed value $24,705,882 thousand per GW-IT (ev_100051); x 4.25 = $105.0 billion (analysis, consistent) | ev_100001, ev_40090, ev_100051 |
| Cap mechanics | Per guaranty Liability Cap = the then-applicable amount on Schedule II (redacted). Cap is reduced by amounts the landlord collects from the tenant's business interruption insurance and from the tenant parent; anything collected after Nvidia pays is turned over to Nvidia. Project Agreement Costs paid by Nvidia reduce the cap except in a redacted case | ev_100050, Ex. 10.1 s.8 and s.2(c) |
| Step-down | GMV "remains constant initially and subsequently declines" on a contractual schedule over each 20-year lease (ev_100014). Nvidia: exposure "builds over time as each building comes online, up to a maximum of $105 billion, and then declines" as OpenAI pays rent (ev_30024 context, ev_100007) | ev_100014, ev_100007 |
| Effectiveness | Each guaranty effective at the lease Commencement Date; no Covered Loss Amount is payable until the ready-for-service (RFS) conditions are met. Building by building; first expected 2028 (Nvidia fiscal 2029). At 30 Sept 2026 no lease had commenced | ev_30005, ev_100007, ev_100015 |
| Trigger | "Guarantor Trigger Event": (i) tenant Insolvency Default, or (ii) Monetary Default (failure to pay Project Agreement Costs after all cure periods including Nvidia's own cure right), where the landlord has the right to and intends to terminate the lease | ev_100002, ev_30009, ev_40091 |
| Payment | Covered Loss Amount = shortfall between GMV and amounts recovered by reletting or sale (formula redacted); discount rate redacted | Ex. 10.1 s.1(b), ev_30009 |
| Nvidia remedies | Verification period (length redacted) while paying certain costs; then elect: (A) assume the lease itself or through a designee, (B) require reletting, (C) sale process, (D) let the lease terminate, (E) defer up to one year while paying specified project agreement costs. Nvidia may cure tenant defaults but is not obliged to. The landlord cannot terminate before Nvidia elects. If a Nvidia designee assumes the lease the guaranty stays in place | ev_100012, ev_40096, Ex. 10.1 s.12 |
| Early costs | Project Agreement Costs in the first period after a trigger (six months per S-1/A) are paid first from the tenant's security deposit and debt service reserve account | ev_100049 |
| Landlord must chase OpenAI first | Landlord may enforce against Nvidia only while concurrently pursuing tenant insurance proceeds and "all commercially reasonable remedies against Tenant Parent" | ev_100050 |
| Subrogation | Nvidia waives and subordinates subrogation; it "shall look solely to Tenant and/or Tenant Parent for any recoupment". OpenAI has agreed to reimburse and indemnify Nvidia for any amount paid | ev_100003, ev_30008 |
| Collateral | None for Nvidia. Nvidia equipment on site ("Guarantor Property") is protected: landlord waives liens on it; lenders' non-disturbance agreements must preserve Nvidia's rights | Ex. 10.1 s.20 |
| Exclusivity | Premises must exclusively deploy Nvidia reference architecture for not less than 20 years from commencement | ev_100004 |
| Termination | Earliest of: tenant terminates the lease under its terms; payment in full of the Covered Loss Amount; tenant or tenant parent posts a bank guaranty, letter of credit or surety bond from a rated issuer; tenant or tenant parent reaches a rating (redacted); a rated replacement tenant; other redacted events; 20th anniversary of the Commencement Date | ev_100011, ev_40095, ev_30007 |
| Option on the other 3.78 GW-IT | Nvidia may guarantee Buildings 10 to 17 at its sole discretion; if it does not by a date certain, OpenAI must provide a replacement guarantor rated at least A- (S&P) or equivalent. Nvidia 8-K rounds to 3.8 GW; press release says 3.75 IT-GW | ev_40092, ev_100025, ev_30004, ev_30011 |
| Amendments | No amendment to the Project Agreements without Nvidia's consent; Nvidia is not bound by unapproved amendments | Ex. 10.1 s.16(c) |
| Governing law | New York | Ex. 10.1 s.14 |
| Payments to date | None | ev_30023 |
| Why it matters to SB Energy | "OpenAI is not currently an investment-grade tenant"; financeability of PORTS-Pike "depend[s] in significant part on the NVIDIA residual value guaranty" | ev_100024 |
| Covered project debt | None in place. Construction pending local approval and the power and financing arrangements (ev_100020). SB Energy targets up to 90% debt on $8 to $9 billion capex per building (ev_100019, ev_100018). Analysis: for nine buildings that implies about $65 to $73 billion of future debt; not entered as `covered_project_debt` because it is a target, not a sourced balance | ev_100018 to ev_100020 |

Classification note for the OpenAI-side record: the documents call it a residual value guaranty, but the trigger is tenant default, not asset value at a date, and the payment is GMV minus recovery. The wrong-way risk is specific to OpenAI. Treat as GU (with RV secondary) or RV by the colleague's choice; the cap is `contingent_max` = $105 billion with trigger "OpenAI tenant insolvency default or uncured monetary default with landlord intent to terminate, after RFS".

---

## Reconciliation table

| Claim | Nvidia side | Counterparty side | Result | Differences |
|---|---|---|---|---|
| SB Energy equity | "will invest $1.5 billion in SB Energy" (ev_30010, 8-K Ex. 99.1, 2026-08-17) | $3.0 billion in total (ev_40086): $1.5bn prepaid forward funded 17 Aug 2026 at 90% of IPO price (ev_40087); $1.5bn private placement at IPO price (ev_40088), lapses 15 May 2027 (ev_100023), needs IPO with at least $1.5bn primary proceeds (ev_100052) (S-1/A No. 3, 2026-11-19) | partial | Amount $1.5bn v $3.0bn; price terms only on SB Energy side; Nvidia does not disclose the prepaid forward |
| SB Energy guaranty (for the OpenAI colleague) | Cap $105bn, ~4.25 GW, nine phases, trigger on tenant default, option ~3.8 GW (ev_30001 to ev_30009, ev_10040, ev_30027) | Same cap and scope (ev_40089, ev_40090, ev_100001 executed form), option 3.78 GW-IT, $24.7bn per GW-IT (ev_100051), compensation paid by OpenAI (ev_40094) | reconciled (terms); option size 3.8 v 3.78 v 3.75 is rounding | Compensation to Nvidia disclosed only by SB Energy; amount undisclosed |
| Financing platforms (RV) | MOUs, over $500bn third-party capital, residual value support up to 25% per opportunity, preliminary (ev_30013 to ev_30016, ev_10045, ev_10046, ev_100006) | No SEC disclosure by Apollo, BlackRock, Blackstone, Brookfield, Goldman Sachs or KKR as of 2026-11-23; KKR quote inside Nvidia release only (ev_30017) | one_sided | n/a |
| Helix (LP) | "a founding investor in Helix" (KKR quote, ev_30017) | KKR: founding investor, participates in returns (ev_100030, ev_100031), >$10bn total commitments (ev_100054); Vistra 10-Q: KKR Helix C L.P., open-ended fund (ev_100032) | reconciled (existence); amount undisclosed on both sides | none |
| Brookfield AI Infrastructure Fund (LP) | "founding partner in the Brookfield Global AI Infrastructure Program" (ev_30074) | Commitments include Nvidia (ev_100034); "strategic limited partners, NVIDIA and the Kuwait Investment Authority" (ev_100038) | reconciled (existence); amount undisclosed in filings | Bloomberg reports $2bn (single source, not used) |
| Meta equity | "NVIDIA will invest $3 billion in Meta's equity offering" (ev_30076) | Nvidia, AMD, Broadcom "indicated an interest in purchasing up to an aggregate of $5.0 billion"; "not binding agreements or commitments to purchase" (ev_100039 to ev_100041) | contradicted (on binding) | Firm verb v non-binding indication; $3bn v share of $5.0bn; no closing evidence |

## Project table

| Project | Location | MW-IT | Status | Tenant, term | Financing | Nvidia link | Evidence |
|---|---|---|---|---|---|---|---|
| `proj_sb_energy_ports_pike_b1_9` PORTS-Pike Buildings 1 to 9 (covered) | Piketon, Pike County, Ohio (former DOE Portsmouth plant) | ~4,250 (9 x ~472) contracted; 0 energized | Pre-construction; pending local approval, power and financing; leases signed 17 Aug 2026, not commenced at 30 Sept 2026; first RFS expected 2028 | VELA I Holdings (OpenAI), parent guarantor OpenAI Global; 20-year NNN, four 5-year extensions, fixed yield-on-cost rent | None in place; target up to 90% debt of $8 to $9bn per building; interconnection credit support may exceed $6bn; AEP Ohio grid capex ~$5.1bn passed through | rel_openai_gu_2026 (guaranty), rel_sb_energy_eq_2026 | ev_40089, ev_100016, ev_100020, ev_100019, ev_100018, ev_100022, ev_100021, ev_100015 |
| `proj_sb_energy_ports_pike_b10_17` PORTS-Pike Buildings 10 to 17 (context) | same | ~3,780 contracted | Later phases to 2032 | Same tenant; floating yield-on-cost rent | None | Nvidia option only | ev_40092, ev_100025, ev_100029 |

Campus power: ~10 GW gross load (ev_100017), grid plus ~9.2 GW of new gas generation to be built and owned by a SoftBank affiliate outside SB Energy. Other SB Energy campuses (Milam County, OpenAI tenant; Cosmos, SoftBank tenant) have no Nvidia link and are not recorded. Lenders: no PORTS-Pike lender exists yet; SB Energy's planned corporate revolver ($3.0bn, Citibank agent, ev_40105) is the only lender recorded as depth 2. Owners: SoftBank (controlling, ev_100027), OpenAI (warrants), Nvidia (Class N after IPO). UCC search not done (SB Energy is a Texas corporation; PORTS landlords are Delaware LLCs; no lien expected before construction financing).

## AI cloud agreements: counterparties found

Nvidia's note ($36bn at 26 Jul 2026, ev_10035, ev_10039; renamed "neocloud agreements", $32bn at 25 Oct 2026, ev_30090) names no counterparty. Full-text searches (`"NVIDIA" "cloud services agreement"`, `"NVIDIA" "revenue share" "capacity"`, `"NVIDIA" "neocloud agreement"`, 2026) found these filers; all are neoclouds for the colleagues:

| Filer | Hit | Status |
|---|---|---|
| SharonAI Holdings (0002068385) | Master Cloud Services Agreement with Nvidia, up to $4.88bn, minimum revenue, resale to third parties: the closest match to Nvidia's description | Recorded by neocloud colleague (ev_40143 to ev_40149) |
| IREN (0001878848) | Nvidia cloud contract ~$3.4bn TCV, five years | Recorded by neocloud colleague (ev_40108, ev_40109) |
| Nscale plc (0002110365) | Nvidia master cloud services agreement; also residual value and guarantor hits | Recorded by neocloud colleague; residual value hit to check (c_veh_005) |
| Ionic Digital (0002007691) | NVIDIA with revenue share and residual value (S-1/A 13 Jul 2026) | Not read; candidate c_veh_006 |
| QumulusAI (0002084026) | NVIDIA with revenue share and capacity (S-1/A 14 May 2026) | Not read; candidate c_veh_007 |
| SpaceX (0001181412) | "Cloud Services Agreements" hit is with Anthropic, not Nvidia | Not a counterparty |

## Records written

| Id | Type | Status | Amounts (displayed) | Evidence |
|---|---|---|---|---|
| rel_sb_energy_eq_2026 | EQ | definitive, filed | headline $3.0bn (ev_40086, 2026-11-19); committed $3.0bn (ev_40086); funded $1.5bn (ev_40087, 2026-08-17); contingent n/a | reconciliation partial |
| rel_ai_financing_platforms_rv_2026 | RV | loi_or_framework, filed | headline not disclosed ($500bn is third-party capital, 25% is a ratio); others n/a | one_sided |
| rel_helix_lp_2026 | LP | definitive, company_announced | all not disclosed | reconciled (existence) |
| rel_brookfield_baiif_lp_2025 | LP | definitive, filed | all not disclosed | reconciled (existence) |
| rel_meta_eq_2026 | EQ | loi_or_framework, filed | headline $3.0bn (ev_30076, 2026-10-26); others n/a | contradicted |
| rel_microsoft_cx_2025 | CX | context | n/a | ev_30050, ev_30041 |
| rel_google_cx_2025 | CX | context | n/a | ev_100047 |

Type decisions. Platforms: RV, not GU, because Nvidia's words are "residual-value support for a portion of specific projects" (ev_10046), a value support, not a guarantee of a named obligation; one record, because no source gives terms per platform. Helix and Brookfield: LP, not EQ-SPV, because both are funds (Vistra: "open-ended investment fund", ev_100032; Brookfield: "strategic limited partners", ev_100038). Meta: the issuer is Meta Platforms itself (Class A common stock through forward sale agreements, initial forward price $622.91875, ev_100044, settlement by 19 Nov 2027, ev_100045; ~$24.9bn net proceeds, ev_100042), not a data center vehicle. Meta's commitment to Nvidia: "intends to expand the deployment" with no volume (ev_30077). Comparator in Meta's 10-Q: Meta's own residual value guarantees to its data center ventures, maximum $41.493bn at 30 Sept 2026 (ev_100046).

## Seeds

| Seed | Result | Reason |
|---|---|---|
| D1 Microsoft | modified | Co-investor with Nvidia in Anthropic (up to $5bn v Nvidia up to $10bn) and Anthropic's $30bn Azure commitment confirmed (ev_30050, ev_30041). No Nvidia capital to Microsoft. Neocloud offtake left to neocloud colleagues. Recorded as CX. |
| D2 Oracle | killed (for this release) | Oracle's 10-Q shows RPO of $664bn (ev_100048) but names no customer; no allowed source read here ties it to OpenAI, and no Nvidia capital, guarantee or financing to Oracle was found. No CX record created. |
| D3 Google, Amazon, Meta | modified | Google: backstop of Fluidstack leases at TeraWulf confirmed (ev_100047), CX comparator. Meta: not context but a direct Nvidia equity indication ($3bn, contradicted on binding) plus a sourced Meta RVG comparator ($41.493bn, ev_100046). Amazon: sales only (R3), no record. |
| E1 Stargate entities | modified | No Nvidia capital in Stargate entities found. Nvidia's capital in the SoftBank and OpenAI orbit went instead to SB Energy (SoftBank controlled): $3.0bn equity and the $105bn guaranty on OpenAI's leases. MGX: nothing found. |
| E2 Humain, UAE, European clouds | killed (as exposure) | Sales and partnerships only (R3 context list); no Nvidia financing, guarantee or investment found in filings or releases. Sovereign money appears instead as co-investor beside Nvidia (KIA in Helix and in Brookfield's fund, ev_100030, ev_100038). Korea: NAVER $1bn conditional investment is R3 c_r3_015 (not re-recorded here). |

## Consequences (summary of the five lenses)

Detail is in the draft. SB Energy: contagion (no unaffiliated data center tenants, ev_100026; an OpenAI failure hits SB Energy, its future lenders, Nvidia's stake and Nvidia's guaranty together); revenue quality (Nvidia cash funds a campus that must deploy only Nvidia systems for 20 years, ev_100004); signaling (Nvidia buying at 90% of the IPO price). Lender reliance: PORTS-Pike debt is not yet raised and SB Energy says its financeability depends on the guaranty (ev_100024). Platforms: lender reliance and collateral loop. Helix and Brookfield: revenue quality and signaling. Meta: revenue quality (equity alongside expanded Nvidia deployment).

## Not found

| Item | Where I looked | Result |
|---|---|---|
| SB Energy 424B4 | EDGAR filing list for CIK 0002133037 to 23 Nov 2026 | None; S-1/A No. 3 is newest |
| GMV schedule, discount rate, termination rating, Nvidia compensation | Ex. 10.1 (10-Q), Ex. 10.31, 10.51 | Redacted |
| PORTS-Pike project debt and lenders | S-1/A No. 3 debt description and exhibits | None in place |
| Nvidia amounts in Helix and Brookfield's fund | Nvidia 10-Q, CFO commentaries, KKR 10-Q, Vistra 10-Q, BAM 10-K, Brookfield 8-Ks | Not disclosed |
| Financing platform counterparty disclosures | EDGAR full text: "NVIDIA" with "memorandum of understanding", "financing platform", "residual value"; KKR 10-Q | None by the six firms |
| Meta: shares actually sold to Nvidia | Meta 8-Ks of 29 Oct, 5 Nov and 12 Nov 2026; Nvidia Q3 FY2027 release and CFO commentary | Not disclosed; Nvidia Q3 10-Q not yet filed |
| Oracle naming OpenAI | Oracle 10-Q Aug 2026, Q1 FY26 release | Not named |
| Stargate, MGX, Humain, UAE, EU, UK, Japan, India Nvidia capital | EDGAR full text `"Stargate" "NVIDIA"`, R3 newsroom crawl | None |

## Unconfirmed

- Nvidia committed $2 billion to Brookfield's AI infrastructure fund: Bloomberg, 17 Sept 2026, "according to investor documents" (single tier 2 source).
- Samsung $1 billion commitment to Helix: CNBC 29 Sept 2026 and a KKR release (KKR page renders empty through the cache; CNBC fetch 403).

## Needs quote

| Claim | Outlet | Date | URL |
|---|---|---|---|
| Nvidia Commits $2 Billion to Brookfield AI Infrastructure Fund | Bloomberg | 2026-09-17 | https://www.bloomberg.com/news/articles/2026-09-17/nvidia-committed-2-billion-to-brookfield-ai-infrastructure-fund |
| Brookfield Targets $10 Billion for AI Fund in Nvidia Pact | Bloomberg | 2025-11-19 | https://www.bloomberg.com/news/articles/2025-11-19/brookfield-targets-10-billion-for-ai-fund-in-nvidia-partnership |
| Samsung to inject $1 billion into Nvidia- and KKR-backed AI infrastructure firm | CNBC | 2026-09-29 | https://www.cnbc.com/2026/09/29/samsung-investment-nvidia-kkr-ai-helix-digital.html |
| KKR, Nvidia, Others Launch $10 Billion Data Center Company | The Information | 2026-06 | https://www.theinformation.com/briefings/kkr-nvidia-others-launch-10-billion-data-center-company |

## Domains added

None. kkr.com (used via go.kkr.com), brookfield.com, meta.com, sbenergy.com, microsoft.com were already listed.

## Domains to add

| Entity | Domain | Why |
|---|---|---|
| ent_helix | helixdi.com | Helix's own site, for later Helix investor disclosures |
| ent_vistra | vistracorp.com | Vistra releases on Helix (SEC filings used meanwhile) |

## Open questions

1. Check command: `research/evidence/fulltext_hits.jsonl` breaks `pipeline.checks draft` for every cluster (rows without `id`); move it out of `research/evidence/` or give rows ids. The register has no `ent_nvidia` yet.
2. Is the SB Energy $1.5bn prepaid forward inside Nvidia's non-marketable equity at 25 Oct 2026, or carried as a prepaid or receivable? Nvidia's Q3 FY2027 10-Q (not yet filed) should say.
3. Meta: did Nvidia buy at the 29 Oct 2026 closing, and how many shares? Upgrade `rel_meta_eq_2026` to completed only on a filing or 13F.
4. Is Nvidia's new $9.5bn "power and systems credit support guarantees" line (ev_30025) linked to the financing platforms, Helix or Brookfield? No source says.
5. OpenAI's fee to Nvidia for the guaranty (letter agreement with OpenAI OpCo, LLC): amount and form undisclosed; OpenAI-side colleague to look.
