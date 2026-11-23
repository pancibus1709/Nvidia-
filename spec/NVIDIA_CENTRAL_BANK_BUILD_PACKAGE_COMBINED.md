# The Central Bank of AI: Nvidia Exposure Map
## Build package for Claude Code

Prepared 22 November 2026 for Resolute Business Development.
Status: **specification only. No research has been executed.** Every company, figure and date in this package is a hypothesis to verify, not a finding.

---

## What this package builds

A continuously updated web application, published under the question **"Is Nvidia the Central Bank of AI?"**, that maps every financial relationship with Nvidia at the center: equity stakes, capacity backstops, leasebacks, guarantees, financing commitments, supply prepayments and licensing deals that support AI capital spending. Each relationship shows the exposure amount, the date, what the transaction actually is, what the counterparty disclosed about the same deal, the credit read, and its first and second order consequences, with a citation on every number.

The thesis the application tests (not assumes): Nvidia has moved from selling chips to underwriting the demand for its own chips. It supplies equity, buys back unused capacity, and anchors financing for customers who then spend that money on Nvidia hardware. That is the behavior of a lender of last resort for the AI buildout. The app exists to show where that is true, where it is not, and how large the exposure is relative to Nvidia's balance sheet and to each counterparty's ability to pay.

## How to use this package

Hand the whole folder to Claude Code. Paste `01_MASTER_PROMPT.md` as the opening instruction. Claude Code reads the rest as reference.

The order is enforced, not suggested:

| Phase | What happens | Gate to pass before the next phase |
|---|---|---|
| R | Research tooling and checks first, then research: map every relationship, reconcile both sides, measure exposure, write consequences | Relationship register complete, critic-agent passed, Thomas approves |
| B | Build: data pipeline, application, design | All acceptance tests in `10_BUILD_PLAN.md` pass |
| U | Continuous update: watchers, review queue, schedule | One full dry-run refresh cycle completes with a correct change log |
| Q | Final critic and design critique | No open critical findings |

**No front-end or site code is written until Phase R is complete and approved.** Relationships are mapped first. Research tooling (the SEC client, cache, schemas, validators and automated checks) is built in R0, so every research record is checked from day one.

## Files

| File | Purpose |
|---|---|
| `00_README.md` | This page |
| `01_MASTER_PROMPT.md` | The prompt to paste into Claude Code. Role, mission, rules, phase order |
| `02_RESEARCH_PROTOCOL.md` | The research sequences R0 to R9, step by step, with exact EDGAR queries |
| `03_SEED_REGISTER.md` | Starting hypotheses: relationships to confirm or kill. Not facts |
| `04_SOURCE_POLICY.md` | Which sources are allowed, which are banned, how to cite |
| `05_CREDIT_RISK_FRAMEWORK.md` | Exposure taxonomy, measurement rules, first and second order analysis, stress scenarios |
| `06_DATA_SCHEMA.md` | JSON schemas for relationships, evidence, entities, events, change log |
| `07_APPLICATION_SPEC.md` | Views, interactions, click and collapse behavior, copy rules |
| `08_DESIGN_SYSTEM.md` | Frida Kahlo palette and type, lifted from the US Economy Monitor's live tokens |
| `09_QA_AND_CRITIC_GATES.md` | Verification checks and the critic-agent loop at each gate |
| `10_BUILD_PLAN.md` | Milestones, file layout, acceptance tests |
| `11_CONTINUOUS_UPDATE.md` | Filings watcher, news watcher, review queue, versioned history, schedule |
| `NVIDIA_CENTRAL_BANK_BUILD_PACKAGE_COMBINED.md` | All of the above in one file, for a single paste |

## Skills this package calls

| Skill | Where | Why |
|---|---|---|
| `/buyside-research:research` | Phase R, once per counterparty cluster | Runs the harness-built analyst on filings with policy hooks, independent critic and change receipt |
| `/investment-banking:datapack-builder` | End of Phase R | Turns the verified register into a sourced Excel evidence pack Thomas can audit cell by cell |
| `anthropic-skills:critic-agent` (invoked as `/critic-agent`) | Every gate | Adversarial review, up to three rounds, before anything moves forward or gets pushed |
| `design:design-critique` | Phase Q | Same rule as the Economy Monitor: critique before any push |
| `anthropic-skills:human-voice` | All on-screen copy | No AI tells, no em dashes |

## Assumptions made (flagged, change any of them)

1. **Architecture mirrors the Economy Monitor**: a Python pipeline writes JSON, and a single self-contained page reads it, published to a subdomain of resolute-bd.com (proposed `nvidia.resolute-bd.com`). "Full stack" here means pipeline plus review tooling plus front end. A database server is not needed at this scale; the data is a few hundred records with an append-only history. If Thomas wants a hosted backend later, the schema in `06` ports to Postgres unchanged.
2. **Public showcase**, like the Economy Monitor: carries "Built By Resolute Business Development", a "Data as of" date, and a not-investment-advice disclaimer.
3. **Scope window**: relationships announced, filed or reported from 1 January 2023 to the present, plus any older relationship still active (for example long-standing equity holdings).
4. **Currency**: USD as disclosed. Non-USD deals shown in original currency with the USD conversion and the conversion date.


<!-- end of 00_README.md -->

# 01 · Master Prompt

Paste everything between the two rules into Claude Code as the first message. Keep this folder in the repository root as `/spec`.

---

## Role

You are three people working as one team.

1. **A senior credit risk officer** who has underwritten leveraged loans, structured asset-backed deals and counterparty exposure at a bank. You think in exposure at default, probability of default, loss given default, seniority, collateral, tenor, wrong-way risk and correlation. You distrust headline numbers until you know what is committed, what is funded and what is contingent.
2. **A forensic filings analyst** who reads 10-Ks, 10-Qs, 8-Ks, S-1s, 424B prospectuses and 13F-HRs footnote first. You know that the press release says "up to $100 billion" and the footnote says what was actually signed.
3. **A product builder in the Steve Jobs tradition**: the interface removes everything that does not help a reader understand exposure in under ten seconds, and reveals depth only when asked.

## Mission

Build **The Central Bank of AI**, a continuously updated application that maps every financial relationship in which Nvidia supplies capital, credit support or demand support to the AI buildout, and shows for each one:

- who the counterparty is and what kind of entity it is (AI lab, neocloud, hyperscaler, chip or supply chain, sovereign, portfolio company, financial vehicle)
- what the transaction is, defined precisely (equity, capacity backstop, leaseback, guarantee, financing commitment, prepayment, licensing, offtake)
- the exposure amount, split into **committed, funded, contingent and headline**
- the dates: announced, signed, filed, effective, maturity, last verified
- what Nvidia disclosed and what the counterparty disclosed about the same deal, and whether they reconcile
- for neoclouds and project vehicles, the **project basis**: which sites, how many megawatts, which GPUs, which end customer, which lenders
- the credit read: counterparty quality, circularity, collateral, wrong-way risk
- first order and second order consequences
- a citation on every number, from an allowed source only

The user clicks a relationship, sees the insight in one sentence, and expands to see more.

## Non-negotiable rules

1. **Map first, build second.** Build the research tooling, schemas, validators and automated checks in R0 (see `/spec/10_BUILD_PLAN.md`). Do not write any front-end or site code until Phase R in `/spec/02_RESEARCH_PROTOCOL.md` is complete, the relationship register has passed `/critic-agent`, and Thomas has approved it in chat.
2. **Allowed sources only**, per `/spec/04_SOURCE_POLICY.md`. A figure is displayed only if supported by a tier 1 source or two independent tier 2 sources. Anything else is excluded, even if it is the only source. A relationship with no allowed source goes to the unconfirmed log, not the app.
3. **Every relationship is examined from both sides.** After establishing what Nvidia disclosed, find what the counterparty disclosed. Record agreement, disagreement or silence, and treat silence as a result worth showing.
4. **Never present a headline number as exposure.** "Up to" amounts, letters of intent and framework agreements are shown as headline, with the committed and funded portions stated separately, or marked unknown.
5. **Every number carries a date and a citation.** No date, no display.
6. **No figure from memory.** The seed register in `/spec/03_SEED_REGISTER.md` is a list of hypotheses to verify or kill. You must re-source every figure in it.
7. **Distinguish fact from inference.** Every claim carries a claim basis and a fact or analysis label, using only the values in `schema/enums.json` (defined in `/spec/06_DATA_SCHEMA.md`). Inference is labeled Analysis on screen.
8. **The data must be continuously updatable.** Build per `/spec/11_CONTINUOUS_UPDATE.md`: new filings and news are detected automatically, land in a review queue, and only reach the live site after verification. History is append-only; nothing is silently overwritten.
9. **Copy rules**: plain English, no em dashes, no hype, no AI tells. Run `anthropic-skills:human-voice` on all on-screen text.
10. **Not investment advice.** The app describes exposure; it never recommends a trade.
11. **Every figure is grounded.** A figure enters a record only with a verbatim quote and locator in a cached copy of its source. The grounding check in `/spec/09_QA_AND_CRITIC_GATES.md` re-finds it there. If you cannot quote it, you cannot use it.

## Skills to use and when

- `/buyside-research:research` for each counterparty cluster in Phase R (sequence R5). Filter its output through `config/sources_allowlist.json` before anything enters `research/candidates.csv`; the plugin's own source rules do not override `/spec/04`. Give it the cluster brief from `02`. SEC.gov requires a declared User-Agent: read it from the environment variable `SEC_USER_AGENT`, which Thomas sets himself (the same contact string his buyside-research plugin already uses). Never hard-code it in the repository.
- `/investment-banking:datapack-builder` at the end of Phase R to produce `research/Nvidia_Exposure_Datapack.xlsx`: one tab per exposure type, one row per relationship, source and date on every cell, plus a reconciliation tab.
- `anthropic-skills:critic-agent` (the `/critic-agent` skill) at every gate listed in `/spec/09_QA_AND_CRITIC_GATES.md`. Up to three rounds. Fix, then re-run.
- `design:design-critique` before any publish.

## Phase order

| Phase | Spec | Output |
|---|---|---|
| R0 tooling, R1 to R9 research | `02`, `03`, `04`, `05`, `06`, `09` | `data/register/*.json`, `research/evidence/`, datapack, unconfirmed log |
| Gate R | `09` | Critic pass plus Thomas approval in chat |
| B1 to B6 Build | `06`, `07`, `08`, `10` | Pipeline, site, tests |
| U1 to U5 Continuous update | `11` | Watchers, review queue, schedule, change log |
| Q Final | `09` | Critic and design critique clean |

## How to work

- Start by reading every file in `/spec`. Then write `research/PLAN.md` restating the phases in your own words, listing any conflicts you found in the spec, and asking Thomas only the questions whose answers change what you build. Then proceed.
- Track progress with a task list. Commit after each sequence with a message naming the sequence.
- When a sequence is done, write a short sequence report in `research/reports/` stating what was found, what was killed from the seed register, and what is still open.
- When you are blocked by a paywall or an unreachable source, log it and move on. Do not substitute a disallowed source.
- When two allowed sources disagree, record both, prefer the filing, and say so in the relationship's notes.

## Definition of done

1. Every relationship in the register has: transaction definition, exposure split, dates, both-sides reconciliation, credit read, first and second order consequences, and every displayed figure passes the display rule and the grounding check.
2. The app renders every relationship, lets the user click, read the one-line insight, and expand to full detail.
3. A scheduled refresh detects a new Nvidia filing, puts any new or changed relationship in the review queue, and after approval publishes it with a dated entry in "What changed".
4. Critic-agent and design critique show no open critical findings.

---


<!-- end of 01_MASTER_PROMPT.md -->

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


<!-- end of 02_RESEARCH_PROTOCOL.md -->

# 03 · Seed Register

## Read this first

This is a list of **hypotheses**, compiled from recall on 22 November 2026 without running any research. It exists so the research starts with a checklist instead of a blank page. **None of it may appear in the app until re-sourced under `04_SOURCE_POLICY.md`.** Some items are likely wrong in amount, date or status. Some deals here were later restructured or abandoned. Some relationships are missing entirely; R1 and R2 exist to find them.

Every row must end as `confirmed`, `modified` (exists but the details differ) or `killed` (no allowed source, or never happened). Record which.

**Anchor warning.** The exact figures below (prices per share, dollar amounts, end years) are easy to "confirm" by citing a plausible filing without finding the number in it. Any register value that equals a seed value must carry a grounded quote, and all such values are re-sourced independently at Gate R (`09`).

Amounts are as remembered and are written as the headline figure. The research must split each into committed, funded and contingent.

---

## A · AI labs

| # | Counterparty | Hypothesis | Type to test | Verify especially |
|---|---|---|---|---|
| A1 | OpenAI | Sept 2025 letter of intent: Nvidia to invest up to $100B progressively as OpenAI deploys at least 10 GW of Nvidia systems, first tranche tied to the first gigawatt | Equity commitment, conditional | Whether a definitive agreement was ever signed; later reports that the structure changed or Nvidia instead joined a funding round for a smaller amount; Nvidia 10-Q language on it |
| A2 | Anthropic | Nov 2025: Nvidia up to $10B and Microsoft up to $5B in Anthropic; Anthropic commits to Azure compute (reported $30B) and up to 1 GW of Nvidia systems | Equity, linked compute commitment | Funded amount, how it reached Anthropic (round participation), the compute linkage |
| A3 | xAI | Oct 2025 reports: Nvidia up to $2B equity in a roughly $20B vehicle that buys Nvidia GPUs and leases them to xAI | Equity in SPV, circular | SPV name, sponsors, debt portion, lessee terms, xAI credit |
| A4 | Mistral AI | Nvidia participation in 2025 funding round | Equity | Amount, if disclosed |
| A5 | Reflection AI | Nvidia reported as large investor in a 2025 round of about $2B | Equity | Nvidia's portion |
| A6 | Poolside | Reported Nvidia commitment up to $1B in 2025 | Equity, conditional | Whether tied to compute purchases |
| A7 | Other labs | Perplexity, Cohere, Sakana, Thinking Machines, Safe Superintelligence, Figure, Wayve and others with Nvidia participation | Equity | Treat as a sweep: venture arm and corporate investments |

## B · Neoclouds and GPU infrastructure

| # | Counterparty | Hypothesis | Type to test | Verify especially |
|---|---|---|---|---|
| B1 | CoreWeave | Nvidia is a major shareholder (stake from before the March 2025 IPO, anchor order in the IPO) | Equity | Share count over time from 13F and CoreWeave proxy |
| B2 | CoreWeave | Sept 2025 8-K: Nvidia order of about $6.3B to purchase CoreWeave capacity not sold to customers, running to 2032 | Capacity backstop | Exact language, term, whether it is a floor on utilization, how CoreWeave counts it in backlog |
| B3 | CoreWeave | Earlier Nvidia agreement to rent CoreWeave capacity (reported about $1.3B over four years) | Capacity purchase, circular | Overlap with B2; Nvidia's cloud service agreement totals |
| B4 | CoreWeave | Early 2026 reports of an additional Nvidia equity investment (about $2B) | Equity | Price, date, filing |
| B5 | Lambda | Sept 2025 reports: Nvidia to lease back about 18,000 of its own GPUs from Lambda, about $1.5B over four years; Nvidia also Lambda's largest customer | Leaseback, circular | Lambda S-1 if filed; customer concentration disclosure |
| B6 | Nebius | Nvidia holding (13F and Nebius disclosures) | Equity | Size and changes |
| B7 | Crusoe | Nvidia participation in funding rounds | Equity | Amount |
| B8 | Nscale | Nvidia participation in 2025 Series B; UK projects | Equity, project | Project basis, offtaker (Microsoft reported) |
| B9 | Applied Digital and others in 13F | Past Nvidia holding | Equity | Whether still held |
| B10 | Nvidia cloud service agreements (aggregate) | Nvidia 10-Q discloses multi-year cloud service agreements in the tens of billions | Capacity purchase, aggregate | Total by period; which counterparties; growth rate |

## C · Semis, networking and supply chain

| # | Counterparty | Hypothesis | Type to test | Verify especially |
|---|---|---|---|---|
| C1 | Intel | Sept 2025: $5B Nvidia equity at about $23.28 per share, plus product collaboration; closed late 2025 after review | Equity | Closing date, share count, filings on both sides |
| C2 | Nokia | Oct 2025: $1B Nvidia equity at about $6.01 per share, AI networking partnership | Equity | 6-K, closing |
| C3 | Synopsys | Dec 2025: $2B Nvidia equity | Equity | 8-K, price |
| C4 | Groq | Dec 2025: non-exclusive license and hiring of leadership, reported about $20B | Licensing and acqui-hire | Classification: this is a purchase, not an exposure to Groq's credit. Decide whether it belongs on the map and say why |
| C5 | Arm | Long-standing Nvidia shareholding (13F) | Equity | Size |
| C6 | Suppliers: TSMC, memory makers, assemblers | Nvidia prepaid supply and capacity agreements and large purchase obligations | Prepayment, purchase obligation | Aggregate figures from 10-K and 10-Q; named suppliers where counterparties disclose |

## D · Hyperscalers and offtakers (expected mostly depth 2)

| # | Counterparty | Hypothesis | Why it may matter |
|---|---|---|---|
| D1 | Microsoft | Co-investor with Nvidia in Anthropic; offtaker of neocloud capacity (Nebius, Nscale, IREN, others) | Its contracts make neocloud debt bankable; if offtake falls, Nvidia-backed neoclouds weaken |
| D2 | Oracle | Hypothesis: very large compute contract with OpenAI, and large Nvidia purchases funded partly with debt | Second order: OpenAI's ability to pay Oracle depends partly on OpenAI funding that Nvidia may supply |
| D3 | Google, Amazon, Meta | Own chips plus Nvidia purchases; Meta's off-balance-sheet data center vehicle with private credit | Comparators: shows that backstops are not unique to Nvidia (for example Google's reported backstop of Fluidstack leases at crypto-miner sites). Include as context nodes |

## E · Sovereign and project vehicles

| # | Counterparty | Hypothesis | Verify |
|---|---|---|---|
| E1 | Stargate entities (OpenAI, Oracle, SoftBank, MGX) | Nvidia as technology partner, not investor | Whether Nvidia put capital in. If not, context only |
| E2 | Saudi Humain, UAE programs, European industrial AI clouds | Large GPU sales agreements | Sales are not exposure unless Nvidia finances, guarantees or invests. Test each |

## F · Disclosed aggregates to extract from Nvidia filings

| # | Item | Why |
|---|---|---|
| F1 | Non-marketable equity securities, carrying value by period | Size of private stakes Nvidia does not name |
| F2 | Marketable equity securities | Public stakes |
| F3 | Multi-year cloud service agreements | Nvidia renting compute back from the ecosystem |
| F4 | Purchase obligations and prepaid supply | Upstream commitments |
| F5 | Customer concentration (Customer A, B, C share of revenue and receivables) | Who Nvidia depends on, and whether financed customers are among them |
| F6 | Any guarantee or indemnification note | Direct contingent liabilities |

## Questions the research must answer that no seed covers

1. What share of Nvidia's revenue in each period came from customers that Nvidia also funded, backstopped or rented from? (Only computable if counterparties disclose purchases; mark where not computable.)
2. How much of the "headline" total is legally binding today?
3. Which relationships were announced, then quietly shrunk, restructured or dropped?
4. Where does Nvidia sit in the capital structure of each counterparty: common equity, preferred, SPV equity, customer, guarantor?


<!-- end of 03_SEED_REGISTER.md -->

# 04 · Source Policy

This policy is enforced in code (`09`): a citation from an unlisted domain fails the build.

## Tier 1: primary (preferred for every number)

| Source | Notes |
|---|---|
| SEC EDGAR filings (sec.gov, data.sec.gov) | 10-K, 10-Q, 8-K and exhibits, S-1, F-1, 424B, 20-F, 6-K, DEF 14A, 13F-HR, Schedules 13D and 13G, Forms 3 and 4. Cite accession number and section |
| Company investor relations and newsroom releases | The company's own domain only. Cite title and date |
| Earnings call transcripts or webcasts published by the company | Quote speaker and date |
| Regulators and courts | FTC, DOJ, Commerce (BIS), CFIUS statements, foreign securities regulators' filing systems, court dockets |
| Public corporate and lien registries | State UCC financing statements, UK Companies House (including registers of charges), equivalent national registries. Cite filing number and date. These are where GPU liens and private company charges show up |
| Credit rating agency publications | Moody's, S&P Global Ratings, Fitch: public rating actions and press releases only |

## Tier 2: named financial news publications

Bloomberg, Reuters, The Wall Street Journal, Financial Times, The Information, CNBC, Barron's, The Economist, Nikkei Asia, Axios (business coverage).

- Prefer the original reporter. If an outlet writes "according to Bloomberg", cite Bloomberg.
- Syndicated copies of one wire story are one source. Two sources are independent only if neither cites the other.
- Record the sourcing: named, documents seen, or anonymous people familiar.
- Paywalled articles: cite title, outlet, date and URL; any quote under fifteen words. The figure is grounded only after a reviewer pastes the sentence (see `11` U2).

## The display rule (one rule, applied everywhere)

**A figure is displayed only if it is supported by a tier 1 source or by two independent tier 2 sources.**

If a relationship's existence is supported but its amount is not, the relationship is displayed with the amount shown as "Not confirmed", never as a number. A relationship supported only by one tier 2 report is displayed with status "Reported, unconfirmed" and no amounts. There is no label or exception that lets a single-source figure through.

## Market data (prices only)

Share prices for public stakes come from the market data source the Economy Monitor already uses (Yahoo Finance quote data, per the monitor's refresh notes of 20 November 2026). This class supports only `market_value`, always shown with the price timestamp and source name. **The one exception to the display rule:** evidence of kind `market_data` (tier `market`) makes a `market_value` eligible on its own, when the price timestamp and source are present. It cannot support any other field. It never supports a relationship fact. Listed separately in `config/sources_allowlist.json` under `market_data`.

## Excluded, always

Blogs, Substack, Medium, Seeking Alpha contributor articles, Motley Fool, Zacks, InvestorPlace, Benzinga opinion, Yahoo Finance contributor content (wire stories on Yahoo are cited to the original wire), Wikipedia, Reddit, X and other social posts (an executive's post counts only if the company repeats it in a release or filing), YouTube commentary, podcasts, AI-generated summaries, press release distribution sites when the company's own copy exists, sell-side research notes.

If the only source is excluded, the relationship goes to `research/unconfirmed.md` with the reason and does not appear in the app.

## Output from skills and subagents

Output from `/buyside-research:research` or any subagent is filtered through `config/sources_allowlist.json` before it enters `research/candidates.csv`. A plugin's own source rules never override this file.

## Citation format and conflicts

Evidence records follow `06`. On screen, each number has a source chip that opens its citations. When sources disagree, show both, state which is preferred and why (filing over announcement over report; a later source over an earlier one when it describes a change), and set the reconciliation result.


<!-- end of 04_SOURCE_POLICY.md -->

# 05 · Credit Risk Framework

How to classify, measure and judge each relationship, written as a credit officer would underwrite it. Every enum named here is defined once, in `schema/enums.json` (see `06`).

---

## 1. Test the "central bank" thesis, do not assume it

A central bank does four things: it supplies liquidity to institutions the market will not fund on equal terms, it stands behind assets so others will lend against them, it influences the price of money for its system, and it acts as lender of last resort when the system strains. The app tests each against the evidence:

| Central bank function | Nvidia analogue to test | Evidence that would support it | Evidence that would weaken it |
|---|---|---|---|
| Liquidity provision | Equity into labs and neoclouds that then buy Nvidia systems | Investment closely followed by equal or larger purchase commitments | Investments with no linked purchases; co-investors on the same terms |
| Collateral support | Capacity backstops and leasebacks that make GPU-backed debt bankable | Lenders or the borrower cite the Nvidia agreement; a facility closes after it | Debt raised before the backstop; backstop small relative to the debt |
| Pricing of money | Nvidia participation sets valuation and cost of capital for counterparties | Rounds priced on Nvidia's entry; spreads tighten after announcement | Pricing set by other leads |
| Lender of last resort | Nvidia steps in when a counterparty cannot raise elsewhere | Deals announced during counterparty stress | Deals only with well-funded counterparties |

The app shows a verdict per function with evidence for and against, and says where the analogy breaks: Nvidia cannot create money, and its support is finite and tied to its own cash flow. That limit is the risk the app measures.

For this reason the public page title is a question: **"Is Nvidia the Central Bank of AI?"** The repository and internal name stays "The Central Bank of AI".

---

## 2. Exposure taxonomy

One primary type per relationship.

| Code | Type | Definition | What Nvidia can lose |
|---|---|---|---|
| EQ | Direct equity | Shares, preferred stock or warrants in the counterparty | Funded cost, last in line |
| EQ-SPV | Vehicle equity | Equity in a special purpose vehicle that owns GPUs or data centers | Funded cost, behind the vehicle's lenders |
| EQ-C | Conditional equity commitment | Agreement to invest later, subject to milestones | Under a letter of intent or framework: **headline only**, no exposure counted. Under a definitive agreement with milestones: **contingent**, with the milestone as the trigger |
| BK | Capacity backstop | Nvidia agrees to buy capacity the counterparty cannot sell to others | Payments for capacity it may not need, minus what that capacity is worth to Nvidia or on resale |
| LB | Leaseback or capacity rental | Nvidia rents compute, often built on its own chips, from the counterparty | Any prepaid rent, and paying above market rates for capacity it does not use; the counterparty gains contracted revenue |
| GU | Guarantee | Nvidia guarantees a lease, loan or obligation of another party | Guaranteed amount minus recovery from collateral |
| RV | Residual value or repurchase obligation | Nvidia guarantees the future value of GPUs or agrees to buy them back | Guaranteed value minus market value at the trigger date |
| FC | Financing commitment | Nvidia lends, extends vendor financing or long payment terms | Outstanding balance minus recovery |
| LP | Fund commitment | Commitment as a limited partner to an investment fund or vehicle | Funded portion as equity; unfunded portion contingent |
| PP | Supply prepayment | Nvidia prepays suppliers for capacity | Prepaid amount, if the supplier fails to deliver |
| LI | License or acqui-hire | Nvidia pays for technology or talent | Usually a purchase, not credit exposure. Include only with a stated reason |
| CX | Context | Matters for second order analysis; no Nvidia capital | None; shown greyed |

---

## 3. Measuring the amount

### The amount fields (never merged)

| Field | Meaning | How set |
|---|---|---|
| `headline` | Largest figure announced, usually "up to" | From the source. Shown, labeled headline, never summed into exposure |
| `committed_total` | Legally binding amount under a definitive agreement, **including** anything already funded | From a filing, a definitive agreement announcement, or two independent tier 2 reports describing a signed agreement |
| `funded` | Cash paid or shares issued to date | From a filing, a closing announcement or 13F |
| `committed_unfunded` | Derived by the pipeline: `committed_total - funded` | Never entered by hand |
| `contingent_max` | Maximum Nvidia could be required to pay (backstop, guarantee, residual value, LP unfunded, EQ-C under definitive agreement) | Contract maximum, with the trigger stated |
| `market_value` | Current value of a public stake | Price source from `04` market data class, timestamped |

Integrity rule (checked in `09`): when known, `funded ≤ committed_total ≤ headline`.

`committed_unfunded` rules: `committed_total - funded` when both are known; `0` when status is `completed` and `funded` is known (for example open-market or 13F stakes); otherwise null.

**Display eligibility.** `checks.py` sets `display_eligible` on every amount (true only if it passes the display rule in `04`). Every total, tile, derived measure, scenario, significance score and summary sentence uses only eligible amounts. Ineligible amounts stay in the register for research but never reach a number on the page.

An optional `annual_obligation` amount holds a sourced yearly payment (rent, backstop minimum). Where absent, the pipeline may derive it as `committed_unfunded ÷ remaining years`, labeled analysis.

### Gross exposure (sizes the map)

`gross = funded + committed_unfunded + contingent_max`, summing the eligible components that are known.

If any component is unknown, gross is a **lower bound**: it is flagged, the missing components are listed in the panel, and tiles read "at least" with the count of relationships that have unknowns. This is the number that sizes nodes and edges on the map. It answers "how much could Nvidia have to put in or stand behind". Headline-only amounts are drawn separately as a faint halo.

### Exposure at default and loss (panel and Stress view only, labeled analysis)

`EAD = funded + committed_unfunded + contingent_max × draw_rate`

`loss = max(0, EAD - value received or recovered)`, where value received is: for BK and LB, the scenario rental price of the capacity received; for EQ, market value or last round value after the scenario's equity haircut; for GU and FC, documented collateral recovery; for RV, market value of the GPUs at the trigger.

Draw rates live in `config/draw_rates.json` per type, labeled `analysis`, each with a written basis. Base case: from the counterparty's disclosed utilization where available, otherwise "not estimated".

Two kinds of stress, never mixed:
- `ead_max` and `loss_max` in `derived`: every contingent amount drawn at 100%. The worst case for one relationship on its own.
- Scenario results in `scenarios.json`: draws and losses computed by S1, S2 or S3 below. The Stress view and the scenario buttons show these.

Show EAD and loss side by side, never EAD alone.

### Dates and currency on every amount

Each amount carries `as_of`, the source's fiscal period where relevant (Nvidia's fiscal year ends in late January), and for non-USD deals the original currency, original value, FX rate and FX date.

### Aggregates must not double count

Nvidia discloses totals (non-marketable equity, multi-year cloud service agreements, purchase obligations) that include named deals. Rules:
- The **unattributed remainder** is computed in R7, after all named deals are known, at carrying value on both sides, at one balance sheet date: `aggregate carrying value - sum of named items' carrying value`.
- It appears as one node per aggregate, labeled "Unattributed carrying value (analysis)", and is **excluded from every tile total**.
- The same rule applies to cloud service agreements against named leasebacks and backstops.

---

## 4. Derived measures (each labeled analysis, shown with inputs, no adjectives)

| Measure | Definition | Computed only when |
|---|---|---|
| Circularity ratio | Nvidia money into X ÷ X's disclosed spending or commitments on Nvidia hardware, both cumulative from announcement to the latest disclosure | Both inputs are sourced. Indirect purchases (through Dell, Supermicro, Oracle, Microsoft and others) count only if a filing names Nvidia hardware as the use of proceeds |
| Round-trip | Nvidia payments to X (rent, backstop draws) in a window, shown **beside** X's disclosed Nvidia hardware spending in the same window. Not divided | Both are sourced |
| Nvidia share of counterparty capital | Nvidia funded equity ÷ X's total equity raised | Both sourced |
| Share of Nvidia equity | Gross exposure ÷ Nvidia shareholders' equity, latest quarter | Always |
| Share of Nvidia free cash flow | Annual obligation ÷ Nvidia trailing twelve month free cash flow | Annual obligation is sourced |
| Backstop coverage | Backstop maximum ÷ debt on the projects it covers | Both sourced |

No thresholds or color judgments are applied to these. The reader sees the number and its inputs.

---

## 5. Counterparty credit read

Record with sources: public ratings (agency, rating, date); debt by facility; maturities within 24 months; liquidity (cash plus undrawn facilities ÷ 12 months of committed spending); top customer and top three customer share; collateral (GPU generation, depreciation life in accounts); market signals (bond yields, CDS spreads, equity drawdown), dated, from allowed sources.

### Grade rubric (internal)

| Grade | Liquidity cover | Debt due in 24 months ÷ cash plus undrawn | Top customer share | Public rating |
|---|---|---|---|---|
| Strong | Over 24 months | Under 0.5 | Under 25% | Investment grade |
| Adequate | 12 to 24 months | 0.5 to 1.0 | 25% to 50% | BB range |
| Watch | 6 to 12 months | 1.0 to 1.5 | 50% to 70% | B range |
| Weak | Under 6 months | Over 1.5 | Over 70% | CCC range |
| Distressed | Missed payment, waiver, going-concern language or restructuring | | | CC or below, or default |
| Insufficient information | Fewer than two of the four columns sourced | | | |

Take the weakest of the sourced columns, then adjust by at most one step with a written reason. Thresholds are starting values in `config/grade_rubric.json`; Thomas can change them.

**Public display rule.** The public page shows the underlying indicators (liquidity months, maturities, concentration, public rating), not the letter grade. Letter grades on a branded public page read like a rating action on a named listed company. They stay internal unless Thomas opts in by setting `show_grades: true` in `config/display.json`.

### Wrong-way risk

Two different things, stored as `wwr` with a reason:
- `specific`: Nvidia's exposure **grows as the counterparty weakens**. Backstops, guarantees, residual value and financing are specific when the trigger is the counterparty's underperformance. This is the one shown as a flag on the map.
- `general`: exposure and counterparty quality both move with the AI demand cycle, but exposure does not grow with distress (most equity, most leasebacks). Equity loss is correlated with the cycle and capped at cost.
- `none`: neither (for example equity in a diversified company whose fortunes do not hinge on AI demand).

---

## 6. First and second order consequences

Each consequence is one sentence with four parts stored separately: **trigger, mechanism, who is affected, direction**. Two to four per relationship. A consequence that would read the same for any company fails review.

**First order**: the direct effect on Nvidia or the counterparty.
Form: "If [counterparty]'s utilization falls below the contracted level, Nvidia pays for the unsold capacity, so a revenue source becomes an expense."

**Second order**: the effect on parties outside the relationship, through it.
Form: "Lenders to [counterparty] sized their loans against contracted revenue that includes the Nvidia agreement, so a decision by Nvidia not to renew would raise refinancing costs for GPU-backed lenders across the segment."

Lenses checked for every relationship:
1. **Revenue quality**: does the relationship support Nvidia's reported demand with Nvidia's own money?
2. **Lender reliance**: does someone's loan depend on it?
3. **Collateral loop**: does it support GPU values used as collateral elsewhere?
4. **Contagion**: if this counterparty fails, which other nodes lose a customer, supplier or offtaker?
5. **Signaling**: does Nvidia's participation lower the counterparty's cost of capital, and what happens if Nvidia stops?

---

## 7. System view and stress scenarios

Aggregate by type, by grade, by cluster and by tenor bucket. Identify the five largest concentrations and every closed loop (Nvidia to A, A to B, B to Nvidia).

Scenarios are parameters in `config/scenarios.json`, adjustable on screen with sliders. Each default is anchored to a cited, dated observed move from an allowed source, or labeled "illustrative" on screen.

| Scenario | Parameters | Transmission, step by step | Output |
|---|---|---|---|
| S1 · Demand pause | Merchant demand shock `d` (negative, for example -0.3), rental price change `p` (negative), price elasticity `e` (negative), duration in quarters, neocloud equity haircut `h1` | For each neocloud: utilization = contracted share + merchant share × (1 + `d`) × (1 + `e` × `p`), floored at 0 and capped at 1. The demand shock lowers utilization; the price cut partly offsets it. Backstop draw = max(0, contracted floor - utilization) × capacity × rate × quarters. Rate and floor only where sourced, else "not computable" | Draw by backstop, equity loss after `h1`, nodes whose liquidity cover drops below 12 months |
| S2 · Lab funding gap | Which lab, months of delay, lab equity haircut `h2` | Lab's disclosed compute commitments at risk by counterparty; Nvidia EQ-C triggers not met; neoclouds and hyperscalers whose backlog depends on that lab | Affected nodes, at-risk backlog, Nvidia equity loss after `h2`, conditional commitments that lapse |
| S3 · Collateral repricing | Prior generation GPU value change `v` | For each GPU-backed facility with sourced balance and collateral: new loan-to-value = balance ÷ (collateral value × (1 + `v`)). Facilities without both inputs are listed "not computable" | Facilities over their covenant (where the covenant is sourced), affected Nvidia-backed nodes |

Per scenario: Nvidia EAD and loss under stress, as a share of shareholders' equity and of free cash flow, and the affected nodes highlighted on the map. The view opens with: "These illustrate how losses would travel, not forecasts."


<!-- end of 05_CREDIT_RISK_FRAMEWORK.md -->

# 06 · Data Schema

All data lives in `data/` as JSON, validated against JSON Schema files in `schema/`. The front end reads only `data/published/`. Research and review work happens in `data/register/`, `data/inbox/` and `data/queue/`. History is append-only in `data/history/`.

Identifiers are stable slugs, never reused: `ent_<name>`, `rel_<counterparty>_<type>_<year>`, `ev_<number>`, `proj_<entity>_<site>`.

**Examples below use a fictional entity (`ent_example`) and placeholders on purpose.** Do not copy example values into real records.

---

## schema/enums.json (the only place enums are defined)

Every other file in this package refers to these lists. Validators, badges and filters read from this file.

```json
{
  "cluster": ["nvidia", "ai_lab", "neocloud", "hyperscaler", "semis_supply", "sovereign_project", "portfolio", "vehicle", "lender", "other"],
  "type": ["EQ", "EQ-SPV", "EQ-C", "BK", "LB", "GU", "RV", "FC", "LP", "PP", "LI", "CX"],
  "status": ["definitive", "loi_or_framework", "reported_unconfirmed", "restructured", "terminated", "completed"],
  "claim_basis": ["filed", "company_announced", "reported_corroborated", "reported_single_source"],
  "label": ["fact", "analysis"],
  "reconciliation": ["reconciled", "partial", "one_sided", "contradicted"],
  "seniority": ["common_equity", "preferred_equity", "warrants", "spv_equity", "lp_interest", "senior_secured_creditor", "unsecured_creditor", "guarantor", "contingent_buyer", "lessee", "prepaying_buyer", "licensee", "none"],
  "grade": ["Strong", "Adequate", "Watch", "Weak", "Distressed", "Insufficient information"],
  "wwr": ["specific", "general", "none"],
  "lens": ["revenue_quality", "lender_reliance", "collateral_loop", "contagion", "signaling"],
  "direction": ["negative", "positive", "mixed"],
  "evidence_kind": ["sec_filing", "company_release", "earnings_call", "regulator", "rating_agency", "lien_registry", "news", "market_data"],
  "sourcing": ["filing", "named", "documents_seen", "anonymous"],
  "change_type": ["added", "amount_changed", "status_changed", "reconciliation_changed", "dates_changed", "evidence_added", "market_value", "link_repair", "reverified", "corrected", "removed_from_display"],
  "project_role": ["covered", "context"],
  "event_kind": ["announcement", "signing", "filing", "closing", "amendment", "drawdown", "restructuring", "termination", "holding_change"]
}
```

Badge labels on screen map one to one: status `definitive` → "Definitive", `loi_or_framework` → "Letter of intent", `reported_unconfirmed` → "Reported, unconfirmed", `restructured` → "Restructured", `terminated` → "Terminated", `completed` → "Completed". Claim basis is shown separately as a small source-strength chip: "Filed", "Company announced", "Reported, two sources", "Reported, one source".

## The amount object (used for every amount)

```json
{
  "value": null,
  "as_of": "YYYY-MM-DD",
  "fiscal_period": "<e.g. Nvidia FY2026 Q3, or null>",
  "original_currency": "USD",
  "original_value": null,
  "fx_rate": null,
  "fx_date": null,
  "last_verified": "YYYY-MM-DD",
  "display_eligible": false,
  "lower_bound": false,
  "evidence": ["ev_0000"]
}
```

`value` is always USD. `display_eligible` is set by `checks.py`, never by hand.

**Not applicable versus unknown.** An amount that cannot exist for the deal type is stored as `0` with `"not_applicable": true`, not null: `contingent_max` for EQ, EQ-SPV, PP and LI unless a source shows a contingent term; `committed_total` for open-market or 13F stakes. Only true unknowns are null, and only they go into `gross_missing`. Grounding checks `original_value` when `original_currency` is not USD, and checks `fx_rate` against its own evidence. `last_verified` lives on each amount, not the record (see `11`).

## entities.json

```json
{
  "id": "ent_example",
  "name": "<legal name>",
  "short_name": "<display name>",
  "cluster": "<enum cluster>",
  "depth": 1,
  "public": true,
  "ticker": "<or null>",
  "cik": "<from EDGAR, or null>",
  "country": "<ISO code>",
  "credit": {
    "grade": "<enum grade>",
    "grade_reason": "<two sentences, analysis>",
    "public_ratings": [{"agency": "<agency>", "rating": "<rating>", "date": "YYYY-MM-DD", "evidence": []}],
    "debt_outstanding": "<amount object>",
    "maturities_24m": "<amount object>",
    "liquidity_months": {"value": null, "inputs": [], "label": "analysis"},
    "top_customer_share": "<amount-like object with value as a fraction>",
    "evidence": []
  }
}
```

Nvidia itself is `ent_nvidia`, cluster `nvidia`, depth 0, CIK `0001045810`.

## relationships.json

```json
{
  "id": "rel_example_bk_2025",
  "from": "ent_nvidia",
  "to": "ent_example",
  "type_primary": "<enum type>",
  "types_secondary": [],
  "title": "<short title>",
  "insight_template": "<sentence with {placeholders}, see rule below>",
  "definition": "<plain description, two to four sentences>",
  "status": "<enum status>",
  "claim_basis": "<enum claim_basis>",
  "amounts": {
    "headline": "<amount object>",
    "committed_total": "<amount object>",
    "funded": "<amount object>",
    "contingent_max": "<amount object plus a 'trigger' string>",
    "annual_obligation": "<amount object, optional>",
    "market_value": "<amount object plus 'price_source'>"
  },
  "dates": {"announced": null, "signed": null, "filed": null, "effective": null, "maturity": null},
  "seniority": "<enum seniority>",
  "reconciliation": {
    "result": "<enum reconciliation>",
    "nvidia_side": "<text with evidence ids>",
    "counterparty_side": "<text with evidence ids, or 'No disclosure found as of YYYY-MM-DD'>",
    "differences": [{"field": "", "nvidia_value": null, "counterparty_value": null, "evidence": []}]
  },
  "derived": {
    "committed_unfunded": null,
    "gross_exposure": null,
    "gross_missing": [],
    "ead_base": null, "ead_max": null,
    "loss_base": null, "loss_max": null,
    "circularity_ratio": {"value": null, "window": null, "inputs": []},
    "round_trip": {"nvidia_paid": null, "counterparty_nvidia_spend": null, "window": null, "inputs": []},
    "share_of_counterparty_capital": {"value": null, "inputs": []},
    "share_of_nvda_equity": {"value": null, "inputs": []},
    "share_of_nvda_fcf": {"value": null, "inputs": []},
    "backstop_coverage": {"value": null, "inputs": []}
  },
  "credit": {"wwr": "<enum wwr>", "wwr_reason": "", "collateral": "", "notes": ""},
  "consequences": {
    "first_order": [{"trigger": "", "mechanism": "", "affected": [], "direction": "<enum>", "text": ""}],
    "second_order": [{"lens": "<enum lens>", "trigger": "", "mechanism": "", "affected": [], "direction": "<enum>", "text": ""}]
  },
  "projects": [],
  "depth2_links": [],
  "aggregate_of": null,
  "significance": {"score": null, "components": {}},
  "version": 1,
  "evidence": []
}
```

All `derived` fields are written by `pipeline/measure.py` only, always labeled analysis. Consequences are always analysis.

`aggregate_of` is set on unattributed-remainder nodes (see `05` section 3); such records are excluded from every total. They use `to: "ent_nvidia_unattributed"` (a synthetic entity, cluster `other`) and the id pattern `rel_unattributed_<aggregate>_<balance sheet date>`.

### Insight rule

The insight is stored as a template. Numbers enter only through placeholders filled by a formatter from `amounts` or `derived` (for example `{funded}`, `{contingent_max}`, `{dates.maturity:year}`). Any digit or number word typed directly into the template fails the check. Maximum 25 words after rendering. No dashes of any kind.

### Significance score (sizing and sorting, analysis)

`score = 40 × gross exposure percentile + 25 × contingent share of gross + 15 × circularity percentile + 10 × counterparty weakness + 10 × lender reliance`, each component 0 to 1, weights in `config/significance.json`. Counterparty weakness is computed from the displayed indicators (liquidity months, maturities, concentration, public rating), never from the internal letter grade. A missing component scores 0.5 (neutral) and is listed, so an opaque private counterparty is not ranked as the safest. Formula shown on the Method view.

## evidence.json

```json
{
  "id": "ev_0000",
  "tier": "<1 | 2 | market>",
  "kind": "<enum evidence_kind>",
  "publisher": "",
  "title": "",
  "url": "",
  "accession": "<filings only>",
  "section": "<Item, Note or page>",
  "published": "YYYY-MM-DD",
  "retrieved": "YYYY-MM-DDThh:mm:ssZ",
  "quote": "<verbatim, under fifteen words>",
  "locator": "<character offset in the cached file, or XBRL fact id>",
  "unit_scale_locator": "<offset of a table header such as '(in millions)', or null>",
  "parent_company": "<from the allowlist, e.g. Dow Jones for WSJ and Barron's>",
  "cites_publisher": [],
  "cache_path": "research/cache/<file>",
  "content_hash": "<sha256 of the cached file>",
  "sourcing": "<enum sourcing>",
  "paywalled": false,
  "supports": ["rel_example_bk_2025.amounts.contingent_max"]
}
```

The grounding check in `09` uses `cache_path`, `content_hash`, `quote` and `locator`. For paywalled articles the cache holds what a human pasted in review, marked as such.

## projects.json

```json
{
  "id": "proj_example_site",
  "entity": "ent_example",
  "name": "", "location": "",
  "power_mw_contracted": "<amount-like>", "power_mw_energized": "<amount-like>",
  "gpu_generation": null, "gpu_count": null,
  "anchor_tenant": null, "contract_years": null,
  "financing": [{"facility": "", "lenders": [], "balance": "<amount object>", "secured_by": "", "covenant_ltv": null, "evidence": []}],
  "expected_completion": null,
  "nvidia_link": [],
  "role": "<enum project_role>",
  "evidence": []
}
```

## events.json (timeline)

`{id, date, relationship, kind, summary, evidence}`, with `kind` from `event_kind` in enums.

## scenarios.json

Generated from `config/scenarios.json` plus the register: parameters with their basis, affected node ids, stressed EAD and loss, not-computable list.

## Change log and history

- `data/changelog.json` is append-only and private: `{timestamp, relationship, change_type, field, old, new, evidence, approved_by, auto_rule}`.
- Each publish writes `data/published/changelog.json` for the What changed view, filtered so any `old` or `new` value that is not display eligible appears as "Not confirmed", and with `approved_by` removed.
- Each publish snapshots `published/` to `data/history/YYYY-MM-DDThhmmssZ/`, so two publishes on one day never collide.
- No record is deleted. Removal from display is a status change with history kept.


<!-- end of 06_DATA_SCHEMA.md -->

# 07 · Application Spec

## Design principle

One idea per screen. Within ten seconds of landing, the reader should know three things: how much Nvidia has put behind its own customers, how much of it is binding, and where the risk concentrates. Everything else sits one click deeper. No decoration. Every number opens its source.

The structure follows the US Economy Monitor so the two read as a family: a written summary at the top generated from the data, then the main visual, then the detail.

---

## Page structure (top to bottom)

### 1. Header
- "Built By Resolute Business Development" with a link to resolute-bd.com, top left, same treatment as the Economy Monitor.
- Title: **Is Nvidia the Central Bank of AI?** Subtitle: "Every dollar Nvidia has put behind the companies that buy its chips, with sources."
- A "Data as of [date]" pill and a "Last change [date]" pill that opens What changed.

### 2. The summary (generated, not hand written)
Three to five sentences built from the data by templates in the pipeline, each figure linked to its source. Example form, not content: "Nvidia has [N] disclosed financial relationships with companies in the AI buildout. [X] is funded, [Y] is committed but not yet paid, and [Z] is contingent on events such as unsold capacity. The headline total announced is [H], of which [share] is legally binding." Numbers enter only through placeholders filled from the published data.

### 3. Headline tiles (four)
Funded · Committed, not yet paid · Contingent maximum · Headline announced. The first three add up to gross exposure; headline is shown apart and never added. Each tile states the number, the count of relationships, and a one-line note. Clicking a tile filters the map to that category.

### 4. The Constellation (main view)
A radial map drawn in SVG in the page.
- Nvidia at the center.
- Rings by cluster: AI labs, neoclouds, semis and supply, hyperscalers and offtakers, sovereign and projects (vehicles such as GPU-owning SPVs sit here), portfolio. Lenders appear only as depth-2 satellites. Entities in `other`, including unattributed remainders, sit in an outer band labeled "Other and unattributed". Each ring is labeled.
- Node size by gross exposure (funded plus committed not yet paid plus contingent maximum; see `05`). Base and stressed EAD appear only in the panel and the Stress view. A specific wrong-way risk mark sits on nodes where exposure grows as the counterparty weakens.
- Node outline: by default a neutral outline; letter grades color the outline only if Thomas turns grades on (`05` section 5).
- Edge color and line style for every exposure type come from the meaning map in `08`.
- Edge thickness by gross exposure, drawn solid; headline-only drawn as a faint outer stroke so the gap between promise and commitment is visible at a glance.
- Closed loops (Nvidia to A to B to Nvidia) can be highlighted with a toggle: "Show circular flows".
- Depth-2 parties (lenders, offtakers) appear as small satellites only when their depth-1 node is selected.
- Hover: name, type, gross exposure (marked "at least" when a lower bound), date. Click: opens the relationship panel.
- Keyboard: every node is focusable, arrow keys move between nodes in a ring, Enter opens.
- On phones the Constellation becomes a ranked list grouped by cluster; the radial view is offered as an optional full-screen.

### 5. Relationship panel (click to open, sections collapse)
Slides in from the right on desktop, full screen on phones. Built with native `details` and `summary` so it works without script.

Always visible at the top:
- Counterparty name, cluster, type badge, status badge and source-strength chip, with labels taken from `schema/enums.json` (`06`).
- **The insight**, one sentence in serif.
- The amounts in a row (funded, committed not yet paid, contingent maximum, headline), unknowns shown as "Not disclosed" and amounts that fail the display rule shown as "Not confirmed", each with a source chip and its as-of date.
- Key dates: announced, effective, matures, last verified.
- Significance bar with its score and a "why" link.

Collapsed by default, each a `details` section:
1. **What the deal is**: the plain-English definition.
2. **Both sides**: what Nvidia disclosed, what the counterparty disclosed, the reconciliation result, any differences listed.
3. **Project basis** (neoclouds and vehicles): the project table from `projects.json`.
4. **Credit read**: public ratings, debt and maturities, liquidity months, customer concentration, collateral, wrong-way risk (specific, general or none, with reason). Letter grade only if grades are turned on.
5. **Exposure and derived measures**: gross exposure, base and stressed EAD and loss side by side, circularity ratio and round-trip and the other measures, each labeled Analysis, with formula and inputs, no adjectives.
6. **First order consequences**.
7. **Second order consequences**, grouped by lens.
8. **Timeline** of this relationship's events.
9. **Sources**: every citation, tier badge, publisher, date, accession number, short quote, link.

A control at the top of the panel: "Expand all" and "Collapse all". The open or closed state of each section is remembered per visitor (local storage wrapped in try and catch).

### 6. The Ledger
A sortable, filterable table of every relationship: counterparty, cluster, type, status, funded, committed not yet paid, contingent maximum, gross exposure, headline, announced, last verified, reconciliation, significance, and grade only when grades are turned on. The totals row sums funded, committed not yet paid and contingent maximum, which never overlap; committed total (which includes funded) is available in the panel and the CSV, labeled as such. Filters: cluster, type, status, wrong-way risk, date range, source strength. Unattributed remainder rows are shown in their own section below the table and excluded from the totals row. Each row expands in place to the same sections as the panel. Download as CSV with the source URL column included; the CSV follows the same column rules, and its grade column exists only when grades are turned on.

### 7. Timeline
A horizontal dated track from 2023 to today, one lane per cluster, a mark per event. Brushing a date range filters the Constellation and Ledger. Makes visible how fast the commitments accumulated and when deals were restructured.

### 8. Loops
A flow diagram of the closed loops found in R9: Nvidia money in, purchases back, rentals out, drawn as paired arrows with amounts and dates. Each loop states its circularity ratio and the caveat that the computation needs both sides sourced.

### 9. Stress
Three scenario buttons (S1, S2, S3 from `05`) with sliders for their parameters. Selecting one highlights affected nodes, shows stressed EAD and loss against Nvidia's equity and free cash flow, lists the assumptions with their basis, and lists anything not computable. A plain sentence at the top: "These illustrate how losses would travel, not forecasts."

### 10. Is Nvidia a central bank?
The four-function table from `05` section 1, with a verdict and the evidence for and against each function, plus the one paragraph on where the analogy breaks. Under 300 words.

### 11. What changed
A reverse-chronological list from `changelog.json`: date, relationship, what changed, old value, new value, source. Filter by type of change. This is how a returning reader sees what moved since their last visit.

### 12. Method and sources
How the data was gathered, the source policy, definitions of every term, the significance formula, the EAD formula, the staleness rule, and the not-investment-advice disclaimer.

---

## Copy rules

- Plain words a non-specialist can follow. Define every credit term on first use with a hover note.
- No em dashes. No hype ("massive", "staggering", "game-changing"). Numbers do the work.
- Every inference says so: a small "Analysis" label beside it.
- Insight sentences state the risk, not the drama. Model template: "Nvidia has agreed to buy whatever capacity {counterparty} cannot sell through {dates.maturity:year}, so its exposure grows exactly when demand weakens." Numbers and names come only from placeholders.
- Run `anthropic-skills:human-voice` on all generated templates and on every insight.

## Interaction and performance requirements

- First paint under one second on a mid-range laptop; data under 1 MB compressed.
- `build_site.py` renders the summary, tiles, Ledger rows and every panel's content into the HTML at build time, so they work with JavaScript off; script adds sorting, filtering, the map and the panel slide-in.
- URL reflects state: `#rel=rel_example_bk_2025&view=constellation&scenario=s1`, so any view can be shared.
- Accessibility: contrast AA at minimum, focus rings visible, panel traps focus and closes on Escape, charts have text equivalents, color is never the only carrier of meaning (edge style plus label as well).
- Print stylesheet: the Ledger and an open panel print cleanly for a board pack.


<!-- end of 07_APPLICATION_SPEC.md -->

# 08 · Design System: Frida Kahlo, as on the US Economy Monitor

These tokens are copied from the live Economy Monitor page (`us-economy-monitor/site/index.html`, read 22 November 2026). Use them exactly so the two products read as one family. If the monitor's tokens change, the monitor wins; re-read its page before building.

## The idea behind the palette

Kahlo's palette is Mexican folk color on a plaster wall: cobalt from the Casa Azul, cochineal red, rosa mexicano, marigold, leaf green, ochre earth. On this app the colors carry meaning, not decoration. The wall stays calm and warm; color appears only where money moves.

## Tokens

```css
:root {
  --wall: #FBFAF6;         /* page ground, warm plaster */
  --panel: #FFFFFF;        /* cards, panels */
  --line: #E4E1D8;         /* hairlines */
  --ink: #1B1D26;          /* text, 16.1:1 on wall */
  --ink-2: #555A6B;        /* secondary text, 6.6:1 */
  --ink-3: #8A8E9C;        /* tertiary, 3.1:1: large text and non-text only */
  --cobalt: #1F4FA8;       /* 7.3:1 */
  --cobalt-deep: #173C82;  /* 10.0:1 */
  --cobalt-wash: #EAF0FA;
  --cochineal: #B5263A;    /* 6.1:1 */
  --rosa: #C9357A;         /* 4.7:1 */
  --leaf: #2F7A52;         /* 5.0:1 */
  --ochre: #C27F0A;        /* 3.2:1: marks and large text only */
  --marigold: #F0B429;     /* 1.8:1: fills and highlights only, never text */
  --serif: var(--font-anthropic-serif, Georgia, "Times New Roman", serif);
  --sans: var(--font-anthropic-sans, system-ui, -apple-system, "Segoe UI", sans-serif);
}
```

Contrast ratios above were computed against `--wall`. Rule carried over from the monitor's video review: highlight rings use ochre, not marigold, on the light page.

## Meaning map

| Meaning | Color | Line style (so color is never the only signal) |
|---|---|---|
| Nvidia (center) | `--ink` fill, marigold ring | Double ring |
| Equity (EQ, EQ-SPV) | `--cobalt` | Solid |
| Conditional equity (EQ-C) | `--cobalt` at 40% | Solid, hollow core |
| Backstop, guarantee (BK, GU) | `--cochineal` | Dashed |
| Leaseback, capacity rental (LB) | `--rosa` | Dotted |
| Financing commitment (FC) | `--cobalt-deep` | Solid with arrowhead |
| Supply prepayment (PP) | `--ochre` | Double line |
| Residual value or repurchase (RV) | `--cochineal` | Dash-dot |
| Fund commitment (LP) | `--cobalt` at 60% | Solid with cross ticks |
| License (LI) | `--leaf` | Thin solid |
| Context (CX) | `--ink-3` | Hairline |
| Headline-only portion | Same hue at 20% | Wide faint halo behind the committed stroke |
| Specific wrong-way risk | Small `--cochineal` notch on the node | Notch shape plus "Specific wrong-way risk" in the hover and panel |
| Counterparty grade (only if grades are turned on) | Node outline: Strong `--leaf`, Adequate `--cobalt`, Watch `--ochre`, Weak `--rosa`, Distressed `--cochineal`, Insufficient information `--ink-3` | Outline thickness rises with weakness, plus a text label in the panel |
| Analysis label | `--ink-2` text on `--cobalt-wash` chip | The word "Analysis" |

## Type

- Serif (`--serif`) for the title, section headings and every insight sentence. This is the voice of the page.
- Sans (`--sans`) for interface, tables and numbers. Numbers use tabular figures (`font-variant-numeric: tabular-nums`) so columns align.
- Scale to match the monitor: title about 2.4rem serif; section headings 1.4rem serif; body 1rem; table and chip text 0.8125rem. Key figures in tiles 2rem sans, below the heading's visual weight (lesson from the Economic Index dashboard critique).

## Components to reuse from the monitor

Chips (`em-chip` pattern with `aria-pressed`), tiles, drawers, history charts and the "Built By" header. Copy their markup and class names where possible so a future shared stylesheet is easy.

## Motion

Panel slides in over 180 ms, ease-out. Constellation nodes fade into place on first load over 400 ms, then never animate again unless the user changes a filter. Respect `prefers-reduced-motion`: no movement, instant state changes.

## What not to do

No gradients, no glow, no drop shadows beyond a 1px hairline, no folk-art illustration or Kahlo imagery (the palette is the reference, not her paintings), no logos of counterparties (names in text only).


<!-- end of 08_DESIGN_SYSTEM.md -->

# 09 · QA and Critic Gates

Four gates. Nothing passes a gate with an open critical finding. The automated checks are built in R0 (see `10`), so they run from the first research record onward.

---

## Automated checks (`make check`; also run by every scheduled job)

| Check | Fails when |
|---|---|
| Schema | Any record fails its JSON Schema or uses a value outside `schema/enums.json` |
| Evidence resolution | Any evidence id does not resolve, or any non-null amount has no evidence |
| **Grounding** | An evidence `quote` is not found verbatim (whitespace normalized) in the cached file at `cache_path`; or the cached file's hash differs from `content_hash`; or an amount it supports does not appear in the quote or within 300 characters of `locator` in the cached text (numbers matched after normalizing units, for example "$6.3 billion" equals 6.3e9, and after applying the scale at `unit_scale_locator` for table figures such as "(in millions)"). Non-USD amounts ground `original_value`. XBRL-sourced figures must match the fact value at the fact id |
| Display rule | `display_eligible` is set false on any amount supported neither by a tier 1 source nor by two independent tier 2 sources (see `04`). The check fails if any ineligible amount is rendered as a number, or feeds any tile, total, derived measure, scenario, significance score, summary sentence or the public change log. Market data follows the single exception in `04`. Arithmetic is recomputed from eligible amounts only, independently of the pipeline |
| Independence | Two tier 2 sources share a `parent_company` (for example WSJ and Barron's), or either lists the other in `cites_publisher` |
| Source allowlist | An evidence URL domain is not in `config/sources_allowlist.json`, or a market data domain supports anything other than `market_value` |
| Dates | A displayed number lacks `as_of`; an amount's `last_verified` is past its limit in `11` without a stale badge |
| Headline leakage | Any tile, total or summary sentence includes `headline` in committed_total, committed_unfunded, funded, contingent_max or gross figures |
| Amount order | Where known, `funded ≤ committed_total ≤ headline` is violated |
| Aggregate exclusion | A record with `aggregate_of` set is included in any total |
| Arithmetic | Tiles and summary differ from an independent recomputation from the register |
| Insight rules | Rendered insight over 25 words; template contains a digit or number word; any placeholder unresolved |
| Copy scan | Any em dash (U+2014), en dash (U+2013), figure dash (U+2012) or minus sign (U+2212) in text we write: `site/` and `data/published/`, **excluding** evidence `quote`, evidence `title` and URLs, which stay verbatim for grounding and render inside a quotation element. Banned words from the human-voice skill. Formulas on the Method view use a plain hyphen-minus |
| Quotes | Any quote of fifteen words or more |
| Reconciliation | `contradicted` or `partial` without a differences list |
| Links | Weekly: a source URL no longer returns 200 and is not marked paywalled or moved |

## Gate R · Register complete (end of research)

1. Automated checks pass on the whole register.
2. **Independent re-sourcing.** A fresh subagent that has not seen the research re-sources from scratch: every relationship where any of headline, committed_total or contingent_max is $1B or more; every relationship with status `loi_or_framework`, `reported_unconfirmed` or `restructured`; every value equal to a seed register value; plus a random 20% of the rest. Any mismatch reopens that relationship.
3. Seed register: every row `confirmed`, `modified` or `killed`, with reason.
4. `anthropic-skills:critic-agent` on the register, cluster reports and system view, up to three rounds. The critic must answer:
   - Is any headline number treated as exposure anywhere?
   - Is any one-sided relationship presented as reconciled?
   - Would any consequence read the same for a different company?
   - Do restructured or abandoned deals show their current status?
   - Is anything sourced to an excluded publication, or displayed on one tier 2 source?
   - Does the "central bank" verdict claim more than the evidence supports?
5. The datapack's totals tie to the register.
6. Thomas approves in chat. The approval date becomes the **Gate R cutoff** in `research/SCOPE.md`.

## Gate B · Application complete

1. Automated checks pass.
2. Every acceptance test in `10` passes.
3. Screenshots at 1440, 1024, 768 and 390 pixels, reduced motion on and off.
4. Keyboard-only walkthrough of every view, screen reader labels, contrast.

## Gate U · Continuous update proven

1. A fixture filing in the inbox produces a queue item; approval publishes it; the change log, history snapshot and What changed all show it.
2. A simulated failure (source unreachable, schema failure, grounding failure) blocks publishing and leaves the live site unchanged.

## Gate Q · Before publishing

**First publish only:**
1. Run every watcher and the news task in backfill mode (`--since` the Gate R cutoff) and resolve every queue item, so the first public version reflects deals that changed during the build. Full-text queries that overflow are split by narrower date ranges per `02` R2.
2. `design:design-critique` on every view.

**Every publish that changes displayed data:**
3. `anthropic-skills:critic-agent` on each new or changed insight and consequence.
4. Approval as set out in `11` U3. This gate does not define its own thresholds.


<!-- end of 09_QA_AND_CRITIC_GATES.md -->

# 10 · Build Plan

## Repository layout

```
nvidia-central-bank/
  spec/                      this package
  research/
    PLAN.md  SCOPE.md  seed_status.csv  candidates.csv  unconfirmed.md
    cache/                   cached sources for grounding: filings in full; news only as the grounding window (300 characters either side of the locator). Stored with git LFS in the private repository so CI can read it
    evidence/                working notes only; the canonical evidence store is data/register/evidence.json
    reports/                 R0.md to R9.md, cluster reports
    Nvidia_Exposure_Datapack.xlsx
  schema/                    JSON Schemas for every data file
  config/
    sources_allowlist.json   significance.json   draw_rates.json   scenarios.json
    grade_rubric.json   display.json   auto_approve.json   staleness.json   limits.json
  data/
    inbox/   queue/   approved/   register/   published/   history/   changelog.json
  pipeline/
    edgar.py                 SEC client: User-Agent from env, throttle, cache
    xbrl.py                  companyfacts reader
    extract.py               filing section extraction
    watchers/                one module per watcher in 11
    tasks/news_watch.md      prompt for the scheduled news task
    triage.py                inbox to queue
    review.py                local review page
    measure.py               EAD, derived measures, significance
    scenarios.py             S1 to S3
    summarize.py             template sentences for the summary
    build_site.py            writes site/index.html with summary, tiles, Ledger and panels rendered into the HTML
    checks.py                every automated check in 09
  site/
    index.html               single self-contained page, charts drawn in-page
  tests/
  .github/workflows/         watch.yml  triage.yml  publish.yml  checks.yml
  SCHEDULE.md   README.md   Makefile
```

**Two repositories.** The working repository (pipeline, research, register, cache, queue) is **private**. A separate **public** repository holds only `site/` and `data/published/`, and is what GitHub Pages serves. `publish.yml` pushes to it. Cached article text is never public.

Python 3.11+, standard library plus `requests`, `jsonschema`, `lxml` or `beautifulsoup4` for filing HTML, `openpyxl` for the datapack. The page uses no framework and loads nothing from other websites, the same rule as the Economy Monitor, so it stays fast and lasts.

## Milestones

| # | Milestone | Done when |
|---|---|---|
| R0 | Research tooling: SEC client, cache, XBRL reader, extractor, `schema/enums.json`, JSON Schemas, `checks.py` with tests, `measure.py`, `scenarios.py`, and the configs research needs (`sources_allowlist.json`, `grade_rubric.json`, `draw_rates.json`, `scenarios.json`, `significance.json`, `staleness.json`) | `make check` runs and its fixture tests pass, including grounding and display eligibility |
| R1 to R9 | Research sequences | Gate R passed, Thomas approved |
| B1 | Remaining configs: display, auto-approve, limits | Each loaded and validated by the pipeline |
| B2 | Pipeline: measure, scenarios, summary, published build | `published/` regenerates from `register/` deterministically; totals tie to datapack |
| B3 | Page shell, header, summary, tiles, Ledger | Ledger lists every relationship with working filters, sorting, CSV export |
| B4 | Relationship panel with collapsible sections | Every section renders for every relationship; works with script off |
| B5 | Constellation, Timeline, Loops, Stress | Visual checks at four widths; keyboard navigation complete |
| B6 | Central bank verdict, What changed, Method | Copy passes human-voice; disclaimer present |
| U1 to U5 | Continuous update per `11` | Gate U passed |
| Q | Final critic and design critique | Gate Q passed; publish |

## Acceptance tests

1. Clicking any node or Ledger row opens a panel showing the insight, the four amounts with source chips, and the dates.
2. Each panel section expands and collapses; Expand all and Collapse all work; state survives reload.
3. Every number on the page opens its citation list in one click.
4. Changing the cluster filter updates the tiles, Constellation and Ledger to the same totals.
5. Headline amounts never appear inside committed, funded, contingent or gross totals (fixture where only headline is known), and an unattributed remainder record is never counted in any total.
5a. A fixture record whose quote is absent from its cached source fails `make check` (grounding).
5b. A fixture figure supported by a single tier 2 source displays as "Not confirmed" **and** is absent from every tile, total, derived measure, scenario and summary sentence.
5c. A filing quote containing an en dash passes grounding and the copy scan, and renders inside a quotation element.
6. A relationship with status `terminated` appears greyed with its history, not deleted.
7. Selecting S1 highlights the expected nodes from a test fixture and shows that scenario's EAD and loss (from `scenarios.json`, not the 100% maximum) equal to an independent calculation. A fixture with a negative demand shock produces a backstop draw greater than zero.
8. The URL reproduces the view: open a copied link in a new browser and the same panel and scenario appear.
9. With a fixture filing dropped in the inbox, triage creates a queue item; approving it updates the site, the change log, the history snapshot and What changed.
10. A fixture citation from an excluded domain fails `make check`.
11. Page works at 390 pixels wide; Constellation becomes the ranked list.
12. No U+2012, U+2013, U+2014 or U+2212 in text we write, per the copy scan in `09`; verbatim quotes, titles and URLs are exempt.
13. Lighthouse accessibility score 95 or higher; performance 90 or higher.


<!-- end of 10_BUILD_PLAN.md -->

# 11 · Continuous Update

The map stays current without anyone editing JSON by hand, and nothing unverified reaches the live site.

## The loop

```
watchers  →  inbox  →  triage and extraction  →  review queue  →  approval  →  publish  →  change log + snapshot
(scheduled)  (raw hits)  (Claude drafts a diff,     (checks and     (human, or   (site
                          grounded in cached docs)   critic notes)   auto rule)   rebuilds)
```

---

## U1 · Watchers

Python modules in `pipeline/watchers/`. Every watcher accepts `--since YYYY-MM-DD` for backfill; scheduled runs use their normal lookback. They write raw hits to `data/inbox/YYYY-MM-DD/<watcher>.jsonl` with a content hash so nothing is processed twice. Watchers never write to `register/` or `published/`.

| Watcher | Checks | Source | Frequency (Eastern) |
|---|---|---|---|
| `earnings_calendar` | Nvidia's next earnings date and each counterparty's | Company investor relations event pages | Weekly |
| `nvda_filings` | New Nvidia filings, any form | `data.sec.gov/submissions/CIK0001045810.json` | Every 2 hours, weekdays 6 am to 10 pm; hourly for the ten days after each Nvidia earnings date |
| `counterparty_filings` | New filings by every entity with a CIK | Same endpoint per CIK | Every 4 hours, weekdays |
| `fulltext_nvidia` | New hits for queries Q1 to Q12 in `02`, filtered by the 50-word window rule | EDGAR full-text search, last 3 days | Daily, 7:10 am |
| `nvda_13f` | New 13F-HR | Submissions endpoint | Daily for 45 days after each quarter end, else weekly |
| `ownership_filings` | Schedules 13D and 13G, Forms 3 and 4, with Nvidia as filer or subject | Submissions endpoint | Daily |
| `ir_releases` | Nvidia and counterparty releases | Each company's own release page or RSS | Every 4 hours |
| `ratings` | Rating actions on counterparties | Agency press release pages that are public; logged-in pages are skipped and flagged for manual check | Daily |
| `market_values` | Prices for public stakes, market value only | Market data source named in `04` | Weekdays after the close |
| `liens` | New UCC financing statements and Companies House charges naming counterparties | State UCC search portals, Companies House | Monthly |
| `staleness` | Amounts past their re-verification limit | Internal | Daily |

**News is not a Python watcher.** Searching tier 2 publications needs Claude's web search, which a GitHub Actions script cannot call. A **scheduled Claude task** runs twice daily (7:37 am and 5:37 pm Eastern), searches only the tier 2 domains in `04` for Nvidia plus each counterparty plus the exposure keywords from `02` R4, and hands its hits to a small `ingest_news.yml` workflow through `workflow_dispatch` (hits passed as an uploaded file). That workflow commits them to `data/inbox/YYYY-MM-DD/news.jsonl` inside the shared concurrency group, so it never races the other jobs. The inbox publishes nothing, so no review is skipped. The task's prompt is stored in `pipeline/tasks/news_watch.md` and accepts a `since` date for backfill.

## U2 · Triage and extraction

A GitHub Actions job runs Claude Code headless over the inbox daily at 8:15 am Eastern, after the 7:10 full-text run and the 7:37 news task, and on demand:

1. **Triage**: discard hits with no money, commitment or credit support between Nvidia and another party; log each discard with reason.
2. **Match** to an existing relationship or mark as new.
3. **Fetch** the source. Filings are cached in full to `research/cache/` (git LFS, private repository). News articles are fetched to a temporary file only.
4. **Extract** a proposed change as a diff, with every new figure carrying a verbatim quote and locator. For news, after extraction write only the grounding window (300 characters either side of the quote) to the cache, delete the temporary file, set the locator as an offset into the window file and hash the window file. The same procedure applies in research sequence R4. For a filed item, also search the other party's filings and record silence if none (R5 rule).
5. **Check**: run every automated check in `09`, grounding included. Proposals that fail grounding are kept in the queue marked "failed grounding", never published.
6. **Critic**: run `anthropic-skills:critic-agent` on any new or changed insight and consequence text.
7. Write `data/queue/<id>.json`: summary, diff, evidence, check results, critic notes, proposed `change_type`.

Paywalled tier 2 articles cannot be read by the job. They enter the queue as "needs quote": the reviewer pastes the relevant sentence, which is cached and then grounded like any other source.

Requirements: `ANTHROPIC_API_KEY` as a repository secret and a monthly spend cap in `config/limits.json` (default to be set by Thomas). The job stops and alerts when the cap is reached.

## U3 · Review and approval

- `make review` opens a local review page listing queue items: summary, old and new side by side, evidence links and quotes, check results, critic notes.
- Actions: Approve, Edit then approve, Reject with reason, Hold. Approving writes the item to `data/approved/<id>.json` and commits it, which triggers `publish.yml`.
- **Auto-approved without a human** (rules in `config/auto_approve.json`): `market_value` updates and `link_repair`. Nothing else.
- **Always needs a human**: any change to `headline`, `committed_total`, `funded` or `contingent_max` at any size, including null to a value; any `added`, `status_changed`, `reconciliation_changed`, `dates_changed`, `corrected`; any `evidence_added` that changes `claim_basis`, the corroboration count or the reconciliation result; every `reverified`.
- A scheduled task sends Thomas a short summary of pending items on weekdays at 8:57 am Eastern, after the 8:15 triage, only when the queue is not empty. Three consecutive watcher failures appear at the top of that summary.

## U4 · Publish

On a commit to `data/approved/`:
1. Apply the diff to `data/register/`; increment `version`.
2. Update `last_verified` **only on the amount fields a human re-checked** in this item. Auto-approved market value and link changes never touch `last_verified`.
3. Append to `data/changelog.json`.
4. Rebuild `data/published/`. Totals, derived measures, scenarios and summary sentences are recomputed from the register, never patched.
5. Run every check. Any failure stops the publish and leaves the live site unchanged.
6. Snapshot to `data/history/YYYY-MM-DDThhmmssZ/`.
7. Update "Data as of" and "Last change", rebuild the page, deploy.

## U5 · Schedule and infrastructure

Same pattern as the Economy Monitor after its 20 November 2026 fix, when GitHub's own scheduler skipped runs:
- Workflows: `watch.yml`, `triage.yml`, `publish.yml`, `checks.yml`, each startable by `workflow_dispatch`.
- Workflows: also `ingest_news.yml`. All workflows that write to the repository share one GitHub Actions `concurrency` group, so they run one at a time and never collide on push.
- An external scheduler (cron-job.org, as the monitor uses) calls `workflow_dispatch` on the timetable in U1; GitHub's own cron stays as a backup.
- A fine-grained GitHub token limited to the two repositories (Actions read and write, contents write), created by Thomas.
- Secrets, never committed: `SEC_USER_AGENT`, `ANTHROPIC_API_KEY`, the scheduler token.
- Hosting: the public site repository (see `10`) on GitHub Pages at `nvidia.resolute-bd.com` (DNS in Squarespace, like `economy.resolute-bd.com`).
- `SCHEDULE.md` in the repository: the timetable, what each run does, how to run it by hand.

## Staleness rule (per amount field)

| Relationship | Re-verify every |
|---|---|
| Any of headline, committed_total or contingent_max at $1B or more | 30 days |
| Status `loi_or_framework`, `reported_unconfirmed` or `restructured`, any size | 30 days |
| Other `definitive` relationships | 90 days |
| `completed` or `terminated` | 365 days |

Past the limit, the amount shows "Not re-verified since [date]" and the `staleness` watcher queues it. Triage does the work first: re-fetches the source, re-runs grounding, and checks for newer filings or reports on the deal. Items where nothing changed are grouped on one **batch confirm** screen, so Thomas confirms them in a single pass; only items where something moved get individual review.

## Failure handling

- Watchers retry at the next scheduled run; three consecutive failures raise an alert.
- Blocked or rate-limited sources back off. A disallowed source is never substituted.
- The live site always shows the last good publish.


<!-- end of 11_CONTINUOUS_UPDATE.md -->

