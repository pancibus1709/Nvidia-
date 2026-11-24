# Brief: guarantees and credit support across the AI complex (24 November 2026)

**Question for the app:** is Nvidia the only lender of last resort for AI capacity, or one of several? To answer it, map
who else guarantees, backstops or credit-supports the leases, loans and compute contracts in the AI buildout, and whether
that support sits on the same capacity Nvidia supports.

**Read first, in order:** research/AGENT_GUIDE.md (with its Update sections), research/DRAFT_GUIDE.md (especially the last
section, "Guarantees and credit support between other parties"), research/DEBT_DOCUMENT_RULE.md, spec/04_SOURCE_POLICY.md,
research/reports/CROSSREF_bloomberg_money_machine.md and research/reports/CROSSREF_tri_polar_map.md.

**What counts:** a party other than Nvidia that guarantees, backstops, provides residual value support for, credit-supports,
vendor-finances, or gives minimum-revenue or take-or-pay protection on another party's obligation in the AI data center,
GPU or compute chain. Also record share options or warrants granted to win a compute customer (for example AMD's to OpenAI),
as kind `share_option_or_warrant`. Ordinary purchase contracts are recorded only when they are the collateral a lender relies
on (kind `compute_contract`), and only above $1 billion.

**Method:** SEC filings first, newest and fullest document first: 10-K and 10-Q notes on guarantees, commitments,
variable interest entities and leases; 8-K Item 1.01 and 2.03 and their exhibits (guaranty agreements, credit agreements,
lease guaranties); 424B prospectuses. Use EDGAR full-text search per party, for example
`python3 -m pipeline.edgar search '"Fluidstack" "backstop"' --start 2024-01-01 --end 2026-11-24` and variants with
guarantee, guaranty, residual value, credit support, parent guarantee, take-or-pay, minimum commitment.
Then the company's own releases (add its corporate domain to the allowlist per the guide). Tier 2 news only as a lead to a
primary document: no figure enters on one news source.

**Rules that matter most here:** no figure from memory; a quote of at most 14 words grounded in the cached source; headline,
maximum and drawn amounts never merged; set `same_capacity_as_nvidia` and `nvidia_links` only when a document shows the same
site, contract or company carries an Nvidia relationship in data/register/relationships.json; plain English; no em or en
dashes; no hype words.

**Output per agent:** `research/drafts/complex_<topic>.json` validated with `python3 -m pipeline.checks draft <file>` until
"All checks passed", and `research/reports/GS_<topic>.md` with: a table of every link found (provider, beneficiary, obligor,
kind, maximum, trigger, dates, same capacity as Nvidia yes or no, evidence ids), the parties searched with nothing found,
"Needs quote" (paywalled leads), "Domains added", and open questions. Final reply under 200 words.
