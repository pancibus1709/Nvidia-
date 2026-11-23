# 09 · QA and Critic Gates

Four gates. Nothing passes a gate with an open critical finding. The automated checks are built in R0 (see `10`), so they run from the first research record onward.

---

## Automated checks (`make check`; also run by every scheduled job)

| Check | Fails when |
|---|---|
| Schema | Any record fails its JSON Schema or uses a value outside `schema/enums.json` |
| Evidence resolution | Any evidence id does not resolve, or any non-null amount has no evidence |
| **Grounding** | An evidence `quote` is not found verbatim (whitespace normalized) in the cached file at `cache_path`; or the cached file's hash differs from `content_hash`; or an amount it supports does not appear in the quote or within 300 characters of `locator` in the cached text (numbers matched after normalizing units, for example "$6.3 billion" equals 6.3e9, and after applying the scale at `unit_scale_locator` for table figures such as "(in millions)"). Non-USD amounts ground `original_value`. XBRL-sourced figures must match the fact value at the fact id |
| Display rule | `display_eligible` is set false on any amount supported neither by a tier 1 source nor by two independent tier 2 sources (see `04`). The check fails if any ineligible amount is rendered as a number, or feeds any tile, total, derived measure, scenario, significance score, summary sentence or the public change log. Market data follows the single exception in `04`. Arithmetic is recomputed from eligible amounts only, independently of the pipeline |
| Independence | Two tier 2 sources share a `parent_company` (for example WSJ and Barron's), or either lists the other in `cites_publisher` |
| Source allowlist | An evidence URL domain is not in `config/sources_allowlist.json`, or a market data domain supports anything other than `market_value` |
| Dates | A displayed number lacks `as_of`; an amount's `last_verified` is past its limit in `11` without a stale badge |
| Headline leakage | Any tile, total or summary sentence includes `headline` in committed_total, committed_unfunded, funded, contingent_max or gross figures |
| Amount order | Where known, `funded ≤ committed_total ≤ headline` is violated |
| Aggregate exclusion | A record with `aggregate_of` set is included in any total |
| Arithmetic | Tiles and summary differ from an independent recomputation from the register |
| Insight rules | Rendered insight over 25 words; template contains a digit or number word; any placeholder unresolved |
| Copy scan | Any em dash (U+2014), en dash (U+2013), figure dash (U+2012) or minus sign (U+2212) in text we write: `site/` and `data/published/`, **excluding** evidence `quote`, evidence `title` and URLs, which stay verbatim for grounding and render inside a quotation element. Banned words from the human-voice skill. Formulas on the Method view use a plain hyphen-minus |
| Quotes | Any quote of fifteen words or more |
| Reconciliation | `contradicted` or `partial` without a differences list |
| Links | Weekly: a source URL no longer returns 200 and is not marked paywalled or moved |

## Gate R · Register complete (end of research)

1. Automated checks pass on the whole register.
2. **Independent re-sourcing.** A fresh subagent that has not seen the research re-sources from scratch: every relationship where any of headline, committed_total or contingent_max is $1B or more; every relationship with status `loi_or_framework`, `reported_unconfirmed` or `restructured`; every value equal to a seed register value; plus a random 20% of the rest. Any mismatch reopens that relationship.
3. Seed register: every row `confirmed`, `modified` or `killed`, with reason.
4. `anthropic-skills:critic-agent` on the register, cluster reports and system view, up to three rounds. The critic must answer:
   - Is any headline number treated as exposure anywhere?
   - Is any one-sided relationship presented as reconciled?
   - Would any consequence read the same for a different company?
   - Do restructured or abandoned deals show their current status?
   - Is anything sourced to an excluded publication, or displayed on one tier 2 source?
   - Does the "central bank" verdict claim more than the evidence supports?
5. The datapack's totals tie to the register.
6. Thomas approves in chat. The approval date becomes the **Gate R cutoff** in `research/SCOPE.md`.

## Gate B · Application complete

1. Automated checks pass.
2. Every acceptance test in `10` passes.
3. Screenshots at 1440, 1024, 768 and 390 pixels, reduced motion on and off.
4. Keyboard-only walkthrough of every view, screen reader labels, contrast.

## Gate U · Continuous update proven

1. A fixture filing in the inbox produces a queue item; approval publishes it; the change log, history snapshot and What changed all show it.
2. A simulated failure (source unreachable, schema failure, grounding failure) blocks publishing and leaves the live site unchanged.

## Gate Q · Before publishing

**First publish only:**
1. Run every watcher and the news task in backfill mode (`--since` the Gate R cutoff) and resolve every queue item, so the first public version reflects deals that changed during the build. Full-text queries that overflow are split by narrower date ranges per `02` R2.
2. `design:design-critique` on every view.

**Every publish that changes displayed data:**
3. `anthropic-skills:critic-agent` on each new or changed insight and consequence.
4. Approval as set out in `11` U3. This gate does not define its own thresholds.
