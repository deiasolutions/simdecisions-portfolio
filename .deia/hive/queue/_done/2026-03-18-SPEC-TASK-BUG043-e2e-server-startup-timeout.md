# SPEC-TASK-BUG043: Fix E2E Server Startup Timeout

**Priority:** P0
**Model:** Sonnet
**Estimated Complexity:** Medium (investigation + fix)
**Created:** 2026-03-18

---

## Objective

Debug and fix E2E server startup failure causing all 28 integration tests in test_e2e.py to timeout with httpx.ConnectTimeout.

---

## Context

From the full test sweep (.deia/hive/responses/20260318-FULL-TEST-SWEEP-REPORT.md):

**All 28 E2E integration tests are failing:**
- Error: httpx.ConnectTimeout: timed out
- Pattern: Server never responds to health check during test setup within 10 seconds
- Affected tests: test_health_returns_ok_status, test_status_returns_node_info, and 25 others

**Root cause hypothesis:**
The E2E server startup failure is almost certainly related to BUG-042 (BUS signature change). The test sweep shows 58+ tests failing with:
TypeError: BUS.__init__() missing 1 required positional argument: 'ledger_publisher'

This error affects:
- Governance tests (16 failures)
- Dispositions tests (17 failures)
- Heartbeat tests (15 failures)
- Cloud storage E2E tests (13 errors)
- E2E integration tests (28 timeouts)

The E2E tests timeout because the hivenode server crashes during initialization when it tries to create a BUS instance without the required ledger_publisher argument.

---

## Files to Read First

### E2E test infrastructure:
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_e2e.py

### Server initialization:
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py

---

## Investigation Steps

### Phase 1: Capture actual startup error

1. Run ONE E2E test with enhanced logging
2. Capture server logs from the test fixture
3. If test times out, manually test server startup

### Phase 2: Locate BUS class or equivalent

1. Search for BUS class definition
2. Search for BUS imports in tests
3. Search for ledger_publisher parameter
4. Check if BUS is an alias or was renamed

### Phase 3: Fix the root cause

Fix based on findings from Phase 1 and 2.

---

## Deliverables

- [ ] Identify exact error causing E2E server startup failure
- [ ] Locate BUS class or confirm it doesn't exist
- [ ] Implement fix
- [ ] Verify all 28 E2E tests pass after fix
- [ ] Run governance tests to ensure no regressions (16 tests)
- [ ] Run dispositions tests to ensure no regressions (17 tests)
- [ ] Run heartbeat tests to ensure no regressions (15 tests)

---

## Test Requirements

After implementing fix:

- 28 E2E tests: all pass (no timeouts)
- 16 governance tests: all pass (no BUS errors)
- 17 dispositions tests: all pass (no BUS errors)
- 15 heartbeat tests: all pass (no BUS errors)

Total: 76 tests passing that are currently failing

---

## Acceptance Criteria

- [ ] All 28 E2E tests in test_e2e.py pass (no timeouts)
- [ ] Server starts successfully in E2E test fixture within 10 seconds
- [ ] All governance tests pass (16 tests)
- [ ] All dispositions tests pass (17 tests)
- [ ] All heartbeat tests pass (15 tests)
- [ ] No new test failures introduced
- [ ] Root cause documented in response file

---

## Response Requirements

Write: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-SPEC-BUG043-RESPONSE.md

Must contain 8 sections: Header, Files Modified, What Was Done, Test Results, Build Verification, Acceptance Criteria, Clock/Cost/Carbon, Issues/Follow-ups.

---

**END OF SPEC**
