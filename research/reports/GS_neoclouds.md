# GS · Guarantee sweep: neoclouds, their landlords and their lenders

Prepared 24 November 2026. Draft: `research/drafts/complex_neoclouds.json` (28 complex links, 30 new depth 2 entities). `python3 -m pipeline.checks draft` prints "All checks passed". Every non-null amount is display eligible (all tier 1, sec.gov).

New evidence is in namespace `gsn`, ev_230001 to ev_230080 (80 records). Reused evidence: crwv ev_20xxx, neo ev_40xxx, r2 ev_170012 to ev_170024, veh ev_100047.

Newest documents read, all third quarter 2026 filings:
- TeraWulf 10-Q (2026-11-06), Cipher 10-Q (2026-11-02), Hut 8 10-Q (2026-11-04)
- Galaxy 10-Q (2026-11-09), Core Scientific 10-Q (2026-11-05), Ionic Digital 10-Q (2026-11-12)
- IREN 10-Q (2026-11-05) and 10-K exhibits 10.37, 10.38 and 10.54 (2026-08-27)
- Applied Digital 10-Q (2026-10-07), SharonAI facility 8-K (2026-10-01)

Older 8-Ks were used only for figures the 10-Qs do not restate. "Analysis" marks my inference.

## Answer in one paragraph

Nvidia is one of several parties standing behind neocloud capacity, and not the largest.
- **Google** backstops about $13 billion of Fluidstack's lease obligations or lease value at four landlords:
  - $3.2 billion at TeraWulf
  - $1.3 billion at Abernathy
  - $1.73 billion at Cipher
  - the full 15-year, $7.0 billion River Bend lease at Hut 8

  It promised the Lake Mariner noteholders directly that it will pay. None of this capacity carries an Nvidia relationship.
- **Meta** has the same contract with Nebius that Nvidia has with CoreWeave: up to $15 billion of unsold capacity it must buy.
- **Microsoft's and OpenAI's contracts** are the collateral behind the neocloud GPU loans:
  - Microsoft's contract backs IREN's $3,645 million GPU Financing 1.0.
  - OpenAI's $11.9 billion contract backs CoreWeave's DDTL 3.0.
- **Neocloud parents** guarantee most of their own debt.
- **Landlords** give completion guarantees and, in Applied Digital's case, warrants to win CoreWeave as tenant.

The only site where Nvidia and another party both guarantee the same lease is Nscale's Ward County, Texas site:
- Nvidia covers rent in years one to five, up to $860.3 million.
- Nscale's parent covers rent from year six.
- Microsoft, the anchor customer, may step in if Nscale fails.

## 1. Every link found

How to read the amount columns:
- **Headline**: the stated size of the supported lease, contract, notes or facility.
- **Maximum**: the provider's stated cap.
- **Drawn**: the amount drawn or issued.

The three are never added together.

| # | Provider | Beneficiary | Obligor | Kind | Headline | Maximum | Drawn | Trigger | Dates | Same capacity as Nvidia | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Google | TeraWulf (Lake Mariner) | Fluidstack | backstop | n/a | about $3.2bn ($1.8bn + $1.4bn) | none paid | Fluidstack payment default or insolvency; Google pays termination fee or assumes lease | announced 2025-08-14; effective at each lease start (one started by Q3 2026) | No | ev_230010, ev_230011, ev_230012, ev_230001, ev_230002, ev_230009, ev_100047 |
| 2 | Google affiliate | Wulf Compute noteholders | Fluidstack | credit support | $3.2bn notes | not stated | n/a | Same as #1; affiliate pays termination fee to collateral agent | 2025-10-22; notes mature 2030-10-15 | No | ev_230003, ev_230005, ev_230004 |
| 3 | TeraWulf | Wulf Compute noteholders | Wulf Compute | parent (completion) guarantee | $3.2bn notes | uncapped (not stated) | n/a | Construction shortfall at Lake Mariner | 2025-10-22 | No | ev_230006, ev_230003 |
| 4 | Google | Abernathy JV (FS CS I LLC) | Fluidstack | backstop | $1.3bn JV notes | $1.3bn, amortizing over 10 years | n/a | Fluidstack default or insolvency | signed 2025-09-26; not in force before lease start | No | ev_230013, ev_230014, ev_230007, ev_230008 |
| 5 | Google | Cipher (Barber Lake) | Fluidstack | backstop | n/a | $1.73bn | n/a | Fluidstack default or insolvency | signed 2025-09-24, raised 2025-11-20; not in force before lease start | No | ev_230020, ev_230019, ev_230015, ev_230016, ev_230017, ev_230018, ev_230021 |
| 6 | Google | Hut 8 (River Bend) | Fluidstack | backstop | $7.0bn lease value (15 years) | not stated; covers rent and pass-throughs for the base term | n/a | Fluidstack fails to pay rent | announced 2025-12-17 | No | ev_230027, ev_230028, ev_230022, ev_230023, ev_230024, ev_230025, ev_230029 |
| 7 | Meta | Nebius | Nebius | backstop (buys unsold capacity) | n/a | up to $15bn | n/a | Nebius cannot sell capacity on specified clusters | signed 2026-03-13; five years from deployment | Yes (company: Nvidia equity) | ev_40081, ev_230071, ev_230072, ev_40080 |
| 8 | OpenAI | DDTL 3.0 lenders (MUFG agent) | CoreWeave SPVs | compute contract (collateral) | up to $11.9bn contract | n/a | $2,323m DDTL 3.0 outstanding | OpenAI stops paying under Phoenix 1 order form | signed 2025-03-07; contract to Oct 2030 | Yes (company: CoreWeave backstop, equity) | ev_20199, ev_20048, ev_20207, ev_20208, ev_20205, ev_20136 |
| 9 | CoreWeave, Inc. | DDTL 1.0 to 3.0 lenders (Blackstone, Magnetar, MUFG) | CoreWeave SPVs | parent guarantee (unconditional) | $15.5bn commitments (analysis: sum of four facilities) | not capped | $8,752m at 2026-09-30 (sum) | Borrower default | 10-K 2026-03-02 | Yes (company) | ev_20138, ev_20133 to ev_20136, ev_20045 to ev_20048, ev_20147 |
| 10 | CoreWeave, Inc. | DDTL 4.0 lenders (MUFG) | CoreWeave SPV | parent guarantee limited to bad acts | $8.5bn facility | limited to bad acts | $4,583m | Fraud or specified bad acts only | matures 2032-03-31 | Yes (company) | ev_20167, ev_20075, ev_20064, ev_20172, ev_20080, ev_20169 |
| 11 | CoreWeave, Inc. | Core Scientific | CW SPV | lease guarantee (remains primary obligor) | $1.8bn payments on leases not yet started | not stated | n/a | CW SPV fails to pay | assignment during 2026 | Yes (company) | ev_230036, ev_230037, ev_230038, ev_230041 |
| 12 | CoreWeave (as tenant) | Helios noteholders | Galaxy Helios II | compute contract (lease as collateral) | $10.4bn minimum lease payments | n/a | $3.5bn notes issued 2026-07-28 | CoreWeave fails to pay rent | lease April 2025; notes due 2031 | Yes (company; lender deck cites Nvidia's $6.3bn backstop) | ev_230034, ev_230030, ev_230032, ev_230033, ev_230035, ev_170016, ev_170017, ev_170018 |
| 13 | Galaxy (GDH LP) | Deutsche Bank (Credit Agreement) | Galaxy Helios | parent (completion) guarantee | not stated | not stated | n/a | Construction not completed within budget | 2026 | Yes (company, via CoreWeave tenant) | ev_230031, ev_230080, ev_230030 |
| 14 | Core Scientific | Core Scientific noteholders | Core Scientific Finance | parent (completion) guarantee, uncapped | $3.3bn notes | uncapped | n/a | Specified projects not completed | 2026-05-06 | No (tenants not named) | ev_230039, ev_230040 |
| 15 | Applied Digital | CoreWeave | Applied Digital | share option or warrant | 13,062,521 + 8,393,611 shares (no $ figure) | n/a | n/a | CoreWeave exercises | 2025-05-28 and 2025-08-28 | Yes (company) | ev_230073, ev_230074 |
| 16 | Applied Digital | APLD ComputeCo 3 noteholders | APLD ComputeCo 3 | parent (completion) guarantee | $1.59bn notes | not stated | n/a | ELN-04 not completed | 2026-06-16; due 2031-06-15 | No (tenant not named) | ev_230075, ev_230076 |
| 17 | Nscale parent | Ionic Digital | Nscale Ward County, LLC | lease guarantee, from year six | about $1.9bn total lease revenue | rent from year six (not in force yet) | n/a | Nscale fails to pay rent after year five | signed 2025-10-14; lease to 2037-01-31 | **Yes (same lease as Nvidia's guarantee)** | ev_230048, ev_230050, ev_230051, ev_230055, ev_230056, ev_230049, ev_170012, ev_170021, ev_230057 |
| 18 | Nscale Global Holdings | Dell Financial Services | Nscale subsidiaries | parent guarantee | about $2.54bn initial-term rent | all obligations | n/a | Subsidiaries fail to pay DFS | 2026-04-18 | Yes (company) | ev_230052, ev_40040 |
| 19 | Nscale Limited (limited) and Nscale Ward County | JPMorgan, Goldman Sachs | Ward County Borrower SPV | parent guarantee, limited | $1.85bn facility | limited, not quantified | not disclosed | Borrower default | 2026-08-27; to 2033-02-27 | **Yes (same site as Nvidia's lease guarantee)** | ev_230042, ev_230043, ev_230044, ev_230054, ev_40035, ev_40036 |
| 20 | Nscale Limited (limited) and Nscale Services US | Goldman Sachs, JPMorgan | NC Borrower SPV | parent guarantee, limited | $1.2bn facility | limited | not disclosed | Borrower default | 2026-08-27; to 2031-12-27 | Yes (company) | ev_230045, ev_230046, ev_230053, ev_40034 |
| 21 | Nscale parent | Goldman Sachs, ABN AMRO affiliates | Nscale Services UK | parent guarantee | $1.4bn facility | not stated | not disclosed | Borrower default | 2026-02-11 | Yes (company) | ev_230047, ev_40041 |
| 22 | Microsoft | GPU Financing 1.0 lenders (CSC Delaware Trust agent) | IE US Hardware 3 | compute contract (collateral) | about $9.7bn contract; $3,645m financing relies on it | n/a | $413m loans + $1,575m notes funded | Microsoft terminates or stops paying | SOW 2025-11-02 | **Yes (Childress site also serves Nvidia's $3.4bn contract; Nvidia is a named replacement customer)** | ev_40118, ev_230058, ev_230059, ev_230067, ev_230070, ev_40129, ev_40130, ev_40131 |
| 23 | IREN Limited | GPU Financing 1.0 lenders | IE US Hardware 3 | residual value guarantee | $3,645m financing | shortfall after remarketing | n/a | Microsoft terminates a tranche before acceptance and remarketing fails or sells short | 2026-05-29 | Yes (company and site) | ev_230065, ev_230066, ev_230067, ev_230068, ev_230058 |
| 24 | IREN Limited | GPU Financing 1.0 lenders | IE US Hardware 3 | parent (performance) guarantee | n/a | outstanding obligations | n/a | Manager fails to perform the managed services | 2026-05-29 | Yes (company) | ev_230069 |
| 25 | IREN Limited | Blue Owl (agent) | IE Mackenzie Compute | parent guarantee | up to $2.4bn | full payment obligations | $947m | Borrower fails to pay | 2026-08-25 | Yes (company) | ev_230060, ev_230061, ev_230062, ev_40126, ev_40127 |
| 26 | IREN Limited | Dell | IE US Hardware 5 and 6 | parent guarantee (supplier) | about $6.7bn purchase orders | unconditional | n/a | Subsidiaries fail to pay Dell | 2026-09-28 | Yes (company) | ev_230063, ev_230064 |
| 27 | SharonAI | GLAS (agent) | SAI AU No. 1 and No. 3 | parent guarantee, releasable | up to $356m | released after Facility A repaid | not disclosed | Borrower default | 2026-09-28 | Yes (company only; funds a different customer contract) | ev_230077, ev_230078, ev_230079, ev_40152 |
| 28 | Two unnamed banks | Bitdeer | Volta subsidiary | credit support (letters of credit), anticipated | about $1.3bn | n/a | n/a | Volta defaults on Tydal lease | announced 2026-08-05 | No | ev_170024, ev_170023 |

**Debt that landlords raised against these leases.**
- TeraWulf (Wulf Compute): $3.2bn 7.75% notes due 2030 (ev_230003). Secured on the campus and a Fluidstack lockbox account (ev_230004).
- Abernathy JV: $1.3bn 7.25% notes due 2030 (ev_230007).
- Cipher Compute: $1.4bn plus $333.0m of 7.125% notes due 2030 (ev_230017, ev_230018).
- Hut 8 River Bend: $3.25bn of notes (ev_230024), not guaranteed by Hut 8, Fluidstack or Google (ev_230023).
- Hut 8 Beacon Point: $4.25bn (ev_230026). The tenant is an unnamed investment grade company, and there is no guarantee.
- Galaxy Helios II: $3.5bn 9.875% notes due 2031 (ev_230030).
- Core Scientific Finance: $3.3bn 7.75% notes due 2031 (ev_230040).
- APLD ComputeCo 3: $1.59bn 7.000% notes due 2031 (ev_230076).
- Ionic Digital: no borrowings at 30 September 2026 (ev_230049).

## 2. Stacked support: where Nvidia and another party stand behind the same obligation

| Company or site | Obligation | Nvidia's support | Other support | Who pays first (analysis) |
|---|---|---|---|---|
| **Nscale, Ward County, Texas (Ionic Digital lease)** | Rent under the 126-month lease, about $1.9bn total (ev_230050) | Guarantee of rent in the first five lease years, up to $860.3m (ev_230051, ev_170012, rel_nscale_gu_2025). Nvidia's recourse is a $470.0m escrow and an indemnity from Nscale (ev_40004) | Nscale parent guarantees rent from year six (ev_230048). The anchor customer may step into the lease within 30 days of an Nscale insolvency (ev_230056); Microsoft holds an option on more power at the site (ev_230057) | The two guarantees run one after the other, not side by side. In years one to five the order is: (1) Nscale Ward County pays rent; (2) Nvidia pays Ionic under its guarantee; (3) Nvidia recovers from the $470m escrow, then from Nscale's indemnity. On insolvency the anchor customer may step in instead, which would stop Nvidia's exposure from growing. From year six, Nscale's parent is the only guarantor. |
| **Nscale, Ward County GPU equipment** | $1.85bn Ward County GPU Facility (ev_40035) | Indirect: Nvidia's lease guarantee keeps the site lease in force for five years | Limited guarantees from Nscale Limited and a guarantee by Nscale Ward County, LLC (ev_230042, ev_230043). Repayment comes from one customer contract (ev_230044) | The customer contract pays first, then Nscale's limited guarantees. Nvidia does not guarantee the GPU debt, but its guarantee of the lease protects the lenders' access to the building. |
| **CoreWeave (company level, many sites)** | CoreWeave's capacity revenue that services its DDTL debt and its leases | Order to buy residual unsold capacity, $6.3bn initial value, to 13 April 2032 (ev_20001, ev_20002, rel_coreweave_bk_2025), terminable after a 90-day insolvency (ev_20006) | (a) OpenAI's contract is DDTL 3.0 collateral (#8). (b) CoreWeave guarantees DDTL 1.0 to 3.0 (#9). (c) Galaxy's noteholders rely on the CoreWeave lease and cite Nvidia's backstop (#12, ev_170016). (d) CoreWeave remains primary obligor to Core Scientific (#11). (e) Galaxy and Core Scientific completion guarantees (#13, #14) | The order is: (1) contracted customers (OpenAI, Meta, Microsoft) pay CoreWeave; (2) Nvidia buys capacity CoreWeave cannot sell, but only while CoreWeave is solvent and delivering; (3) the CoreWeave parent guarantee for DDTL 1.0 to 3.0; (4) the GPU and lease collateral. Landlords' completion guarantees cover construction only. Nvidia's support stops when it is needed most (the 90-day insolvency termination), so in a CoreWeave failure the lenders and landlords would rely on the parent and on collateral, not on Nvidia. |
| **IREN, Childress, Texas** | GPU Financing 1.0 ($3,645m) for Microsoft's Horizons 1 to 4 (ev_230058, ev_230059) | Nvidia's own $3.4bn cloud contract at IREN (rel_iren_lb_2026; site proj_iren_childress). Nvidia is one of five named "Qualified Customers" lenders would accept in Microsoft's place (ev_230070) | Microsoft contract about $9.7bn (ev_40118). IREN residual value guarantee if remarketing fails (ev_230065, ev_230066). IREN performance guarantee (ev_230069) | Nvidia does not guarantee this debt; it is a named acceptable replacement buyer. The order is: (1) Microsoft; (2) if Microsoft drops a tranche, remarketing, where Nvidia, Amazon, Meta or Alphabet would qualify as replacement customers; (3) IREN Limited pays any shortfall. |
| **SharonAI (company level)** | SharonAI's debt and capacity | Nvidia Master Cloud Services Agreement with minimum revenue, up to $4.88bn (ev_40144, rel_sharonai_bk_2026) | SharonAI's parent guarantee of the $356m facility (ev_230077) | Not the same obligation. The facility funds a different customer's contract (ev_230079), and the Nvidia capacity has no binding financing yet (ev_170019). |

Not stacked (one supporter only), but useful comparators:
- **Nebius:** Meta, not Nvidia, is the buyer of last resort for up to $15bn of capacity (ev_230071). Nvidia's link to Nebius is equity only.
- **Fluidstack:** Google is the only supporter at all four landlords. Nvidia has no recorded relationship with Fluidstack.

## 3. Parties searched with nothing found

| Party | Searched | Result |
|---|---|---|
| Lambda | Company releases (ev_110002 to ev_110009); EDGAR full text | The $926m TLB and the $1.008bn DDTL rest on "investment-grade offtakers" that are not named. No guarantor is named. |
| Crusoe | crusoe.ai releases already in register; EDGAR | Brookfield $750m and Upper90 about $225m facilities with no guarantor named. The Abilene $15bn Blue Owl joint venture is equity, not credit support. AMD's backstop of a Crusoe loan is tier 2 only (Needs quote). |
| Fluidstack (as obligor) | EDGAR "Fluidstack" with backstop, guarantee | Only the Google backstops above. No Fluidstack parent guarantee to landlords appears in landlord filings. |
| Together AI, Firmus | Company releases | No third-party guarantee or pledged contract. Firmus's US$10bn Blackstone-led facility (ev_110035) names no guarantor. |
| WhiteFiber / Bit Digital | WhiteFiber 10-Q (2026-11-10), 8-K (2026-11-10) | Only small intra-group guarantees: a $20m Landsbankinn loan and a completion guarantee by the operating partnership on a $300m NC-1 loan. R2 found the customer's obligations are guaranteed by its own unnamed affiliate. Not recorded: no named provider and under $1bn. |
| Nebius debt | Q3 2026 6-K note 12 | The Term Loan ($773.3m) and Citi facility ($3.5bn) are secured on Nebius assets. No customer contract is named as collateral and there is no third-party guarantor. |
| Core Scientific and AMD | 10-Q 2026-11-05; EDGAR "Core Scientific" "AMD" "guarant" | AMD leases about 530 MW and holds a reservation right on 1,925 MW. No AMD guarantee of the unnamed neocloud co-tenant was found. |
| Riot Platforms | 8-K 2026-08-10 | An "investment-grade credit backstop" is still being finalised for a Rockdale lease. The provider is not named. Not recorded. |
| Hut 8 Beacon Point | 10-Q | The tenant is an unnamed high investment grade company. The notes are not guaranteed by the tenant. |
| Macquarie, Apollo, Brookfield | Nscale S-1/A, Crusoe releases, EDGAR | They are lenders only (Macquarie Iceland and Glomfjord facilities, Brookfield $750m to Crusoe). No guarantor or pledged contract is named. |
| IREN GPU Financing 3.0 ($363m) | 10-Q | Parent guaranteed; the lenders are not named. Not recorded as a link because there is no beneficiary entity. |

## Not found

- **Lambda, CoreWeave DDTL 4.0 and Nscale facilities:** the customer behind each pledged contract is not named. This covers Lambda's two investment grade offtakers, CoreWeave's "leading AI enterprise" (DDTL 4.0) and the customers behind Nscale's Ward County and North Carolina facilities.
- **CoreWeave DDTL 5.0 and 5.5:** whether they carry a CoreWeave parent guarantee. Not stated in the 10-Q summary.
- **Fluidstack's end user** at River Bend, Barber Lake and Abernathy. Not named in landlord filings.
- **Which customer Abernathy's GPUs and Applied Digital's ELN-04 serve.** Not stated.

## Unconfirmed

- AMD backstops a $300m Crusoe loan. The Information only; already in research/unconfirmed.md.
- Nvidia is Lambda's investment grade offtaker. Bloomberg only.
- Anthropic is the end user behind Fluidstack's Hut 8 lease. Tier 2 only.

## Needs quote

None new. The tier 2 items above are listed in R5_cluster_b_private.md.

## Domains added

None. All new evidence is on sec.gov.

## Open questions

1. Ward County: is the anchor customer that may step in Microsoft? The Ionic S-1/A names Microsoft only as holder of an option on more power. If it is Microsoft, Nvidia's guarantee and a Microsoft step-in protect the same lease.
2. Ward County: does Nscale's parent guarantee from year six also back Nvidia's indemnity claim? Nvidia's recourse beyond the $470m escrow ranks with Nscale's other unsecured claims (analysis).
3. Abernathy: did the Google backstop survive TeraWulf's sale of its 50.1% joint venture stake in July 2026, and who is the landlord now?
4. CoreWeave: is the DDTL 4.0 contract (rated A3) Microsoft's or Meta's? If Meta's, Meta is both CoreWeave's customer collateral and Nebius's buyer of last resort.
5. IREN: is the Mackenzie GPU Financing 2.0 tied to Nvidia's $3.4bn contract or to the Together AI, Perplexity and Prometheus contracts?
