# R5 cluster A2 + F: AI model developers, venture and portfolio companies

**Date:** 23 November 2026. **Namespace:** `labb` (ev_90001 to ev_90072). **Draft:** `research/drafts/cluster_a2f.json`: 36 entities (30 depth 1, 6 depth 2), 31 relationships, 24 events. `python3 -m pipeline.checks draft research/drafts/cluster_a2f.json` prints "All checks passed".

Tier 2 sources: every fetch through `pipeline.cache fetch` from bloomberg.com, cnbc.com and axios.com returned HTTP 403, and WebSearch refuses reuters.com, wsj.com, ft.com, barrons.com and economist.com. No tier 2 evidence could be created. Every displayed figure below is tier 1: SEC filings, Nvidia releases, or the counterparty's own site. All tier 2 claims are under "Needs quote".

Evidence ids ev_90001 to ev_90013 duplicate R1 13F evidence (ev_50003 to ev_50029), which I found after creating them. The draft cites the R1 ids. The duplicates are not referenced and can be dropped at merge. ev_90059 duplicates ev_50068 (Groq) and is not referenced.

## 1. Disposition of every company checked

| Company | Disposition | Record / reason | Key evidence |
|---|---|---|---|
| Mistral AI | Recorded | rel_mistral_eq_2025, EQ, completed. Series C EUR 1.7B at EUR 11.7B led by ASML, with Nvidia among existing investors. Nvidia amount not disclosed | ev_90026, ev_90027, ev_90067 (Mistral Compute on Nvidia reference architectures) |
| Safe Superintelligence | Recorded | rel_ssi_eq_2026, EQ, completed. Amount not disclosed. Tied to Vera Rubin compute access | ev_30059, ev_30060 |
| Thinking Machines Lab | Recorded | rel_thinking_machines_eq_2026, EQ, reconciled. Includes a commitment to deploy at least 1 GW of Vera Rubin | ev_30057, ev_30058, ev_90045, ev_90046 |
| Reflection AI | Recorded | rel_reflection_eq_2025, EQ. Reflection raised $2B (ev_90030). Nvidia's portion is unconfirmed | ev_90029, ev_90030 |
| Poolside | Unconfirmed (needs quote) | Tier 2 only. No tier 1 source found on Poolside's site, in Nvidia releases or in the Q2 FY27 10-Q | see R4 |
| Perplexity | Participation reported, not recorded | perplexity.ai blog (tier 1, domain added) names NVIDIA in the Jan 2024 Series B and the Apr 2024 extension. The cache gets HTTP 403, so no quote can be stored | search result only |
| Cohere | Recorded | rel_cohere_eq_2025, EQ. Aug 2025 $500M round (ev_90032) and Series E initial close, 29 Oct 2026 | ev_90031, ev_90035 |
| Sakana AI | Recorded (long tail) | rel_sakana_eq_2024 | ev_90044 |
| Figure | Recorded | rel_figure_eq_2025. Series C over $1B (ev_90043). Figure has a $3.5B compute commitment with Nscale on Vera Rubin (ev_90065) | ev_90042 |
| Wayve | Recorded (2 records) | rel_wayve_eq_2024 (Series C 2024 and Series D 2026 equity). rel_wayve_eqc_2025 (LOI headline $500M, ev_90036) | ev_90036 to ev_90041 |
| Hugging Face | Excluded | A full acquisition (8-K 2026-09-02, ev_30080 and ev_30081), not credit exposure. On closing it is consolidated. The map gains nothing from an LI node; listing it would put about $11.9B of purchase price on an exposure map | ev_30081, ev_50089 |
| Groq | Excluded | Nvidia's 10-K Note 2: a non-exclusive license plus hires. "No customer contracts, existing products, or equity interests were purchased" (ev_50068). $13.0B paid at closing (ev_50066) and $4B payable within a year (ev_50067), booked as goodwill and an intangible. Nvidia has no claim on Groq and Groq owes Nvidia nothing, so there is no credit exposure to show. The cash outflow belongs in the R1 aggregates and the system view as a use of Nvidia cash, not as a node | ev_50066, ev_50067, ev_50068 |
| Point2 Technology | Recorded (long tail) | rel_point2_eq_2026 | ev_30069 |
| Motif Technologies, RLWRLD, Upstage | Recorded (3 records) | rel_*_eqc_2026, EQ-C, loi_or_framework. "Planned" only, no terms | ev_30070 |
| NAVER | Recorded | rel_naver_eq_2026. **Status changed from LOI to definitive.** On 27 Oct 2026 NAVER said the precondition was met (ev_90068). $1B headline and committed (ev_30072, ev_90072). Not yet funded | ev_90068 to ev_90072 |
| UK AI startup commitment (GBP 2B) | Recorded | rel_uk_ai_startup_program_eqc_2025, loi_or_framework. GBP 2B kept as original_value. USD value is null because no FX source is on file | ev_30084, ev_50090 |
| Generate Biomedicines | Recorded (13F, current) | market_value $12,516,542 at 2026-09-30 (ev_50029). 833,325 shares | ev_50028, ev_50029 |
| Recursion | Recorded (13F, exited) | $50M PIPE on 2023-07-11 (ev_90017, ev_90019). Exited Q4 2025 | ev_50003, ev_50004, ev_90016 |
| SoundHound | Recorded (13F, exited Q4 2024) | | ev_50005, ev_50006, ev_90015 |
| Serve Robotics | Recorded (13F, exited Q4 2024) | Over $12M invested since 2022 (ev_90021). $2.5M convertible note converted to equity (ev_90024). 10.0% holder | ev_50110, ev_50111, ev_90022 |
| Nano-X | Recorded (13F, exited Q4 2024) | | ev_50008, ev_50009 |
| WeRide | Recorded (13F, exited Q4 2025) | Investor since 2017 (ev_90025) | ev_50016, ev_50017 |
| TuSimple | Recorded (13F, exited Q1 2024) | | ev_50007, ev_90014 |
| Applied Digital, Arm | Excluded | Out of cluster (neocloud and semis) | |
| Scale AI | Recorded | Series F $1B, Nvidia an existing investor | ev_90047 |
| Anysphere (Cursor) | Recorded, restructured | Series D, Nov 2025 (ev_90048). Acquired by SpaceX 2026-08-14 (ev_90049) | |
| Databricks | Recorded | Series I over $500M, Sept 2023 | ev_90050, ev_90051 |
| Commonwealth Fusion Systems | Recorded | NVentures in the $863M Series B2 | ev_90052, ev_90053 |
| PsiQuantum | Recorded | NVentures in the $1B Series E | ev_90054, ev_90060 |
| Quantinuum | Recorded | NVentures in the ~$600M round. Listed 2026 but absent from Nvidia's 13F | ev_90055, ev_90056 |
| TerraPower | Recorded | NVentures in the $650M raise | ev_90057, ev_90058 |
| Skild AI | Recorded | NVentures in the $1.4B Series C | ev_90061, ev_90062 |
| Black Forest Labs | Recorded (long tail) | $300M Series B | ev_90063 |
| Nuro | Participation reported, not recorded | nuro.ai listing page did not render the release (Series E $203M, Nvidia reported) | nuro.ai |
| Inflection AI | Participation reported, not recorded | Jun 2023 $1.3B round. No allowed page found | none |
| Imbue, Runway, Together AI, Periodic Labs, Physical Intelligence, World Labs, Lila Sciences, Humans&, Field AI, Waabi, ElevenLabs | Not checked (budget) | Long tail candidates for a follow-up pass. Together AI is arguably a neocloud | |
| Nvidia and Eli Lilly $1B AI drug lab (Bloomberg, Jan 2026) | Excluded | A joint lab spend, not an investment in a company | |

Seniority for every equity record is common_equity where stated, otherwise assumed and noted. All equity wrong-way risk is general except the exited 13F positions (none). No record carries specific wrong-way risk. The one debt instrument found is the Serve Robotics note, which converted to equity.

## 2. R4 tier 2 table (all "needs quote": fetch HTTP 403)

| Claim | Publication 1 | Publication 2 | Dates | Status |
|---|---|---|---|---|
| Nvidia to invest up to $1B in Poolside | Bloomberg, "Nvidia to Invest Up to $1 Billion in AI Startup Poolside" | The Information, "Nvidia Said to Plan $1 Billion Investment in Poolside" | 2025-10-30 / 2025-10 | Two outlets in the search, neither cached. Not recorded |
| Nvidia to pay Poolside a $6B license and hire staff | Bloomberg (citing Newcomer) | The Information | 2026-08-20 / 2026-08 | Bloomberg cites Newcomer, so not independent of it. Not recorded. A possible LI record |
| Nvidia committed $5B to SSI | Bloomberg, 2026-07-27 (people familiar) | Bloomberg circular-deals graphic (same outlet) | 2026-07-27 | Single source. Not displayed |
| Nvidia in talks for about $2.5B in Thinking Machines | The Information | none | 2026 | Single source |
| Nvidia joined the TML $2B seed (Jul 2025) and the SSI Apr 2025 round | CNBC, 2025-09-26 and 2026-03-10 | none | | Single source |
| Nvidia leads Reflection $1B round with $500M | Bloomberg, 2025-09-17 | none (the NYT $800M is not allowed) | | Single source. Later round reported as $2B (tier 1 ev_90030) |
| Nvidia explores larger investment in or acquisition of Reflection | Bloomberg (citing FT), 2026-10-10 | FT (not reachable) | | Unconfirmed |
| Reflection compute: SpaceX up to $6.3B; Nebius $1B | CNBC 2026-06-22; Bloomberg 2026-07-14 | | | Depth 2 links not recorded |
| Mistral 2023 round with Nvidia and Salesforce | Bloomberg, 2023-12-04 | none | | Not recorded |
| Groq deal "about $20B"; DOJ probe; Groq raising $650M | CNBC 2025-12-24; Bloomberg 2026-09-10; Axios 2026-05-28 | | | Context for the Groq exclusion |

## 3. Seeds

| Seed | Result | Reason |
|---|---|---|
| A4 Mistral AI | **Confirmed** | Mistral's Series C release, 2025-09-09, lists NVIDIA among existing investors (ev_90026). The amount is undisclosed on both sides |
| A5 Reflection AI | **Modified** | Reflection says it raised $2B and names NVIDIA as an investor (ev_90029, ev_90030). "Large investor" and Nvidia's portion are tier 2 only. Nvidia is silent, so the record is one_sided |
| A6 Poolside | **Unconfirmed (kept open)** | The up to $1B figure appears only in tier 2 (Bloomberg, The Information), now joined by a reported $6B license. No tier 1 source exists, so no record. It is not killed, because two outlets report it; it needs quotes pasted |
| A7 Other labs | **Modified** | Confirmed by tier 1: SSI, Thinking Machines, Cohere, Sakana, Figure, Wayve (plus a $500M LOI), Point2, Skild, Black Forest Labs and others. Perplexity is confirmed on its own site but not cacheable. No Nvidia amount is disclosed anywhere except NAVER and Recursion |
| C4 Groq | **Modified** | Not "about $20B" in filings. Filed figures are $13.0B paid at closing plus $4B payable within a year, with no equity acquired (ev_50066 to ev_50068). Excluded from the map: a purchase, not credit exposure |
| B9 (13F part, my holdings) | **Confirmed / modified** | Recursion, SoundHound, Serve, Nano-X, WeRide and TuSimple are all exited (TuSimple Q1 2024; Nano-X, Serve and SoundHound Q4 2024; Recursion and WeRide Q4 2025). Generate Biomedicines is still held, worth $12.5M at 2026-09-30 |

## 4. Reconciliation table

| Relationship | Result | Note |
|---|---|---|
| rel_thinking_machines_eq_2026 | reconciled | Same wording on both sites. Amount silent |
| rel_naver_eq_2026 | reconciled | $1B on both sides. NAVER adds that the precondition was met on 27 Oct |
| rel_recursion_eq_2023 | reconciled | 13F shares match the 8-K: 7,706,363 |
| rel_serve_robotics_eq_2022 | reconciled | 13G 10.0% matches the S-1 10.0% |
| rel_weride_eq_2017 | reconciled | Existence and type only. Neither side discloses cost |
| rel_ssi_eq_2026, rel_point2_eq_2026, Motif/RLWRLD/Upstage, rel_uk_ai_startup_program_eqc_2025, 13F-only (SoundHound, Nano-X, TuSimple, Generate) | one_sided | Counterparty silent |
| All other venture records (Mistral, Reflection, Cohere, Sakana, Figure, Wayve x2, Skild, BFL, Scale, Cursor, Databricks, CFS, PsiQuantum, Quantinuum, TerraPower) | one_sided | Only the counterparty disclosed. No Nvidia release or filing names them |

## 5. Top findings

1. **NAVER is the only Nvidia amount in this cluster that both sides state and that is now committed.** The $1B headline (ev_30072, ev_90072) became definitive on 27 Oct 2026, when NAVER said a $9B Brookfield vehicle agreement met the precondition (ev_90068, ev_90070). The vehicle will buy GPUs and data centers, and NAVER guarantees NAVER Cloud's usage fees for up to eight years (ev_90071). This is a closed loop: Nvidia equity, then Brookfield GPU financing, then an Nvidia DSX AI factory.
2. **Nvidia never states the size of its lab investments.** Across 20 private venture relationships, no allowed source gives Nvidia's dollar amount. Where Nvidia announces the deal itself (SSI, Thinking Machines), it pairs the investment with a compute commitment on its own Vera Rubin systems ("at least one gigawatt" for Thinking Machines). Figure separately committed $3.5B of compute on Vera Rubin through Nscale (ev_90065).
3. **The 13F small caps are all exited except Generate.** Recursion was bought for about $50M (8-K) and was worth $37.6M at its last 13F. Serve was bought for over $12M including a convertible note. The Cursor stake was restructured by the SpaceX acquisition: Nvidia's SpaceX share count rose by 7.7M shares in Q3 2026 (analysis; whether this is linked is unknown).

## Not found

- Nvidia-side disclosure (release, 10-K or 10-Q) for Mistral, Reflection, Poolside, Cohere, Figure, Wayve, Scale, Databricks and the others. Searched R3 crawl results, Nvidia 8-K earnings releases Q2 FY26 and Q3 FY27, the Q2 FY27 10-Q, and EDGAR full text.
- NVIDIA in Generate Biomedicines' 424B4 and in Quantinuum's 424B4 (2026-06-05): not named.
- The Poolside investment or license on poolside.ai (blog and newsroom).
- Mistral's Series D release (EUR 3B, led by Samsung) does not name NVIDIA.
- Cohere's 2023 Series C page caches without body text.
- SoundHound, Nano-X and TuSimple counterparty filings describing the Nvidia stake (one EDGAR full-text query each; nothing relevant).

## Unconfirmed

- Poolside: up to $1B equity (Oct 2025) and a $6B license and hiring deal (Aug 2026). Tier 2 only.
- SSI: $5B. Thinking Machines: $2.5B talks. Reflection: Nvidia led, $500M or $800M. All single source or not allowed.
- Perplexity: tier 1 page not cacheable (HTTP 403). The candidate row c_labb_021 carries source_date 2024-01-04, which I did not verify from the page and must be checked.
- Inflection AI, Nuro: participation reported, not confirmed from a cached allowed source.

## Needs quote

| Title | Outlet | Date | URL |
|---|---|---|---|
| Nvidia to Invest Up to $1 Billion in AI Startup Poolside | Bloomberg | 2025-10-30 | https://www.bloomberg.com/news/articles/2025-10-30/nvidia-to-invest-up-to-1-billion-in-ai-startup-poolside |
| Nvidia Said to Plan $1 Billion Investment in Poolside | The Information | 2025-10 | https://www.theinformation.com/briefings/nvidia-said-plan-1-billion-investment-poolside |
| Nvidia to Pay AI Startup Poolside a $6 Billion License, Newcomer Says | Bloomberg | 2026-08-20 | https://www.bloomberg.com/news/articles/2026-08-20/nvidia-to-pay-ai-startup-poolside-a-6-billion-license-newcomer-says |
| Nvidia to Invest $5B in Ilya Sutskever's AI Startup Safe Superintelligence | Bloomberg | 2026-07-27 | https://www.bloomberg.com/news/articles/2026-07-27/nvidia-makes-substantial-investment-in-sutskever-s-ai-startup |
| Nvidia Discusses $2.5 Billion Investment in Mira Murati's Thinking Machines Lab | The Information | 2026 | https://www.theinformation.com/briefings/nvidia-discusses-2-5-billion-investment-mira-muratis-thinking-machines-lab |
| Nvidia, 1789 Capital Invest in Reflection AI | Bloomberg | 2025-09-17 | https://www.bloomberg.com/news/articles/2025-09-17/1789-said-to-join-nvidia-in-backing-deepseek-rival-reflection-ai |
| Nvidia Explores Deal Options With Reflection AI | Bloomberg | 2026-10-10 | https://www.bloomberg.com/news/articles/2026-10-10/nvidia-is-in-talks-to-acquire-reflection-ai-the-ft-reports |
| SpaceX signs computing power deal with Reflection worth up to $6.3 billion | CNBC | 2026-06-22 | https://www.cnbc.com/2026/06/22/spacex-ai-colossus-data-center-reflection.html |
| These are the European startups Nvidia backed in 2025 | CNBC | 2026-01-26 | https://www.cnbc.com/2026/01/26/nvidia-ai-startup-investments-europe-chips-jensen-huang.html |
| DOJ Probes Nvidia's $20 Billion License Deal With Groq | Bloomberg | 2026-09-10 | https://www.bloomberg.com/news/articles/2026-09-10/doj-probes-nvidia-s-license-deal-with-groq-on-antitrust-concerns |

## Domains added

All added to `config/sources_allowlist.json` under `tier1.company_domains`, each the company's own corporate site:

| Entity | Domain | Why |
|---|---|---|
| ent_cohere | cohere.com | Funding round releases |
| ent_wayve | wayve.ai | LOI, Series C and Series D releases |
| ent_figure | figure.ai | Series C and Nscale compute release |
| ent_perplexity | perplexity.ai | Funding blog (fetch blocked) |
| ent_sakana | sakana.ai | Series A and corporate info |
| ent_recursion | recursion.com | Counterparty site (SEC used instead) |
| ent_generate_biomedicines | generatebiomedicines.com | Counterparty site (not used) |
| ent_scale_ai | scale.com | Series F |
| ent_anysphere | cursor.com | Series D and SpaceX acquisition |
| ent_databricks | databricks.com | Series I |
| ent_commonwealth_fusion | cfs.energy | Series B2 |
| ent_psiquantum | psiquantum.com | Series E |
| ent_quantinuum | quantinuum.com | 2025 raise |
| ent_terrapower | terrapower.com | 2025 raise |
| ent_skild_ai | skild.ai | Series C |
| ent_black_forest_labs | bfl.ai | Series B |
| ent_nuro | nuro.ai | Series E (page did not render) |

Already present and used: mistral.ai, ssi.inc, thinkingmachines.ai, reflection.ai, poolside.ai, navercorp.com.

## Open questions

1. Quantinuum is listed (QNT) but absent from Nvidia's 13F for 2026-06-30 and 2026-09-30. Was the NVentures stake sold, or is it held outside the 13F filer?
2. Cursor: what did Nvidia receive in the SpaceX acquisition? Does any of the SpaceX 13F increase in Q3 2026 (122.76M to 130.47M shares) come from it? This is analysis only and belongs with the SpaceX cluster.
3. Wayve: did the $500M LOI convert in full into Series D shares?
4. NAVER: closing date and price per share of the private placement. Watch for NAVER's capital increase disclosure.
5. Poolside: if Nvidia's next 10-Q (Q3 FY27) names a Poolside license, record it as LI, mirroring Groq.
6. Reflection: the announcement date on the page (9 Aug 2025) conflicts with tier 2 coverage (9 Oct 2025). `dates.announced` is left null.
7. GBP 2B UK commitment: the lead should supply an allowed FX source (or a USD figure from a later Nvidia filing) before display.
8. Entities ent_asml, ent_brookfield, ent_nscale, ent_spacex, ent_softbank and ent_microsoft are defined here as depth 2 stubs. Merge with the other clusters' definitions.
