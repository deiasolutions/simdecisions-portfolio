---
id: REFACTOR-051
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-050
---
# SPEC-REFACTOR-051: Compare VALIDATION-POST to VALIDATION-BASELINE

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-050

## Intent
Diff the pre-refactor and post-refactor validation results. Identify regressions (was passing, now failing), improvements (was failing, now passing), and unchanged.

## Files to Read First
- `.deia/hive/refactor/VALIDATION-BASELINE.json`
- `.deia/hive/refactor/VALIDATION-POST.json`

## Acceptance Criteria
- [ ] File created: `.deia/hive/refactor/validation-diff.json` with:
  - `regressions` — features that were passing, now failing
  - `improvements` — features that were failing, now passing
  - `unchanged_pass` — still passing
  - `unchanged_fail` — still failing
  - `new_features` — features that didn't exist before
- [ ] If regressions > 0: list each with root cause analysis

## Constraints
- You are in EXECUTE mode. Write the diff. Do NOT enter plan mode.
- Read-only — no code changes
- No git operations
