# Gate R re-source 3 (claims n = 31 to 43)

Independent re-sourcing, 23 November 2026. Evidence namespace `gr3` (ev_160001 to ev_160053). Detail is in `resource_3.json`.

Result: 8 confirmed, 5 reopen.

| n | id | overall | mismatches / not found / missed |
|---|---|---|---|
| 31 | rel_intel_eq_2025 | reopen | All fields verified ($5.0bn, ev_160001/160003; closed 2025-12-26, ev_160002). Missed: holding cut to 161,082,488 shares at 2026-09-30 from 214,776,632 (13F, ev_160005/160006) |
| 32 | rel_nokia_eq_2025 | reopen | All fields verified (USD 1.0bn, ev_160013/160016; delivered Nov 2025, ev_160015). Missed: holding cut to 72,859,751 ADRs at 2026-09-30 from 166,389,351 (ev_160007/160008) |
| 33 | rel_synopsys_eq_2025 | reopen | All fields verified ($2bn, ev_160017/160019). Missed: holding cut to 4,354,077 from 4,821,717 shares at 2026-09-30 (ev_160009/160010) |
| 34 | rel_marvell_eq_2026 | confirmed | none ($2.0bn preferred, closed 2026-03-31, ev_160020 to 160022) |
| 35 | rel_lumentum_eq_2026 | confirmed | none ($2.0bn preferred, closed 2026-03-02, ev_160023 to 160025) |
| 36 | rel_coherent_eq_2026 | confirmed | none ($2bn common, closed 2026-03-02, ev_160026 to 160028; full position held at 2026-09-30, ev_160011) |
| 37 | rel_arm_eq_2023 | confirmed | none. Exit in Q4 2025 (1,101,249 ADS at 2025-09-30, absent at 2025-12-31; ev_160012). Missed: 2023-12-31 13F value $147.3m (ev_160029); IPO cornerstone aggregate up to $735m, non-binding, not split by investor (ev_160030) |
| 38 | rel_corning_pp_2026 | reopen | Missed: funded is $1.0bn, deposit received (ev_160031); announced 2026-05-06 (ev_160032). Headline/committed $1.0bn and maturity 2029-12-31 verified (ev_160033). Depositor not named by Corning; tied to Nvidia only through the warrant (ev_160034), which is inference |
| 39 | rel_amkor_pp_2026 | confirmed | Headline is "nearly $3 billion" (ev_160035). Committed 2.8bn is a derived sum: $1.5bn (Jul) + $1.3bn (Oct), both from an unnamed customer and to be received in 2027 (ev_160037/160038). Announced should include October 2026 too |
| 40 | rel_kyec_pp_2026 | confirmed | Status definitive: not found on the counterparty side (Nvidia release only, ev_160039). $1.1bn and 2026-10-21 verified (ev_160039/160040) |
| 41 | rel_sb_energy_eq_2026 | confirmed | none ($3.0bn total, ev_160043; $1.5bn funded 2026-08-17, ev_160044). Note: the second $1.5bn depends on the IPO closing (ev_160041). The IPO is still unpriced (S-1/A No. 3, 2026-11-19) |
| 42 | rel_ai_financing_platforms_rv_2026 | confirmed | none (MOUs dated 2026-08-10, subject to final agreements, ev_160045/160046; RV support is optional and unquantified, ev_160049) |
| 43 | rel_meta_eq_2026 | reopen | $3bn and 2026-10-26 verified (ev_160050). The status is stale: the offering settled 2026-10-29 (ev_160053). Meta discloses only a non-binding $5.0bn aggregate across Nvidia, AMD and Broadcom (ev_160051/160052). No filing yet confirms whether Nvidia bought |

## Most serious problems

1. **Corning (38): funded is understated.** Corning's 10-Q reports "the receipt of an upfront customer deposit of $1.0 billion" (ev_160031), so funded should be $1.0bn, not blank. The announced date (2026-05-06) is also missing. Corning never names Nvidia as the depositor; the link runs only through the warrant.
2. **Partial disposals are missing from the stake records (31, 32, 33).** The 13F for 2026-09-30 shows Nvidia sold about 25% of Intel, about 56% of Nokia and about 10% of Synopsys during Q3 2026. Showing the full original stakes overstates current exposure.
3. **Meta (43): the indication has resolved but the outcome is unknown.** The offering closed 2026-10-29. Meta's prospectus calls the indications non-binding. The CNBC, Axios and The Information articles all returned HTTP 403, so nothing confirms an actual purchase yet.
4. **Single-side support.** Amkor's committed $2.8bn comes from an unnamed customer in Amkor's filings. KYEC's $1.1bn has only Nvidia's release behind it. SB Energy's $3.0bn includes $1.5bn that depends on the IPO closing.

## Not found
- KYEC-side disclosure of the $1.1bn advance (TWSE/MOPS not reached with the available tools).
- Nvidia's actual allocation in Meta's 2026-10 offering. Not in Meta's 8-Ks of 2026-10-29, 11-05 or 11-12. Nvidia's Q3 FY27 10-Q is not yet filed.
- A Nvidia-specific dollar figure for the Arm IPO purchase.

## Needs quote (tier 2, fetch blocked, HTTP 403)
- CNBC, 2026-10-27, "Nvidia, AMD to invest $4 billion in Meta as tech giants deepen AI partnership", https://www.cnbc.com/2026/10/27/nvidia-invest-meta.html
- Axios, 2026-10-27, "Nvidia investing $3 billion in Meta in Muse partnership", https://www.axios.com/2026/10/27/nvidia-meta-muse-investment
- The Information, "Nvidia Invests $3 Billion in Meta in Deeper AI Partnership", https://www.theinformation.com/briefings/nvidia-invests-3-billion-meta-deeper-ai-partnership
- CNBC, 2026-07-24, Amkor and Nvidia $1.5bn deal, https://www.cnbc.com/2026/07/24/this-semi-stock-just-struck-a-deal-with-nvidia-ubs-sees-big-gains-ahead.html
- Amkor release "Amkor Technology and NVIDIA Advance Strategic Partnership for AI Infrastructure" (ir.amkor.com, proxy error)

## Domains to add
- ent_amkor: ir.amkor.com (Amkor's own release on the Nvidia agreements). Not added: the config file could not be read in this session.
