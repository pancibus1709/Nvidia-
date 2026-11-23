# The Central Bank of AI

Working repository for **"Is Nvidia the Central Bank of AI?"**, a sourced map of every financial relationship in which Nvidia supplies capital, credit support or demand support to the AI buildout.

Built by Resolute Business Development. Not investment advice.

## Status

| Phase | State |
|---|---|
| R0 research tooling and checks | Done |
| R1 to R9 research | Waiting for the SEC contact string |
| Gate R | Needs Thomas's approval before any app code |
| B, U, Q | Not started |

## Layout

`spec/` the build package. `pipeline/` tools. `schema/` and `config/` rules. `research/` plans, reports, cache. `data/register/` the register. `tests/` fixture tests.

## Commands

```
make test     fixture tests
make check    every automated check on the register
```

SEC requests need the environment variable `SEC_USER_AGENT` (a name and an email). It is never stored in this repository.
