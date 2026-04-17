---
id: REFACTOR-060
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-052
  - REFACTOR-053
---
# SPEC-REFACTOR-060: Calculate Retention Rate

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-052
- REFACTOR-053

## Intent
Calculate the final retention rate: features present in post-refactor / features in baseline manifest.

## Files to Read First
- `.deia/hive/refactor/retention-data.json`
- `.deia/hive/refactor/FEATURE-MANIFEST.json`

## Acceptance Criteria
- [ ] Retention rate calculated: (RETAINED + IMPROVED) / total_baseline_features
- [ ] Result written to `.deia/hive/refactor/gate-results.json` with field `retention_rate`
- [ ] Console output: `RETENTION: X.XX (threshold: 0.80)`
- [ ] If < 0.80: `RETENTION GATE: FAILED`
- [ ] If >= 0.80: `RETENTION GATE: PASSED`

## Constraints
- You are in EXECUTE mode. Calculate and write. Do NOT enter plan mode.
- No code changes
- No git operations
