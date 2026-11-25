# The Central Bank of AI

Working repository for **"Is Nvidia the Central Bank of AI?"**, a sourced map of every financial relationship in which Nvidia supplies capital, credit support or demand support to the AI buildout.

Built by Resolute Business Development. Not investment advice.

## Status

| Phase | State |
|---|---|
| R research | Done: 93 records, about 1,300 citations, three critic rounds, independent re-sourcing |
| Gate R | Approved by Thomas, 25 November 2026 |
| B application | Built: `site/index.html`, generated from `data/published/` |
| U continuous update | Built: watchers, triage, review page, apply, workflows (`SCHEDULE.md`) |
| Q final checks | Freshness check against filings to 25 November 2026; design critique fixed and re-tested in the browser |
| Go live | Needs Thomas's one-time setup in `SCHEDULE.md` (public repository, DNS, secrets, scheduler) |

## Layout

`spec/` the build package. `pipeline/` tools. `schema/` and `config/` rules. `research/` plans, reports, cache. `data/register/` the register. `tests/` fixture tests.

## Commands

```
make test                         tests
make check                        every automated check on the register
python3 -m pipeline.build_register   assemble the register from research drafts
python3 -m pipeline.system_view      totals, bridge, concentrations, scenarios
python3 -m pipeline.datapack         Excel evidence pack
```

Continuous update (spec/11): `make watch`, `make triage`, `make review`, `make apply`, `make publish`, `make site`. The timetable, how to run each part by hand and the one-time setup are in `SCHEDULE.md`.

SEC requests need the environment variable `SEC_USER_AGENT` (a name and an email). It is never stored in this repository.
