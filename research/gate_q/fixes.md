# Gate Q fixes: response to design_critique.md

25 November 2026. Files changed: `pipeline/build_site.py`, `pipeline/site_assets.py`, `pipeline/publish.py` (summary figures and bridge rows now carry their sources), `tests/test_site.py` (new). `site/index.html` and `data/published/` are regenerated, never hand edited.

Verified with Playwright (Chromium) on `file:///home/user/Nvidia-/site/index.html` at 1440, 1024, 768 and 390, reduced motion on and off, plus 320 and 360 for sideways scroll. Scripts are in the session scratchpad (`fix/acc.js`, `fix/phone.js`, `fix/print.js`, `fix/a11y.js`, `fix/scan.js`), not in the repository. After screenshots: `research/gate_q/screens/after_01` to `after_10`.

Pipeline: `python3 -m pipeline.publish && python3 -m pipeline.build_site && python3 -m pipeline.checks && python3 -m pytest -q tests` gives "All checks passed" and 65 tests passed.

Status words: Fixed (as the critique specifies), Changed (fixed a different way, reason given), Not fixed (reason given).

## Usability findings

| # | Finding | Severity | Status | What was done |
|---|---|---|---|---|
| 1 | Filtered tiles state things that are false | Critical | Fixed | `applyFilters()` recomputes each tile's value, count and note from the visible set. Under a filter the note reads "Filtered: 24 of 81 relationships." and the summary note reads "Filters are on: 24 of 81 relationships. For this set ... gross exposure of at least $12.6 billion; 18 of 24 have a part that is not disclosed." with a Clear filters button beside the tiles. Unfiltered it ends "No filter is on." Both notes are `role="status"`. The ranked list filters too. |
| 2 | Headline numbers do not open sources | Critical | Fixed | Every lede figure has a chip (9 of 9). Each tile has a sibling Sources chip (4 of 4) and so does the gross exposure note. Every Ledger money cell is a link that opens that amount's citations (74 of 74), the totals row opens the contributing relationships (5 of 5), stress figures carry chips (4 of 4 in S1), Method and "Who else guarantees" amounts carry chips (29 of 29 and 21 of 21; four bridge cells read "None" and have no figure). Totals open a short list of the largest relationships, each with its publisher, date, an Open source link and an "All n sources" chip. Nvidia's own figures open the Nvidia filing. |
| 3 | Phone full-screen map is a dead end | Critical | Fixed | Close map button fixed inside the map box (92 by 44 px), focus moves to it, Escape closes, a history entry is pushed on open so Back closes and stays on the page. The SVG is 1300 px wide in a scrolling box, so labels render at 14 px, and the box opens centered on Nvidia. |
| 4 | Print is not board-pack ready | Critical | Fixed | `@page{size:A4 landscape;margin:12mm}`, wrap overflow visible, 8.5pt table, all 13 columns fit, badges keep fills (`print-color-adjust:exact`), totals print once, detail rows, chips, hints and the other views are hidden, the Ledger starts on its own page with a repeating header. With a panel open, `beforeprint` moves it to the front and opens every section; `afterprint` restores it. A CSS fallback (`::details-content`) opens the sections when print is emulated. |
| 5 | Clicking a node's name does nothing | Moderate | Fixed | Labels take pointer events; each node has a transparent hit circle of at least 15 px radius. |
| 6 | Map labels too small | Moderate | Changed | Labels 14 px, ring labels 13 px in `--ink-2` with a white halo, viewBox `-90 0 1300 1000`, ring labels placed by a search for a gap clear of nodes and node labels. Changed: the map is one column at every width with the legend beneath (the critique asked for this only below 1100), because beside a 280 px legend the labels would still render near 9 px. Labels now render at 12.4 px at 1440 and 10.6 px at 1024 and 768 (`min-width:980px` in a scrolling box). |
| 7 | Stress highlight at first load | Moderate | Fixed | S1 is computed on load for the Stress view but no ring is drawn until the reader presses a scenario or the URL carries `scenario=`. Legend row "Red ring: touched by the selected stress scenario" with a Clear highlight button, shown only while active. |
| 8 | Filtered-out halos at full strength | Moderate | Fixed | `#map .halo.dim{opacity:.03}`. |
| 9 | Escape closes two layers; popover outside the dialog | Moderate | Fixed | The popover is appended inside the panel when its chip is there. One key handler closes the popover first and returns focus to the chip; a second Escape closes the panel. |
| 10 | Timeline brush, inputs and marks disagree | Moderate | Fixed | One `setRange()` feeds the filter, both inputs, the brush and the caption ("Showing 9 March 2025 to 9 January 2026. 21 of 81 relationships. 18 undated relationships hidden."). Marks dim by their own date. Undated relationships are excluded and counted. Clear resets inputs, brush and caption. `user-select:none`. Out-of-range marks are drawn hollow, so stacked marks cannot look lit. |
| 11 | Ledger header does not stick | Moderate | Changed | `.ledger-wrap{max-height:80vh;overflow:auto}`, sticky header and sticky first column, a 3 px right edge and a text hint while more columns sit to the right. Headers shortened. Changed: amounts use B and M suffixes with a key under the table instead of a "$ billion" unit column, because cells run from $1.2 million to $105 billion. All 13 columns fit at 1440 (scroll width 1146 in 1146). |
| 12 | "Full detail for" rows double the Ledger | Moderate | Fixed | With script on, detail rows are hidden; a disclosure button in the first cell (`aria-expanded`, `aria-controls`) shows the row in place. Script-off markup is unchanged. |
| 13 | Type column shows bare codes | Moderate | Fixed | Full label in the badge ("Guarantee", "Capacity rental"). |
| 14 | Shared links lose most of the view | Moderate | Fixed | The hash carries `lab`, `p` (slider values), `cluster`, `type`, `status`, `wwr`, `basis`, `from`, `to`, `filter`. Scenario is upper-cased on read. `hashchange` reapplies the state. An unknown `rel` is still dropped without a message. |
| 15 | Sliders that change nothing | Moderate | Fixed | Four S1 sliders and "Months of delay" are disabled with the caption "No effect yet: the inputs this would move are not disclosed." Outputs read "-30%", "50%", "4 quarters"; `aria-valuetext` matches. |
| 16 | About 280 tab stops | Moderate | Fixed | Roving tabindex: one stop for the map, one for the timeline (Left, Right, Home, End). "Skip the map" and "Skip the timeline" links appear on focus. Up and Down now move to the nearest node by angle. |
| 17 | "What changed" nav target broken | Moderate | Fixed | No duplicate ids on the page. Nav and the header pill point to `#changes-view`; the list is `#changes-list`. |
| 18 | Ten seconds to the three facts | Moderate | Fixed | Tiles come first in the source. At 1100 px and up the lede sits left and the tiles 2 by 2 on the right. At 390 all four tiles end 709 px down the first screen and the lede shows two paragraphs with the rest under "More of the summary". |
| 19 | Horizontal page scroll at 390 | Moderate | Fixed | `scrollWidth` equals the viewport at 320, 360 and 390, with every `details` open. `overflow-wrap:anywhere` on change items; loop cards no longer force 320 px; `html{overflow-x:clip}` as a backstop. |
| 20 | Ledger and wide tables on a phone | Moderate | Fixed | Sticky first column (150 px) and header at 390. "Who else guarantees", Method, stress and project tables become stacked cards with a label per value at 600 px and below. |
| 21 | Timeline unusable at 390, weak at 768 | Moderate | Fixed | At 600 px and below the SVG is hidden and an event list grouped by year opens (136 items, each opens its panel). The same list sits in a `details` at every width. The SVG draws at one unit per pixel (12 px labels at every width), `min-width:720px`, `touch-action:pan-y`. Legend: circle "Event", diamond "Restructured or ended". |
| 22 | Loops are text cards | Moderate | Fixed | Each leg starts "Out:", "Back:" or "Onward:", has a colored left border, and puts its amount on its own right-aligned line. Nested parentheses are gone. Each loop also has a small inline SVG with numbered paired arrows that match the list. |
| 23 | Depth-2 satellites not drawn | Moderate | Fixed | Satellites (name and role, up to six, then "and n more in the panel") are drawn from `depth2_links` when a node is pointed at, focused or opened. The legend says so, and each panel has a "Lenders, co-investors and offtakers" section with sources. |
| 24 | Invisible open dialog after quick close and reopen | Moderate | Fixed | The close timer id is kept and cleared in `openPanel()`. |
| 25 | Truncated text | Moderate | Fixed | Full text everywhere. Long descriptions fold after the first sentence in a `details`. |
| 26 | Sort gives no visible state | Minor | Fixed | Arrows on sortable headers; Cluster, Type, Status and Both sides now sort; a status line announces the sort. |
| 27 | Expand all label wrong after reload | Minor | Fixed | Label follows the real state. It is a `button`. |
| 28 | Expand all touches the close button | Minor | Fixed | 8 px gap; close is 44 by 44 px. |
| 29 | Significance row breaks at 390 | Minor | Fixed | Wraps as whole phrases. |
| 30 | Active nav item wrong for short sections | Minor | Fixed | `rootMargin:'-60px 0px -70% 0px'`, the active item scrolls into view, right-edge fade at 820 px and below. |
| 31 | Selection ring persists | Minor | Fixed | `selectNode(null)` in `closePanel()`. |
| 32 | Nav clicks add history entries | Minor | Fixed | `preventDefault`, `scrollIntoView`, `replaceState` only. History length is unchanged after nav clicks. |
| 33 | 122 identical "Added" lines | Minor | Fixed | One line per same-day bulk ("25 November 2026: register published with 93 records: 81 relationships in the totals, plus unattributed remainders and context records.") with a `details` list. Duplicate prefixes removed. Three top-level items now. |
| K1 | Panel does not trap focus | Critical | Fixed | Everything behind the panel is `inert`; a scrim closes on click; Tab and Shift+Tab cycle over visible controls only (60 Tab presses, 0 outside). Focus returns to the opener. Page scroll is locked at 600 px and below. |
| K2 | Focus on map nodes not visible | Critical | Fixed | A focused node scrolls to the center of the view and draws its own ink ring plus an ochre ring. The stress ring is a separate circle and cannot override it. |

## Visual hierarchy

Fixed: tile figure 1.75rem weight 500 with a small unit, labels on a shared baseline, "Loss in this scenario" label with Analysis, "Partly supported" in ink with an ochre square.

## Consistency table

| Item | Status | Note |
|---|---|---|
| Dates | Fixed | "17 Aug 2026" in tables, "17 August 2026" in prose, captions and labels. ISO stays only in attributes, inputs, the CSV and verbatim quotes. Scan: 0 ISO dates in reader text. |
| Internal identifiers | Fixed | Scan: 0 `ev_`, `rel_`, `ent_`, field names or `spec/` strings in visible text. Evidence ids in prose become Source chips. Research notes are left out of the public build. |
| Body text size | Fixed | 0.9375rem in cards and panel sections; prose capped at 70ch. |
| Meaning map vs drawn styles | Fixed | Financing has an arrowhead, prepayment is a double line, fund commitment has cross ticks, conditional equity has a hollow core, license is thin, context is a hairline. Legend swatches match and say the style in words. |
| Node with several deal types | Changed | Legend line: "A node with several deals shows its largest; the hover lists all." Parallel edges would crowd the center. |
| Verdict colors | Fixed | "Not testable" in `--ink-2` with a hollow square; "Not supported" cochineal with a diamond; "Supported" leaf with a dot. |
| Verdict layout and length | Not fixed | The cards and their text come from the register, which this task may not edit. |
| Range inputs | Fixed | `accent-color:var(--cobalt)`. |
| Analysis labelling | Fixed | Added to the stress result, the "Who else guarantees" lede, each verdict and each insight. "Illustrative" has its own plain bordered class. |
| Amount cells | Fixed | "None", "Not applicable" and italic "Not disclosed" are distinct, with the same words in Ledger and panel. |
| Panel amounts | Fixed | Market value, carrying value and annual obligation sit on their own row. |
| Key dates line | Fixed | "Matures: not disclosed". |
| Definitions | Not fixed (partly) | Dotted underline removed in Method; Ledger headers carry a `title`. A focusable hover note on first use in each view is not built. |

## Contrast failures table

All ten Fixed. A scan of 2,816 visible text nodes (17 color pairs) with the panel open and expanded finds 0 below AA.

| Element | Now |
|---|---|
| `.amt .d` | `--ink-2` |
| `.amt .v.nc` | `--ink-2`, weight 500 |
| `td.num .nc` | `--ink-2` |
| Terminated rows | `--ink-2`, a "Terminated" badge, line-through on amounts |
| `#map .ringlab` | `--ink-2`, 13 px |
| `#tl .axis` | `--ink-2`, 12 px |
| `.verdict.v-Partly` | `--ink` with an ochre marker |
| `.badge.b-EQ-C` | `#4F6DB0` (5.06:1) |
| Conditional equity line | `#6F8BC8` with a hollow core |
| Focus ring on pressed controls | 2 px offset plus a 2 px white band |

Text floor is 12 px (0 elements below). Touch targets at 390 with a coarse pointer: every control is at least 44 px in one dimension and 24 px in the other (chips 46 px tall, buttons, selects, date inputs, summaries, sort buttons, row buttons, amount links, range input 44 px). Timeline marks are replaced by the list on phones.

Screen reader items: Fixed for edge and ring groups (`aria-hidden`), node names (ring and wrong-way risk added), `#tip` (no live role), the map's `aria-describedby` and "View as list" at every width, timeline dates in words, the panel (`aria-labelledby` an `h2`), tile announcements, `aria-current="location"`, the Ledger (`caption`, `scope`, a real button per row, status line), chip names ("6 sources for contingent maximum"), the significance bar, slider `aria-valuetext`, a Summary heading, labelled sections, `h4` for inline detail. 0 unnamed controls.

## Acceptance tests re-run

| # | Test | Result | Evidence |
|---|---|---|---|
| 1 | Node or Ledger row opens a panel with insight, four amounts with chips, dates | Pass | Label click on "CoreWeave" opens the panel; row button opens it with a non-empty insight, four amounts and dates. 77 of 77 dollar amounts in panels carry a chip. |
| 2 | Sections expand and collapse; Expand all; state survives reload | Pass | All sections open, reload restores them and the button reads "Collapse all". |
| 3 | Every number opens its citation list in one click | Pass | Coverage above. One click on a lede chip, tile chip, Ledger cell, total, stress figure and Method cell each opens a popover in view with at least one Open source link; all `data-ev` ids resolve. Not covered: counts of our own records and derived percentages in Method prose, which have no external source. |
| 4 | Cluster filter gives the same totals in tiles, map and Ledger | Pass | Neoclouds: tiles $6.18 billion, $5.6 billion, $860.3 million, $25.9 billion equal independent sums and the totals row; counts 4, 3, 1, 10; 24 rows; 10 nodes lit; 9 halos dimmed; ranked list 10. after_02. |
| 8 | A copied URL reproduces the view | Pass | `#view=stress&scenario=s2&lab=ent_anthropic&p=h2:0.8&cluster=ai_lab&status=completed&from=2025-01-01&to=2026-11-25&filter=funded` in a fresh context restores the lab, "$8 billion", both selects, both dates and the tile. The spec example with `scenario=s1` opens the panel with S1 pressed. |
| 11 | Works at 390; map becomes the ranked list | Pass | No sideways scroll at 320, 360, 390; full-screen map closes three ways; event list replaces the timeline. after_07 to after_09. |
| 12 | No banned dashes | Pass | Browser scan 0 hits; `pipeline.checks` passes. |
| 13 | Lighthouse | Not run | Lighthouse is not installed and cannot be fetched here. Run instead: contrast scan (0 failures), duplicate ids (0), unnamed controls (0), landmarks and headings, focus order and trap, touch targets. First paint 112 ms, DOMContentLoaded 212 ms, 0 external requests, 2.33 MB raw, 329 KB gzip. |
| Gate B 3 | Four widths, reduced motion on and off | Pass | 73 of 73 checks at 1440, 1024 and 768, and 59 of 59 at 390, each with reduced motion on and off; console clean in every run. |
| Gate B 4 | Keyboard walkthrough, labels, contrast | Pass | Skip link, skip-the-map link, one Tab stop for the map, focused node in view with its ring (after_03), Enter opens, trap holds, Escape order, focus returns. |
| Spec 07 | Print: Ledger and an open panel | Pass | Ledger PDF: A4 landscape, 15 pages, all columns, totals once, no hints (after_10). Panel PDF: panel first with every section open, then the Ledger. |

## Notes

- `pipeline.publish` rewrites derived fields in `data/register/`; those two files were restored with `git checkout` after each run so the register is untouched. One new snapshot remains in `data/history/`.
- `data/published/summary.json` now carries, per sentence figure, the measure or citations behind it, and per bridge row its evidence. `evidence.json` gained the Nvidia filing citations those need.
