# 11 · Continuous Update

The map stays current without anyone editing JSON by hand, and nothing unverified reaches the live site.

## The loop

```
watchers  →  inbox  →  triage and extraction  →  review queue  →  approval  →  publish  →  change log + snapshot
(scheduled)  (raw hits)  (Claude drafts a diff,     (checks and     (human, or   (site
                          grounded in cached docs)   critic notes)   auto rule)   rebuilds)
```

---

## U1 · Watchers

Python modules in `pipeline/watchers/`. Every watcher accepts `--since YYYY-MM-DD` for backfill; scheduled runs use their normal lookback. They write raw hits to `data/inbox/YYYY-MM-DD/<watcher>.jsonl` with a content hash so nothing is processed twice. Watchers never write to `register/` or `published/`.

| Watcher | Checks | Source | Frequency (Eastern) |
|---|---|---|---|
| `earnings_calendar` | Nvidia's next earnings date and each counterparty's | Company investor relations event pages | Weekly |
| `nvda_filings` | New Nvidia filings, any form | `data.sec.gov/submissions/CIK0001045810.json` | Every 2 hours, weekdays 6 am to 10 pm; hourly for the ten days after each Nvidia earnings date |
| `counterparty_filings` | New filings by every entity with a CIK | Same endpoint per CIK | Every 4 hours, weekdays |
| `fulltext_nvidia` | New hits for queries Q1 to Q12 in `02`, filtered by the 50-word window rule | EDGAR full-text search, last 3 days | Daily, 7:10 am |
| `nvda_13f` | New 13F-HR | Submissions endpoint | Daily for 45 days after each quarter end, else weekly |
| `ownership_filings` | Schedules 13D and 13G, Forms 3 and 4, with Nvidia as filer or subject | Submissions endpoint | Daily |
| `ir_releases` | Nvidia and counterparty releases | Each company's own release page or RSS | Every 4 hours |
| `ratings` | Rating actions on counterparties | Agency press release pages that are public; logged-in pages are skipped and flagged for manual check | Daily |
| `market_values` | Prices for public stakes, market value only | Market data source named in `04` | Weekdays after the close |
| `liens` | New UCC financing statements and Companies House charges naming counterparties | State UCC search portals, Companies House | Monthly |
| `staleness` | Amounts past their re-verification limit | Internal | Daily |

**News is not a Python watcher.** Searching tier 2 publications needs Claude's web search, which a GitHub Actions script cannot call. A **scheduled Claude task** runs twice daily (7:37 am and 5:37 pm Eastern), searches only the tier 2 domains in `04` for Nvidia plus each counterparty plus the exposure keywords from `02` R4, and hands its hits to a small `ingest_news.yml` workflow through `workflow_dispatch` (hits passed as an uploaded file). That workflow commits them to `data/inbox/YYYY-MM-DD/news.jsonl` inside the shared concurrency group, so it never races the other jobs. The inbox publishes nothing, so no review is skipped. The task's prompt is stored in `pipeline/tasks/news_watch.md` and accepts a `since` date for backfill.

## U2 · Triage and extraction

A GitHub Actions job runs Claude Code headless over the inbox daily at 8:15 am Eastern, after the 7:10 full-text run and the 7:37 news task, and on demand:

1. **Triage**: discard hits with no money, commitment or credit support between Nvidia and another party; log each discard with reason.
2. **Match** to an existing relationship or mark as new.
3. **Fetch** the source. Filings are cached in full to `research/cache/` (git LFS, private repository). News articles are fetched to a temporary file only.
4. **Extract** a proposed change as a diff, with every new figure carrying a verbatim quote and locator. For news, after extraction write only the grounding window (300 characters either side of the quote) to the cache, delete the temporary file, set the locator as an offset into the window file and hash the window file. The same procedure applies in research sequence R4. For a filed item, also search the other party's filings and record silence if none (R5 rule).
5. **Check**: run every automated check in `09`, grounding included. Proposals that fail grounding are kept in the queue marked "failed grounding", never published.
6. **Critic**: run `anthropic-skills:critic-agent` on any new or changed insight and consequence text.
7. Write `data/queue/<id>.json`: summary, diff, evidence, check results, critic notes, proposed `change_type`.

Paywalled tier 2 articles cannot be read by the job. They enter the queue as "needs quote": the reviewer pastes the relevant sentence, which is cached and then grounded like any other source.

Requirements: `ANTHROPIC_API_KEY` as a repository secret and a monthly spend cap in `config/limits.json` (default to be set by Thomas). The job stops and alerts when the cap is reached.

## U3 · Review and approval

- `make review` opens a local review page listing queue items: summary, old and new side by side, evidence links and quotes, check results, critic notes.
- Actions: Approve, Edit then approve, Reject with reason, Hold. Approving writes the item to `data/approved/<id>.json` and commits it, which triggers `publish.yml`.
- **Auto-approved without a human** (rules in `config/auto_approve.json`): `market_value` updates and `link_repair`. Nothing else.
- **Always needs a human**: any change to `headline`, `committed_total`, `funded` or `contingent_max` at any size, including null to a value; any `added`, `status_changed`, `reconciliation_changed`, `dates_changed`, `corrected`; any `evidence_added` that changes `claim_basis`, the corroboration count or the reconciliation result; every `reverified`.
- A scheduled task sends Thomas a short summary of pending items on weekdays at 8:57 am Eastern, after the 8:15 triage, only when the queue is not empty. Three consecutive watcher failures appear at the top of that summary.

## U4 · Publish

On a commit to `data/approved/`:
1. Apply the diff to `data/register/`; increment `version`.
2. Update `last_verified` **only on the amount fields a human re-checked** in this item. Auto-approved market value and link changes never touch `last_verified`.
3. Append to `data/changelog.json`.
4. Rebuild `data/published/`. Totals, derived measures, scenarios and summary sentences are recomputed from the register, never patched.
5. Run every check. Any failure stops the publish and leaves the live site unchanged.
6. Snapshot to `data/history/YYYY-MM-DDThhmmssZ/`.
7. Update "Data as of" and "Last change", rebuild the page, deploy.

## U5 · Schedule and infrastructure

Same pattern as the Economy Monitor after its 20 November 2026 fix, when GitHub's own scheduler skipped runs:
- Workflows: `watch.yml`, `triage.yml`, `publish.yml`, `checks.yml`, each startable by `workflow_dispatch`.
- Workflows: also `ingest_news.yml`. All workflows that write to the repository share one GitHub Actions `concurrency` group, so they run one at a time and never collide on push.
- An external scheduler (cron-job.org, as the monitor uses) calls `workflow_dispatch` on the timetable in U1; GitHub's own cron stays as a backup.
- A fine-grained GitHub token limited to the two repositories (Actions read and write, contents write), created by Thomas.
- Secrets, never committed: `SEC_USER_AGENT`, `ANTHROPIC_API_KEY`, the scheduler token.
- Hosting: the public site repository (see `10`) on GitHub Pages at `nvidia.resolute-bd.com` (DNS in Squarespace, like `economy.resolute-bd.com`).
- `SCHEDULE.md` in the repository: the timetable, what each run does, how to run it by hand.

## Staleness rule (per amount field)

| Relationship | Re-verify every |
|---|---|
| Any of headline, committed_total or contingent_max at $1B or more | 30 days |
| Status `loi_or_framework`, `reported_unconfirmed` or `restructured`, any size | 30 days |
| Other `definitive` relationships | 90 days |
| `completed` or `terminated` | 365 days |

Past the limit, the amount shows "Not re-verified since [date]" and the `staleness` watcher queues it. Triage does the work first: re-fetches the source, re-runs grounding, and checks for newer filings or reports on the deal. Items where nothing changed are grouped on one **batch confirm** screen, so Thomas confirms them in a single pass; only items where something moved get individual review.

## Failure handling

- Watchers retry at the next scheduled run; three consecutive failures raise an alert.
- Blocked or rate-limited sources back off. A disallowed source is never substituted.
- The live site always shows the last good publish.
