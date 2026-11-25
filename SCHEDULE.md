# Schedule

How the map stays current (spec/11). Every time below is Eastern. Nothing reaches the live site without passing every check, and nothing except market values and link repairs reaches it without a person's approval.

```
watchers  ->  inbox  ->  triage and extraction  ->  review queue  ->  approval  ->  publish  ->  change log and snapshot
```

## Timetable

| When (Eastern) | What runs | Workflow | What it does |
|---|---|---|---|
| Every hour at ten past | Watchers that are due | `watch.yml` | Runs `python3 -m pipeline.watchers.run --due`. The module decides in Eastern time which watchers are due (table below), writes new hits to `data/inbox/YYYY-MM-DD/<watcher>.jsonl` and commits them. New market values start `triage.yml` without the paid step |
| 7:37 am and 5:37 pm | News task | Scheduled Claude task, then `ingest_news.yml` | Searches the ten tier 2 publications only, uploads its hits and starts `ingest_news.yml`, which commits them to `data/inbox/YYYY-MM-DD/news.jsonl` |
| 7:45 am and 5:45 pm | News backup | `ingest_news.yml` | Picks up any uploaded news file whose start signal failed |
| 8:15 am daily | Triage and extraction | `triage.yml` | Discards hits with no money, commitment or credit support (reason logged), matches the rest to a relationship or marks them new, writes queue items, runs Claude Code headless to draft diffs inside the spend cap, checks every proposal, approves by rule what the rule allows and starts `publish.yml` |
| 8:45 am daily, 5:45 pm weekdays | Publish backup | `publish.yml` | Applies anything in `data/approved/` that an earlier start missed. Does nothing if nothing is approved |
| 8:57 am weekdays | Pending items summary | `triage.yml` (summary only) | Opens a GitHub issue listing the queue, with watcher alerts first. Sends nothing if the queue is empty and no watcher is in alert |
| On approval | Publish | `publish.yml` | Starts when a commit touches `data/approved/`. Applies the diff, rebuilds, checks, snapshots, builds the page, deploys |
| 6:30 am daily | Checks | `checks.yml` | Fixture tests, every automated check, and a dry run of approved items |
| Mondays 6:40 am | Link check | `checks.yml` | Opens an issue listing sources that no longer load |

### Watchers and their frequency

| Watcher | Frequency | Source |
|---|---|---|
| `nvda_filings` | Every 2 hours, weekdays 6 am to 10 pm. Hourly for the ten days after each Nvidia earnings date | SEC submissions for Nvidia |
| `counterparty_filings` | Every 4 hours, weekdays | SEC submissions for every entity with a CIK in `data/register/entities.json` |
| `ir_releases` | Every 4 hours | Company feeds in `config/watch_sources.json` |
| `fulltext_nvidia` | Daily, 7:10 am | EDGAR full-text search, queries Q1 to Q12, last 3 days, 50-word window |
| `ownership_filings` | Daily | Schedules 13D and 13G, Forms 3 and 4 on Nvidia's filing list |
| `ratings` | Daily | Public agency pages in `config/watch_sources.json`; pages behind a login are logged as "manual check needed" |
| `staleness` | Daily | Internal: amounts past the limits in `config/staleness.json` |
| `market_values` | Weekdays after the close (first run after 4:30 pm) | Yahoo Finance quote data, for listed holdings only |
| `nvda_13f` | Daily for 45 days after each quarter end, otherwise weekly | SEC submissions for Nvidia |
| `earnings_calendar` | Weekly | Results filings (Form 8-K item 2.02) and event pages in `config/watch_sources.json` |
| `liens` | Monthly | Companies House registers of charges; state UCC portals are logged as "manual check needed" |

Run state is in `data/inbox/_status.json`: last run, last success, warnings, manual checks. Three failures in a row for one watcher set an alert, which opens an issue and heads the 8:57 summary. A failed watcher is tried again at its next run. A blocked source is never replaced by a source that is not on the allowlist.

### Eastern time and UTC

GitHub's own cron runs in UTC and does not follow daylight saving. The cron lines in the workflows are written for standard time (UTC minus 5): 8:15 am is `15 13`, 8:57 am is `57 13`, 8:45 am is `45 13`, 5:45 pm is `45 22`, 6:30 am is `30 11`. In daylight time (UTC minus 4) those backup runs land one hour later by the Eastern clock. The hourly watcher trigger is not affected, because the watchers work out what is due in Eastern time themselves. cron-job.org is set to the America/New_York time zone, so its calls are right all year, and it is the primary trigger. GitHub's cron stays as the backup, because GitHub can skip scheduled runs.

All five workflows share the concurrency group `nvidia-update`, so they run one at a time and never collide on a push. GitHub keeps one run waiting per group: if two more are started while one is running, the older waiting run is dropped. Nothing is lost when that happens, because every job works from files (`data/inbox/`, `data/queue/`, `data/approved/`) and the next run or the backup picks them up.

## Run each part by hand

Set `SEC_USER_AGENT` first (a name and an email, as SEC.gov requires). It is never stored in the repository.

| Step | Command | Notes |
|---|---|---|
| Watchers | `make watch` | All watchers. `make watch ONLY=nvda_filings,ir_releases`, `make watch DUE=1` for the timetable, `make watch SINCE=2026-11-25` for a backfill |
| One watcher | `python3 -m pipeline.watchers.nvda_filings --since 2026-11-25` | Every watcher module takes `--since YYYY-MM-DD` |
| Watcher state | `python3 -m pipeline.watchers.run --status` | Last runs, failures, manual checks |
| News hits | `python3 -m pipeline.ingest_news hits.jsonl` | The prompt for the task is `pipeline/tasks/news_watch.md` |
| Triage | `make triage` | Needs no API key. Items wait as "needs extraction" until a diff is drafted |
| Extraction | Start `triage.yml` in GitHub, or follow `pipeline/tasks/triage_extract.md` in a Claude Code session, then `python3 -m pipeline.triage --merge` | Paid step; see the spend cap below |
| Review | `make review` | Opens `http://127.0.0.1:8765`. Approve, Edit then approve, Reject with reason, Hold, and the batch confirm screen. Approving commits `data/approved/<id>.json`; `git push` starts the publish |
| Apply and publish | `make apply` | Applies approved items, then runs `pipeline.build_register`, `pipeline.system_view`, `pipeline.publish`, `pipeline.build_site` in order. Stops on the first failure and puts everything back |
| Check approved items | `python3 -m pipeline.apply_approved --dry-run` | Writes nothing |
| Publish only | `make publish` | Rebuilds `data/published/` from the register, runs every check, snapshots to `data/history/` |
| Page only | `make site` | Writes `site/index.html` from `data/published/` |
| Checks | `make check` and `make test` | |

In GitHub: Actions, choose the workflow, Run workflow. `watch.yml` takes `watchers` (`due`, `all` or a list) and `since`; `triage.yml` takes `extract` and `summary_only`; `publish.yml` takes `force`.

## What needs a person

- Approved by rule, no person: `market_value` updates and `link_repair`. Nothing else (`config/auto_approve.json`).
- Always a person: any change to headline, committed total, funded or contingent maximum at any size; anything added; any change of status, reconciliation or dates; every correction; every re-verification; evidence that changes the claim basis.
- `last_verified` moves only on amounts a person re-checked. A market value update never moves it.
- A proposal that fails grounding stays in the queue marked "failed grounding" and cannot be approved.
- A paywalled article waits as "needs quote" until the sentence is pasted on the review page.

## One-time setup (Thomas)

1. **Public repository.** Create a public repository for the site (for example `nvidia-central-bank-site`). It receives only `site/` (at its root) and `data/published/`. This working repository stays private.
2. **Repository variable.** In this repository: Settings, Secrets and variables, Actions, Variables, add `PUBLIC_REPO` with the value `owner/name` of the public repository.
3. **Fine-grained token.** GitHub, Settings, Developer settings, Fine-grained tokens. Limit it to the two repositories. Permissions: Actions read and write, Contents read and write. Use it in two places: as the secret `PUBLIC_REPO_TOKEN` in this repository (it pushes the site), and as the bearer token in cron-job.org (it starts the workflows).
4. **Secrets.** Settings, Secrets and variables, Actions, Secrets:
   - `SEC_USER_AGENT`: a name and an email, for example `Resolute Business Development name@example.com`.
   - `ANTHROPIC_API_KEY`: the key the extraction step uses.
   - `PUBLIC_REPO_TOKEN`: the token from step 3.
   None of these is ever committed.
5. **Spend cap.** Set `monthly_usd_cap` in `config/limits.json`. While it is null the paid extraction step does not run and items wait as "needs extraction". When the month's spend reaches the cap the step stops and an issue is opened. Spend is tracked in `data/queue/_spend.json`.
6. **GitHub Pages.** In the public repository: Settings, Pages, deploy from the `main` branch, root folder. Custom domain `nvidia.resolute-bd.com`; turn on Enforce HTTPS once the certificate is issued. The first publish writes the `CNAME` file.
7. **DNS (Squarespace, like economy.resolute-bd.com).** Add a CNAME record: host `nvidia`, value `<owner>.github.io`.
8. **cron-job.org.** Time zone America/New_York. Each job is a POST to `https://api.github.com/repos/<owner>/<private repo>/actions/workflows/<file>/dispatches` with headers `Authorization: Bearer <token>`, `Accept: application/vnd.github+json`, `Content-Type: application/json`:

   | Job | Schedule | File | Body |
   |---|---|---|---|
   | Watchers | Every hour at minute 10 | `watch.yml` | `{"ref":"main","inputs":{"watchers":"due"}}` |
   | Triage | Daily 8:15 am | `triage.yml` | `{"ref":"main"}` |
   | Publish backup | Daily 8:45 am; weekdays 5:45 pm | `publish.yml` | `{"ref":"main"}` |
   | Summary | Weekdays 8:57 am | `triage.yml` | `{"ref":"main","inputs":{"summary_only":"true"}}` |
   | Checks | Daily 6:30 am | `checks.yml` | `{"ref":"main"}` |

9. **News task.** Create a scheduled Claude task at 7:37 am and 5:37 pm Eastern with the prompt in `pipeline/tasks/news_watch.md`. It needs permission to add a file to the branch `news-uploads` of this repository and to start `ingest_news.yml`. Create the empty branch `news-uploads` once.
10. **Notifications.** Watch this repository for issues, so the 8:57 summary, watcher alerts, a stopped publish and the spend cap alert reach your inbox.
11. **Sources to fill in** (`config/watch_sources.json`): Nvidia's next earnings date when announced, release feeds for counterparties, Companies House numbers for UK counterparties, and any public rating agency pages. Until a source is listed the watcher logs "manual check needed" rather than guessing.
12. **Before the first publish (Gate Q).** Run every watcher and the news task in backfill mode from the Gate R cutoff: `make watch SINCE=<cutoff>`, then `make triage`, then resolve every queue item on the review page.

## If something fails

- A watcher fails: it is retried at the next run. Three failures in a row open an issue.
- A check fails during publish: the publish stops, everything it changed is put back, an issue is opened, and the live site keeps the last good publish. Fix or reject the approved item, then run `make apply` or start `publish.yml`.
- The spend cap is reached: extraction stops until next month or a higher cap. Watchers, triage, review and publishing carry on.
