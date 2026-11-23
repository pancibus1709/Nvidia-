# R7: Unattributed remainders of Nvidia's disclosed aggregates

Namespace `agg`, new evidence ev_130001 to ev_130024 (`research/evidence/agg.jsonl`). Files: `research/drafts/nvidia_financials.json`, `research/drafts/lead_aggregates.json` (7 records, 7 filing events).

**One balance sheet date: 2026-10-25 (Q3 FY2027).** The Q3 FY2027 Form 10-Q was not filed by 2026-11-23 (EDGAR listing checked), so the sources are the 8-K of 2026-11-17: Exhibit 99.3 supplemental financial information (balance sheet, cash flow, fair value table, non-marketable roll forward) and Exhibit 99.2 CFO commentary (commitments, neocloud agreements, guarantees). All unaudited. The 2026-07-26 10-Q is the newest full set of notes and is used only for prior-period comparisons.

Method: remainder = disclosed aggregate minus named register items that belong in that aggregate at 2026-10-25, display-eligible amounts only, each subtraction a negative component grounded on the evidence stating the item's figure. Every remainder is analysis and is excluded from totals (`aggregate_of` set, `to: ent_nvidia_unattributed`).

**Tool limitation (blocks "All checks passed").** `pipeline.checks draft` fails with 21 grounding errors, one for every negative component: `pipeline/common.value_in_text` only matches positive numbers, so a subtraction such as -6.3e9 never matches "$6.3 billion". Re-running the same checks in memory with `evidence_contains(ev, abs(value))` gives "All checks passed" (no files edited). The one-line fix, in `pipeline/checks.py` `evidence_contains` (or in `check_grounding`/`supporting`), is to compare `abs(value)`. I did not edit `pipeline/`. For `nvidia_financials.json` I avoided negative components (see Deliverable 1), so all six amounts print True.

## Nvidia financials (nvidia_financials.json)

| Key | Value | Date | Evidence | Note |
|---|---|---|---|---|
| shareholders_equity | $266,666M | 2026-10-25 | ev_130001 | |
| fcf_ttm | $148,574M | TTM to 2026-10-25 | ev_130016 ($34,902M FY26 Q4) + ev_130020 ($113,672M 9M FY27) | Nvidia's own FCF (CFO less capex less principal payments). Cross check: CFO 36,190 (ev_130017) + 122,675 (ev_130004); capex 1,284 (ev_130018) + 8,856 (ev_130006); principal payments 151 |
| revenue_ttm | $361,808M | TTM to 2026-10-25 | ev_130019 ($68,127M) + ev_130008 ($293,681M) | cross check 215,938 (ev_10136) + 293,681 - 147,811 (ev_130009) |
| cash_and_marketable_securities | $53,512M | 2026-10-25 | ev_130002 ($29,089M) + ev_130003 ($24,423M) | excludes marketable equity $44,219M (ev_130014) |
| total_guarantees_max | $118.0B | 2026-10-25 | ev_50044 | |
| total_equity_investments | $99B | 2026-07-26 | ev_10043 | only MD&A total; none given at 2026-10-25 |

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
| less SharonAI, contract value of up to $4.88B | rel_sharonai_bk_2026 | $4.88B | ev_40144 |
| **Remainder** (`contingent_max`) | rel_unattributed_neocloud_agreements_2026_10_25 | **$27.12B** | |

Which agreements belong here (analysis). The aggregate covers agreements where a neocloud buys Nvidia systems with financing, Nvidia commits to rent the capacity for about six years, the neocloud can sell it to third parties first, and revenue is shared. The commitments take effect only on financing and acceptance (ev_50081). The category first appears in July 2026, and its schedule shows nothing payable in the rest of FY2027. SharonAI (order of 2026-06-08: six years, five phases, minimum revenue, revenue share) and Firmus (revenue-sharing and credit-support model) fit this description. CoreWeave's $6.3B residual capacity order (2025-09-09, under an existing MSA, running since 2025) does not, so it is placed in (e), as are IREN and Nscale. Caveat: SharonAI's 10-Q says the deal has no fixed aggregate value (ev_40146). Nvidia's figure is also a maximum, so the two are compared on the same basis, but this is analysis. Firmus is named but not quantified, so the remainder is an upper bound.

## e. Multi-year cloud service agreements

| Item | Record | Amount | Evidence |
|---|---|---|---|
| Disclosed: cloud service agreements | | $28B at 2026-10-25 ($29B at 2026-07-26, ev_10030) | ev_130013 |
| less CoreWeave residual capacity order (initial value) | rel_coreweave_bk_2025 | $6.3B | ev_20001 |
| less IREN five-year contract (total contract value, as of 2026-08-27) | rel_iren_lb_2026 | $3.4B | ev_40109 |
| less Nscale reserved clusters (aggregate, as of 2026-11-12) | rel_nscale_lb_2025 | $1.2B | ev_40001 |
| **Remainder** (`committed_total`) | rel_unattributed_cloud_service_agreements_2026_10_25 | **$17.1B** | |

Named but not quantified: other CoreWeave MSA order forms (only payments disclosed), hyperscaler rentals, Lambda (seed B5, no amount). Caveat: Nvidia reports the remaining unpaid commitment, while the named figures are contract values at signing. Subtracting them overstates attribution, and the unquantified items understate it, so the remainder is neither an upper nor a lower bound.

## f. Equity investment commitments (unfunded)

| Item | Record | Amount | Evidence |
|---|---|---|---|
| Disclosed: equity investment commitments | | $20B at 2026-10-25 ($25B at 2026-07-26, ev_10032) | ev_120011 |
| less SB Energy IPO private placement (second $1.5B, conditional on IPO by 2027-05-15) | rel_sb_energy_eq_2026 | $1.5B | ev_40088 |
| less NAVER placement (signed 2026-07-24, precondition met 2026-10-27) | rel_naver_eq_2026 | $1.0B | ev_30072 |
| less Nscale "NVIDIA Sale" (notes or non-voting shares, closing about 2026-11-16) | rel_nscale_fc_2026 | $1.0B | ev_40012 |
| **Remainder** (`committed_total`) | rel_unattributed_equity_investment_commitments_2026_10_25 | **$16.5B** | |

Named but not quantified: the unfunded part of OpenAI's $30B, and Anthropic (the $10B November 2025 agreement and the $10.0B placement that closed 2026-11-20). The remainder is an upper bound. Analysis: the commitment schedule shows only $5B for the rest of FY2027, so the Anthropic $10B placement was at most partly committed at 2026-10-25. Nvidia counts commitments "subject to certain contingencies" (ev_120010), so I subtracted NAVER although its precondition was met two days after the date. Caveat: the Nscale sale may settle in convertible notes, which are debt until the IPO. Not commitments: IREN rights (an option), Meta and Wayve (letters of intent).

## g. Supply prepayments and capacity reservation advances

| Item | Record | Amount | Evidence |
|---|---|---|---|
| Disclosed prepaid supply balance at 2026-10-25 | | not disclosed (last: long-term $1,536M, ev_10147; short-term $2.0B, ev_10148; at 2025-10-26) | |
| Recorded instead: supply and capacity commitments | | $390B at 2026-10-25 ($279B at 2026-07-26, ev_10029) | ev_130023 |
| **Remainder** (`committed_total`, nothing attributed) | rel_unattributed_supply_and_capacity_commitments_2026_10_25 | **$390B** | |

A like-for-like subtraction cannot be defended here. Nvidia stopped disclosing prepaid supply after October 2025, and each named deal's paid part (an asset) cannot be separated from its unpaid part (inside the $390B). The named deals are listed only: Amkor about $2.8B (two agreements, attribution to Nvidia is analysis), KYEC $1.1B advance (ev_30062), Corning $1.0B deposit (ev_60094), and Ibiden, Unimicron and SPIL (no amounts).

## Answers the seed register asks for (spec/03)

**(1) Share of Nvidia revenue from customers it also funded, backstopped or rented from: not computable.** Nvidia names no customer. In Q3 FY2027, three unnamed direct customers were 14%, 11% and 11% of revenue (ev_130024). Indirect customers explicitly include neoclouds and frontier labs. TTM revenue is $361,808M (nvidia_financials). The few sourced counterparty-side data points:

| Data point | Evidence |
|---|---|
| Crusoe: about $225M credit facility for Nvidia GPUs (the only Crusoe spend tied to Nvidia hardware) | ev_110025 |
| Anthropic: up to $120.5B to SpaceXAI for NVIDIA GPU compute into 2029 (indirect, through a third party) | ev_120047 |
| Nvidia CFO: each PORTS-Pike generation could be about $150B to $200B of Nvidia revenue (a projection, not purchases) | ev_50046 |
| Nvidia: one AI research and deployment company was a meaningful amount of revenue through cloud purchases (unnamed) | ev_50055 |

A share needs counterparty disclosures of Nvidia purchases by period. None of CoreWeave, Nebius, IREN, Nscale or the labs states one in a form that can be added up here.

**(2) How much of the headline total is legally binding today?** Computed from display-eligible amounts with `pipeline.checks.Register` (81 counted relationships, aggregates and CX excluded):

| Measure | Amount |
|---|---|
| Headline sum (30 relationships with an eligible headline) | $308.1B |
| Committed total (binding, including funded) | $75.2B |
| of which funded | $32.2B |
| Contingent maximum (guarantees, backstops) | $112.2B |
| Gross exposure (funded + committed unfunded + contingent) | $187.4B, a lower bound (49 relationships have unknowns) |
| Headline under letters of intent only (OpenAI $100B, Meta $3B, Wayve $0.5B) | $103.5B, not binding |

So about $75B is a binding commitment, a further $112B is binding but contingent, and about a third of the headline total is letters of intent. Analysis: $105B of the contingent amount is the SB Energy cap, which does not take effect before fiscal 2029.

**(3) Announced, then shrunk, restructured or dropped**

| Relationship | What changed | Source |
|---|---|---|
| OpenAI $100B letter of intent (Sept 2025) | No definitive agreement; replaced in practice by $30B in the February 2026 round | rel_openai_eqc_2025, rel_openai_eq_2026 |
| PORTS-Pike backstop | Reported talks of up to $250B (needs quote) became a $105B cap | rel_openai_gu_2026 |
| AI cloud / neocloud agreements | $36B (Jul 2026) to $32B (Oct 2026), and now contingent on neocloud financing | ev_50079, ev_50080 |
| Equity investment commitments | $27B (Apr 2026), $25B (Jul), $20B (Oct) as amounts were funded | ev_10032, ev_120011 |
| Cloud service agreements | $30B to $29B to $28B; purpose shifted to R&D of open models | ev_10030, ev_130013 |
| SharonAI | "up to $4.88B" in the 8-K; the 10-Q says no fixed aggregate value | ev_40144, ev_40146 |
| Anysphere (Cursor) | Acquired by SpaceX 2026-08-14; consideration to Nvidia unknown | rel_anysphere_eq_2025 |
| Intel, Nokia, Synopsys | Stakes cut in Q3 2026 (13F) | ev_50021, ev_50025, ev_50023 |
| Arm, Recursion, SoundHound, TuSimple, Nano-X, Serve, WeRide, Applied Digital | Exited | register status terminated or completed |

**(4) Where Nvidia sits in each counterparty's capital structure** (register `seniority`, aggregates and CX excluded)

| Seniority | Count | Relationships |
|---|---|---|
| common_equity | 48 | Intel, SpaceX, CoreWeave, Coherent, Synopsys, Nokia, Nebius, SB Energy, NAVER, Anthropic (2026 placement), Mistral, SSI, Thinking Machines, Reflection, Cohere, Crusoe x3, Lambda, Firmus x3, Together AI x3, Meta (LOI) and others |
| preferred_equity | 5 | OpenAI Series C, Anthropic (2025 agreement), Nscale, Marvell, Lumentum |
| warrants | 3 | Nebius pre-funded warrant, IREN rights, Corning |
| unsecured_creditor | 1 | Nscale convertible notes |
| guarantor | 3 | OpenAI/SB Energy, Nscale lease, financing platforms (LOI) |
| contingent_buyer | 3 | CoreWeave residual capacity, SharonAI, Firmus |
| lessee | 3 | CoreWeave MSA, Nscale clusters, IREN |
| prepaying_buyer | 6 | Amkor, KYEC, Corning, Ibiden, Unimicron, SPIL |
| lp_interest | 2 | Helix, Brookfield BAIIF |
| none | 7 | letters of intent and frameworks (OpenAI LOI, CoreWeave land/power/shell, Wayve, Motif, RLWRLD, Upstage, UK programme) |

Analysis: Nvidia is never a secured creditor. Where it lends or guarantees, it ranks as an unsecured creditor, or as a guarantor with only escrow for recourse (Nscale $470M).

## Seeds

| Seed | Verdict | Reason |
|---|---|---|
| B10 Cloud service agreements aggregate | Modified | $28B at 2026-10-25 (ev_130013), down from $30B. The backstop-shaped part is disclosed separately as neocloud agreements ($32B). Named: CoreWeave, IREN, Nscale ($10.9B). Remainder $17.1B |
| F1 Non-marketable equity by period | Confirmed | $61,650M at 2026-10-25 (ev_130010), up from $47,898M (ev_10001); $1.8B impairment in Q3 (ev_50099). Remainder up to $59.0B |
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
- Partners behind the $9.5B power and systems credit support and the $3.5B land, power and shell guarantees (other than Nscale).

## Unconfirmed
- Reported talks of a backstop of up to $250B for PORTS-Pike (tier 2, see R5); not used.

## Needs quote
None new.

## Domains to add / Domains added
None.

## Open questions
1. Lead: fix negative-component grounding (`abs(value)` in `pipeline/checks.py` `evidence_contains`), then rerun `python3 -m pipeline.checks draft research/drafts/lead_aggregates.json`.
2. When the Q3 FY2027 10-Q is filed: check whether Nvidia names any neocloud or power and systems partner, whether it gives a prepaid supply balance, and how SpaceX is classed (Level 1 or 2), which would explain the $10B gap between the 13F total and Level 1.
3. OpenAI Series C funded amount: this one figure moves the private-stake remainder by up to $30B.
4. Re-run R7 if a researcher adds relationships from the filings sweep (the register had 83 when this was computed).
