# R4/R5 · Cluster B, private neoclouds with no SEC filings

Namespace `neop` (ev_110001 to ev_110064). Prepared 23 November 2026. Draft: `research/drafts/cluster_b_private.json` (15 entities, 11 relationships, 5 projects, 16 events). Every figure below is followed by its evidence id and date. "Analysis" marks my inference. All amounts USD unless stated.

## 0. Method and what blocked it

- **EDGAR re-check.** `pipeline.edgar cik` finds no CIK for Lambda, Crusoe, Firmus, Fluidstack, Together AI/Together Computer, Vultr/Constant Company or Voltage Park (the tool reads the ticker list, so it only confirms none is listed). Full-text search (1 Jun 2025 to 23 Nov 2026, S-1, S-1/A, DRS, F-1, 424B4, 10-K, 8-K) found **no filing by any of the seven as registrant**. Third-party filings that describe them: Anthropic's 424B4 of 19 Nov 2026 (Lambda Agreements, Fluidstack colocation), IREN's 10-K and 8-K (Together AI and Fluidstack as customers), Exascale Labs filings (Voltage Park as a competitor). `research/evidence/fulltext_hits.jsonl` and `research/drafts/r3_announcements.json` contain none of the seven names. R3 found only the 9 Sep 2026 Australia release naming Firmus.
- **Tier 2 news could not be fetched.** WebSearch refuses reuters.com, wsj.com, ft.com, barrons.com and economist.com for this user agent. `pipeline.cache fetch` returned HTTP 403 for every bloomberg.com, theinformation.com, cnbc.com and axios.com URL tried. Only asia.nikkei.com fetched. Every Bloomberg, Information, CNBC and Axios item is therefore under "Needs quote" and none is in the register.
- **Company releases** (tier 1 after domain additions) carried the work: lambda.ai, lambda.com, crusoe.ai, firmus.co, together.ai, plus Nvidia's blog.
- **Check tooling.** After the lead's fixes (full-text hits moved to `.ndjson`, `ent_nvidia` added to `data/register/entities.json`), `python3 -m pipeline.checks draft research/drafts/cluster_b_private.json` prints **"All checks passed"**. All neop evidence still grounds (none was affected by the reverted XBRL rendering change).
- **Grounding parser.** Figures written as `$480M`, `$1.5B`, `A$330m`, `$102.5M` are not parsed by `common.numbers_in`, so those evidence records (ev_110059, ev_110060, ev_110062, ev_110064) carry no grounded value and the amounts are not entered.

## 1. R4 table (claim, publication 1, publication 2, dates, status)

| # | Claim | Publication 1 (date) | Publication 2 (date) | Status |
|---|---|---|---|---|
| 1 | NVIDIA invested in Lambda Series D | Lambda release (2025-02-19) ev_110001, tier 1 | CNBC "Lambda raises $480 million ... Nvidia among investors: Reuters" (2025-02-19), 403 | Existence confirmed (tier 1); amount not disclosed |
| 2 | Nvidia rents back its own GPUs from Lambda, about $1.5bn over four years (B5) | The Information (2025, exact date not fetched), 403 | The Information briefing, same outlet | Needs quote; not in register |
| 3 | Lambda $926M TLB funds GPUs for an "Nvidia-tied chip deal" | Bloomberg (2026-08-10, 2026-08-12), 403, one outlet | Lambda release (2026-08-12) ev_110002/ev_110003 names only "an investment-grade offtaker" | Facility confirmed; Nvidia as offtaker unconfirmed |
| 4 | Lambda $1bn private debt tied to Microsoft deal | Bloomberg (2026-08-28), 403 | Lambda release (2026-10-01) ev_110006: $1.008bn DDTL, two investment-grade offtakers | Facility confirmed; offtaker names unconfirmed |
| 5 | Anthropic $35bn compute from Lambda; Nvidia holds the data center lease | The Information citing WSJ, 403 | Anthropic 424B4 (2026-11-19) ev_110012: about $34.9bn agreement; ev_110013 lease not secured | Amount confirmed tier 1; Nvidia lease role unconfirmed; **deal now terminable** |
| 6 | Lambda pre-IPO round up to $3bn; bankers hired | Bloomberg (2026-08-24), 403 | The Information, 403 | Needs quote |
| 7 | NVIDIA in Crusoe Series D, E, F | Crusoe releases (2024-12-12, 2025-10-24, 2026-09-17) ev_110016, ev_110018, ev_110020 | Bloomberg (2025-10-23, 2026-09-03), Axios Pro (2026-09-04), 403 | Confirmed tier 1; Nvidia amounts not disclosed |
| 8 | Crusoe Series F size | Crusoe release $3.9bn anticipated, initial close (2026-09-17) ev_110019 | Bloomberg "over $3 billion" (2026-09-03), 403 | Tier 1 figure displayed; round total may change |
| 9 | AMD backstops a $300M Crusoe loan | The Information, 403 | none | Needs quote (context, not Nvidia) |
| 10 | NVIDIA in Firmus A$330m, USD505m, USD2bn rounds | Firmus releases (2025-09-16, 2026-04-07, 2026-08-07) ev_110062, ev_110030, ev_110033 | Nikkei Asia (2026-04-07) ev_110063; Nikkei (2026-10-09) ev_110051 | Confirmed; USD505m is tier 1 plus tier 2 |
| 11 | Firmus Batam: Nvidia revenue share and credit support | Firmus release (2026-06-28) ev_110037 | Nvidia blog (2026-07-01) ev_110043, ev_110044 (tier 1, other side); The Information, 403 | Existence reconciled both sides; size undisclosed |
| 12 | Firmus withdrew ASX IPO | Nikkei Asia (2026-10-09) ev_110048 | Bloomberg/Information (2026-10-20), 403 | Single tier 2 fetched (reported) |
| 13 | Nvidia in talks to invest more in Firmus after the IPO flop | The Information (Oct 2026), 403 | Bloomberg (2026-10-20) cites The Information, so not independent | Needs quote, single source |
| 14 | Firmus seeks about $7.5bn debt plus $2.5bn equity for Indonesian site | Bloomberg (2026-09-23 per search), 403 | none | Needs quote |
| 15 | NVIDIA in Together AI Series A, B, C | Together releases (2023-11-29, 2025-02-20, 2026-07-01) ev_110053, ev_110055, ev_110057 | Bloomberg (2025-02-20), 403 | Confirmed tier 1 |
| 16 | Nvidia invests in Volta (new neocloud) at $2.4bn valuation | Bloomberg (2026-08-04), 403 | none fetched (other hits are excluded sites) | Needs quote; new candidate |
| 17 | Nvidia invests in Fluidstack | none found | none | Not found |
| 18 | Nvidia invests in or finances Vultr | none found (AMD led the equity) | none | Not found |
| 19 | Nvidia financing of Voltage Park | none found | none | Not found |

## 2. Per-company findings

### Lambda (`ent_lambda`, rel_lambda_eq_2025)
- **Nvidia relationship sourced:** equity only. Lambda's Series D release names NVIDIA among new investors (ev_110001, 2025-02-19). The Series E release (over $1.5B, 2025-11-18, ev_110060) does not name Nvidia. Nvidia amount, class and ownership: not disclosed by either side. Reconciliation: one_sided (Nvidia silent).
- **Leaseback (seed B5):** not quotable from any fetchable allowed source. Nvidia's 10-Q reports AI cloud agreements only in aggregate ($36bn, ev_10036; Nvidia buys capacity the clouds cannot sell, ev_50078).
- **Debt (all company releases, drawn balances not disclosed):** $1bn syndicated senior secured credit facility, upsized from $275M, J.P. Morgan (ev_110009, 2026-05-07); $926M TLB, SOFR + 3.00%, matures 2030-12-31, Morgan Stanley lead left, Moody's facility rating Baa2, funds GPUs "dedicated to an investment-grade offtaker" (ev_110002 to ev_110005, 2026-08-12); $1.008bn fixed rate DDTL at 6.78%, matures 2033-05-30, Moody's Baa1 and DBRS A (low), two investment-grade offtakers (ev_110006 to ev_110008, 2026-10-01). Both asset level loans are secured by the funded GPUs and contracted cash flows.
- **Customers:** Microsoft, multibillion multi-year (ev_110010, 2025-11-03). Anthropic agreed to spend about **$41.3bn** under the Lambda Agreements (ev_110011, Anthropic 424B4 2026-11-19).
- **Change tracked:** of that, the August 2026 agreement (about **$34.9bn**, ev_110012) is now **terminable by either party because Lambda did not secure the facility lease** by the contractual date (ev_110013). Neither party had given notice; Anthropic says it does not intend to terminate. Analysis: about 85% of Lambda's disclosed Anthropic backlog hangs on one lease.
- **Credit grade:** Insufficient information (facility ratings are not issuer ratings).

### Crusoe (`ent_crusoe`, rel_crusoe_eq_2024, _2025, _2026)
- **Nvidia relationship:** equity participant in Series D $600M (ev_110015, ev_110016, 2024-12-12), Series E $1.375bn initial close (ev_110017, ev_110018, 2025-10-24) and Series F $3.9bn anticipated at $30.9bn post-money (ev_110019 to ev_110021, 2026-09-17). Nvidia amounts not disclosed. Reconciliation one_sided.
- **Debt:** Brookfield $750M credit facility (ev_110024, 2025-06-11); Upper90 about $225M facility "used exclusively for the purchase of NVIDIA GPUs" (ev_110025, ev_110026, page dated 2025-03-27 in metadata). Lenders BCI, FS Investments, King Street, Liberty Mutual, ORIX USA in the Upper90 syndicate (same release, not separately recorded).
- **Scale:** over $140bn contracted value (ev_110022), 6GW+ gross contracted capacity (ev_110023).
- **Project:** Abilene, 1.2 GW, second phase of a $15bn joint venture with Blue Owl and Primary Digital (ev_110061, 2025-05-21), up to 50,000 GB200 NVL72s per building (ev_110027). No Nvidia credit support found. Tenant not named in the release.
- **Measure input:** `counterparty_nvidia_spend` at least $225M (Upper90 use of proceeds, ev_110025), lower bound.
- No Nvidia backstop, lease or guarantee found for Crusoe.

### Firmus (`ent_firmus`, rel_firmus_eq_2025, _2026a, _2026b, rel_firmus_bk_2026)
- **Equity:** A$330m placement with NVIDIA participation (ev_110062, 2025-09-16; AUD, unparsed); USD505m led by Coatue with NVIDIA "subject to certain closing conditions" (ev_110029, ev_110030, 2026-04-07; Nikkei ev_110063 independently reports $505m with a further Nvidia infusion); USD2bn fully committed with NVIDIA follow-on (ev_110032, ev_110033, 2026-08-07); more than USD3bn new equity in the year (ev_110034).
- **Credit support (BK):** Firmus's partnership with NVIDIA runs through 2034 for a 360 MW Batam campus, up to 170,000 accelerators, on "a revenue-sharing and credit-support model" (ev_110037 to ev_110040, 2026-06-28). Nvidia's blog names Firmus as among the first partners in that model (ev_110044, 2026-07-01). **Reconciliation partial:** both sides confirm existence and scale; neither states the size, form or trigger of the credit support. Firmus expects US$25 to 30bn of committed customer offtake over six years (ev_110041); that is Firmus revenue, not Nvidia exposure. WWR specific.
- **Debt:** US$10bn debt facility led by Blackstone, supported by Coatue (ev_110035, 2026-02-09; Nikkei ev_110050).
- **Change tracked:** Firmus withdrew its ASX IPO, which sought up to A$7.9bn (about $5.5bn) (Nikkei, ev_110048, ev_110049, 2026-10-09). An analyst quoted by Nikkei said 46 MW was built of 912 MW contracted (ev_110052, opinion). Reported follow-up Nvidia investment talks: Needs quote.
- **Customers:** OpenAI anchor, two Malaysian sites (ev_110046, 2026-09-08); total contracted capacity more than 900 MW (ev_110047).

### Together AI (`ent_together_ai`, rel_together_ai_eq_2023, _2025, _2026)
- **Equity:** NVIDIA in Series A (ev_110053, 2023-11-29), Series B $305M (ev_110054, ev_110055, 2025-02-20), Series C $800M (ev_110056, ev_110057, 2026-07-01). Series C adds over 500 MW of compute "to be capitalized independently by our new investors" (ev_110058): who finances it is not stated.
- **Context:** customer of IREN, whose July 2026 contracts with Prometheus, Perplexity and Together AI total about $2.8bn (ev_40120, aggregate, not Together alone); named as a Crusoe Cloud customer.

### One line each, nothing sourced
- **Fluidstack:** no Nvidia investment, backstop or lease found in allowed sources; Anthropic's 424B4 names Fluidstack USA I Inc. as its colocation and data center operator (context only, not recorded).
- **Vultr:** no Nvidia financial tie found; equity was led by AMD Ventures and LuminArx (CNBC, 403).
- **Voltage Park:** no Nvidia financial tie found; company site says it is backed by a Navigation Fund grant and has merged with Lightning AI (not recorded).
- **Volta (new):** Bloomberg reports Nvidia invested; Needs quote; candidate c_neop_010.

## 3. Reconciliation table

| Relationship | Result | Nvidia side | Counterparty side |
|---|---|---|---|
| rel_lambda_eq_2025 | one_sided | No disclosure found as of 2026-11-23 | ev_110001 |
| rel_crusoe_eq_2024 / 2025 / 2026 | one_sided | No disclosure found as of 2026-11-23 | ev_110016 / ev_110018 / ev_110020 |
| rel_firmus_eq_2025 / 2026a / 2026b | one_sided | No disclosure found as of 2026-11-23 | ev_110062 / ev_110030 / ev_110033 |
| rel_firmus_bk_2026 | partial | ev_110043, ev_110044, ev_110045 (blog), aggregate ev_10036 | ev_110037 to ev_110041 |
| rel_together_ai_eq_2023 / 2025 / 2026 | one_sided | No disclosure found as of 2026-11-23 | ev_110053 / ev_110055 / ev_110057 |

## 4. Seeds

| Seed | Status | Reason |
|---|---|---|
| B5 Lambda leaseback (about 18,000 GPUs, about $1.5B over four years; Nvidia largest customer) | **modified** | No seed number is quotable: The Information pages return 403 and no tier 1 source names a Lambda leaseback or Nvidia as Lambda's largest customer. What is confirmed instead: Nvidia is a Lambda equity investor (ev_110001), and Lambda's backlog leans on Anthropic (about $41.3bn, ev_110011), now partly terminable (ev_110013). Lambda has filed no S-1; no customer concentration disclosure exists. Leaseback stays in Needs quote. |
| B7 Crusoe, Nvidia participation in funding rounds | **confirmed** (amount Not confirmed) | Crusoe's own releases name NVIDIA in Series D, E and F (ev_110016, ev_110018, ev_110020). No source states Nvidia's amount; nothing in the seed's amount column is quoted. |

## 5. Entries for `research/unconfirmed.md`

- Lambda: Nvidia rents back its own GPUs (about 10,000 for $1.3bn plus 8,000 for $200M per search snippets of The Information). Only source paywalled (403). Reason: no fetchable allowed source.
- Lambda: Nvidia is Lambda's largest customer. No allowed source found.
- Lambda/Anthropic: Nvidia supplies the chips and holds the lease for the Anthropic data center developed by Hut 8 (The Information citing WSJ). Paywalled; WSJ not searchable.
- Lambda: term loan B tied to an Nvidia contract (Bloomberg only).
- Firmus: Nvidia in talks to invest hundreds of millions after the IPO withdrawal (The Information; Bloomberg cites it).
- Firmus: about $7.5bn debt and $2.5bn equity sought for an Indonesian site (Bloomberg only).
- Crusoe: AMD guarantees a $300M Crusoe loan (The Information only; AMD, not Nvidia).
- Crusoe: Nvidia helped facilitate Meta's talks to lease the Abilene expansion (Bloomberg, March 2026, per search snippet).
- Volta: Nvidia and Michael Dell back Volta at $2.4bn valuation; $5bn financing; $10bn Anthropic contract (Bloomberg; other copies on excluded sites).

## 6. Not found

- SEC registrant filings for any of the seven (EDGAR CIK and full-text, through 2026-11-23).
- Nvidia newsroom or filings naming an investment amount in Lambda, Crusoe, Firmus or Together AI; Nvidia 13F lists none (private).
- Any Nvidia guarantee, lease or backstop for Crusoe (Abilene or elsewhere), Fluidstack, Vultr or Voltage Park.
- UCC or Companies House searches were not run (lien registries not reachable with the tools in this session).
- Firmus's ASX prospectus and withdrawal announcement (ASX/ASIC documents) were not located; they would be tier 1.

## 7. Needs quote (paywalled or blocked, HTTP 403)

| Title | Outlet | Date | URL |
|---|---|---|---|
| Nvidia to Pay $1.5 Billion to Rent Back Its Own Chips From Cloud Startup | The Information | not shown | https://www.theinformation.com/articles/nvidia-quietly-boosts-cloud-ally-1-5-billion-deal-rent-ai-chips |
| Nvidia Quietly Agrees to Pay $1.5 Billion to Rent its Own AI Chips From Lambda | The Information | not shown | https://www.theinformation.com/briefings/nvidia-quietly-agrees-pay-1-5-billion-rent-ai-chips-lambda |
| Lambda Sells $917 Million Loan to Fund Nvidia Chip Deal | Bloomberg | 2026-08-10 | https://www.bloomberg.com/news/articles/2026-08-10/ai-cloud-provider-lambda-taps-loans-for-nvidia-tied-chip-deal |
| AI Cloud Provider Lambda Secures $926 Million Loan for Nvidia Chip Deal | Bloomberg | 2026-08-12 | https://www.bloomberg.com/news/articles/2026-08-12/ai-cloud-provider-lambda-prices-loan-for-nvidia-tied-chip-deal |
| Nvidia-Backed Lambda Secures $1 Billion Debt to Fund AI Chip Purchases | Bloomberg | 2026-08-28 | https://www.bloomberg.com/news/articles/2026-08-28/nvidia-backed-lambda-inks-1-billion-private-debt-for-chip-deal |
| Anthropic Said to Reach $35 Billion Compute Deal With Nvidia-Backed Lambda | The Information | not shown | https://www.theinformation.com/briefings/anthropic-said-reach-35-billion-compute-deal-nvidia-backed-lambda |
| AI Cloud Provider Lambda in Talks for $3 Billion Pre-IPO Round | Bloomberg | 2026-08-24 | https://www.bloomberg.com/news/articles/2026-08-24/ai-cloud-provider-lambda-in-talks-for-3-billion-pre-ipo-round |
| AI cloud startup Lambda raises $480 million in new round; Nvidia among investors | CNBC (Reuters) | 2025-02-19 | https://www.cnbc.com/2025/02/19/ai-cloud-startup-lambda-raises-480-million-in-new-round-nvidia-among-investors.html |
| Nvidia Will Backstop Customers' GPUs, Take a Cut of Their Cloud Revenues | The Information | not shown | https://www.theinformation.com/briefings/nvidia-will-backstop-customers-gpus-take-cut-cloud-revenues |
| Crusoe Raises Over $3 Billion in Funding at $30 Billion Valuation | Bloomberg | 2026-09-03 | https://www.bloomberg.com/news/articles/2026-09-03/crusoe-raises-over-3-billion-in-funding-at-30-billion-valuation |
| Data center developer Crusoe raises $3.9 billion in pre-IPO round | Axios Pro | 2026-09-04 | https://www.axios.com/pro/climate-deals/2026/09/04/crusoe-funding-pre-ipo-round-data-center-fundraise |
| AMD to Backstop $300 Million Crusoe Loan, Following Nvidia Playbook | The Information | not shown | https://www.theinformation.com/articles/amd-backstop-300-million-crusoe-loan-following-nvidia-playbook |
| AI Data Center Group Firmus Draws $2 Billion From Coatue, Nvidia | Bloomberg | 2026-08-07 | https://www.bloomberg.com/news/articles/2026-08-07/ai-data-center-group-firmus-draws-2-billion-from-coatue-nvidia |
| Nvidia Moves to Back GPU Cloud Provider Firmus After Investors Balk at Its IPO | The Information | Oct 2026 | https://www.theinformation.com/articles/nvidia-moves-back-gpu-cloud-provider-firmus-investors-balk-ipo |
| Nvidia in Talks to Back Firmus After IPO Flop, Information Says | Bloomberg | 2026-10-20 | https://www.bloomberg.com/news/articles/2026-10-20/nvidia-in-talks-to-back-firmus-after-ipo-flop-information-says |
| Firmus And Nvidia Partner On Massive Data Center Project In Indonesia | The Information | not shown | https://www.theinformation.com/briefings/firmus-nvidia-partner-massive-data-center-project-indonesia |
| Nvidia-Backed AI Startup Seeks $10 Billion Before Australian IPO | Bloomberg | 2026-09-23 | https://www.bloomberg.com/news/articles/2026-09-23/nvidia-backed-ai-startup-seeks-10-billion-before-australian-ipo |
| Nvidia, Dell Back AI Cloud Startup Volta at $2.4 Billion Value | Bloomberg | 2026-08-04 | https://www.bloomberg.com/news/articles/2026-08-04/nvidia-dell-back-ai-cloud-startup-volta-at-2-4-billion-value |
| Nvidia's role as AI financier faces first big test as neoclouds take market hit | CNBC | 2026-10-24 | https://www.cnbc.com/2026/10/24/nvidias-role-as-ai-financier-faces-first-big-test-as-neoclouds-take-market-hit.html |
| Startup Together AI Valued at $3.3 Billion as AI Demand Grows | Bloomberg | 2025-02-20 | https://www.bloomberg.com/news/articles/2025-02-20/startup-together-ai-valued-at-3-3-billion-as-ai-demand-grows |

## 8. Domains added (to `config/sources_allowlist.json`, `tier1.company_domains`)

| Entity | Domain | Why |
|---|---|---|
| ent_lambda | lambda.com (appended to existing lambda.ai, lambdalabs.com) | Lambda moved its site to lambda.com; Series D and credit facility releases live there |
| ent_firmus | firmus.co | Firmus newsroom (funding, Batam, OpenAI releases) |
| ent_together_ai | together.ai | Together AI funding announcements |

Domains to add (not added): `fluidstack.io` (ent_fluidstack, if Fluidstack enters the register), `voltagepark.com`, Volta's domain once identified.

## 9. Open questions

1. Is the Firmus Batam credit support one of the "AI cloud agreements" in Nvidia's $36bn aggregate (ev_10036), and what is its cap? Nvidia's Q3 FY2027 10-Q (due after the 17 Nov 2026 8-K) should be checked for partner names.
2. Who is the "investment-grade offtaker" behind Lambda's $926M TLB: Nvidia (as Bloomberg's headline implies) or Microsoft? If Nvidia, the TLB lenders rely directly on Nvidia rent (lender_reliance, specific WWR).
3. Will Anthropic or Lambda terminate the $34.9bn August 2026 agreement, and did Nvidia's lease role (reported) lapse with the unsecured lease?
4. Did Nvidia invest again in Firmus after the October 2026 IPO withdrawal?
5. Who capitalizes Together AI's 500 MW (ev_110058), and is Nvidia's AI cloud model involved?
6. `common.numbers_in` does not parse values written as `$480M`, `$1.5B`, `A$330m`; if the lead extends it, ev_110059, ev_110060, ev_110062 and ev_110064 can be re-created with values and the round sizes entered.
