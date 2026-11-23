# 02 · Research Protocol

Ten sequences, run in order, all required. Each ends with a sequence report in `research/reports/R#.md` and a commit. The guiding principle: **start from what Nvidia was legally required to disclose, then follow the money outward, then check every claim against the other party.**

---

## R0 · Setup and scope

1. Create the repository layout from `10_BUILD_PLAN.md`. Build the research tooling now: `pipeline/edgar.py` (SEC client), `xbrl.py`, `extract.py`, the document cache, `schema/enums.json` and all JSON Schemas from `06`, and `pipeline/checks.py` with every automated check in `09`, grounding included. Write tests for the checks with fixtures. Every record written from R1 onward must pass `make check`.
2. Confirm `SEC_USER_AGENT` is set. If not, stop and ask Thomas to set it. Throttle SEC requests to at most 8 per second; cache every response to `research/cache/` with its retrieval timestamp so the work is reproducible and nothing is fetched twice.
3. Write `research/SCOPE.md`: the window (1 Jan 2023 to today, plus older relationships still active), the exposure types from `05`, the source tiers from `04`.
4. Load `03_SEED_REGISTER.md` into `research/seed_status.csv` with a status column: `unverified`, `confirmed`, `modified`, `killed`. Every seed must end in one of the last three.

**Key identifiers.** Nvidia Corporation, CIK `0001045810`. Fiscal year ends on the last Sunday of January, so "fiscal 2026" is mostly calendar 2025. Record both fiscal and calendar dates on every Nvidia figure.

---

## R1 · The anchor: Nvidia's own filings

Goal: extract everything Nvidia itself disclosed about money it has put at risk outside its own operations. This is the floor of the map, and the only part with legal weight.

**Filings to pull** (from `https://data.sec.gov/submissions/CIK0001045810.json`): every 10-K and 10-Q in the window, every 8-K, every 13F-HR, every SC 13D and SC 13G (and their 2024+ successors on Schedule 13D/G electronic forms) that Nvidia filed as the reporting person, every Form 3 or 4 Nvidia filed as a 10% owner of another issuer.

**Read these sections in every 10-K and 10-Q**, and write each disclosed item as an evidence record in `data/register/evidence.json` (the canonical store, schema in `06`, with cache path, hash and locator) plus a working note in `research/evidence/nvda_filings.jsonl` if useful. Capture accession number, section, note number, verbatim figure and period end date:

| Section | What to look for |
|---|---|
| Note: Investments / Fair value | Marketable equity securities (by issuer where named), non-marketable equity securities carrying value, gains and losses, impairments, new investments in the period |
| Note: Commitments and contingencies | Purchase obligations, **multi-year cloud service agreements** (Nvidia renting capacity, often from the same neoclouds it invests in), capacity agreements, guarantees, indemnifications, any obligation to purchase unused capacity |
| Note: Balance sheet components | Prepaid supply and capacity agreements (prepayments to suppliers), long-term prepaids, other assets that may hide financing |
| Note: Concentration of credit risk | Accounts receivable concentration, direct customers above 10% of revenue (Customer A, B, C) |
| Note: Related parties, VIEs | Any variable interest entity, special purpose vehicle or consolidated structure |
| Note: Subsequent events | Deals signed after period end |
| MD&A, liquidity | Commitments to invest, stated intent to support ecosystem partners |
| Risk factors | New language about investments in customers, collectability, demand from financed customers. **Diff risk factors filing over filing**; new sentences are signals |

**Use XBRL to cross-check numbers.** Pull `https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json` and record the time series for any concept covering marketable securities, non-marketable equity, purchase obligations, prepaid supply, other long-term assets, and receivables. Record the concept name you used. Where the tagged number differs from the text, the text wins and the difference is logged.

**13F-HR.** For each quarter in the window, list every holding: issuer, CUSIP, shares, value, change from prior quarter. A new position, a doubled position or an exit is an event.

**Output of R1.** `research/reports/R1.md`: every relationship Nvidia itself named, and every aggregate it disclosed (non-marketable equity, cloud service agreements, purchase obligations, prepaid supply) with its balance sheet date. Do not compute the unattributed remainder yet; named private deals found in R3 and R4 would make it too large. It is computed in R7.

---

## R2 · The counterparty filings sweep (EDGAR full-text search)

Goal: find what other companies filed about Nvidia. Counterparties often disclose more than Nvidia does, because the deal is material to them and immaterial to Nvidia.

Use EDGAR full-text search (the API behind sec.gov/edgar/search, `efts.sec.gov/LATEST/search-index`) across all filers, forms 10-K, 10-Q, 8-K, S-1, S-1/A, F-1, 424B4, 424B5, 20-F, 6-K, DEF 14A, and exhibits. Run each query below for the window. Where a row lists several queries separated by semicolons, run each as its own search; every query pairs NVIDIA with one term and never uses OR. Save every hit with accession number and the paragraph containing it.

| # | Query | What it finds |
|---|---|---|
| Q1 | `"NVIDIA" "backstop"` | Capacity backstops |
| Q2 | `"NVIDIA" "unused capacity"`; `"NVIDIA" "unsold capacity"`; `"NVIDIA" "residual capacity"` | Agreements to buy what customers do not |
| Q3 | `"NVIDIA" "guarantee"`; `"NVIDIA" "guaranty"` | Guarantees of leases, debt or purchase obligations |
| Q4 | `"NVIDIA" "subscription agreement"`; `"NVIDIA" "securities purchase agreement"`; `"NVIDIA" "investment agreement"` | Equity investments |
| Q5 | `"NVIDIA" "warrant"` | Warrants issued to Nvidia |
| Q6 | `"NVIDIA" "master services agreement"`; `"NVIDIA" "cloud services agreement"` | Nvidia as a renter of compute |
| Q7 | `"NVIDIA" "lease" "GPU"`; `"NVIDIA" "leaseback"` | Leasebacks of Nvidia's own chips |
| Q8 | `"NVIDIA" "prepayment"`; `"NVIDIA" "prepaid"`; `"NVIDIA" "deposit"` | Supply prepayments and customer deposits |
| Q9 | `"NVIDIA" "principal stockholder"`; `"NVIDIA" "beneficial owner"` | Nvidia as a 5% holder in proxies and prospectuses |
| Q10 | `"NVIDIA" "collateral"`; `"NVIDIA" "security interest"`; `"NVIDIA" "GPU-backed"` | Debt secured by Nvidia GPUs, delayed draw term loans, ABS |
| Q11 | `"NVIDIA" "concentration" "supplier"` | Counterparties that depend on Nvidia as sole supplier |
| Q12 | `"NVIDIA" "license" "non-exclusive"` | Licensing and acqui-hire structures |

Full-text search matches whole documents, so filter each hit: fetch the document, keep it only if the query terms fall within a 50-word window, and store that window as the paragraph. Cap at 500 hits per query per date window; if a query overflows, log it and narrow the date range. Then discard hits where Nvidia is only a supplier in a routine sentence. Keep any hit describing money, credit support or a contractual commitment between Nvidia and the filer.

**Output of R2.** `research/reports/R2.md` and new candidate relationships appended to `research/candidates.csv` with source.

---

## R3 · Company announcements (tier 1, non-filing)

Goal: capture deals announced by press release that never reached a filing.

1. Nvidia newsroom and investor relations releases in the window. Search for: invest, investment, partnership, strategic, gigawatt, capacity, agreement, letter of intent, stake.
2. For every counterparty found so far, read that company's own newsroom and investor relations releases about Nvidia.
3. Record the exact wording of any amount ("up to", "invest", "commit", "intend") because the verb determines the exposure category in `05`.
4. Note whether a release describes a **definitive agreement** or a **letter of intent, memorandum or framework**. This drives the status field.

**Output of R3.** Candidates appended, each with the announcement date and the binding status.

---

## R4 · Tier 2 news sweep for private counterparties

Goal: cover relationships with private companies (AI labs, private neoclouds, SPVs) where no filing exists.

1. Search only the publications listed in `04_SOURCE_POLICY.md` tier 2. Use WebSearch with the publication's domain as an allowed domain filter.
2. For each private counterparty: search `"<counterparty> Nvidia invest"`, `"<counterparty> Nvidia stake"`, `"<counterparty> Nvidia backstop"`, `"<counterparty> Nvidia guarantee"`, `"<counterparty> financing GPUs"`, `"<counterparty> special purpose vehicle"`.
3. Apply the display rule from `04`: a figure needs a tier 1 source or two independent tier 2 sources. If a tier 1 source confirms only that the relationship exists, the amount stays "Not confirmed". A relationship on one tier 2 report is recorded with claim basis `reported_single_source`, status `reported_unconfirmed`, and no displayed amounts.
4. Track what was reported **and later changed**: deals renegotiated, shrunk, restructured or abandoned. A later report that a deal was not finalized is as important as the announcement.

**Output of R4.** `research/reports/R4.md` with a table: claim, publication 1, publication 2, date of each, status.

---

## R5 · Both sides: counterparty reconciliation (run with /buyside-research:research)

Goal: for every candidate, establish what the counterparty says, and test whether the two accounts agree.

Run `/buyside-research:research` once per cluster below. The brief for each run: "For each named counterparty, find every disclosure of its financial relationship with Nvidia in allowed sources. For each: transaction type, amount, committed versus contingent, dates, tenor, use of proceeds, whether proceeds flow back to Nvidia purchases, collateral, seniority, and the counterparty's own credit position (debt, maturities, ratings, liquidity, customer concentration). Reconcile against the Nvidia-side record attached. Flag every disagreement." Attach the cluster's rows from `candidates.csv`.

| Cluster | Counterparty types | Extra questions for this cluster |
|---|---|---|
| A · AI labs | Model developers receiving Nvidia equity | Funding round size, Nvidia's share, valuation, compute commitments the lab has signed elsewhere, revenue versus committed spend, who else is funding the same compute |
| B · Neoclouds | GPU cloud providers | Backlog, customer concentration, debt stack by facility, GPU collateral, depreciation life, Nvidia as customer and as shareholder at the same time |
| C · Semis and supply chain | Chipmakers, EDA, networking, memory, foundry | Strategic rationale, prepayments, capacity reservations, whether Nvidia's stake is tied to a product agreement |
| D · Hyperscalers and offtakers | Large cloud and software platforms | Where Nvidia's relationship is indirect: offtake contracts that make a neocloud's debt bankable, co-investments alongside Nvidia |
| E · Sovereign and project vehicles | National AI programs, joint ventures, data center SPVs | Who owns the SPV, who funds it, what Nvidia contributed, government guarantees, export license conditions |
| F · Portfolio and venture | 13F holdings and venture arm investments | Size, follow-on rights, whether the company is also a material customer |

**Reconciliation result per relationship**, one of:
- `reconciled`: both sides agree on type, amount and timing
- `partial`: agree on existence, differ on amount, timing or terms (record both)
- `one_sided`: only one side has disclosed
- `contradicted`: the sides disagree on whether the deal exists or is binding

**Output of R5.** Cluster reports plus a reconciliation table.

---

## R6 · Project basis for neoclouds and vehicles

Goal: credit risk at a neocloud sits in its individual sites and the debt raised against each, so map it site by site.

Also search lien registries: UCC financing statements naming each counterparty in its state of incorporation (secured party, collateral description, filing date), and Companies House registers of charges for UK entities. These show which lenders hold GPU liens.

For every neocloud and project vehicle in the register, build a project table: site name and location, power capacity in megawatts (contracted versus energized), GPU generation and count where disclosed, anchor tenant and contract length, financing facility and lenders, collateral, expected completion, and which Nvidia relationship touches it (for example a backstop that covers this site's unsold capacity). Sources: the counterparty's filings (S-1 and 10-K property and debt sections, 8-K credit agreements as exhibits), the lenders' announcements, tier 2 reporting.

Where a project cannot be tied to a specific Nvidia relationship, it is still listed under the counterparty, marked `context`.

**Output of R6.** `data/register/projects.json` per `06_DATA_SCHEMA.md`.

---

## R7 · Classify and measure

Apply `05_CREDIT_RISK_FRAMEWORK.md` to every relationship:

1. Assign the exposure type (one primary, any number of secondary).
2. Fill headline, committed_total, funded and contingent_max per `05` section 3. Unknown stays unknown; never infer a split without a source.
3. Compute the unattributed remainder for each Nvidia aggregate (`05` section 3), at carrying value, at one balance sheet date, as its own record with `aggregate_of` set, excluded from totals.
4. Run `pipeline/measure.py` for the derived measures in `05` section 4; it leaves any measure blank whose inputs are not sourced.
5. Assign the credit read: grade by the rubric in `05` section 5, collateral, seniority, tenor, and wrong-way risk as specific, general or none with a reason.

---

## R8 · The second ring: who else is exposed

Goal: map the money that depends on each Nvidia relationship. This is where second order risk lives.

For each relationship, identify parties whose position relies on it:
- lenders to the counterparty whose loan is supported by an Nvidia backstop, Nvidia equity, or GPU collateral
- offtakers (hyperscalers, labs) whose contracts make the counterparty's debt bankable
- co-investors in the same round or vehicle
- bondholders, ABS investors and private credit funds in GPU-backed debt
- utilities and landlords tied to the counterparty's sites

Record each as a depth-2 entity linked to the depth-1 relationship, with the same sourcing rules. Do not go beyond depth 2 in this release.

---

## R9 · Consequences, critic, datapack, approval

1. For every relationship, write first order and second order consequences per the method in `05`. Each consequence names the mechanism, the party affected, the direction, and what would make it happen.
2. Write the system-level view: aggregate exposure by type and by counterparty grade, top five concentrations, every closed loop (these feed the Loops view), and the three scenarios in `05` run against the register, using display-eligible amounts only.
3. Run Gate R in `09`: independent re-sourcing, then `anthropic-skills:critic-agent` on the register and reports, up to three rounds.
4. Run `/investment-banking:datapack-builder` to produce `research/Nvidia_Exposure_Datapack.xlsx`.
5. Post a summary to Thomas in chat: number of relationships, seeds confirmed, modified and killed, totals by category, open questions. **Wait for approval before Phase B.** Record the approval date as the Gate R cutoff in `research/SCOPE.md`.
