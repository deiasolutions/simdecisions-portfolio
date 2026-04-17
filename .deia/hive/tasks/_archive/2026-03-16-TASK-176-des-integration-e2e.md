# TASK-176: DES Backend Integration E2E Test

## Objective
Write end-to-end integration test verifying flow designer → backend DES engine → results display pipeline, and verify no regressions.

## Context
TASK-174 created the `desClient` service. TASK-175 wired it into `useSimulation`. This task verifies the full pipeline works end-to-end:

1. User loads FlowDesigner with a flow
2. User clicks "Simulate" mode (triggers `useSimulation.start()`)
3. Frontend calls `POST /api/des/run` with flow data
4. Backend processes simulation
5. Backend returns `RunResponse` with events and statistics
6. Frontend displays results in ProgressPanel and ResultsPreview

This is a **verification task** — no new production code, only tests.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\simulation\useSimulation.ts` (modified in TASK-175)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\services\desClient.ts` (created in TASK-174)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py` (backend routes)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_des_routes.py` (backend tests)

## Deliverables

### 1. E2E Integration Test
- [ ] Load `FlowDesigner` component with a simple test flow (2 nodes, 1 edge)
- [ ] Simulate user clicking "Simulate" mode pill in toolbar
- [ ] Mock `fetch()` to intercept `/api/des/run` call
- [ ] Verify request payload matches backend `RunRequest` schema
- [ ] Mock backend response (valid `RunResponse`)
- [ ] Verify `ProgressPanel` renders simulation events
- [ ] Verify `ResultsPreview` renders final statistics
- [ ] Edge case: backend returns 400 error → verify LocalDESEngine fallback
- [ ] Edge case: backend returns 500 error → verify LocalDESEngine fallback
- [ ] Edge case: network error → verify LocalDESEngine fallback

**Expected:** 3-5 tests, all passing

### 2. Backend Smoke Test
Run existing backend tests to verify routes still work:
```bash
python -m pytest tests/hivenode/test_des_routes.py -v
```

Expected output: **22 tests passing** (from TASK-146)

### 3. Frontend Regression Test
Run full frontend test suite to verify no regressions:
```bash
cd browser && npx vitest run
```

Expected: **No new failures** compared to baseline.

## File Structure

**Files to Create:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\e2e-backend-sim.test.tsx` (~100 lines)

**No production code changes in this task.** This is verification only.

## Test Requirements

### TDD Process
This is a verification task, so TDD doesn't apply the same way:
1. Write E2E test file
2. Run tests (they should pass if TASK-174 and TASK-175 succeeded)
3. If tests fail, report issues back to Q33N (do NOT fix production code in this task)

### Test Commands
```bash
# Run E2E test
cd browser && npx vitest run src/apps/sim/components/flow-designer/__tests__/e2e-backend-sim.test.tsx

# Run backend smoke test
cd hivenode && python -m pytest tests/hivenode/test_des_routes.py -v

# Run full frontend suite (regression check)
cd browser && npx vitest run

# Run full backend suite (regression check)
cd hivenode && python -m pytest tests/ -v
```

All tests must pass.

## Constraints

### Hard Rules
- **CSS:** var(--sd-*) only. No hex, rgb, or named colors. (N/A for this task — only tests)
- **File size:** Test file must be under 500 lines (~100 lines expected)
- **No stubs:** Test setup must be complete (mock responses realistic)
- **No production code changes:** This task only creates tests

### Test Data
Use a simple test flow:
```typescript
const testFlow: PhaseFlow = {
  id: 'test-flow-1',
  name: 'E2E Test Flow',
  version: '1.0.0',
  created_at: '2026-03-16T00:00:00Z',
  nodes: [
    { id: 'source-1', type: 'source', data: { label: 'Source' } },
    { id: 'sink-1', type: 'sink', data: { label: 'Sink' } }
  ],
  edges: [
    { id: 'e1', source: 'source-1', target: 'sink-1' }
  ]
};
```

Mock backend response:
```typescript
const mockRunResponse: DESRunResponse = {
  run_id: 'run-12345',
  status: 'completed',
  sim_time: 100.0,
  events_processed: 50,
  tokens_created: 10,
  tokens_completed: 10,
  statistics: {
    throughput: 0.1,
    avg_cycle_time: 10.0
  }
};
```

## File Claims (IMPORTANT — parallel bees)

Before modifying any file, claim it:
```bash
curl -X POST http://localhost:8420/build/claim \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-176", "files": ["browser/src/apps/sim/components/flow-designer/__tests__/e2e-backend-sim.test.tsx"]}'
```

Since this is a new file, no conflicts expected.

When done, release:
```bash
curl -X POST http://localhost:8420/build/release \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-176", "files": ["browser/src/apps/sim/components/flow-designer/__tests__/e2e-backend-sim.test.tsx"]}'
```

On heartbeat complete/failed, all claims auto-release.

## Heartbeat

POST to build monitor every 3 minutes during work:
```bash
curl -X POST http://localhost:8420/build/heartbeat \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-176", "status": "running", "model": "sonnet", "message": "writing E2E integration test"}'
```

On completion:
```bash
curl -X POST http://localhost:8420/build/heartbeat \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-176", "status": "complete", "model": "sonnet", "message": "5 E2E tests passing, 22 backend tests passing, no regressions"}'
```

On failure:
```bash
curl -X POST http://localhost:8420/build/heartbeat \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-176", "status": "failed", "model": "sonnet", "message": "reason for failure"}'
```

## Acceptance Criteria

- [ ] E2E test loads FlowDesigner and simulates user clicking "Simulate" mode
- [ ] Test verifies `/api/des/run` called with correct request payload
- [ ] Test verifies ProgressPanel renders backend results
- [ ] Test verifies ResultsPreview renders final statistics
- [ ] Test verifies fallback to LocalDESEngine on backend errors (400, 500, network)
- [ ] 3-5 E2E tests written, all passing
- [ ] Backend smoke test: 22 tests passing (no regressions)
- [ ] Frontend smoke test: no new failures (baseline + TASK-174 + TASK-175 tests)
- [ ] File size under 500 lines (~100 lines)
- [ ] Mock data realistic (matches backend schemas)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-176-RESPONSE.md`

The response MUST contain these 8 sections:

1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full absolute paths
3. **What Was Done** — bullet list of concrete changes (not intent)
4. **Test Results** — test files run, pass/fail counts, command used
5. **Build Verification** — smoke test output, last 5 lines of test run
6. **Acceptance Criteria** — copy from above, mark [x] or [ ] with explanation
7. **Clock / Cost / Carbon** — all three metrics (wall time, estimated USD, estimated CO2e)
8. **Issues / Follow-ups** — edge cases, dependencies, recommended next tasks

DO NOT skip any section. All 8 sections are mandatory.

## Notes

- **Depends on:** TASK-174 (desClient) and TASK-175 (useSimulation wire) must be complete
- **Verification only:** No production code changes in this task
- If tests fail, report issues to Q33N — do NOT fix production code here
- This is the final task in the flow-des-wire spec (2026-03-16-1022-SPEC-w2-04)
- Mock realistic backend responses (don't just return empty objects)
- Test both success and error paths (happy path + 3 error cases)

**Estimated Clock:** 30 minutes
**Model:** Sonnet
**Priority:** P1.00 (part of flow-des-wire spec)
