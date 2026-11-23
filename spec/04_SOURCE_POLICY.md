# 04 · Source Policy

This policy is enforced in code (`09`): a citation from an unlisted domain fails the build.

## Tier 1: primary (preferred for every number)

| Source | Notes |
|---|---|
| SEC EDGAR filings (sec.gov, data.sec.gov) | 10-K, 10-Q, 8-K and exhibits, S-1, F-1, 424B, 20-F, 6-K, DEF 14A, 13F-HR, Schedules 13D and 13G, Forms 3 and 4. Cite accession number and section |
| Company investor relations and newsroom releases | The company's own domain only. Cite title and date |
| Earnings call transcripts or webcasts published by the company | Quote speaker and date |
| Regulators and courts | FTC, DOJ, Commerce (BIS), CFIUS statements, foreign securities regulators' filing systems, court dockets |
| Public corporate and lien registries | State UCC financing statements, UK Companies House (including registers of charges), equivalent national registries. Cite filing number and date. These are where GPU liens and private company charges show up |
| Credit rating agency publications | Moody's, S&P Global Ratings, Fitch: public rating actions and press releases only |

## Tier 2: named financial news publications

Bloomberg, Reuters, The Wall Street Journal, Financial Times, The Information, CNBC, Barron's, The Economist, Nikkei Asia, Axios (business coverage).

- Prefer the original reporter. If an outlet writes "according to Bloomberg", cite Bloomberg.
- Syndicated copies of one wire story are one source. Two sources are independent only if neither cites the other.
- Record the sourcing: named, documents seen, or anonymous people familiar.
- Paywalled articles: cite title, outlet, date and URL; any quote under fifteen words. The figure is grounded only after a reviewer pastes the sentence (see `11` U2).

## The display rule (one rule, applied everywhere)

**A figure is displayed only if it is supported by a tier 1 source or by two independent tier 2 sources.**

If a relationship's existence is supported but its amount is not, the relationship is displayed with the amount shown as "Not confirmed", never as a number. A relationship supported only by one tier 2 report is displayed with status "Reported, unconfirmed" and no amounts. There is no label or exception that lets a single-source figure through.

## Market data (prices only)

Share prices for public stakes come from the market data source the Economy Monitor already uses (Yahoo Finance quote data, per the monitor's refresh notes of 20 November 2026). This class supports only `market_value`, always shown with the price timestamp and source name. **The one exception to the display rule:** evidence of kind `market_data` (tier `market`) makes a `market_value` eligible on its own, when the price timestamp and source are present. It cannot support any other field. It never supports a relationship fact. Listed separately in `config/sources_allowlist.json` under `market_data`.

## Excluded, always

Blogs, Substack, Medium, Seeking Alpha contributor articles, Motley Fool, Zacks, InvestorPlace, Benzinga opinion, Yahoo Finance contributor content (wire stories on Yahoo are cited to the original wire), Wikipedia, Reddit, X and other social posts (an executive's post counts only if the company repeats it in a release or filing), YouTube commentary, podcasts, AI-generated summaries, press release distribution sites when the company's own copy exists, sell-side research notes.

If the only source is excluded, the relationship goes to `research/unconfirmed.md` with the reason and does not appear in the app.

## Output from skills and subagents

Output from `/buyside-research:research` or any subagent is filtered through `config/sources_allowlist.json` before it enters `research/candidates.csv`. A plugin's own source rules never override this file.

## Citation format and conflicts

Evidence records follow `06`. On screen, each number has a source chip that opens its citations. When sources disagree, show both, state which is preferred and why (filing over announcement over report; a later source over an earlier one when it describes a change), and set the reconciliation result.
