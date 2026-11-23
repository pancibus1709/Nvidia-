# Plan

Written 23 November 2026 after reading every file in `/spec`.

## The phases in my own words

**R0. Tools before research.** Build the SEC client, the source cache, the evidence tool, the schemas and every automated check, with tests. Done. A research record cannot be written unless its quote is found in the cached source, so grounding happens at the moment of writing.

**R1. Start with what Nvidia had to disclose.** Read every 10-K and 10-Q in the window footnote first: investments, commitments, prepaid supply, concentration, subsequent events, risk factor changes. Cross-check against XBRL. Read every 13F quarter.

**R2. Then read what everyone else filed about Nvidia.** Twelve full-text searches across all filers, kept only where the terms sit within fifty words of each other.

**R3 and R4. Then announcements and news.** Company releases for deals that never reached a filing. Named financial publications for private counterparties, two independent sources or the amount stays "Not confirmed".

**R5. Check every deal from the other side.** What did the counterparty say? Agree, differ, or silent.

**R6. Map neoclouds site by site.** Sites, megawatts, GPUs, tenant, lenders, liens. Newest debt instrument first.

**R7. Classify and measure.** Split each amount into headline, committed, funded and contingent. Compute the unattributed remainder once all named deals are known.

**R8. Find who else relies on each deal.** Lenders, offtakers, co-investors.

**R9. Write consequences, run the critic, build the evidence pack, ask for approval.**

**Then stop.** No app code until Thomas approves the register (confirmed in chat, 23 November 2026).

## Who does what

Research runs on Opus agents. Tooling, the application and reviews run on the lead model. Both per Thomas's instruction.

## Conflicts and gaps found in the spec, and how each is handled

| # | Issue | Handling |
|---|---|---|
| 1 | Grounding says the quote must be found "in the cached file". Filings are HTML with tags inside sentences and around numbers, so a readable quote never matches the raw bytes. | The cached file stays raw and is hashed raw. Quotes and locators refer to a deterministic text rendering of it (`pipeline/common.py`), which the check re-derives each time. |
| 2 | An amount is sometimes the sum of several disclosed pieces (two tranches, several funds). No single quote contains the sum. | Amount objects may carry `components`, each grounded on its own; the check confirms they add up. |
| 3 | The schema has no place for the inputs to the derived measures or the stress scenarios, or for carrying value. | Added optional `measure_inputs`, `stress_inputs` and `amounts.carrying_value`, each an amount object under the same rules. |
| 4 | "Share of Nvidia equity" and "share of free cash flow" need Nvidia's own figures. | Added `data/register/nvidia_financials.json`, sourced and grounded like any amount. |
| 5 | The loss formula needs "value received or recovered". No source states it for most deals. | `loss_max` assumes nothing is recovered and is labeled an upper bound. Base loss is "not estimated" unless inputs are sourced. |
| 6 | The spec runs `/buyside-research:research` per cluster. Thomas asked for Opus research agents. | Each cluster runs as an Opus agent with the cluster brief from spec/02. Its output passes the same allowlist and grounding checks. |
| 7 | Two repositories, a custom domain, an external scheduler and repository secrets are required for Phase U. This session can reach one repository only. | Workflows and instructions are written here. Thomas creates the public repository, DNS record, scheduler and secrets. Listed in SCHEDULE.md when Phase U is built. |
| 8 | The cache should use git LFS in a private repository. | Filings cited by the register are committed (they are public documents). News is stored only as the 300-character grounding window. Whether this repository is private needs Thomas's confirmation before any news window is pushed. |
| 9 | Tier 2 articles behind a paywall cannot be read here. | They are recorded as "needs quote" and stay ineligible until a reviewer pastes the sentence. |
| 10 | "Open source" links (added by Thomas, 23 November 2026). | Every evidence record carries `source_link`, which opens the document itself at the quoted passage. |

## Questions for Thomas (only those that change what gets built)

1. **SEC contact string.** Needed before any research can run. See chat.
2. **Is this repository private?** It decides whether news grounding windows can be committed here.
3. **Letter grades on the public page.** Default is off, per the spec.
