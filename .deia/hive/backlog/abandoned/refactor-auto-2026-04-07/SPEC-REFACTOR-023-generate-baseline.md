---
id: REFACTOR-023
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-020
  - REFACTOR-021
  - REFACTOR-022
---
# SPEC-REFACTOR-023: Generate VALIDATION-BASELINE.json

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-020
- REFACTOR-021
- REFACTOR-022

## Intent
Consolidate all test results from Phase 1 into a single VALIDATION-BASELINE.json. This is the pre-refactor snapshot that Phase 4 will compare against.

## Files to Read First
- `.deia/hive/refactor/test-results-systems.json`
- `.deia/hive/refactor/test-results-sets.json`
- `.deia/hive/refactor/test-results-routes.json`

## Acceptance Criteria
- [ ] File created: `.deia/hive/refactor/VALIDATION-BASELINE.json` with:
  - `generated_at` timestamp
  - `systems` — merged from test-results-systems.json
  - `sets` — merged from test-results-sets.json
  - `routes` — merged from test-results-routes.json
  - `summary`: total_tested, total_passing, total_failing, total_skipped
  - `pass_rate`: (passing / (passing + failing))
- [ ] File created: `.deia/hive/refactor/VALIDATION-BASELINE-SUMMARY.md` — human-readable

## Constraints
- You are in EXECUTE mode. Write all output files. Do NOT enter plan mode.
- Read-only — no code changes
- No git operations
