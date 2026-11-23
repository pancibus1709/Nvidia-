# R1 part A: Nvidia's disclosed aggregates (10-K and 10-Q, Jan 2023 to Jul 2026)

Namespace `r1a`, evidence ev_10001 to ev_10324 (324 records, all from Nvidia's own filings, CIK 0001045810). Machine-readable version: `research/drafts/r1_aggregates.json`.
Nvidia's fiscal year ends on the last Sunday of January (FY2027 = Jan 26 2026 to Jan 31 2027, a 53-week year). Figures in USD. "n.d." means the filing does not disclose the item. Percentages are shares of revenue or of receivables.

Filings (period end · fiscal period · form · filed · accession):

| Period end | Fiscal | Form | Filed | Accession |
|---|---|---|---|---|
| 2026-07-26 | FY2027 Q2 | 10-Q | 2026-08-26 | 0001045810-26-000075 |
| 2026-04-26 | FY2027 Q1 | 10-Q | 2026-05-20 | 0001045810-26-000052 |
| 2026-01-25 | FY2026 (Q4) | 10-K | 2026-02-25 | 0001045810-26-000021 |
| 2025-10-26 | FY2026 Q3 | 10-Q | 2025-11-19 | 0001045810-25-000230 |
| 2025-07-27 | FY2026 Q2 | 10-Q | 2025-08-27 | 0001045810-25-000209 |
| 2025-04-27 | FY2026 Q1 | 10-Q | 2025-05-28 | 0001045810-25-000116 |
| 2025-01-26 | FY2025 (Q4) | 10-K | 2025-02-26 | 0001045810-25-000023 |
| 2024-10-27 | FY2025 Q3 | 10-Q | 2024-11-20 | 0001045810-24-000316 |
| 2024-07-28 | FY2025 Q2 | 10-Q | 2024-08-28 | 0001045810-24-000264 |
| 2024-04-28 | FY2025 Q1 | 10-Q | 2024-05-29 | 0001045810-24-000124 |
| 2024-01-28 | FY2024 (Q4) | 10-K | 2024-02-21 | 0001045810-24-000029 |
| 2023-10-29 | FY2024 Q3 | 10-Q | 2023-11-21 | 0001045810-23-000227 |
| 2023-07-30 | FY2024 Q2 | 10-Q | 2023-08-28 | 0001045810-23-000175 |
| 2023-04-30 | FY2024 Q1 | 10-Q | 2023-05-26 | 0001045810-23-000093 |
| 2023-01-29 | FY2023 (Q4) | 10-K | 2023-02-24 | 0001045810-23-000017 |

## What changed and when

1. **Investment commitments first disclosed in the Q3 FY2026 10-Q (Oct 26, 2025):** $6.5 billion, including $5 billion in Intel Corporation subject to regulatory approval (ev_10154, ev_10155). They then rise to $11.4 billion (Jan 2026, ev_10121), $27 billion (Apr 2026, ev_10072) and $25 billion (Jul 2026, ev_10032). Before Oct 2025 no investment-commitment figure was disclosed. The Q2 FY2026 10-Q said only that its $45.8 billion of total commitments "include ... investments" (ev_10179).
2. **Non-marketable equity went up about 14 times in four quarters:** $3.8 billion (Jul 2025, ev_10167), $8.2 billion (Oct 2025, ev_10138), $22.3 billion (Jan 2026, ev_10099), $42.3 billion (Apr 2026, ev_10064) and $47.9 billion (Jul 2026, ev_10001). Net additions were $17.4 billion in FY2026 (ev_10100), $17.9 billion in Q1 FY2027 (ev_10065) and $13.1 billion in Q2 FY2027 (ev_10002). In Q2 FY2027, $12.3 billion moved to marketable after public trading began (ev_10006).
3. **Publicly-held equity went from immaterial to $40 billion and more:** $381 million (Jan 2025, ev_10206), $17.7 billion (Jan 2026, ev_10106) and $42.8 billion current at Jul 2026 (ev_10013), plus $5.0 billion of locked-up stock in Other assets (ev_10016). Level 2 warrants and convertible preferred of $10.8 billion first appear in Apr 2026 (ev_10076). $36.9 billion is under short-term lock-up (ev_10017). Issuers named in the filings: CoreWeave (ev_10186) and Intel (ev_10111).
4. **Guarantees first appear in Q3 FY2026:** an $860 million facility lease guarantee given in exchange for warrants (ev_10159). This became $3.5 billion of "land, power, and shell" guarantees by Jan 2026 (ev_10123). After the Q2 FY2027 period, in Aug 2026, Nvidia gave **SB Energy guarantees capped at $105 billion** for leases to an OpenAI affiliate, which takes the total maximum gross exposure to $108.5 billion (ev_10040, ev_10041). The FY2026 10-K said "We have not entered into any financing arrangements" (ev_10127). The Q2 FY2027 10-Q describes "financial guarantees, and other forms of credit support and financing arrangements".
5. **A new category, "AI cloud agreements", appears in Q2 FY2027:** $36 billion, typically six years. AI clouds buy Nvidia systems and Nvidia commits to rent the capacity back. The clouds can stop providing it to Nvidia and sell it to third parties (ev_10035, ev_10039). This is the closest disclosed analogue to an obligation to buy unsold capacity.
6. **Supply and capacity commitments:** $4.9 billion (Jan 2023, ev_10308), $30.8 billion (Jan 2025, ev_10210), $95.2 billion (Jan 2026, ev_10118), $119 billion (Apr 2026, ev_10084) and **$279 billion (Jul 2026, ev_10029)**.
7. **Cloud service agreements:** $2.2 billion (Jan 2023, first entered in H2 FY2023, ev_10311, ev_10317), $10.9 billion (Jan 2025, ev_10212), $26 billion (Oct 2025, ev_10151) and $30 billion (Apr 2026, ev_10085). The figure then falls to $29 billion (Jul 2026, ev_10030) and the stated purpose changes to R&D of open models (Nemotron, Cosmos, GR00T). DGX Cloud is no longer mentioned.
8. **Equity method and VIEs first disclosed in Q1 FY2027:** $1.0 billion in infrastructure funds, with maximum loss of $2.3 billion (ev_10070, ev_10071). By Q2 FY2027 this is $3.3 billion in "infrastructure financiers", classed as VIEs with maximum loss exposure of $4.7 billion (ev_10010, ev_10011).
9. **The prepaid supply breakdown stopped being disclosed after Oct 2025.** The FY2026 10-K moved non-marketable equity to its own balance-sheet line and gives no "Other assets" table (see Not found).
10. **Total equity investments of $99 billion and commitments of $25 billion at Jul 26, 2026** (MD&A, ev_10043, ev_10044). The Aug 2026 MOUs aim to mobilize more than $500 billion of third-party capital. They are preliminary (ev_10045) and are a headline only, not exposure.

## 1. Investments: non-marketable equity

Carrying value under the measurement alternative. Before FY2025 the 10-Qs showed this as "Privately-held equity securities, Level 3".

| Period end | Fiscal | Carrying value | Net additions (period) | Unrealized gains (period) | Impairments and losses (period) | Cumulative gross unrealized gains / losses |
|---|---|---|---|---|---|---|
| 2026-07-26 | FY27 Q2 | $47,898M (ev_10001) | $13,106M Q2 (ev_10002); $31,005M H1 (ev_10003) | $4,900M Q2 (ev_10004); $7,504M H1 (ev_10005) | $121M Q2 (ev_10007); reclassified to marketable $12,323M (ev_10006) | $9.1B (ev_10008) / $250M (ev_10009) |
| 2026-04-26 | FY27 Q1 | $42,336M (ev_10064) | $17,899M (ev_10065) | $2,603M (ev_10066) | reclassified $389M (ev_10067) | $5.3B (ev_10068) / $199M (ev_10069) |
| 2026-01-25 | FY26 | $22,251M (ev_10099) | $17,444M FY (ev_10100) | $2,369M FY (ev_10101) | $101M (ev_10103); reclassified $848M (ev_10102) | $2.7B (ev_10104) / $176M (ev_10105) |
| 2025-10-26 | FY26 Q3 | $8,187M (ev_10138) | $3,704M Q3 (ev_10139); $4,652M 9M (ev_10140) | $758M (ev_10141) | $74M (ev_10142) | $1.4B (ev_10143) / $167M (ev_10144) |
| 2025-07-27 | FY26 Q2 | $3,799M (ev_10167) | $299M (ev_10168) | $267M (ev_10169) | n.d. | $661M (ev_10170) / $93M (ev_10171) |
| 2025-04-27 | FY26 Q1 | $3,240M (ev_10183) | $649M (ev_10184) | n.d. | CoreWeave reclassified $843M (ev_10185, ev_10186) | $396M (ev_10189) / $110M (ev_10190) |
| 2025-01-26 | FY25 | $3,387M (ev_10200) | $1,309M FY (ev_10201) | $816M FY (ev_10202); one $565M secondary-sale gain (ev_10205) | n.d. | $1.1B (ev_10203) / $105M (ev_10204) |
| 2024-10-27 | FY25 Q3 | $2,237M (ev_10217) | $409M (ev_10218) | n.d. | n.d. | $374M (ev_10219) |
| 2024-07-28 | FY25 Q2 | $1,819M (ev_10228) | $294M (ev_10229) | n.d. | n.d. | $362M (ev_10230) |
| 2024-04-28 | FY25 Q1 | $1,463M (ev_10240) | $127M (ev_10241) | n.d. | n.d. | n.d. |
| 2024-01-28 | FY24 | $1,321M (ev_10253) | $859M FY (ev_10254) | one $178M secondary-raise gain (ev_10255) | n.d. | $270M (ev_10256) |
| 2023-10-29 | FY24 Q3 | $1,019M (ev_10268) | n.d. | n.d. | n.d. | n.d. |
| 2023-07-30 | FY24 Q2 | $676M (ev_10280) | n.d. | n.d. | n.d. | n.d. |
| 2023-04-30 | FY24 Q1 | $496M (ev_10293) | n.d. | n.d. | n.d. | n.d. |
| 2023-01-29 | FY23 | $288M (ev_10304) | n.d. | n.d. | n.d. | n.d. |

Other related figures:
- The balance-sheet "Non-marketable securities" line was $51,157M at Jul 2026 (ev_10012) and $43,364M at Apr 2026 (ev_10073). It includes equity method investments; the line was renamed in Q1 FY2027.
- "Investments in non-affiliated entities" in Other assets (private plus public): $1,750M (Apr 2024, ev_10243), $1,546M (Jan 2024, ev_10258), $1,172M (Oct 2023, ev_10270), $800M (Jul 2023, ev_10282), $505M (Apr 2023, ev_10295), $299M (Jan 2023, ev_10306).
- Invested in the period (MD&A): $18.6B in private companies and infrastructure funds in FY27 Q1 (ev_10083; cash purchases of non-marketable securities $18,582M, ev_10081). $17.5B in FY2026 (ev_10114; cash $17,502M, ev_10116). H1 FY27 cash purchases of equity securities were $42,404M (ev_10022) and sales $7,241M (ev_10023).
- Equity gains in income: gains from equity securities, net, $7,771M in Q2 FY27 (ev_10020) and $23,707M in H1 (ev_10021). Other income (expense), net, $15,929M in Q1 FY27 (ev_10080). Other income, net, $9,022M in FY2026 (ev_10110), driven by equity gains including Intel (ev_10111).

## 1b. Investments: publicly-held (marketable) equity

| Period end | Fiscal | Fair value | Detail |
|---|---|---|---|
| 2026-07-26 | FY27 Q2 | $42,783M current (ev_10013) + $4,957M in Other assets (ev_10016) | Level 1 $36,934M (ev_10014); Level 2 (warrants, convertible preferred) $10,806M (ev_10015); $36.9B under short-term lock-up (ev_10017); unrealized gains $1.5B Q2 / $12.5B H1 (ev_10018, ev_10019) |
| 2026-04-26 | FY27 Q1 | $30,237M current (ev_10074) + $8.9B LT (ev_10077) | L1 $29,887M (ev_10075); L2 $9,214M (ev_10076); $27.4B locked (ev_10078); unrealized gains $13.4B (ev_10079) |
| 2026-01-25 | FY26 | $17,726M (ev_10106) | $4.8B LT locked to Dec 2027 (ev_10108); $10.5B under lock-up (ev_10107); unrealized gains $6.6B FY (ev_10109); Intel named (ev_10111) |
| 2025-10-26 | FY26 Q3 | $3,869M (ev_10145) | unrealized gains $670M Q3 (ev_10146) |
| 2025-07-27 | FY26 Q2 | $3,199M (ev_10172) | the one investment reclassified in Q1 FY26 was worth $2.8B (ev_10173); unrealized gains $1.9B Q2 (ev_10174) |
| 2025-04-27 | FY26 Q1 | $1,251M (ev_10188) | CoreWeave, Inc. fair value $1B (ev_10187) |
| 2025-01-26 | FY25 | $381M (ev_10206) | unrealized gains $163M FY (ev_10207) |
| 2024-10-27 | FY25 Q3 | $472M (ev_10220) | |
| 2024-07-28 | FY25 Q2 | $419M (ev_10231) | reclassified from Other assets to marketable securities from this quarter |
| 2024-04-28 | FY25 Q1 | $287M in Other assets (ev_10242) | |
| 2024-01-28 | FY24 | $225M (ev_10257) | |
| 2023-10-29 | FY24 Q3 | $153M (ev_10269) | |
| 2023-07-30 | FY24 Q2 | $124M (ev_10281) | |
| 2023-04-30 | FY24 Q1 | $9M (ev_10294) | |
| 2023-01-29 | FY23 | $11M (ev_10305) | |

Analysis: total public equity at Jul 26, 2026 is $47,740M (L1 + L2), and at Apr 26, 2026 it is $39,101M. These are sums, not quoted figures.

Warrants and derivatives (Q2 FY27, Note 8): public company warrants notional $4,800M (ev_10026), fair value $824M, Level 3 (ev_10024); equity forward contract notional $1,000M (ev_10027).

## 1c. Equity method and VIEs

| Period end | Fiscal | Equity method carrying value | Maximum loss exposure |
|---|---|---|---|
| 2026-07-26 | FY27 Q2 | $3.3B in "infrastructure financiers" (ev_10010) | VIEs $4.7B including future committed amounts; Nvidia is not the primary beneficiary and does not consolidate (ev_10011) |
| 2026-04-26 | FY27 Q1 | $1.0B in "infrastructure funds" (ev_10070) | $2.3B including future committed amounts (ev_10071) |
| 2026-01-25 and earlier | | the FY2026 10-K says "Equity method investments were not material"; no VIE disclosure | n.d. |

No related-party transactions, special purpose vehicles or consolidated VIEs are disclosed in any of the 15 filings.

## 2. Commitments and contingencies

### 2a. Supply and purchase obligations, totals

| Period end | Fiscal | Supply, capacity and inventory obligations | Other non-inventory obligations | Total future commitments |
|---|---|---|---|---|
| 2026-07-26 | FY27 Q2 | $279B (ev_10029) | n/a (new table) | $366B main table (ev_10034) + $56B "additional commitments" (ev_10038) |
| 2026-04-26 | FY27 Q1 | $119B, $95B due rem. FY27 (ev_10084) | other vendor $6B (ev_10087) | n.d. as a single figure |
| 2026-01-25 | FY26 | $95.2B (ev_10118) | other $3.4B (ev_10122) | n.d. |
| 2025-10-26 | FY26 Q3 | $50.3B (ev_10150) | other $2.1B (ev_10158) | n.d. |
| 2025-07-27 | FY26 Q2 | n.d. (no breakdown) | n.d. | $45,774M including investments and cloud (ev_10177, ev_10179) |
| 2025-04-27 | FY26 Q1 | $29.8B (ev_10193) | $13.7B (ev_10194) | $43,520M (ev_10196) |
| 2025-01-26 | FY25 | $30.8B (ev_10210) | $14.3B (ev_10211) | $45,079M (ev_10213) |
| 2024-10-27 | FY25 Q3 | $28.9B (ev_10223) | $13.2B (ev_10224) | $42,044M (ev_10226) |
| 2024-07-28 | FY25 Q2 | $27.8B (ev_10234) | $12.0B (ev_10235) | $39,781M (ev_10237) |
| 2024-04-28 | FY25 Q1 | $18.8B (ev_10246) | $10.6B (ev_10247) | $29,373M (ev_10249); plus about $1.2B for business combinations and land (ev_10250) |
| 2024-01-28 | FY24 | $16.1B (ev_10261) | $4.6B (ev_10262) | $20,707M (ev_10264) |
| 2023-10-29 | FY24 Q3 | $17.11B (ev_10274) | $4.43B (ev_10275) | $21,540M (ev_10277) |
| 2023-07-30 | FY24 Q2 | $11.15B (ev_10286) | $4.31B (ev_10287) | $15,460M (ev_10289) |
| 2023-04-30 | FY24 Q1 | $7.27B (ev_10298) | $3.26B (ev_10299) | $10,527M (ev_10301) |
| 2023-01-29 | FY23 | $4.92B, including $810M unpaid on prepaid supply deals (ev_10308, ev_10309) | $3.14B (ev_10310) | $8,063M (ev_10312) |

**Newest schedule, Jul 26, 2026 (Note 10, $ billions, by fiscal year):**

| Category | Rem. FY27 | FY28 | FY29 | FY30 | FY31 | FY32+ | Total | Evidence |
|---|---|---|---|---|---|---|---|---|
| Supply and capacity | 92 | 87 | 88 | 6 | 5 | 1 | 279 | ev_10097, ev_10029 |
| Cloud service agreements | 3 | 8 | 7 | 6 | 4 | 1 | 29 | ev_10030 |
| Data center leases not commenced | 0 | 1 | 1 | 2 | 1 | 20 | 25 | ev_10031 |
| Equity investments | 18 | 3 | 2 | 2 | 0 | 0 | 25 | ev_10032 |
| Capital expenditures | 7 | 1 | 0 | 0 | 0 | 0 | 8 | ev_10033 |
| **Total** | 120 | 100 | 98 | 16 | 10 | 22 | 366 | ev_10034 |
| *Additional:* AI cloud agreements | 0 | 6 | 8 | 7 | 6 | 9 | 36 | ev_10036, ev_10035 |
| *Additional:* DC leases not commenced for third party | 0 | 0 | 1 | 1 | 1 | 17 | 20 | ev_10037 |
| *Additional total* | 0 | 6 | 9 | 8 | 7 | 26 | 56 | ev_10038 |

Year cells other than the first are read from the same table rows the evidence quotes. The supply row's FY30 to FY32+ cells and the total row's yearly cells are outside the 14-word quotes, but they are in the same table, within 300 characters.

### 2b. Multi-year cloud service agreements (Nvidia as renter of compute)

| Period end | Fiscal | Total | Schedule / purpose |
|---|---|---|---|
| 2026-07-26 | FY27 Q2 | $29B (ev_10030) | rem. FY27 3, FY28 8, FY29 7, FY30 6, FY31 4, FY32+ 1. "These commitments provide the cloud infrastructure to support our research and development of our open models, such as NVIDIA Nemotron, Cosmos, and GR00T, and our autonomous vehicle software" |
| 2026-04-26 | FY27 Q1 | $30B (ev_10085) | 6/7/7/5/3/2 (ev_10086); "Cloud service capacity may be reduced or terminated"; mainly R&D |
| 2026-01-25 | FY26 | $27B (ev_10119) | FY27 7, FY28 6, FY29 5, FY30 5, FY31 2, FY32+ 2 (ev_10120); capacity "may be reduced, terminated or sold to others by the CSPs" |
| 2025-10-26 | FY26 Q3 | $26B (ev_10151) | FY26 Q4 1, FY27 6, FY28 6, FY29 5, FY30 4, FY31+ 4 (ev_10152); for R&D and DGX Cloud (ev_10153) |
| 2025-07-27 | FY26 Q2 | n.d. (inside the $45.8B total, ev_10179) | |
| 2025-04-27 | FY26 Q1 | $10.6B (ev_10195) | R&D and DGX Cloud |
| 2025-01-26 | FY25 | $10.9B (ev_10212) | |
| 2024-10-27 | FY25 Q3 | $11.3B (ev_10225) | |
| 2024-07-28 | FY25 Q2 | $9.8B (ev_10236) | |
| 2024-04-28 | FY25 Q1 | $8.8B (ev_10248) | |
| 2024-01-28 | FY24 | $3.5B (ev_10263) | |
| 2023-10-29 | FY24 Q3 | $3.60B (ev_10276) | |
| 2023-07-30 | FY24 Q2 | $3.50B (ev_10288) | |
| 2023-04-30 | FY24 Q1 | $2.43B (ev_10300) | |
| 2023-01-29 | FY23 | $2.23B (ev_10311) | first entered in H2 FY2023 (ev_10317); CSP partners bought Nvidia products "to support multi-year cloud service agreements" (ev_10313) |

**AI cloud agreements (new in Q2 FY27):** $36B, typically six years (ev_10035). "AI clouds procure our data center infrastructure products and we commit to cloud service agreements, which the AI clouds can unilaterally stop providing to us and sell to third-party customers" (ev_10039). The commitment decreases as third parties or Nvidia use the capacity. Nvidia shares revenue if certain criteria are met. Analysis: this is functionally a capacity backstop (BK). No counterparties are named.

### 2c. Commitments to invest in other companies

| Period end | Fiscal | Amount | Wording and conditions |
|---|---|---|---|
| 2026-07-26 | FY27 Q2 | $25B (ev_10032; MD&A ev_10044) | "We committed to make certain equity investments in AI model makers, infrastructure financiers, and other private companies, subject to certain contingencies." By FY: rem. FY27 18, FY28 3, FY29 2, FY30 2 |
| 2026-04-26 | FY27 Q1 | $27B (ev_10072) | "subject to certain contingencies, which we expect will be made through the remainder of fiscal year 2027" |
| 2026-01-25 | FY26 | $11.4B (ev_10121) | "subject to certain contingencies"; MD&A: "We are finalizing an investment and partnership agreement with OpenAI" (ev_10125), no amount |
| 2025-10-26 | FY26 Q3 | $6.5B (ev_10154) | "including $5 billion in Intel Corporation which is subject to regulatory approval" (ev_10155); a letter of intent "with an opportunity to invest in OpenAI" (ev_10156), headline only with no amount; after the period, in Nov 2025, "to invest up to $10 billion in Anthropic", subject to closing conditions (ev_10157) |
| 2025-07-27 and earlier | | n.d. | Q2 FY26 total commitments "include ... investments" (ev_10179). Q1 FY25 shows about $1.2B "to complete business combinations ... and acquire land and buildings" (ev_10250), which are not equity investments |

Equity investments held, per MD&A: $99B at Jul 26, 2026 (ev_10043).

### 2d. Guarantees, indemnifications and capacity backstops

| Period end | Fiscal | Maximum gross exposure | Detail |
|---|---|---|---|
| 2026-07-26 | FY27 Q2 | $3.5B land, power and shell guarantees for AI clouds (ev_10042; notional $3,529M, ev_10025) | partners' escrow $712M (ev_10028). **Aug 2026 (after the period):** SB Energy Corp. guarantees capped at $105B (ev_10040), credit support for ~4.25 GW of leases to an affiliate of OpenAI Group PBC at the PORTS campus in Pike County, Ohio. Each guarantee becomes effective at lease commencement across nine phases (first expected FY2029) and is triggered on tenant default. It terminates when OpenAI reaches a satisfactory credit rating. The site will exclusively host Nvidia infrastructure. Nvidia has an option for ~3.8 GW more. Total exposure including SB Energy is $108.5B (ev_10041) |
| 2026-04-26 | FY27 Q1 | $3.5B facility lease guarantees (ev_10088) | escrow $712M (ev_10089); given "in exchange for warrants" (ev_10098) |
| 2026-01-25 | FY26 | $3.5B (ev_10123) | escrow $712M (ev_10124); MD&A: "We provided $3.5 billion in land, power, and shell guarantees" to early-stage companies (ev_10115) |
| 2025-10-26 | FY26 Q3 | $860M, one partner (ev_10159) | escrow $470M (ev_10160); the partner agreed to sell the data center capacity (ev_10161); guarantee given for warrants |
| 2025-07-27 and earlier | | none disclosed | |

Indemnifications appear in every filing in standard language: tax, product, employee and IP indemnities, with no maximum stated and no liability recorded (for example Q2 FY27 Note 10). Residual value: Aug 2026 MD&A says Nvidia "may provide limited residual-value support for a portion of specific projects" at its option (ev_10046). No amount is given.

### 2e. Data center leases not yet commenced

$25B for Nvidia's own use plus $20B "for third party" that Nvidia expects to reassign (Jul 2026, ev_10031, ev_10037). $22.7B (Jan 2026, ev_10126). $7.6B (Jan 2025, ev_10214).

## 3. Balance sheet components: prepaid supply, prepaid cloud and other assets

| Period end | Fiscal | Prepaid supply and capacity, long-term | Prepaid supply and capacity, short-term | Prepaid cloud services |
|---|---|---|---|---|
| 2026-07-26 | FY27 Q2 | n.d. | n.d. | n.d. |
| 2026-04-26 | FY27 Q1 | n.d. | n.d. | n.d. |
| 2026-01-25 | FY26 | n.d. | n.d. | n.d. |
| 2025-10-26 | FY26 Q3 | $1,536M (ev_10147) | $2.0B (ev_10148) | n.d. |
| 2025-07-27 | FY26 Q2 | $1,776M (ev_10175) | $1.8B (ev_10176) | n.d. |
| 2025-04-27 | FY26 Q1 | $2,079M (ev_10191) | $2.1B (ev_10192) | n.d. |
| 2025-01-26 | FY25 | $1,747M (ev_10208) | $3.3B (ev_10209) | n.d. |
| 2024-10-27 | FY25 Q3 | $2,041M (ev_10221) | $3.2B (ev_10222) | n.d. |
| 2024-07-28 | FY25 Q2 | $1,313M (ev_10232) | $3.3B (ev_10233) | n.d. |
| 2024-04-28 | FY25 Q1 | $2,232M (ev_10244) | $3.3B (ev_10245) | n.d. |
| 2024-01-28 | FY24 | $2,458M (ev_10259) | $2.5B (ev_10260) | n.d. |
| 2023-10-29 | FY24 Q3 | $2,927M (ev_10271) | $743M (ev_10272) | $60M (ev_10273) |
| 2023-07-30 | FY24 Q2 | $3,008M (ev_10283) | $799M (ev_10284) | $170M (ev_10285) |
| 2023-04-30 | FY24 Q1 | $3,002M (ev_10296) | n.d. | $171M (ev_10297) |
| 2023-01-29 | FY23 | $2,989M "Prepaid supply agreements" (ev_10307) | $458M (ev_10323) | n.d. |

Other assets (long-term) totals: $15,746M (Jul 2026, ev_10062) and $11,724M (Oct 2025, ev_10149). The FY26 10-K and the FY27 10-Qs give no breakdown of Other assets, apart from the locked public equity in Note 5 ($4,957M at Jul 2026).

Notes receivable or loans: none disclosed in any filing. Vendor financing: Q2 FY27 says that for investment-grade customers Nvidia has given and may give "longer payment terms ranging from 90 days up to one year" (ev_10051). Customer advances in deferred revenue were $2.8B at Jul 2026 (Note 7, not separately grounded). Accounts receivable were $63,059M at Jul 2026 (ev_10063).

## 4. Concentration of credit risk and customers

| Period end | Fiscal | Accounts receivable concentration | Direct customers >=10% of revenue | Indirect customers |
|---|---|---|---|---|
| 2026-07-26 | FY27 Q2 | five direct: 22/14/13/11/10% (ev_10047) | Q2: one at 16% (ev_10048); H1: 16/15/13% (ev_10049) | one "AI research and deployment company contributed a meaningful amount" through cloud purchases (ev_10050) |
| 2026-04-26 | FY27 Q1 | three: 30/18/16% (ev_10090) | three: 21/17/16% (ev_10091) | indirect customers include AI clouds and AI model makers |
| 2026-01-25 | FY26 | three: 25/18/13% (ev_10128) | 22% and 14% (ev_10129, ev_10130) | same AI research and deployment company statement (ev_10131) |
| 2025-10-26 | FY26 Q3 | four: 22/17/14/12% (ev_10162) | A 22%, B 15%, C 13%, D 11% (ev_10163, ev_10164) | |
| 2025-07-27 | FY26 Q2 | three: 23/19/14% (ev_10180) | A 23%, B 16% (ev_10181, ev_10182) | |
| 2025-04-27 | FY26 Q1 | three: 27/18/12% (ev_10197) | A 16%, B 14% (ev_10198, ev_10199) | |
| 2025-01-26 | FY25 | two: 17/16% (ev_10215) | A 12%, B 11%, C 11% (ev_10216) | |
| 2024-10-27 | FY25 Q3 | four: 18/13/11/11% (ev_10227) | A, B, C 12% each (ev_10316) | |
| 2024-07-28 | FY25 Q2 | three: 23/15/11% (ev_10238) | A 14%, B 11%, C 11%, D 10% (ev_10239) | |
| 2024-04-28 | FY25 Q1 | two: 16/15% (ev_10251) | A 13%, B 11% (ev_10252) | |
| 2024-01-28 | FY24 | two: 24/11% (ev_10265) | A 13% (ev_10266) | one indirect customer about 19% of FY24 revenue (ev_10267) |
| 2023-10-29 | FY24 Q3 | two: 11% each (ev_10278) | A 12% (Q3), B 11% (9M) (ev_10279) | |
| 2023-07-30 | FY24 Q2 | two: 16/13% (ev_10290) | one distributor about 17% (ev_10291) | one indirect customer about 22% Q2 and 19% H1 (ev_10292) |
| 2023-04-30 | FY24 Q1 | two: 12/10% (ev_10302) | none (ev_10303) | |
| 2023-01-29 | FY23 | two: 14/11% (ev_10314) | none (ev_10315) | |

The filings warn that the Customer A, B and so on labels "may represent different customers" from period to period. No customer is named.

## 5. Related parties, VIEs, SPVs, equity method

See 1c. VIEs are disclosed only at Jul 26, 2026: $4.7B maximum loss, not consolidated (ev_10011). No related-party transactions, SPVs or consolidated structures appear in any filing.

## 6. Subsequent events

| Filing | Items | Evidence |
|---|---|---|
| 10-Q FY27 Q2 | No note. Note 10 and MD&A report Aug 2026 events: SB Energy guarantees capped at $105B for an OpenAI affiliate's leases; MOUs with "several large capital providers" for platforms to mobilize more than $500B of third-party capital, preliminary and possibly never definitive; optional limited residual-value support | ev_10040, ev_10041, ev_10045, ev_10046 |
| 10-Q FY27 Q1 | none | |
| 10-K FY26 | No note. "finalizing an investment and partnership agreement with OpenAI" | ev_10125 |
| 10-Q FY26 Q3 | No note. Nov 2025 agreement to invest up to $10B in Anthropic, subject to closing conditions; letter of intent on OpenAI | ev_10157, ev_10156 |
| 10-Q FY25 Q1 | Note 15: stock split and dividend increase (not investment-related) | ev_10324 |
| Other 10 filings | no subsequent events note | |

## 7. Nvidia financial measures for the app (as of Jul 26, 2026, FY27 Q2)

| Measure | Value | Evidence |
|---|---|---|
| Total shareholders' equity | $228,984M | ev_10052 |
| Cash, cash equivalents and marketable debt securities | $56,586M | ev_10053 |
| Marketable equity securities (current) | $42,783M ($42.8B in MD&A) | ev_10013, ev_10054 |
| Cash plus all marketable securities (analysis) | $99,369M (56,586 + 42,783) | derived |
| Revenue Q2 FY27 | $96,221M | ev_10061 |
| Accounts receivable, net | $63,059M | ev_10063 |

**Free cash flow, trailing twelve months to Jul 26, 2026 (analysis).** The window is FY26 Q3 + FY26 Q4 + FY27 Q1 + FY27 Q2, built as FY2026 annual + FY2027 H1 - FY2026 H1:
- CFO: +102,718 FY26 (ev_10134) +74,421 H1 FY27 (ev_10055) -42,779 H1 FY26 (ev_10056) = **$134,360M**
- Purchases related to property and equipment and intangible assets: -6,042 FY26 (ev_10135) -4,434 H1 FY27 (ev_10057) +3,122 H1 FY26 (ev_10058) = **-$7,354M**
- **FCF TTM = $127,006M**. Principal payments on PP&E (finance-type) of -$92M in H1 FY27 are excluded.
- Revenue TTM: 215,938 (ev_10136) + 177,837 (ev_10059) - 90,805 (ev_10060) = **$302,970M**.

Other quarter-end values: equity $195,474M (Apr 2026, ev_10092), $157,293M (Jan 2026, ev_10132), $118,897M (Oct 2025, ev_10165). Cash plus marketable securities $62,556M (Jan 2026, ev_10133) and $60,608M (Oct 2025, ev_10166). Q1 FY27: CFO $50,344M (ev_10093), capex $1,757M (ev_10094), revenue $81,615M (ev_10095).

## XBRL concepts used (cross-check)

| Concept | Series result | Comparison with text |
|---|---|---|
| us-gaap:EquitySecuritiesWithoutReadilyDeterminableFairValueAmount | 288M (2023-01) ... 3,387M (2025-01), 8,187M (2025-10), 22,251M (2026-01), 42,336M (2026-04), 47,898M (2026-07) (ev_10318) | matches note text every period; FY24 quarterly values match "Privately-held equity Level 3" |
| us-gaap:EquitySecuritiesFVNINoncurrent | 1,546M (2024-01) ... 22,251M (2026-01) | used for non-marketable equity, not public equity |
| us-gaap:EquitySecuritiesFvNi | 12,886M (2026-01), 30,237M (2026-04), 42,783M (2026-07) (ev_10319) | current portion only; excludes the long-term locked portion (4,957M at Jul 2026) |
| us-gaap:PurchaseObligation | 8,063M (2023-01) to 45,774M (2025-07) (ev_10321) | matches text totals; **no fact after 2025-07-27**, so the text is the only source for $50.3B, $95.2B, $119B and $279B |
| us-gaap:OtherCommitment | 3.14B (2023-01) to 13.7B (2025-04) = other non-inventory obligations; **6.5B at 2025-10-26 = investment commitments** (ev_10322) | the concept's meaning changed in Q3 FY26; difference logged |
| us-gaap:GuaranteeObligationsMaximumExposure | 860M (2025-10-26); **108.5B at 2026-07-26** (ev_10320) | **difference:** the 108.5B tagged at 2026-07-26 includes the $105B SB Energy guarantees signed in Aug 2026, after the period. Per the text, exposure at the balance sheet date was $3.5B (ev_10042). The text wins |
| us-gaap:UnrecordedUnconditionalPurchaseObligationBalanceSheetAmount | 7.6B (2025-01), 22.7B (2026-01) | the tag is used for leases not yet commenced, not purchase obligations |
| us-gaap:OtherAssetsNoncurrent | 3,820M (2023-01) ... 15,746M (2026-07) | 2025-01-26 restated from 6,425M to 3,038M in the FY26 10-K because non-marketable equity was moved out; not a conflict |
| us-gaap:PrepaidExpenseAndOtherAssetsCurrent | 791M (2023-01) ... 3,409M (2026-07) | no prepaid-supply-specific concept is tagged |
| us-gaap:AccountsReceivableNetCurrent | 3,827M (2023-01) ... 63,059M (2026-07) | matches |

No XBRL concept was found for cloud service agreements, AI cloud agreements, prepaid supply and capacity, or equity method/VIE amounts.

## Not found

- **Prepaid supply and capacity agreements after Oct 26, 2025.** The FY26 10-K and the FY27 Q1 and Q2 10-Qs have no "Other assets" breakdown. Searched "Prepaid supply" and "repaid" in all three. Only the risk-factor wording remains: "purchase obligations and prepaids have grown".
- **Total commitments as a single figure** in the Q3 FY26, FY26 and Q1 FY27 filings. Only the components are given.
- **Cloud service agreements and the supply split in the Q2 FY26 10-Q.** Only a $45,774M total including investments is given.
- **Named investees beyond CoreWeave, Intel, Anthropic and OpenAI.** Infrastructure financiers, infrastructure funds, AI model makers and AI cloud partners are not named. The $3.5B guarantee partners are not named.
- **A formal Subsequent Events note** in 14 of 15 filings (Q1 FY25 has one, about the stock split only).
- **Notes receivable, loans, or "investments in non-affiliated entities"** after Apr 2024 (the line was renamed "Non-marketable equity securities").
- **Short-term prepaid supply at Apr 30, 2023** (the 10-Q table shows only the long-term amount).
- **Equity method and VIE amounts before Apr 2026** (the FY26 10-K says "not material").

## Unconfirmed

None. Every figure above is quoted from Nvidia's own filings. These counterparty facts appear only as text in Nvidia filings, without terms or amounts: the OpenAI LOI and the "finalizing" agreement have no amount; the Anthropic figure is "up to" $10B, subject to closing conditions, with no funded amount disclosed. R2 to R5 should confirm them on the counterparty side.

## Needs quote

None (no tier 2 sources used).

## Domains to add

None needed for this task.

## Open questions

1. How the $99B of "equity investments" in the Jul 2026 MD&A (ev_10043) reconciles with the balance sheet: non-marketable $51.2B + current marketable equity $42.8B + locked $5.0B is about $99.0B (analysis). Does it include warrants ($824M fair value)?
2. What the $25B of Jul 2026 equity investment commitments contains, and how much of the Apr 2026 $27B was funded in Q2 (net additions were $13.1B). Look for named items such as OpenAI and Anthropic in R3 and R4.
3. Who the "infrastructure financiers" (equity method VIEs, $3.3B carrying, $4.7B max loss) are, and whether they are the financing platforms in the Aug 2026 MOUs.
4. Who the AI cloud counterparties are in the $36B AI cloud agreements, and whether they overlap with the land, power and shell guarantee partners and with investees. Counterparty filings (R2) should name them.
5. Why cloud service agreements fell from $30B to $29B while the purpose changed: was DGX Cloud capacity moved into the AI cloud agreements?
6. The XBRL guarantee fact of 108.5B dated at period end overstates exposure at that date. Should the app use $3.5B at Jul 26, 2026 and $108.5B as of Aug 2026 (contingent_max, triggered only as leases commence from FY2029)?
