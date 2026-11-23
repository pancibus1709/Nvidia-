# Gate R re-sourcing, batch 2 (claims n = 16 to 30)

Independent verifier, 23 November 2026. Evidence namespace `gr2` (ev_150001 to ev_150050). Field-level detail with quotes and URLs is in `resource_2.json`.

**Result: 11 confirmed, 4 reopen.** Every claimed figure was found verbatim in a tier 1 source. No figure is wrong. The four reopens are a wrong status, a wrong type and two classification errors.

| n | id | overall | mismatches / not found / classification |
|---|---|---|---|
| 16 | rel_anysphere_eq_2025 | confirmed | none |
| 17 | rel_databricks_eq_2023 | confirmed | none |
| 18 | rel_tusimple_eq_2023 | reopen | status: mismatch (Last 13F line Q4 2023: 3,465,372 sh, $3,041,904. Absent from Q1 2024 13F, but TuSimple voluntarily delisted (F); classification: 'terminated' is inferred from 13F absence. Absence follows delisting, not a disclosed disposal. Should be 'completed, holding unknown since Q1 2024' unless a sale document is found. |
| 19 | rel_generate_biomedicines_eq_2026 | confirmed | none |
| 20 | rel_coreweave_eq_2025 | confirmed | none |
| 21 | rel_coreweave_bk_2025 | confirmed | none |
| 22 | rel_coreweave_gu_2026 | reopen | classification: Type GU is not supported. No guarantee instrument, amount or beneficiary is disclosed. The release says the companies 'intend to' leverage Nvidia's financial strength, and the 8-K says it is subject t |
| 23 | rel_nscale_lb_2025 | confirmed | none |
| 24 | rel_nscale_eq_2025 | reopen | contingent_max: mismatch (Fully paid purchase; no further contingent payment is disclosed for these shares. contingent_max should be bla); classification: Amounts are exact. contingent_max duplicates funded for a completed purchase, which double counts if summed with contingent exposures. The figure excludes the $60M Series B warrants granted for the le |
| 25 | rel_nscale_fc_2026 | confirmed | none |
| 26 | rel_nebius_eq_2024 | confirmed | none |
| 27 | rel_nebius_eq_2026 | reopen | contingent_max: mismatch (Fully paid pre-funded warrant; remaining exercise price is only $0.0001 per share (about $2,107). No contingen); classification: contingent_max should be blank or not applicable for a fully paid instrument. Share count 21,065,936 (title says 21.1 million, which is fine). The warrant was not yet exercised in 13F terms: the Q3 20 |
| 28 | rel_iren_lb_2026 | confirmed | none |
| 29 | rel_iren_eq_2026 | confirmed | none |
| 30 | rel_sharonai_bk_2026 | confirmed | none |

## Most serious problems

1. **n=22 CoreWeave "GU"**: there is no guarantee. The 2026-01-26 release says the companies *intend to* "leverage NVIDIA's financial strength to accelerate CoreWeave's procurement of land, power and shell" (ev_150004). That depends on future agreements, and no instrument, amount or beneficiary is disclosed. Calling it a guarantee overstates Nvidia's credit exposure.
2. **n=24 Nscale equity and n=27 Nebius warrant**: `contingent_max` equals `funded` on fully paid purchases. Any total of contingent exposure across records would count $3.18B of cash already spent a second time. Both should be blank or not applicable.
3. **n=18 TuSimple "terminated"**: the only evidence is that TuSimple drops out of the 13F after Q4 2023 (3,465,372 shares, $3.04M, ev_150020). TuSimple delisted and deregistered in January and February 2024 (ev_150021), so it simply stopped being a 13F-reportable security. A sale is not shown.
4. **n=21 CoreWeave $6.3B**: this is the order form's "initial value", not a stated cap. It is fine as contingent, but should be labelled "initial value".
5. **n=25 Nscale notes**: the second $1.0B (the "NVIDIA Sale") was due to close around 2026-11-16. No later filing confirms it closed, and it may be settled in Non-Voting Shares. All the notes convert to equity on the IPO.

## Missed figures worth adding

- Nscale: NVIDIA guarantees the Ward County lease up to $860,340,000 (ev_150018), in exchange for warrants worth $60M.
- Nebius 2024: announced 2024-12-02 at $21.00 per share (ev_150028, ev_150029). Implied cost is about $25.0M (analysis only).
- IREN: the Investment Rights had a grant-date fair value of $793.4M (ev_150037). Both IREN records were announced 2026-05-07.
- Nscale MSA: dated July 2025 (ev_150010). Notes: Subscription Agreement dated 2026-09-15.

## Not found

- Nvidia's own amount for Anysphere, Databricks and Generate. Nvidia's 10-Q of 2026-08-26 names none of the counterparties in batch 2.
- The filed CoreWeave–NVIDIA order form exhibit. The 10-K lists only the 2023 MSA (as S-4/A Exhibit 10.31).
- Confirmation that the Nscale NVIDIA Sale closed: no Nscale filing after 2026-11-12.
- Evidence of a TuSimple disposal.

## Needs quote (tier 2, fetch returned 403)

- CNBC, 2025-11-13, "AI startup Cursor raises $2.3 billion funding round at $29.3 billion valuation".
- CNBC, 2026-06-16, "SpaceX to buy Cursor AI parent Anysphere for $60 billion".
- CNBC and Axios, 2023-09-14, on Databricks' Series I.

## Note

ev_150043 (SharonAI's commitment of about $4B in hardware) was recorded with the placeholder title "x". The quote is valid, but the title should be read as "SharonAI Form 10-Q quarter ended 2026-09-30".
