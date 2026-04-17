---
id: REFACTOR-062
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-061
---
# SPEC-REFACTOR-062: Gate Enforcement — Pass or Fail

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-061

## Intent
Read gate results. If BOTH gates pass, mark the pipeline as successful. If either fails, mark as failed and generate a failure analysis.

## Files to Read First
- `.deia/hive/refactor/gate-results.json`
- `.deia/hive/RETENTION-REPORT.md`
- `.deia/hive/FUNCTIONALITY-REPORT.md`

## Acceptance Criteria
- [ ] Read retention_rate and functionality_rate from gate-results.json
- [ ] IF retention >= 0.80 AND functionality >= 0.95:
  - Write `pipeline_status: PASSED` to gate-results.json
  - Generate `.deia/hive/refactor/PIPELINE-PASSED.md` with summary
- [ ] IF either gate fails:
  - Write `pipeline_status: FAILED` to gate-results.json
  - Generate `.deia/hive/refactor/PIPELINE-FAILED.md` with:
    - Which gate(s) failed
    - Top regressions causing failure
    - Recommended fixes
  - Do NOT proceed to REFACTOR-063

## Constraints
- You are in EXECUTE mode. Evaluate and write. Do NOT enter plan mode.
- No code changes
- No git operations
