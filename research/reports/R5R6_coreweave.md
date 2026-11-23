# R5/R6 · CoreWeave, Inc. (CRWV, CIK 0001769628): NVIDIA counterparty side, debt and project basis

Namespace `crwv`, evidence ev_20001 to ev_20212 (212 records). Facts file: `research/drafts/coreweave_facts.json`.
Newest documents used: 10-Q for Q3 2026 (filed 2026-11-12), 424B5 ATM supplement (2026-09-17), DDTL 5.5 credit agreement (2026-08-07), DEF 14A (2026-04-22), 10-K FY2025 (2026-03-02).
"Analysis" marks figures I derived. Everything else is quoted from a filing.

## NVIDIA relationship as CoreWeave describes it

CoreWeave gives NVIDIA three roles: customer, supplier and stockholder. The 2025-09-15 8-K says so directly: "NVIDIA supplies the Company with NVIDIA GPUs and is a stockholder" (ev_20007).

- **Backstop order (2025-09-09).** "a new order form ... which has an initial value of $6.3 billion, that establishes an arrangement with respect to the sale by the Company of reserved cloud computing capacity to its customers and provides NVIDIA access to any residual unsold cloud computing capacity" (ev_20001, ev_20004). "NVIDIA is obligated to purchase the residual unsold capacity through April 13, 2032" (ev_20002). This is "subject to ... satisfaction of delivery and availability of service requirements" (ev_20005). The same text appears in the S-4 424B3 (ev_20190).
- **Termination.** Either party may terminate on 30 days' notice of a breach, or if the other party's insolvency proceeding is "not dismissed within 90 days" (ev_20006). Under the MSA, on termination the "Customer is released of payment obligations for Services that would have been provided" after termination (ev_20015). Analysis: the backstop does not survive a CoreWeave bankruptcy that lasts more than 90 days.
- **Capacity rental under the MSA (2023-04-10).** "we provide NVIDIA with our infrastructure and platform services through fulfillment of order forms submitted to us by NVIDIA" (ev_20029). NVIDIA paid about $320m cumulative to 2024-12-31 (ev_20033), $326.3m in FY2025 (ev_20025) and $59.6m in Q1 2026 (ev_20026).
- **Supplier.** "all of the GPUs used in our infrastructure today are NVIDIA GPUs" (ev_20127). "our current customers have contractually specified our use of NVIDIA GPUs" (ev_20128). "NVIDIA accounted for 17% of our total purchases from suppliers" in FY2025 (ev_20027).
- **Partner.** "We work with NVIDIA to deploy the latest GPU technologies at scale" (ev_20034, IPO).
- **Equity and framework (2026-01-23).** NVIDIA bought $2bn of stock at $87.20 per share (ev_20010). A "collaboration framework" aims to "accelerate the Company's buildout of more than 5 gigawatts" of AI factories by 2030 (ev_20011). In the joint release the companies "intend to ... Leverage NVIDIA's financial strength to accelerate CoreWeave's procurement of land, power and shell" (ev_20013). All of this is subject to "future execution of additional agreements and/or order forms" (ev_20012). It is headline only.
- **Related party status.** The proxy lists NVIDIA as a related party because it "beneficially owns more than 5%" (ev_20028). The Q3 2026 10-Q related-party note names only Magnetar, the co-founders and the JV, not NVIDIA (ev_20194).

## A. NVIDIA as shareholder

| Date | Event | Shares | % Class A | Source |
|---|---|---|---|---|
| Before IPO (Mar 2025) | Holding | 17,932,460 (ev_20030) | 5.96% (ev_20031); 5.18% after IPO, excluding any IPO purchase (ev_20032) | 424B4, 2025-03-31 |
| 2025-03-31 | 13G, Rule 13d-1(d) | 24,182,460 (ev_20017) | 7.0% (ev_20018) | NVIDIA 13G, 2025-05-15 |
| 2026-01-23 | Private placement purchase | +22,935,780 (ev_20008) at $87.20 (ev_20009), $2.0bn cash (ev_20010, ev_20014, ev_20114, ev_20145) | | 8-K, 2026-01-26 |
| 2026-01-23 | 13G/A No.1, Rule 13d-1(c), passive (ev_20021) | 47,213,353 (ev_20019) | 11.5% (ev_20020) | NVIDIA 13G/A, 2026-01-26 |
| Proxy (base 2026-04-15) | Holding | 47,213,353 (ev_20022) | 10.66% (ev_20023); 3.27% of voting power (ev_20024) | DEF 14A, 2026-04-22 |

Analysis:
- **Implied IPO purchase.** The 13G minus the pre-IPO holding is 6,250,000 shares. At the $40 IPO price that is $250m. CoreWeave does not state this purchase.
- **Unexplained shares.** The 13G/A total is 95,113 shares above the 13G holding plus the January 2026 purchase.
- **Current stake.** On 458,871,690 Class A shares outstanding at 2026-07-31 (ev_20040), the stake is 10.29%.
- **Cost basis.** Known funded cost is $2.0bn, plus $250m if the inferred IPO purchase is right. The pre-IPO price is not disclosed.

## B. NVIDIA as customer

| Agreement | Date | Type | Value | End | Residual-capacity obligation? | Evidence |
|---|---|---|---|---|---|---|
| Order form under the MSA | 2025-09-09 (8-K 2025-09-15) | BK | $6.3bn, stated as the "initial value" | 2032-04-13 | Yes, "obligated to purchase the residual unsold capacity" | ev_20001-ev_20007, ev_20015, ev_20190 |
| MSA order forms (rental) | MSA 2023-04-10 | LB | Paid: $320m cumulative to 2024 (ev_20033), $326.3m FY2025 (ev_20025), $59.6m Q1 2026 (ev_20026) | Runs until all order forms expire | No | ev_20029, ev_20016, ev_20146 |
| Collaboration framework | 2026-01-23 | Headline (BK/FC flavour) | None stated; >5 GW by 2030 | 2030 | No | ev_20011-ev_20013 |

- **Interaction with other customers.** CoreWeave sells reserved capacity to its own customers first. NVIDIA takes what is left (ev_20001).
- **Remaining performance obligations.** No filing says whether the $6.3bn is in RPO. The RPO note treats "committed cloud computing capacity that the Company has the right to resell" as variable consideration (ev_20097). Analysis: that wording is consistent with the backstop, but CoreWeave does not link it to NVIDIA.
- **Share of revenue.** Not disclosed. Analysis: FY2025 payments of $326.3m against revenue of $5.1bn (ev_20124) are about 6.4%. Those are cash payments, not recognized revenue.
- **Amounts due from NVIDIA.** Not disclosed.

## C. NVIDIA as supplier

| Item | Value | Evidence |
|---|---|---|
| GPUs in the fleet that are NVIDIA | All | ev_20127 |
| Customers who contractually specify NVIDIA GPUs | Yes | ev_20128 |
| NVIDIA share of FY2025 purchases | 17% (FY2025 supplier shares: 23%, 20%, 17%) | ev_20027, ev_20129 |
| GPU serial-number documents from NVIDIA or Dell feed lender collateral tracking | DDTL 3.0, §5.22 | ev_20210 |
| NVIDIA-provided financing, allocation or payment terms | None found. OEM financing of $7.4bn names no OEM | ev_20090 |

## D. Debt stack (10-Q, 2026-09-30, unless noted)

| Facility | Committed | Drawn | Rate | Maturity | Collateral / backing | Lenders / agents | Covenants | Evidence |
|---|---|---|---|---|---|---|---|---|
| DDTL 1.0 | $2.3bn | $1,139m | 15% eff. | 2028-03-28 | Special purpose vehicle (SPV) GPU servers and contracts | Blackstone, Magnetar | Restricted cash | ev_20133, ev_20045, ev_20143, ev_20147 |
| DDTL 2.0 | $7.6bn | $2,796m | 11% eff. | Aug 2030 | SPV; sized on the depreciable cost of GPU servers | Led by Blackstone and Magnetar | Restricted cash | ev_20134, ev_20046, ev_20144, ev_20147 |
| DDTL 2.1 | $3.0bn | $2,494m | SOFR+4.25% | Mar 2031 | As DDTL 2.0 | Not found | As DDTL 2.0 | ev_20135, ev_20047, ev_20140 |
| DDTL 3.0 | $2.6bn | $2,323m | SOFR+4.00% | Aug 2030 | OpenAI MSA of 2025-03-07, order form "Phoenix 1" | MUFG (agent), U.S. Bank (collateral agent) | DSCR first test moved to 2027-10-31; contract realization ratio; minimum liquidity cut to $100m; unlimited equity cures before 2026-10-28 | ev_20136, ev_20048, ev_20141, ev_20201-ev_20205, ev_20207-ev_20209, ev_20211 |
| DDTL 4.0 (non-recourse) | $8.5bn ($7.5bn initially) | $4,583m | SOFR+2.25% / ~5.9% fixed | 2032-03-31 | One contract with a "leading AI enterprise"; $5.2bn of assets | MUFG, Morgan Stanley | DSCR ≥1.15x; parent liable only for "bad acts" | ev_20075-ev_20080, ev_20064, ev_20164-ev_20172 |
| DDTL 5.0 | $3.1bn | $2,749m | SOFR+4.50% | 2031-11-15 | Two non-investment-grade customers | Morgan Stanley (agent), MUFG | DSCR ≥1.35x | ev_20081, ev_20082, ev_20049, ev_20174-ev_20178 |
| DDTL 5.5 | $2.6bn | $1,555m | SOFR+5.50% | 2031-09-01 | Five customer MSAs (names redacted), about 3-year contracts | JPMorgan (agent), MUFG, 11 bookrunners | DSCR ≥1.35x; cash sweep down to $1.3bn; cross-default above $35m; "Qualified Customer" needs only a borrower certificate | ev_20083, ev_20084, ev_20050, ev_20094, ev_20149-ev_20163 |
| Revolver | $2.5bn | $1,200m drawn; $546m of letters of credit; $754m available | 7% eff. | Nov 2029 | Pledged assets | Not found | Amended Nov 2025 | ev_20137, ev_20059, ev_20088, ev_20089 |
| 2030 senior notes, 9.25% | $2.0bn | $2.0bn | 9.25% | Jun 2030 | Unsecured, guaranteed by subsidiaries | 144A buyers | 101% change-of-control put | ev_20051, ev_20142, ev_20179 |
| 2031 senior notes, 9.00% | $1.75bn | $1.75bn | 9.00% | Feb 2031 | Unsecured | | | ev_20052 |
| 2031 senior notes, 9.75% | $2.75bn (incl. $1.0bn add-on) | $2.75bn | 9.75% | Oct 2031 | Unsecured | | 101% put | ev_20053, ev_20180, ev_20181 |
| 2032 senior notes, 9.625% | $1.25bn | $1.25bn | 9.625% | Jul 2032 | Unsecured | | | ev_20054 |
| 2032 EUR notes, 8.50% | €2.0bn, carried at $2,272m | | 8.50%, swapped | Jul 2032 | Unsecured | | | ev_20055 |
| 2031 convertible notes | $2,588m | | 1.75% | Dec 2031 | Unsecured | | | ev_20056 |
| 2032 convertible notes | $4.0bn | | 1.75%, converts at $119.60 | Oct 2032 | Unsecured | | | ev_20057, ev_20091 |
| 2033 convertible notes | $4.2bn | | 2.875%, converts at $97.85 | Apr 2033 | Unsecured | | | ev_20058, ev_20092 |
| OEM financing (recourse) | | $6,891m | ~10% | Dec 2026 to Jul 2030 | Equipment | OEMs not named | | ev_20060, ev_20090 |
| OEM financing (non-recourse) | | $770m | ~9% | Oct 2026 to Aug 2028 | Equipment | | | ev_20065 |
| Magnetar loan | | $195m | ~12% | Jan 2029 | | Magnetar | | ev_20061 |

| Debt totals | Value | Evidence |
|---|---|---|
| Recourse debt, net | $41,600m (current $9,183m) | ev_20062, ev_20063 |
| Non-recourse debt, net | $5,273m (current $1,389m) | ev_20066, ev_20067 |
| Total principal | $47,505m | ev_20071 |
| Principal due rest of 2026 / 2027 / 2028 | $2,433m / $10,974m / $5,479m | ev_20068-ev_20070 |
| Interest expense, Q3 2026 / 9M 2026 | $769m / $1,754m | ev_20073, ev_20072 |
| SPV debt secured by non-current assets | $22.2bn | ev_20086 |

Analysis: debt due within 24 months is about $17.5bn, with 2028 pro-rated. Against $9.84bn of liquidity that is about 1.78x.

## E. Liquidity, RPO and concentration

| Item | Value | Evidence |
|---|---|---|
| Cash and equivalents | $4,122m | ev_20104 |
| Restricted cash, current / non-current | $1,405m / $877m | ev_20105, ev_20106 |
| Undrawn committed facilities | $5,653m | ev_20108 |
| Total liquidity as CoreWeave defines it | $9,837m | ev_20109 |
| Operating cash flow / investing outflow, 9M 2026 | $5,638m / $24,710m | ev_20112, ev_20111 |
| Other purchase commitments | ~$4bn | ev_20113 |
| Leases not yet commenced (undiscounted) | $47.4bn | ev_20196 |
| Deferred revenue | $10.0bn, of which $1.9bn was moved to liabilities "as contracts became cancellable" | ev_20117, ev_20118, ev_20098 |
| RPO | $132.3bn at 2026-09-30, 36% within 24 months. Was $60.7bn at 2025-12-31 | ev_20095, ev_20096, ev_20122 |
| Revenue backlog (non-GAAP), Q2 2026 | $104.2B | ev_20184, ev_20182 |
| Top customer share of revenue | Q3 2026: 30% and 24% for the top two. 9M 2026 Customer A: 33%. FY2025 Microsoft: 67%. FY2024 Microsoft: 62%, top two 77% | ev_20099-ev_20101, ev_20125, ev_20035, ev_20036 |
| Named commitments | OpenAI $11.9bn (ev_20199) + $6.5bn (ev_20102); Meta $21.0bn (ev_20103) | |
| ATM equity program | Up to 35,000,000 shares | ev_20039 |

Analysis: annualizing the 9M investing outflow gives a liquidity cover of about 3.6 months. That ignores operating cash flow and new financing. A next-12-month capex total is not disclosed.

## F. Project basis

| Site / item | Data | Evidence |
|---|---|---|
| Portfolio, 2025-12-31 | 43 data centers; >850 MW active; ~3.1 GW contracted | ev_20120, ev_20121 |
| Portfolio, Q2 2026 call (2026-08-11) | 51 data centers; ~1.5 GW active; ~4.2 GW contracted (3.7 GW at 2026-06-30) | ev_20185, ev_20186, ev_20041, ev_20042 |
| GPUs | >250,000 at 2024-12-31 | ev_20189 |
| GPU depreciation life | 6 years (changed from 5 in 2023) | ev_20130 |
| Kenilworth, NJ joint venture | Developer owns 85%, CoreWeave 15% | ev_20197, ev_20212 |
| Unnamed lease | 453 MW undelivered, phases in 2026 and 2028 | ev_20191 |
| Other leases | 354 MW undelivered, 2026 to 2028 | ev_20192 |
| Data center service provider (unnamed) | Up to 78 MW; CoreWeave lends to the provider | ev_20195 |
| Core Scientific | ~500 MW hosting (Oct 2024); merger terminated 2025-10-30 | ev_20188, ev_20187 |
| Which facility funds which contract | DDTL 3.0: OpenAI "Phoenix 1". DDTL 4.0: one "leading AI enterprise". DDTL 5.0: two non-investment-grade customers. DDTL 5.5: five MSAs with names redacted | ev_20207, ev_20208, ev_20172, ev_20178, ev_20163 |

No filing ties the NVIDIA backstop to a particular site or facility. NVIDIA is not named in the DDTL 3.0, 4.0, 5.0 or 5.5 credit agreements as a customer, MSA party or "Qualified Customer". NVIDIA appears in DDTL 3.0 only as a source of GPU serial-number documents (ev_20210).

## G. Depth-2 parties

| Party | Role | Evidence |
|---|---|---|
| Blackstone, Magnetar | Led DDTL 2.0; lenders on DDTL 1.0. Magnetar also holds the $195m loan | ev_20147, ev_20061 |
| MUFG | Agent on DDTL 3.0 and 4.0; lead on DDTL 5.0 and 5.5 | ev_20205, ev_20077, ev_20154 |
| Morgan Stanley | Agent on DDTL 5.0; lead on DDTL 4.0 | ev_20082, ev_20168 |
| JPMorgan | Agent on DDTL 5.5 | ev_20084 |
| U.S. Bank Trust | Collateral agent | ev_20205 |
| Citigroup, Credit Agricole, Deutsche Bank, Goldman Sachs, PNC, Société Générale, SMBC, TD, Wells Fargo | DDTL 5.5 bookrunners | ev_20161 |
| OpenAI | Its contract backs DDTL 3.0 | ev_20207 |
| Meta, Microsoft | Offtakers | ev_20103, ev_20125 |
| Core Scientific | Hosting provider | ev_20188 |
| Dell | Server supplier | ev_20210 |

## H. Credit signals

| Signal | Detail | Evidence |
|---|---|---|
| Ratings | Facility ratings only: DDTL 4.0 A3 / A (low); DDTL 5.0 and 5.5 Ba2 / BB+. No corporate rating found in filings | ev_20169, ev_20177, ev_20155 |
| Covenant relief | DDTL 3.0 amended 2025-12-31 because of delivery delays: minimum liquidity cut, DSCR testing postponed, unlimited equity cures | ev_20201-ev_20204, ev_20206 |
| Covenant compliance | In compliance at 2026-09-30 | ev_20074 |
| Going concern | None. Management says liquidity covers one year | ev_20119 |
| Material weaknesses | Unremediated at 2025-12-31; disclosure controls not effective at 2026-09-30 | ev_20132, ev_20148 |
| Cross-default | DDTL 5.5 cross-defaults to indebtedness above $35m and has events of default tied to material contracts | ev_20160, ev_20151, ev_20152 |
| Litigation | Securities class action filed 2026-01-12 | ev_20198 |
| Cancellable contracts | $1.9bn of deferred revenue reclassified | ev_20118 |

Rubric read (internal, analysis):
- Debt due in 24 months ÷ liquidity is about 1.78: Weak.
- Liquidity cover is about 3.6 months on gross capex: Weak.
- Top customer share is 30%: Adequate.
- Public rating: only facility ratings, BB range for DDTL 5.x.

Weakest column: Weak. The 24-month figure mixes self-amortizing SPV debt with bullet maturities.

Wrong-way risk on the backstop: specific. NVIDIA's obligation grows as CoreWeave fails to sell capacity. The 90-day insolvency termination right limits it.

## Which document supersedes which

- **NVIDIA stake.**
  1. 424B4 holding table (2025-03): 17.9m shares.
  2. Superseded by the 13G (2025-05-15): 24.2m shares, 7.0%.
  3. Superseded by the 8-K and 13G/A (2026-01-26): 47.2m shares, 11.5%.
  4. Restated by the DEF 14A (2026-04-22): 10.66%, the latest percentage.
- **MSA payments.** The 424B4 cumulative $320m is extended by the DEF 14A figures ($326.3m FY2025, $59.6m Q1 2026).
- **Debt.**
  - The 10-K FY2025 debt note is superseded by the Q3 2026 10-Q table.
  - The DDTL 3.0 credit agreement (2025-07-28) is amended by its First Amendment (2025-12-31).
  - DDTL 2.1 amends DDTL 2.0.
  - The revolver was amended in Nov 2025. The amendment itself was not read.
  - The newest credit agreement read is DDTL 5.5 (2026-08-07).
  - The newest indenture is the 2033 convertible notes (2026-09-17). Only its 8-K summary was read.
- **Customers.** Meta $14.2bn (10-K) is superseded by Meta $21.0bn (Q3 2026 10-Q). Concentration moves from Microsoft 62% (2024) to 67% (2025) to unnamed customers at 30% and 24% (Q3 2026).
- **RPO and backlog.** RPO of $15.1bn (2024), then $60.7bn (2025), then $132.3bn (2026-09-30). The $104.2B revenue backlog (Q2 2026, non-GAAP) predates the 10-Q.
- **Power.** Contracted power of 2.2 GW (Jun 2025), then 3.1 GW (Dec 2025), then 3.7 GW (Jun 2026), then 4.2 GW (Aug 2026).
- **Prospectuses.** The 424B5 (2026-09-17) is an at-the-market program that does not mention NVIDIA. The 424B4 (IPO) is the last prospectus with an NVIDIA holding table.

## Not found

- NVIDIA's pre-IPO purchase price or round. NVIDIA is not in the Series B or Series C tables in the 424B4.
- An NVIDIA IPO purchase stated by CoreWeave.
- Whether the $6.3bn is in RPO.
- NVIDIA's share of revenue and any receivable due from NVIDIA.
- Any NVIDIA financing or allocation terms.
- The text of the 2025-09-09 order form. Only the MSA was filed (Ex. 10.31 to the S-4/A); no order form exhibit was found.
- A corporate credit rating.
- Revolver lenders.
- Site names beyond Kenilworth. Galaxy and Applied Digital do not appear in the CoreWeave filings read.
- UCC searches (not run).
- The full 2033 convertible notes indenture, the DDTL 1.0 and 2.0 credit agreements, and the Q1 and Q2 2026 10-Qs (read only through full-text hits).

## Unconfirmed

- The NVIDIA IPO purchase of 6.25m shares (about $250m) is inferred from 13G arithmetic. No CoreWeave or NVIDIA document states it.

## Needs quote

None.

## Domains to add

coreweave.com (investors.coreweave.com), for CoreWeave press releases not filed as 8-K exhibits. Optional: every release used here was an 8-K Ex. 99.1.

## Open questions

1. Which customer is the "leading AI enterprise" behind DDTL 4.0, and are the 30% and 24% Q3 customers Meta and OpenAI?
2. Is the NVIDIA $6.3bn order "initial value" a ceiling, a minimum, or an estimate subject to resale? Does CoreWeave count it in RPO? Ask for the order form exhibit.
3. Has NVIDIA bought any unsold capacity to date? FY2025 payments of $326.3m are not split between the backstop order and other order forms.
4. Did the framework "leverage NVIDIA's financial strength" produce any guarantee, lease support or financing after January 2026? None was found in the Q3 2026 10-Q.
