# Guarantee sweep: hyperscalers (Meta, Microsoft, Oracle, Amazon, Alphabet/Google)

Prepared 24 November 2026. Evidence namespace `gsh` (ev_240001 to ev_240073). Draft: `research/drafts/complex_hyperscalers.json`
(14 new depth 2 entities, 17 complex links, `python3 -m pipeline.checks draft` returns "All checks passed").
Every figure below is quoted from a tier 1 source: SEC filings, 8-K exhibits, or OpenAI's own release.

## Bottom line

Nvidia is not the only lender of last resort. Google is the second large one. At 30 September 2026 Alphabet reported $75.7 billion
of data center backstop obligations (ev_240032). $48.0 billion of that is executed with third-party data center providers (ev_240033);
$27.7 billion is a commitment to put more backstops in place (ev_240034). Executed backstops were $16,940 million at 31 December 2025.
Meta has given residual value guarantees of $41,493 million to two off-balance-sheet data center ventures (ev_240042). Meta also
backstops unsold Nebius capacity (up to $15 billion, ev_40081), the same tool Nvidia uses with CoreWeave. Amazon and Oracle give
smaller, targeted support. Microsoft gives no guarantees; its role is the contract lenders rely on.

## Links found (newest first within each provider)

| Provider | Beneficiary | Obligor | Kind | Amount | Trigger | Dates | Same capacity as Nvidia | Evidence |
|---|---|---|---|---|---|---|---|---|
| Google | TeraWulf (landlord, project lenders) | Anthropic | credit_support | Headline: about $19 billion of lease commitments (ev_240012, 2026-11-04). Maximum: not stated (cap blank in filed form, ev_240016) | Anthropic payment default or insolvency; Google pays rent and assumes the lease, or pays a termination fee and takes landlord equity | Signed 2026-11-04; in force only when the last data hall of each lease commences (late 2027 to Q2 2028); ends once Anthropic is investment grade for three months | Yes, company level (rel_anthropic_eq_2026, rel_anthropic_eqc_2025). Hardware is Google TPU pods (ev_240015), not Nvidia | ev_240012 to ev_240016, ev_240031 |
| Google | Third-party data center providers (unnamed) | Same | backstop (aggregate) | Headline $75.7 billion (ev_240032); maximum executed $48.0 billion (ev_240033), both at 2026-09-30 | Specified tenant defaults | Terms up to 15 years (ev_240036) | No (aggregate; contains the named links) | ev_240032 to ev_240036 |
| Google | Crux AI (Google and Blackstone venture) | Crux AI | backstop commitment | Up to $10.0 billion (ev_240037); Blackstone up to $5.0 billion capital (ev_240038) | Crux AI signing agreements that call for backstops | Q3 2026; not yet executed | No | ev_240037, ev_240038 |
| Google | TPU buyers and assignees (unnamed) | Same | residual_value_guarantee | Maximum $6.6 billion at 2026-09-30 (ev_240039) | Holder requires Google to repurchase TPUs at preset prices | Multi-year | No | ev_240039, ev_240040 |
| Google | Hut 8 (River Bend) | Fluidstack | backstop | Headline $7.0 billion base-term lease value (ev_240028); maximum not stated | Fluidstack fails to pay rent and certain other obligations | Announced 2025-12-17; 15-year base term. Supports $3.25 billion River Bend Notes (ev_240029) | No (Fluidstack has no Nvidia link in the register) | ev_240027 to ev_240030 |
| Google | Cipher (Barber Lake) | Fluidstack | backstop | Up to $1.73 billion (ev_240018, 2025-11-20); initial $1.4 billion (ev_240017) | Fluidstack payment default or insolvency | Signed 2025-09-24; in force at lease commencement (phased from Q4 2026). Supports $1.4 billion bond (ev_240023) | No | ev_240017 to ev_240019, ev_240023 |
| Cipher | Google | Cipher | share_option_or_warrant | Warrant over 24,178,576 shares (ev_240021); booked at $544.5 million (ev_240022); Cipher tops up if worth under $435.0 million (ev_240020) | Exercisable from lease commencement | Expires 2030-11-20 | No | ev_240020 to ev_240022 |
| Google | Abernathy JV (FS CS I LLC) | Fluidstack | backstop | About $1.3 billion (ev_240008, 2025-10-28) | Fluidstack payment default or insolvency | Recognition agreement 2025-09-26; in force at lease commencement. Supports $1,300.0 million JV notes due 2030 (ev_240010) | No | ev_240008 to ev_240011 |
| Google | TeraWulf (Lake Mariner) | Fluidstack | backstop | About $3.2 billion (ev_240004, 2025-08-18); first $1.8 billion (ev_240003, 2025-08-14) | Fluidstack payment default or insolvency; Google pays the termination fee or pays rent and assumes the lease (ev_240002) | Signed 2025-08-13 and 2025-08-17; one lease commenced by 2026-09-30. Supports $3,200.0 million 2030 Secured Notes (ev_240007) | No | ev_100047, ev_240001 to ev_240004, ev_240007 |
| TeraWulf | Google | TeraWulf | share_option_or_warrant | Warrants over 73,580,000 shares at $0.01 (ev_240006); $515.5 million at issuance (ev_240005); about 14% stake (ev_240004) | Exercisable from lease commencement | Expire August 2030 | No | ev_240004 to ev_240006 |
| Meta | Meta Texas venture (El Paso; co-owner not named) | Same | residual_value_guarantee | Maximum not stated separately; at least $13.4 billion (analysis: $41,493 million combined, ev_240042, less $28,091 million Louisiana, ev_240043) | Meta ends or does not renew a lease when the campus is worth less than the threshold | Venture July 2026; lease starts 2028 | No | ev_240042, ev_240043, ev_240047 to ev_240049 |
| Meta | Nebius | Nebius | backstop (unsold capacity) | Up to $15 billion (ev_40081) | Nebius fails to sell specified GPU capacity to others (ev_240057) | Signed 2026-03-13; five years from deployment | Yes (rel_nebius_eq_2026, rel_nebius_eq_2024) | ev_40079, ev_40081, ev_240057, ev_240054 |
| Meta | Blue Owl fund affiliate (80% owner) | Meta Louisiana venture | residual_value_guarantee | Maximum $28,091 million at 2025-12-31 (ev_240043); threshold about $28 billion, falling over time (ev_240052) | As Texas | Venture October 2025; lease starts 2029, four-year terms renewable to 20 years | No | ev_240043, ev_240046, ev_240048 to ev_240053, ev_240056 |
| Microsoft | IREN GPU Financing 1.0 lenders | IREN | compute_contract | Contract about $9.7 billion (ev_40118); financing commitments $3,645 million (ev_240061) | Microsoft not accepting or paying for capacity | Contract November 2025; draws tied to Microsoft delivery milestones (ev_240060) | Yes, company level (rel_iren_lb_2026, rel_iren_eq_2026) | ev_40118, ev_40131, ev_240059 to ev_240061 |
| Oracle | Unnamed lessor's lenders | Unnamed lessor | guarantee | Up to $3.3 billion at 2026-05-31 (ev_240062); up to $2.2 billion at 2026-02-28 (ev_240063) | Lessor fails to repay | Borrowing matured September 2026; not mentioned in the August 2026 10-Q | No (site not named) | ev_240062 to ev_240064 |
| Amazon | Anthropic | Anthropic | vendor_financing | Up to $20.0 billion (ev_240070); $5.0 billion used (ev_240072); $15.0 billion left (ev_240071) | Anthropic draws as AWS hits compute delivery milestones (ev_240073) | Q2 2026; expires 30 months after an Anthropic IPO | Yes, company level (rel_anthropic_eq_2026, rel_anthropic_eqc_2025). Compute is AWS chips | ev_240070 to ev_240073 |
| Amazon.com, Inc. | Cipher (Black Pearl) | AWS | parent_guarantee | Headline about $5.5 billion contracted revenue (ev_240025); no cap stated | AWS fails to pay base rent or operating expenses | Lease from November 2025; phased delivery from August 2026; supports $2.0 billion bond (ev_240026) | No | ev_240024 to ev_240026 |

The register's context record `rel_google_cx_2025` (ev_100047) is now recorded properly as `cx_google_fluidstack_backstop_2025`.

## Lease commitments not yet commenced (context, not links)

| Company | Amount | As of | Evidence |
|---|---|---|---|
| Microsoft | $364.6 billion, commencing fiscal 2027 to 2034 | 2026-09-30 | ev_240058 |
| Meta | about $355.73 billion, commencing 2026 to 2036 | 2026-09-30 | ev_240055 |
| Oracle | $288 billion, terms of 15 to 19 years | 2026-08-31 | ev_240064 |
| Alphabet | $130.5 billion, commencing 2026 to 2031 | 2026-09-30 | ev_240041 |
| Amazon | $164,922 million in Amazon's commitments table (not recorded as evidence; table only) | 2026-09-30 | not recorded |

## Oracle and OpenAI

Confirmed:
- OpenAI's own release of 23 September 2025 says the Oracle partnership "exceeds $300 billion between the two companies over the next five years" (ev_240067). This is the source for the Bloomberg chart's figure. It is a company-announced headline, not a filed contract value.
- The July 2025 OpenAI release: Oracle and OpenAI agreed to develop 4.5 gigawatts of additional Stargate capacity (ev_240068).
- OpenAI says Oracle began delivering Nvidia GB200 racks at Abilene in June 2025 (ev_240069): the one allowed source that names Nvidia hardware in Oracle's OpenAI capacity.
- Oracle's remaining performance obligations: $638 billion at 31 May 2026 (ev_240065) and $664 billion at 31 August 2026 (ev_100048). Oracle attributes growth to "certain significant cloud contracts" and names no customer.
- Oracle guaranteed up to $3.3 billion of one lessor's borrowing (ev_240062). Oracle does not name the lessor or site.

Not confirmed:
- No Oracle filing (10-K, 10-Qs, 8-Ks, earnings releases read) names OpenAI as a customer or states the contract amount, date or term. Oracle's side is silent; the $300 billion stands on OpenAI's release alone.
- No document ties Oracle's $3.3 billion guarantee, or any Oracle support, to Abilene, Vantage (Port Washington, Wisconsin) or a Crusoe-built site.
- No Oracle guarantee of an OpenAI obligation, or OpenAI credit support to Oracle, was found.
- Oracle's November 2026 debt ($10.0 billion of notes, ev_240066, with a concurrent $10 billion share sale) is for general corporate purposes including capital expenditure; no prospectus read ties it to OpenAI or names Nvidia.

## Same capacity

Places where a hyperscaler and Nvidia both stand behind the same company (register relationship in brackets):

1. **Nebius**: Meta backstops unsold GPU capacity up to $15 billion; Nvidia holds a $2 billion pre-funded warrant and shares (rel_nebius_eq_2026, rel_nebius_eq_2024). Microsoft's Nebius contract (up to about $17.4 billion, ev_40084) has no lender reliance shown.
2. **Anthropic**: Google backstops about $19 billion of Anthropic's Justified leases and Amazon offers a $20.0 billion financing facility; Nvidia bought $10 billion of Anthropic shares and committed up to $10 billion earlier (rel_anthropic_eq_2026, rel_anthropic_eqc_2025). Both hyperscaler supports finance their own chips (TPU, AWS), so the overlap is the company, not the hardware. Anthropic also owes Nscale and Lambda for Nvidia capacity (crossref report).
3. **IREN**: Microsoft's contract is what IREN's $3,645 million GPU financing relies on; Nvidia has a $3.4 billion cloud contract with IREN and an equity link (rel_iren_lb_2026, rel_iren_eq_2026). Different hardware at Childress.
4. **CoreWeave** (not a link: no hyperscaler guarantee): Meta committed up to about $21.0 billion (ev_20103) and Microsoft was 67% of 2025 revenue (ev_20125), beside Nvidia's unsold-capacity order (rel_coreweave_bk_2025).
5. **Nscale** (not a link): Microsoft statements of work up to about $43.8 billion (ev_40027) beside Nvidia's $860 million lease guarantee and other support (rel_nscale_gu_2025 and others).
6. **OpenAI** (not a link): Oracle's capacity for OpenAI runs Nvidia GB200 racks (ev_240069); Nvidia's $105 billion rent guaranty covers a different site, in Ohio (rel_openai_gu_2026).

No case was found where a hyperscaler and Nvidia guarantee the same lease or loan.

## Parties searched with nothing found

- **Microsoft**: 10-Q (2026-09-30) and 10-K (2026-06-30) have no guarantee, backstop or residual value disclosure; purchase commitments (about $194 billion in the 10-K table, not recorded as evidence) are described as open orders and take-or-pay contracts with no counterparty. No credit support in the OpenAI arrangements (equity method, about 24%). Full-text searches for Microsoft backstops of leases returned nothing relevant. Nscale and Nebius filings read show no financing that relies on the Microsoft contracts.
- **Amazon**: no backstop or residual value guarantee in the 10-Q. OpenAI arrangements are $50.0 billion of preferred stock (equity, no credit support).
- **Meta**: no guarantee of CoreWeave or Nebius debt. Meta's 8-Ks of October and November 2026 concern its recapitalization and share offerings.
- **Alphabet**: the $20.0 billion "future capital funding commitments with a private company" (equity derivative, milestones through 2030) is equity funding, not credit support; the company is not named.
- Other bitcoin miners: Core Scientific (only proxy-fight material mentions Google), no other Google backstop filer found beyond TeraWulf, Cipher and Hut 8.

## Needs quote

- The size, coupon and holders of the Beignet Investor LLC notes (Meta Louisiana venture debt). Fund holdings reports confirm the notes exist (6.58% due 2049, ev_240056) but no filing links Beignet to Meta or states the issue size. Tier 2 news was not searched in this sweep; a Bloomberg or Reuters report on the October 2025 bond sale is the lead.

## Domains added

None. All sources were SEC filings or openai.com (already listed).

## Open questions

1. Is Meta's $14.72 billion contingent cloud capacity obligation (ev_240054) the Nebius unsold-capacity order? Timing fits; Meta does not name the provider.
2. Who is the Oracle lessor whose $3.3 billion borrowing Oracle guaranteed, and was it repaid at the September 2026 maturity?
3. Who is the other owner of Meta's Texas venture, and has it issued debt?
4. What is the cap on Google's termination fee at Justified (blank in the filed form)?
5. Does Fluidstack run Nvidia GPUs at Lake Mariner, Barber Lake, Abernathy or River Bend? If so, Google's Fluidstack backstops sit under Nvidia hardware even though Fluidstack has no Nvidia relationship in the register.
6. Pipeline note for the lead: `pipeline.checks draft` copies all register relationships into a complex draft (the draft's relationships list is extended in place). The copies were removed after validation; the complex links are unchanged.
