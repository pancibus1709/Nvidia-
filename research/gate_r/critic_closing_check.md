# Gate R critic: closing check after round 3

Checked 23 November 2026 against the live files at commit 220bfbd (clean working tree). This is not a fourth round. The only question: are the 18 round 3 findings closed, and is any critical finding open.

What was done: `python3 -m pipeline.checks` ("All checks passed") and `python3 -m pytest -q tests` (37 pass). `system_view.build()` rerun in memory and compared with `system_view.json`: identical, so the printed summary is current. Each lab's contract, soft and lease totals recomputed from `entities.json` `compute_commitments`. The in-period equity figure recomputed from every funded component's `paid_on`. The remainder record's insight, notes, `bridge_rows` and funded amount read against each other and against R7 and the seed row. All 14 rows of the positions table compared with their records. The records named in findings 5 to 14 and 18 opened. The workbook's Summary sheet read. `R9_system_view.md` read once, top to bottom, against the register.

## Status of the 18 round 3 findings

| # | Class | Status | Tested how; what remains |
|---|---|---|---|
| 1 | Critical | RESOLVED | Both keyword tests are gone from `scenarios.py`; all 21 entries carry `kind` and `soft_amount`. My sums: OpenAI contracts 250 + 38 + 11.9 + 6.5 = $306.4 billion, 4 contracts, 3 counterparties, soft $18.4 billion, no sized lease. Anthropic contracts 121.3 + 110 + 47.2 + 120.5 + 44.6 + 41.3 = $484.9 billion, 6, soft 120.5 + 44.6 + 34.9 = $200 billion; lease $161.2 billion, 1 lessor. SpaceX leases 20.206 + 40 = $60.2 billion, 2 lessors. All match the printed lines. The test covers "release". Not done as written: no check fails when a live entry lacks `kind`; the pipeline prints it on a separate "not yet classified" line instead, which is safe. Carry as minor |
| 2 | Critical | RESOLVED | My sum of components with `paid_on` from 2026-01-26 to 2026-10-25: Nebius 2.0, Marvell 2.0, Lumentum 2.0, Coherent 2.0, Corning 0.5, SB Energy 1.5, Nscale Series C-4 0.4774, Iambic Series B-4 0.005 = $10,482,399,382. Bridge prints $10.5 billion and `named` 10,482,399,382.46. 18% of $58.1 billion is right. Undated: Nscale SAFE $300 million plus Serve $12 million = $312 million, as printed. Nscale Series B (2025-10-08), Iambic Series B (2023) and Anthropic (2026-11-20) are excluded. Workbook row carries the same figure and note |
| 3 | Critical | RESOLVED | `funded.value` null, not display eligible, note "Not computable: see the two bridge rows." Two rows from `bridge_rows`: Level 1 $38.4 billion, "not comparable"; Level 2 $10.5 billion against $6.5 billion at cost (2.0 + 2.0 + 2.0 + 0.5, the four records named). Insight, definition, title, credit note and notes agree with one another; the $557.3 million survives only in the notes as a withdrawn figure. R7 rows 39 to 40, 79 and 217 and the seed F2 row say the same; "almost all" appears nowhere |
| 4 | Major | RESOLVED | Every row matches its record. Anthropic: common, effective 2026-11-20, "bought after 30 September 2026". Nebius 2026 warrant, Marvell and Lumentum preferred, Corning warrant: each labelled by its own instrument, all bought before 30 September. Corning added. The two Nebius rows are told apart. Iambic: common after its October 2026 listing, "not in Nvidia's holdings report of 30 September 2026", true. No listed, costed, live position is missing |
| 5 | Major | RESOLVED | `floor` 10,000,000,000, `floor_as_of` 2026-10-25, value null, in no total. Printed with its condition in the concentration cell and on the S2 line |
| 6 | Major | RESOLVED | Five quotes on file and attached; each contains the product fact. ev_90016 is off the WeRide consequence. The noun check left 48 misses, listed in FIXES.md for the copy pass, which is what the fix asked for |
| 7 | Major | RESOLVED | Text as written; "reported but unconfirmed" is gone |
| 8 | Major | RESOLVED | Last clause as written and consistent with the loop's note |
| 9 | Major | PARTLY | Insights: one "cannot be sized" left (Reflection); the other six end on a fact. Consequences rewritten; four use the honest line. Remains: `rel_quantinuum_eq_2025` `consequences.second_order[0]` now cites ev_50031, whose quote is the SpaceX line of Nvidia's 13F. The chip opens on a sentence about another company; this is the WeRide fault of finding 6, newly introduced. Also for the copy pass: Skild, Black Forest Labs and CFS first order items share one down-round template |
| 10 | Major | RESOLVED | Text as written; ev_110035 attached |
| 11 | Minor | RESOLVED | (a) and (b) as written. My count of displayed strings: 297 words |
| 12 | Minor | RESOLVED | Both insights and the consequence phrase as written; the record no longer contradicts itself |
| 13 | Minor | RESOLVED | All five carry "(analysis)"; Applied Digital reworded |
| 14 | Minor | PARTLY | Relationship titles, definitions and consequences are in one style and `check_money_style` guards them (test has a true and a false case). Remains: `loops.json`, which is on-screen text and is not read by the check, still has the old styles in ten strings, for example `loop_coreweave.legs[1].description` "$320m ... $326.3m ... $59.6m", `loop_nscale.legs[1].description` "$1.0bn", `loop_firmus.legs[0].description` "USD505m ... USD2bn", `loop_spacex_xai.legs[2].description` "$1.25bn", `loop_sharonai.legs[0].description` "$4.88bn" |
| 15 | Minor | PARTLY | (b), (c), (d) done; the UK program is named in words. Remains (a): the S2 OpenAI guaranty line still prints "(ev_120002, ev_120009)" and "(ev_30023)". `strip_ids` is defined at `pipeline/system_view.py` line 186 and never called |
| 16 | Minor | RESOLVED | `check_report_totals` and `check_lead_grades` exist and run. The totals pattern matches R7 lines 167, 170 and 171 and fires on a changed figure (tested on the line in memory) |
| 17 | Minor | RESOLVED | Summary sheet carries the source-mix sentence followed by "53 of 80 relationships are disclosed by one side only." |
| 18 | Minor | RESOLVED | (a) `lower_bound` true on Anthropic `maturities_24m`. (b) left by agreement |

Count: 15 resolved, 3 partly, 0 not resolved. The three critical findings are resolved.

## New concrete defects in generated text

Two found in the top to bottom read. Neither changes a number.

**A.**
> **Location:** `pipeline/system_view.py` line 268; `R9_system_view.md` "S2 Lab funding gap: other labs".
> **Problem:** One hard-coded reason is printed for ten labs: "no confirmed value for Nvidia's stake and no sourced commitments". It is false for two and loose for two more. SSI and Thinking Machines each have a sourced compute commitment on the entity; only the amount is missing. Motif Technologies and Upstage have no stake at all, only a letter or framework record.
> **Evidence:** `ent_ssi.compute_commitments[0]`: "Access to Nvidia Vera Rubin systems to increase SSI's compute by an order of magnitude (ev_30060)". `ent_thinking_machines.compute_commitments[0]`: "Multiyear partnership to deploy at least one gigawatt of Nvidia Vera Rubin systems". `rel_motif_eqc_2026` and `rel_upstage_eqc_2026`: type EQ-C, status `loi_or_framework`, no equity record.
> **Fix:** Drive the reason from the data. Print "Not computable: no stake value and no commitment with a disclosed amount" and append, from the entity's entries, "SSI and Thinking Machines have Nvidia system commitments of undisclosed amount". List Motif and Upstage apart as "letter or framework only, no stake".

**B.**
> **Location:** `pipeline/system_view.py` lines 254 to 265; `R9_system_view.md` "S2 Lab funding gap: OpenAI", contracts line.
> **Problem:** The line gives "up to $306.4 billion in 4 contracts" and no lease line, and says nothing of three sourced commitments whose amount is not disclosed. A reader takes "up to" as a ceiling and takes the missing lease line as no leases, two lines below a guaranty of OpenAI's leases.
> **Evidence:** `system_view.json` `scenarios.S2.ent_openai.not_computable`: PORTS-Pike "about 8 GW-IT under 17 leases of 20 years each"; "6 GW of AMD Instinct GPUs"; "10 GW of OpenAI-designed accelerators with Broadcom". None is printed.
> **Fix:** After the contracts line print, from `not_computable` and each entry's `kind`: "Not sized: 2 further contracts (AMD, Broadcom) and the PORTS-Pike leases have no disclosed amount." Replace "up to" with "at least" when any entry is unsized and no soft amount applies to it, or drop the qualifier and rely on the bracket.

Not defects today, but two sentences are unconditional strings and will go wrong when the data moves: line 219, "publishes no balance sheet and cannot be graded", printed for whichever counterparty is largest; and the Loops line "None has a disclosed dollar value on the return leg", although `closing_leg_valued` is on each loop. Both are true of the register as it stands.

## To carry into the application's copy pass

Major
- Finding 9 residue: replace ev_50031 on the Quantinuum second order item with a record that says what the sentence says, or cut the "no source says" clause to the definition's own wording.
- Finding 6 list: the 48 text and quote mismatches named in FIXES.md.

Minor
- Finding 15 (a): call `strip_ids` on `effective_note`.
- Finding 14 residue: restyle the ten `loops.json` strings and extend `check_money_style` to loops, entity descriptions and `central_bank.json`.
- Finding 1 residue: add a check that fails when a compute commitment lacks `kind` or `soft_amount`.
- New defects A and B.
- The two unconditional sentences above: drive each from its field, with a true and a false test case.
- Copy nits in the bridge: the Level 2 note says "at cost, not fair value" twice; the Level 1 row says "not comparable" in the cell and again in the note; the Guarantees row has no note that $105 billion of the named figure is not in force.
- Finding 18 (b): show "Link to Nvidia: analysis" on context records.

OPEN CRITICAL FINDINGS: 0

**Gate verdict: PASSED.** No critical finding is open. Every total, the bridge and the scenario lines recompute from the register, the checks and tests are green, and the generated summary matches a fresh build. Open items go to the copy pass: two major (finding 9 residue, the finding 6 list) and the minor items listed above, including new defects A and B.
