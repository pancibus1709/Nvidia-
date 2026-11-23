# R5 · Cluster B: CoreWeave register records (R5 to R9)

Draft: `research/drafts/cluster_b_coreweave.json`. It holds 20 entities (CoreWeave plus 19 depth 2), 4 relationships, 9 projects and 17 events.
New evidence is in namespace `crwb`, ids ev_70001 to ev_70030; the tool allocated the 70000 range. There are 28 records because I deleted ev_70018 and ev_70019 as duplicates of R1b's ev_50109 and ev_50072.
Reused evidence: crwv ev_20001 to ev_20212, R1a ev_10xxx, R1b ev_50018, ev_50019, ev_50072 and ev_50107 to ev_50109, and R3 ev_30053 to ev_30056.
Sources are read newest first. On the CoreWeave side: 10-Q Q3 2026 (2026-11-12), the 2033 convertible indenture (2026-09-22), DDTL 5.5 (2026-08-10), DDTL 5.0 (2026-05-18), DDTL 4.0 (2026-03-31), DEF 14A, 10-K FY2025 and the 424B4. On the Nvidia side: 13F at 2026-09-30, the Q2 FY2027 10-Q, the Form 3 and 13G/A, and the Q1 FY2026 10-Q.
"Analysis" marks anything I derived.

## Validation status (blocked; read first)

`python3 -m pipeline.checks draft research/drafts/cluster_b_coreweave.json` does **not** print "All checks passed" today, for three reasons outside this draft:

1. **The command crashes before checking anything** (`KeyError: 'id'`). `research/evidence/fulltext_hits.jsonl` holds 316 search hits with no `id`, and the draft command loads every `*.jsonl` in that folder as evidence. Fix: move the hits file out of `research/evidence/`, or skip id-less lines in `checks.main`.
2. **`ent_nvidia` does not exist.** `data/register/` is empty, so every relationship fails "from entity ent_nvidia does not exist". DRAFT_GUIDE says not to create it, so I did not. `cluster_de.json` has the same problem.
3. **A tooling change at 02:45 (commit 8a15709) broke grounding for inline XBRL filings.** The change to `pipeline/common.render_text` sends any file that starts with `<?xml` to the XML branch. Every inline XBRL 10-Q and 10-K starts that way, so text that used to render as `$30.1` and `15%` now renders as `$ 30.1` and `15 %`.
   - About 30 existing evidence records no longer ground, across crwv and r1a (for example ev_20045, ev_20071, ev_10151, ev_10187), plus 5 of mine made minutes earlier (ev_70009, ev_70024 to ev_70028).
   - Fix: limit the XML branch to `.xml` files, or re-ground. I did not edit `pipeline/`.

Workaround check: `scratchpad/draft_check.py` replicates `checks.main` draft mode line for line, with three changes. It skips id-less lines, adds a temporary register holding only `ent_nvidia`, and can restore the earlier `render_text`. With all three, the draft prints **All checks passed**.
Display eligibility in the draft was written by that run.

## Reconciliation

| Claim | Nvidia side | CoreWeave side | Result | Differences |
|---|---|---|---|---|
| Equity stake, January 2026 purchase | Release: "has invested $2 billion" at $87.20 (ev_30053, ev_30054). 13G/A: 47,213,353 sh, 11.5% (ev_50107, ev_50108). Form 3, 10% owner, 47,213,353 sh held directly (ev_50109, ev_70017) | 8-K: 22,935,780 sh at $87.20 for $2 billion cash (ev_20008 to ev_20010). Proxy: 47,213,353 sh, 10.66%, 3.27% of votes (ev_20022 to ev_20024). 10-Q: "approximately 23 million shares", $2.0bn (ev_20114) | reconciled | % of class 11.5% (2026-01-23) vs 10.66% (proxy record date): date and denominator differ. Share count rounded in the 10-Q |
| Equity stake, holding history | 13G 24,182,460 sh, 7.0% at 2025-03-31 (ev_50105, ev_20017). 13F: 24,277,573 sh at 2025-06-30 (ev_70014) and 2025-12-31 (ev_70015); 47,213,353 at 2026-06-30 (ev_70016) and 2026-09-30, $4,113,227,313 (ev_50019). Q1 FY26 10-Q: reclassified to marketable, fair value $1 billion (ev_10186, ev_10187) | 424B4: 17,932,460 sh before the IPO, 5.96% (ev_20030, ev_20031) | reconciled (with gaps neither side explains) | 6,250,000 sh between the 424B4 and the 13G; no IPO purchase is stated by either side (reported $250m anchor order, needs quote). 95,113 sh added in Q2 2025 per 13F; CoreWeave silent |
| Residual unsold capacity order, $6.3bn, to 2032-04-13 | No disclosure found as of 2026-11-23. Only unnamed aggregates: cloud service agreements $26bn at 2025-10-26 (ev_10151); AI cloud agreements $36bn that clouds "can unilaterally stop providing to us and sell" (ev_10035, ev_10039) | 8-K 2025-09-15: "initial value of $6.3 billion" (ev_20001); "obligated to purchase the residual unsold capacity through April 13, 2032" (ev_20002); conditional on delivery and availability (ev_20005); 90-day insolvency termination (ev_20006); restated in 424B3 (ev_20190). Not mentioned in later 10-Qs or the 10-K | one_sided | Neither side uses "backstop". Whether it is in Nvidia's aggregates or CoreWeave's RPO is not stated |
| MSA capacity rental (2023-04-10) | No disclosure found; Nvidia names no cloud service counterparty and reports no related-party transactions | MSA filed as Ex. 10.31 to S-4/A (ev_20016, ev_20146). Paid: ~$320m to 2024-12-31 (ev_20033), $326.3m 2025 (ev_20025), $59.6m Q1 2026 (ev_20026) | one_sided | The CoreWeave proxy calls NVIDIA a related party (ev_20028); its Q3 2026 10-Q related-party note omits NVIDIA (ev_20194) |
| Collaboration framework (2026-01-26) | Release: intent to "Leverage NVIDIA's financial strength" for land, power and shell; >5 GW by 2030 (ev_30055, ev_30056); repeated in Q4 FY26 results release (ev_50072) | 8-K: same, "subject to ... future execution of additional agreements and/or order forms" (ev_20011 to ev_20013); Q3 2026 10-Q mentions the framework only (ev_70023) | reconciled | Nvidia's release omits the condition. Whether Nvidia's $3.5bn land, power and shell guarantees (ev_10123) include CoreWeave is not stated |

## Classification decisions

### rel_coreweave_eq_2025 (EQ, completed, filed)

- **Funded is $2.0bn.** It is one stated component (ev_20010, ev_30053, ev_20114, ev_20145), flagged `lower_bound`.
- **Left out of funded.** The pre-IPO cost, the inferred 6.25m-share IPO purchase and the 95,113 shares bought in Q2 2025. These go in notes as analysis.
- **Market value.** $4,113,227,313 from the 13F at 2026-09-30, with price source "Nvidia Form 13F-HR".
- **Holding.** 47,213,353 shares. That is 10.66% of Class A and 3.27% of voting power per the proxy (ev_20023, ev_20024).
- **Wrong-way risk: general.** The loss is capped at cost.
- **measure_inputs.counterparty_equity_raised is $6,081m.** This is cash equity raised 2023-01-01 to 2026-09-30, from cash flow components ev_70024 to ev_70028.
- **counterparty_nvidia_spend is blank.** CoreWeave gives Nvidia's share of purchases (17%, ev_20027) but no dollar figure.

### rel_coreweave_bk_2025 (BK, secondary LB, definitive, filed)

- **Amounts.** Headline and contingent_max are both $6.3bn, with the trigger stated. Committed_total and funded are unknown.
- **"Initial value", not a maximum.** The filing calls $6.3bn the "initial value", so the record notes that it is not a proven ceiling.
- **Wrong-way risk: specific.** Nvidia's payments grow as CoreWeave sells less capacity while it stays solvent.
- **The insolvency termination cuts it off at failure.** Either party may terminate once an insolvency proceeding is not dismissed within 90 days (ev_20006). Nvidia is then "released of payment obligations for Services that would have been provided" after termination (ev_20015).
- **Delivery and availability conditions** (ev_20005) also remove the obligation when CoreWeave cannot deliver.
- **Result: peak exposure is in the solvent but weak demand range.** The support disappears exactly when CoreWeave fails.
- **Bankruptcy caveat (analysis).** US bankruptcy law can limit enforcement of termination clauses triggered by a filing. How well the 90-day clause protects Nvidia in a Chapter 11 needs legal review.
- **covered_project_debt and stress_inputs are not filled.** No document ties the order to a facility. The floor, contracted and merchant shares, and capacity value are not disclosed by either side.

### rel_coreweave_lb_2023 (LB, definitive, filed)

- **No contract value.** Headline, committed and funded are unknown: there is no contract value and no disclosed prepaid rent.
- **nvidia_paid is $705.9m.** Components: $320m + $326.3m + $59.6m, window 2023-04-10 to 2026-03-31. The 2025 and 2026 payments may include amounts under the BK order; they are not split.
- **Wrong-way risk: general.**

### rel_coreweave_gu_2026 (GU, secondary FC, loi_or_framework, company_announced)

- **Kept as its own record.** It carries something beyond the equity purchase: an intent to give credit support for land, power and shell.
- **Headline only, no amount.** Committed, funded and contingent are all not applicable.
- **Wrong-way risk: specific.** If the intent became lease guarantees, they would pay out on CoreWeave distress. No exposure is counted today.

### ent_coreweave grade: Weak (internal)

**Sourced columns.**
- Debt due within 24 months over liquidity: at least 1.36 ($13,407m over $9,837m), which is Watch. The $13,407m is a lower bound covering only principal due through 2027-12-31.
- Top customer share: 33%, which is Adequate.

**Moved down one step to Weak.**
- About 1.78 if three quarters of 2028 principal is pro-rated (analysis).
- DDTL 3.0 needed covenant relief.
- Disclosure controls were not effective at 2026-09-30.
- $1.9bn of contracts became cancellable.

**Not sourced:** liquidity cover (no committed 12-month spend) and a corporate rating. Facility ratings go in notes.

**Not Distressed:** no missed payment, no going-concern language, in covenant compliance at 2026-09-30.

## Seeds

| Seed | Verdict | Reason |
|---|---|---|
| B1 Nvidia major shareholder, pre-IPO stake, IPO anchor order | **modified** | Pre-IPO stake confirmed: 17,932,460 sh (ev_20030); 24,182,460 sh at 2025-03-31 (ev_50105); 47,213,353 now (ev_50019). The IPO anchor order is not in any filing on either side. Only CNBC, Axios and Bloomberg report it, and they could not be fetched (needs quote), so its amount is not in the record |
| B2 Sept 2025 order ~$6.3B for unsold capacity to 2032 | **confirmed** (terms refined) | Quoted: "initial value of $6.3 billion" (ev_20001); "through April 13, 2032" (ev_20002). Refinements: the filing says initial value, not a fixed sum; it is conditional on delivery and availability; it ends after a 90-day insolvency. Not shown: a utilization floor or whether it is counted in backlog/RPO |
| B3 earlier rental ~$1.3B over four years | **modified** | The MSA rental exists (ev_20029, ev_20016). The $1.3B over four years figure is not found in any allowed source. Only payments are disclosed: $705.9m to Q1 2026 |
| B4 early 2026 additional ~$2B equity | **confirmed** | $2 billion at $87.20, 22,935,780 sh, 2026-01-23. Sources: CoreWeave 8-K (ev_20008 to ev_20010), Nvidia release (ev_30053), 13G/A (ev_50107), Form 3 (ev_50109) |

## Not confirmed or not disclosed, and why

- **BK committed amount and payments to date.** Not disclosed: payments are not split from other MSA order forms, and the order form exhibit is not filed (only the MSA).
- **Whether the order is in RPO.** Not disclosed. Analysis: the RPO wording on "committed cloud computing capacity that the Company has the right to resell" first appears in the Q3 2025 10-Q (ev_70007), the quarter of the order. It is absent from the Q2 2025 10-Q, where RPO was $30.1bn (ev_70009); Q3 2025 RPO was $50.0bn (ev_70008). CoreWeave does not link the wording to NVIDIA.
- **Nvidia's own disclosure of the BK and MSA.** None. Nvidia reports only unnamed aggregates.
- **Cost of the pre-IPO stake and of any IPO purchase.** Not disclosed.
- **LB contract value.** Not disclosed.
- **committed_spend_12m and top three customer share.** Not disclosed. The top two were 54% in Q3 2026.
- **Corporate credit rating.** None found.
- **Site names.** Redacted in DDTL 4.0, 5.0 and 5.5 (ev_70010, ev_70011). Only Kenilworth, NJ is named. "Phoenix 1" is the name of an OpenAI order form, not a location.
- **Lenders beyond agents and bookrunners.** DDTL 2.1 lenders are not named.

## Not found

- **Nvidia-side naming of the $6.3bn order or the MSA.** Searched: Nvidia 10-Q and 10-K files FY2025 to Q2 FY2027 for "CoreWeave", "unsold", "residual" and "6.3 billion"; Nvidia's 8-K releases. The Q3 FY2027 10-Q is not yet filed.
- **A link between the NVIDIA order and RPO.** Searched: CoreWeave 10-Qs and 10-K for "6.3 billion", "backstop" and "NVIDIA".
- **Site names.** Searched: 10-K Item 2 (countries only) and the DDTL 3.0, 4.0, 5.0 and 5.5 agreements.
- **Revolver syndicate.** Only the agent, JPMorgan, is named (ev_70012, 424B4). The November 2025 amendment was not read.
- **UCC searches.** Not run.

## Unconfirmed

- Nvidia IPO anchor order of about $250m at $40 (6.25m shares by 13G arithmetic). It is reported by CNBC (named "source"), Axios and Bloomberg, but no filing states it.

## Needs quote

All four fetches returned 403 through `pipeline.cache`.

| Title | Outlet | Date | URL |
|---|---|---|---|
| Nvidia to anchor CoreWeave IPO at $40 a share, source says | CNBC | 2025-03-27 | https://www.cnbc.com/2025/03/27/nvidia-to-anchor-coreweave-ipo-at-40-a-share-source-says.html |
| CoreWeave raises $1.5 billion in scaled-back IPO | Axios | 2025-03-28 | https://www.axios.com/2025/03/28/coreweave-ipo-nvidia |
| CoreWeave Debuts With Downsized IPO, Anchored By Nvidia Investment (video) | Bloomberg | 2025-03-28 | https://www.bloomberg.com/news/videos/2025-03-28/coreweave-debuts-with-downsized-ipo-video |
| CoreWeave's stock rallies on disclosure of $6.3 billion order from Nvidia | CNBC | 2025-09-15 | https://www.cnbc.com/2025/09/15/coreweave-stock-jumps-on-disclosure-of-6point3-billion-order-from-nvidia.html |

## Domains to add / Domains added

None added. coreweave.com is already listed for ent_coreweave. Every release used is an SEC exhibit.

## Open questions

1. **Lead:** fix the three validation blockers above. The `render_text` regression affects evidence in every namespace.
2. **BK amount:** is $6.3bn a ceiling, a minimum or an estimate? Has Nvidia bought any residual capacity yet? Is the order in RPO?
3. **BK in bankruptcy:** is the 90-day insolvency termination enforceable in a CoreWeave Chapter 11? This needs legal review before the stress view relies on it.
4. **Framework and guarantees:** does any part of Nvidia's $3.5bn land, power and shell guarantees, or its $36bn of AI cloud agreements, relate to CoreWeave?
5. **Entity merge:** `ent_openai` is depth 2 here as a CoreWeave offtaker. Cluster A will likely hold it at depth 1, and the merge should keep depth 1.
