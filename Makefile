.PHONY: check test eligibility measure evidence all watch triage review apply publish site
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

# ---- continuous update (spec/11; timetable and setup in SCHEDULE.md)

watch:            ## run the watchers into data/inbox (ONLY=nvda_filings,ir_releases  SINCE=2026-11-25  DUE=1 for the timetable)
	$(PY) -m pipeline.watchers.run $(if $(DUE),--due) $(if $(ONLY),--only $(ONLY)) $(if $(SINCE),--since $(SINCE))

triage:           ## inbox to review queue; merges extracted diffs; needs no API key
	$(PY) -m pipeline.triage

review:           ## open the local review page (Approve, Edit then approve, Reject, Hold, batch confirm)
	$(PY) -m pipeline.review

apply:            ## apply data/approved, then rebuild, check, publish and build the page; stops on the first failure
	$(PY) -m pipeline.apply_approved

publish:          ## rebuild data/published from the register, run every check, snapshot
	$(PY) -m pipeline.publish

site:             ## write site/index.html from data/published
	$(PY) -m pipeline.build_site
