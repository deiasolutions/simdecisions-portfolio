# SPEC: Full integration test verification after rebuild

## Priority
P0.85

## Model Assignment
sonnet

## Objective
Run the entire hivenode and browser test suites to verify all 16 rebuild tasks restored functionality without cross-task regressions.

## Task File
`.deia/hive/tasks/2026-03-15-TASK-R13-full-integration-verify.md`

## Acceptance Criteria
- [ ] `python -m pytest tests/hivenode/ -v` — all tests pass (target: 969+)
- [ ] `cd browser && npx vitest run` — all tests pass (target: 1122+)
- [ ] No import errors across any module
- [ ] Any regressions documented and fixed
- [ ] Final pass/fail counts reported by module
