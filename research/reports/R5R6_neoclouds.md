# R5/R6 · Neoclouds other than CoreWeave: NVIDIA relationships, debt and project basis

Namespace `neo` (ev_40001 to ev_40155). Prepared 23 November 2026. Sources are SEC filings only (tier 1). Where a figure says "analysis", it is my inference, not a sourced fact. All amounts are USD.

## 1. Triage: every company checked

| Company | CIK | Relationship with NVIDIA beyond buying chips? | Type | Key evidence |
|---|---|---|---|---|
| Nscale plc | 0002110365 | **Yes** | EQ (preferred stock, warrants, convertible loan notes), GU (lease guarantee), LB (NVIDIA buys capacity) | ev_40001, ev_40003, ev_40009, ev_40011 |
| Nebius Group N.V. | 0001513845 | **Yes** | EQ ($2bn pre-funded warrant plus shares; 13G 9.3%) | ev_40051, ev_40055 |
| SB Energy, Inc. | 0002133037 | **Yes** | RV ($105bn-capped residual value guaranty for OpenAI's leases), EQ ($3.0bn Class N stock) | ev_40089, ev_40090, ev_40086 |
| IREN Limited | 0001878848 | **Yes** | LB ($3.4bn NVIDIA cloud contract), EQ option (30m Investment Rights at $70) | ev_40109, ev_40111 |
| SharonAI Holdings Inc. | 0002068385 | **Yes** | BK/LB (NVIDIA Master Cloud Services Agreement, up to $4.88bn, backstop-style) | ev_40144, ev_40148 |
| Applied Digital Corp. | 0001144879 | Yes, in the past (exited) | EQ (2024 private placement, 7.7m shares; exited per 13F) | ev_40136, ev_40137 |
| Bitdeer Technologies | 0001899123 | No: supplier only (Master Agreement for purchases) | supplier | ev_40139, ev_40140 |
| Bit Digital / WhiteFiber | 0001710350 / 0002042022 | No: NVIDIA Preferred Partner co-marketing only | supplier | ev_40141 |
| QumulusAI, Inc. | 0002084026 | No: buys GPUs through OEMs | supplier | ev_40142 |
| ChronoScale Holdings | 0001549084 | No: supplier only | supplier | ev_40154 |
| Cipher Digital (Cipher Mining) | 0001819989 | Not found (NVIDIA not mentioned in 10-K FY25 or 10-Q Q3 26) | n/a | n/a |
| TeraWulf | 0001083301 | Not found (10-K FY25, 10-Q Q3 26) | n/a | n/a |
| Core Scientific | 0001839341 | Not found (10-K FY25, 10-Q Q3 26) | n/a | n/a |
| Galaxy Digital | 0001859392 | Not found (10-K FY25, 10-Q Q3 26) | n/a | n/a |
| Hut 8 | 0001964789 | Not found (3 product mentions in 10-K FY25) | n/a | n/a |
| DigitalOcean | 0001582961 | Not found (product mention only) | n/a | n/a |
| Exascale Labs (D. Boral ARC; names Voltage Park as a competitor) | 0002109869 | Not found | n/a | n/a |
| CleanSpark | 0000827876 | No: NVIDIA appears only as a "Pre-Approved Tenant" in a 2026 indenture | CX | not recorded |
| HIVE Digital | 0001720424 | No: $350m contract with an unnamed investment-grade customer using NVIDIA GPUs | n/a | not recorded |
| Lambda (Lambda, Inc. / Lambda Labs) | no SEC filings found | Unknown | needs tier 2 | n/a |
| Crusoe | no SEC filings found | Unknown | needs tier 2 | n/a |
| Firmus, Fluidstack, Together AI, Vultr, Voltage Park | no SEC filings found | Unknown | needs tier 2 | n/a |

From the 13F summary (`research/evidence/nvda_13f.txt`), the only infrastructure names besides CoreWeave are Nebius (1,190,476 shares since Q4 2024) and Applied Digital (7,716,050 shares from Q3 2024; exited by 31 December 2025).

---

## 2. Nscale plc (CIK 0002110365, UK, IPO pending)

Documents: S-1/A filed 12 November 2026 (0001193125-26-458722). This is the newest and fullest document; no 424B4 had been filed as of 23 November. It supersedes the S-1 (18 September 2026) and the DRS drafts.

**NVIDIA relationship as the company describes it.** The company calls NVIDIA "a minority shareholder and ... the primary manufacturer of the GPUs" (ev_40015). It also says "NVIDIA became a holder of greater than 5% of our outstanding share capital" (ev_40014), and that NVIDIA "agreed to guarantee up to $860,340,000 of our obligations" (ev_40003). The prospectus states that NVIDIA "is not obligated under any agreement to give us priority allocation, favorable pricing or early access".

### A. NVIDIA as shareholder
| Instrument | Amount | Terms | Evidence |
|---|---|---|---|
| Series B Non-Default warrants | 9,476,700 Series B preferred shares; aggregate value $60.0m | Exercise price $0.000167 (financial statement note) or $0.01 (related party section); exercisable from 1 August 2026. Consideration for the lease guarantee. | ev_40005, ev_40006 (S-1/A, 2026-11-12) |
| Series B Default warrants (A/B/C) | Fair value $11.3m at issue | Exercisable only on a "Relevant Default Event" under the guaranteed lease. Survive the IPO and settle in Non-Voting Shares. | ev_40007 |
| Pre-Series C SAFE, converted | $300.0m into 16,346,160 Series C-3 preferred shares | Converted at Series C Completion (March 2026) at the SAFE Conversion Price of $18.35 | ev_40008 |
| Series C-4 preferred | 23,410,920 shares for $477,399,382.46 | $20.39 per share, March 2026 | ev_40009, ev_40010 |
| Convertible Loan Notes | $1.0bn subscribed by NVIDIA (15 September 2026) | Unsecured; convert automatically into Non-Voting Shares at the IPO | ev_40011 |
| "NVIDIA Sale" | Further $1.0bn of CLNs or Non-Voting Shares | Closing "on or around November 16, 2026"; post-closing status not confirmed | ev_40012 |
| Total CLN programme | $3.36bn (incl. NVIDIA Sale) | | ev_40013 |
| Percent of class | Not stated. NVIDIA holds non-voting shares and is absent from the principal shareholder table (blank). | | n/a |

Analysis: NVIDIA's cash invested is $300m + $477.4m + $1.0bn + $1.0bn (NVIDIA Sale, if closed) = about $2.78bn. The warrants were received for the guarantee, not for cash.

### B. NVIDIA as customer
| Item | Detail | Evidence |
|---|---|---|
| Agreement | NVIDIA master cloud services agreement (NVIDIA MSA), July 2025: "reserved GPU cluster capacity" in Iceland, the UK and Norway | ev_40002 |
| Value | Aggregate $1.2bn | ev_40001 |
| Term | Initial service terms of 12 to 48 months | ev_40002 |
| Revenue share or backlog treatment | Not disclosed. The largest customer (52% of H1 2026 revenue, 73% of FY2025 revenue) is not named. | ev_40025, ev_40026 |
| Leaseback of NVIDIA's own GPUs | Not stated | n/a |

### C. NVIDIA credit support
| Item | Detail | Evidence |
|---|---|---|
| Guarantee of Lease Agreement (14 October 2025) | NVIDIA guarantees Nscale's payment obligations under a net lease of a facility in Ward County, Texas, for the first five years. Maximum $860,340,000 (stated as $860.3m in the note). | ev_40003, ev_40046 |
| Recourse to NVIDIA | $470.0m escrow held as restricted cash, plus an Indemnity and Undertaking Agreement from Nscale to NVIDIA | ev_40004 |
| Compensation to NVIDIA | Non-Default warrants ($60m) plus Default warrants ($11.3m fair value) | ev_40006, ev_40007 |
| Wrong-way risk (analysis) | Specific: NVIDIA pays only if Nscale defaults on the lease, and the Default warrants add equity at that point. Net contingent exposure, after the escrow, is about $390m (analysis: $860.3m - $470.0m). | n/a |

### D. NVIDIA as supplier
GPUs are bought through third-party OEMs. In H1 2026 three suppliers accounted for 53%, 37% and 10% of related purchases (ev_40016). Technology equipment purchase commitments were $24.0bn at 30 June 2026 (ev_40017). Some customers require NVIDIA GPUs by contract.

### E. Debt stack (newest instruments; S-1/A 2026-11-12)
| Facility | Date | Committed | Rate | Maturity | Collateral | Lenders | Evidence |
|---|---|---|---|---|---|---|---|
| Ward County GPU Facility (DDTL) | Aug 2026 | $1.85bn ($630m fixed + $1.22bn floating) | SOFR+2.375% | Feb 2033 | project SPV; rated investment grade | JPMorgan, Goldman Sachs; U.S. Bank Trust (agent) | ev_40035, ev_40036, ev_40050 |
| North Carolina GPU Facility (DDTL) | Aug 2026 | $1.2bn | SOFR+2.375% | Dec 2031 | project SPV; rated investment grade | Goldman Sachs, JPMorgan; U.S. Bank Trust | ev_40034 |
| GPU Financing Facility | Feb 2026 | $1.4bn | SOFR+5.00% (+0.25% step-up) | per agreement | substantially all borrower assets | Goldman Sachs affiliate, ABN AMRO affiliate; GLAS (agent) | ev_40041 |
| Revolving Credit Facility | May 2026 | $900m (upsized from $770m) | SOFR+1.75% | 3 yrs + 2×1 yr | GLAS collateral agent | JPMorgan (agent), GS, MS MUFG, RBC, BofA, DB, CA, Mizuho, SMBC, TD, KeyBanc | ev_40047 |
| Dell Financial Services equipment leases | Apr 2026 schedules | $2.54bn initial-term rent | ~$34.8m charges | 3 to 4 month initial terms from Aug/Sep 2026 (**inside 24 months**) | equipment; Nscale Global Holdings guaranty | DFS | ev_40040 |
| Kvandal South DC term loan / VAT facility | Jul 2026 | $725m / $65m | SOFR+3.00-3.75% / +2.00% | 6 yrs after completion / long-stop | project | DNB (agent), ABN AMRO, Nordea, Export Finance Norway, SEB | ev_40038, ev_40039 |
| Macquarie Iceland Facility | Jul 2026 | $331.9m | SOFR+5.50% + MOIC | 46 months | GPU assets | Macquarie | ev_40037 |
| Macquarie Senior Facility (Glomfjord) | Jun 2025 | $105m (fully drawn) | n/a | n/a | GPU equipment | Macquarie | ev_40042 |
| Series A Convertible Notes | Nov 2024 | $160m | 12% PIK | Nov 2029 | secured subordinated | n/a | ev_40043 |

Drawn amounts per facility are not disclosed. Total debt was $137.4m at 30 June 2026 (ev_40023) and an estimated $5,516.3m at 30 September 2026 (ev_40022).

### F. Liquidity and concentration
| Item | Value | Evidence |
|---|---|---|
| Cash, 30 June 2026 | $1.5bn | ev_40020 |
| Cash, 30 September 2026 (preliminary estimate) | $3,575.9m | ev_40021 |
| Customer prepayments received H1 2026 | $2.3bn | ev_40033 |
| Data center build commitments | $3.5bn | ev_40018 |
| Leases not yet commenced | $1.4bn | ev_40019 |
| RPO, 30 June 2026 | $56.4bn | ev_40024 |
| Top customer share | 52% (H1 2026), 73% (FY2025) | ev_40025, ev_40026 |
| Microsoft SOWs | "up to approximately" $43.8bn through Dec 2033; one $3.22bn SOW terminated | ev_40027, ev_40028 |
| Anthropic GPU Services Agreements (25 Aug 2026) | "up to approximately" $44.6bn | ev_40029 |

### G. Project basis
| Site | Capacity / GPUs | Anchor | Financing | NVIDIA link | Evidence |
|---|---|---|---|---|---|
| Ward County, Texas (leased) | n/a | n/a | Ward County GPU Facility $1.85bn; DFS | NVIDIA lease guarantee (GU) | ev_40003, ev_40035 |
| North Carolina | n/a | n/a | NC GPU Facility $1.2bn; DFS | n/a | ev_40034 |
| Monarch Compute Campus, Mason County, WV (owned) | Vera Rubin NVL72 | Anthropic | None committed. Capex: DC $10-10.5bn, GPUs $21-22bn | none | ev_40031, ev_40032, ev_40030 |
| Kvandal South, Norway | n/a | n/a | $790m DC facility | n/a | ev_40038 |
| Iceland | n/a | NVIDIA MSA capacity (Iceland, UK, Norway) | Macquarie Iceland $331.9m | LB | ev_40037, ev_40001 |
| Glomfjord, Norway | n/a | n/a | Macquarie $105m | possibly NVIDIA MSA (Norway) | ev_40042 |
| Portfolio | ~1.37 GW active and contracted | | | | ev_40044 |

### H. Depth-2 parties
Microsoft and Anthropic (offtakers); Aker ASA (shareholder and JV partner); Sandton Capital (shareholder, former lender); Macquarie; JPMorgan, Goldman Sachs and U.S. Bank Trust; Dell Financial Services; DNB, ABN AMRO, Nordea, SEB and Export Finance Norway; the Ward County landlord (not named).

### I. Credit signals
- Going concern: the company says substantial doubt was "initially raised" and later alleviated (ev_40045). It must obtain additional financing for 2027 obligations (ev_40049).
- Material weaknesses in internal control (ev_40048).
- Project facilities are rated investment grade; the agency is not named (ev_40050).

---

## 3. Nebius Group N.V. (CIK 0001513845, NBIS, Netherlands)

Documents: 6-K for Q3 2026 filed 12 November 2026 (Ex. 99.1 operating review, Ex. 99.2 financial statements); 20-F FY2025 filed 30 April 2026; NVIDIA's Schedule 13G filed 20 July 2026; 6-K press release of 11 March 2026. No 424B in 2026: the 2026 convertible notes were sold under Rule 144A. The newest 424B5 is dated 12 November 2025 (not read; superseded by the Q3 2026 debt note).

**NVIDIA relationship as the company describes it.** "NVIDIA will invest $2 billion in Nebius" (ev_40060). The 20-F says "We currently rely on Nvidia for the GPU chips we use" (ev_40061). The transaction is "part of a broader strategic collaboration". No NVIDIA capacity purchase, backstop or guarantee was found.

### A. NVIDIA as shareholder
| Instrument | Amount | Terms | Evidence |
|---|---|---|---|
| Pre-funded warrant (11 March 2026 securities purchase agreement) | 21,065,936 Class A shares; gross proceeds $2,000m | Exercise price $0.0001. Lock-up until 11 September 2026. Exercise is limited by the HSR threshold. | ev_40053, ev_40055, ev_40056, ev_40059, ev_40054 |
| Class A shares (earlier holding) | 1,190,476 shares | Reported on 13F | ev_40051 (in total) |
| Total beneficial ownership | 22,256,412 Class A shares, 9.3% of class (event date 13 July 2026) | Schedule 13G | ev_40051, ev_40052 |
| Discrepancy | 20-F subsequent-events note says 21,065,396 shares | Likely a typo; Q3 note and 13G say 21,065,936 | ev_40058 |

B (NVIDIA as customer): not found. C (credit support): not found. D (supplier): NVIDIA is the sole GPU supplier (ev_40061). The partnership "Enables Nebius to Deploy More Than 5 Gigawatts of NVIDIA Systems" by end of 2030 (ev_40085); this is a headline, not a commitment.

### E. Debt stack (Q3 2026 note 12, 30 September 2026)
| Facility | Principal | Rate | Maturity | Collateral / covenants | Evidence |
|---|---|---|---|---|---|
| Convertible notes due Jun 2029 | $105.0m | 2.00% | Jun 2029 | unsecured | ev_40066 |
| Convertible notes due Feb 2030 | $3,795.0m | 0.50% | Feb 2030 | unsecured (August 2026 144A) | ev_40067 |
| Convertible notes due Sep 2030 | $1,818.4m | 1.00% | Sep 2030 | unsecured | ev_40071 |
| Convertible notes due Mar 2031 | $3,105.0m | 1.25% | Mar 2031 | unsecured | ev_40069 |
| Convertible notes due Mar 2033 | $2,100.0m | 2.63% | Mar 2033 | unsecured | ev_40070 |
| Convertible notes due Feb 2034 | $2,875.0m | 4.50% | Feb 2034 | unsecured | ev_40068 |
| Term Loan Facility (10 July 2026; MUFG agent) | $773.3m committed, $751.8m outstanding | SOFR+2.50% | 31 Oct 2030 | substantially all borrower assets; DSCR ≥1.15x and minimum liquidity | ev_40063, ev_40064, ev_40065 |
| **Total principal** | **$16,478.0m** | | | | ev_40062 |
| Citi Facility (22 Oct 2026, subsequent event) | $3.5bn | SOFR+2.75% rising to 3.50% | **364 days (inside 24 months)** | senior secured | ev_40072, ev_40073 |

### F. Liquidity and concentration
| Item | Value | Evidence |
|---|---|---|
| Cash, 30 September 2026 | $7,425.6m | ev_40074 |
| RPO, 30 September 2026 | $38.7bn (40% within 24 months) | ev_40075 |
| Customers, 9M 2026 | C 20%, D 21%, E 21%; top three 62% (analysis) | ev_40076, ev_40077 |
| Customers, Q3 2026 | E 33%, D 22%, C 15% | ev_40076, ev_40077 |
| Receivables concentration | D 75%, E 10% | ev_40078 |
| Fixed energy and co-location commitments | $287.1m in 2027 | ev_40083 |
| Microsoft (Sept 2025, Vineland NJ, 5 years) | "estimated to be up to about" $17.4bn | ev_40084 |
| Meta (13 March 2026) | up to ~$27bn: $12bn dedicated orders plus up to $15bn purchase of unsold capacity (Meta acts as backstop) | ev_40079, ev_40080, ev_40081 |
| Meta (1 Nov 2025) | ~$2.9bn, 5 years | ev_40082 |

G (project basis): Vineland, NJ (Microsoft); Vera Rubin clusters for Meta from 2027. No site-level debt; the Term Loan is the only secured facility. H (depth-2): Microsoft, Meta, MUFG, Citi, 144A noteholders. I (credit signals): no ratings, going-concern language or waivers found in the documents read.

---

## 4. SB Energy, Inc. (CIK 0002133037, US, IPO pending; SoftBank-controlled)

Documents: S-1/A Amendment No. 3 filed 19 November 2026 (supersedes the S-1 of 1 September and the amendments of 21 September). No 424B4 yet.

**NVIDIA relationship as the company describes it.** "NVIDIA is a strategic investor and residual value guarantor at the PORTS-Pike Technology Campus". The company says "We and OpenAI are highly dependent on NVIDIA for the successful completion" of that campus (ev_40097). The guaranty "is not a guaranty of rent or other payment obligations".

### A. NVIDIA as shareholder
| Instrument | Amount | Status | Evidence |
|---|---|---|---|
| Prepaid Forward Contract (17 August 2026; Class N non-voting stock at 90% of IPO price) | $1.5bn | **Funded** 17 August 2026 | ev_40087 |
| Concurrent Private Placement (Class N at IPO price) | $1.5bn | Committed, contingent on the IPO | ev_40088 |
| Total | $3.0bn | Percent of class blank in the S-1/A | ev_40086 |

### C. NVIDIA credit support: residual value guaranty (type RV)
| Item | Detail | Evidence |
|---|---|---|
| Covered | OpenAI affiliate's obligations under the leases for the first nine buildings, about 4.25 GW-IT of the 8.0 GW-IT campus | ev_40089, ev_40098 |
| Cap | Aggregate remedy cap of $105bn across the related guaranties | ev_40090 |
| Trigger | "triggered only upon tenant insolvency or an uncured monetary default" | ev_40091 |
| Value | The guaranteed minimum value declines over the 20-year leases. It covers debt principal, interest, invested equity, targeted equity returns and AEP Ohio transmission payments. | ev_40093 |
| NVIDIA remedies | NVIDIA may assume the tenancy itself or through an assignee, or direct a re-let or sale | ev_40096 |
| Option | NVIDIA may, at its sole discretion, guarantee the remaining ~3.78 GW-IT. If it does not, OpenAI must find a replacement guarantor rated A- or better. | ev_40092 |
| Compensation | Paid by OpenAI under a separate agreement; amount not disclosed | ev_40094 |
| Release | On an OpenAI credit-rating upgrade or a replacement guaranty | ev_40095 |
| Wrong-way risk (analysis) | Specific: the guaranty pays when OpenAI fails | n/a |

B (NVIDIA as customer) and D (as supplier) are not applicable: OpenAI is the tenant, and OpenAI depends on NVIDIA GPU deliveries.

### E/F. Debt and liquidity (30 September 2026)
| Item | Value | Evidence |
|---|---|---|
| Project-level debt, non-recourse | ~$4.6bn, of which ~$1.2bn current | ev_40100, ev_40101 |
| Intercompany notes from SBE Global (to be repaid at IPO) | $709.5m | ev_40102 |
| New Credit Facility at IPO (Citibank agent): $1.875bn RCF + $1.125bn LC facility | $3.0bn, 3.5 years; minimum liquidity covenant; no dividends before 2029 | ev_40105 |
| Unrestricted cash | $996.7m | ev_40103 |
| Undrawn committed capacity | $1.9bn | ev_40104 |
| Consolidated backlog | ~$439bn (~$2bn within 24 months) | ev_40106 |

G (project basis): PORTS-Pike Technology Campus (Ohio): 17 leases signed 17 August 2026 with an OpenAI affiliate, about 8.0 GW-IT, 20-year terms, commencement in stages 2028 to 2032 (ev_40098, ev_40099). Other campuses: Milam County (OpenAI) and Cosmos (SoftBank); site financing not extracted. H (depth-2): SoftBank, OpenAI (which also holds warrants), AEP Ohio, Citibank. I (credit signals): material weakness (ev_40107).

---

## 5. IREN Limited (CIK 0001878848, IREN, Australia)

Documents: 10-Q for Q1 FY27 filed 5 November 2026; 10-K FY2026 filed 27 August 2026; 8-K of 26 May 2026. A 424B7 of 4 August 2026 mentions NVIDIA but was not read (resale prospectus).

**NVIDIA relationship as the company describes it.** "five-year cloud services contract with NVIDIA to support its internal AI and research workloads" (ev_40108). "NVIDIA is a customer of the Group" (ev_40110). The company "granted NVIDIA the right to invest up to $2.1 billion in Ordinary shares, subject to delivery of up to 600,000 GPUs" (ev_40113, ev_40114).

| Area | Detail | Evidence |
|---|---|---|
| B. NVIDIA as customer (LB) | May 2026, five years, TCV ~$3.4bn | ev_40108, ev_40109 |
| A. Investment Rights (EQ option) | Up to 30,000,000 shares at $70.00, granted 7 May 2026, expiring 7 May 2031. Vest by volume of GPUs NVIDIA supplies. Headline "up to $2.1 billion". Grant-date fair value $793.4m, capitalised into GPU cost. | ev_40111, ev_40112, ev_40113, ev_40115, ev_40116 |
| D. Supplier | GPUs bought from NVIDIA directly. Dell purchase of ~$1.6bn for Childress, to service a "$3.4 billion managed services AI cloud contract" (analysis: the same value as the NVIDIA contract). Capital commitments $18,947m. | ev_40116, ev_40121, ev_40123 |
| Partnership headline | Up to 5GW of NVIDIA DSX-aligned infrastructure | ev_40117 |
| E. GPU Financing 1.0 (Microsoft, May 2026) | ~$3.6bn (DDTL $1.5bn at SOFR+2.25% + $2.1bn USPP notes). Funded: DDTL $413m, USPP $1,575m. Undrawn: $1,132m and $525m. Non-recourse; matures 31 Dec 2031. CSC Delaware Trust is collateral agent. | ev_40131, ev_40129, ev_40130 |
| E. GPU Financing 2.0 (Aug 2026) | Up to $2.4bn, 9.0% fixed, 30-month amortisation, parent-guaranteed, equipment pledged. $947m funded, $1,500m available. | ev_40126, ev_40127 |
| E. GPU Financing 3.0 (Aug 2026) | $363m, 9.51%, 36 months | ev_40128 |
| E. Totals | Total principal $10,041m; current $950m; due rest of FY27 $723m and FY28 $1,059m. Dec 2033 convertible notes $3,000m. These table figures are in "USD millions", a header the tool does not parse, so no value was attached. | ev_40132, ev_40133, ev_40134, ev_40135 |
| F. Liquidity | Cash $3,522m (30 September 2026) | ev_40122 |
| F. Concentration | 28% / 24% / 18% of revenue (top three 70%). Microsoft and NVIDIA contracts are a "substantial majority of our contracted revenue". RPO $6,347m. | ev_40125, ev_40119, ev_40124 |
| F. Contracts | Microsoft ~$9.7bn (Nov 2025, Horizon 1-4); Prometheus, Perplexity and Together AI ~$2.8bn (Jul 2026) | ev_40118, ev_40120 |
| G. Sites | Childress, Texas (Microsoft Horizon 1-4; Dell GPUs for the $3.4bn contract); British Columbia transitioning to AI cloud | ev_40118, ev_40121 |

---

## 6. SharonAI Holdings Inc. (CIK 0002068385, SHAZ)

Documents: 10-Q filed 16 November 2026; 8-K of 12 June 2026; 8-K of 1 October 2026 (Facility Agreement).

**NVIDIA relationship as the company describes it.** The 8-K describes a "Master Cloud Services Agreement and Order Form 1 dated June 8, 2026" that "has a contract value of up to $4.88 billion" (ev_40143, ev_40144). The 10-Q says the arrangement "does not specify a fixed aggregate contractual value" (ev_40146). The arrangement "includes minimum revenue provisions" (ev_40145). The significant customer "will have little to no access to or use of the services" unless capacity goes unsold to third parties (ev_40148), and SharonAI must "comply with all notice obligations to NVIDIA in respect of sold services" (ev_40149).

Classification (analysis): this works as a capacity backstop (BK) with a revenue share. NVIDIA pays a minimum and SharonAI resells the capacity to third parties.

| Area | Detail | Evidence |
|---|---|---|
| D. Hardware commitment tied to the NVIDIA contract | ~$4bn | ev_40155, ev_40147 |
| E. SPV facility (28 Sept 2026) | $356m ($150m A + $206m B), 7.25% rising to 9.95% (A) and 9.95% fixed (B), 42-month bullet. Secured by all obligor assets; limited parent guarantee; GLAS agent. Supports the Global Technology Customer contract, not the NVIDIA contract. | ev_40152 |
| F. Cash, 30 September 2026 | ~$1.34bn | ev_40150 |
| F. Other contract | New Zealand, ~$1.32bn, 5 years | ev_40151 |
| I. Credit signals | Material weakness (ev_40153); a going-concern assessment is discussed and the company concluded it is a going concern | ev_40153 |

---

## 7. Applied Digital Corp. (CIK 0001144879, APLD): historical shareholder only

NVIDIA joined a $160m private placement in September 2024 (ev_40138) at $3.24 per share (ev_40137). It held 7,716,050 shares, registered for resale (ev_40136). Cost was about $25.0m (analysis). The 13F summary shows the stake exited by 31 December 2025. The latest 10-K (FY ended May 2026) and 10-Q (August 2026) do not mention NVIDIA. No current exposure, so no credit work was done.

## 8. Supplier-only names (one line each)
- Bitdeer: master purchase agreement with NVIDIA (2023 exhibit); NVIDIA server orders ~$56.0m (ev_40139, ev_40140). A separate credit backstop for Bitdeer's Tydal (Norway) lease to Volta comes from J.P. Morgan letters of credit, not NVIDIA (6-K, 5 August 2026; not recorded).
- WhiteFiber / Bit Digital: NVIDIA Preferred Partner co-marketing agreement (ev_40141).
- QumulusAI: GPUs bought through OEMs (ev_40142).
- ChronoScale: relies on NVIDIA as GPU supplier (ev_40154).

---

## Not found
- Nscale: amounts drawn per facility; NVIDIA's percentage of shares outstanding (non-voting, left blank); revenue recognised from the NVIDIA MSA; the Ward County landlord's name and the lease's MW and rent; final status of the "NVIDIA Sale" (due around 16 November). Searched the S-1/A; next check is the 424B4 when it is filed.
- Nebius: any NVIDIA capacity purchase, backstop or guarantee (none in the 20-F, Q3 6-K or the March 2026 press release); 20-F risk sections for material weakness (not searched).
- SB Energy: NVIDIA percentage after the IPO (blank); OpenAI's compensation to NVIDIA for the guaranty; site-level debt for PORTS-Pike.
- IREN: exhibit text of the NVIDIA cloud services agreement and the securities purchase agreement (not located in 8-Ks; look in the 10-K exhibit index); whether NVIDIA is Customer A, B or C.
- SharonAI: the customer-concentration table (not extracted).
- Cipher, TeraWulf, Core Scientific, Galaxy, Hut 8, DigitalOcean: NVIDIA does not appear in their latest 10-K or 10-Q except as a product name.

## Unconfirmed (no allowed source in hand)
- Lambda leasing NVIDIA GPUs back to NVIDIA, or NVIDIA renting capacity from Lambda: no SEC registrant found.
- Crusoe, Fluidstack, Firmus, Together AI, Vultr and Voltage Park: any NVIDIA equity or offtake. Not in SEC filings.

## Not found in SEC filings: needs tier 2 news
| Company | Search for |
|---|---|
| Lambda | NVIDIA equity rounds; NVIDIA leaseback or cloud-rental agreements (amounts, terms); IPO filing status; GPU-backed debt (lenders) |
| Crusoe | NVIDIA participation in funding rounds; Abilene/OpenAI project financing; any NVIDIA offtake |
| Fluidstack | NVIDIA involvement; Google backstops of TeraWulf and Cipher leases (context) |
| Firmus (Australia) | NVIDIA investment; Project Southgate financing |
| Together AI | NVIDIA equity; compute contracts (IREN 10-K names it as a customer) |
| Vultr | NVIDIA or AMD equity, GPU-backed loans |
| Voltage Park | NVIDIA-related financing |
| Nscale | post-IPO pricing; whether the NVIDIA Sale closed |

## Needs quote
None: no tier 2 sources were used.

## Domains to add
None required. All evidence is from sec.gov.

## Open questions
1. Nscale: is NVIDIA the unnamed largest customer (73% of FY2025 revenue)? The timing of the July 2025 NVIDIA MSA would fit, but this is unconfirmed.
2. Nscale guarantee: is the $860.3m cap net of the $470m escrow, and is the Ward County lease capacity the same as the capacity used for the NVIDIA MSA?
3. SB Energy: the $105bn guaranty is a cap on remedies, not an expected loss. The R7 measurement needs the declining guaranteed-value schedule, which is not disclosed.
4. IREN: is the $3.4bn "managed services AI cloud contract" served with the Dell GPUs the NVIDIA contract? The values match (analysis).
5. NVIDIA's own 10-Q of 20 May 2026 contains "lease guarantee" wording. It should be reconciled with the Nscale guarantee (and possibly others).
