# R5, R8, R9 draft: Cluster C (chipmakers, optics, EDA, packaging, test, substrate)

Namespace `semi` (ev_60001 to ev_60114). Draft: `research/drafts/cluster_c.json` (16 entities, 14 relationships, 23 events; `pipeline.checks draft` prints "All checks passed"). As of 23 November 2026.

## Reconciliation table

| Claim | Nvidia side | Counterparty side | Result | Differences |
|---|---|---|---|---|
| Intel EQ, $5.0B for 214,776,632 shares at $23.28 | Release $5B at $23.28 (ev_30033, ev_30034, 2025-09-18); $5B investment commitment subject to regulatory approval (ev_50061, ev_10155, 10-Q 2025-11-19); gains on Intel stock (ev_10111); 13F 214,776,632 sh at 2025-12-31 (ev_50020), 161,082,488 sh worth $19,366,947,532 at 2026-09-30 (ev_50021) | SPA 2025-09-15, 214,776,632 sh at $23.28, $5.0B, HSR condition, no governance or information rights (ev_60001, ev_60002, ev_60009, ev_60003, ev_60004, 8-K 2025-09-18); closed 2025-12-26 (ev_60005, ev_60006, ev_60008, 8-K 2025-12-29); 10-Q repeats (ev_60010) | reconciled | Holding cut by 53,694,144 shares in Q3 2026 (analysis); no source gives the reason |
| Nokia EQ, $1.0B for 166,389,351 shares at $6.01 | Release $1B at $6.01 (ev_30038, ev_30036); 13F 166,389,351 ADS (ev_50024), 72,859,751 ADS worth $738,797,875 at 2026-09-30 (ev_50025) | 6-K 2025-10-28: USD 1.0B, USD 6.01, 2.90% (ev_60036, ev_60037, ev_60038); completed 2025-11-13 (ev_60041); 20-F: 166 389 351 shares, USD 1 000 million proceeds, EUR 859m cash (ev_60033, ev_60035, ev_60030) | reconciled | No Nvidia closing statement; holding cut 56% in Q3 2026 with no disclosure on either side |
| Synopsys EQ, $2B for 4,821,717 shares at $414.79 | Release (ev_30039, ev_30040, 2025-12-01); 13F 4,821,717 (ev_50022), 4,354,077 worth $1,893,762,250 at 2026-09-30 (ev_50023) | 8-K 2025-12-01 (ev_60042, ev_60044, ev_60045); 10-Q net proceeds $2.0B (ev_60047) | reconciled | Holding cut by 467,640 shares in Q3 2026 |
| Marvell EQ, $2.0B convertible preferred | Release: "has invested $2 billion" (ev_30078, 2026-03-31) | 8-K 2026-03-31: 2,000,000 Series A convertible preferred, $2,000,000,000.00, convertible into up to 21,778,000 shares at about $91.8355 (ev_60051 to ev_60054); 10-Q (ev_60059) | reconciled | Nvidia does not state the security; preferred not on 13F |
| Lumentum EQ, $2.0B convertible preferred | Release: "is investing $2 billion" plus multi-billion purchase commitment (ev_30046, ev_30047) | 8-K 2026-03-02: 2,876,415 preferred at $695.31, $2,000,000,000 (ev_60064 to ev_60066); 10-Q (ev_60072) | reconciled | Security not stated by Nvidia |
| Coherent EQ, $2B for 7,788,161 shares at $256.80 | Release (ev_30048); 13F 7,788,161, $2,241,510,617 at 2026-09-30 (ev_50027) | 8-K 2026-03-02 (ev_60075 to ev_60077); 10-Q: six-month lock-up, price protection expired untriggered Sept 2026 (ev_60082, ev_60079) | reconciled | Lock-up and price protection only on Coherent's side |
| Arm EQ (13F only) | 13F 1,960,784 ADS 2023-12-31 (ev_50001); 1,101,249 ADS 2025-09-30 (ev_50002); absent 2025-12-31 | No disclosure found as of 2026-11-23 | one_sided | Exited |
| Corning EQ, $500M warrants | Q1 FY27 release names agreements with Corning (ev_50140); no investment named | 8-K 2026-05-06: warrant for 15M shares at $180 plus pre-funded warrant for 3M shares, $500M (ev_60085 to ev_60088); 10-Q proceeds from warrants $500M (ev_60097) | partial | Nvidia never states the warrants |
| Corning PP, $1.0B customer deposit (new) | No disclosure found as of 2026-11-23 | 10-Q: $1.0B customer deposit, supply agreement to 2029-12-31, offset by $267M warrant to the customer (ev_60094 to ev_60096); warrants issued 2026-05-06 (ev_60102) | one_sided | Customer identity is analysis |
| Amkor PP, "nearly $3 billion" incl. prepayments | Release 2026-11-17 (ev_30065, ev_30066) | 10-Qs: July 2026 agreement about $1.5B in 2027 (ev_60110, ev_60111); October 2026 agreement about $1.3B in 2027 (ev_60104, ev_60105); $200M standby LCs (ev_60106) | partial | $2.8B of advances vs "nearly $3B" of agreements; customer unnamed by Amkor |
| KYEC PP, $1.1B advance | Release 2026-10-21 (ev_30062) | No disclosure found as of 2026-11-23 | one_sided | |
| IBIDEN PP, multibillion | Release 2026-10-21 (ev_30063) | No disclosure found (PDF text not extractable) | one_sided | |
| Unimicron PP, capacity reservation | Release 2026-10-21 (ev_30064) | No disclosure found | one_sided | No amount, no advance stated |
| SPIL PP, multibillion funding | Release 2026-11-17 (ev_30067) | No disclosure found (ASE 20-F searched) | one_sided | Form of funding unknown |

## Per-company notes

**Intel.** Signed 2025-09-15, closed 2025-12-26 after HSR (ev_60003, ev_60008). Funded $5.0B, 214,776,632 shares (ev_60006). Tied to products: Intel builds Nvidia-custom x86 CPUs and x86 SOCs with RTX chiplets (ev_60021, ev_60022). No lock-up, standstill or registration rights found; no governance or information rights (ev_60004). Held 161,082,488 shares worth $19,366,947,532 at 2026-09-30 (ev_50021). Co-investors (depth 2): SoftBank 87M shares at $23.00, $2.0B, closed 2025-09-26 (ev_60011, ev_60012); US Department of Commerce 275M shares, 159M escrowed shares, warrant for 241M shares at $20 if Intel owns under 51% of foundry (ev_60024, ev_60025, ev_60013); escrow derivative liability $13.7B (ev_60014). Credit: BBB after an August 2025 downgrade by an unnamed agency (ev_60026); total debt $50,134M (ev_60017); cash and short-term investments $54,005M (ev_60016); short-term debt $3,817M (ev_60018); $15.0B undrawn revolvers (ev_60019, ev_60020); $23.0B equity offering in August 2026 (ev_60015). Internal grade Adequate (stepped down from Strong; reasons in the draft).

**Nokia.** 2.90% at issuance (ev_60038). Issue described as "an essential part of the strategic partnership" (ev_60039): Nokia's RAN software on Nvidia's architecture and AI networking collaboration (ev_60040, ev_60031). Share count fell from 166,389,351 to 72,859,751 between the 2026-06-30 and 2026-09-30 13Fs. Explanation from allowed sources: none. Nokia's 6-Ks from July to November 2026 contain no Nvidia sale; Nvidia's Q3 FY2027 release shows $2,253M of equity-sale proceeds without naming issuers (ev_60113). wwr none: telecom equipment demand does not hinge on AI.

**Synopsys.** Signed and funded the same day (ev_60043). The 10-Q says term loan repayment of $3.5B was partly offset by the Nvidia proceeds (ev_60048); it does not say the proceeds paid the loans. Long-term debt $9,017M, cash and short-term investments $3,608M at 2026-07-31 (ev_60050, ev_60049).

**Marvell and Lumentum.** Both bought convertible preferred, not common: that is why neither appears on Nvidia's 13F (analysis). Neither preferred has a liquidation preference or redemption right (ev_60056, ev_60057, ev_60068), so seniority is preferred in name only. Holder conversion waits for HSR (ev_60055, ev_60067). Marvell also issued Google a warrant for 58,970,907 shares at $206.58 tied to TPU-ecosystem silicon (ev_60062, ev_60063). Lumentum is building a new fab (ev_60069) and has $1,360.3M of current debt against $1,272.2M cash (ev_60074, ev_60073).

**Coherent.** Six-month lock-up (ev_60082) and six-month price protection that expired untriggered (ev_60079, ev_60080). Access to five co-packaged optics product families (ev_60078).

**Arm.** Not a current exposure; exit by 2025-12-31. Seed C5 modified.

**Corning (new).** Two records. (1) Warrants: 15M shares at $180 plus 3M pre-funded, $500M paid, three-year life, traditional warrant ends if the partnership agreement terminates (ev_60085 to ev_60091). The widely reported "up to $3.2 billion" equals $500M plus 15M x $180 (analysis); exercise is Nvidia's option. (2) Customer deposit: $1.0B recorded in Q2 2026 under a supply agreement to 2029-12-31, applied against receivables as delivered (ev_60094, ev_60098, ev_60099). Attribution to Nvidia is analysis from three quotes (ev_60096, ev_60102, ev_60088). Corning commits to 10x US optical connectivity capacity and three plants (ev_60092).

**Amkor.** Amkor's 10-Q also expects about $1.9B of customer advances in the next 12 months, $200M of which need standby letters of credit (ev_60103); contract liabilities $547.6M (ev_60107). Advances are expected in 2027, so funded is unknown.

**KYEC, IBIDEN, Unimicron, SPIL.** Nvidia side only (R3 evidence). Not SEC registrants (SPIL's parent ASE files a 20-F; nothing found).

**Aggregate context (R1, no record created).** Prepaid supply and capacity: long-term $1,536M and short-term $2.0B at 2025-10-26 (ev_10147, ev_10148); breakdown not disclosed after October 2025. Supply and capacity commitments $279B at 2026-07-26 (ev_10029). Level 2 public equity (warrants, convertible preferred) $10,806M (ev_10015); public company warrants notional $4,800M (ev_10026): Marvell, Lumentum and Corning instruments likely sit here (analysis).

## Seeds

| Seed | Status | Reason |
|---|---|---|
| C1 Intel | confirmed | $5.0B, 214,776,632 shares at $23.28 quoted from Intel 8-Ks (ev_60002, ev_60007, ev_60009); closed 2025-12-26 (ev_60008). Modified detail: stake cut to 161,082,488 by 2026-09-30 |
| C2 Nokia | confirmed | USD 1.0B at USD 6.01 quoted from Nokia 6-K (ev_60036, ev_60037); completed 2025-11-13 (ev_60041). Stake cut to 72,859,751 by 2026-09-30, reason not found |
| C3 Synopsys | confirmed | $2B, 4,821,717 shares at $414.79 (ev_60042, ev_60044, ev_60045) |
| C5 Arm | modified | Long-standing 13F holding confirmed (ev_50001, ev_50002) but exited by 2025-12-31; no current exposure |
| C6 Suppliers | modified | Aggregates from R1 confirmed. Named prepayments found for Amkor (counterparty filings), KYEC, IBIDEN, SPIL, Unimicron (Nvidia side only) and a newly found $1.0B Corning deposit. No TSMC, SK hynix, Samsung, Micron, Foxconn or Wistron prepayment found in an allowed source |

## Not found

- Reason and date for Nvidia's Q3 2026 sales of Intel, Nokia and Synopsys shares: Intel 8-Ks and 10-Q, Nokia 6-Ks July to November 2026, Synopsys filings, Nvidia Q3 FY2027 release and CFO commentary. Nvidia's Q3 FY2027 10-Q not yet filed.
- Intel rating agency name and maturities in months 13 to 24.
- Any lock-up, standstill or registration rights for Intel, Nokia, Synopsys, Marvell, Lumentum.
- KYEC, Unimicron and SPIL counterparty disclosure; IBIDEN notice PDF fetched (research/cache/web/ibiden.com/...icpkggcapitalinvestment2026.pdf) but text not extractable.
- Prepayments to TSMC, SK hynix, Samsung, Micron, Foxconn, Wistron: full-text search `"NVIDIA" "prepayment"` on 6-K and 20-F, Arm and ASE filings; Nvidia's Q3 FY2027 release lists Samsung Electro-Mechanics and Kinsus without amounts.
- Nvidia-side disclosure of the Corning deposit.

## Unconfirmed

- Nvidia "reduced stake" in Nokia, headline dated 2026-11-17 listed on a CNBC quote page, attributed to TipRanks (excluded source).

## Needs quote

- CNBC, "Arm shares edge higher as Nvidia sells entire stake in company", 2026-02-18, https://www.cnbc.com/2026/02/18/arm-nvidia-nokia-ai-stake-shares.html (HTTP 403).
- CNBC, "NVIDIA to Invest Up to $3.2 Billion in Corning...", 2026-05-06 (from R3; URL not captured).
- Amkor IR releases (tier 1 but proxy and WebFetch return 403): https://ir.amkor.com/news-releases/news-release-details/amkor-technology-announces-strategic-partnership-nvidia-expand and https://ir.amkor.com/news-releases/news-release-details/amkor-technology-and-nvidia-advance-strategic-partnership-ai. A search snippet says the July release describes a $1.5B agreement with a Nvidia prepayment; this would let committed_total drop its "analysis" label.

## Domains added

None. All needed domains were already in `config/sources_allowlist.json`. `ir.amkor.com` falls under `amkor.com` but the proxy blocks it.

## Open questions

1. Should the Corning deposit and the Amkor $2.8B carry `label: analysis` through to display, or wait for a source naming Nvidia?
2. Coherent's cash and debt are reported in $000; the evidence tool does not accept "($000)" as a scale anchor, so no amount objects were made.
3. Incident: my scratchpad helper `ev.sh` was overwritten by another researcher's script of the same name; sourcing it once re-ran their commands and appended about 24 duplicate records to `research/evidence/laba.jsonl` (e.g. ev_120072, ev_120074 ... ev_120122). I did not edit that file. The lab researcher or lead should decide which ids to keep.
