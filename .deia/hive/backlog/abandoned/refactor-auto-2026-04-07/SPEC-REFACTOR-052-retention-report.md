---
id: REFACTOR-052
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-051
---
# SPEC-REFACTOR-052: Generate RETENTION-REPORT.md

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-051

## Intent
Generate a feature-by-feature retention report. For every feature in FEATURE-MANIFEST.json, state whether it was RETAINED, IMPROVED, or DROPPED — with justification for every drop.

## Files to Read First
- `.deia/hive/refactor/FEATURE-MANIFEST.json`
- `.deia/hive/refactor/validation-diff.json`
- `.deia/hive/refactor/dead-code-removals.json`
- `.deia/hive/refactor/changes-*.json` (all change logs)

## Acceptance Criteria
- [ ] File created: `.deia/hive/RETENTION-REPORT.md` with:
  - Header line: `Retention: X.XX` (decimal ratio)
  - Table: every feature with status RETAINED / IMPROVED / DROPPED
  - Every DROPPED feature has explicit justification
  - Summary stats
- [ ] File created: `.deia/hive/refactor/retention-data.json` — machine-readable version

## Constraints
- You are in EXECUTE mode. Write the report. Do NOT enter plan mode.
- Every drop MUST have justification. No silent removals.
- No code changes
- No git operations
