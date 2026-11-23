# 07 · Application Spec

## Design principle

One idea per screen. Within ten seconds of landing, the reader should know three things: how much Nvidia has put behind its own customers, how much of it is binding, and where the risk concentrates. Everything else sits one click deeper. No decoration. Every number opens its source.

The structure follows the US Economy Monitor so the two read as a family: a written summary at the top generated from the data, then the main visual, then the detail.

---

## Page structure (top to bottom)

### 1. Header
- "Built By Resolute Business Development" with a link to resolute-bd.com, top left, same treatment as the Economy Monitor.
- Title: **Is Nvidia the Central Bank of AI?** Subtitle: "Every dollar Nvidia has put behind the companies that buy its chips, with sources."
- A "Data as of [date]" pill and a "Last change [date]" pill that opens What changed.

### 2. The summary (generated, not hand written)
Three to five sentences built from the data by templates in the pipeline, each figure linked to its source. Example form, not content: "Nvidia has [N] disclosed financial relationships with companies in the AI buildout. [X] is funded, [Y] is committed but not yet paid, and [Z] is contingent on events such as unsold capacity. The headline total announced is [H], of which [share] is legally binding." Numbers enter only through placeholders filled from the published data.

### 3. Headline tiles (four)
Funded · Committed, not yet paid · Contingent maximum · Headline announced. The first three add up to gross exposure; headline is shown apart and never added. Each tile states the number, the count of relationships, and a one-line note. Clicking a tile filters the map to that category.

### 4. The Constellation (main view)
A radial map drawn in SVG in the page.
- Nvidia at the center.
- Rings by cluster: AI labs, neoclouds, semis and supply, hyperscalers and offtakers, sovereign and projects (vehicles such as GPU-owning SPVs sit here), portfolio. Lenders appear only as depth-2 satellites. Entities in `other`, including unattributed remainders, sit in an outer band labeled "Other and unattributed". Each ring is labeled.
- Node size by gross exposure (funded plus committed not yet paid plus contingent maximum; see `05`). Base and stressed EAD appear only in the panel and the Stress view. A specific wrong-way risk mark sits on nodes where exposure grows as the counterparty weakens.
- Node outline: by default a neutral outline; letter grades color the outline only if Thomas turns grades on (`05` section 5).
- Edge color and line style for every exposure type come from the meaning map in `08`.
- Edge thickness by gross exposure, drawn solid; headline-only drawn as a faint outer stroke so the gap between promise and commitment is visible at a glance.
- Closed loops (Nvidia to A to B to Nvidia) can be highlighted with a toggle: "Show circular flows".
- Depth-2 parties (lenders, offtakers) appear as small satellites only when their depth-1 node is selected.
- Hover: name, type, gross exposure (marked "at least" when a lower bound), date. Click: opens the relationship panel.
- Keyboard: every node is focusable, arrow keys move between nodes in a ring, Enter opens.
- On phones the Constellation becomes a ranked list grouped by cluster; the radial view is offered as an optional full-screen.

### 5. Relationship panel (click to open, sections collapse)
Slides in from the right on desktop, full screen on phones. Built with native `details` and `summary` so it works without script.

Always visible at the top:
- Counterparty name, cluster, type badge, status badge and source-strength chip, with labels taken from `schema/enums.json` (`06`).
- **The insight**, one sentence in serif.
- The amounts in a row (funded, committed not yet paid, contingent maximum, headline), unknowns shown as "Not disclosed" and amounts that fail the display rule shown as "Not confirmed", each with a source chip and its as-of date.
- Key dates: announced, effective, matures, last verified.
- Significance bar with its score and a "why" link.

Collapsed by default, each a `details` section:
1. **What the deal is**: the plain-English definition.
2. **Both sides**: what Nvidia disclosed, what the counterparty disclosed, the reconciliation result, any differences listed.
3. **Project basis** (neoclouds and vehicles): the project table from `projects.json`.
4. **Credit read**: public ratings, debt and maturities, liquidity months, customer concentration, collateral, wrong-way risk (specific, general or none, with reason). Letter grade only if grades are turned on.
5. **Exposure and derived measures**: gross exposure, base and stressed EAD and loss side by side, circularity ratio and round-trip and the other measures, each labeled Analysis, with formula and inputs, no adjectives.
6. **First order consequences**.
7. **Second order consequences**, grouped by lens.
8. **Timeline** of this relationship's events.
9. **Sources**: every citation, tier badge, publisher, date, accession number, short quote, link.

A control at the top of the panel: "Expand all" and "Collapse all". The open or closed state of each section is remembered per visitor (local storage wrapped in try and catch).

### 6. The Ledger
A sortable, filterable table of every relationship: counterparty, cluster, type, status, funded, committed not yet paid, contingent maximum, gross exposure, headline, announced, last verified, reconciliation, significance, and grade only when grades are turned on. The totals row sums funded, committed not yet paid and contingent maximum, which never overlap; committed total (which includes funded) is available in the panel and the CSV, labeled as such. Filters: cluster, type, status, wrong-way risk, date range, source strength. Unattributed remainder rows are shown in their own section below the table and excluded from the totals row. Each row expands in place to the same sections as the panel. Download as CSV with the source URL column included; the CSV follows the same column rules, and its grade column exists only when grades are turned on.

### 7. Timeline
A horizontal dated track from 2023 to today, one lane per cluster, a mark per event. Brushing a date range filters the Constellation and Ledger. Makes visible how fast the commitments accumulated and when deals were restructured.

### 8. Loops
A flow diagram of the closed loops found in R9: Nvidia money in, purchases back, rentals out, drawn as paired arrows with amounts and dates. Each loop states its circularity ratio and the caveat that the computation needs both sides sourced.

### 9. Stress
Three scenario buttons (S1, S2, S3 from `05`) with sliders for their parameters. Selecting one highlights affected nodes, shows stressed EAD and loss against Nvidia's equity and free cash flow, lists the assumptions with their basis, and lists anything not computable. A plain sentence at the top: "These illustrate how losses would travel, not forecasts."

### 10. Is Nvidia a central bank?
The four-function table from `05` section 1, with a verdict and the evidence for and against each function, plus the one paragraph on where the analogy breaks. Under 300 words.

### 11. What changed
A reverse-chronological list from `changelog.json`: date, relationship, what changed, old value, new value, source. Filter by type of change. This is how a returning reader sees what moved since their last visit.

### 12. Method and sources
How the data was gathered, the source policy, definitions of every term, the significance formula, the EAD formula, the staleness rule, and the not-investment-advice disclaimer.

---

## Copy rules

- Plain words a non-specialist can follow. Define every credit term on first use with a hover note.
- No em dashes. No hype ("massive", "staggering", "game-changing"). Numbers do the work.
- Every inference says so: a small "Analysis" label beside it.
- Insight sentences state the risk, not the drama. Model template: "Nvidia has agreed to buy whatever capacity {counterparty} cannot sell through {dates.maturity:year}, so its exposure grows exactly when demand weakens." Numbers and names come only from placeholders.
- Run `anthropic-skills:human-voice` on all generated templates and on every insight.

## Interaction and performance requirements

- First paint under one second on a mid-range laptop; data under 1 MB compressed.
- `build_site.py` renders the summary, tiles, Ledger rows and every panel's content into the HTML at build time, so they work with JavaScript off; script adds sorting, filtering, the map and the panel slide-in.
- URL reflects state: `#rel=rel_example_bk_2025&view=constellation&scenario=s1`, so any view can be shared.
- Accessibility: contrast AA at minimum, focus rings visible, panel traps focus and closes on Escape, charts have text equivalents, color is never the only carrier of meaning (edge style plus label as well).
- Print stylesheet: the Ledger and an open panel print cleanly for a board pack.
