# BRIEFING: Fix E2E Server Startup Timeout

**Date:** 2026-03-16
**Priority:** P0.93
**Model Assignment:** sonnet
**Spec:** `.deia/hive/queue/2026-03-16-1103-SPEC-fix-R16-e2e-server-fixture.md`

---

## Objective

Debug and fix the E2E test fixture that fails to start the hivenode subprocess, causing ConnectTimeout errors in 28 E2E tests.

## Context from Q88N

The E2E test suite is experiencing widespread failures due to the test server not starting properly. This is a P0 issue blocking further E2E test work.

## Current State

- 28 E2E tests are failing with ConnectTimeout errors
- Root cause: hivenode subprocess fails to start in test fixture
- This is blocking all E2E test validation

## What Q33N Must Deliver

Write a task file for a sonnet bee to:

1. **Investigate the E2E test fixture** - identify why the hivenode subprocess fails to start
2. **Fix the startup issue** - ensure the server starts successfully in test context
3. **Verify all 28 tests** - document which tests now pass, which have pre-existing failures
4. **No regressions** - ensure existing passing tests remain green

## Relevant File Paths

Start investigation here:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_e2e.py` (E2E test file)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (hivenode server entry point)
- Any pytest fixtures related to server startup

## Constraints

- Hard Rule 5: TDD - tests first
- Hard Rule 6: NO STUBS - full implementation
- Hard Rule 4: No file over 500 lines
- Model: sonnet (as specified in spec)

## Acceptance Criteria from Spec

- [ ] E2E test server starts successfully
- [ ] 28 E2E tests pass (or pre-existing failures documented)
- [ ] No regressions

## Task File Destination

`.deia/hive/tasks/2026-03-16-TASK-R16-fix-e2e-server-fixture.md`

---

## Instructions for Q33N

1. Read the E2E test file and related fixtures
2. Identify the root cause of the subprocess startup failure
3. Write ONE task file for a sonnet bee
4. Include specific investigation steps in the task
5. Return task file for Q33NR review BEFORE dispatching
