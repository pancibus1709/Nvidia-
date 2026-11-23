# R5 · Cluster B neoclouds: Nscale, Nebius, IREN, SharonAI, Applied Digital

Draft: `research/drafts/cluster_b_neoclouds.json` (17 entities, 10 relationships, 11 projects, 17 events). `python3 -m pipeline.checks draft` prints "All checks passed"; every non-null amount is display eligible (all tier 1). Prepared 23 November 2026. Excludes SB Energy (colleague) and CoreWeave (done).

Evidence reused: ev_40001 to ev_40155 (neo), ev_10xxx (R1), ev_30xxx (R3), ev_50012 to ev_50015 and ev_50045, ev_50074 (R1b 13F and filings). New evidence in namespace `neob`: ev_80001 to ev_80039 (39 records; ev_80037 superseded by ev_80039, see below). "Analysis" marks my inference.

## 1. Reconciliation table

| Relationship | Type | Headline | Committed | Funded | Contingent max | Nvidia side | Counterparty side | Result | Differences |
|---|---|---|---|---|---|---|---|---|---|
| rel_nscale_gu_2025 Ward County lease guarantee | GU | $860.34m (ev_40003, ev_40046, ev_10159) | n/a | Not disclosed (no guarantee payments to date, ev_50045) | $860.34m, trigger: Nscale fails to pay the lease in its first five years | 10-Q Q3 FY26: one partner, $860m, $470m escrow, for warrants, partner unnamed (ev_10159, ev_10160, ev_50074, ev_10161) | S-1/A 2026-11-12 (ev_40003, ev_40046, ev_40004) | reconciled | $860m rounded vs $860,340,000; Nvidia does not name Nscale (identification by matching amount, escrow, warrants and quarter is analysis); Nvidia cites a capacity sale agreement as mitigant, Nscale does not |
| rel_nscale_lb_2025 NVIDIA MSA | LB | $1.2bn (ev_40001) | $1.2bn (ev_40001) | Not disclosed | n/a | No disclosure found as of 2026-11-23 | S-1/A (ev_40001, ev_40002) | one_sided | n/a |
| rel_nscale_eq_2025 Series B, SAFE to C-3, C-4 | EQ | $1,177,399,346.78 (components ev_80030, ev_40008, ev_40009) | same | same, 2025-10-08 and 2026-03-27 | n/a | No disclosure found | S-1/A RPT tables (ev_80030, ev_80031) | one_sided | n/a |
| rel_nscale_fc_2026 2028 Convertible Loan Notes | FC (EQ secondary) | $2.0bn (ev_80019) | $2.0bn ($1.0bn ev_40011 + NVIDIA Sale $1.0bn ev_40012) | $1.0bn (ev_40011, issued ev_80021) | n/a | No disclosure found | S-1/A (ev_40011, ev_40012, ev_80019, ev_80020) | one_sided | n/a |
| rel_nebius_eq_2024 13F common stake | EQ | Not disclosed | n/a | Not disclosed (cost) | n/a; market value $280,809,479 at 2026-09-30 (ev_50015, Nvidia 13F) | 13F (ev_50014, ev_50015), 13G (ev_40051) | No disclosure found | one_sided | n/a |
| rel_nebius_eq_2026 pre-funded warrant | EQ | $2.0bn (ev_30052, ev_40060) | $2.0bn (ev_40055, ev_40057) | $2.0bn, 2026-03-11 | n/a | Release ev_30052; 13G ev_40051, ev_40053 | ev_40055, ev_40056, ev_40057 | reconciled | Warrant shares 21,065,936 (13G) vs 21,065,396 (20-F note, ev_40058), likely a typo |
| rel_iren_lb_2026 cloud services contract | LB | $3.4bn (ev_40109) | $3.4bn (TCV of signed contract) | Not disclosed | n/a | No disclosure found; Nvidia's IREN release covers only the share right | 10-K FY2026 (ev_40108 to ev_40110) | one_sided | n/a |
| rel_iren_eq_2026 Investment Rights | EQ (warrants) | $2.1bn (ev_30045, ev_40113) | n/a (right, not obligation) | Not disclosed (no exercise reported) | n/a | Release ev_30043 to ev_30045 | 10-K ev_40111 to ev_40114 | reconciled | Conditions: "regulatory" vs vesting with up to 600,000 GPUs plus regulatory; IREN capitalised $793.4m fair value into Nvidia GPU cost (ev_40115), no Nvidia disclosure |
| rel_sharonai_bk_2026 Master Cloud Services Agreement | BK (LB secondary) | $4.88bn "up to" (ev_40144) | Not disclosed | Not disclosed | Not disclosed; trigger: reserved capacity not sold to third parties | No disclosure of the agreement; Australia release names Sharon AI as partner (ev_80029) | 8-K, 10-Q (ev_40143 to ev_40149, ev_80015, ev_80016) | one_sided | SharonAI's own documents differ: "up to $4.88bn" (8-K) vs "no fixed aggregate contractual value" (10-Q, ev_40146) |
| rel_applied_digital_eq_2024 (exited) | EQ | Not disclosed | n/a | Not disclosed (about $25.0m, analysis: 7,716,050 x $3.24) | n/a | 13F 2024-09-30 to 2025-09-30 (ev_50012, ev_50013) | 8-K PIPE (ev_40138, ev_80026), 424B3 (ev_40136) | reconciled | None |

## 2. Classification decisions

- **Nscale equity split in two records.** Preferred shares (Series B $400.0m, SAFE $300m into C-3, C-4 $477.4m) are one EQ record with components: same company, same class, all for cash. The convertible loan notes are a separate FC record (EQ secondary, seniority unsecured_creditor): they are debt until the IPO, mature 2028-06-15, accrue 2% rising to 5.5%, and rank behind the secured GPU and project facilities. The NVIDIA Sale ($1.0bn, closing "on or around" 2026-11-16) is in committed, not funded, until closing is confirmed.
- **Nscale warrants** (Non-Default $60.0m value, Default $11.3m fair value) are consideration for the guarantee, not cash, so they sit in the GU record's notes and collateral, not in any amount.
- **Nscale GU.** contingent_max = $860.34m gross; the $470.0m escrow is in `credit.collateral` (net about $390m, analysis). funded left null (Nvidia says no guarantee payments made, but the statement holds no number to ground a zero). maturity null: five years from lease commencement, which is not disclosed. covered_project_debt = $1.85bn Ward County GPU Facility commitments (equipment at the guaranteed site, not the lease; labelled).
- **Nebius split in two records.** The 13F common stake (1,190,476 shares, since Q4 2024) and the March 2026 pre-funded warrant are distinct transactions, and the 13F market value covers only the common shares (warrants are not 13F securities). Putting $280.8m on the warrant record would mislabel it. Warrant: seniority warrants, funded $2.0bn; market_value Not disclosed.
- **IREN Investment Rights: EQ with seniority warrants, not EQ-C.** Nvidia holds a right it alone can trigger; it cannot be required to pay. Headline $2.1bn; committed and contingent not applicable; funded unknown. No Nvidia cash is at risk before exercise. The rights were granted as consideration alongside GPU supply (IREN capitalised $793.4m into GPU cost), a revenue-quality point, not an exposure.
- **IREN and Nscale LB committed_total** = total contract value of signed agreements ($3.4bn, $1.2bn). Termination rights are not disclosed; flagged in notes.
- **SharonAI: BK, LB secondary, seniority contingent_buyer, wwr specific.** SharonAI calls Nvidia a customer, but Nvidia has "little to no access" to the capacity unless it is not sold to third parties, minimum revenue applies, and SharonAI itself calls the structure "revenue-sharing and credit-support". Committed and contingent are Not disclosed; only the "up to $4.88bn" headline is recorded.
- **Applied Digital:** status completed (exited), wwr none, history only; exit quarter Q4 calendar 2025 inferred from 13F lists.

### Grades (spec/05 section 5, applied literally)

| Entity | Sourced columns | Grade | Reason |
|---|---|---|---|
| Nscale | Top customer 52% (Watch); 24m maturities/cash at least 0.94 (Adequate) | **Distressed** | Audited notes: forecast reliance on uncommitted financing "initially raised substantial doubt" about going concern (ev_40045), later alleviated by management's plan to cut capex. Going-concern language maps to Distressed. |
| Nebius | 24m maturities/cash 0.02 (Strong); top customer 33% (Adequate) | Adequate | Weakest column; the going-concern wording is the standard basis-of-preparation sentence with no doubt raised. |
| IREN | 24m maturities/(cash+undrawn) at least 0.27 (Strong); top customer 28% (Adequate) | Watch | Adequate moved down one step: commitments $18,947m are about 2.8x cash plus undrawn $6,679m; top three customers 70%. |
| SharonAI | 24m maturities/cash about 0 (Strong) | **Distressed** | Literal: the 10-Q has a going-concern section whose conclusion rests on management's discretion to delay expansion if financing fails (ev_80009, ev_80010). It does not say "substantial doubt"; this is the borderline case. |
| Applied Digital | none | Insufficient information | Exited; no credit work. |

## 3. Seeds

| Seed | Result | Reason |
|---|---|---|
| B6 Nebius | **Confirmed and extended** | 13F holding of 1,190,476 shares since 2024-12-31 (ev_50014, ev_50015); plus a $2.0bn pre-funded warrant over 21,065,936 shares (ev_40055, ev_40053); 13G 9.3% (ev_40052). No Nvidia backstop, rental or guarantee found. |
| B8 Nscale | **Modified** | Series B participation confirmed with cash: 63,177,840 shares for $399,999,964.32 on 2025-10-08 (ev_80030, ev_80032). This was missed by the earlier neo pass and by R1_named. The relationship is much wider than the seed: Series C $777.4m, $2.0bn of convertible notes, an $860.34m lease guarantee and a $1.2bn capacity rental. "UK projects": the MSA covers UK, Iceland and Norway capacity; Stargate UK is context only (OpenAI withdrew in April 2026). |
| B9 Applied Digital and others in 13F | **Confirmed (Applied Digital)** | 7,716,050 shares from the September 2024 PIPE, on 13F 2024-09-30 to 2025-09-30, absent at 2025-12-31. Other past 13F names (Arm, Recursion, WeRide etc.) belong to the portfolio cluster. |

## 4. Still "Not confirmed" or "Not disclosed"

No amount in the draft is "Not confirmed". Not disclosed: Nvidia's payments under the Nscale MSA and IREN contract; Nscale guarantee lease commencement, landlord, MW and rent; cost of the Nebius 13F stake; Nebius warrant market value; IREN rights exercise status beyond 2026-11-05; SharonAI minimum revenue amount and maximum Nvidia payment; SharonAI customer concentration; drawn balances of Nscale's facilities; 12-month committed spend for all four live counterparties (so liquidity cover is not computable for any); GPU depreciation life for IREN and SharonAI; whether the NVIDIA Sale closed.

## 5. Evidence notes

- IREN debt table: ev_40132 to ev_40135 had no machine-checked value. Replaced by ev_80001 (total $10,041m), ev_80002 (current $950m), ev_80003 and ev_80004 (FY27 remainder $723m and FY28 $1,059m, one record per figure), ev_80005 (Dec 2033 notes $3,000m), all with `--scale-anchor "in USD millions"`.
- ev_80037 was created during the inline-XBRL rendering fault (its scale locator pointed at the wrong text); re-created as ev_80039 and used instead. ev_80037 is unused.
- Draft entities overlapping other clusters (ent_microsoft, ent_meta, ent_anthropic, ent_jpmorgan, ent_goldman_sachs, ent_mufg, ent_citigroup) use the names, depth and tickers already in cluster_de / cluster_b_coreweave / cluster_b_private; descriptions are cluster-neutral. The lead should reconcile depth for ent_anthropic (depth 2 in cluster_b_private, depth 1 here because Nvidia invests in it).

## Not found
- Nscale: per-facility drawn amounts, Ward County lease MW/rent/landlord, whether Nvidia is the 73% FY2025 customer, NVIDIA Sale closing (searched S-1/A; check the 424B4 when filed).
- Nebius: how Nvidia acquired the 1,190,476 shares and at what price (20-F FY2025, Q3 6-K: not described).
- IREN: exhibit text of the Nvidia cloud contract and securities purchase agreement; which of Customers A to C is Nvidia; GPU useful life (10-K and 10-Q searched).
- SharonAI: customer concentration table; minimum revenue schedule (10-Q, 8-K, Ex. 99.1 searched).
- Nvidia side: no Nvidia filing names Nscale, IREN's cloud contract or SharonAI's agreement (R1, R1_named, R3 sources).

## Unconfirmed
- None new. (Lambda, Crusoe and others remain as listed in R5R6_neoclouds.md.)

## Needs quote
- None: no tier 2 sources used.

## Domains to add / Domains added
- Added to `config/sources_allowlist.json` under `tier1.company_domains`: `ent_sharonai` → sharonai.com (SharonAI's official site, for its investor releases); `ent_applied_digital` → applieddigital.com (official site). No evidence uses them yet; all evidence is sec.gov or nvidianews.nvidia.com.

## Open questions
1. Grading: should a going-concern section that concludes "no doubt" but rests on management discretion (SharonAI) count as going-concern language? Applied literally here as Distressed. Same question for Nscale, where doubt was raised and then alleviated.
2. Is Nvidia Nscale's unnamed largest customer (73% FY2025, 52% H1 2026)? The MSA timing fits.
3. Does the Ward County leased capacity serve the NVIDIA MSA, or other customers (Nvidia's 10-Q says the partner agreed to sell the capacity, ev_10161)?
4. Is the IREN "$3.4 billion managed services AI cloud contract" served by Dell GPUs at Childress the Nvidia contract (values match)?
5. Are the IREN, Nscale and SharonAI agreements inside Nvidia's $32bn neocloud agreements aggregate (ev_50080), and the Nscale guarantee inside the $3.5bn land, power and shell guarantees? Needed for the R7 unattributed remainder.
