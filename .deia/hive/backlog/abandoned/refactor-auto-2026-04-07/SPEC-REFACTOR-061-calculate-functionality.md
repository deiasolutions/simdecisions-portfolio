---
id: REFACTOR-061
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-060
---
# SPEC-REFACTOR-061: Calculate Functionality Rate

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-060

## Intent
Calculate the final functionality rate: tests passing / tests run (for retained features only).

## Files to Read First
- `.deia/hive/refactor/functionality-data.json`
- `.deia/hive/refactor/gate-results.json`

## Acceptance Criteria
- [ ] Functionality rate calculated: tests_passing / (tests_passing + tests_failing)
- [ ] Result appended to `.deia/hive/refactor/gate-results.json` with field `functionality_rate`
- [ ] Console output: `FUNCTIONALITY: X.XX (threshold: 0.95)`
- [ ] If < 0.95: `FUNCTIONALITY GATE: FAILED`
- [ ] If >= 0.95: `FUNCTIONALITY GATE: PASSED`

## Constraints
- You are in EXECUTE mode. Calculate and write. Do NOT enter plan mode.
- No code changes
- No git operations
