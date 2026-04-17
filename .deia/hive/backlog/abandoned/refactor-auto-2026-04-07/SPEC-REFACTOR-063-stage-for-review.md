---
id: REFACTOR-063
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-062
---
# SPEC-REFACTOR-063: Stage Branch for Morning Review

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-062

## Intent
If the pipeline passed (REFACTOR-062 wrote PIPELINE-PASSED.md), commit all remaining changes, push the branch, and generate a morning briefing document.

## Files to Read First
- `.deia/hive/refactor/gate-results.json` — must have `pipeline_status: PASSED`
- `.deia/hive/refactor/PIPELINE-PASSED.md` — must exist
- `.deia/hive/RETENTION-REPORT.md`
- `.deia/hive/FUNCTIONALITY-REPORT.md`

## Acceptance Criteria
- [ ] ONLY proceed if `pipeline_status == PASSED` in gate-results.json
- [ ] If FAILED: write "Pipeline failed — branch not staged" and exit
- [ ] If PASSED:
  - Commit all outstanding changes on `refactor/auto-2026-04-07`
  - Push branch to origin
  - Generate `.deia/hive/coordination/2026-04-08-MORNING-REFACTOR-BRIEFING.md` with:
    - Retention rate and functionality rate
    - Summary of changes per phase
    - List of dropped features with justifications
    - List of new/completed features
    - Recommendation: merge or review further
- [ ] Console output: `REFACTOR PIPELINE COMPLETE. Branch ready for review.`

## Constraints
- You are in EXECUTE mode. Do NOT enter plan mode.
- ONLY push if pipeline passed. Safety first.
- Commit message: `[REFACTOR] Autonomous overnight refactor — retention X.XX, functionality X.XX`
