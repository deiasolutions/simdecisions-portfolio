# TASK-W1-D: Slot reservation integration smoke test

## Objective
Write and execute an end-to-end smoke test that validates the full slot reservation protocol: hivenode endpoints + queue runner polling + regent workflow (simulated).

This test ensures that all 3 components (TASK-W1-A, TASK-W1-B, TASK-W1-C) work together correctly.

## Context
After TASK-W1-A (hivenode endpoints), TASK-W1-B (queue runner polling), and TASK-W1-C (regent protocol doc), we need to verify the integration works end-to-end.

The test scenario:
1. Hivenode starts with capacity = 10
2. Regent reserves 8 slots for spec-1
3. Queue runner submits spec-1 (slot available)
4. Queue runner tries to submit spec-2 (only 2 slots available, but spec-2 might need more → queue waits)
5. Regent releases 1 slot (spec-1's first bee done)
6. Queue runner sees slot freed, submits spec-2 if now eligible
7. Regent releases remaining 7 slots (spec-1 all bees done)
8. Queue runner sees all slots free, proceeds

This can be a manual test script (bash + curl) OR an automated Python test. Choose based on what's faster to implement.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` — slot endpoints
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` — queue runner with slot polling
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\processes\P-10-SLOT-RESERVATION.md` — regent protocol doc (written by TASK-W1-C)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_e2e.py` — existing E2E test pattern (if writing automated test)

## Deliverables

Choose ONE approach (manual script OR automated test):

### Option A: Manual Smoke Test Script (bash + curl)
- [ ] Create file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\smoke\slot-reservation-smoke.sh`
- [ ] Script steps:
  1. Start hivenode in background (`cd hivenode && python -m uvicorn main:app --reload &`)
  2. Wait for health check (`curl http://localhost:8000/health` until 200)
  3. Check initial slot status (`curl http://localhost:8000/build/slot-status`)
  4. Reserve 8 slots for spec-1 (`curl -X POST http://localhost:8000/build/slot-reserve -d '{"spec_id": "spec-1", "bee_count": 8}'`)
  5. Check slot status (expect: `reserved=8, available=2`)
  6. Release 1 slot for spec-1 (`curl -X POST http://localhost:8000/build/slot-release -d '{"spec_id": "spec-1", "released": 1}'`)
  7. Check slot status (expect: `reserved=7, available=3`)
  8. Release remaining 7 slots (`curl -X POST http://localhost:8000/build/slot-release -d '{"spec_id": "spec-1", "released": 7}'`)
  9. Check slot status (expect: `reserved=0, available=10`)
  10. Kill hivenode process
- [ ] Script prints PASS/FAIL for each step
- [ ] README.md in `smoke/` explaining how to run the script

### Option B: Automated Python Test (pytest)
- [ ] Create file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_slot_integration.py`
- [ ] Test function: `test_slot_reservation_integration_flow()`
- [ ] Steps (same as Option A, but using `httpx` or `TestClient`):
  1. Start test server (use `TestClient` from FastAPI)
  2. Check initial slot status
  3. Reserve 8 slots for spec-1
  4. Assert `reserved=8, available=2`
  5. Release 1 slot
  6. Assert `reserved=7, available=3`
  7. Release remaining 7 slots
  8. Assert `reserved=0, available=10`
- [ ] Test should be runnable via `pytest tests/hivenode/test_slot_integration.py -v`

### Option C: Queue Runner Integration (more realistic, but longer)
- [ ] Create 3 dummy spec files in `.deia/hive/smoke/specs/`:
  - `spec-1.md` with `## Bee Count: 8`
  - `spec-2.md` with `## Bee Count: 3`
  - `spec-3.md` with `## Bee Count: 2`
- [ ] Run queue runner in dry-run mode: `python .deia/hive/scripts/queue/run_queue.py --queue-dir .deia/hive/smoke/specs --dry-run`
- [ ] Manually simulate regent actions:
  1. Reserve 8 slots for spec-1
  2. Run queue runner (it should see only 2 slots available, wait)
  3. Release 1 slot
  4. Queue runner should proceed
  5. Release remaining slots
- [ ] Document the test scenario in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\smoke\SLOT-RESERVATION-INTEGRATION.md`

**Choose Option A (manual script) — fastest to implement and sufficient for smoke test.**

## Test Requirements
- [ ] Smoke test executes without errors
- [ ] All assertions pass (slot counts match expected values)
- [ ] Hivenode slot state persists across test steps
- [ ] Test is repeatable (can run multiple times)

## Constraints
- No file over 500 lines
- Clear pass/fail output
- Documented steps (README or inline comments)
- Runnable by a human or CI (if automated)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-W1-D-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — smoke test output (PASS/FAIL for each step)
5. **Build Verification** — N/A for smoke tests, but confirm script executes
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Model Assignment
**Haiku** — execute test scenario.

## Success Criteria
- Smoke test script/test exists and is documented
- Test passes (all steps return expected slot counts)
- Test is repeatable
- README or inline docs explain how to run it
