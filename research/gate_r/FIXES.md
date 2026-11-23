# Gate R fixes applied after independent re-sourcing

- rel_openai_eqc_2025: status loi_or_framework to restructured; insight rewritten; event added (verifier 1, n=1)
- rel_wayve_eqc_2025: status to restructured; closing event added (verifier 1, n=14)
- rel_uk_ai_startup_program_eqc_2025: sterling headline now dated and shown in pounds, not converted (verifier 1, n=12)
- rel_tusimple_eq_2023: status terminated to completed; insight no longer claims the position is closed (verifier 2, n=18)
- rel_coreweave_gu_2026: type GU to CX because no guarantee exists, only a stated intent (verifier 2, n=22)
- rel_meta_eq_2026: note added that the offering priced and Nvidia's purchase is unconfirmed (verifier 3, n=43)
- rel_corning_pp_2026: announced date set to 2026-05-06 (verifier 3, n=38). Funded stays undisclosed because Corning does not name the depositor.
- rel_coreweave_bk_2025: depth 2 link to Galaxy Digital added, the first sourced case of a financing document citing the order (R2)
- rel_nscale_gu_2025: depth 2 link to the landlord, Ionic Digital, added (R2)

## Verifier findings not acted on, with reasons

- n=5 Anthropic, n=24 Nscale equity, n=27 Nebius warrant: the verifiers read the claims file as showing a contingent amount equal to the funded amount. The register records contingent as not applicable on all three. No change needed.
- n=3 OpenAI lease guaranties: the filing calls them residual value guaranties. The record keeps guarantee as the primary type because the trigger is the tenant's default, and already lists residual value as a secondary type.
- n=21 CoreWeave: the filing calls $6.3 billion the initial value of the order, not a cap. The record already says so in the amount note.
- n=31 to 33 Intel, Nokia, Synopsys: funded is the cash Nvidia paid, which does not change when shares are later sold. The holdings, market values and notes already show the reduced positions at 30 September 2026.
- n=38 Corning: the $1.0 billion deposit is not entered as funded by Nvidia because Corning does not name the depositor. The link is labeled analysis.
- n=25 Nscale notes: no filing confirms the second $1.0 billion closed, so funded stays at $1.0 billion.

## Fixes from the closing credit review (R9)

Applied in the draft files on 2026-11-23 (namespace `fix` for new evidence). Each consequence now carries its evidence ids in its `evidence` list, not in the text.

- rel_motif_eqc_2026, rel_rlwrld_eqc_2026, rel_upstage_eqc_2026: generic template replaced by one first order item (plan only, no amount or terms, nothing owed until signed) and one second order item (other investors cannot count on Nvidia money until terms are signed), both on ev_30070 (R9 a1, generic).
- rel_sakana_eq_2024, rel_skild_ai_eq_2026, rel_black_forest_labs_eq_2025, rel_scale_ai_eq_2024, rel_databricks_eq_2023, rel_commonwealth_fusion_eq_2025, rel_psiquantum_eq_2025, rel_terrapower_eq_2025: generic "down round" first order replaced by the round specific fact on file (round, lead, size) and either "reaches Nvidia only inside the unattributed non-marketable equity line" or "immaterial unless sized" (R9 a1, generic).
- rel_sakana_eq_2024: unsourced signaling item (drew Japanese banks) dropped; replaced by a second order item stating the signaling effect is unknown (R9 a1, overstates).
- rel_quantinuum_eq_2025: "share price moves daily" replaced by the 13F absence at 2026-06-30 and 2026-09-30, so holding and market value are unknown (R9 a1).
- rel_crusoe_eq_2026, rel_firmus_eq_2026b, rel_together_ai_eq_2026: keep the full consequence set as the latest round; rel_crusoe_eq_2024/2025, rel_firmus_eq_2025/2026a, rel_together_ai_eq_2023/2025 each now carry one first and one second order item on what that round added (R9 a1, duplicated text).
- rel_firmus_eq_2026b: trigger on talks after the failed IPO marked "reported, unconfirmed"; signaling item rewritten to Coatue and Blackstone equity and the $10 billion facility beside Nvidia (ev_110035, ev_110033, ev_110037), lens lender_reliance (R9 a1, overstates).
- rel_firmus_bk_2026: lender reliance item rewritten: no Batam lender is identified; Blackstone facility use for Batam is conditional (R9 a1, overstates).
- rel_together_ai_eq_2026: contagion item limited to IREN's three-customer July 2026 contracts of about $2.8 billion (ev_40120); unsourced Crusoe naming dropped here and in the capacity item (R9 a1, overstates).
- rel_ai_financing_platforms_rv_2026: template fill errors fixed; first order and lender reliance now say support covers up to a quarter of an opportunity and is not in place until final agreements (ev_30013, ev_30015) (R9 a1, generic).
- rel_soundhound_eq_2023: unsourced "market read" signaling item replaced by "history only" (ev_50005, ev_50006) (R9 a1).
- rel_openai_eq_2026: unsourced "SoftBank borrowed" replaced by SoftBank's USD 30.0 billion in three tranches (ev_120103, ev_120104) (R9 a1, overstates).
- rel_anthropic_eqc_2025: "trains on Trainium, TPUs and AMD" replaced by the sourced Google, Amazon and Broadcom lease commitments (ev_120045, ev_120046, ev_120051) (R9 a1, overstates).
- rel_ssi_eq_2026: "lowering SSI's cost of capital" replaced by "substantial but no amount" (ev_30059, ev_30060) (R9 a1, overstates).
- rel_reflection_eq_2025: signaling rewritten to Nvidia named in a $2 billion raise without its share (ev_90029, ev_90030); contagion item on clouds dropped until sourced (R9 a1, overstates).
- rel_coreweave_eq_2025: signaling item rewritten to Galaxy Digital's Helios noteholder presentation citing Nvidia's ~11.5% stake and order (ev_170016, ev_170017) (R9 a1, overstates).
- rel_coreweave_bk_2025: lender reliance item added on the landlord's noteholders shown "up to $6.3Bn" while the order ends after a 90 day insolvency (ev_170016, ev_20006); contingent_max note now cites ev_170016 and keeps the "not a proven ceiling" caveat (R9 a1, a3).
- rel_lambda_eq_2025: signaling item rewritten: rated loans rest on funded GPUs and investment-grade offtakers (ev_110003, ev_110005 to ev_110007), Nvidia as offtaker unconfirmed (R9 a1, overstates).
- rel_meta_eq_2026: revenue quality item made conditional on a purchase under the non-binding indication (ev_100041, ev_30077) (R9 a1, overstates).
- rel_helix_lp_2026: signaling item rewritten to Vistra (up to $1 billion) and KIA as founding investors, causation not stated (ev_100055, ev_100030); reconciliation reconciled to partial with a difference: Nvidia's only reference is a KKR executive's quote (R9 a1, a2).
- rel_brookfield_baiif_lp_2025: signaling item rewritten (Nvidia named strategic LP, commitment undisclosed, ev_100038; unconfirmed $10 billion target removed); contagion item labeled analysis because no source places the NAVER vehicle in the fund (R9 a1).
- rel_corning_pp_2026: first order item reworded "if the unnamed customer is Nvidia"; headline and committed_total set to unknown; facts moved to notes labeled analysis (ev_60094, ev_60095, ev_60096, ev_60102, ev_60088); insight no longer uses {committed_total} and states the uncertainty; definition updated (R9 a1, a3).
- rel_nscale_gu_2025: second order lender reliance item added for Ionic Digital (ev_170021, ev_170013); reconciliation reconciled to partial with a difference: Nvidia never names Nscale, the landlord or the site (ev_10159, ev_40003, ev_170012) (R9 a1, a2).
- rel_tusimple_eq_2023: duplicate ev_50007 removed from nvidia_evidence (R9 a2).
- rel_amkor_pp_2026: committed_total ($2.8 billion from Amkor filings that do not name the customer) set to unknown; facts moved to notes labeled analysis (ev_60111, ev_60105); headline kept because Nvidia's release grounds "nearly $3 billion" (ev_30065); definition says "nearly" and labels the customer link analysis (R9 a3).
- rel_sb_energy_eq_2026: committed_total $3.0 billion to the $1.5 billion already paid (ev_40087); contingent_max $1.5 billion (ev_40088) with trigger: IPO with at least $1.5 billion of primary proceeds, lapse on 15 May 2027 (ev_100052, ev_100023); headline stays $3.0 billion; definition, notes and insight updated (R9 a3).
- rel_naver_eq_2026: kept definitive with committed $1 billion: NAVER states it "signed a strategic investment agreement worth $1 billion with NVIDIA" on 24 July 2026 (new ev_180001) and the precondition was met (ev_90068); notes, definition, insight and reconciliation updated; funded unknown until closing (R9 a3).
- rel_applied_digital_eq_2024: status completed to terminated, the position was exited by 2025-12-31 (R9 a4).
- rel_firmus_eq_2026a: status completed to definitive; ev_110033 ("follow-on participation", August round) does not prove the April round closed (R9 a4).
- evt_intel_reduced, evt_nokia_reduced, evt_synopsys_reduced: holding_change events were already present with ev_50021, ev_50025, ev_50023; prior quarter 13F evidence (ev_160006, ev_160008, ev_160010) added (R9 a4).
- evt_lambda_anthropic_terminable: event on rel_lambda_eq_2025 with ev_110013 was already present; no change (R9 a4).
- ent_naver: cluster other to hyperscaler (NAVER Cloud operates AI data centers and buys Nvidia systems).
- Not applied: rel_wayve_eqc_2025 signaling rewrite (R9 a1), because the brief says not to change that record; rel_openai_eqc_2025 untouched for the same reason.
