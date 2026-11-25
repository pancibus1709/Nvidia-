# Scope

**Window.** Relationships announced, filed or reported from 1 January 2023 to today (work began 23 November 2026), plus any older relationship still active, such as long-held equity stakes.

**Anchor entity.** NVIDIA Corporation, CIK 0001045810. Its fiscal year ends on the last Sunday of January, so fiscal 2026 is mostly calendar 2025. Every Nvidia figure records both the fiscal period and the calendar date.

**Exposure types** (spec/05 section 2): EQ direct equity, EQ-SPV vehicle equity, EQ-C conditional equity commitment, BK capacity backstop, LB leaseback or capacity rental, GU guarantee, RV residual value or repurchase, FC financing commitment, LP fund commitment, PP supply prepayment, LI license or acqui-hire (only with a stated reason), CX context.

**Source tiers** (spec/04, enforced by `config/sources_allowlist.json`):
- Tier 1: SEC EDGAR, the company's own releases and calls, regulators and courts, lien registries, rating agency public releases.
- Tier 2: Bloomberg, Reuters, The Wall Street Journal, Financial Times, The Information, CNBC, Barron's, The Economist, Nikkei Asia, Axios.
- Market data: share prices only, for market value only.
- Everything else is excluded.

**Display rule.** A figure is shown only if a tier 1 source or two independent tier 2 sources contain it. Otherwise it reads "Not confirmed".

**Debt documents.** Newest instrument first, fullest prospectus first. See `research/DEBT_DOCUMENT_RULE.md`.

**Depth.** Depth 1 is a direct Nvidia relationship. Depth 2 is a party whose position relies on one. Nothing beyond depth 2 in this release.

**Gate R cutoff.** 25 November 2026. Thomas approved the register in chat on this date ("Go ahead and build the application") and asked that the data be checked against the most recent documents and releases before publishing.

**Defaults applied for the open decisions** (Thomas did not answer them; each is the recommended option and can be changed in config):
- The $105 billion PORTS-Pike guaranty is shown at full value with a "not yet in force" label.
- Paywalled news stays "Not confirmed" until a reviewer pastes the quote.
- Letter grades stay off on the public page (`config/display.json`, `show_grades: false`).
- Groq and Hugging Face stay off the exposure map as purchases.
- The central bank verdict gains the evidence that Google, Broadcom and AMD give the same support for their own products.
- The CoreWeave insolvency termination clause is described as written, with a note that it has not been reviewed by counsel.
