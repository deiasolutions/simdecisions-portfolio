# SPEC: Fix E2E test server startup timeout (28 errors)

## Priority
P0.93

## Model Assignment
sonnet

## Objective
Debug and fix E2E test fixture that fails to start hivenode subprocess, causing ConnectTimeout errors.

## Task File
`.deia/hive/tasks/2026-03-16-TASK-R16-fix-e2e-server-fixture.md`

## Acceptance Criteria
- [ ] E2E test server starts successfully
- [ ] 28 E2E tests pass (or pre-existing failures documented)
- [ ] No regressions
