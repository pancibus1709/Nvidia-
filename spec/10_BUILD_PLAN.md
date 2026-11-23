# 10 · Build Plan

## Repository layout

```
nvidia-central-bank/
  spec/                      this package
  research/
    PLAN.md  SCOPE.md  seed_status.csv  candidates.csv  unconfirmed.md
    cache/                   cached sources for grounding: filings in full; news only as the grounding window (300 characters either side of the locator). Stored with git LFS in the private repository so CI can read it
    evidence/                working notes only; the canonical evidence store is data/register/evidence.json
    reports/                 R0.md to R9.md, cluster reports
    Nvidia_Exposure_Datapack.xlsx
  schema/                    JSON Schemas for every data file
  config/
    sources_allowlist.json   significance.json   draw_rates.json   scenarios.json
    grade_rubric.json   display.json   auto_approve.json   staleness.json   limits.json
  data/
    inbox/   queue/   approved/   register/   published/   history/   changelog.json
  pipeline/
    edgar.py                 SEC client: User-Agent from env, throttle, cache
    xbrl.py                  companyfacts reader
    extract.py               filing section extraction
    watchers/                one module per watcher in 11
    tasks/news_watch.md      prompt for the scheduled news task
    triage.py                inbox to queue
    review.py                local review page
    measure.py               EAD, derived measures, significance
    scenarios.py             S1 to S3
    summarize.py             template sentences for the summary
    build_site.py            writes site/index.html with summary, tiles, Ledger and panels rendered into the HTML
    checks.py                every automated check in 09
  site/
    index.html               single self-contained page, charts drawn in-page
  tests/
  .github/workflows/         watch.yml  triage.yml  publish.yml  checks.yml
  SCHEDULE.md   README.md   Makefile
```

**Two repositories.** The working repository (pipeline, research, register, cache, queue) is **private**. A separate **public** repository holds only `site/` and `data/published/`, and is what GitHub Pages serves. `publish.yml` pushes to it. Cached article text is never public.

Python 3.11+, standard library plus `requests`, `jsonschema`, `lxml` or `beautifulsoup4` for filing HTML, `openpyxl` for the datapack. The page uses no framework and loads nothing from other websites, the same rule as the Economy Monitor, so it stays fast and lasts.

## Milestones

| # | Milestone | Done when |
|---|---|---|
| R0 | Research tooling: SEC client, cache, XBRL reader, extractor, `schema/enums.json`, JSON Schemas, `checks.py` with tests, `measure.py`, `scenarios.py`, and the configs research needs (`sources_allowlist.json`, `grade_rubric.json`, `draw_rates.json`, `scenarios.json`, `significance.json`, `staleness.json`) | `make check` runs and its fixture tests pass, including grounding and display eligibility |
| R1 to R9 | Research sequences | Gate R passed, Thomas approved |
| B1 | Remaining configs: display, auto-approve, limits | Each loaded and validated by the pipeline |
| B2 | Pipeline: measure, scenarios, summary, published build | `published/` regenerates from `register/` deterministically; totals tie to datapack |
| B3 | Page shell, header, summary, tiles, Ledger | Ledger lists every relationship with working filters, sorting, CSV export |
| B4 | Relationship panel with collapsible sections | Every section renders for every relationship; works with script off |
| B5 | Constellation, Timeline, Loops, Stress | Visual checks at four widths; keyboard navigation complete |
| B6 | Central bank verdict, What changed, Method | Copy passes human-voice; disclaimer present |
| U1 to U5 | Continuous update per `11` | Gate U passed |
| Q | Final critic and design critique | Gate Q passed; publish |

## Acceptance tests

1. Clicking any node or Ledger row opens a panel showing the insight, the four amounts with source chips, and the dates.
2. Each panel section expands and collapses; Expand all and Collapse all work; state survives reload.
3. Every number on the page opens its citation list in one click.
4. Changing the cluster filter updates the tiles, Constellation and Ledger to the same totals.
5. Headline amounts never appear inside committed, funded, contingent or gross totals (fixture where only headline is known), and an unattributed remainder record is never counted in any total.
5a. A fixture record whose quote is absent from its cached source fails `make check` (grounding).
5b. A fixture figure supported by a single tier 2 source displays as "Not confirmed" **and** is absent from every tile, total, derived measure, scenario and summary sentence.
5c. A filing quote containing an en dash passes grounding and the copy scan, and renders inside a quotation element.
6. A relationship with status `terminated` appears greyed with its history, not deleted.
7. Selecting S1 highlights the expected nodes from a test fixture and shows that scenario's EAD and loss (from `scenarios.json`, not the 100% maximum) equal to an independent calculation. A fixture with a negative demand shock produces a backstop draw greater than zero.
8. The URL reproduces the view: open a copied link in a new browser and the same panel and scenario appear.
9. With a fixture filing dropped in the inbox, triage creates a queue item; approving it updates the site, the change log, the history snapshot and What changed.
10. A fixture citation from an excluded domain fails `make check`.
11. Page works at 390 pixels wide; Constellation becomes the ranked list.
12. No U+2012, U+2013, U+2014 or U+2212 in text we write, per the copy scan in `09`; verbatim quotes, titles and URLs are exempt.
13. Lighthouse accessibility score 95 or higher; performance 90 or higher.
