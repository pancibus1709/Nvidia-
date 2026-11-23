# R4, R5, R8 and R9 drafts: cluster A1 (OpenAI, Anthropic, xAI / SpaceX)

Date: 23 November 2026. Namespace `laba` (ev_120001 to ev_120112). Draft: `research/drafts/cluster_a1.json` (6 relationships, 16 entities, 17 events; `python3 -m pipeline.checks draft` prints "All checks passed").
Reused evidence: R1 (ev_10040, ev_10041, ev_10125, ev_10156, ev_10157), R1 13F (ev_50030, ev_50031), R3 (ev_30001 to ev_30031, ev_30050, ev_30092), CoreWeave (ev_20102, ev_20199), neocloud (ev_40029, ev_40030), SB Energy S-1/A (ev_40086 to ev_40099), guaranty documents from the vehicle cluster (ev_100001 to ev_100051).

What is binding today, in one table:

| Record | Type | Status | Binding amount displayed | Evidence |
|---|---|---|---|---|
| rel_openai_eqc_2025 | EQ-C | loi_or_framework | none (headline $100 billion only) | ev_30021, ev_120020 |
| rel_openai_eq_2026 | EQ | definitive | committed $30 billion (OpenAI's figure); funded not disclosed | ev_120098, ev_120015 |
| rel_openai_gu_2026 | GU (RV secondary) | definitive, not yet effective | contingent max $105 billion; paid $0 to date | ev_30001, ev_10040, ev_30024, ev_30023 |
| rel_anthropic_eqc_2025 | EQ-C | definitive (subject to closing conditions) | headline $10 billion; Series G portion undisclosed | ev_10157, ev_120066 |
| rel_anthropic_eq_2026 | EQ | completed 2026-11-20 | funded $10.0 billion, 120,481,927 Class N shares | ev_120038, ev_120069 |
| rel_spacex_eq_2026 | EQ | completed | market value $19.68 billion at 2026-09-30 (13F); cost not disclosed | ev_50031 |

## OpenAI

**Found.**
- Letter of intent, 2025-09-22: "NVIDIA intends to invest up to $100 billion in OpenAI progressively" (ev_30021, ev_120020); details to be finalized (ev_120021). Nvidia's 10-K of 2026-02-25 says it is "finalizing an investment and partnership agreement" (ev_10125). No definitive agreement on the gigawatt structure has been disclosed by either side as of 2026-11-23. Headline only.
- Equity in the 2026 round: OpenAI, 2026-02-27, $110B at $730B pre-money "includes $30B from NVIDIA" (ev_120098, ev_120099), paired with 3 GW inference and 2 GW training on Vera Rubin (ev_120105). Series C Preferred Stock Purchase Agreement dated 2026-02-27 (Amazon 8-K Ex. 10.1, ev_120032), which names NVIDIA Corporation as an investor in OpenAI (ev_120031). Round closed 2026-03-31 with $122 billion committed at $852 billion post-money, anchored by Amazon, NVIDIA and SoftBank (ev_120015, ev_120016, ev_120017). Funded amount and schedule: not disclosed. SoftBank's parallel USD 30.0 billion was paid in three USD 10 billion tranches (April, July, October 2026; ev_120103, ev_120104). Nvidia filings name only unnamed "frontier labs" commitments, $20 billion at 2026-10-25 (ev_120010, ev_120011).
- Guaranties (as tenant credit): residual value guaranties to SB Energy's PORTS-Pike building entities for leases of about 4.25 GW-IT to VELA I Holdings, LLC (an OpenAI affiliate; parent OpenAI Global, LLC by joinder, ev_100008, ev_100009). Cap $105 billion (ev_30001, ev_10040, ev_100001). Trigger: tenant insolvency default or uncured monetary default (ev_30009, ev_120001, ev_40091). Effective building by building at ready-for-service, nine phases, first expected fiscal 2029 (ev_120002, ev_30027); exposure builds to $105 billion then declines as OpenAI pays rent (ev_120009, ev_120005). Term: earliest of 20 years from each lease commencement, lease termination, OpenAI reaching a designated rating, or replacement credit support (ev_30006, ev_30007, ev_100011, ev_40095). Leases commence 2028 to 2032 (ev_40099). Limited to defined portions of lease and power payments (ev_120003). OpenAI reimburses Nvidia (ev_30008, ev_120007); no payments to date (ev_30023). Option, Nvidia's sole discretion, on the remaining capacity; if not exercised OpenAI must find an A- rated guarantor (ev_120035).
- Vehicles buying Nvidia GPUs for OpenAI: none found in allowed sources.
- Credit: not investment grade (ev_120034); revolver about $4.7 billion, undrawn (ev_120018, ev_120019); revenue "$2B in revenue per month" in March 2026 (ev_120100). Cash, losses and debt: not disclosed in allowed sources.
- Compute commitments (entity record): Microsoft Azure incremental $250 billion (ev_120111, Microsoft 10-Q); AWS $38 billion (ev_120028); CoreWeave up to $11.9 billion (ev_20199) and up to $6.5 billion (ev_20102); SB Energy PORTS-Pike about 8 GW-IT of 20-year leases, rent total not disclosed (ev_120022, ev_40098); AMD 6 GW and Broadcom 10 GW, no dollar amounts (ev_120029, ev_120030).

**Reconciliation.**

| Claim | Nvidia side | Counterparty side | Result |
|---|---|---|---|
| LOI up to $100 billion | Release ev_30021; 10-Q ev_10156; "finalizing" ev_10125 | OpenAI ev_120020, ev_120021 | reconciled (both: LOI only) |
| $30B equity in 2026 round | Not named in any Nvidia filing or release (ev_120010 unnamed) | OpenAI ev_120098, ev_120015, ev_120017; Amazon exhibit ev_120031 | one_sided |
| PORTS-Pike guaranties, cap $105 billion | ev_30001, ev_10040, ev_120001, ev_30023 | OpenAI ev_120024; SB Energy ev_40089, ev_40090, ev_40091; executed guaranty ev_100001 | partial: option 3.8 GW (Nvidia) v 3.75 IT-GW (Nvidia release) v 3.78 GW-IT (SB Energy); compensation to Nvidia stated only by SB Energy (ev_40094); replacement guarantor clause only on SB Energy side |

**R4 (tier 2).** None of these could be fetched (HTTP 403 for cnbc.com, axios.com, bloomberg.com; reuters.com, wsj.com, ft.com refused by the search tool), so none is evidence.

| Claim | Publication 1 | Publication 2 | Dates | Status |
|---|---|---|---|---|
| Huang: Nvidia to join OpenAI's round, possibly largest investment | Bloomberg | none | 2026-01-31 | needs quote |
| Nvidia nears $20B OpenAI investment | Bloomberg | none | 2026-02-03 | superseded by OpenAI's $30B (tier 1) |
| Nvidia in talks to invest up to $30B | CNBC (source) | none | 2026-02-19 | superseded by tier 1 |
| $100B LOI "on ice" (WSJ, as cited by CNBC) | WSJ | CNBC citing WSJ (not independent) | 2026-01 | needs quote; not contradicted by any tier 1 |
| Nvidia in talks on up to $250B backstop for OpenAI's Ohio lease | WSJ (via Bloomberg, CNBC) | Bloomberg | 2026-07-26/27 | changed: signed at $105 billion cap (tier 1) |
| Nvidia near deal to guarantee about $100B | The Information | none | 2026-08 | consistent with signed $105 billion |

**Seed A1: modified.** The $100 billion letter of intent was never converted (headline only, still loi_or_framework). The binding relationships are a $30B equity commitment in OpenAI's 2026 round (counterparty-disclosed, funded amount unknown) and the $105 billion guaranty of OpenAI's PORTS-Pike rent, which is the largest single contingent exposure in the register and specific wrong-way risk.

## Anthropic

**Found.**
- November 2025 agreement: Nvidia "agreed, subject to certain closing conditions, to invest up to $10 billion" (ev_10157); Anthropic: NVIDIA committing up to $10 billion, Microsoft up to $5 billion (ev_120062, ev_120063); Anthropic to buy $30 billion of Azure compute (ev_120065) and initially up to 1 GW on Grace Blackwell and Vera Rubin (ev_120064).
- Series G, 2026-02-12: $30 billion at $380 billion post-money (ev_120067, ev_120068), "includes a portion of the previously announced investments from Microsoft and NVIDIA" (ev_120066). Nvidia's portion not disclosed by either side; Nvidia is not among related-person purchasers in the 424B4.
- IPO concurrent private placement: at the $83.00 IPO price Nvidia buys 120,481,927 Class N shares for about $10.0 billion (ev_120038), contingent on the IPO (ev_120039); part of $26.0 billion with Google ($10.0 billion, ev_120042), AMD, Broadcom, Micron, Microsoft ($1.0 billion, ev_120041) and TSMC (ev_120040). Closed 2026-11-20 (ev_120069, ev_120070). Restricted securities, no lock-up. Whether this counts against the November 2025 "up to $10 billion" is not stated; recorded separately.
- Vehicles: none involving Nvidia. Anthropic's GPU capacity comes through SpaceXAI (up to $120.5 billion, ev_120047, cancellable on 90 days notice after early 2027, ev_120048), Nscale (up to $44.6 billion, ev_120049; Nscale has no binding financing, ev_40030) and Lambda ($41.3 billion, ev_120050; $34.9 billion of it currently terminable).
- Credit (2026-09-30): cash $95.6 billion (ev_120054), short-term investments $36.3 billion (ev_120055), undrawn revolver $14.8 billion of $15.0 billion (ev_120056, ev_120060, ev_120061); Amazon notes $6.2 billion principal (ev_120059); revenue nine months $33,242 million (ev_120058); capital raised $141.1 billion (ev_120057); purchase commitments $313,819 million (ev_120052), of which about $186.2 billion of obligations are contingent or terminable (ev_120053). Other commitments: Google $121.3 billion (ev_120045), Amazon $110.0 billion (ev_120046), Microsoft at least $47.2 billion (ev_120044), Broadcom leases $161.2 billion (ev_120051).

**Reconciliation.**

| Claim | Nvidia side | Counterparty side | Result |
|---|---|---|---|
| Up to $10 billion (Nov 2025) | ev_10157, ev_30050, ev_30031 | ev_120062 | partial: Anthropic says a portion funded in Series G (ev_120066); Nvidia silent on funding |
| $10.0 billion IPO placement | No disclosure found as of 2026-11-23 (Q3 FY27 10-Q not filed; Q3 release ev_120012 silent) | ev_120038, ev_120039, ev_120069 | one_sided |

**R4.** No tier 2 needed: all amounts are tier 1. Bloomberg/CNBC IPO coverage not used.

**Seed A2: modified.** The "up to $10 billion" became (a) an undisclosed Series G portion and (b) a separate, completed $10.0 billion purchase of listed Class N stock at the IPO. Microsoft's Azure commitment grew from $30 billion to at least $47.2 billion. The "1 GW of Nvidia systems" is delivered mainly through third-party clouds, not bought from Nvidia directly.

## xAI / SpaceX

**How Nvidia came to hold SpaceX.** Established from sources, step by step:
1. xAI closed a $20 billion Series E on 2026-01-06 with "NVIDIA and Cisco Investments" as strategic investors (ev_120096, ev_120097). Amount not stated.
2. SpaceX acquired X.AI Holdings Corp. effective 2026-02-02 (ev_120072); each xAI preferred share, Series E included, converted into 0.1433 SpaceX Class A shares (ev_120073), before a five-for-one split effective 2026-05-04 (ev_120074).
3. SpaceX listed in June 2026 (424B4 filed 2026-06-12, IPO price $135.00).
4. Nvidia's 13F: new position of 122,764,805 Class A shares, $20.98 billion, at 2026-06-30 (ev_50030); 130,472,925 shares, $19.68 billion, at 2026-09-30 (ev_50031).
Unexplained: the 7,708,120 share increase in Q3 2026. SpaceX issued 389,289,254 Class A shares to Cursor (Anysphere) holders on 2026-08-14 (8-K), but no allowed source names Nvidia as a Cursor holder. Analysis: at Tesla's conversion (USD 2,000 million into 3.8 million pre-split shares, ev_120080) Nvidia's share count implies an investment far larger than any quotable figure; the cost basis stays unknown.
- SpaceX's 424B4 and Q3 10-Q do not name Nvidia as a holder. Nvidia names SpaceXAI/SpaceXSI only as a customer (ev_120013, ev_120014).
- GPU vehicles: Valor leases computing equipment to xAI subsidiaries under three leases with aggregate payments of $6,986m, $6,633m and $6,587m, guaranteed by SpaceX (ev_120075 to ev_120078); recorded as failed sale-leaseback debt of $12.9 billion at 2026-09-30 (ev_120085, ev_120086). Apollo-managed lessor: binding commitment letter for a GPU finance lease of about $40 billion principal from H1 2027 (ev_120094, ev_120095). No allowed source puts Nvidia money in either.
- Credit (2026-09-30): debt principal $38,006 million (ev_120088) incl. $25.0 billion notes (ev_120084); maturities rest of 2026 $495m, 2027 $2,425m (ev_120092, ev_120093); cash $51,294m, short-term securities $38,561m, undrawn $5,000m (ev_120081 to ev_120083); non-cancelable commitments $37,840m, $25,569m due 2027 (ev_120089, ev_120090). Anthropic pays SpaceX $1.25 billion per month through May 2029 (ev_120079).

**Reconciliation.**

| Claim | Nvidia side | Counterparty side | Result |
|---|---|---|---|
| Equity stake | 13F ev_50030, ev_50031 | xAI ev_120096; SpaceX conversion ev_120072, ev_120073 | partial: cost not disclosed by either; Q3 share increase unexplained |
| SPV equity (seed A3) | None | Valor leases disclosed without Nvidia | not recorded as a relationship |

**R4.**

| Claim | Publication 1 | Publication 2 | Dates | Status |
|---|---|---|---|---|
| Nvidia up to $2B in equity of a ~$20B SPV buying Nvidia GPUs leased to xAI (anonymous) | Bloomberg (incl. Spanish edition) | none | 2025-10-08 | unconfirmed; single source, needs quote |
| Nvidia's SpaceX shares came from a $10 billion xAI investment in January (anonymous) | CNBC | none (Bloomberg 2026-08-14 reports the 13F value only) | 2026-08-14 | unconfirmed; single source |
| xAI raised $20B with Nvidia among investors | CNBC (citing xAI) | Bloomberg | 2026-01-06 | tier 1 exists (ev_120096) |

**Seed A3: modified.** The GPU leasing vehicle exists (Valor, about $20.2 billion of lease payments) but Nvidia's participation in it is unconfirmed. Nvidia's real exposure is listed SpaceX equity worth $19.68 billion at 2026-09-30, which started as an xAI Series E investment.

## Second ring (R8)

| Relationship | Depth 2 party | Role | Amount | Evidence |
|---|---|---|---|---|
| rel_openai_gu_2026 | SB Energy | landlord, guaranty beneficiary | DC backlog about $430 billion, mostly PORTS-Pike | ev_120109, ev_120036, ev_120037 |
| rel_openai_gu_2026 | SoftBank | controlling shareholder of SB Energy | n.d. | ev_120110 |
| rel_openai_eq_2026 | SoftBank | co-investor | USD 30.0 billion, fully paid | ev_120103, ev_120104 |
| rel_openai_eq_2026 | Amazon | co-investor | conditional $34,999,999,447.98 | ev_120033 |
| rel_openai_eq_2026 | Microsoft | co-investor, about 27% | $13 billion historical commitments | ev_120112 |
| rel_anthropic_eqc_2025 | Microsoft | co-investor, Azure supplier | up to $5 billion | ev_120063 |
| rel_anthropic_eq_2026 | Google, Microsoft | co-investors | $10.0 billion, $1.0 billion | ev_120042, ev_120041 |
| rel_anthropic_eq_2026 | SpaceX, Nscale, Lambda | Anthropic is their offtaker | up to $120.5bn, up to $44.6bn, $41.3bn | ev_120047, ev_120049, ev_120050 |
| rel_spacex_eq_2026 | Valor; Apollo-managed lessor | GPU lessors | $12.9bn debt; about $40bn principal | ev_120085, ev_120086, ev_120094 |
| rel_spacex_eq_2026 | Anthropic; Tesla | offtaker; co-investor | $1.25bn per month; $2.0bn | ev_120079, ev_120080 |

Loop noted for R9 (analysis): Nvidia to Anthropic (equity) to SpaceX (GPU compute contracts) to Nvidia (GPU and CPU purchases), while Nvidia also holds SpaceX equity.

## Not found

- Any Nvidia filing naming the OpenAI $30B investment or its funded amount (10-K FY26, 10-Qs Q1 and Q2 FY27, Q2 and Q3 FY27 releases and CFO commentaries). Nvidia's Q3 FY27 10-Q is not yet filed.
- OpenAI balance sheet, cash burn, debt; Oracle's OpenAI commitment amount in an allowed tier 1 source.
- Nvidia's cost for its xAI / SpaceX stake; any Nvidia investment in Cursor.
- Nvidia participation in the Valor or Apollo GPU vehicles.
- Public credit ratings for OpenAI, Anthropic or SpaceX in allowed sources.

## Unconfirmed

- Nvidia up to $2B equity in an xAI GPU SPV (Bloomberg, single anonymous source).
- Nvidia's xAI investment of $10 billion (CNBC, single anonymous source).
- "$250 billion backstop" talks (Eightco 8-K citing The New York Times; NYT is not an allowed source).

## Needs quote

- Bloomberg, "Nvidia CEO Says New OpenAI Investment May Be Largest Yet", 2026-01-31, bloomberg.com/news/articles/2026-01-31/nvidia-to-join-openai-s-current-funding-round-huang-says
- Bloomberg, "Nvidia Nears Deal to Invest $20 Billion in OpenAI Round", 2026-02-03
- CNBC, "Nvidia is in talks to invest up to $30 billion in OpenAI, source says", 2026-02-19
- CNBC, "OpenAI announces $110 billion funding round with backing from Amazon, Nvidia, SoftBank", 2026-02-27
- Bloomberg, "Nvidia in Talks to Back OpenAI Lease of $500 Billion Data Center", 2026-07-26; CNBC 2026-07-27 (up to $250B backstop)
- The Information, "Nvidia Nears Deal to Guarantee Roughly $100 Billion in Credit for OpenAI", 2026-08
- CNBC, "Nvidia discloses $21 billion stake in SpaceX at end of second quarter", 2026-08-14 ($10 billion xAI investment, anonymous)
- Bloomberg, "Musk's xAI Closed $20 Billion Funding Round With Nvidia Backing", 2026-01-06; Bloomberg 2025-10-08 (SPV)

## Domains added

None. openai.com, anthropic.com, x.ai, spacex.com, group.softbank and microsoft.com were already listed. Note: blogs.microsoft.com was fetched but not used.

## Open questions

1. Has Nvidia funded its $30B in OpenAI, and on what schedule? The Q3 FY27 10-Q may say.
2. Does the $10.0 billion Anthropic placement count toward the November 2025 "up to $10 billion"? How much did Nvidia put into Series G?
3. What explains Nvidia's 7,708,120 extra SpaceX shares in Q3 2026, and what was the cost of the xAI stake?
4. Entities ent_coreweave, ent_nscale, ent_lambda, ent_sb_energy and others are minimal depth 2 records here; the lead should merge them with the fuller records from other clusters.
5. Draft note: the guaranty `effective` and `maturity` dates are null because they differ per building; the stress team may want a per-building schedule once Schedule II (redacted) is available.
