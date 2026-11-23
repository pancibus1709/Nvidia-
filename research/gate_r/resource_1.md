# Gate R re-sourcing, claims 1-15 (verifier 1)

Sourced independently on 2026-11-23. Evidence is in namespace `gr1` (ev_140001 to ev_140027).

| n | id | overall | mismatches / not found / missed |
|---|---|---|---|
| 1 | rel_openai_eqc_2025 | reopen | status: mismatch (LOI as of 2025-11-19 (10-Q Q3 FY26); by 2026-02-25 10-K says NVIDIA is 'finalizing an investment and partnership agreement'; the $30B Feb 2026 round followed and NVIDIA's Q1/Q2 FY27 10-Qs no longer mention the LOI); classification: Headline correctly treated as headline only (committed/funded/contingent blank) |
| 2 | rel_openai_eq_2026 | confirmed | missed: funded: CNBC 2026-05-09 'Nvidia embraces role of AI investor' says the $30 billion was 'pumped into OpenAI in  |
| 3 | rel_openai_gu_2026 | confirmed | missed: maturity: each guaranty ends no later than the 20th anniversary of its lease commencement; missed: Option for about 3.8 GW of further credit support, no amount |
| 4 | rel_anthropic_eqc_2025 | confirmed | - |
| 5 | rel_anthropic_eq_2026 | reopen | contingent_max: mismatch (The purchase closed on 2026-11-20, so NVIDIA has no remaining contingent payment obligation; the prospectus contingency (IPO completion) is satisfied); classification: contingent_max should be blank or 0 |
| 6 | rel_thinking_machines_eq_2026 | confirmed | - |
| 7 | rel_cohere_eq_2025 | confirmed | missed: Series E date: initial close announced 2026-10-29 |
| 8 | rel_motif_eqc_2026 | confirmed | missed: Same release: NVIDIA 'announced an investment in Korean startup Point2' |
| 9 | rel_rlwrld_eqc_2026 | confirmed | missed: Same release: NVIDIA 'announced an investment in Korean startup Point2' |
| 10 | rel_upstage_eqc_2026 | confirmed | missed: Same release: NVIDIA 'announced an investment in Korean startup Point2' |
| 11 | rel_naver_eq_2026 | confirmed | - |
| 12 | rel_uk_ai_startup_program_eqc_2025 | reopen | missed: headline GBP 2 billion: 'NVIDIA commits £2 billion to catalyze the U.K.’s AI startup ecosystem' |
| 13 | rel_figure_eq_2025 | confirmed | - |
| 14 | rel_wayve_eqc_2025 | reopen | status: mismatch (Superseded: Wayve 'closed a $1.2B Series D' (2026-02-25) with NVIDIA participating; NVIDIA amount undisclosed); classification: The LOI was for 'Wayve's next funding round', and that round (Series D) closed on 2026-02-25 with NVIDIA participating; missed: Series D closed 2026-02-25, NVIDIA a participant |
| 15 | rel_skild_ai_eq_2026 | confirmed | - |

**Totals:** 11 confirmed, 4 reopen (n = 1, 5, 12, 14). No NOT FOUND fields.

## Most serious problems
1. **rel_openai_eqc_2025 (n=1): stale status.** The $100B LOI (ev_140005, ev_140006) is still recorded as an open framework. NVIDIA's 10-K (2026-02-25) says it was "finalizing an investment and partnership agreement" (ev_140027). The $30B round followed (ev_140008, ev_140025). NVIDIA's Q1 and Q2 FY27 10-Qs no longer mention the LOI. Mark it superseded/restructured so the $100B is not displayed as a live commitment next to the $30B.
2. **rel_anthropic_eq_2026 (n=5): contingent_max = $10B on a closed purchase.** The placement closed on 2026-11-20 (ev_140012). Recording the $10B as contingent as well as funded double-counts exposure. Set contingent_max blank or 0.
3. **rel_wayve_eqc_2025 (n=14): stale LOI.** Wayve closed its Series D on 2026-02-25 with NVIDIA participating (ev_140022). The LOI was for that round. Status should be completed, with the amount undisclosed. The $500M must not be treated as funded.
4. **rel_uk_ai_startup_program_eqc_2025 (n=12): missed headline.** NVIDIA's own release says "commits £2 billion" (ev_140020). The headline is blank.
5. Lesser points. rel_openai_gu_2026 is described in the 8-K as residual value guaranties (type RV rather than GU), and the 20-year term per lease is not recorded as a maturity. rel_naver_eq_2026's commitment is conditional on NAVER finalizing $9B of financing (ev_140018). Cohere's Series E is only at initial close.

## Not found
- No NVIDIA filing names the OpenAI $30B, the Anthropic placement, NAVER or any startup amount. The 10-Qs for Q1/Q2 FY27 give only aggregates: $18.6B of private investments in Q1, $99B equity investments and $25B commitments at 2026-07-26. NVIDIA's Q3 FY27 10-Q was not on EDGAR as of 2026-11-23.
- NAVER closing or share-issuance notice: not on navercorp.com; DART not checked.
- No Upstage, Motif or RLWRLD release on NVIDIA's investment.

## Needs quote
- CNBC, "Nvidia embraces role of AI investor, pushing past $40 billion in equity bets this year", 2026-05-09, https://www.cnbc.com/2026/05/09/nvidia-embraces-ai-investor-topping-40-billion-in-equity-bets-2026.html. Says the $30B was "pumped into OpenAI in late February" (bears on funded for n=2) and that Huang said $100B is "not in the cards" (n=1). The fetch returned HTTP 403.

## Domains to add
- None needed. skild.ai, figure.ai, wayve.ai, cohere.com, thinkingmachines.ai and navercorp.com are already allowlisted.
