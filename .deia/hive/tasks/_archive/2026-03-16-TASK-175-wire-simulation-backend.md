# TASK-175: Wire useSimulation Hook to Backend DES Engine

## Objective
Modify `useSimulation.ts` to call the backend DES engine (via desClient from TASK-174) instead of LocalDESEngine, with fallback to LocalDESEngine for offline mode.

## Context
The flow designer currently uses `LocalDESEngine` (client-side simulation) in `useSimulation.ts`. This task wires it to the backend `/api/des/run` endpoint via the `desClient` service created in TASK-174.

**Current Flow:**
1. User clicks "Simulate" mode in FlowToolbar
2. `useSimulation.start()` called
3. `LocalDESEngine.run(flow)` executes client-side
4. Events emitted to `SimEvent` bus
5. `ProgressPanel` and `ResultsPreview` display results

**New Flow:**
1. User clicks "Simulate" mode in FlowToolbar
2. `useSimulation.start()` called
3. **NEW:** Check `useBackend` flag
4. **NEW:** If `useBackend: true`, call `desClient.run(flow, config)` → `/api/des/run`
5. **NEW:** If backend fails OR `useBackend: false`, fall back to `LocalDESEngine`
6. **NEW:** Map `DESRunResponse` events to `SimEvent` bus
7. Existing panels display results (no changes needed)

**Key Design Decision (Q33NR approved):**
- Use SYNC API (current `/api/des/run` is synchronous, not streaming)
- Display all events at once (not real-time streaming)
- Fall back to LocalDESEngine if backend unavailable
- Keep existing UX — clicking "Simulate" mode starts simulation (no new Run button)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\simulation\useSimulation.ts` (381 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\simulation\LocalDESEngine.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\services\desClient.ts` (created in TASK-174)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\panels\ProgressPanel.tsx`

## Deliverables

### 1. Add Backend Support to useSimulation
- [ ] Import `desClient` from TASK-174
- [ ] Add `useBackend?: boolean` config option (default: true)
- [ ] On `start()`, if `useBackend === true`, call `desClient.run(flow, config)`
- [ ] Map `DESRunResponse` to existing `SimEvent` bus format
- [ ] On backend error, log warning and fall back to `LocalDESEngine`
- [ ] If `useBackend === false`, use `LocalDESEngine` directly
- [ ] Keep all existing state variables (`isRunning`, `progress`, `results`, etc.)
- [ ] Keep all existing methods (`start`, `pause`, `reset`, `step`, etc.)

### 2. Event Mapping
The backend returns:
```typescript
DESRunResponse {
  run_id: string
  status: string
  sim_time: float
  events_processed: int
  tokens_created: int
  tokens_completed: int
  statistics: dict
}
```

Map to existing `SimEvent` bus:
- Create synthetic events from response statistics
- Emit events in sequence (even though they arrive all at once)
- Match existing `SimEvent` format so panels work unchanged

### 3. Test Coverage (TDD — Write Tests FIRST)
- [ ] Test: `useSimulation({ useBackend: true })` → calls `desClient.run()`
- [ ] Test: `useSimulation({ useBackend: false })` → uses `LocalDESEngine`
- [ ] Test: Backend success → verify events mapped correctly to SimEvent bus
- [ ] Test: Backend error (400) → verify fallback to LocalDESEngine
- [ ] Test: Backend error (500) → verify fallback to LocalDESEngine
- [ ] Test: Backend network error → verify fallback to LocalDESEngine
- [ ] Test: Backend disabled (`useBackend: false`) → LocalDESEngine used, no backend calls
- [ ] Test: Existing `start()`, `pause()`, `reset()` still work with backend mode
- [ ] Test: Progress updates correctly from backend response
- [ ] Test: Results state matches backend response statistics
- [ ] Mock `desClient` for all tests (no real backend calls)
- [ ] Mock `LocalDESEngine` to verify fallback behavior

**Expected:** 10-12 tests, all passing

## File Structure

**Files to Modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\simulation\useSimulation.ts`
  - Current: 381 lines
  - After: ~450 lines
  - **Status:** ✅ Under 500 line limit

**Files to Create:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\simulation\__tests__\useSimulation.test.ts` (~250 lines)

**No UI changes needed.** All panels (`ProgressPanel`, `ResultsPreview`) already exist and work with the SimEvent bus.

## Test Requirements

### TDD Process
1. Write test file FIRST (`useSimulation.test.ts`)
2. Run tests (they should fail)
3. Modify `useSimulation.ts`
4. Run tests until all pass
5. No stubs — every function fully implemented

### Test Commands
```bash
# Run this task's tests
cd browser && npx vitest run src/apps/sim/components/flow-designer/simulation/__tests__/useSimulation.test.ts

# Verify no regressions on other sim tests
cd browser && npx vitest run src/apps/sim/

# Full browser test suite
cd browser && npx vitest run
```

All existing tests must still pass.

## Constraints

### Hard Rules
- **CSS:** var(--sd-*) only. No hex, rgb, or named colors. (N/A for this task — no UI)
- **File size:** `useSimulation.ts` must stay under 500 lines (currently 381 → ~450)
- **No stubs:** Every function fully implemented. No `// TODO`, no empty bodies.
- **TDD:** Tests written FIRST, then implementation.
- **No breaking changes:** All existing callers of `useSimulation()` must continue to work.

### API Contract
- Backend: `/api/des/run` (POST) — sync response with all events
- Frontend: `desClient.run(flow, config)` from TASK-174
- SimEvent bus: existing format, no changes

### Error Handling
- Backend 400/500/network error → log warning, fall back to LocalDESEngine
- Don't show error modals — graceful degradation
- Log backend errors to console for debugging

## File Claims (IMPORTANT — parallel bees)

Before modifying any file, claim it:
```bash
curl -X POST http://localhost:8420/build/claim \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-175", "files": ["browser/src/apps/sim/components/flow-designer/simulation/useSimulation.ts"]}'
```

If response has conflicts (`ok: false`), you are queued FIFO. Poll every 30s until file is yours.

When done with a file, release it early:
```bash
curl -X POST http://localhost:8420/build/release \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-175", "files": ["browser/src/apps/sim/components/flow-designer/simulation/useSimulation.ts"]}'
```

On heartbeat complete/failed, all claims auto-release.

## Heartbeat

POST to build monitor every 3 minutes during work:
```bash
curl -X POST http://localhost:8420/build/heartbeat \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-175", "status": "running", "model": "sonnet", "message": "wiring backend to useSimulation"}'
```

On completion:
```bash
curl -X POST http://localhost:8420/build/heartbeat \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-175", "status": "complete", "model": "sonnet", "message": "12 tests passing"}'
```

On failure:
```bash
curl -X POST http://localhost:8420/build/heartbeat \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-175", "status": "failed", "model": "sonnet", "message": "reason for failure"}'
```

## Acceptance Criteria

- [ ] `useSimulation({ useBackend: true })` calls backend via desClient
- [ ] `useSimulation({ useBackend: false })` uses LocalDESEngine (no backend calls)
- [ ] Backend errors gracefully fall back to LocalDESEngine (no user-facing errors)
- [ ] Backend response events mapped to SimEvent bus correctly
- [ ] Existing panels (ProgressPanel, ResultsPreview) display backend results correctly
- [ ] 10-12 tests written FIRST (TDD), all passing
- [ ] No stubs — all functions fully implemented
- [ ] File size under 500 lines (useSimulation.ts: ~450 lines)
- [ ] No breaking changes — existing callers still work
- [ ] No regressions — all existing browser tests pass

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-175-RESPONSE.md`

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

- **Depends on:** TASK-174 (desClient must exist first)
- **Next task:** TASK-176 will add E2E integration test
- Keep `LocalDESEngine` — it's the fallback for offline mode
- Default `useBackend: true` for online-first behavior
- Log all backend errors to console for debugging (don't throw, don't show modals)
- The spec says "Run button" but the actual UX is clicking "Simulate" mode — wire that existing trigger

**Estimated Clock:** 90 minutes
**Model:** Sonnet
**Priority:** P1.00 (part of flow-des-wire spec)
