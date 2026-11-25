# The Central Bank of AI

Working repository for **"Is Nvidia the Central Bank of AI?"**, a sourced map of every financial relationship in which Nvidia supplies capital, credit support or demand support to the AI buildout.

Built by Resolute Business Development. Not investment advice.

## Status

| Phase | State |
|---|---|
| R0 research tooling and checks | Done |
| R1 to R9 research | Done: 92 records, 1,094 citations, three critic rounds |
| Gate R | Waiting for Thomas's approval. See `research/GATE_R_SUMMARY.md` |
| B, U, Q | Not started. No application code is written before approval |

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
