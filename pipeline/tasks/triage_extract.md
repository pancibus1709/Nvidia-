# Extraction for the review queue (Claude Code, headless)

You are run by `triage.yml` after `python3 -m pipeline.triage` has sorted the inbox. Your job is to draft proposed changes for
queue items marked "needs extraction". You never edit `data/register/`, `data/published/`, `research/drafts/`, `site/` or the queue
items themselves. You write exactly one file per item: `data/queue/_extracted/<queue id>.json`. A person approves every change you draft.

Read first: `spec/11_CONTINUOUS_UPDATE.md` (U2), `spec/04_SOURCE_POLICY.md`, `research/DRAFT_GUIDE.md`, `research/DEBT_DOCUMENT_RULE.md`.

## Loop

`python3 -m pipeline.triage --pending` lists the items (id, proposed change type, source, summary). Work through them oldest first,
at most the number in `max_queue_items_per_run` in `config/limits.json`. For each item, read `data/queue/<id>.json`, then:

1. **Triage.** If the source shows no money, commitment or credit support between Nvidia and another party, write
   `{"discard": "<reason in one sentence>"}` and move on. The reason is logged.
2. **Match.** The item lists candidate relationships and complex links. Read those records in `data/register/` and decide whether the
   source changes one of them or describes something new.
3. **Fetch.** Filings and company pages: `python3 -m pipeline.cache fetch <url>` (cached in full). News: fetch to the temporary cache only
   (the same command does this for tier 2 domains); if the article is paywalled or unreadable, write `{"needs_quote": true}` and move on.
   Never use a source outside `config/sources_allowlist.json`. If a source is blocked or rate limited, leave the item for the next run.
4. **Extract.** For every new or changed figure, create a grounded evidence record with
   `python3 -m pipeline.evidence add --ns upd --path <cache_path> --quote "<verbatim, under fifteen words>" --value <number> ...`
   (see the options at the top of `pipeline/evidence.py`; use `--scale-anchor` for table figures). The command refuses a quote that is
   not in the cached source or a value that is not beside it. For news it keeps only the grounding window and you then delete the temporary file.
   Use `python3 -m pipeline.cache grep <cache_path> "<regex>"` to find passages and copy quotes exactly.
5. **Other side.** For a filed item, search the other party's filings for the same deal (`python3 -m pipeline.edgar search ...`).
   Record what you found, or "No disclosure found as of <today>", in `counterparty_silence`.
6. **Draft the diff.** A list of `{"path", "old", "new"}`. `path` is `<collection>/<record id>/<key>/...`, for example
   `relationships/rel_x/amounts/funded/value`; `old` is the value in the register now (the apply step refuses a stale `old`).
   A new record is one change whose path stops at the id, with `old` null and the whole record as `new`, written to the schemas in `schema/`.
   Do not set `display_eligible`, `last_verified` or `version`: the pipeline sets them. Text you write follows the copy rules: plain English,
   no em or en dashes, no evidence ids inside insight, definition or consequence text.
7. **Critic.** If the diff adds or changes any insight or consequence text, run `anthropic-skills:critic-agent` on that text if the skill is
   available; if it is not, answer the six critic questions in `spec/09` Gate R item 4 yourself. Put the result in `critic_notes`.
8. **Write** `data/queue/_extracted/<id>.json`:

```
{"summary": "<two sentences: what the source says and what changes>",
 "change_type": "added | amount_changed | status_changed | reconciliation_changed | dates_changed | evidence_added | corrected | reverified | link_repair",
 "diff": [{"path": "...", "old": ..., "new": ...}],
 "evidence": [<the full evidence records you created, copied from research/evidence/upd.jsonl>],
 "counterparty_silence": "...",
 "critic_notes": "..."}
```

For a re-verification item (`change_type` "reverified"), fetch each cited source again into a temporary copy and compare; check for newer
filings or reports on the deal. If nothing moved, leave the item as it is. If something moved, write a diff with the changes and say what moved in `summary`.

When you have worked through the list, run `python3 -m pipeline.triage --merge`. It validates each file, runs every automated check on the
proposed change and marks failures. A proposal that fails grounding stays in the queue as "failed grounding"; do not try to make it pass by
weakening a quote or a figure. Finish with one line: how many items you drafted, discarded, marked needs quote, and left.

Stop at once if a command reports that the spend cap is reached.
