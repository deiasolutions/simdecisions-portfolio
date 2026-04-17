# TASK-067: Build Monitor Integration Tests

**Spec ID:** QUEUE-TEMP-2026-03-13-2010-SPEC-build-monitor-fixes
**Model:** sonnet
**Priority:** P0
**Depends on:** TASK-063, TASK-064, TASK-065, TASK-066

---

## Objective

Add integration tests covering the full build monitor stack: backend heartbeat → SSE stream → frontend display. Verify all existing tests still pass.

---

## Files to Read

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_build_monitor.py` — backend tests
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\buildMonitorAdapter.test.tsx` — frontend tests

---

## Deliverables (absolute paths)

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_build_monitor.py` — MODIFIED (if adding backend integration tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\buildMonitorAdapter.test.tsx` — MODIFIED (verify all tests pass)

---

## Acceptance Criteria

### Backend integration tests (test_build_monitor.py)
- [ ] Test heartbeat with tokens → verify tokens appear in get_status response
- [ ] Test multiple heartbeats → verify token totals accumulate correctly
- [ ] Test SSE stream includes token data in heartbeat events
- [ ] Test SSE snapshot includes `total_input_tokens` and `total_output_tokens`

### Frontend tests (buildMonitorAdapter.test.tsx)
- [ ] All existing tests pass (from TASK-064, TASK-065, TASK-066)
- [ ] Add 1+ integration test: mock SSE snapshot with tokens → verify header displays totals
- [ ] Add 1+ integration test: mock SSE heartbeat with tokens → verify log entry displays tokens

### Full test suite (all repos)
- [ ] Run `pytest tests/hivenode/test_build_monitor.py` → all pass
- [ ] Run `npm test -- buildMonitorAdapter.test.tsx` → all pass
- [ ] Run full hivenode test suite → no regressions
- [ ] Run full browser test suite → no regressions

---

## Test Requirements Summary (from spec)

Total new tests across all tasks:
- **5+ tests** for token formatting helper (TASK-065)
- **2+ tests** for timestamp formatting (TASK-064)
- **1+ test** for elapsed time formatting (TASK-066)
- **4+ tests** for backend token accumulation (TASK-063)
- **2+ tests** for frontend integration (this task)

**Total: 14+ new tests**

---

## Constraints

- Do NOT change any application code in this task — only add tests
- All tests must pass on first run after implementation tasks are complete
- Use existing test patterns (pytest for backend, vitest/jest for frontend)

---

## Test Protocol

1. Run all backend tests: `pytest tests/hivenode/test_build_monitor.py -v`
2. Run all frontend tests: `npm test -- buildMonitorAdapter.test.tsx`
3. If any fail, identify root cause (implementation bug or test bug)
4. Fix tests or report implementation issues
5. Re-run until all green

---

## Definition of Done

- [ ] All acceptance criteria met
- [ ] 2+ new integration tests written and passing
- [ ] All existing tests passing (backend + frontend)
- [ ] Full test suite green (hivenode + browser)
- [ ] Response file written to `.deia/hive/responses/`
- [ ] Task archived to `.deia/hive/tasks/_archive/`
- [ ] Feature inventory updated: `python _tools/inventory.py add --id FEAT-BUILD-MONITOR-TOKENS-001 --title 'Build Monitor Token Tracking' --task TASK-063,TASK-064,TASK-065,TASK-066,TASK-067 --layer integration --tests 14`
- [ ] Feature inventory exported: `python _tools/inventory.py export-md`
