# R7: Unattributed remainders of Nvidia's disclosed aggregates

**Computed on 23 November 2026. Section (2) and the seniority table in (4) were recomputed after Gate R critic round 2 against the register rebuilt after commit 141d92d (data/register/relationships.json: 92 records: 80 counted, 4 context, 8 remainders; 108 entities).** Revised after Gate R critic rounds 1 (findings 2, 7, 15, 16) and 2 (findings 1 and 10): see `research/gate_r/FIXES.md`.

Namespaces `agg` (ev_130001 to ev_130024) and `fixc` (ev_190001 to ev_190009, `research/evidence/fixc.jsonl`). Files: `research/drafts/nvidia_financials.json`, `research/drafts/lead_aggregates.json` (8 records, 8 filing events).

**One balance sheet date: 2026-10-25 (Q3 FY2027).** The Q3 FY2027 Form 10-Q was not filed by 2026-11-23 (EDGAR listing checked), so the sources are the 8-K of 2026-11-17: Exhibit 99.3 supplemental financial information (balance sheet, cash flow, fair value table, non-marketable roll forward) and Exhibit 99.2 CFO commentary (commitments, neocloud agreements, guarantees). All unaudited. The 2026-07-26 10-Q is the newest full set of notes and is used only for prior-period comparisons.

Method: remainder = disclosed aggregate minus named register items that belong in that aggregate at 2026-10-25. A named item is subtracted only if a source states a like-for-like figure for it: carrying value or cost for stakes, fair value for listed stakes, the cap for guarantees and backstops, the unfunded amount for commitments. Headlines, "up to" figures, initial order values and total contract values at signing are not subtracted; those items are listed as "named but not quantified". Every remainder is analysis and is excluded from totals (`aggregate_of` set, `to: ent_nvidia_unattributed`).

Validation: `python3 -m pipeline.checks draft research/drafts/lead_aggregates.json` now reports only `citations:` failures for ids written in the text of the register files themselves (entities.json, relationships.json, loops.json and others). Draft mode keeps only the evidence the draft uses and then scans every register file, so it fails for any draft. Run against a scratch register holding entities.json (with text ids masked) and evidence.json, the same draft prints "All checks passed". Negative components now ground.

## Nvidia financials (nvidia_financials.json)

| Key | Value | Date | Evidence | Note |
|---|---|---|---|---|
| shareholders_equity | $266,666M | 2026-10-25 | ev_130001 | |
| fcf_ttm | $148,574M | TTM to 2026-10-25 | ev_130016 ($34,902M FY26 Q4) + ev_130020 ($113,672M 9M FY27) | Nvidia's own FCF (CFO less capex less principal payments). Cross check: CFO 36,190 (ev_130017) + 122,675 (ev_130004); capex 1,284 (ev_130018) + 8,856 (ev_130006); principal payments 151 |
| revenue_ttm | $361,808M | TTM to 2026-10-25 | ev_130019 ($68,127M) + ev_130008 ($293,681M) | cross check 215,938 (ev_10136) + 293,681 - 147,811 (ev_130009) |
| cash_and_marketable_securities | $53,512M | 2026-10-25 | ev_130002 ($29,089M) + ev_130003 ($24,423M) | excludes marketable equity $44,219M (ev_130014) |
| total_guarantees_max | $118.0B | 2026-10-25 | ev_50044 | |
| total_equity_investments | $99B | 2026-07-26 | ev_10043 | only MD&A total; none given at 2026-10-25 |
| equity_purchases_9m | $58,100M | 9M to 2026-10-25 | ev_190001 | cash paid for equity securities (Q3 alone $15,696M) |
| non_marketable_net_additions_9m | $46,436M | 9M to 2026-10-25 | ev_190002 | roll forward of private stakes (Q3 alone $15,431M) |
| equity_sale_proceeds_9m | $9,493M | 9M to 2026-10-25 | ev_190003 | Q3 alone $2,253M (ev_60113) |
| non_marketable_equity_carrying_value | $61,650M | 2026-10-25 | ev_130010 | balance sheet line "Non-marketable securities" is $65,528M (ev_130015) |
| marketable_equity_fair_value | $48,888M | 2026-10-25 | ev_130011 ($38,372M L1) + ev_130012 ($10,516M L2) | balance sheet marketable equity $44,219M (ev_130014); rest in other assets |
| unfunded_equity_commitments | $20B | 2026-10-25 | ev_120011 | $5B rest of FY27, $11B FY28, $2B FY29, $2B FY30 |
| neocloud_agreements_max | $32B | 2026-10-25 | ev_50080 | takes effect only if neoclouds secure financing (ev_50081) |
| cloud_service_agreements | $28B | 2026-10-25 | ev_130013 | |
| data_center_leases_not_commenced | $74B | 2026-10-25 | ev_190004 | $63B due FY2032 and after |
| supply_commitments | $390B | 2026-10-25 | ev_130023 | |

### Bridge to Nvidia's own disclosures at 2026-10-25

| Nvidia's figure | Amount | Named and sized in the remainder records | Unattributed remainder |
|---|---|---|---|
| Private stakes, carrying value | $61.65B (ev_130010) | $2.68B (Nscale $1.18B, SB Energy $1.5B, at cost) | $58.97B |
| Public equity, fair value | $48.89B (ev_130011, ev_130012) | $48.33B (13F values at 2026-09-30) | $0.56B |
| Guarantees, maximum | $118.0B (ev_50044) | $105.86B (PORTS-Pike $105B, Nscale $0.86B) | $12.14B |
| Neocloud agreements, maximum | $32B (ev_50080) | $0 | $32B |
| Cloud service agreements | $28B (ev_130013) | $0 (CoreWeave, IREN, Nscale named, no remaining balance stated) | $28B |
| Unfunded equity commitments | $20B (ev_120011) | $3.5B (SB Energy $1.5B, NAVER $1B, Nscale $1B) | $16.5B |
| Data center leases not commenced | $74B (ev_190004) | $0 | $74B |
| Supply and capacity commitments | $390B (ev_130023) | $0 | $390B |
| Equity purchases, nine months | $58.1B (ev_190001) | flow, no remainder | |
| Net additions to private stakes, nine months | $46.4B (ev_190002) | flow, no remainder | |

Deviation from the brief: fcf_ttm and revenue_ttm are built from positive quarterly and nine-month figures (FY26 Q4 plus FY27 nine months) instead of CFO and capex with negative components, because negative components cannot ground. The CFO and capex figures are grounded and listed in the note.

## a. Non-marketable equity securities (private stakes), carrying value

| Item | Record | Amount | Evidence |
|---|---|---|---|
| Disclosed: non-marketable equity securities, carrying value | | $61,650M at 2026-10-25 | ev_130010 |
| less Nscale Series B (cost) | rel_nscale_eq_2025 | $399,999,964 | ev_80030 |
| less Nscale SAFE to Series C-3 (cost) | rel_nscale_eq_2025 | $300,000,000 | ev_40008 |
| less Nscale Series C-4 (cost) | rel_nscale_eq_2025 | $477,399,382 | ev_40009 |
| less SB Energy prepaid forward (funded 2026-08-17) | rel_sb_energy_eq_2026 | $1,500M | ev_40087 |
| **Remainder** (`funded`) | rel_unattributed_non_marketable_equity_2026_10_25 | **$58,973M** | |

Named but not quantified: OpenAI Series C ($30B committed, ev_120098; funded not disclosed), Anthropic Series G portion, and 27 other private stakes with no funded amount (Mistral, SSI, Thinking Machines, Reflection, Cohere, Crusoe, Lambda, Firmus, Together AI and others). Caveats: upper bound. Named items are at cost and the aggregate is at carrying value, which includes cumulative gross unrealized gains of $9.9B (ev_130021) and losses and impairments of $2.2B (ev_130022). Cost as a proxy for carrying value is analysis. Whether the SB Energy prepaid forward sits in this line is analysis. Analysis: if OpenAI's $30B was fully paid by 2026-10-25, the remainder would be about $29.0B. Excluded: Anthropic placement (closed 2026-11-20); Nscale convertible notes (debt); equity method LP interests (in the $65,528M balance sheet line, ev_130015, outside the $61,650M table).

## b. Publicly held equity securities, fair value

| Item | Record | Amount | Evidence |
|---|---|---|---|
| Disclosed: Level 1 publicly held equity (current and locked) | | $38,372M at 2026-10-25 | ev_130011 |
| Disclosed: Level 2 (warrants, convertible preferred) | | $10,516M at 2026-10-25 | ev_130012 |
| less Intel (13F 2026-09-30) | rel_intel_eq_2025 | $19,367M | ev_50021 |
| less SpaceX | rel_spacex_eq_2026 | $19,683M | ev_50031 |
| less CoreWeave | rel_coreweave_eq_2025 | $4,113M | ev_50019 |
| less Coherent | rel_coherent_eq_2026 | $2,242M | ev_50027 |
| less Synopsys | rel_synopsys_eq_2025 | $1,894M | ev_50023 |
| less Nokia | rel_nokia_eq_2025 | $739M | ev_50025 |
| less Nebius common | rel_nebius_eq_2024 | $281M | ev_50015 |
| less Generate Biomedicines | rel_generate_biomedicines_eq_2026 | $13M | ev_50029 |
| **Remainder** (`funded`, fair value) | rel_unattributed_marketable_equity_2026_10_25 | **$557M** | |

Named but not quantified at fair value (Level 2, register holds cost only): Marvell preferred $2.0B, Lumentum preferred $2.0B, Corning warrants $0.5B, Nebius pre-funded warrant $2.0B, IREN rights. Caveats: 13F covers only US-listed 13(f) securities (no warrants, private-placement preferred, convertible debt or non-US listings), and its date (2026-09-30) is 25 days before the balance sheet date. The remainder is neither an upper nor a lower bound. Analysis: the 13F common total ($48.3B) exceeds Level 1 ($38.4B) by about $10B, so some 13F positions are probably carried as Level 2 or were sold or repriced in October. Subtracting the Level 2 named items at cost would make the remainder negative. Conclusion: nearly all public equity is named. Excluded: $3,471M of debt convertible into a public company's equity (ev_50098), which is in marketable debt.

## c. Guarantees, maximum gross exposure

| Item | Record | Amount | Evidence |
|---|---|---|---|
| Disclosed: total maximum gross exposure | | $118.0B at 2026-10-25 | ev_50044 |
| less SB Energy credit support for OpenAI's PORTS-Pike leases | rel_openai_gu_2026 | $105.0B | ev_30024 |
| less Nscale Ward County lease guarantee | rel_nscale_gu_2025 | $860.34M | ev_40003 |
| **Remainder** (`contingent_max`) | rel_unattributed_guarantees_2026_10_25 | **$12.14B** | |

Composition: land, power and shell for neoclouds $3.5B (ev_30026) less Nscale, plus power and systems credit support $9.5B (ev_30025). Neither line names a partner. Named but not quantified: CoreWeave land, power and shell framework (letter of intent), Firmus credit support, SharonAI credit support. The remainder is an upper bound. Both sides count the SB Energy cap at its maximum, although no guaranty is effective before fiscal 2029. No payments have been made (ev_50045). Wrong-way risk: specific.

## d. Neocloud (formerly AI cloud) agreements

| Item | Record | Amount | Evidence |
|---|---|---|---|
| Disclosed: neocloud agreements, maximum commitment | | $32B at 2026-10-25 ($36B at 2026-07-26, ev_50079) | ev_50080 |
| **Remainder** (`contingent_max`) | rel_unattributed_neocloud_agreements_2026_10_25 | **$32B** (was $27.12B) | |

No named agreement has a disclosed Nvidia maximum, so nothing is subtracted. The SharonAI $4.88B was removed (critic finding 16): it is SharonAI's "up to" headline (ev_40144), and SharonAI's 10-Q says the arrangement does not specify a fixed aggregate contractual value (ev_40146), so it is not a like-for-like maximum. Named but not quantified: SharonAI, CoreWeave (residual capacity order, initial value $6.3B, ev_20001), Firmus (size not disclosed), IREN and Nscale (rentals whose line, this one or e, Nvidia does not state). The aggregate covers agreements where a neocloud buys Nvidia systems with financing, Nvidia commits to rent the capacity for about six years, the neocloud can sell it to third parties first, and revenue is shared; the commitments take effect only on financing and acceptance (ev_50081). The remainder is an upper bound on what is truly unattributed.

## e. Multi-year cloud service agreements

| Item | Record | Amount | Evidence |
|---|---|---|---|
| Disclosed: cloud service agreements (remaining commitment) | | $28B at 2026-10-25 ($29B at 2026-07-26, ev_10030) | ev_130013 |
| **Remainder** (`committed_total`) | rel_unattributed_cloud_service_agreements_2026_10_25 | **$28B** (was $17.1B) | |

Nothing is subtracted. Nvidia's figure is the remaining unpaid commitment, and no named rental has a stated remaining commitment at the same date. Removed: CoreWeave $6.3B (critic finding 2: the 8-K calls it the order form's "initial value", not a commitment balance, and neither side says the order sits in this aggregate), which alone would have given $23.4B; then, on the same test, IREN $3.4B ("total contract value" of a contract signed in May 2026, ev_40109) and Nscale $1.2B ("aggregate amount" of order forms with 12 to 48 month terms from July 2025, ev_40001), since neither side states what Nvidia has already paid. Named but not quantified: CoreWeave (residual capacity order and other MSA order forms), IREN, Nscale, hyperscaler rentals (Microsoft, Google), Lambda. The remainder is an upper bound on what is truly unattributed.

## f. Equity investment commitments (unfunded)

| Item | Record | Amount | Evidence |
|---|---|---|---|
| Disclosed: equity investment commitments | | $20B at 2026-10-25 ($25B at 2026-07-26, ev_10032) | ev_120011 |
| less SB Energy IPO private placement (second $1.5B, conditional on IPO by 2027-05-15) | rel_sb_energy_eq_2026 | $1.5B | ev_40088 |
| less NAVER placement (signed 2026-07-24, precondition met 2026-10-27) | rel_naver_eq_2026 | $1.0B | ev_30072 |
| less Nscale "NVIDIA Sale" (notes or non-voting shares, closing about 2026-11-16) | rel_nscale_fc_2026 | $1.0B | ev_40012 |
| **Remainder** (`committed_total`) | rel_unattributed_equity_investment_commitments_2026_10_25 | **$16.5B** | |

Basis check (critic round 1): each subtraction is an unfunded amount stated by a source at or before the date; all three were kept. Named but not quantified: the unfunded part of OpenAI's $30B, and Anthropic (the $10B November 2025 agreement and the $10.0B placement that closed 2026-11-20). The remainder is an upper bound. Analysis: the commitment schedule shows only $5B for the rest of FY2027, so the Anthropic $10B placement was at most partly committed at 2026-10-25. Nvidia counts commitments "subject to certain contingencies" (ev_120010), so I subtracted NAVER although its precondition was met two days after the date. Caveat: the Nscale sale may settle in convertible notes, which are debt until the IPO. Not commitments: IREN rights (an option), Meta and Wayve (letters of intent).

## g. Supply prepayments and capacity reservation advances

| Item | Record | Amount | Evidence |
|---|---|---|---|
| Disclosed prepaid supply balance at 2026-10-25 | | not disclosed (last: long-term $1,536M, ev_10147; short-term $2.0B, ev_10148; at 2025-10-26) | |
| Recorded instead: supply and capacity commitments | | $390B at 2026-10-25 ($279B at 2026-07-26, ev_10029) | ev_130023 |
| **Remainder** (`committed_total`, nothing attributed) | rel_unattributed_supply_and_capacity_commitments_2026_10_25 | **$390B** | |

A like-for-like subtraction cannot be defended here. Nvidia stopped disclosing prepaid supply after October 2025, and each named deal's paid part (an asset) cannot be separated from its unpaid part (inside the $390B). The named deals are listed only: Amkor (Nvidia says multiyear agreements total nearly $3 billion including prepayments, ev_30065; committed amount not attributable to Nvidia), KYEC $1.1B advance (ev_30062; paid part not stated), Corning (customer deposit by an unnamed customer; committed amount unknown), and Ibiden, Unimicron and SPIL (no amounts).

## h. Data center leases not commenced

| Item | Record | Amount | Evidence |
|---|---|---|---|
| Disclosed: data center leases not commenced | | $74B at 2026-10-25 ($0 rest of FY27, $1B FY28, $2B FY29, $4B FY30, $4B FY31, $63B FY32 and after) | ev_190004 |
| Earlier split at 2026-07-26: leases not commenced | | $25B | ev_10031 |
| Earlier split at 2026-07-26: leases not commenced "for third party" | | $20B | ev_10037 |
| **Remainder** (`committed_total`, type LB, secondary GU) | rel_unattributed_data_center_leases_2026_10_25 | **$74B** | |

Nvidia has signed long leases on its own credit for capacity it may pass to others. In October it says the leases have terms of up to twenty years (ev_190006), are expected to commence between Q4 FY2027 and FY2033 (ev_190007), and "We may assign some of these leases to third parties in the future" (ev_190005). In July it showed $20B separately as leases "for third party" that it expected to reassign (ev_190008) and warned that delays in completing assignments could leave it bearing the lease costs (ev_190009). The October table no longer splits own use from third party, so how much of the $74B is meant for others is not disclosed. Analysis: the line rose by $29B in one quarter against the July sum of $45B. No landlord or assignee is named, so nothing is subtracted. This is credit support in the sense of the mission statement: Nvidia's covenant stands behind buildings that other companies may occupy.

## Answers the seed register asks for (spec/03)

**(1) Share of Nvidia revenue from customers it also funded, backstopped or rented from: not computable.** Nvidia names no customer. In Q3 FY2027, three unnamed direct customers were 14%, 11% and 11% of revenue (ev_130024). Indirect customers explicitly include neoclouds and frontier labs. TTM revenue is $361,808M (nvidia_financials). The few sourced counterparty-side data points:

| Data point | Evidence |
|---|---|
| Crusoe: about $225M credit facility for Nvidia GPUs (the only Crusoe spend tied to Nvidia hardware) | ev_110025 |
| Anthropic: up to $120.5B to SpaceXAI for NVIDIA GPU compute into 2029 (indirect, through a third party) | ev_120047 |
| Nvidia CFO: each PORTS-Pike generation could be about $150B to $200B of Nvidia revenue (a projection, not purchases) | ev_50046 |
| Nvidia: one AI research and deployment company was a meaningful amount of revenue through cloud purchases (unnamed) | ev_50055 |

A share needs counterparty disclosures of Nvidia purchases by period. None of CoreWeave, Nebius, IREN, Nscale or the labs states one in a form that can be added up here.

**(2) How much of the headline total is legally binding today?** Computed on 2026-11-23 from display-eligible amounts with `pipeline.checks.independent_totals` on the register rebuilt after 141d92d (92 records: 80 counted, 4 context, 8 remainders; aggregates and CX excluded). The same figures are in `research/reports/R9_system_view.md`, Totals. Headline and binding amounts cover different sets of records, so no binding share is computed.

| Measure | Amount |
|---|---|
| Headline sum (30 relationships with an eligible headline) | $307.1B, plus GBP 2B for the UK programme (not converted) |
| of which guaranty and backstop figures announced | $117.0B (PORTS-Pike $105B, CoreWeave $6.3B initial value, SharonAI up to $4.88B, Nscale $0.86B) |
| of which announced, not binding or not followed by a disclosed agreement | $103.5B (OpenAI letter of intent $100B, Meta $3B, Wayve $0.5B) |
| of which other announced amounts (equity, rentals, prepayments, IREN option) | $86.6B |
| Committed total (binding, including funded; 20 relationships) | $70.0B |
| Cash paid where stated (16 relationships) | $32.3 billion; cost of what is still held $30.2 billion (14 relationships) |
| Committed, confirmed not yet paid | $1.0B (Nscale NVIDIA Sale) |
| Committed, paid portion not disclosed (5 relationships) | $36.7B (OpenAI $30B, IREN $3.4B, Nscale rental $1.2B, KYEC $1.1B, NAVER $1B) |
| Contingent maximum (3 relationships) | $107.4 billion, of which $105 billion is the PORTS-Pike cap, not in force before fiscal 2029, and $2.36 billion is in force (Nscale lease $0.86B, SB Energy placement $1.5B) |
| Gross exposure (lower bound: 50 relationships have unknowns) | $175.3 billion |

Caveats. Nvidia's own aggregates are larger than the named items in every line: see the bridge table above.

**(3) Announced, then shrunk, restructured or dropped**

| Relationship | What changed | Source |
|---|---|---|
| OpenAI $100B letter of intent (Sept 2025) | No definitive agreement disclosed; followed by (analysis; no source links them) $30B in the February 2026 round | rel_openai_eqc_2025, rel_openai_eq_2026 |
| PORTS-Pike backstop | Reported talks of up to $250B (needs quote) became a $105B cap | rel_openai_gu_2026 |
| AI cloud / neocloud agreements | $36B (Jul 2026) to $32B (Oct 2026), and now contingent on neocloud financing | ev_50079, ev_50080 |
| Equity investment commitments | $27B (Apr 2026), $25B (Jul), $20B (Oct) as amounts were funded | ev_10032, ev_120011 |
| Cloud service agreements | $30B to $29B to $28B; purpose shifted to R&D of open models | ev_10030, ev_130013 |
| SharonAI | "up to $4.88B" in the 8-K; the 10-Q says no fixed aggregate value | ev_40144, ev_40146 |
| SB Energy | $3.0B announced; $1.5B prepaid forward funded 2026-08-17, the other $1.5B payable only if the IPO closes by 2027-05-15 | rel_sb_energy_eq_2026 |
| Data center leases not commenced | $25B plus $20B "for third party" (Jul 2026) became one line of $74B (Oct 2026) | ev_10031, ev_10037, ev_190004 |
| Anysphere (Cursor) | Acquired by SpaceX 2026-08-14; consideration to Nvidia unknown | rel_anysphere_eq_2025 |
| Intel, Nokia, Synopsys | Stakes cut in Q3 2026 (13F) | ev_50021, ev_50025, ev_50023 |
| Arm, Recursion, SoundHound, Nano-X, Serve, WeRide, Applied Digital | Exited | register status terminated or completed |
| TuSimple | Left the 13F on delisting; whether still held is not disclosed | rel_tusimple_eq_2023 |

**(4) Where Nvidia sits in each counterparty's capital structure** (register `seniority`, aggregates and CX excluded; counted on 2026-11-23 with `python3 -c "import json,collections;R=json.load(open('data/register/relationships.json'));print(collections.Counter(r['seniority'] for r in R if not r.get('aggregate_of') and r['type_primary']!='CX'))"`)

| Seniority | Count | Relationships |
|---|---|---|
| common_equity | 48 | Intel, SpaceX, CoreWeave, Coherent, Synopsys, Nokia, Nebius, SB Energy, NAVER, Anthropic (2026 placement), Mistral, SSI, Thinking Machines, Reflection, Cohere, Crusoe x3, Lambda, Firmus x3, Together AI x3 and others |
| none | 7 | letters of intent and frameworks (OpenAI LOI, Wayve, Meta, Motif, RLWRLD, Upstage, UK programme) |
| preferred_equity | 5 | OpenAI Series C, Anthropic (2025 agreement), Nscale, Marvell, Lumentum |
| prepaying_buyer | 5 | Amkor, KYEC, IBIDEN, Unimicron, SPIL |
| warrants | 3 | Nebius pre-funded warrant, IREN rights, Corning |
| guarantor | 3 | OpenAI/SB Energy, Nscale lease, financing platforms (LOI) |
| contingent_buyer | 3 | CoreWeave residual capacity, SharonAI, Firmus |
| lessee | 3 | CoreWeave MSA, Nscale clusters, IREN |
| lp_interest | 2 | Helix, Brookfield BAIIF |
| unsecured_creditor | 1 | Nscale convertible notes |

Total 80. Meta moved to "none" (its seniority is none: a non-binding indication). The Corning customer deposit is a context record and is not counted; the CoreWeave land, power and shell framework is also a context record.

Analysis: Nvidia is never a secured creditor. Where it lends or guarantees, it ranks as an unsecured creditor, or as a guarantor with only escrow for recourse (Nscale $470M).

## Seeds

| Seed | Verdict | Reason |
|---|---|---|
| B10 Cloud service agreements aggregate | Modified | $28B at 2026-10-25 (ev_130013), down from $30B. The backstop-shaped part is disclosed separately as neocloud agreements ($32B). Named but not quantified: CoreWeave, IREN, Nscale (no remaining balance stated). Remainder $28B |
| F1 Non-marketable equity by period | Confirmed | $61,650M at 2026-10-25 (ev_130010), up from $47,898M (ev_10001); $1.8B impairment in Q3 (ev_50099). Remainder up to $59.0B; nine-month purchases of equity securities $58.1B (ev_190001), net additions $46.4B (ev_190002) |
| F2 Marketable equity | Confirmed | $48,888M Level 1 + Level 2 (ev_130011, ev_130012); 13F-named stakes explain almost all |
| F3 Multi-year cloud service agreements | Modified | Split into ordinary cloud service agreements and contingent neocloud backstops; see d and e |
| F4 Purchase obligations and prepaid supply | Modified | Supply and capacity commitments $390B (ev_130023). The prepaid balance has not been disclosed since 2025-10-26, so no attribution is possible |
| F5 Customer concentration | Confirmed, not attributable | 14/11/11% in Q3 FY27 (ev_130024); no customer named |
| F6 Guarantees | Confirmed | $118.0B maximum (ev_50044); $12.1B not tied to a named partner |

## Not found
- Q3 FY2027 Form 10-Q (not filed by 2026-11-23).
- Prepaid supply and capacity balances after 2025-10-26 (8-K exhibits and the three latest periodic filings).
- An MD&A total of equity investments at 2026-10-25.
- Funded amounts for OpenAI Series C and the Anthropic Series G portion.
- The split of the $74B data center leases between own use and third parties at 2026-10-25.
- Partners behind the $9.5B power and systems credit support and the $3.5B land, power and shell guarantees (other than Nscale).

## Unconfirmed
- Reported talks of a backstop of up to $250B for PORTS-Pike (tier 2, see R5); not used.

## Needs quote
None new.

## Domains to add / Domains added
None.

## Open questions
1. Lead: `pipeline.checks draft` scans every register file for text citations but keeps only the draft's evidence, so it cannot pass for any draft; limit `check_text_citations` to the draft (or keep the full evidence store) in draft mode.
2. When the Q3 FY2027 10-Q is filed: check whether Nvidia names any neocloud or power and systems partner, whether it gives a prepaid supply balance, and how SpaceX is classed (Level 1 or 2), which would explain the $10B gap between the 13F total and Level 1.
3. OpenAI Series C funded amount: this one figure moves the private-stake remainder by up to $30B.
4. Sections (2) and (4) were re-run on the register rebuilt after 141d92d (92 records); re-run again if counted records change.
5. How much of the $74B of leases not commenced is meant for third parties: ask at the 10-Q, which may restore the split.
