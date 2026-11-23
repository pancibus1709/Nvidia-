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
