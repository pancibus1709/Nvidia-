.PHONY: check test eligibility measure evidence all
PY ?= python3

check:            ## every automated check in spec/09 on the register and the published build
	$(PY) -m pipeline.checks

test:             ## fixture tests for the checks, measures and scenarios
	$(PY) -m pytest -q tests

evidence:         ## fold research evidence into the canonical store
	$(PY) -m pipeline.merge_evidence

eligibility:      ## write display_eligible on every amount (the only place it is set)
	$(PY) -m pipeline.checks eligibility

measure:          ## recompute derived measures and significance
	$(PY) -m pipeline.measure

all: evidence measure check test
