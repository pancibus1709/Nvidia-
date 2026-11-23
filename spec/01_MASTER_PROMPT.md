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
