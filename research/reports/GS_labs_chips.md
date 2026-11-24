# Guarantee sweep: AI labs, SoftBank and SB Energy, chipmakers other than Nvidia

Prepared 24 November 2026. Namespace `gsl` (ev_250001 to ev_250075). Draft: `research/drafts/complex_labs_chips.json`: 27 complex links and 12 minimal depth 2 entities. `python3 -m pipeline.checks draft` prints "All checks passed". Every figure below is tier 1 (SEC filing or the company's own release) and display eligible.

Reused evidence: Anthropic 424B4 (ev_120044 to ev_120051, ev_120064, ev_120065, ev_120069), SpaceX 424B4 and 10-Q (ev_120075 to ev_120087), SB Energy S-1/A and the executed guaranty (ev_100008, ev_100009, ev_100050, ev_40098, ev_120025, ev_120034), CoreWeave (ev_20199, ev_20207, ev_20208), Nscale (ev_40029, ev_40030, ev_40040).

## Answer in one paragraph

Nvidia is not the only one doing this. **AMD** discloses the same toolkit as Nvidia: $8.5 billion of guarantees of unnamed partners' leases and debt, a $6,175 million commitment to buy cloud capacity nobody else buys, $13.3 billion of data center leases signed to pass to partners, and 160 million share warrants each to OpenAI and Meta. **Broadcom** now backstops its own customer's leases: about $29 billion (June 2026) plus about $43 billion (October 2026) of residual value support to financiers, and up to $42 billion of notes it will buy to fund the rent. That customer matches Anthropic. **Anthropic** itself guarantees its lease subsidiaries, up to $4.2 billion of developers' costs and a $500 million power contract. **SpaceX** guarantees $20.2 billion of xAI GPU lease payments to Valor. **SoftBank** guarantees about $2.9 billion of its own tenant's lease at SB Energy. **OpenAI** stands behind its PORTS-Pike and Milam County leases. The only links on capacity Nvidia also supports are the PORTS-Pike parent guaranty, OpenAI's CoreWeave contract, Anthropic's Nscale contract, Anthropic's Microsoft commitment and Dell's lease financing to Nscale.

## Every link found

"Same capacity" is yes when the supported site or contract, or the obligor's capacity, also carries Nvidia credit or demand support (or the contract is part of an Nvidia deal). "Company only" means the only Nvidia tie is equity in the company, listed in `nvidia_links` with `same_capacity_as_nvidia` false.

| Link id | Provider | Beneficiary | Obligor | Kind | Amount (field) | Trigger | Dates | Same capacity as Nvidia | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| cx_openai_vela_i_parent_guarantee_2026 | OpenAI (OpenAI Global, LLC) | SB Energy building subsidiaries | VELA I Holdings, LLC | parent_guarantee | Not disclosed; 17 leases, about 8.0 GW-IT, 20 years | Tenant fails to pay or perform | Leases signed 2026-08-17 | **Yes**: rel_openai_gu_2026, rel_sb_energy_eq_2026. Landlord must pursue OpenAI while calling on Nvidia | ev_100008, ev_100009, ev_100050, ev_40098, ev_120025, ev_120034 |
| cx_openai_orion_dc_parent_guarantee_2026 | OpenAI (OpenAI Global, LLC) | SB Energy (Milam County DC, LLC) | Orion DC I, LLC | parent_guarantee | Not disclosed; about 753 MW, 15 years | Tenant fails to pay or perform | 2026-01-09; Building 1 amended 2026-07-22 | Company only (rel_sb_energy_eq_2026) | ev_250055 to ev_250058 |
| cx_sb_energy_openai_share_option_or_warrant_2026 | SB Energy | OpenAI | OpenAI | share_option_or_warrant | Headline: fair value about $4.603 billion at issuance (ev_250061); about $2.3 billion at 2026-09-30 (ev_250062); 3,991,809 warrants | Vests on Milam financing or SB Energy value thresholds | 2026-01-09 to 2036-01-09 | Company only (rel_sb_energy_eq_2026) | ev_250060 to ev_250063 |
| cx_sb_energy_orion_dc_guarantee_2026 | SB Energy parent entity | Orion DC I (OpenAI) | SB Energy | guarantee (completion) | Not disclosed | Buildings not completed | 2026 | Company only | ev_250059, ev_250055 |
| cx_sb_energy_cosmos_guarantee_2026 | SB Energy parent entity | Cosmos noteholders and SoftBank tenant | SB Energy | guarantee (completion) | Not disclosed; notes $999.0 million (ev_250054) | Project not completed | May 2026 | Company only | ev_250073, ev_250054 |
| cx_softbank_cosmos_tenant_lease_guarantee_2026 | SoftBank (SoftBank Group Capital Limited) | SB Energy | SoftBank affiliate tenant | lease_guarantee | Maximum about $2.9 billion (ev_250052); rent about $2.5 billion (ev_250053) | Tenant default | 15 year lease; rent from 2026-12-11 or ready for service | Company only | ev_250051 to ev_250053 |
| cx_openai_coreweave_compute_contract_2025 | OpenAI | MUFG as agent for DDTL 3.0 lenders | CoreWeave | compute_contract | Headline up to $11.9 billion (ev_20199, 10-K 2026-03-02) | Contract payments service DDTL 3.0 | 2025-03-07, through October 2030 | **Yes**: rel_coreweave_bk_2025, rel_coreweave_eq_2025, rel_coreweave_lb_2023 | ev_20199, ev_20207, ev_20208 |
| cx_anthropic_nscale_compute_contract_2026 | Anthropic | Nscale | Nscale | compute_contract | Headline up to $44.6 billion (ev_120049, ev_40029) | Paid as capacity delivered; Nscale must seek GPU financing | 2026-08-25, into 2033 | **Yes**: rel_nscale_gu_2025, rel_nscale_lb_2025, rel_nscale_eq_2025, rel_nscale_fc_2026 | ev_120049, ev_40029, ev_40030, ev_250071 |
| cx_anthropic_microsoft_minimum_revenue_2025 | Anthropic | Microsoft | Microsoft | minimum_revenue | Headline $47.2 billion minimum, maximum up to $49.2 billion (ev_120044) | Usage short of minimum | Nov 2025; Nov 2026 to Jun 2033 | **Yes**: rel_anthropic_eqc_2025, rel_microsoft_cx_2025 (same November 2025 deal, Nvidia systems) | ev_120044, ev_250018, ev_120064, ev_120065 |
| cx_anthropic_google_minimum_revenue_2026 | Anthropic | Google | Google | minimum_revenue | Headline about $121.3 billion (ev_120045) | Shortfall paid as true-up | Mar 2026; Apr 2026 to Jul 2033 | No (TPU) | ev_120045, ev_250016 |
| cx_anthropic_amazon_minimum_revenue_2026 | Anthropic | Amazon | Amazon | minimum_revenue | Headline $110.0 billion (ev_120046) | Shortfall paid as true-up | Apr 2026; May 2026 to Apr 2036 | No | ev_120046, ev_250017 |
| cx_anthropic_lease_spvs_parent_guarantee_2026 | Anthropic, PBC | Broadcom (and assignees) | Anthropic lease subsidiaries | parent_guarantee | No cap stated; guaranteed rent about $161.2 billion (on the next row) | Subsidiary default | Five year leases | Company only (TPU capacity) | ev_250001 to ev_250004, ev_120051 |
| cx_broadcom_anthropic_vendor_financing_2026 | Broadcom | Anthropic | Anthropic lease subsidiaries | vendor_financing | Headline about $161.2 billion rent excluding interest (ev_120051) | Rent from ready for service | Five years; non-cancelable | Company only | ev_120051, ev_250001, ev_250002 |
| cx_broadcom_anthropic_credit_support_2026 | Broadcom | Lessors (Broadcom, financing SPVs) | Anthropic | credit_support | Maximum $42.0 billion (ev_250005, ev_250072); none drawn at 2026-09-30 | Anthropic elects to fund rent with notes | March 2026; five year draw period | Company only | ev_250005 to ev_250007, ev_250072 |
| cx_broadcom_anthropic_backstop_2026 | Broadcom | AI XPV financial partner | Customer's lease (analysis: Anthropic) | backstop | Maximum about $29 billion once all racks deployed (ev_250043); nothing paid (ev_250044) | Lease default: gap below 85% of amount owed after rack sale | June 2026; five years | Company only | ev_250041 to ev_250045, ev_250072, ev_250004 |
| cx_broadcom_anthropic_residual_value_guarantee_2026 | Broadcom | New special purpose vehicle | Customer's lease (analysis: Anthropic) | residual_value_guarantee | Maximum about $43 billion once deployed (ev_250047) | Lease default: gap below 72.5% of amount owed | 2026-10-26 | Company only | ev_250046 to ev_250048, ev_250003 |
| cx_amd_openai_share_option_or_warrant_2025 | AMD | OpenAI (OpenAI OpCo, LLC) | OpenAI | share_option_or_warrant | Up to 160 million shares at $0.01; no USD figure per warrant | First tranche after 1 GW of MI450; full at 6 GW; price targets to $600 | 2025-10-05 to 2030-10-05 | Company only | ev_250074, ev_250075, ev_250033 to ev_250037, ev_250029, ev_250032, ev_120029 |
| cx_amd_meta_share_option_or_warrant_2026 | AMD | Meta | Meta | share_option_or_warrant | Up to 160 million shares at $0.01 | Same structure, 1 to 6 GW equivalent | 2026-02-23 to 2031-02-23 | Company only (rel_meta_eq_2026) | ev_250038 to ev_250040, ev_250029, ev_250032 |
| cx_amd_commercial_partners_lease_guarantee_2026 | AMD | Partners' landlords | Unnamed commercial partners | lease_guarantee | Maximum $7.7 billion (ev_250021) | Partner lease default | Up to 15 years | Unknown partners | ev_250021, ev_250023 to ev_250025 |
| cx_amd_commercial_partners_guarantee_2026 | AMD | Partners' lenders | Unnamed commercial partners | guarantee (debt) | Maximum $750 million (ev_250022) | Partner loan default | Up to six months remaining | Unknown | ev_250022 to ev_250024 |
| cx_amd_cloud_providers_backstop_2026 | AMD | Unnamed cloud providers | Same | backstop | Maximum $6,175 million (ev_250027) | Capacity not bought by customers | 2026 to 2031 and after | Unknown | ev_250026, ev_250027 |
| cx_amd_commercial_partners_credit_support_2026 | AMD | Landlords | Unnamed commercial partners | credit_support | Headline $13.3 billion of lease payments (ev_250028) | Partners do not take or pay the subleases | From Q2 fiscal 2027, 10 to 15 years | Unknown | ev_250028 |
| cx_amd_anthropic_vendor_financing_2026 | AMD | Anthropic | Anthropic | vendor_financing | Maximum up to $5.0 billion (ev_250070); paid about $2.5 billion at 2026-11-20 (ev_250013) | Draws on AMD GPU delivery milestones | July 2026 | Company only | ev_250070, ev_250013 to ev_250015, ev_120069 |
| cx_anthropic_dc_developers_credit_support_2026 | Anthropic | Unnamed developers | Same | credit_support | Maximum up to $4.2 billion (ev_250008) | Lease not signed or no construction financing | Mostly under one year | Unknown | ev_250008, ev_250009 |
| cx_anthropic_dc_provider_guarantee_2026 | Anthropic | Power contract counterparty | Unnamed data center provider | guarantee | Maximum $500 million (ev_250011) | Provider fails to pay; written demand | To 2038-12-31 | Unknown | ev_250010 to ev_250012 |
| cx_spacex_spacexai_lease_guarantee_2025 | SpaceX | Valor | xAI lessee subsidiary | lease_guarantee | Headline $20,206 million: $6,986m + $6,633m + $6,587m (ev_120075 to ev_120077); lessee paid $885m in 2025 and $1,917m Jan to Apr 2026 (ev_250049, ev_250050); debt $12,897m at 2026-09-30 (ev_120085, ev_120086) | Lessee default | 2025 and 2026 | Company only (rel_spacex_eq_2026) | ev_120075 to ev_120078, ev_120085 to ev_120087, ev_250049, ev_250050 |
| cx_dell_financial_services_nscale_vendor_financing_2026 | Dell Financial Services | Nscale | Nscale | vendor_financing | Headline about $2.54 billion initial-term rent, 40 schedules (ev_40040) | Rent per schedule | April 2026 | **Yes**: Nscale links | ev_40040 |

Totals of the displayed maximums are not summed here: the Broadcom backstops, note facility and lease all sit on the same Anthropic leases, and the AMD $8.5 billion total (ev_250025) already contains the $7.7 billion and $750 million.

## Other chipmakers doing what Nvidia does

| Tool | Nvidia (register) | AMD | Broadcom |
|---|---|---|---|
| Lease guarantees for partners | $105.0 billion SB Energy guaranties (ev_30024) and $3.5 billion land, power and shell guarantees (ev_30026), plus $9.5 billion power and systems credit support (ev_30025); total $118.0 billion at 2026-10-25 (ev_50044) | $7.7 billion of data center lease guarantees, terms up to 15 years (ev_250021); $8.5 billion total with debt guarantees (ev_250025) | None for third parties; it backstops its own leases (next row) |
| Backstop of a customer's leases or residual value | Residual value guaranties at PORTS-Pike (ev_30001) | Not disclosed | About $29 billion (85% coverage, ev_250043) plus about $43 billion (72.5% coverage, ev_250047), both on its customer's AI rack leases |
| Debt guarantees | Not separately disclosed | $750 million, up to six months (ev_250022) | None found |
| Buying unsold cloud capacity | Up to $32 billion of neocloud agreements (ev_50080); CoreWeave order, initial value $6.3 billion (ev_20001) | $6,175 million of cloud compute capacity commitments (ev_250027) | None found |
| Leases on its own credit, to pass on | $74 billion not commenced (ev_190004) | $13.3 billion not commenced, to be assigned or subleased (ev_250028) | Not disclosed |
| Lending to fund purchases | Nscale notes, equity in OpenAI and Anthropic (register) | Up to $5.0 billion equity commitment to Anthropic tied to GPU deployment, $2.5 billion paid (ev_250070, ev_250013) | Up to $42 billion of convertible notes to fund the customer's rent (ev_250072); lessor of about $161.2 billion of equipment (ev_120051) |
| Share instruments | Receives warrants for guarantees: $4.8 billion notional (ev_50095) | **Gives** warrants to customers: up to 160 million shares each to OpenAI and Meta; liability $1.2 billion, unrecognized value $4.5 billion (ev_250030, ev_250031) | None |
| Named beneficiaries | OpenAI, Nscale, CoreWeave and others | Only OpenAI and Meta (warrants) and Anthropic; guarantee partners unnamed | Customer unnamed; matches Anthropic (analysis) |
| Payments made | None (ev_50045) | None (ev_250024) | None (ev_250044) |

Analysis: AMD copies Nvidia's credit toolkit at about a tenth of the size and pays its customers in its own shares, the reverse of Nvidia, which receives warrants. Broadcom's support is concentrated on one customer. Its two backstops plus the note facility total up to $114 billion of contingent support. That is about the same as Nvidia's $118.0 billion and sits on the Anthropic TPU capacity in which Nvidia owns equity. Both rivals' guarantees decline as the customer pays, and both may take over the lease after a default, as Nvidia may at PORTS-Pike.

## Found but not recorded as links (reason)

| Item | Figures | Why not a link | Evidence |
|---|---|---|---|
| OpenAI and Oracle (Stargate, 4.5 GW) | Partnership "exceeds $300 billion" over five years (ev_250064) | Purchase contract; no allowed source shows a lender relying on it or any guarantee behind Oracle's leases. Closes the crossref gap on the amount | ev_250064, ev_250065 |
| Anthropic and SpaceXAI | Up to $120.5 billion into 2029; cancellable on 90 days notice after January and March 2027 (ev_120047, ev_120048) | Cancellable purchase contract; no lender reliance shown | ev_120047, ev_120048 |
| Anthropic and Lambda | About $41.3 billion (ev_120050), of which about $34.9 billion is currently terminable by either party (ev_250019, ev_250020) | Fees accrue only on delivery; terminable | ev_120050, ev_250019, ev_250020 |
| Anthropic and AMD supply agreement | Expected spend above $20.0 billion (ev_250015) | No fixed commitment; recorded only AMD's equity commitment | ev_250015 |
| SpaceX and Apollo-managed lessor | About $40 billion principal, binding commitment letter, from H1 2027 (ev_120094, ev_120095) | SpaceX is the direct lessee; no third-party guarantee disclosed | ev_120094, ev_120095 |
| SoftBank bridge facility for OpenAI | USD 40.0 billion facility (ev_250066), USD 30.0 billion drawn (ev_250068), USD 25.9 billion prepaid on 2026-09-15 (ev_250069); unsecured (ev_250067) | SoftBank's own borrowing, no guarantee of another party stated; repaid | ev_250066 to ev_250069 |
| xAI and X loans guaranteed by subsidiaries | Subsidiary guarantees of group debt, repaid at the merger | Intra-group, extinguished | SpaceX 10-Q Note 9 (no new evidence) |
| Anthropic consolidated VIE guarantees | Anthropic guarantees certain VIE obligations; no maximum stated | No sized amount | 424B4 Note 7 (no new evidence) |
| OpenAI's Azure ($250 billion) and AWS ($38 billion) commitments | ev_120111, ev_120028 | Purchase contracts, no lender reliance | as cited |

## Parties searched with nothing found

- **Intel** 10-Q for Q3 2026: supplier prepayments only ($1.2 billion paid year to date), no customer guarantees or vendor financing for GPU buyers.
- **Micron** 10-K for fiscal 2026: guarantees only of its own subsidiaries and the Commerce Department agreement; nothing for customers. Micron bought Anthropic shares in the IPO (equity, not support).
- **TSMC**: no filing or release found with customer guarantees; TSMC Partners bought Anthropic shares (equity).
- **Super Micro** 10-Q for September 2026: no customer financing or guarantees; it states it does not guarantee Ablecom or Compuware obligations.
- **HPE** 10-Q for July 2026: HPE Financial Services is reported as one segment with no AI or GPU buyer split; no guarantees found.
- **Dell** 10-Q for July 2026: DFS funds leases and loans generally, not sized for AI; the only AI-specific item is the Nscale schedules.
- **AMD guarantee of Crusoe**: AMD names no partner. EDGAR full-text searches ("guaranteed by Advanced Micro Devices", "Advanced Micro Devices" "lease guarantee") returned nothing.
- **OpenAI guarantees for Oracle, Microsoft, AMD, Stargate sites other than SB Energy**: none disclosed by OpenAI, Oracle (10-Q for August 2026 names no customer) or Microsoft.
- **SoftBank guarantees for Stargate entities**: none in a US filing or an HTML SoftBank release. **SB Energy sponsor guarantees**: the S-1/A says project debt is non-recourse except "temporary limited sponsor guaranties" with no amounts.
- **SOAR AI**: a three-year revenue backstop of about $215 million on 4,096 AMD MI355X GPUs, provider not named in the 10-Q or release; not attributed.

## Unconfirmed

- AMD to backstop a $300 million Goldman Sachs loan to Crusoe for AMD chips in an Ohio data center (The Information, about 20 February 2026, single source; other copies are syndications). Consistent in kind with AMD's $750 million of unnamed partner debt guarantees, but not attributable.
- SoftBank's guarantee of a $10.0 billion SVF2 loan tied to OpenAI shares (August 2026). It appears only in SoftBank's Q2 FY2026 report and investor PDFs on group.softbank. The pipeline cannot extract text from these PDFs, so it is not quoted yet (see Needs quote).

## Needs quote

- SoftBank Group Corp., "Consolidated financial report for the six-month period ended September 30, 2026" (PDF), group.softbank/media/Project/sbg/sbg/pdf/ir/financials/financial_reports/financial-report_q2fy2026_01_en.pdf: SBG guarantee of the SVF2 $10 billion OpenAI-linked loan, Arm margin loan increase, $11.87 billion term loan. Tier 1, but the cached file is raw PDF.
- SoftBank Q2 FY2026 Investor Briefing (PDF), group.softbank/system/files/pdf/ir/presentations/2026/investor-presentation_q2fy2026_01_en.pdf: same items.
- The Information, "AMD to backstop $300 million Crusoe loan", about 2026-02-20 (paywalled; syndicated copies not usable).

## Domains added

None. group.softbank, softbank.jp, openai.com, anthropic.com, spacex.com, sbenergy.com and oracle.com were already listed. AMD, Broadcom and Dell were read only through SEC filings.

## Open questions

1. Broadcom's customer: the $42 billion note facility and the June and October lease assignments match Anthropic's 424B4. Broadcom does not name the customer, so the obligor on the two Broadcom backstops is analysis.
2. Who are AMD's commercial partners behind $8.5 billion of guarantees, $13.3 billion of leases and $6,175 million of capacity commitments? If any is a neocloud Nvidia also supports (Crusoe, for example), `same_capacity_as_nvidia` would change.
3. Does SpaceX's Valor equipment use Nvidia GPUs? The filings say "computing and related equipment".
4. PORTS-Pike rent and the OpenAI parent guaranty's size are not disclosed; Nvidia's GMV schedule is redacted.
5. Tooling: `pipeline.checks draft` on a file with `complex_links` writes every register relationship into the draft's `relationships` list. `reg.relationships` is the same list object as `d["relationships"]` and is extended in place, so the later filter keeps everything. I reset `relationships` to [] after the passing check. Other complex drafts (complex_hyperscalers, complex_neoclouds) may carry the same 92 copies. A fix in `pipeline/checks.py` (copy the list) is for the lead.
6. Dates given as the first of a month (Google, Amazon, AMD Anthropic, Dell, Broadcom NPA, Cosmos) stand for a month-only source date; the link notes say so.
