---
id: REFACTOR-053
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-051
---
# SPEC-REFACTOR-053: Generate FUNCTIONALITY-REPORT.md

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-051

## Intent
Generate a test pass/fail report for every retained feature. This feeds the functionality gate.

## Files to Read First
- `.deia/hive/refactor/VALIDATION-POST.json`
- `.deia/hive/refactor/validation-diff.json`
- `.deia/hive/refactor/retention-data.json` (from REFACTOR-052 if available, otherwise use FEATURE-MANIFEST)

## Acceptance Criteria
- [ ] File created: `.deia/hive/FUNCTIONALITY-REPORT.md` with:
  - Header line: `Functionality: X.XX` (decimal ratio)
  - Table: every retained feature with test status PASS / FAIL / SKIP
  - Failure details for any FAIL
  - Summary stats
- [ ] File created: `.deia/hive/refactor/functionality-data.json` — machine-readable

## Constraints
- You are in EXECUTE mode. Write the report. Do NOT enter plan mode.
- No code changes
- No git operations
