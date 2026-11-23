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
