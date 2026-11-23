# Gate R critic review, round 2

Reviewed 23 November 2026 against the register as rebuilt at 13:19 UTC (commit 39b8598). Scope: `data/register/*.json`, `research/reports/R9_system_view.md`, `R9.md`, `R7_aggregates.md`, `R2.md`, `R4.md`, `R8.md`, `research/seed_status.csv`, `research/unconfirmed.md`, `pipeline/datapack.py`, `pipeline/system_view.py`, `pipeline/build_register.py`. Rules applied: spec/01, 04, 05, 09. No voice file exists, so Voice Match was not run.

What was done: `python3 -m pipeline.checks` (passes); totals recomputed by hand from `relationships.json` using display-eligible amounts only; the workbook formulas in `pipeline/datapack.py` traced row by row against the same amounts; all 92 insights rendered and read; all 255 consequences scanned for evidence, figures and sameness; `central_bank.json` word count; all 11 loops; 13 credit blocks compared between `research/drafts/lead_credit.json` and `entities.json`, 6 opened to the evidence quote; 8 `nvidia_financials.json` figures re-found in Exhibits 99.2 and 99.3 of the 8-K of 17 November 2026; the Anthropic 424B4 passage for finding 41 read in context.

## Round report

| Test | Result |
|---|---|
| Substance | Needs Work |
| Specificity of claims | Needs Work (better than round 1) |
| Deliverability | No |
| Anti-Over-Polish | Flag |
| Open findings | 5 critical, 16 major, 8 minor |

**What holds.** The arithmetic is right. My own sums from `relationships.json` match `system_view.json` and what the workbook formulas produce: funded and still held $30.196 billion across 14, cash paid $32.264 billion across 16, confirmed not yet paid $1.0 billion across 1, paid portion not disclosed $36.7 billion across 5, contingent $107.36 billion across 3 ($105 billion not in force, $2.36 billion in force), gross $175.257 billion, headline $307.093 billion in groups of $117.04, $103.5 and $86.55 billion, 80 counted, 50 lower bounds. Every by-type, by-cluster and by-status row I recomputed ties. All eight Nvidia financial figures tested match the cached exhibits. Every evidence id in the seven register files resolves. The verdict is 299 words. No headline amount sits in a register total.

**Round 1 Killshot: answered in the system view, not in the other two reports.** The system view now splits unpaid from undisclosed, counts cost still held, sets the guaranty not yet in force apart and carries a bridge. R7 section (2) and the R9.md summary were not brought along (findings 1 and 2).

**Killshot now.** The bridge shows the gap and then declines to measure the register against it. Nvidia paid $58.1 billion for equity securities in the nine months to 25 October 2026. The register's dated, costed equity purchases inside that window add up to about $11.2 billion (Nscale preferred, Nebius, Marvell, Lumentum, Coherent, Corning, SB Energy), 19%. The row that should say so is blank. The register's own remainder arithmetic also implies that at least $13.5 billion of OpenAI's $30 billion had been paid by that date ($20 billion of total unfunded commitments less the $3.5 billion R7 attributes elsewhere), and the register shows OpenAI as "Not disclosed". Meanwhile one third of "funded and still held" is an Anthropic purchase made 26 days after the bridge date, so the totals and the bridge are struck at different dates without a word saying so. What is left as "gross at least $175.3 billion" is 77% one counterparty with no credit grade and 60% a guaranty not in force before fiscal 2029. The number is honest in its parts and still says little about what Nvidia has at risk today.

**The next four.**
1. Three reports, three stories. R7 section (2) still prints contingent $113.7 billion and gross $183.6 billion with the CoreWeave initial order value inside. R9.md still tells Thomas the lender of last resort test is "partly supported" on going-concern language and that SharonAI and Nscale are graded Distressed. The two bridges disagree on three of their rows.
2. A fix logged as done did not reach the register. The new Anthropic and SpaceX credit blocks lost the merge, so Anthropic ($10 billion) is still ungraded and SpaceX is still "Strong" where the team's own sourced figure makes it Adequate.
3. Sentences about named companies still rest on news reports nobody could open. Reflection's insight and Firmus's "talks" consequence both sit in the unconfirmed log as blocked.
4. 112 of 255 consequences carry no evidence, and several of the new insights state a product or customer fact that no evidence in the record supports.

**Anti-Over-Polish: Flag.** Three places where a fact on file became "not disclosed" or a blank: OpenAI paid amount (a floor of $10 billion follows from Nvidia's own $20 billion total, and round 1 asked for it); the bridge row for private stakes (R7 holds $2.68 billion named, the system view shows nothing); NAVER (the record says closing is pending and R7 treats it as unpaid at 25 October, the totals file it under "paid portion not disclosed"). The reverse fault also appears: "small" was added to the Sakana and Black Forest Labs insights where the size is undisclosed.

## Status of the 41 round 1 findings

| # | Status | What remains |
|---|---|---|
| 1 | PARTLY | Buckets split, derived fields null, OpenAI shown "Not disclosed", S2 fixed. Not done: the funded note with the $10 billion floor (fix 1c). NAVER moved to the undisclosed bucket against the record's own text (finding 6 below). |
| 2 | PARTLY | Register, loop leg, remainder and system view fixed. R7 section (2) still counts the $6.3 billion in contingent and gross (finding 1). |
| 3 | PARTLY | Verdict, insights, consequence and grades fixed. R9.md section (c) and decision 1 still state the old verdict and grades (finding 2). `loop_sharonai` note still says the going-concern section "matters for the backstop". |
| 4 | PARTLY | Three insights and the loop summary fixed. First order item 2 now adds an uncached "talks" claim; `ent_firmus` market signals still carry two single-source figures (finding 4). |
| 5 | RESOLVED | |
| 6 | RESOLVED | Register files resolve and the check exists. R7, R9.md, R2, R4 and R8 still cite ids outside the store (finding 27). |
| 7 | PARTLY | Lines captured, bridge published. Two bridges disagree; private stakes and equity purchases have no named figure (findings 7, 8). |
| 8 | RESOLVED | |
| 9 | PARTLY | Table added. Values are still the 13F of 30 September; no Anthropic value (finding 20). |
| 10 | PARTLY | Split and insight done. The tenor table still puts the guaranty in "No stated maturity" (finding 12). |
| 11 | RESOLVED | |
| 12 | PARTLY | Register, S2 and R7 fixed. R9.md (a4, b3) and R4 line 68 still say "replaced" (finding 10). |
| 13 | RESOLVED | |
| 14 | PARTLY | R9.md totals replaced by a pointer. R7 section (2) table not regenerated; no check added (finding 1). |
| 15 | RESOLVED | |
| 16 | RESOLVED | |
| 17 | PARTLY | 11 of 13 new blocks are in the register. Anthropic and SpaceX are not (finding 5). The OpenAI sentence is missing (finding 11). |
| 18 | PARTLY | 18 insights rewritten. Sakana and Black Forest Labs still share one sentence; several new insights carry unsupported clauses (finding 13). |
| 19 | PARTLY | Korea records distinct, figures cited, ids out of text. 112 of 255 consequences have no evidence; new duplicates (findings 14, 15). |
| 20 | PARTLY | The ten named items fixed. The same class remains elsewhere (finding 14). Lumentum and Coherent are now word for word identical, which follows round 1's own instruction (finding 15). |
| 21 | RESOLVED | R9.md (b3) still says "xAI stake converted into SpaceX shares" (finding 10). |
| 22 | RESOLVED | |
| 23 | RESOLVED | 299 words; no room left. |
| 24 | PARTLY | Register fixed. R7 (3) and R9.md (b3) still list TuSimple as exited (finding 10). |
| 25 | PARTLY | NAVER loop open, CoreWeave wording, Azure leg, new field: done. The sentence is not printed; the OpenAI loop keeps a CoreWeave leg dated before the round (finding 21). |
| 26 | RESOLVED | |
| 27 | PARTLY | Corning is context, KYEC moved and reworded. Amkor still renders "$3 billion" (finding 19). |
| 28 | RESOLVED | |
| 29 | RESOLVED | |
| 30 | RESOLVED | |
| 31 | RESOLVED | New label problems in S2 (finding 17). |
| 32 | PARTLY | System view header says it. R9.md does not; the log has 47 rows, R9.md says 46 (finding 11). |
| 33 | RESOLVED | |
| 34 | RESOLVED | R7 (4) still lists Meta under common equity (finding 10). |
| 35 | RESOLVED | |
| 36 | RESOLVED | |
| 37 | RESOLVED | |
| 38 | RESOLVED | |
| 39 | RESOLVED | |
| 40 | RESOLVED | |
| 41 | REJECTED-BY-TEAM, correctly | The Anthropic 424B4 reads: "Following initial non- cancelable periods ending in January 2027 and March 2027 under the respective agreements, each agreement may be cancelled by either party upon 90 days' advance written notice", in the paragraph on the SpaceXAI Arrangements. "From early 2027" stands. Round 1 was wrong. |

Count: 23 resolved, 17 partly, 0 not resolved, 1 rejected correctly.

## Answers to the Gate R questions

**1. Is any headline number treated as exposure?** Not in the register, the system view or the workbook. Yes in `R7_aggregates.md` section (2): "Contingent maximum (4 relationships) $113.7B" and "Gross exposure ... $183.6B" include the CoreWeave $6.3 billion, which the same table's caveat calls "an initial order value, not a cap" (finding 1). Softer cases: the Amkor headline is stored and summed as $3.0 billion where the source says "nearly $3 billion" (finding 19); S2 prints "compute commitments at risk: $646.1 billion" for Anthropic, a sum of "up to" contract values, minimum commitments and equipment leases (finding 17).

**2. Is any one-sided relationship presented as reconciled?** No. The 14 records marked reconciled each cite both sides; Brookfield, NAVER, the CoreWeave framework and the OpenAI letter of intent are now partial. 53 of 80 are one-sided and the header says so.

**3. Would any consequence read the same for a different company?** Yes, fewer than before. `rel_lumentum_eq_2026` and `rel_coherent_eq_2026` second order: identical apart from the name. Five supply records (`rel_amkor_pp_2026`, `rel_kyec_pp_2026`, `rel_ibiden_pp_2026`, `rel_unimicron_pp_2026`, `rel_spil_pp_2026`) share one first order sentence: "If X's [site] is late, Nvidia's advance is tied up and its supply tightens". `rel_commonwealth_fusion_eq_2025` and `rel_terrapower_eq_2025` second order are one sentence. Insights: Sakana and Black Forest Labs. Details in finding 15.

**4. Do restructured or abandoned deals show their current status?** In the register, yes: Wayve and Cursor are restructured, seven exits are terminated at zero, the OpenAI letter of intent is an open letter with a partial reconciliation, TuSimple says what is and is not known. In the reports, no: R9.md (b3) still says the letter was "replaced by $30 billion in the round" and lists TuSimple among exits; R7 (3) lists TuSimple under "Exited". One register inconsistency: `rel_firmus_eq_2026b` is status "definitive" with an insight saying Nvidia "made a follow-on investment" (finding 24).

**5. Is anything sourced to an excluded publication, or displayed on a single tier 2 source?** No excluded domain (1,052 tier 1, 6 tier 2, all Nikkei Asia). Three single-source or unsourced displays remain. `rel_reflection_eq_2025`: the insight, the wrong-way risk reason and both first order items describe cloud contracts known only from CNBC and Bloomberg reports that returned 403 (unconfirmed log row "Compute deals with SpaceX (up to $6.3B) and Nebius ($1B)"). `rel_firmus_eq_2026b` first order item 2: "talks for Nvidia to back Firmus afterwards" is the unconfirmed log row "Nvidia in talks to invest more after the IPO withdrawal", and the evidence attached (ev_110048) is about the listing, not the talks. `ent_firmus.credit.market_signals` items 2 and 3 carry figures (A$7.9 billion, 46 MW of 912 MW) on one article.

**6. Does the verdict claim more than the evidence supports?** `central_bank.json` no longer does: 299 words, "Not supported" for last resort, "not shown" for pricing and rescue, Nvidia's own CFO sentence cited. R9.md section (c) does: it still reports "lender of last resort partly supported (Nvidia backs firms with going-concern language ...)", the claim round 1 rated critical (finding 2).

**Deliverability: No.** Before this goes to a committee: fix the five critical findings; make R7 section (2) and the R9.md summary say what the system view says; put one bridge in one place and have the other quote it, with the equity purchases row filled and the date mismatch stated; merge the Anthropic and SpaceX credit blocks and regenerate the by-grade table; state under that table that OpenAI cannot be graded; fix the NAVER contradiction. The register file and the workbook totals can go as they are once the Reflection, Firmus and credit-merge records are corrected.

## NEW or REMAINING findings

### Critical

**1.**
> **Location:** `research/reports/R7_aggregates.md`, section "(2) How much of the headline total is legally binding today?", table and caveat; header line "91 relationships, 81 counted".
> **Problem:** The table was computed on commit 1c4f796 and contradicts the current register. It counts the CoreWeave initial order value as exposure and gives a cost-still-held figure that is the cash-paid figure. A reader comparing R7 with the system view finds gross differing by $8.3 billion.
> **Evidence:** R7: "Contingent maximum (4 relationships) | $113.7B", "Gross exposure (lower bound: 51 relationships have unknowns) | $183.6B", "cost of what is still held $32.2B", "The CoreWeave $6.3B in the contingent total is an initial order value, not a cap". `system_view.json` totals: contingent_max 107,360,340,000 across 3; gross 175,256,654,380; funded 30,196,314,380; count 80; lower_bound_count 50. spec/01 rule 4.
> **Fix:** Replace the six stale cells with: "Cash paid where stated (16 relationships) | $32.3B; cost of what is still held $30.2B (14 relationships)"; "Contingent maximum (3 relationships) | $107.4B, of which $105B is the PORTS-Pike cap, not in force before fiscal 2029, and $2.36B is in force (Nscale lease $0.86B, SB Energy placement $1.5B)"; "Gross exposure (lower bound: 50 relationships have unknowns) | $175.3B". Delete the caveat sentence about CoreWeave. Change the header and the lead-in to "92 records: 80 counted, 4 context, 8 remainders" and the commit to the current one. Add to `pipeline.checks` a check that fails when `R7_aggregates.md` or `R9.md` contains a "Gross exposure" or "Contingent maximum" figure that differs from `fmt.money` of the system view totals.

**2.**
> **Location:** `research/reports/R9.md` section (c): paragraph "Central bank test", "Decisions needed from Thomas" items 1 and 2, and the opening line "91 records: 82 counted exposure relationships, 2 context records, 7 unattributed remainders".
> **Problem:** The summary for the approver states the verdict and grades that round 1 rated critical and the register no longer holds. It tells Thomas that two named companies, one listed and one in registration, are graded Distressed.
> **Evidence:** R9.md: "lender of last resort partly supported (Nvidia backs firms with going-concern language, but its CoreWeave support ends at insolvency)"; "Both are Distressed now"; "against shareholders' equity of $266,666 million"; "it is 72% of gross exposure". `central_bank.json` last_resort verdict: "Not supported". `ent_sharonai.credit.grade`: "Insufficient information"; `ent_nscale.credit.grade`: "Watch". The guaranty is 59.9% of gross ($105 billion of $175.3 billion).
> **Fix:** Central bank paragraph: "Liquidity partly supported; collateral partly supported (SB Energy and Galaxy's noteholders cite Nvidia support, CoreWeave's lenders do not); pricing of money not testable; lender of last resort not supported (no rescue deal is sourced; SharonAI and Nscale say they rely on financing not yet committed). Where it breaks: guarantees of up to $118.0 billion (ev_50044) against shareholders' equity of $266.7 billion (ev_130001)." Decision 1: "Grading: going-concern language that ends in 'able to continue' (SharonAI, ev_80009) or doubt alleviated (Nscale, ev_40045) is no longer graded Distressed; SharonAI is Insufficient information and Nscale is Watch. Confirm." Decision 2: replace "72%" with "60%" and add "The totals now show it as signed but not yet in force. Confirm." Opening line: "92 records: 80 counted, 4 context, 8 remainders".

**3.**
> **Location:** `rel_reflection_eq_2025`: `insight_template`, `credit.wwr_reason`, `consequences.first_order[0]` and `[1]`.
> **Problem:** Four on-screen statements say Reflection rents Nvidia GPUs from other clouds and owes large cloud bills. The record holds two evidence ids, both about the investor list. The cloud contracts are known only from two news reports that could not be opened.
> **Evidence:** Rendered insight: "Nvidia is a named investor in Reflection, which rents Nvidia GPUs from other clouds, so the stake depends on it paying those bills." Record notes: "CNBC (2026-06-22) reports a SpaceX compute deal worth up to $6.3 billion; Bloomberg (2026-07-14) reports $1 billion of Nebius capacity. None cached (HTTP 403): needs quote." `research/unconfirmed.md`: "Reflection AI | Compute deals with SpaceX (up to $6.3B) and Nebius ($1B) | Tier 2 fetch blocked". spec/04: "If a relationship's existence is supported but its amount is not ... A relationship supported only by one tier 2 report is displayed with status 'Reported, unconfirmed' and no amounts."
> **Fix:** Insight: "Reflection names Nvidia among the investors in its latest raise; Nvidia's share is not disclosed, so the stake cannot be sized." `wwr_reason`: "Equity in an open model developer; loss is capped at an undisclosed cost and moves with the AI funding cycle." Delete both first order items and replace with one: "Reflection names Nvidia among investors in a $2 billion raise without stating Nvidia's share, so a lower Reflection price reaches Nvidia only inside its private holdings total." with evidence ev_90029, ev_90030. Move the second order item's lens unchanged.

**4.**
> **Location:** `rel_firmus_eq_2026b` `consequences.first_order[1]`; `ent_firmus.credit.market_signals[1]` and `[2]`; `loop_firmus.circularity_note`; `loop_sharonai.circularity_note`.
> **Problem:** (a) The consequence adds "talks for Nvidia to back Firmus afterwards", a claim the team's own log lists as blocked and not independent; the evidence attached is the Nikkei sentence about the listing. (b) Two market signals display figures from one tier 2 article, one of them an analyst's opinion. (c) The Firmus loop note states the withdrawal as fact. (d) The SharonAI loop note still points to the going-concern section as mattering, after finding 3.
> **Evidence:** Consequence: "One news report, unconfirmed, says Firmus withdrew its IPO; if talks for Nvidia to back Firmus afterwards lead to new equity, Nvidia's exposure would rise" with evidence ["ev_110048"], whose quote is "decided to withdraw its application to list on the Australian Securities Exchange". `research/unconfirmed.md`: "Firmus | Nvidia in talks to invest more after the IPO withdrawal | The Information blocked; Bloomberg cites it, so not independent". Signals: "Withdrawn offer sought up to A$7.9 billion (about $5.5 billion) (Nikkei Asia, single tier 2 source)"; "46 MW was built out of 912 MW contracted (opinion, single tier 2 source)". spec/04: "There is no label or exception that lets a single-source figure through."
> **Fix:** (a) Replace the consequence with: "One news report, unconfirmed, says Firmus withdrew its Australian listing application; if so, Firmus's next funding would again come from private investors such as Nvidia, Coatue and Blackstone." Keep ev_110048 and add ev_110033. (b) Delete market signals [1] and [2]; in their place, where the tier 1 figure is wanted, add "Firmus says contracted capacity across all customers is more than 900 MW" with ev_110047. Keep signal [0]. (c) Loop note: "One news report, unconfirmed, says Firmus withdrew its listing application (ev_110048)." (d) SharonAI loop note last sentence: "SharonAI says it must keep access to additional financing (ev_80010)."

**5.**
> **Location:** `data/register/entities.json` `ent_spacex.credit` (grade "Strong") and `ent_anthropic.credit` (grade "Insufficient information"); `pipeline/build_register.py` `merge_entity`; `R9_system_view.md` "By counterparty grade (internal)"; `research/gate_r/FIXES.md` line "17:".
> **Problem:** FIXES.md says 13 new credit blocks were applied. Two were not. `merge_entity` keeps whichever record has the longer JSON, and the older cluster blocks for Anthropic and SpaceX are longer than the new ones in `lead_credit.json`. The register therefore grades SpaceX Strong although the team has since sourced a top customer share that makes it Adequate, and leaves Anthropic, the second largest concentration, ungraded although a block grading it Adequate exists. The by-grade table is wrong by $10 billion in two rows.
> **Evidence:** FIXES.md: "Anthropic Adequate (424B4), SpaceX Adequate (10-Q; was Strong, top customer 34.5% now sourced)". `entities.json` `ent_spacex.credit.grade_reason`: "Customer concentration and rating not sourced." `ent_anthropic.credit.grade_reason`: "Only liquidity is sourced". `research/drafts/lead_credit.json`: ent_anthropic "Adequate", ent_spacex "Adequate". `build_register.py`: `hi, lo = (a, b) if richness(a) >= richness(b) else (b, a)`. spec/05 section 5: "Take the weakest of the sourced columns".
> **Fix:** In `merge_entity`, take a `source_file` argument and, when the incoming entity comes from a `lead_*.json` draft and has a `credit` block, set `out["credit"] = incoming["credit"]` after the merge. Rebuild, rerun `make evidence measure check`, regenerate the system view. Expected by-grade change: Anthropic's 2 relationships and $10 billion move from "Insufficient information" to "Adequate"; SpaceX's 1 relationship moves from "Strong" to "Adequate". Add a check that every `grade` in `lead_credit.json` equals the grade in `entities.json`.

### Major

**6.**
> **Location:** `rel_naver_eq_2026`: `insight_template`, `credit.notes`, `amounts.funded`; `system_view.json` `totals.committed_split_unknown` and bridge row "Unfunded equity commitments"; `rel_unattributed_equity_investment_commitments_2026_10_25` component "Less NAVER private placement".
> **Problem:** The same $1 billion is three things at once. The record's text says it is unpaid. The totals file it under "paid portion not disclosed". The remainder record subtracts it from Nvidia's unfunded commitments as unpaid, while the system view bridge leaves it out of the named unfunded figure.
> **Evidence:** Insight: "Nvidia signed to buy $1 billion of new NAVER shares with closing still pending". `credit.notes`: "Not yet funded as of 2026-11-23." Record notes: "No board resolution or closing has been found as of 2026-11-23, so funded stays unknown". `R9_system_view.md`: "Committed, paid portion not disclosed: $36.7 billion across 5". R7 section f: "less NAVER placement ... $1.0B".
> **Fix:** The sourced fact is that it was unpaid on 27 October 2026 and nothing has been disclosed since. Make the text say that and no more. Insight: "Nvidia signed to buy {committed_total} of new NAVER shares; no closing has been disclosed, so the stake rides on an AI factory using its chips." `credit.notes`: "Unpaid at 2026-10-27, when NAVER said it would promptly complete the share issue (ev_90068); no closing disclosed as of 2026-11-23." Keep the totals bucket. In the bridge, see finding 7.

**7.**
> **Location:** `R9_system_view.md` "Bridge to Nvidia's own disclosures" (built in `pipeline/system_view.py` `bridge`) against `R7_aggregates.md` "Bridge to Nvidia's own disclosures at 2026-10-25" and the eight remainder records.
> **Problem:** Two bridges in two reports give different "named" figures for the same Nvidia line, and the system view's figures do not match the remainder records it sits beside.
> **Evidence:** Private stakes: system view blank; R7 "$2.68B (Nscale $1.18B, SB Energy $1.5B, at cost)". Cloud service agreements: system view "$4.6 billion"; R7 "$0 (CoreWeave, IREN, Nscale named, no remaining balance stated)", and the remainder record subtracts nothing. Unfunded equity commitments: system view "$1 billion"; R7 "$3.5B (SB Energy $1.5B, NAVER $1B, Nscale $1B)", and the remainder record is $16.5 billion.
> **Fix:** Build the bridge from the remainder records, not from type sums: for each row, `named = disclosed aggregate - remainder value` using the record's `components`. That gives private stakes $2.68 billion, public equity $48.33 billion, guarantees $105.86 billion, neocloud $0, cloud service agreements $0, unfunded equity commitments $3.5 billion, leases $0, supply $0. Keep the $4.6 billion only in the note: "IREN and Nscale state contract values at signing of $4.6 billion; the balance still owed is not disclosed." Replace the R7 table with a sentence pointing to the system view bridge.

**8.**
> **Location:** `R9_system_view.md` bridge row "Equity purchases, nine months" and the "Totals" line "Funded and still held, at cost"; `pipeline/system_view.py`.
> **Problem:** The row that most directly tests the register is blank, and the totals are struck on 23 November while the bridge is struck on 25 October. $10 billion of the $30.2 billion funded (Anthropic, paid 20 November) falls after the bridge date and is not in any Nvidia figure in the table.
> **Evidence:** `rel_anthropic_eq_2026` `amounts.funded.as_of`: "2026-11-20". Funded amounts dated 2026-01-26 to 2026-10-25, equity only: Nscale preferred up to $1.18 billion, Nebius $2.0 billion, Marvell $2.0 billion, Lumentum $2.0 billion, Coherent $2.0 billion, Corning $0.5 billion, SB Energy $1.5 billion; total about $11.2 billion. Exhibit 99.3: "Purchases of equity securities (15,696) (3,706) (58,100) (4,952)".
> **Fix:** Have the pipeline fill the row: named = sum of eligible `funded` on EQ records with `funded.as_of` inside Nvidia's fiscal 2027 nine months (2026-01-26 to 2026-10-25), with the note "Dated, costed equity purchases in this register inside the period; the rest of Nvidia's purchases are not attributed. Nscale's figure includes rounds before the period." Add under Totals: "Totals are at 23 November 2026 and include the $10 billion Anthropic purchase of 20 November; the bridge compares against Nvidia's figures at 25 October 2026, before that purchase."

**9.**
> **Location:** `rel_openai_eq_2026` `amounts.funded.note` (absent), `insight_template`; `R9_system_view.md` "Top five concentrations", OpenAI row "Not disclosed".
> **Problem:** Round 1 fix 1(c) was not applied. The register says nothing is known about what Nvidia has paid OpenAI when its own figures bound it from below.
> **Evidence:** ev_120011: "Equity investments 5 11 2 2 — — 20". R7 section f attributes $3.5 billion of that $20 billion to SB Energy, NAVER and Nscale, leaving at most $16.5 billion for OpenAI and every other investee. `rel_openai_eq_2026` committed_total 30,000,000,000. Credit notes: "consistent with but not proof of tranche payments".
> **Fix:** Add `amounts.funded.note`: "Analysis: Nvidia's total unfunded equity commitments were $20 billion at 2026-10-25 (ev_120011). If the $30 billion OpenAI names is a binding commitment in that total, at least $10 billion had been paid by that date, and at least $13.5 billion after the $3.5 billion this register attributes to other investees. The exact amount is not disclosed." Concentration table cell: "Not disclosed; at least $10 billion by 25 October 2026 (analysis)". Leave `funded.value` null.

**10.**
> **Location:** `R9.md` section (b) items 3 and 4 and table a4; `R7_aggregates.md` answers (3) and (4); `R4.md` line 68; `R9.md` "Unconfirmed ... (46 rows)".
> **Problem:** Lists and counts written before the fixes. They contradict the register on five records.
> **Evidence:** R9.md (b3): "OpenAI $100 billion letter of intent, never definitive, replaced by $30 billion in the round"; "xAI stake converted into SpaceX shares"; "Arm, Applied Digital and six small 13F positions exited" (TuSimple is one of the six). R9.md (b4): "common equity 48 ... prepaying buyer 6 ... none 7". R7 (3): "Arm, Recursion, SoundHound, TuSimple, Nano-X, Serve, WeRide, Applied Digital | Exited". R7 (4): "common_equity | 49 | ... Meta (LOI)"; "prepaying_buyer | 6 | Amkor, KYEC, Corning". R4: "replaced in practice by the $30B round investment". Register: `rel_openai_eqc_2025` notes "no source says the letter of intent was terminated, restructured or replaced"; `rel_tusimple_eq_2023` "whether still held is not disclosed"; `rel_meta_eq_2026` seniority "none"; `rel_corning_pp_2026` type CX. `research/unconfirmed.md` has 47 rows.
> **Fix:** R9.md (b3) and R4: "OpenAI $100 billion letter of intent: no definitive agreement disclosed; followed by $30 billion in the 2026 round (analysis; no source links them)". "SpaceX shares at least partly from xAI stakes (origin not fully disclosed)". "Arm, Applied Digital and five small 13F positions exited; TuSimple left the 13F on delisting, holding unknown". Recount (b4) and R7 (4) from the register's `seniority` field with a one-line script and paste the output; move Meta to "none" and drop Corning from prepaying buyer (5). R7 (3) last row: remove TuSimple and add a row "TuSimple | Left the 13F on delisting; whether still held is not disclosed". R9.md: "47 rows".

**11.**
> **Location:** `R9_system_view.md` under "By counterparty grade (internal)" and after the loops are named; `R9.md` section (c).
> **Problem:** Three sentences round 1 asked for are missing: that OpenAI cannot be graded (finding 17), that no loop has a dollar on its return leg (25d), and in R9.md that no news source could be read (32). After finding 5 is fixed, 56 of 80 relationships and $137.1 billion of $175.3 billion gross (78%) remain "Insufficient information", and the reader is not told why.
> **Evidence:** By-grade row: "Insufficient information | 58 | ... | $147.1 billion". R9.md (c) "Loops": "No circularity ratio is computable for any loop" but still "Loops (11 ...)" with no statement that the NAVER loop is open.
> **Fix:** Under the by-grade table: "OpenAI, 77.0% of gross exposure, publishes no balance sheet and cannot be graded." (use `fmt.pct` of the concentration share). In R9.md (c) Loops: "Ten loops close through a supplier relationship and one (NAVER and Brookfield) is open at the closing leg; none has a disclosed dollar value on the return leg." At the top of R9.md (c): "Sources: company filings and releases only. No financial news source could be retrieved during this pass, so amounts reported by the press but not by a company are shown as not confirmed. 47 such claims are listed in the unconfirmed log."

**12.**
> **Location:** `pipeline/system_view.py` `tenor_bucket`; `R9_system_view.md` "By tenor".
> **Problem:** 76 of 80 relationships and all $107.4 billion of contingent exposure sit in "No stated maturity", including a guaranty the record describes as "Over 10 years". The table tells a credit reader nothing about tenor.
> **Evidence:** `tenor_bucket` reads only `r["dates"]["maturity"]`. `rel_openai_gu_2026.credit.tenor`: "Over 10 years: up to 20 years per building from each lease commencement". Table row: "No stated maturity | 76 | ... | $107.4 billion | $105 billion".
> **Fix:** Add an optional enum field `credit.tenor_bucket` (same five values) and have `tenor_bucket` return it when set. Set it on `rel_openai_gu_2026` ("Over 10 years"), `rel_nscale_gu_2025` ("2 to 5 years" on the five lease years stated, ev_170013), `rel_iren_lb_2026` ("2 to 5 years", five-year contract), `rel_sharonai_bk_2026` ("5 to 10 years", six years), `rel_sb_energy_eq_2026` contingent part ("Under 2 years", lapses 2027-05-15). Rename the first bucket "Equity or no stated maturity".

**13.**
> **Location:** `insight_template` on `rel_cohere_eq_2025`, `rel_wayve_eq_2024`, `rel_skild_ai_eq_2026`, `rel_sakana_eq_2024`, `rel_black_forest_labs_eq_2025`, `rel_ssi_eq_2026`, `rel_coreweave_lb_2023`.
> **Problem:** Each insight states a fact about the company that no evidence in the record supports, or sizes a stake the record calls undisclosed.
> **Evidence:** Cohere: "a sovereign AI vendor whose deployments use Nvidia hardware"; the record's five evidence ids are all about funding rounds. Wayve: "whose driving software runs on Nvidia DRIVE chips"; five ids, all about rounds. Skild: "trains on Nvidia simulation tools"; two ids, both about the raise. Sakana: "a small undisclosed stake"; one id, ev_90044, "with participation from Translink Capital, 500 Global and NVIDIA". Black Forest Labs: "a small undisclosed stake". SSI: "so the money likely returns as compute spending". CoreWeave rental: "which runs only Nvidia GPUs"; the supporting quote, ev_20127 "all of the GPUs used in our infrastructure today are NVIDIA GPUs", is on the entity, not the record. spec/01 rules 7 and 11.
> **Fix:** Cohere: "Nvidia has joined two Cohere rounds, the latest led by Schwarz Group, without stating an amount, so the stake cannot be sized." Wayve: "Nvidia entered Wayve in a round led by SoftBank and joined the next one; neither side states its amounts." Skild: "Nvidia's venture arm joined Skild AI's Series C led by SoftBank for an undisclosed amount, so the stake cannot be sized." Sakana: "Sakana AI names Nvidia among its Series A investors without an amount, so the stake cannot be sized." Black Forest Labs: "Black Forest Labs lists Nvidia among its existing investors; no amount has been disclosed by either side." SSI: "Nvidia calls its SSI investment substantial and pairs it with Vera Rubin access; no amount is stated (analysis: some may return as compute spending)." or drop the bracket. CoreWeave rental: add ev_20127 to the record's `evidence`. Alternatively attach a tier 1 quote for each product claim and keep the sentence.

**14.**
> **Location:** Consequences in `relationships.json` with an empty `evidence` list (112 of 255), in particular: `rel_naver_eq_2026` second order revenue_quality and first order [1]; `rel_figure_eq_2025` second order [1]; `rel_amkor_pp_2026` second order; `rel_nokia_eq_2025` second order; `rel_recursion_eq_2023` first order; `rel_unattributed_guarantees_2026_10_25` second order; `rel_unattributed_neocloud_agreements_2026_10_25` second order; `rel_anthropic_eq_2026` second order; `rel_unattributed_marketable_equity_2026_10_25` second order; `rel_openai_eqc_2025` all three; `rel_openai_eq_2026` first order [0].
> **Problem:** Statements of fact or causation about named companies with nothing attached. Two are true and merely uncited; the rest are the class round 1 finding 20 removed elsewhere.
> **Evidence:** NAVER: "conditioned on financing that will buy GPUs, so some of Nvidia's NAVER related revenue rests on a deal it helped trigger", while `loop_naver_brookfield` says "no allowed source states that the Brookfield vehicle's GPUs are bought from Nvidia". Figure: "a visible Nvidia exit would weigh on Figure's next valuation". Amkor: "Amkor funds its expansion with both new debt and Nvidia's advances", while the record says the customer link is analysis. Nokia: "weakens the signal Nokia used to justify issuing shares without pre-emptive rights"; no evidence on pre-emptive rights in the record. Recursion: "likely came back as service revenue". Guarantees remainder: "Lenders relying on the Unattributed power and systems credit support would reprice neocloud debt". Uncited but true: Anthropic "carry no underwriter lock-up" (424B4: "will not be subject to any market standoff agreement or lock-up agreement"); marketable remainder "$21.0B under short-term lock-up" (Exhibit 99.3: "Included $21.0 billion of investments that are subject to short-term lock-up restrictions").
> **Fix:** Add evidence records for the two true quotes above and attach them. NAVER revenue_quality: "Nvidia's NAVER investment was conditional on project financing for an Nvidia DSX AI factory (ev_90068, ev_30072); no source says the vehicle's GPUs are bought from Nvidia." Figure: "Brookfield and Nvidia invested in the same Figure round (ev_90042); no source ties the round's price to Nvidia." Amkor: "Nvidia says its Amkor agreements include prepayments to scale capacity (ev_30066); Amkor does not name the customer, so how much of its expansion Nvidia funds is not disclosed." Nokia: end the sentence at "within a year" and cite ev_50024, ev_50025. Recursion: delete "likely" clause; "Recursion agreed to train models on Nvidia DGX Cloud (ev_90020) in the same announcement as the investment." Delete the two remainder sentences about lenders. For the OpenAI items, attach ev_30021 and ev_120020 where they describe the letter's terms and label the rest "(analysis)". Then run the scan again and, for every remaining item with no evidence, either attach an id or add "(analysis)".

**15.**
> **Location:** `rel_lumentum_eq_2026` and `rel_coherent_eq_2026` second order; first order [0] on `rel_amkor_pp_2026`, `rel_kyec_pp_2026`, `rel_ibiden_pp_2026`, `rel_unimicron_pp_2026`, `rel_spil_pp_2026`; second order on `rel_commonwealth_fusion_eq_2025` and `rel_terrapower_eq_2025`; all 16 consequences on the eight remainder records.
> **Problem:** Sameness. The optics pair is identical apart from the name, which followed round 1's instruction ("Coherent: same form"); that instruction was wrong. The five supply items are one template. The remainder items all open with the placeholder entity name and read as machine output.
> **Evidence:** "Nvidia is both a shareholder and a committed buyer of Lumentum; neither discloses the size of the purchase commitment, so the share of Lumentum revenue that Nvidia funds cannot be measured." and the same with "Coherent". "If SPIL's dedicated lines are late, Nvidia's funding to SPIL is tied up and its advanced packaging supply tightens." "Lenders to Unattributed neoclouds rely on Nvidia's commitment". spec/05 section 6: "A consequence that would read the same for any company fails review."
> **Fix:** Lumentum: "Nvidia's preferred stock funds a new Lumentum fab and Nvidia has also agreed to buy from it (ev_60070, ev_30047); the purchase commitment is not sized, so the share of the fab's output Nvidia will take is unknown." Coherent: "Nvidia bought Coherent common stock in a placement and is a committed buyer of its optics (ev_30049, ev_60077); Coherent's largest customer was 20% of fiscal 2026 revenue (ev_190088) and is not named, so Nvidia's share cannot be measured." Supply records: keep the delay sentence on one record (Amkor) and give each of the others the one fact its evidence holds (site, product, amount or the absence of any amount); if a record has no such fact, leave one item saying so. Remainder records: rewrite without the entity name, for example "A default by a partner Nvidia does not name would become an Nvidia payment with no prior warning to readers."

**16.**
> **Location:** `insight_template` on `rel_unattributed_non_marketable_equity_2026_10_25`, `rel_unattributed_equity_investment_commitments_2026_10_25`, `rel_unattributed_neocloud_agreements_2026_10_25`.
> **Problem:** The insights present an upper bound as a point figure and say "no named deal" or "companies it does not name" where the record's own definition says named counterparties (OpenAI, Anthropic, SharonAI, Firmus) sit inside the figure unsized.
> **Evidence:** Insight: "Nvidia carries $59 billion of private company stakes that no named deal explains". Definition: "it is an upper bound because several named stakes, including OpenAI, have no disclosed funded amount". R7: "if OpenAI's $30B was fully paid by 2026-10-25, the remainder would be about $29.0B". Insight: "Nvidia has promised $16.5 billion of future equity to companies it does not name". Definition: "an upper bound because the unfunded parts of the OpenAI and Anthropic commitments are not disclosed". Insight: "up to $32 billion of neocloud capacity for unnamed partners"; definition: "SharonAI ... and Firmus are named but not quantified".
> **Fix:** "Up to {funded} of Nvidia's private stakes cannot be tied to a sized deal; OpenAI and other named stakes of undisclosed cost sit inside that figure." "Up to {committed_total} of Nvidia's unfunded equity commitments cannot be tied to a named deal; unpaid OpenAI and Anthropic amounts may sit inside it." "Nvidia stands behind up to {contingent_max} of neocloud capacity; SharonAI and Firmus are known partners, but no partner's share is disclosed."

**17.**
> **Location:** `R9_system_view.md` scenario lines for S2 (built in `pipeline/system_view.py` and `pipeline/scenarios.py`).
> **Problem:** (a) "compute commitments at risk: $646.1 billion across 7 counterparties" for Anthropic adds an "up to" amount that is cancellable on 90 days' notice ($120.5 billion), a terminable agreement ($41.3 billion), minimum commitments and $161.2 billion of Broadcom equipment leases, and prints the sum as one figure. (b) For SpaceX, "$60.2 billion across 2 counterparties" is Valor and Apollo GPU lease obligations, labelled "compute commitments". (c) Anthropic's definitive 2025 agreement is counted under "Conditional commitments or letters of intent". (d) Lines print raw record ids and repeat themselves.
> **Evidence:** "Equity loss: not computable; not computable for rel_anysphere_eq_2025". S2 Anthropic backlog entries: "SpaceXAI arrangements ... up to this amount into 2029 ... cancellable on 90 days notice"; "Five-year Broadcom master equipment leases (finance leases)". spec/01 rule 4.
> **Fix:** Print "Counterparty contracts that depend on this lab: up to $X across N (includes $Y stated as 'up to' or cancellable)", computing Y from entries whose description or label says "up to", "cancellable" or "terminable". Give lease obligations their own line: "GPU lease obligations of this lab: $60.2 billion across 2 lessors". Print "Other Nvidia commitments to this lab: 1 (up to $10 billion agreement of 2025, amount paid not disclosed)". Replace record ids with the relationship title and print "not computable" once.

**18.**
> **Location:** `entities.json` `credit.maturities_24m` on `ent_intel`, `ent_lumentum`, `ent_corning`, `ent_nokia`; `ent_coherent.credit.maturities_24m.note`; `ent_synopsys.credit.top_customer_share`.
> **Problem:** (a) Four blocks store debt due within 12 months in the 24 month field and grade the column on it. Each says "lower bound" in a note, but the rubric ratio is then understated and the column can read one grade too strong. (b) The Coherent note calls the revolver "$350 million"; the filing says $350 million was added to reach $700 million, and the block's own cash figure uses $669 million of availability. (c) Synopsys stores 0.1 as a top customer share on a quote about other years; the column is inferred, and with it the entity has two sourced columns, without it one.
> **Evidence:** `ent_intel` note: "Short-term debt due within 12 months only; debt due in months 13 to 24 not found"; grade reason: "the 10-K schedule adds $3.8 billion due in 2027". `ent_lumentum` note: "Current portion of debt, 12 months only". Coherent 10-Q: "$350 million of senior secured incremental revolving credit commitments were added, increasing the total availability under the 2025 Revolving Loans to $700 million". ev_190064: "accounted for 12.6%, and 13.5% of our consolidated revenue in fiscal 2024 and 2023". spec/05 section 5: "Debt due in 24 months ÷ cash plus undrawn".
> **Fix:** (a) For each of the four, add the second-year principal from the latest annual debt schedule as a component, as was done for Coherent and Amkor (Intel: the $3.8 billion due in 2027 the grade reason already cites), recompute the ratio and re-run the rubric; where no schedule is cached, state in `grade_reason` "12 month figure; column graded as a lower bound" and do not count the column as Strong. (b) Coherent note: "The $700 million revolver ($669 million available, ev_190087) matures 2027-07-01". (c) Synopsys: set `top_customer_share.value` to null with the note kept as analysis, and re-run the rubric; if only the debt column remains, the grade is "Insufficient information".

**19.**
> **Location:** `rel_amkor_pp_2026` `amounts.headline` (value 3,000,000,000; note "Should display as nearly $3 billion"); `pipeline/fmt.py` `amount_text`; headline group "other".
> **Problem:** Round 1 finding 27 remains. Tables, the workbook and the headline total show and add "$3 billion" for a figure the source gives as "nearly $3 billion".
> **Evidence:** `fmt.amount_text` of the amount returns "$3 billion". ev_30065: "totaling nearly $3 billion".
> **Fix:** Add an optional `qualifier` field to the amount schema with values "nearly", "about", "more than"; set "nearly" here; have `fmt.amount_text` prefix it and the workbook write it in the cell note; add to the Totals headline line "(one figure is stated as 'nearly')".

**20.**
> **Location:** every `amounts.market_value` (as_of 2026-09-30, source Nvidia Form 13F-HR); `rel_anthropic_eq_2026` (no market value); "Largest positions by current value where known".
> **Problem:** Round 1 finding 9(c) remains. The table headed "current value" is 54 days old, and the largest funded position, listed on 19 November, has no value.
> **Evidence:** spec/05 section 3: market_value is "Current value of a public stake", from the market data class, "timestamped". Table rows all "2026-09-30".
> **Fix:** Before publication, refresh each value from the market data source in spec/04 with a price timestamp, including the 120,481,927 Anthropic shares. Until then retitle the table "Largest positions by value at 30 September 2026 (Nvidia's holdings report)" and add the row "Anthropic | not yet valued | listed 2026-11-19 | Yes".

**21.**
> **Location:** `loops.json`: `loop_openai_equity_compute` leg 3; `loop_anthropic_gpu_clouds` summary; `loop_nscale` summary; `loop_nebius` summary.
> **Problem:** (a) The OpenAI loop keeps a CoreWeave contract of March 2025 as a leg of a round that closed in March 2026; round 1 removed the Azure leg for the same reason. (b) "All three buy Nvidia GPUs" has legs for two; Lambda has none. (c) "so Nvidia's cash and credit come back as hardware demand" asserts a flow the note says has no dollar value. (d) "relies on Nvidia for all its GPU chips" adds "all" to the source.
> **Evidence:** Leg: "ent_openai -> ent_coreweave compute_contract 11900000000 up to (contract) ... 2026-03-02", described in S2 as "CoreWeave master services agreement of March 2025". `loop_nscale.circularity_note`: "gives no dollar value. Ratio not computable." ev_40061: "We currently rely on Nvidia for the GPU chips we use".
> **Fix:** (a) Move the CoreWeave leg to the note with its date, or relabel `amount_label` "up to (contract signed March 2025, before the round)". (b) "SpaceX and Nscale are Nvidia customers or buy Nvidia GPUs; Lambda's purchases are not on file." (c) "so Nvidia's cash and credit can come back as hardware demand; no amount is disclosed." (d) "Nebius says it relies on Nvidia for the GPU chips it uses."

### Minor

**22.**
> **Location:** `rel_nokia_eq_2025` `insight_template` and second order item.
> **Problem:** "then sold most of them within a year" states a sale; the record says no source shows one.
> **Evidence:** `holding.note`: "No allowed source states why or when Nvidia sold." Intel's insight for the same pattern: "its later holdings reports show a smaller stake".
> **Fix:** "Nvidia paid {funded} for new Nokia shares tied to an AI radio partnership, and its latest holdings report shows fewer than half of them."

**23.**
> **Location:** `rel_anthropic_eq_2026` `amounts.funded.evidence`.
> **Problem:** The funded amount cites only the prospectus sentence "will purchase"; the closing evidence is cited in the reconciliation text but not on the amount.
> **Evidence:** ev_120038: "NVIDIA Corporation (“NVIDIA”) will purchase 120,481,927 shares". Reconciliation: "concurrent private placement closed (ev_120069, ev_120070)".
> **Fix:** Add ev_120069 to `amounts.funded.evidence`.

**24.**
> **Location:** `rel_firmus_eq_2026b` `status` ("definitive") against `insight_template`.
> **Problem:** The insight says Nvidia "made a follow-on investment"; the status and source say participation in a committed round. The wording came from round 1.
> **Evidence:** ev_110033: "The round includes follow-on participation from Coatue and NVIDIA".
> **Fix:** "Firmus names Nvidia as a follow-on participant in its latest round for an undisclosed amount, ranking behind a large debt facility led by Blackstone."

**25.**
> **Location:** `rel_corning_pp_2026` `status` ("definitive"), `claim_basis` ("filed"); `research/seed_status.csv` row C6.
> **Problem:** A context record whose link to Nvidia is analysis is still labelled definitive and filed; the seed row lists "a $1.0B Corning deposit" among named prepayments found.
> **Evidence:** Insight: "Corning does not name the customer, so Nvidia's exposure is unconfirmed."
> **Fix:** `claim_basis` to the enum value for analysis or inference; seed row: "... and a $1.0B Corning customer deposit whose depositor is not named (context only)".

**26.**
> **Location:** `pipeline/datapack.py` Summary tab; variable `closed` in `type_tab`.
> **Problem:** The Summary shows "Contingent maximum" as one column with no split between in force and not in force, and carries no bridge, so the workbook's first page still reads as round 1's totals did. `closed` is computed and never used.
> **Evidence:** `cols` list in `build()`; `closed = "TRUE" if ...` has no reader.
> **Fix:** Add a Summary column "of which not yet in force" fed by a type-tab formula on the "Contingent in force?" column, add the bridge as a block under the tie-out, and delete `closed`.

**27.**
> **Location:** `R7_aggregates.md` (ev_10001, ev_130024, ev_50046, ev_50055), `R9.md` (ev_130024), `R8.md` (ev_170018), `R2.md` (eight ids), `R4.md` (ev_50066, ev_50067).
> **Problem:** Reports cite evidence ids that are not in `data/register/evidence.json`, beside figures such as the 14%, 11%, 11% customer shares and "$150B to $200B" per generation.
> **Evidence:** Diff of `re.findall(r"ev_\d+")` on each report against the evidence store.
> **Fix:** Add the records from `research/evidence/*.jsonl` to the store through an `evidence` list on `nvidia_financials.json` or the relevant entity, or mark each such citation "(working evidence, not in the register)". Extend `check_text_citations` to the reports listed in Gate R.

**28.**
> **Location:** `R9_system_view.md` Totals line "Committed, confirmed not yet paid: $1 billion across 1"; `rel_uk_ai_startup_program_eqc_2025` insight; `central_bank.json` `where_the_analogy_breaks`.
> **Problem:** (a) The one confirmed-unpaid amount, Nscale's second $1.0 billion, was due to close "on or about 16 November 2026", a week ago; the line carries no date. (b) "Nvidia announced a sterling headline" is register jargon on screen. (c) "the OpenAI guaranty alone is $105 billion, unsecured" can be read as saying the guaranty is unsecured; the source point is that Nvidia's reimbursement claim on OpenAI is unsecured.
> **Evidence:** R9.md a4: "The second $1.0 billion 'NVIDIA Sale' was due around 2026-11-16; closing unconfirmed". ev_30008 as described in R9.md: "OpenAI's unsecured reimbursement promise".
> **Fix:** (a) Append "(as of the Nscale filing of 12 November 2026; closing was due about 16 November and is not yet confirmed)". (b) "Nvidia announced an amount in pounds for the UK startup program with no named recipients, so none of it counts as exposure until deals close." (c) "the OpenAI guaranty alone is $105 billion, with only an unsecured claim on OpenAI in return" and trim two words elsewhere to stay under 300.

**29.**
> **Location:** `R9.md` section a1 to a4 tables.
> **Problem:** The tables describe the register before the fixes ("inside the $43 billion committed total", "replaced in practice by") with no marker that they are a historical log, in a file that also holds the live summary for Thomas.
> **Evidence:** R9.md a3: "the amount is display eligible and inside the $43 billion committed total".
> **Fix:** Add under the heading "(a) Quality review": "Findings as raised before the fixes of 23 November 2026; see `research/gate_r/FIXES.md` for what was applied. Figures in these tables are superseded."

## Self-audit

Every finding names a record and field or a file and section, quotes the source, record or rule, and gives replacement text or a computable instruction. Findings 15 and 24 correct wording that round 1 itself supplied. Finding 9 rests on an assumption stated in the fix (that OpenAI's $30 billion is inside Nvidia's commitments table); it is to be labelled analysis and does not change any total. Not tested in this round: the rendered workbook cells (formulas were traced in code, not recalculated in a spreadsheet engine), link liveness, and the credit blocks for Meta, Microsoft, Marvell, Amkor, SB Energy and Nebius beyond reading their grade reasons and evidence quotes.
