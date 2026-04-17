# Q33N REPORT: Task Files Ready for Review — Flow Designer to DES Wire

**From:** Q33N (QUEEN-2026-03-16-Q33NR-APPROVAL-flow-des-wire)
**To:** Q33NR
**Date:** 2026-03-16
**Status:** TASK FILES READY FOR FINAL REVIEW

---

## Summary

I have written **3 task files** per Q33NR's approval, incorporating all corrections and requirements:

1. **TASK-174:** Backend DES Client Service (~45 min, 8-10 tests)
2. **TASK-175:** Wire useSimulation to Backend (~90 min, 10-12 tests)
3. **TASK-176:** E2E Integration Test (~30 min, 3-5 tests)

**Total:** ~3 hours, 21-27 new tests
**Model:** Sonnet for all 3 tasks
**Priority:** P1.00

---

## Task Files Created

### 1. TASK-174: Backend DES Client Service
**File:** `.deia/hive/tasks/2026-03-16-TASK-174-des-backend-client.md`

**Scope:**
- Create TypeScript HTTP client for `/api/des/run` and `/api/des/validate`
- Types matching backend Pydantic schemas exactly
- Error handling for 400/500/network errors
- 8-10 tests (TDD)

**New Files:**
- `browser/src/apps/sim/services/desClient.ts` (~150 lines)
- `browser/src/apps/sim/services/__tests__/desClient.test.ts` (~200 lines)

**No modifications to existing files.** This is an isolated API client.

**Key Corrections Applied:**
- ✅ API endpoint: `/api/des/run` (not `/sim/start` from spec)
- ✅ Documented spec discrepancy in task context
- ✅ Added file claims section with task ID `TASK-174`
- ✅ Added heartbeat section with proper JSON examples
- ✅ Added absolute file paths (Windows format)
- ✅ CSS rule: N/A (no UI in this task)
- ✅ No stubs rule: explicitly stated
- ✅ 8-section response template included

---

### 2. TASK-175: Wire useSimulation Hook to Backend
**File:** `.deia/hive/tasks/2026-03-16-TASK-175-wire-simulation-backend.md`

**Scope:**
- Modify `useSimulation.ts` to call backend via desClient
- Add `useBackend` flag (default: true)
- Fall back to LocalDESEngine on backend errors
- Map `DESRunResponse` to existing SimEvent bus
- 10-12 tests (TDD)

**Files Modified:**
- `browser/src/apps/sim/components/flow-designer/simulation/useSimulation.ts` (381 → ~450 lines)

**Files Created:**
- `browser/src/apps/sim/components/flow-designer/simulation/__tests__/useSimulation.test.ts` (~250 lines)

**No UI changes.** Existing panels (ProgressPanel, ResultsPreview) work unchanged.

**Key Corrections Applied:**
- ✅ Q33NR decision: Use sync API (not streaming)
- ✅ Q33NR decision: Fall back to LocalDESEngine if backend unavailable
- ✅ Q33NR decision: Wire existing "Simulate" mode trigger (no new Run button)
- ✅ Acceptance criteria: "Simulate mode trigger calls `/api/des/run`" (not "Run button")
- ✅ File size verified: 381 → ~450 lines (under 500 limit)
- ✅ Depends on TASK-174 (desClient must exist first)
- ✅ Added file claims section with task ID `TASK-175`
- ✅ Added heartbeat section
- ✅ Absolute file paths
- ✅ No stubs rule: explicitly stated

---

### 3. TASK-176: E2E Integration Test
**File:** `.deia/hive/tasks/2026-03-16-TASK-176-des-integration-e2e.md`

**Scope:**
- Full end-to-end test: FlowDesigner → backend → results display
- Verify `/api/des/run` called with correct payload
- Verify results rendered in panels
- Test error fallback paths
- 3-5 tests

**Files Created:**
- `browser/src/apps/sim/components/flow-designer/__tests__/e2e-backend-sim.test.tsx` (~100 lines)

**No production code changes.** This is verification only.

**Smoke Tests:**
- Backend: `python -m pytest tests/hivenode/test_des_routes.py -v` (expect 22 passing)
- Frontend: `cd browser && npx vitest run` (expect no new failures)

**Key Corrections Applied:**
- ✅ Depends on TASK-174 and TASK-175
- ✅ Added file claims section with task ID `TASK-176`
- ✅ Added heartbeat section
- ✅ Absolute file paths
- ✅ Test data examples (realistic mock flow + response)

---

## All Corrections Applied

Per Q33NR's requirements, every task file includes:

### 1. File Claims Section ✅
```markdown
## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it:
POST http://localhost:8420/build/claim
{"task_id": "TASK-XXX", "files": ["path/to/file"]}
```

### 2. Heartbeat Section ✅
```markdown
## Heartbeat
POST to http://localhost:8420/build/heartbeat every 3 minutes:
{"task_id": "TASK-XXX", "status": "running", "model": "sonnet", "message": "working"}
```

### 3. Response File Template ✅
All task files include the 8-section response template with explicit section names.

### 4. Absolute File Paths ✅
All file paths use Windows absolute format:
`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\...`

### 5. CSS Rule ✅
Stated explicitly in constraints (N/A for these tasks — no CSS changes).

### 6. No Stubs Rule ✅
Stated explicitly in every task file: "NO STUBS. Every function fully implemented. If you can't finish, say so — don't ship a stub."

### 7. API Endpoint Correction ✅
Task files use `/api/des/run` (actual backend route), not `/sim/start` (spec error). Documented in context sections.

### 8. Acceptance Criteria Mapping ✅
TASK-175 acceptance criteria says: "Simulate mode trigger calls `/api/des/run` with current flow" (not "Run button").

---

## File Size Verification

| File | Lines | Status |
|------|-------|--------|
| `desClient.ts` | ~150 | ✅ Under 500 |
| `desClient.test.ts` | ~200 | ✅ Under 500 |
| `useSimulation.ts` | 381 → ~450 | ✅ Under 500 |
| `useSimulation.test.ts` | ~250 | ✅ Under 500 |
| `e2e-backend-sim.test.tsx` | ~100 | ✅ Under 500 |

**All files under 500 line limit.**

---

## Test Coverage Summary

| Task | Tests | Type |
|------|-------|------|
| TASK-174 | 8-10 | Unit (desClient) |
| TASK-175 | 10-12 | Unit (useSimulation hook) |
| TASK-176 | 3-5 | E2E (integration) |
| **Total** | **21-27** | **All new tests** |

**Plus:**
- Backend smoke test: 22 existing tests (from TASK-146)
- Frontend regression: ~1,122 existing tests (from baseline)

---

## Dependency Chain

```
TASK-174 (desClient)
  ↓
TASK-175 (wire useSimulation) — depends on TASK-174
  ↓
TASK-176 (E2E test) — depends on TASK-174 + TASK-175
```

**Dispatch order:** Sequential (175 waits for 174, 176 waits for 175)

OR

**Parallel option:** Dispatch 174 immediately, queue 175 and 176 to start when dependencies complete.

---

## Acceptance Criteria Mapping (Original Spec)

From `2026-03-16-1022-SPEC-w2-04-flow-des-wire.md`:

- [x] **Run button calls `/api/des/start` with current flow**
  - → TASK-175 (wires "Simulate" mode trigger to `/api/des/run`)
  - ✅ Corrected: `/api/des/run` (not `/sim/start`)
  - ✅ Clarified: "Simulate mode" trigger (not new "Run button")

- [x] **Simulation events stream to browser**
  - → TASK-175 (maps `DESRunResponse` to SimEvent bus)
  - ✅ Clarified: Sync API (all events at once, not real-time streaming)

- [x] **Results displayed in pane**
  - → TASK-175 (existing panels work unchanged)
  - ✅ No new UI needed

- [x] **Tests written and passing**
  - → TASK-174 (8-10 tests)
  - → TASK-175 (10-12 tests)
  - → TASK-176 (3-5 tests + smoke tests)
  - ✅ Total: 21-27 new tests

**All acceptance criteria covered.**

---

## Questions Answered by Q33NR

1. **Streaming vs Sync:** ✅ Use sync API (display all events at once)
2. **Fallback behavior:** ✅ Fall back to LocalDESEngine if backend unavailable
3. **Run button location:** ✅ Keep existing UX (wire "Simulate" mode trigger)

---

## Ready for Dispatch

**Task IDs:**
- `2026-03-16-TASK-174-des-backend-client.md`
- `2026-03-16-TASK-175-wire-simulation-backend.md`
- `2026-03-16-TASK-176-des-integration-e2e.md`

**Model:** Sonnet (all 3 tasks)
**Priority:** P1.00
**Estimated Total Clock:** ~3 hours

**Dispatch commands:**
```bash
# Task 174 (independent — start immediately)
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-16-TASK-174-des-backend-client.md --model sonnet --role bee --inject-boot --timeout 3600

# Task 175 (depends on 174 — queue or wait)
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-16-TASK-175-wire-simulation-backend.md --model sonnet --role bee --inject-boot --timeout 5400

# Task 176 (depends on 175 — queue or wait)
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-16-TASK-176-des-integration-e2e.md --model sonnet --role bee --inject-boot --timeout 1800
```

---

## Issues / Follow-ups

### Known Limitations
1. **No real-time streaming:** Backend API is sync, not streaming. If Q88N wants real-time event streaming, that's a separate backend enhancement (SSE or WebSocket).
2. **No validation UI:** The `/api/des/validate` endpoint exists but isn't wired to UI. Future enhancement: show validation errors before running sim.
3. **No progress bar:** Backend returns all results at once. Progress is synthetic (derived from final statistics). Real progress would require streaming.

### Recommended Next Tasks (not in current spec)
- Add validation UI (show errors before running)
- Add real-time streaming endpoint (SSE or WebSocket)
- Add retry logic for transient backend errors
- Add backend health check (ping before running)

---

## Q33NR Actions Required

1. **Review task files:**
   - `.deia/hive/tasks/2026-03-16-TASK-174-des-backend-client.md`
   - `.deia/hive/tasks/2026-03-16-TASK-175-wire-simulation-backend.md`
   - `.deia/hive/tasks/2026-03-16-TASK-176-des-integration-e2e.md`

2. **If corrections needed:** Tell Q33N what to fix, Q33N will revise and return.

3. **If approved:** Tell Q33N to dispatch bees (sequential or queued).

---

**Q33N awaiting Q33NR final review and dispatch approval.**
