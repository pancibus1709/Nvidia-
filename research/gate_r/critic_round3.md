# Gate R critic review, round 3 (final)

Reviewed 23 November 2026 against the register as rebuilt at 13:51 UTC (commit c5cc561). Scope and rules as in round 2. No voice file exists, so Voice Match was not run.

What was done: `python3 -m pipeline.checks` (passes) and `pytest -q tests` (35 pass); totals recomputed by hand from the display-eligible amounts in `relationships.json`; the bridge rebuilt from the remainder records' components and from the funded components of each equity record; all 92 insights rendered and read, 14 tested against the cached source; all 251 consequences read; `central_bank.json` counted and each verdict item opened to its quote; all 11 loops read; the 13 lead credit blocks compared with `entities.json` and six opened to their quotes (Anthropic, SpaceX, Intel, Corning, Lumentum, Nokia); the S2 scenario lines traced to `system_view.json` and `pipeline/scenarios.py`; the two team rejections tested in the cached filings.

## Round report

| Test | Result |
|---|---|
| Substance | Pass for the register; Needs Work for the generated summary |
| Specificity of claims | Pass with reservations (findings 6, 9, 10) |
| Deliverability | No, on three pipeline defects in the summary. The register files and the workbook can go as they are |
| Anti-Over-Polish | Flag (smaller than round 2) |
| Open findings | 3 critical, 7 major, 8 minor |

**What holds.** Every total ties. My own sums: cash paid $32.264 billion across 16; funded and still held $30.196 billion across 14; confirmed unpaid $1.0 billion across 1; paid portion not disclosed $36.7 billion across 5 (OpenAI 30, IREN 3.4, Nscale rental 1.2, KYEC 1.1, NAVER 1.0); contingent $107.36 billion across 3 ($105 billion not in force); gross $175.257 billion; committed total $69.95 billion across 20; headline $307.093 billion across 30; 80 counted, 50 lower bounds. `system_view.json`, `R9_system_view.md`, R7 section (2), the R9.md pointer and the workbook's register row all carry these figures. The seniority counts in R7 (4) and R9.md (b4) recount to the same ten numbers. The unconfirmed log has 47 rows as stated. No headline sits in any exposure total. No amount rests on a tier 2 source. All 13 lead credit grades are now in `entities.json`: Anthropic Adequate, SpaceX Adequate. Intel's and Corning's second-year principal are grounded in XBRL facts and the ratios (0.11, 0.33) are right. No consequence is without evidence. The verdict claims no more than its evidence.

**Both team rejections are correct.** Round 2 finding 23: the closing release (ev_120069) reads "an aggregate of 313,253,007 shares ... to Advanced Micro Devices, Inc., Broadcom Inc., Google LLC, Micron Technology, Inc., Microsoft Corporation, NVIDIA Corporation, and TSMC Partners, Ltd. ... for an aggregate purchase price of approximately $26.0 billion". It cannot ground Nvidia's $10 billion; the note on the amount says so. "Unsecured": the 8-K says "OpenAI has agreed to reimburse and indemnify NVIDIA" and the form guaranty says "Guarantor shall look solely to Tenant and/or Tenant Parent for any recoupment". Neither uses the word. Round 2's suggested wording was wrong.

**Killshot.** The register is sound and the sentences the pipeline writes about it are not tested. Three of the round 2 fixes were made with string matching or a date field, and each now prints something false in the summary that goes to the committee. OpenAI's $250 billion Azure contract is printed as "Lease obligations of this lab: $250 billion across 1 lessors" because its description contains the word "release". The bridge row that answered the round 2 Killshot counts as "inside the period" a $400 million Nscale purchase of October 2025 and a $20 million Iambic purchase of 2023. Three stakes bought in March 2026 are labelled "listed or bought after 30 September 2026". The checks recompute totals; nothing recomputes a scenario line, a bridge row or a table label. A reader who finds one of these will discount the 80 records that are right.

**The disclosed limits, and whether each is disclosed well.** These are limits, not defects.

| Limit | Where stated | Verdict |
|---|---|---|
| No news source could be read | First paragraph of the system view; first line of R9.md (c) | Prominent and accurate. Missing from the workbook's "How to read this pack" block (finding 17) |
| 50 of 80 relationships are lower bounds | First Totals line; every table has a column; workbook note | Prominent, accurate, next to the number |
| OpenAI cannot be graded | One line under the by-grade table, with its 77.0% share | Accurate. Not next to the gross figure, where it matters most; acceptable |
| The $105 billion guaranty is not in force | In the Totals line, a table column, S2 and the insight | Prominent, accurate, next to the number |
| Totals and bridge are struck at different dates | Sentence under Totals naming the Anthropic purchase | Accurate, next to the number |
| Only about a fifth of Nvidia's equity purchases can be attributed | Bridge row | Stated, but the figure is overstated and no share is printed (finding 2) |
| OpenAI's paid amount is unknown | Insight, totals bucket, record note | The floor is in the record; the summary table sends the reader elsewhere for it (finding 5) |
| Values are at 30 September 2026 | Table title and a sentence | Accurate; the label on the unvalued rows is wrong (finding 4) |

**Anti-Over-Polish: Flag.** The round 2 rewrites removed every unsupported product claim, which was right, but seven insights now end in the same clause ("so the stake cannot be sized") and eight first order "consequences" are the round's fact pattern restated ("X states no Nvidia amount"). In at least five cases the removed or kept product fact is in the cached source and only the quote on file is wrong (finding 6), so the cure was a better quote, not a blander sentence. The OpenAI floor is computed and then hidden behind a pointer.

## Status of the 29 round 2 findings

| # | Class | Status | What remains |
|---|---|---|---|
| 1 | Critical | RESOLVED | R7 (2) ties to the system view. The check that would keep it tied was not added (finding 16) |
| 2 | Critical | RESOLVED | |
| 3 | Critical | RESOLVED | Insight, reason and consequences rest on ev_90029 and ev_90030 only |
| 4 | Critical | RESOLVED | The withdrawal is labelled one unconfirmed report in all three places; no figure from it is shown |
| 5 | Critical | RESOLVED | All 13 grades match; by-grade table moved $10 billion to Adequate. No check added (finding 16) |
| 6 | Major | RESOLVED | |
| 7 | Major | RESOLVED | Built from the remainder records; R7's table kept and agrees on eight rows. The ninth differs (finding 15) |
| 8 | Major | PARTLY | Row filled and date sentence added. The figure includes purchases outside the period and the Nscale note was dropped (finding 2) |
| 9 | Major | PARTLY | Note on the record as written. The concentration cell does not state the floor (finding 5) |
| 10 | Major | RESOLVED | Counts verified by recount |
| 11 | Major | RESOLVED | All three sentences present |
| 12 | Major | RESOLVED | SB Energy's funded equity now sits in "Under 2 years" (finding 15) |
| 13 | Major | RESOLVED | The seven insights no longer carry unsupported clauses; sameness is new (finding 9) |
| 14 | Major | PARTLY | 0 of 251 without evidence. One reported claim from an unread source is still printed (finding 7); labels are uneven (finding 13) |
| 15 | Major | PARTLY | The named pairs now differ. Two new templates (finding 9) |
| 16 | Major | RESOLVED | Two further remainder insights carry the same fault in milder form (finding 12) |
| 17 | Major | PARTLY, with a regression | Lines separated and ids removed from the equity line, but the classification is by keyword and misstates four contracts (finding 1) |
| 18 | Major | RESOLVED | Intel, Corning verified; Lumentum and Nokia reasons state the bound; Synopsys nulled and regraded |
| 19 | Major | RESOLVED | Renders "nearly $3 billion"; workbook note written. Totals line carries no marker (finding 15) |
| 20 | Major | PARTLY, with a regression | Retitled; Anthropic row added. Label on four rows is false for three (finding 4). Refresh deferred to publication and said so |
| 21 | Major | PARTLY | (a) to (d) done. `loop_naver_brookfield` summary still asserts the purchase its own note says is unsourced (finding 8) |
| 22 | Minor | RESOLVED | |
| 23 | Minor | REJECTED-BY-TEAM, correctly | See above |
| 24 | Minor | RESOLVED | |
| 25 | Minor | REJECTED-BY-TEAM in part | Seed row and definition fixed. `status` definitive and `claim_basis` filed kept by the lead. Acceptable for a context record excluded from totals; noted in finding 18 |
| 26 | Minor | RESOLVED | Column, bridge block present; tie-out row matches |
| 27 | Minor | RESOLVED | The check covers the five reports and passes |
| 28 | Minor | RESOLVED | (c) reworded; see finding 11 for what the new wording leaves out |
| 29 | Minor | RESOLVED | |

Count: 19 resolved, 7 partly, 0 not resolved, 2 rejected (both judged correct).

## Status of the 17 round 1 findings round 2 marked PARTLY

| R1 # | Status | What remains |
|---|---|---|
| 1 | RESOLVED | Funded note present; cell wording is finding 5 |
| 2 | RESOLVED | |
| 3 | RESOLVED | |
| 4 | RESOLVED | |
| 7 | PARTLY | Bridge published once and consistent; two rows are wrong (findings 2, 3) |
| 9 | PARTLY | Still the 30 September holdings values, stated as such; label wrong (finding 4) |
| 10 | RESOLVED | |
| 12 | RESOLVED | |
| 14 | RESOLVED | No check (finding 16) |
| 17 | RESOLVED | |
| 18 | PARTLY | Finding 9 |
| 19 | PARTLY | Finding 9 |
| 20 | RESOLVED | |
| 24 | RESOLVED | |
| 25 | PARTLY | Finding 8 |
| 27 | RESOLVED | |
| 32 | RESOLVED | |

## Answers to the Gate R questions

**1. Is any headline number treated as exposure?** No. The $307.1 billion headline is reported in three groups and labelled "never added". R7 (2) no longer counts the CoreWeave $6.3 billion. Gross exposure of $175.3 billion contains only funded cost, committed amounts and contingent caps. The S2 line "up to $443.6 billion" is a sum of counterparties' contract values, not Nvidia exposure, and is labelled as such; its composition is wrong (finding 1).

**2. Is any one-sided relationship presented as reconciled?** No. 14 reconciled, each with evidence on both sides; 12 partial; 53 one-sided; 1 contradicted (Meta, with two differences listed). The header states the 53.

**3. Would any consequence read the same for a different company?** Not word for word. By template, yes: eight first order items of the form "[Investor] joined [round] beside [names], and [company] states no Nvidia amount" (Skild, Black Forest Labs, Databricks, CFS, PsiQuantum, TerraPower, Scale, Sakana) and six second order items of the form "so a [company] setback would fall on [co-investor] as well as on Nvidia" (Quantinuum, TerraPower, Cohere, Scale, Crusoe 2025, Firmus 2026a). Each names real co-investors from its own evidence, so none is false; none says what the trigger does. Finding 9.

**4. Do restructured or abandoned deals show their current status?** Yes, in the register and now in R7, R9.md and R4. Wayve and Cursor restructured; seven exits terminated; OpenAI letter an open letter with "(analysis; no source links them)"; TuSimple "holding unknown"; Firmus 2026a "may not exist"; NAVER "no closing is disclosed".

**5. Is anything sourced to an excluded publication, or displayed on a single tier 2 source?** No excluded domain. Six tier 2 records, all Nikkei Asia, none supporting an amount. One tier 2 claim is displayed, the Firmus listing withdrawal, each time as "One news report, unconfirmed", with no figure: within spec/04. One claim from sources nobody could open is still printed: `rel_lambda_eq_2025` second order, "whether Nvidia is one of those Lambda offtakers is reported but unconfirmed" (finding 7).

**6. Does the verdict claim more than the evidence supports?** No. Two partly supported, one not testable, one not supported; the overall line says "price setting and rescue are not shown". Every evidence item opened matches its sentence. Two wording faults (finding 11). The file is 300 words on my count of every displayed string including the label, 299 on the team's; there is no margin.

**Deliverability: No.** Exactly what must change: findings 1, 2 and 3, all in generated output, none in a counted record. Then finding 4, a one-line label. With those four regenerated and `make check` green, I would send the register, the workbook and the system view to a committee as the evidence base for the build. The remaining major findings are for the on-screen copy pass and do not change a number.

## REMAINING findings

### Critical

**1.**
> **Location:** `pipeline/scenarios.py` lines 123 to 124 (`"soft": any(w in low for w in ("up to", "cancel", "terminable", "terminat"))`, `"lease": "lease" in low`); `system_view.json` `scenarios.S2`; `R9_system_view.md` S2 lines for OpenAI and Anthropic.
> **Problem:** Contracts are classified by searching their description for words. Four are misclassified and the printed figures are wrong. (a) OpenAI's $250 billion Azure services contract is printed as a lease obligation with Microsoft as "1 lessors"; the match is on "lease" inside "release". It is then missing from OpenAI's contracts line. (b) Anthropic's $41.3 billion Lambda compute agreement is counted as a lease obligation because its description mentions a "facility lease". (c) Microsoft's $47.2 billion, the stated minimum, is counted in "stated as up to, cancellable or terminable" because the description mentions the $49.2 billion ceiling. (d) Nscale's $44.6 billion is not counted as "up to" although `loops.json` labels the same contract "up to (contract)" and R8 calls it "up to $44.6 billion".
> **Evidence:** System view: "Lease obligations of this lab: $250 billion across 1 lessors"; "Counterparty contracts that depend on this lab: up to $56.4 billion across 3 (includes $18.4 billion ...)"; Anthropic "up to $443.6 billion across 5 (includes $167.7 billion stated as up to, cancellable or terminable)"; "Lease obligations of this lab: $202.5 billion across 2 lessors". Backlog entry: "Incremental Azure services contracted under the October 2025 restructured Microsoft agreement (Microsoft 10-Q; same figure in OpenAI release ev_120102)", `lease: true`. Lambda entry: "agreements for NVIDIA GPU compute into 2034", `lease: true`. spec/01 rule 4; spec/05 section 7.
> **Fix:** Delete both keyword tests. Add two explicit fields to each commitment entry where it is recorded on the entity: `kind` ("contract" or "lease") and `soft_amount` (the part stated as up to, cancellable or terminable; 0 if none). Set: OpenAI Azure contract, 0; AWS contract, 0; both CoreWeave contract, full amount. Anthropic Google contract 0; Amazon contract 0; Microsoft contract 0; SpaceX contract 120.5; Nscale contract 44.6; Lambda contract 34.9 (the terminable agreement, ev_110012); Broadcom lease 0. SpaceX Valor and Apollo lease, 0. Expected lines: OpenAI "up to $306.4 billion across 3 counterparties (includes $18.4 billion ...)", no lease line; Anthropic "up to $484.9 billion across 6 (includes $200 billion ...)", "Lease obligations of this lab: $161.2 billion across 1 lessor". Print "lessor" when the count is 1. Add a test that fails if any S2 entry lacks `kind`.

**2.**
> **Location:** `pipeline/system_view.py` `bridge`, row "Equity purchases, nine months to 25 October 2026"; `system_view.json` `bridge[8].named` (11,202,399,346.78); workbook Summary row 36.
> **Problem:** The row says the named column is "the dated, costed equity purchases in this register inside the period". It is not. The pipeline tests the `as_of` of the whole funded amount, so it takes in every earlier round of a record whose last purchase fell in the period. At least $420 million was bought before 26 January 2026 and another $300 million has no cash date. Round 2 asked for the sentence "Nscale's figure includes rounds before the period"; it was not printed.
> **Evidence:** `rel_nscale_eq_2025.amounts.funded.components`: "Series B, issued 2025-10-08" 399,999,964.32; "SAFE principal, converted 2026-03-27" 300,000,000; "Series C-4, issued 2026-03-27" 477,399,382.46. `rel_iambic_eq_2023` components: "Series B purchase price" 20,000,000 (definition: "sold from September to December 2023"); "Series B-4 purchase price" 5,000,000 (May 2026). In-period sum: Nebius 2.0, Marvell 2.0, Lumentum 2.0, Coherent 2.0, Corning 0.5, SB Energy 1.5, Nscale Series C-4 0.477, Iambic 0.005 = $10.48 billion; $10.78 billion if the SAFE cash was paid in the period.
> **Fix:** Sum funded components, not records: give each component an optional `paid_on` date and count a component only when `paid_on` falls from 2026-01-26 to 2026-10-25. Set `paid_on` on the Nscale and Iambic components from their notes; leave the SAFE's null. Print the named cell as "$10.5 billion" and the note as "Dated, costed equity purchases in this register inside the period, 18% of Nvidia's figure; a further $300 million Nscale SAFE has no payment date. The rest of Nvidia's purchases are not attributed." Mirror the figure in the workbook block.

**3.**
> **Location:** `rel_unattributed_marketable_equity_2026_10_25`: `amounts.funded` (557,283,926 and its components), `insight_template`, first order consequence; bridge row "Public equity, fair value"; R7 bridge row and seed F2 "13F-named stakes explain almost all".
> **Problem:** The remainder subtracts eight common stock positions from a total that includes $10.5 billion of Level 2 instruments (warrants and convertible preferred) that cannot appear in a 13F. The record's own note says the comparison does not hold. The summary nonetheless shows $48.3 billion named against $48.9 billion reported, and the insight states as fact that named stakes explain almost all of Nvidia's listed equity, with a $557.3 million residual. The register itself holds $6.5 billion at cost of exactly those Level 2 instruments, unsubtracted.
> **Evidence:** Components: "Level 1 ... 38,372,000,000"; "Level 2 (unregistered warrants, convertible preferred) ... 10,516,000,000"; eight 13F subtractions totalling 48,330,717,074. Record notes: "the 13F common total ($48.3B) exceeds Level 1 ($38.4B) by about $10B ... if the Level 2 items were subtracted at cost the remainder would be negative". Insight: "Named public stakes explain almost all of Nvidia's listed equity, leaving $557.3 million unattributed at fair value." spec/01 rules 7 and 11.
> **Fix:** Split the row in two, like for like. "Listed shares (Level 1) | $38.4 billion | not comparable | Nvidia's holdings report of 30 September shows $48.3 billion of named common stock, $10 billion more than Level 1 at 25 October; the dates differ and the level of the SpaceX shares is not disclosed." "Warrants and convertible preferred (Level 2) | $10.5 billion | $6.5 billion at cost | Marvell and Lumentum preferred, Nebius warrant, Corning warrants; cost, not fair value." Set the remainder record's `funded.value` to null with `display_eligible` false and the note "Not computable: see the two bridge rows." Insight: "Nvidia's listed holdings cannot be matched to its balance sheet line by line, because the dates and instruments differ, so no unattributed figure is shown." First order: "Nvidia's holdings report names Intel, SpaceX and CoreWeave as its largest listed positions (ev_50021, ev_50031, ev_50019), so a fall in its public equity value can be traced mainly to those names." R7 row and F2: same two rows; replace "explain almost all" with "exceed Level 1 by $10 billion at a date 25 days earlier".

### Major

**4.**
> **Location:** `pipeline/system_view.py` line 175; `R9_system_view.md` "Largest positions by value at 30 September 2026", last four rows.
> **Problem:** One hard-coded label, "listed or bought after 30 September 2026", is printed on four positions. It is true of Anthropic only. Nebius appears twice in the table with no way to tell the two positions apart. Corning's warrants, a fourth position of the same kind, are missing.
> **Evidence:** `rel_nebius_eq_2026` dates.signed 2026-03-11, market_value note "warrants are not 13F securities"; `rel_marvell_eq_2026` 2026-03-31, "convertible preferred is not a 13F security"; `rel_lumentum_eq_2026` 2026-03-02. `rel_corning_eq_2026` note: "Warrants are not 13F securities".
> **Fix:** Take the reason from the record: if `dates.effective` is after 2026-09-30 print "bought after 30 September 2026"; otherwise print "warrant or preferred stock, not in the holdings report". Print the instrument beside the name ("Nebius (warrant)", "Nebius (common)"). Include every record with a funded cost, a listed counterparty and no market value, which adds Corning.

**5.**
> **Location:** `R9_system_view.md` "Top five concentrations", OpenAI row; `pipeline/system_view.py` `lower_bound_notes`.
> **Problem:** The cell reads "Not disclosed; see the analysis note on the record for a lower bound". A reader of the summary cannot see the record. The largest unknown in the register has a sourced floor and the summary withholds it.
> **Evidence:** `rel_openai_eq_2026.amounts.funded.note`: "at least $10 billion had been paid by that date, and at least $13.5 billion after the $3.5 billion this register attributes to other investees". Round 2 fix 9: "Concentration table cell: 'Not disclosed; at least $10 billion by 25 October 2026 (analysis)'".
> **Fix:** Add `funded.floor` (10,000,000,000) and `funded.floor_as_of` ("2026-10-25") to the amount, not display eligible and in no total, and print "Not disclosed; at least $10 billion by 25 October 2026 if the commitment sits in Nvidia's $20 billion unfunded total (analysis)". Use the same sentence on the S2 OpenAI equity line.

**6.**
> **Location:** evidence lists on `rel_point2_eq_2026` (insight, both consequences), `rel_figure_eq_2025` (insight, first order [0]), `rel_together_ai_eq_2025` (insight, second order), `rel_psiquantum_eq_2025` (insight, second order), `rel_weride_eq_2017` (second order).
> **Problem:** Each sentence states a product fact that is in the cached source, but no quote on the record contains it. The source chip would open on a sentence that does not say what the text says. On WeRide the second id attached is a Synopsys line from Nvidia's 13F.
> **Evidence:** Point2 text "builds radio frequency interconnects for AI factories"; only quote on file, ev_30069: "NVIDIA also announced an investment in Korean startup Point2". Figure text "committed to rent Nvidia Vera Rubin capacity"; quotes on file say "initial commitment of $3.5 billion of compute". Together text "funds a deployment of NVIDIA Blackwell GPUs"; quotes on file name the round and investors. PsiQuantum text "GPU and quantum processor integration"; ev_200008 stops at "across a broad range of development areas". WeRide text "uses Nvidia cloud GPU clusters and DRIVE chips"; evidence ev_90025 ("early-stage investor") and ev_90016 ("SYNOPSYS INC COM ...").
> **Fix:** Add five evidence records from the same cached files and attach them. Point2: "builds scalable, radio frequency-based interconnects that move data between chips and racks". Figure: "deploy the NVIDIA Vera Rubin platform for up to 100,000 GPUs". Together: "our upcoming large-scale deployment of NVIDIA Blackwell GPUs". PsiQuantum: "including quantum algorithms and software, GPU-QPU integration". WeRide: "such as cloud-based GPU clusters and the NVIDIA DRIVE Xavier system-on-a-chip"; remove ev_90016 from that consequence. Then, for every insight and consequence, check that at least one attached quote shares a noun with the product or site named in the text; list the misses for the copy pass.

**7.**
> **Location:** `rel_lambda_eq_2025` `consequences.second_order[1]`.
> **Problem:** The sentence puts on screen a claim that exists only in reports nobody could open. The unconfirmed log says such claims do not appear.
> **Evidence:** Text: "whether Nvidia is one of those Lambda offtakers is reported but unconfirmed". `research/unconfirmed.md`: "Lambda | The $926M term loan B funds an 'Nvidia-tied chip deal' | One outlet, blocked; Lambda's release names only an investment-grade offtaker". spec/04: "If the only source is excluded, the relationship goes to `research/unconfirmed.md` ... and does not appear in the app."
> **Fix:** Replace the text with: "Lambda's rated GPU loans rest on the GPUs they fund and on contracts with investment-grade offtakers that Lambda does not name, so no source shows whether Nvidia's stake sits beside a loan that depends on Nvidia." Keep the evidence list.

**8.**
> **Location:** `loops.json` `loop_naver_brookfield.summary`.
> **Problem:** The summary ends with a statement of fact that the loop's own note says no source supports. The matching consequence was corrected in round 2; the loop was not.
> **Evidence:** Summary: "so Nvidia's equity helps trigger financing that buys Nvidia systems". `circularity_note`: "no allowed source states that the Brookfield vehicle's GPUs are bought from Nvidia or their value".
> **Fix:** Last clause: "so Nvidia's equity helped trigger financing for a site Nvidia describes as its own AI factory design; no source says whose GPUs the vehicle buys."

**9.**
> **Location:** `insight_template` on `rel_reflection_eq_2025`, `rel_cohere_eq_2025`, `rel_sakana_eq_2024`, `rel_ssi_eq_2026`, `rel_skild_ai_eq_2026`, `rel_scale_ai_eq_2024`, `rel_commonwealth_fusion_eq_2025`; `consequences.first_order[0]` on Skild, Black Forest Labs, Databricks, CFS, PsiQuantum, TerraPower, Scale, Sakana; `second_order[0]` on Quantinuum, TerraPower, Cohere, Scale, `rel_crusoe_eq_2025`, `rel_firmus_eq_2026a`.
> **Problem:** Sameness of a new kind. Seven insights end "so the stake cannot be sized". Eight first order items restate who was in the round and that no amount is stated; they have no trigger and no effect. Six second order items say a setback "would fall on" a named co-investor "as well as on Nvidia", which is true of any syndicate.
> **Evidence:** "Nvidia has joined repeated Cohere rounds, the latest led by Schwarz Group, without stating an amount, so the stake cannot be sized." "Sakana AI names Nvidia among its Series A investors without an amount, so the stake cannot be sized." "NVentures entered PsiQuantum's $1 billion Series E beside Ribbit Capital and Adage Capital Management, and PsiQuantum states no Nvidia amount." spec/05 section 6: "one sentence with four parts ... trigger, mechanism, who is affected, direction ... A consequence that would read the same for any company fails review."
> **Fix:** Insights: keep "cannot be sized" on one record (Reflection) and end each of the others on the one fact its evidence holds: Cohere "... alongside the Government of Canada"; Sakana "... beside Translink Capital and 500 Global"; SSI "... and pairs it with Vera Rubin access; no amount is stated"; Skild "... led by SoftBank; no amount is stated"; Scale "... with nearly all existing investors; no amount is stated"; CFS "... in a round of many backers; no amount is stated". Consequences: for each of the fourteen items, either write the trigger and effect the evidence supports (PsiQuantum's second order item is the model: "collaborating with Nvidia on ... integration, so part of its roadmap depends on its investor") or cut the record to one first order item reading "No amount, terms or commercial tie is disclosed, so no consequence can be drawn beyond a write-down of an unsized stake." Two to four generic items are worse than one honest one.

**10.**
> **Location:** `rel_firmus_eq_2026b` `consequences.first_order[1]`.
> **Problem:** The second half is conjecture about who would fund Firmus next, unlabelled, and it calls Blackstone a private investor when the record's evidence shows Blackstone as lender. The wording came from round 2.
> **Evidence:** Text: "if so, Firmus's next funding would again come from private investors such as Nvidia, Coatue and Blackstone". ev_110035: "secured a US$10 billion debt financing facility led by funds managed by Blackstone".
> **Fix:** "One news report, unconfirmed, says Firmus withdrew its Australian listing application; if so, Firmus stays privately funded, with Coatue and Nvidia as named equity investors and a Blackstone-led debt facility (analysis)."

### Minor

**11.**
> **Location:** `central_bank.json`: liquidity `evidence_against[1].text`; `where_the_analogy_breaks`.
> **Problem:** (a) "Intel's Nvidia stake" reads as a stake Intel holds in Nvidia. (b) "with only OpenAI's reimbursement promise in return" is wrong on Nvidia's own disclosure: in return for the guaranties the site hosts only Nvidia infrastructure. What Nvidia has only one of is recourse. (c) No margin on the 300 word limit.
> **Evidence:** ev_120004: "In exchange for the guarantees, the site will exclusively host NVIDIA AI infrastructure". ev_100003: "Guarantor shall look solely to Tenant and/or Tenant Parent for any recoupment".
> **Fix:** (a) "Nvidia's Intel stake came with a product deal but no disclosed purchase commitment." (b) "the OpenAI guaranty alone is $105 billion, recoverable only from OpenAI." This removes two words; do not add any.

**12.**
> **Location:** `rel_unattributed_cloud_service_agreements_2026_10_25` insight against its first order consequence; `rel_unattributed_guarantees_2026_10_25` insight.
> **Problem:** (a) The insight says Nvidia "names none of the providers"; the consequence on the same record says it "names only some providers". (b) The guarantees insight says "unnamed partners ... it does not say who they are"; the record's notes list CoreWeave, Firmus and SharonAI as partners that may sit inside the figure.
> **Evidence:** Record definition: "No named rental has a disclosed remaining commitment at the same date: CoreWeave, IREN and Nscale give only an initial order value or total contract values." Guarantees notes: "Any of these could sit in the remainder".
> **Fix:** (a) Insight: "Nvidia has {committed_total} of cloud rental commitments; CoreWeave, IREN and Nscale are known providers, but no provider's remaining balance is disclosed." Consequence: replace "names only some providers" with "does not say what it still owes each provider". (b) "Up to {contingent_max} of Nvidia's guarantees cannot be tied to a named partner; CoreWeave, Firmus and SharonAI support may sit inside it."

**13.**
> **Location:** consequences on `rel_nscale_eq_2025` second order [0], `rel_applied_digital_eq_2024` second order [0], `rel_anthropic_eq_2026` second order [1], `rel_iren_eq_2026` second order [1], `rel_sb_energy_eq_2026` second order [0].
> **Problem:** 50 consequences carry "(analysis)"; these five make the same kind of inference about signalling or cost of capital without it.
> **Evidence:** "so a pause by Nvidia in later Nscale rounds would raise Nscale's cost of equity"; "helped Applied Digital raise $160m at market, and its quiet exit ... removed that signal"; "a sale by Nvidia would signal reduced supplier support"; "a lapse would signal the opposite to IREN's lenders". spec/01 rule 7.
> **Fix:** Append "(analysis)" to each. Applied Digital: replace "helped Applied Digital raise" with "was part of Applied Digital's".

**14.**
> **Location:** consequence texts across `relationships.json` (for example `rel_nscale_eq_2025`, `rel_nebius_eq_2024`, `rel_black_forest_labs_eq_2025`, `rel_firmus_eq_2026a`, `rel_firmus_eq_2025`, `rel_applied_digital_eq_2024`).
> **Problem:** Typed figures use six styles in text that will go on screen.
> **Evidence:** "$43.8bn", "$33.0m", "$300M", "USD5.5 billion", "A$330m", "$102.5M", beside "$3.5 billion" and "$326.3 million" elsewhere.
> **Fix:** One style, the one `fmt.money` produces ("$43.8 billion", "$33 million", "A$330 million"). Add to `check_copy` a pattern that fails on a digit followed by "bn", "m", "M" or "B" in consequence text, and on "USD" followed by a digit.

**15.**
> **Location:** `R9_system_view.md` Totals headline line and S2 OpenAI guaranty line; "By tenor"; `R7_aggregates.md` bridge row "Equity purchases, nine months".
> **Problem:** (a) Raw ids in summary text. (b) No marker that one headline figure is stated as "nearly". (c) SB Energy's $1.5 billion of funded equity is in "Under 2 years" because the bucket is set on the whole record. (d) R7's bridge says "flow, no remainder" where the system view shows a named figure.
> **Evidence:** "excludes GBP 2 billion (rel_uk_ai_startup_program_eqc_2025), not converted"; "(ev_120002, ev_120009) ... (ev_30023)". Tenor row: "Under 2 years | 2 | $2.5 billion | $1 billion | $0 | $1.5 billion".
> **Fix:** (a) Print "the UK startup program" and strip `ev_` ids from `effective_note` when rendering. (b) Append "(one figure is stated as 'nearly')". (c) Add under the tenor table: "SB Energy is placed by its conditional $1.5 billion, which lapses in May 2027; its funded $1.5 billion is equity." (d) Replace R7's two flow rows with "See the system view bridge".

**16.**
> **Location:** `pipeline/checks.py`.
> **Problem:** Two checks round 2 asked for were not added, so R7 (2), R9.md and the credit grades tie today by hand only.
> **Evidence:** No reference to "Gross exposure" or `lead_credit` in `checks.py`; FIXES.md: "The pipeline check part is the lead's."
> **Fix:** Add `check_report_totals` (fails when R7 or R9.md prints a "Gross exposure", "Contingent maximum" or "Cash paid" figure that differs from `fmt.money` of the system view total) and `check_lead_grades` (fails when a grade in `lead_credit.json` differs from `entities.json`).

**17.**
> **Location:** `pipeline/datapack.py` "How to read this pack" block.
> **Problem:** The workbook's first page states the lower bound count but not that no news source could be read or that 53 of 80 relationships are disclosed by one side only. The system view leads with both.
> **Evidence:** Summary rows 20 to 25; `system_view.json` `source_mix.note`.
> **Fix:** Add one row: the `source_mix.note` text followed by "53 of 80 relationships are disclosed by one side only."

**18.**
> **Location:** `ent_anthropic.credit.maturities_24m` and `committed_spend_12m`; `rel_corning_pp_2026` `status`, `claim_basis`.
> **Problem:** (a) Anthropic's 24 month maturities cover 15 months with `lower_bound` false; SpaceX's block, built on the same 15 month window, sets it true. The grade does not change. (b) The Corning context record remains "definitive" and "filed" although its link to Nvidia is analysis; kept by the lead.
> **Evidence:** Anthropic note: "Finance lease payments due in Q4 2026 and calendar 2027 (15 months)". SpaceX note: "the 2028 maturities that fall inside 24 months are excluded", `lower_bound: true`.
> **Fix:** (a) Set `lower_bound` true on the Anthropic amount. (b) Leave as is; when the application renders context records, show "Link to Nvidia: analysis" beside the status.

## Calibration note

**What held across three rounds. Preserve it.**
- The four-way split of amounts, with headline never added and "paid portion not disclosed" kept apart from "unpaid". It survived every recomputation.
- Null instead of zero. Nothing unknown is printed as $0 in a record; "not computable" is said once and plainly.
- Grounding. Every figure tested in three rounds was found in its cached source. No fabricated quote was found in any round.
- The willingness to reject a critic's fix with the source in hand (round 1 finding 41, round 2 finding 23, "unsecured"). All three rejections were right and two corrected errors the critic introduced.
- Status discipline: letters of intent stay letters, exits are terminated, "may not exist" is said where true.
- The verdict. It was cut from a claim to a test and now says less than a hostile reader would concede.

**The recurring fault.** Each round fixed the records and then broke something in the layer that talks about them. Round 1: reports not regenerated. Round 2: three reports telling three stories. Round 3: generated lines built from keywords and whole-record dates. The checks guard amounts; no check reads a generated sentence. When the on-screen copy is written, three rules follow.
1. Any sentence or label the application generates from data must be driven by an explicit field, never by searching text, and must have a test with one true and one false case.
2. A fix that removes an unsupported clause should first ask whether the source supports it. Round 2's removals were safe and left a third of the long-tail insights saying the same thing; in five cases tested the fact was in the cache.
3. Wording supplied by a critic is not evidence. Three of this round's findings (9, 10, 11b) trace to text written in rounds 1 and 2. Test it against the quote like any other sentence.
