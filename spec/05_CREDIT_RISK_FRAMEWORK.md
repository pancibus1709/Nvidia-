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
