# Gate R summary for Thomas

**Date:** 23 November 2026. **Status:** research complete, waiting for your approval. No application code has been written.

Everything below uses confirmed figures only: a number counts only if a company filing, a company release or two independent named publications contain it, and the exact quote was found in a saved copy of the source.

## What was built

| Item | Count |
|---|---|
| Relationships in the register | 92 records: 80 counted, 4 context, 8 unattributed remainders |
| Counterparties and second-ring parties | 108 |
| Citations, each tied to a saved source and a quote | 1,094 |
| Site and financing records | 27 |
| Timeline events | 135 |
| Circular flows mapped | 11 |
| Seed hypotheses | 34: 13 confirmed, 18 modified, 3 killed |
| Claims with no usable source, kept out | 47 (logged in `research/unconfirmed.md`) |

## The numbers

| Measure | Amount | What it means |
|---|---|---|
| Funded and still held, at cost | $30.2 billion | Cash Nvidia paid for stakes it still holds, where a source states the cost |
| Committed, confirmed not yet paid | $1.0 billion | Signed and shown as unpaid by a source |
| Committed, paid portion not disclosed | $36.7 billion | Binding, but no source says how much has been paid (OpenAI's $30 billion is most of it) |
| Contingent maximum | $107.4 billion | The most Nvidia could be made to pay under guarantees and backstops |
| of which not yet in force | $105 billion | The lease guaranty where OpenAI is tenant; it cannot be called before the first building is ready, expected in Nvidia's fiscal 2029 |
| Gross exposure | at least $175.3 billion | The four lines above added together |
| Headline announced | $307.1 billion | What was announced. Never added to exposure |

Fifty of the 80 relationships are lower bounds, because at least one part is undisclosed.

## What the register cannot see, stated plainly

Nvidia's own accounts show far more than can be tied to named deals.

| Nvidia reports (25 October 2026) | Total | Named and sized here |
|---|---|---|
| Private stakes, carrying value | $61.6 billion | $2.7 billion at cost |
| Guarantees, maximum | $118 billion | $105.9 billion |
| Neocloud agreements, maximum | $32 billion | $0 (partners known, shares undisclosed) |
| Unfunded equity commitments | $20 billion | $3.5 billion |
| Equity purchases in nine months | $58.1 billion | $10.5 billion (18%) |
| Data center leases signed, not started | $74 billion | $0 |

Two further limits:

- **No news source could be read.** Bloomberg, Reuters, the Wall Street Journal, the Financial Times, CNBC and The Information all blocked automated reading. Almost every figure therefore rests on filings and company releases, and 53 of 80 relationships are disclosed by one side only. Reported figures that could not be read are logged as "needs quote" in `research/reports/R4.md`.
- **OpenAI is 77% of gross exposure and cannot be graded.** It publishes no balance sheet.

## Main findings

1. **Guarantees are the story, not equity.** Nvidia's disclosed guarantees rose from under $1 billion in October 2025 to $118 billion in October 2026. $105 billion is one set of lease guaranties at an Ohio campus where OpenAI is the tenant, and Nvidia can recover only from OpenAI.
2. **The $100 billion OpenAI deal is still a letter of intent.** No definitive agreement has been disclosed. A separate $30 billion equity commitment is named in OpenAI's own release; Nvidia has not disclosed it.
3. **Nvidia's position on financing customers reversed inside six months.** Its annual report in February 2026 said it had entered no financing arrangements. By August it described guarantees, credit support and capacity backstops.
4. **Several counterparties have Nvidia on every side.** At Nscale it is shareholder, lender, lease guarantor and customer. At CoreWeave it is shareholder, supplier, renter and buyer of unsold capacity, though that support ends if CoreWeave is insolvent for 90 days.
5. **Two releases overstate what the other side filed.** Nvidia said it "will invest $3 billion" in Meta; Meta's prospectus calls the interest not binding. Nvidia said $1.5 billion for SB Energy; SB Energy's filing shows $3.0 billion, half of it conditional on an IPO.

## Is Nvidia a central bank?

| Function | Verdict |
|---|---|
| Supplying liquidity | Partly supported |
| Standing behind collateral | Partly supported |
| Setting the price of money | Not testable |
| Lender of last resort | Not supported |

Nvidia gives equity and credit support to its buyers from a finite balance sheet. Price setting and rescue are not shown.

## How it was checked

- **Automated checks:** 37 tests and every check in the spec pass. They reject a quote that is not in the source, a single-source figure, a banned source, and a headline counted as exposure.
- **Independent re-sourcing:** three fresh agents re-sourced the 43 largest and least settled claims without seeing the research. No dollar figure was found wrong. Nine status and classification fixes were applied.
- **Critic review, three rounds:** the critic found real faults each round and the totals changed as a result (gross fell from $187 billion to $175.3 billion). By round three every total tied to the critic's own recomputation and no fabricated quote was found in any round. The remaining faults were in generated summary text, now driven by explicit fields with tests. The closing check result is in `research/gate_r/critic_closing_check.md`.
- **Evidence pack:** `research/Nvidia_Exposure_Datapack.xlsx` ties to the register to the dollar.

## Decisions needed from you

1. **Approve the register** so the application build can start. The approval date becomes the Gate R cutoff.
2. **Is this GitHub repository private?** If yes, I will also commit the six short news excerpts used for verification.
3. **The $105 billion guaranty:** show it at full value with a "not yet in force" label (current treatment), or show it on its effectiveness schedule?
4. **Paywalled news:** will you paste the ten priority quotes listed in `research/reports/R4.md` so those private-company figures can be shown, or should they stay "Not confirmed"?
5. **Letter grades on the public page:** off by default, as the spec recommends. Keep off?
6. **Groq and Hugging Face:** left off the map as purchases, not credit exposure. Confirm.
7. **Legal read:** the CoreWeave order's insolvency termination clause should be reviewed before the Stress view relies on it.

## Where things are

| File | What it is |
|---|---|
| `research/Nvidia_Exposure_Datapack.xlsx` | Evidence pack: one tab per exposure type, source and date beside every amount |
| `research/reports/R9_system_view.md` | Totals, bridge, concentrations, scenarios |
| `research/reports/R9.md`, `R7_aggregates.md`, `R8.md`, `R4.md`, `R2.md` | Closing review, aggregates, second ring, news log, filings sweep |
| `research/gate_r/` | Re-sourcing results, three critic rounds, the fix log |
| `data/register/` | The register itself |
