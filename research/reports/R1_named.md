# R1 part B: named relationships and signals in NVIDIA's own filings

Sequence R1b. Evidence namespace `r1b`: ev_50001 to ev_50146 (146 records, `research/evidence/r1b.jsonl`). Machine-readable version: `research/drafts/r1_named.json`. Window 1 Jan 2023 to 23 Nov 2026. CIK 0001045810.

Sources read: 15 Forms 10-K and 10-Q (filed 2023-02-24 to 2026-08-26); all 40 Forms 8-K with every EX-99.1, 99.2 and 99.3; Exhibit 10.1 to the Q2 FY27 10-Q (Form of Residual Value Guaranty, heavily redacted); the June 2026 424B5; 8 ownership filings where NVIDIA is the reporting person; 12 Forms 13F-HR. The four newest periodic filings (Q2 FY27 10-Q, Q1 FY27 10-Q, FY26 10-K, Q3 FY26 10-Q) were read in the sections the brief lists. The Q3 FY27 10-Q (period ended 2026-10-25) was not filed by 23 Nov 2026, so the 8-K of 17 Nov 2026 (CFO commentary and supplemental information) is the newest disclosure.

Fiscal calendar: FY2026 = Jan 27 2025 to Jan 25 2026; Q2 FY27 ended 2026-07-26; Q3 FY27 ended 2026-10-25.
Conventions: "n/s" = not stated in NVIDIA filings. Amounts appear only as far as the source states them, with the source's verb. Type codes per spec/05 section 2. "Type guess" and every "Analysis" line are my classification, not NVIDIA's.

## (a) Named relationships

| # | Counterparty | Type guess | What NVIDIA's filings say (verbatim key wording) | Headline | Committed | Funded | Contingent max | Dates | Binding status | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | SB Energy Corp. (lessor) for 20-year leases to an affiliate of OpenAI Group PBC, PORTS-Pike Technology Campus, Pike County, Ohio | GU (8-K calls them "residual value guaranties"); wrong-way risk specific to OpenAI | "aggregate payment obligation is cumulatively capped at $105 billion"; leases "for approximately 4.25 gigawatts of IT load"; Trigger Event = OpenAI insolvency causing lease default, or "OpenAI's failure to make payments under a lease"; NVIDIA pays the shortfall between the "guaranteed minimum value of a lease" and recoveries from re-letting or sale; "OpenAI has agreed to reimburse and indemnify NVIDIA for any and all amounts"; terminates on OpenAI "achieving a satisfactory credit rating" or the 20th anniversary; option to back "approximately an additional 3.8 gigawatts"; in exchange "the site will exclusively host NVIDIA AI infrastructure, subject to limited exceptions"; "To date, we have not made any payments related to our guarantees." CFO: each generation at the site "could represent ... approximately $150 billion to $200 billion in NVIDIA revenue" | n/s separately | n/s | $0 paid as of 2026-10-25 (ev_50045) | $105B (ev_50032, 8-K 2026-08-17; ev_50039, 10-Q 2026-08-26). All guarantees: $108.5B at Q2 FY27 (ev_50042); $118.0B at 2026-10-25 (ev_50044) | Signed 2026-08-17; effective per building after ready-for-service "expected beginning in 2028" (ev_50036), first in FY2029; up to 20 years (ev_50037) | Definitive (8-K Items 1.01 and 2.03; form filed as Ex. 10.1) | ev_50032 to ev_50046, ev_50048, ev_50049, ev_50128 |
| 2 | SB Energy Corp. (equity) | EQ | "NVIDIA will invest $1.5 billion in SB Energy", joining SoftBank Group and OpenAI | $1.5B, "will invest" (ev_50047, Ex. 99.1, 2026-08-17) | n/s | n/s | - | Announced 2026-08-17 | Announced; closing n/s | ev_50047 |
| 3 | OpenAI (investment) | EQ-C | Q3 FY26 10-Q: "we entered into a letter of intent with an opportunity to invest in OpenAI"; "There is no assurance that we will enter into definitive agreements with respect to the OpenAI opportunity". FY26 10-K: "We are finalizing an investment and partnership agreement with OpenAI." and "There is no assurance that we will enter into an investment and partnership agreement with OpenAI or that a transaction will be completed." Q1 and Q2 FY27 10-Qs: no mention of an OpenAI investment. Q3 FY26 release: "strategic partnership with OpenAI to deploy at least 10 gigawatts of NVIDIA systems" | n/s (no amount in any NVIDIA filing) | n/s | n/s | - | LOI in Q3 FY26 (Jul 28 to Oct 26, 2025); "finalizing" on 2026-02-25 | Letter of intent; later outcome not stated | ev_50050 to ev_50054, ev_50146 |
| 3b | OpenAI (unnamed customer signal) | CX | Q2 FY27 10-Q: "We estimate that one AI research and deployment company contributed a meaningful amount of our revenue by purchasing cloud services from our customers" (company not named) | - | - | - | - | Q2 FY27 | - | ev_50055 |
| 4 | Anthropic | EQ | "In November 2025, we entered into an agreement, subject to certain closing conditions, to invest up to $10 billion in Anthropic." Q4 FY26 release: "Announced an investment and deep technology partnership with Anthropic". Q3 FY26 release: Anthropic "initially adopting 1 gigawatt of compute capacity with NVIDIA Grace Blackwell and Vera Rubin systems". Q3 FY27 release: "Expanded Anthropic's access to NVIDIA Grace Blackwell and Vera Rubin capacity through cloud providers" | "up to $10 billion" (ev_50056, 10-Q filed 2025-11-19) | n/s | n/s | - | Agreement Nov 2025 | Agreement subject to closing conditions; closing n/s | ev_50056 to ev_50060 |
| 5 | Intel Corporation | EQ | "Investment commitments are $6.5 billion as of October 26, 2025, including $5 billion in Intel Corporation which is subject to regulatory approval"; MD&A: "we committed to invest $5 billion in Intel Corporation, subject to regulatory approval"; Q4 FY26 CFO: "gains from our previously announced investment in Intel's common stock". Release: collaboration "to jointly develop multiple generations of custom data center and PC products" | $5B (ev_50063) | $5B at 2025-10-26 (ev_50061) | n/s in dollars; 13F 214,776,632 sh from 2025-12-31 (ev_50020); 161,082,488 sh, $19,366,947,532 at 2026-09-30 (ev_50021) | - | Committed Q3 FY26; held by 2025-12-31; cut in Q3 2026 | Completed | ev_50061 to ev_50065, ev_50020, ev_50021 |
| 6 | Groq, Inc. | LI (a purchase, not exposure to Groq's credit) | "non-exclusive license agreement with Groq, Inc., or Groq, for its language processing unit technology and hired certain Groq employees. No customer contracts, existing products, or equity interests were purchased." "Total consideration consists of $13.0 billion paid at closing and $4 billion, inclusive of imputed interest, payable within one year" | - | $17.0B (sum of two filed figures; analysis) | $13.0B at closing (ev_50066); $2,944M more paid in H1 FY27 (ev_50069) | - | Dec 2025 | Completed | ev_50066 to ev_50069 |
| 7 | CoreWeave, Inc. | EQ | Q1 FY26 10-Q: CoreWeave investment "reclassified from non-marketable equity securities" after IPO; "The fair value of the investment as of April 27, 2025 was $1 billion". 13G: 24,182,460 sh, 7.0% (event 2025-03-31). Form 3 ("10% Owner") and 13G/A: 47,213,353 sh, 11.5% (event 2026-01-23). Q4 FY26 release: "Strengthened a collaboration with CoreWeave to accelerate the buildout of more than 5 gigawatts of AI factories by 2030" | - | - | n/s in dollars; 13F $4,113,227,313 at 2026-09-30 (ev_50019) | - | Pre-IPO stake; doubled by 2026-01-23 | Completed | ev_50070 to ev_50072, ev_50105 to ev_50109, ev_50018, ev_50019 |
| 8 | Nebius Group N.V. | EQ (common plus pre-funded warrant) | 13G: 22,256,412 Class A shares, 9.3%: 1,190,476 shares plus 21,065,936 shares "issuable upon exercise of a pre-funded Class A ordinary share purchase warrant" "acquired by NVIDIA on March 11, 2026 pursuant to a Securities Purchase Agreement"; exercise and sale barred before 2026-09-11 | - | - | n/s (price not stated) | - | SPA 2026-03-11; 13G event 2026-07-13 | Completed | ev_50101 to ev_50104, ev_50014, ev_50015 |
| 9 | Serve Robotics Inc. | FC, then EQ | Form 4: NVIDIA held a "6.00% Convertible Promissory Note" that converted in April 2024 "at a conversion price per share equal to $2.42" into 1,050,129 shares; 62,500 shares "purchased in a private placement" at $4 on 2023-07-31. 13G: 3,727,033 sh, 10.0%. 13G/A: 0.0% at 2024-12-31 | - | - | Note principal n/s | - | Merger 2023-07-31; conversion 2024-04-22; exit by 2024-12-31 | Completed, exited | ev_50110 to ev_50115, ev_50010, ev_50011 |
| 10 | Unnamed AI cloud partners: land, power and shell (facility lease) guarantees | GU | Q3 FY26 10-Q: "an agreement to guarantee a partner's facility lease obligations in the event of their default", a lease "backed by our credit profile, in exchange for issuing us warrants"; "The maximum gross exposure is $860 million"; "The partner has placed $470 million in escrow". FY26 10-K: "The maximum gross exposure under all agreements is $3.5 billion", terms 5 to 7 years, "$712 million in escrow" | - | - | - | $860M at 2025-10-26 (ev_50073); $3.5B at 2026-01-25 (ev_50076), unchanged at 2026-10-25 (ev_50044) | First in Q3 FY26 | Definitive, in force | ev_50073 to ev_50077 |
| 11 | Unnamed AI clouds, renamed "neoclouds" (AI cloud agreements) | BK | "AI clouds procure our data center infrastructure products and we commit to cloud service agreements"; risk factor: "if AI clouds do not successfully sell committed capacity to third-party customers, we have agreed to purchase that capacity"; "Our commitments, which are typically six years in duration, totaled $36 billion"; Q3 FY27: "Our commitments take effect only if the neoclouds secure financing to purchase the data center infrastructure products" | - | $36B at 2026-07-26 (ev_50079) | n/s | $32B at 2026-10-25, contingent on financing and acceptance (ev_50080, ev_50081) | Introduced Q2 FY27 | Definitive, conditional | ev_50078 to ev_50081, ev_50127 |
| 12 | Unnamed partners: power and systems credit support guarantees | GU | Q3 FY27 CFO: "land, power, shell, and hardware financing arrangements, under which we may be required to make payments to third parties if certain of our partners default"; table line "Power and systems credit support guarantees 9.5" | - | - | $0 paid (ev_50045) | $9.5B at 2026-10-25 (ev_50043) | First disclosed 2026-11-17 | In force | ev_50043 to ev_50045 |
| 13 | Apollo, BlackRock, Blackstone, Brookfield, Goldman Sachs, KKR (financing platforms) | RV (optional) / CX | Q2 FY27 release: "strategic partnerships to establish independent compute financing platforms ... to mobilize over $500 billion of third-party capital ... subject to definitive agreements". 10-Q: "These and other preliminary arrangements may not lead to definitive agreements." "At our option, we may provide limited residual-value support for a portion of specific projects" | "over $500 billion" of third-party capital, not NVIDIA's (ev_50083) | n/s | n/s | n/s | MOUs Aug 2026 | Memoranda of understanding | ev_50082 to ev_50085, ev_50129 |
| 14 | Unnamed infrastructure financiers and funds (equity method; some are VIEs) | EQ-SPV / LP | Q1 FY27: "$1.0 billion of investments in infrastructure funds accounted for using the equity method", maximum loss including future commitments "$2.3 billion". Q2 FY27: "$3.3 billion of investments in infrastructure financiers"; VIE "maximum loss exposure, including carrying values and future committed amounts, of $4.7 billion"; NVIDIA is not the primary beneficiary | - | - | $3.3B carrying at 2026-07-26 (ev_50086) | $4.7B VIE max loss (ev_50087) | 2026-04-26 and 2026-07-26 | Completed and committed | ev_50100, ev_50088, ev_50086, ev_50087 |
| 15 | Unnamed investment-grade customers (extended payment terms) | FC | "for investment-grade customer purchases, we have and may in the future provide longer payment terms ranging from 90 days up to one year"; FY26 10-K: "We have not entered into any financing arrangements."; Q2 FY27 10-Q lists "financing arrangements" among arrangements NVIDIA enters | - | - | n/s | - | Q2 FY27 | In force | ev_50137, ev_50131, ev_50121, ev_50122, ev_50125 |
| 16 | Unnamed public companies (warrants, equity forward, convertible debt) | EQ / FC | "Public company warrants $ 4,800" (notional, $M), fair value "$824 million"; "Equity forward contract $ 1,000"; Q3 FY27: "Debt securities convertible into publicly held equity securities" $3,471M | - | - | $3,471M convertible debt at 2026-10-25 (ev_50098) | - | Q2 to Q3 FY27 | Completed | ev_50095 to ev_50098 |
| 17 | Hugging Face, Inc. | LI / CX (acquisition) | "entered into a definitive agreement to acquire Hugging Face, Inc."; "approximately $11.9 billion purchase price" plus retention program up to about $1.0 billion | $11.9B (ev_50089) | n/s | - | - | Signed 2026-09-02; close expected H1 2027 | Definitive, pending | ev_50089, ev_50145 |
| 18 | U.K. AI market (partners named in same bullet: CoreWeave, Microsoft, Nscale) | EQ-C | Q3 FY26 release: "announced an investment of £2 billion in the U.K. market" | GBP 2 billion, not USD (ev_50090) | n/s | n/s | - | By 2025-11-19 | Announced | ev_50090 |
| 19 | Synopsys, Inc. | EQ | 13F 4,821,717 sh first at 2025-12-31; 4,354,077 sh ($1,893,762,250) at 2026-09-30. Release: "expanded strategic partnership with Synopsys". No price or amount in NVIDIA filings | - | - | n/s | - | First 13F 2025-12-31 | Completed | ev_50022, ev_50023, ev_50141 |
| 20 | Nokia Corporation | EQ | 13F 166,389,351 ADS first at 2025-12-31; 72,859,751 ($738,797,875) at 2026-09-30. Release: AI-RAN partnership | - | - | n/s | - | First 13F 2025-12-31; cut in Q3 2026 | Completed | ev_50024, ev_50025, ev_50142 |
| 21 | Coherent Corp. | EQ | 13F 7,788,161 sh first at 2026-03-31 ($2,241,510,617 at 2026-09-30). Q1 FY27 release: "multi-year strategic agreements with Coherent, Corning and Lumentum" | - | - | n/s | - | First 13F 2026-03-31 | Completed | ev_50026, ev_50027, ev_50140 |
| 22 | Space Exploration Technologies Corp. | EQ | 13F Class A: 122,764,805 sh ($20,975,594,582) first at 2026-06-30; 130,472,925 sh ($19,683,145,466) at 2026-09-30. Q2 FY27 release: "SpaceXAI will deploy NVIDIA Vera CPUs". No investment terms in NVIDIA filings | - | - | n/s | - | First 13F 2026-06-30 | Completed | ev_50030, ev_50031, ev_50143 |
| 23 | xAI | CX | Named only as a partner: "Partnered with industry leaders, including Google Cloud, Microsoft, Oracle and xAI" | - | - | - | - | Q3 FY26 | - | ev_50144 |
| 24 | Arm Holdings plc | EQ | 13F: 1,960,784 ADS at 2023-12-31; 1,101,249 from 2024-12-31; exited by 2025-12-31. Q1 FY26 10-Q MD&A: unrealized losses "particularly CoreWeave and Arm, Inc." | - | - | - | - | 2023-12-31 to 2025-09-30 | Exited | ev_50001, ev_50002 |
| 25 | Applied Digital Corp. | EQ | 13F only: 7,716,050 sh 2024-09-30 to 2025-09-30; exited by 2025-12-31 | - | - | - | - | | Exited | ev_50012, ev_50013 |
| 26 | Recursion, WeRide, SoundHound AI, TuSimple, Nano-X | EQ | 13F only; all exited (section e) | - | - | - | - | | Exited | ev_50003 to ev_50009, ev_50016, ev_50017 |
| 27 | Generate Biomedicines | EQ | 13F only: 833,325 sh from 2026-03-31 | - | - | - | - | | Held | ev_50028, ev_50029 |

Aggregates that name no counterparty but frame the rows above (detail is R1a's): equity investments of $99 billion and equity investment commitments of $25 billion at 2026-07-26 (ev_50091, ev_50092); Q1 FY27 investments of "$18.6 billion in private companies and infrastructure funds", which "include AI model makers that may indirectly purchase or use our products in the cloud" (ev_50093, ev_50094); Q3 FY27 equity commitments "focused on frontier labs, infrastructure financiers, and other private companies" (ev_50139); Q3 FY27 impairment of $1.8 billion on non-marketable holdings (ev_50099).

Analysis (my reading, not NVIDIA's words):
- NVIDIA's own statement on customer financing reversed within six months. FY26 10-K (2026-02-25): "We have not entered into any financing arrangements" (ev_50122). Q2 FY27 10-Q (2026-08-26) lists "financial guarantees and other forms of credit support, financing arrangements, and data center leases" among arrangements it enters (ev_50125).
- Named or disclosed guarantee exposure grew from $0.86B (Oct 2025) to $3.5B (Jan 2026) to $118.0B (Oct 2026); $105B of it rests on one tenant (OpenAI) at one site, with OpenAI also the indemnitor.
- The Nebius pre-funded warrant (bought 2026-03-11, in Q1 FY27) is not the "public company warrants" NVIDIA says it received in Q2 FY27; the issuers behind the $4.8B notional are not named.
- OpenAI equity: NVIDIA filings never state an amount. The last status is "finalizing" (Feb 2026); later 10-Qs are silent. The only signed OpenAI-linked exposure in NVIDIA filings is the SB Energy guarantee.

## (b) Risk factor and disclosure signals, by the filing where each first appears

Method: the risk factor section of each of the 15 10-K/10-Qs since Feb 2023 was split into sentences; a sentence counts as new only if absent from every earlier filing in the window. `pipeline.extract riskdiff` was also run for each consecutive pair from the FY25 10-K onward; for 10-Qs that tool takes the table-of-contents hit as the section start and sweeps in the whole filing, so the first-appearance list below uses a corrected section boundary. Keyword filter: invest, customer, financ, capacity, collect, credit, lease, guarantee, circular, partner, demand, debt, fund.

| First filing | New sentence (summary) | Verbatim anchor | Evidence |
|---|---|---|---|
| FY24 10-K (2024-02-21), baseline already present at window start | Extended payment terms, customers unable to pay, credit insurance, bad debt | "our ability to obtain credit insurance for customers with extended payment terms" | ev_50135 |
| FY24 10-K, baseline | Regulators request information on investments in foundation model companies | "partnerships and other agreements with companies developing foundation models" | ev_50136 |
| FY25 10-K (2025-02-26) | No substantive new sentence on investments or customer financing (flagged sentences are reflowed FY24 text and updated customer concentration figures) | - | - |
| Q1 FY26 10-Q (2025-05-28) | Announced purchase intentions often non-binding | "as such announcements are often non-binding and may not result in committed volumes" | ev_50134 |
| Q2 FY26 10-Q (2025-08-27) | Investments in public and private companies create volatility | "Our investments in publicly traded and private companies could create volatility" | ev_50138 |
| Q3 FY26 10-Q (2025-11-19) | Customers' access to capital is constrained | "access to capital can be particularly constrained for less-capitalized companies" | ev_50118 |
| Q3 FY26 10-Q | OpenAI letter of intent; no assurance of definitive agreements | "we will enter into definitive agreements with respect to the OpenAI opportunity" | ev_50051 |
| Q3 FY26 10-Q | Anthropic agreement up to $10B | "to invest up to $10 billion in Anthropic" | ev_50056 |
| Q3 FY26 10-Q | Investment timing depends on partners' deployment of AI infrastructure | "including the ability of our partners to successfully develop and deploy AI infrastructure" | ev_50120 |
| Q3 FY26 10-Q | Investments limited by NVIDIA's own liquidity | "we may be limited by our available liquidity and capital resources" | ev_50119 |
| Q3 FY26 10-Q | Obligations under guarantees and commercial commitments | "We may be required to satisfy financial obligations under guarantees and other commercial commitments." | ev_50116 |
| Q3 FY26 10-Q | Capacity purchase obligations and financial guarantees for customers | "including long-term capacity purchase obligations and financial guarantees supporting our customers" | ev_50117 |
| FY26 10-K (2026-02-25) | OpenAI agreement being finalized; no assurance | "We are finalizing an investment and partnership agreement with OpenAI." | ev_50052, ev_50053 |
| FY26 10-K | Investees may never be profitable | "these companies may not achieve profitability in the near term, or at all" | ev_50124 |
| FY26 10-K | Asked to provide customer financing | "and have been asked to offer financing arrangements to support our customers" | ev_50121 |
| FY26 10-K | No financing arrangements entered | "We have not entered into any financing arrangements." | ev_50122 |
| FY26 10-K | Financing would cut upfront cash and raise credit risk | "Financing arrangements, if undertaken, may in some circumstances result in lower upfront cash flows" | ev_50123 |
| FY26 10-K | Groq licence required large nonrefundable payments | "required significant, nonrefundable payments" | (amounts: ev_50066) |
| Q1 FY27 10-Q (2026-05-20) | No new investment or financing sentences (new text is export control and competition) | - | - |
| Q2 FY27 10-Q (2026-08-26) | NVIDIA now enters guarantees, credit support, financing arrangements, data center leases | "financial guarantees and other forms of credit support, financing arrangements, and data center leases" | ev_50125 |
| Q2 FY27 10-Q | Demand depends on customers' ability to earn revenue and keep investing | "Future demand may be affected by the ability of customers and partners" | ev_50126 |
| Q2 FY27 10-Q | Extended terms for investment-grade customers | "Financing arrangements with certain investment-grade customers, including extended payment terms" | ev_50131 |
| Q2 FY27 10-Q | Agreed to buy capacity that AI clouds cannot sell | "if AI clouds do not successfully sell committed capacity to third-party customers" | ev_50078 |
| Q2 FY27 10-Q | May be unable to use or resell committed capacity | "We may not have sufficient demand for, or the operational ability to use" | ev_50127 |
| Q2 FY27 10-Q | OpenAI default or insolvency triggers SB Energy guarantees; NVIDIA may assume leases | "If OpenAI does not perform its obligations or becomes subject to an insolvency event" | ev_50049 |
| Q2 FY27 10-Q | OpenAI indemnity may not be recovered promptly or in full | "Although OpenAI has agreed to reimburse and indemnify us for certain losses" | ev_50128 |
| Q2 FY27 10-Q | Memoranda with capital providers; may not become definitive | "we entered into memoranda of understanding with large capital providers" | ev_50129 |
| Q2 FY27 10-Q | Data center leases to be assigned to third parties | "We intend to assign certain data center leases to third parties." | ev_50130 |
| Q2 FY27 10-Q (MD&A, not a risk factor) | AI clouds and model makers lack investment-grade financing capacity | "currently lack the ability to secure long-term infrastructure contracts and investment-grade financing capacity" | ev_50132 |
| Q2 FY27 CFO commentary (8-K 2026-08-26) | Customers growing faster than their balance sheets | "many are growing faster than their balance sheets and long-term credit profiles can support" | ev_50133 |

The Q2 FY27 10-Q also added, without an evidence record here: "SB Energy may not complete or deliver the infrastructure as expected or on schedule" and a new indebtedness risk factor ($33.5 billion of senior notes, $25.0 billion commercial paper programme).

## (c) Forms 8-K in the window (40)

| Filed | Event date | Accession | Items | Content relevant to investments, commitments, financing | Evidence |
|---|---|---|---|---|---|
| 2026-11-17 | 2026-11-17 | 0001045810-26-000088 | 2.02,9.01 | Q3 FY27 results (EX-99.1 PR, EX-99.2 CFO commentary, EX-99.3 supplemental). Commitments table: supply $390B, cloud $28B, DC leases not commenced $74B, equity investments $20B; neocloud agreements $32B contingent on neoclouds securing financing; guarantees max $118.0B incl. new $9.5B power and systems credit support; no guarantee payments to date; impairment $1.8B on private investments; convertible debt of a public company $3,471M; pending Hugging Face acquisition; independent board committee investigation referenced. | ev_50080, ev_50081, ev_50043, ev_50044, ev_50045, ev_50139, ev_50099, ev_50098, ev_50060 |
| 2026-11-12 | 2026-11-11 | 0001045810-26-000082 | 5.02,9.01 | CEO transition: Jensen Huang resigned 2026-11-11; Colette Kress interim CEO; Harvey Jones chair. No financing content. | - |
| 2026-09-03 | 2026-09-02 | 0001045810-26-000078 | 8.01 | Definitive agreement to acquire Hugging Face (~$11.9B + up to ~$1.0B retention), closing expected H1 2027; supplemental risk factor. | ev_50145, ev_50089 |
| 2026-08-26 | 2026-08-26 | 0001045810-26-000073 | 2.02,9.01 | Q2 FY27 results. PR: financing platform MOUs with Apollo, BlackRock, Blackstone, Brookfield, Goldman Sachs, KKR (>$500B third-party capital, subject to definitive agreements); SB Energy partnership. CFO: AI cloud agreements $36B, DC leases for third parties $20B, SB Energy guarantees $105B, each PORTS-Pike generation ~$150-200B Nvidia revenue; AI clouds/model makers 'growing faster than their balance sheets'. | ev_50082, ev_50083, ev_50046, ev_50133, ev_50143 |
| 2026-08-17 | 2026-08-17 | 0001045810-26-000069 | 1.01,2.03,7.01 | Items 1.01, 2.03, 7.01: residual value guaranties with SB Energy for OpenAI-leased PORTS-Pike site, capped $105B; EX-99.1 press release: Nvidia to invest $1.5B in SB Energy. | ev_50032, ev_50038, ev_50035, ev_50047 |
| 2026-07-02 | 2026-06-28 | 0001045810-26-000060 | 5.02 | Item 5.02: EVP Worldwide Field Operations retirement. No financing content. | - |
| 2026-06-30 | 2026-06-24 | 0001045810-26-000056 | 5.07 | Item 5.07: annual meeting vote results. No financing content. | - |
| 2026-06-18 | 2026-06-15 | 0001193125-26-275783 | 8.01,9.01 | Item 8.01: completion of $25.0B senior notes offering (seven tranches); exhibits underwriting agreement, officers' certificate, opinion. Use of proceeds general corporate purposes (424B5). | - |
| 2026-05-20 | 2026-05-20 | 0001045810-26-000051 | 2.02,9.01 | Q1 FY27 results. Supply commitments $119B, multi-year cloud service $30B; outlays for strategic investments; strategic agreements with Coherent, Corning, Lumentum; Marvell partnership. | ev_50140 |
| 2026-05-08 | 2026-05-07 | 0001045810-26-000028 | 5.02 | Item 5.02: new director appointed. No financing content. | - |
| 2026-04-27 | 2026-04-24 | 0001045810-26-000026 | 5.02 | Item 5.02: Chief Accounting Officer retirement. No financing content. | - |
| 2026-03-06 | 2026-03-02 | 0001045810-26-000024 | 5.02,9.01 | Items 5.02/9.01: FY27 variable compensation plan. No financing content. | - |
| 2026-02-25 | 2026-02-25 | 0001045810-26-000019 | 2.02,9.01 | Q4 FY26 results. PR: investment and deep technology partnership with Anthropic; Groq non-exclusive license; CoreWeave 5 GW collaboration; Synopsys partnership; Meta partnership. CFO: gains from Intel investment; outlays for IP license and strategic investments. | ev_50058, ev_50072, ev_50141, ev_50064 |
| 2026-01-23 | 2026-01-20 | 0001045810-26-000003 | 5.02 | Item 5.02: director resignation. No financing content. | - |
| 2025-11-19 | 2025-11-19 | 0001045810-25-000228 | 2.02,9.01 | Q3 FY26 results. PR: OpenAI strategic partnership (at least 10 GW); Anthropic 1 GW adoption; Intel collaboration; Nokia AI-RAN partnership; xAI named as infrastructure partner; £2B UK investment with CoreWeave, Microsoft, Nscale. | ev_50054, ev_50059, ev_50065, ev_50142, ev_50144, ev_50090 |
| 2025-08-27 | 2025-08-27 | 0001045810-25-000207 | 2.02,9.01 | Q2 FY26 results. Partnership mentions only (OpenAI open models). No investment amounts. | - |
| 2025-08-05 | 2025-07-31 | 0001045810-25-000197 | 5.02 | Item 5.02: director resignation. No financing content. | - |
| 2025-07-01 | 2025-06-25 | 0001045810-25-000179 | 5.07 | Item 5.07: annual meeting votes. | - |
| 2025-05-28 | 2025-05-28 | 0001045810-25-000115 | 2.02,9.01 | Q1 FY26 results incl. H20 $4.5B charge; Stargate UAE partner mention. No investment amounts. | - |
| 2025-04-15 | 2025-04-09 | 0001045810-25-000082 | 8.01 | Item 8.01: USG H20 export license requirement. No financing content. | - |
| 2025-03-07 | 2025-03-03 | 0001045810-25-000039 | 5.02 | Item 5.02: FY26 variable compensation plan. | - |
| 2025-02-26 | 2025-02-26 | 0001045810-25-000021 | 2.02,9.01 | Q4 FY25 results; Stargate 'key technology partner' mention. No investment amounts. | - |
| 2025-01-17 | 2025-01-13 | 0001045810-25-000007 | 8.01 | Item 8.01: AI Diffusion export rule. No financing content. | - |
| 2024-11-20 | 2024-11-20 | 0001045810-24-000315 | 2.02,9.01 | Q3 FY25 results; CoreWeave/xAI named as customers/partners only. | - |
| 2024-11-07 | 2024-11-07 | 0001045810-24-000300 | 5.02 | Item 5.02: director appointment. | - |
| 2024-08-28 | 2024-08-28 | 0001045810-24-000262 | 2.02,9.01 | Q2 FY25 results; CoreWeave named as H200 cloud provider only. | - |
| 2024-07-02 | 2024-06-26 | 0001045810-24-000206 | 5.07 | Item 5.07: annual meeting votes. | - |
| 2024-06-07 | 2024-06-07 | 0001045810-24-000144 | 5.03 | Item 5.03: charter amendment (stock split authorisation). | - |
| 2024-05-22 | 2024-05-22 | 0001045810-24-000113 | 2.02,8.01,9.01 | Q1 FY25 results; Item 8.01 ten-for-one stock split and dividend. No investment amounts. | - |
| 2024-03-14 | 2024-03-08 | 0001045810-24-000069 | 5.02,5.03,9.01 | Items 5.02/5.03: FY25 variable comp plan, bylaws. | - |
| 2024-02-21 | 2024-02-21 | 0001045810-24-000028 | 2.02,9.01 | Q4 FY24 results. No named investments. | - |
| 2023-11-21 | 2023-11-21 | 0001045810-23-000225 | 2.02,9.01 | Q3 FY24 results. No named investments. | - |
| 2023-10-24 | 2023-10-23 | 0001045810-23-000221 | 8.01 | Item 8.01: export rule effective immediately (A100/H100 etc.). | - |
| 2023-10-17 | 2023-10-17 | 0001045810-23-000217 | 8.01 | Item 8.01: October 2023 export control interim final rule. | - |
| 2023-08-23 | 2023-08-23 | 0001045810-23-000171 | 2.02,9.01 | Q2 FY24 results; partnership mentions (VMware, Snowflake etc.). No investment amounts. | - |
| 2023-07-24 | 2023-07-24 | 0001045810-23-000164 | 5.02 | Item 5.02: director appointment. | - |
| 2023-06-27 | 2023-06-22 | 0001045810-23-000146 | 5.07 | Item 5.07: annual meeting votes. | - |
| 2023-05-24 | 2023-05-24 | 0001045810-23-000087 | 2.02,9.01 | Q1 FY24 results. No named investments. | - |
| 2023-03-08 | 2023-03-02 | 0001045810-23-000039 | 5.02,5.03,9.01 | Items 5.02/5.03: FY24 variable comp, bylaws. | - |
| 2023-02-22 | 2023-02-22 | 0001045810-23-000014 | 2.02,9.01 | Q4 FY23 results. No named investments. | - |

Not read in full: none relevant were skipped. Items 5.02, 5.03 and 5.07 filings were checked for their item text only. The 2026-06-18 notes 8-K was cross-checked against the 424B5 (use of proceeds "general corporate purposes, including the repayment and refinancing of outstanding notes").

## (d) Ownership filings where NVIDIA is the reporting person

Method: every Form 3, 4, 5, SC 13G/13D and SCHEDULE 13G/13D in NVIDIA's submissions list since 2023-01-01 (269 under NVIDIA's own accession prefix, 141 under agent prefixes) was checked against its SEC header. Only 8 have NVIDIA as reporting person or filer; the rest are insiders' filings about NVIDIA stock or other holders' 13G filings on NVIDIA (Vanguard, BlackRock, FMR). No Schedule 13D, no Form 4 for CoreWeave or Nebius, no Form D, NT or other unusual NVIDIA-as-investor form was found. NVIDIA's own S-3 (2023), S-3ASR (2025), 424B5 and FWP (June 2026, $25.0B notes) and N-PX (2025, 2026) are its own securities or proxy votes, not stakes.

| Filed | Form | Accession | Subject company | Event date | Shares | % of class | What it implies | Evidence |
|---|---|---|---|---|---|---|---|---|
| 2024-07-18 | 3 | 0001045810-24-000231 | Serve Robotics Inc. | 2023-07-31 | 2,614,404 | n/s | 10% owner on SPAC merger (shares for pre-merger stock) | ev_50112 |
| 2024-07-18 | 4 | 0001045810-24-000232 | Serve Robotics Inc. | 2023-07-31; 2024-04-22 | +62,500 at $4; +1,050,129 at $2.42; total 3,727,033 | n/s | Increase: private placement and conversion of NVIDIA's 6.00% convertible promissory note | ev_50113, ev_50114, ev_50115 |
| 2024-07-18 | SC 13G | 0001045810-24-000230 | Serve Robotics Inc. | 2023-07-31 | 3,727,033 | 10.0% | Passive 13G (late filing for 2023 event) | ev_50110 |
| 2025-02-14 | SCHEDULE 13G/A | 0001045810-25-000014 | Serve Robotics Inc. | 2024-12-31 | 0 | 0.0% | Exit | ev_50111 |
| 2025-05-15 | SCHEDULE 13G | 0001045810-25-000103 | CoreWeave, Inc. | 2025-03-31 | 24,182,460 | 7.0% | New reportable stake after IPO | ev_50105, ev_50106 |
| 2026-01-26 | 3 | 0001045810-26-000007 | CoreWeave, Inc. | 2026-01-23 | 47,213,353 | n/s ("10% Owner") | Became Section 16 insider (increase) | ev_50109 |
| 2026-01-26 | SCHEDULE 13G/A | 0001045810-26-000008 | CoreWeave, Inc. | 2026-01-23 | 47,213,353 | 11.5% | Increase from 24.3M to 47.2M shares | ev_50107, ev_50108 |
| 2026-07-20 | SCHEDULE 13G | 0001045810-26-000062 | Nebius Group N.V. | 2026-07-13 | 22,256,412 (1,190,476 shares plus 21,065,936 via pre-funded warrant bought 2026-03-11 under an SPA) | 9.3% | New reportable stake, mostly warrant | ev_50101 to ev_50104 |

Analysis: NVIDIA's later stakes in Intel (about 214.8M shares), SpaceX (130.5M), Nokia (166.4M) and Synopsys (4.8M) generated no 13G or Form 3 from NVIDIA. Whether that is because each is below 5% of class was not checked against share counts outstanding.

## (e) 13F-HR position history (shares and reported value in dollars, per quarter)

Values are as reported in each information table (dollars, not thousands). Evidence was recorded against the SEC-rendered information table (`xslForm13F_X02/information_table.xml`) of the same filing, because the raw XML text in `cache_path` runs all fields together and the value cannot be grounded as a separate number. The 13F covers only US-listed 13(f) securities: it omits private stakes, warrants (Nebius warrant), convertible notes and non-US listings.

| Issuer (CUSIP) | 23-12 | 24-03 | 24-06 | 24-09 | 24-12 | 25-03 | 25-06 | 25-09 | 25-12 | 26-03 | 26-06 | 26-09 | First / latest evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ARM HOLDINGS PLC (042068205) | 1.96M sh / $147M | 1.96M sh / $245M | 1.96M sh / $321M | 1.96M sh / $280M | 1.10M sh / $136M | 1.10M sh / $118M | 1.10M sh / $178M | 1.10M sh / $156M | - | - | - | - | ev_50001 / ev_50002 |
| RECURSION PHARMACEUTICALS IN (75629V104) | 7.71M sh / $76M | 7.71M sh / $77M | 7.71M sh / $58M | 7.71M sh / $51M | 7.71M sh / $52M | 7.71M sh / $41M | 7.71M sh / $39M | 7.71M sh / $38M | - | - | - | - | ev_50003 / ev_50004 |
| SOUNDHOUND AI INC (836100107) | 1.73M sh / $4M | 1.73M sh / $10M | 1.73M sh / $7M | 1.73M sh / $8M | - | - | - | - | - | - | - | - | ev_50005 / ev_50006 |
| TUSIMPLE HLDGS INC (90089L108) | 3.47M sh / $3M | - | - | - | - | - | - | - | - | - | - | - | ev_50007 / ev_50007 |
| NANO X IMAGING LTD (M70700105) | 0.06M sh / $0M | 0.06M sh / $1M | 0.06M sh / $0M | 0.06M sh / $0M | - | - | - | - | - | - | - | - | ev_50008 / ev_50009 |
| SERVE ROBOTICS INC (81758H106) | - | - | 3.73M sh / $7M | 3.73M sh / $30M | - | - | - | - | - | - | - | - | ev_50010 / ev_50011 |
| APPLIED DIGITAL CORP (038169207) | - | - | - | 7.72M sh / $64M | 7.72M sh / $59M | 7.72M sh / $43M | 7.72M sh / $78M | 7.72M sh / $177M | - | - | - | - | ev_50012 / ev_50013 |
| NEBIUS GROUP N.V. (N97284108) | - | - | - | - | 1.19M sh / $33M | 1.19M sh / $25M | 1.19M sh / $66M | 1.19M sh / $134M | 1.19M sh / $100M | 1.19M sh / $124M | 1.19M sh / $329M | 1.19M sh / $281M | ev_50014 / ev_50015 |
| WERIDE INC (950915108) | - | - | - | - | 1.74M sh / $25M | 1.74M sh / $24M | 1.74M sh / $14M | 1.74M sh / $17M | - | - | - | - | ev_50016 / ev_50017 |
| COREWEAVE INC (21873S108) | - | - | - | - | - | 24.18M sh / $897M | 24.28M sh / $3,959M | 24.28M sh / $3,322M | 24.28M sh / $1,739M | 47.21M sh / $3,658M | 47.21M sh / $4,700M | 47.21M sh / $4,113M | ev_50018 / ev_50019 |
| INTEL CORP (458140100) | - | - | - | - | - | - | - | - | 214.78M sh / $7,925M | 214.78M sh / $9,478M | 214.78M sh / $29,989M | 161.08M sh / $19,367M | ev_50020 / ev_50021 |
| SYNOPSYS INC (871607107) | - | - | - | - | - | - | - | - | 4.82M sh / $2,265M | 4.82M sh / $1,912M | 4.82M sh / $2,151M | 4.35M sh / $1,894M | ev_50022 / ev_50023 |
| NOKIA CORP (654902204) | - | - | - | - | - | - | - | - | 166.39M sh / $1,077M | 166.39M sh / $1,338M | 166.39M sh / $2,210M | 72.86M sh / $739M | ev_50024 / ev_50025 |
| COHERENT CORP (19247G107) | - | - | - | - | - | - | - | - | - | 7.79M sh / $1,855M | 7.79M sh / $3,072M | 7.79M sh / $2,242M | ev_50026 / ev_50027 |
| GENERATE BIOMEDICINES INC (370920100) | - | - | - | - | - | - | - | - | - | 0.83M sh / $10M | 0.83M sh / $14M | 0.83M sh / $13M | ev_50028 / ev_50029 |
| SPACE EXPLORATION TECHN CORP (84615Q103) | - | - | - | - | - | - | - | - | - | - | 122.76M sh / $20,976M | 130.47M sh / $19,683M | ev_50030 / ev_50031 |

Totals (reported value): 2023-12-31 $0.23B; 2024-03-31 $0.33B; 2024-06-30 $0.39B; 2024-09-30 $0.43B; 2024-12-31 $0.30B; 2025-03-31 $1.15B; 2025-06-30 $4.33B; 2025-09-30 $3.84B; 2025-12-31 $13.10B; 2026-03-31 $18.37B; 2026-06-30 $63.44B; 2026-09-30 $48.33B

Events (entry, change, exit):

| Report date | Event | Shares | Evidence |
|---|---|---|---|
| 2023-12-31 | First 13F in window: Arm, Recursion, SoundHound, TuSimple, Nano-X held | see table | ev_50001, ev_50003, ev_50005, ev_50007, ev_50008 |
| 2024-03-31 | Exit TuSimple | 3,465,372 to 0 | ev_50007 |
| 2024-06-30 | New: Serve Robotics | 3,727,033 | ev_50010 |
| 2024-09-30 | New: Applied Digital | 7,716,050 | ev_50012 |
| 2024-12-31 | New: Nebius, WeRide. Exit: Serve, SoundHound, Nano-X. Arm cut | Arm 1,960,784 to 1,101,249 | ev_50014, ev_50016, ev_50011, ev_50006, ev_50009 |
| 2025-03-31 | New: CoreWeave (after IPO) | 24,182,460 | ev_50018 |
| 2025-06-30 | CoreWeave small increase | 24,182,460 to 24,277,573 | (nvda_13f.json) |
| 2025-12-31 | New: Intel, Synopsys, Nokia. Exit: Applied Digital, Arm, Recursion, WeRide | Intel 214,776,632; Synopsys 4,821,717; Nokia 166,389,351 | ev_50020, ev_50022, ev_50024, ev_50013, ev_50002, ev_50004, ev_50017 |
| 2026-03-31 | New: Coherent, Generate Biomedicines. CoreWeave nearly doubled | CoreWeave 24,277,573 to 47,213,353 | ev_50026, ev_50028, ev_50019 |
| 2026-06-30 | New: Space Exploration Technologies Corp. | 122,764,805 | ev_50030 |
| 2026-09-30 | SpaceX up; Intel, Nokia, Synopsys cut | SpaceX to 130,472,925; Intel to 161,082,488; Nokia to 72,859,751; Synopsys to 4,354,077 | ev_50031, ev_50021, ev_50025, ev_50023 |

Total reported 13F value went from $0.23B (2023-12-31) to $63.44B (2026-06-30) and $48.33B (2026-09-30).

## (f) Closing sections

### Seed hypotheses checked against NVIDIA filings (filings only; other sequences may find more)

| Seed | Result in NVIDIA filings |
|---|---|
| A1 OpenAI up to $100B LOI | LOI "with an opportunity to invest" confirmed (ev_50050); 10 GW partnership confirmed (ev_50054); the $100B figure and any tranche structure: not found in Nvidia filings. Definitive agreement: not found (FY26 10-K says "finalizing"). |
| A2 Anthropic up to $10B; Microsoft $5B; Azure $30B | "up to $10 billion" agreement subject to closing conditions confirmed (ev_50056); 1 GW adoption confirmed (ev_50059); Microsoft amount and Azure $30B: not found in Nvidia filings. Funded amount: not found. |
| A3 xAI SPV up to $2B | Not found in Nvidia filings (xAI named only as partner, ev_50144). |
| A4 Mistral, A5 Reflection, A6 Poolside | Not found in Nvidia filings (Mistral appears only as a model NVIDIA optimised). |
| A7 other labs | Not named in Nvidia filings; only unnamed "AI model makers" and "frontier labs" (ev_50094, ev_50139). |
| B1 CoreWeave stake | Confirmed and quantified (shares) by 13G, 13G/A, Form 3, 13F. |
| B2 CoreWeave $6.3B unsold-capacity order | Not found by name. NVIDIA discloses unnamed AI cloud agreements of this shape ($36B, ev_50079). |
| B3 CoreWeave $1.3B rental | Not found by name. |
| B4 CoreWeave additional ~$2B equity (2026) | Share count doubled to 47,213,353 by 2026-01-23 (ev_50107); the dollar amount: not found in Nvidia filings. |
| B5 Lambda leaseback | Not found in Nvidia filings. |
| B6 Nebius | Confirmed: 1,190,476 shares plus pre-funded warrant for 21,065,936 shares (ev_50101 to ev_50104). Price: not found. |
| B7 Crusoe, B8 Nscale | Not found as investments (Nscale named only as UK partner, ev_50090). |
| B9 Applied Digital | Held 2024-09-30 to 2025-09-30, exited by 2025-12-31 (ev_50012, ev_50013). |
| C1 Intel $5B at about $23.28 | $5B commitment confirmed (ev_50061); 214,776,632 shares in 13F (ev_50020); price per share: not found in Nvidia filings. |
| C2 Nokia $1B at about $6.01 | 166,389,351 ADS in 13F (ev_50024); amount and price: not found in Nvidia filings. |
| C3 Synopsys $2B | 4,821,717 shares in 13F (ev_50022); amount: not found in Nvidia filings. |
| C4 Groq about $20B | Licence: $13.0B paid at closing plus $4B within one year (ev_50066, ev_50067); no equity. "$20B" not found. |
| C5 Arm | 13F holding, exited by 2025-12-31 (ev_50001, ev_50002). |
| E1 Stargate | NVIDIA named as "key technology partner" only (Q4 FY25 release); no capital found. |

### Not found
- Named counterparties for: the unnamed facility lease guarantees ($3.5B), AI cloud or neocloud agreements ($36B / $32B), power and systems credit support guarantees ($9.5B), infrastructure financier equity-method stakes, public company warrants ($4.8B notional), the equity forward ($1.0B), the convertible debt ($3,471M) and the "frontier labs" equity commitments. Searched all 10-K/10-Q notes, MD&A, risk factors, 8-K exhibits.
- Any NVIDIA statement that the OpenAI investment agreement was signed, its amount, or its termination.
- Anthropic closing or funded amount.
- Purchase prices for Intel, Nokia, Synopsys, Coherent, SpaceX, Nebius and CoreWeave stakes.
- Grep hits for Lambda, Crusoe, Nscale, Mistral, xAI, SpaceX (by those names), "backstop", "note receivable", "special purpose", "letter of intent" (other than OpenAI) in any 10-K/10-Q: none.
- Related-party transactions: no related-party note concerning investees in the 10-K/10-Qs (DEF 14A not read).

### Unconfirmed
None added. All claims above are from NVIDIA's own SEC filings.

### Needs quote
None (no paywalled sources used).

### Domains to add
None needed for this work (all sources on sec.gov).

### Open questions
1. Which neoclouds hold the $36B (Jul 2026) / $32B (Oct 2026) AI cloud agreements and the $3.5B facility lease guarantees (with warrants)? R2 counterparty filings (CoreWeave, Nebius, IREN, Lambda) should be searched for the matching agreements.
2. What is behind the new $9.5B "power and systems credit support guarantees" first shown on 2026-11-17, and the Q3 FY27 release bullet "Partnered with Firebird to scale the company's total potential AI infrastructure capacity"? Check the Q3 FY27 10-Q when filed.
3. Did the OpenAI investment agreement close, change or lapse after Feb 2026? The Q1 and Q2 FY27 10-Qs are silent. The "AI research and deployment company" that "contributed a meaningful amount of our revenue" is unnamed.
4. Which issuers granted the $4.8B notional public company warrants (Q2 FY27) and the $3,471M convertible debt (Q3 FY27)?
5. The Q3 FY27 press release mentions an "independent committee" investigation and the CEO's resignation (8-K 2026-11-12); the subject of the investigation is not stated in the filings read. It may bear on disclosure of these arrangements.
6. Whether NVIDIA's Intel, SpaceX, Nokia and Synopsys stakes stayed below the 5% 13G threshold (no NVIDIA 13G was filed).
