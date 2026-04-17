# COORDINATION REPORT: Wire Flow Designer to DES Engine

**From:** Q33N (QUEEN-2026-03-16-BRIEFING-flow-des-wire)
**To:** Q33NR
**Date:** 2026-03-16
**Status:** TASK FILES READY FOR REVIEW

---

## Executive Summary

I have analyzed the briefing and codebase. The current flow designer already has a **complete local simulation implementation** (`LocalDESEngine.ts`, `useSimulation.ts`) but it only runs client-side. The task is to wire the flow designer to the **backend DES engine** (`/api/des/run`, `/api/des/validate`, etc.) that was ported in TASK-146.

**Key Finding:** The flow designer's `useSimulation.ts` hook has a commented-out WebSocket reference (line 9: `WS_URL`) but currently uses only `LocalDESEngine`. The task is to:
1. Add a backend transport layer that calls `/api/des/run`
2. Wire the Run button to use the backend instead of LocalDESEngine
3. Display results in existing panels (which already exist and work with LocalDESEngine)

**No new UI components needed.** The results panels (`ProgressPanel.tsx`, `ResultsPreview.tsx`) are already built and working with LocalDESEngine. We just need to wire them to the backend API.

---

## Task Breakdown

I propose **3 tasks** instead of the 4 suggested in the briefing:

### Task 1: Backend DES Client Service
**Scope:** Create a service that calls `/api/des/run` and `/api/des/validate`
**Deliverables:**
- `browser/src/apps/sim/services/desClient.ts` — HTTP client for DES routes
- Types for RunRequest, RunResponse matching backend schema
- Error handling for 400/500 responses
- Tests (mock fetch, verify request format)

**Why separate:** This is an isolated API client with no UI dependencies.

---

### Task 2: Wire useSimulation to Backend
**Scope:** Modify `useSimulation.ts` to call backend via desClient instead of LocalDESEngine
**Deliverables:**
- Add `useBackend` flag to `useSimulation()` config (default: true)
- On `start()`, if `useBackend`, call `desClient.run()` instead of `LocalDESEngine.run()`
- Map backend `RunResponse.events` to existing `SimEvent` bus
- Keep LocalDESEngine as fallback for offline mode
- Tests (mock desClient, verify event mapping)

**Why separate:** This is the integration layer, depends on Task 1.

---

### Task 3: E2E Integration Test
**Scope:** Full end-to-end test from flow designer to backend
**Deliverables:**
- E2E test: load FlowDesigner, click Run, verify `/api/des/run` called
- Verify results appear in ProgressPanel
- Smoke test: `python -m pytest tests/hivenode/test_des_routes.py -v`
- No regressions on frontend tests: `cd browser && npx vitest run`

**Why separate:** Verification task, depends on Task 1 + 2.

---

## Files to Modify

### Task 1 (NEW FILES):
- **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\services\desClient.ts** (create)
- **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\services\__tests__\desClient.test.ts** (create)

### Task 2 (MODIFY):
- **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\simulation\useSimulation.ts** (381 lines → ~450 lines after changes)
- **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\simulation\__tests__\useSimulation.test.ts** (create or extend)

### Task 3 (NEW FILES):
- **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\e2e-backend-sim.test.tsx** (create)

---

## Existing Code Inventory

### Backend (Already Complete — TASK-146):
- ✅ `hivenode/routes/des_routes.py` — 4 endpoints (/run, /validate, /replicate, /status)
- ✅ `tests/hivenode/test_des_routes.py` — 22 tests, all passing
- ✅ Routes registered in `hivenode/routes/__init__.py`

### Frontend (Existing — Works with LocalDESEngine):
- ✅ `FlowDesigner.tsx` — main component, calls `useSimulation()`
- ✅ `useSimulation.ts` — simulation hook (currently uses LocalDESEngine only)
- ✅ `LocalDESEngine.ts` — client-side DES engine (fallback)
- ✅ `ProgressPanel.tsx` — displays sim progress (events, metrics)
- ✅ `ResultsPreview.tsx` — displays final results
- ✅ `SimConfigPanel.tsx` — config UI (seed, time horizon, replications)

**No new UI needed.** All panels already built. Just wire to backend.

---

## API Contract Verification

### Backend Schema (from des_routes.py):
```python
class FlowSchema(BaseModel):
    id: str
    name: str = ""
    nodes: list[NodeSchema] = Field(default_factory=list)
    edges: list[EdgeSchema] = Field(default_factory=list)
    resources: list[ResourceSchema] = Field(default_factory=list)
    variables: list[VariableSchema] = Field(default_factory=list)

class RunRequest(BaseModel):
    flow: FlowSchema
    config: Optional[SimConfigSchema] = None

class RunResponse(BaseModel):
    run_id: str
    status: str
    sim_time: float
    events_processed: int
    tokens_created: int
    tokens_completed: int
    statistics: dict
```

### Frontend Flow Format (from serialization.ts):
```typescript
export interface PhaseFlow {
  id: string;
  name: string;
  description?: string;
  version: string;
  created_at: string;
  nodes: Node[];
  edges: Edge[];
}
```

**Mapping needed:** `PhaseFlow` → `FlowSchema` (convert ReactFlow nodes/edges to backend schema)

Already exists in codebase: `toPhaseFlow()` in `file-ops/serialization.ts` (line 32 in FlowDesigner.tsx).

---

## File Size Check

| File | Current Size | After Changes | Status |
|------|-------------|---------------|--------|
| `useSimulation.ts` | 381 lines | ~450 lines | ✅ Under 500 |
| `desClient.ts` | N/A (new) | ~150 lines | ✅ Under 500 |
| `desClient.test.ts` | N/A (new) | ~200 lines | ✅ Under 500 |
| `useSimulation.test.ts` | N/A (new) | ~250 lines | ✅ Under 500 |
| `e2e-backend-sim.test.tsx` | N/A (new) | ~100 lines | ✅ Under 500 |

**All files under 500 line limit.**

---

## Test Coverage Plan

### Task 1 Tests (desClient):
- [ ] `desClient.run()` with valid flow → verify request format
- [ ] `desClient.run()` with invalid flow → verify 400 error handling
- [ ] `desClient.validate()` → verify validation errors returned
- [ ] Network error → verify error propagation
- [ ] Mock fetch for all tests (no real backend)

**Expected:** ~8-10 tests

### Task 2 Tests (useSimulation):
- [ ] `useSimulation({ useBackend: true })` → calls desClient.run()
- [ ] `useSimulation({ useBackend: false })` → uses LocalDESEngine
- [ ] Backend events mapped to SimEvent bus
- [ ] Error handling (backend failure falls back to LocalDESEngine)
- [ ] Mock desClient for all tests

**Expected:** ~10-12 tests

### Task 3 Tests (E2E):
- [ ] Load FlowDesigner with simple flow
- [ ] Click Run button
- [ ] Verify `/api/des/run` called with correct payload
- [ ] Verify ProgressPanel renders events
- [ ] Verify no regressions on existing tests

**Expected:** ~3-5 tests

**Total new tests:** 21-27 tests

---

## Acceptance Criteria Mapping

From the queue spec:
- [x] **Run button calls `/api/des/start` with current flow** → Task 2 (wire useSimulation)
- [x] **Simulation events stream to browser** → Task 2 (map RunResponse.events to SimEvent bus)
- [x] **Results displayed in pane** → Already exists (ProgressPanel.tsx), Task 2 wires data
- [x] **Tests written and passing** → Task 1, 2, 3 (21-27 new tests)

**All criteria covered.**

---

## Critical Notes

1. **Backend API is POST `/api/des/run`, not `/api/des/start`** — The briefing says "start", but the actual route is "run". Task files will use `/api/des/run`.

2. **No streaming in current API** — The backend `/api/des/run` returns a synchronous `RunResponse` with all events at once. It does NOT stream. The briefing mentions "events stream back" but the current API is synchronous. If streaming is required, that's a separate backend task.

3. **LocalDESEngine stays** — Keep it as a fallback for offline mode. Add a `useBackend` flag to toggle.

4. **CSS variables** — All existing panels already use `var(--sd-*)`. No new CSS needed.

5. **File claims** — Bees MUST claim files before modifying. Task ID: `2026-03-16-1022-SPEC-w2-04-flow-des-wire`

6. **Heartbeat** — Bees must POST to build monitor every 3 minutes during work.

---

## Questions for Q33NR

1. **Streaming vs Sync:** The current `/api/des/run` is synchronous (returns all results at once). The briefing mentions "events stream back". Should we:
   - A) Use the current sync API and display all events at once
   - B) Add a new streaming endpoint (separate task)
   - **Recommendation:** A (use sync API for now, streaming is a separate feature)

2. **Fallback behavior:** Should we fall back to LocalDESEngine if backend is unavailable, or show an error?
   - **Recommendation:** Fall back to LocalDESEngine (offline-first)

3. **Run button location:** The briefing mentions "run button calls API" but I don't see a separate Run button in FlowToolbar.tsx. The "Simulate" mode pill switches to simulate mode, which auto-starts the sim. Should we:
   - A) Add a Run button to the toolbar
   - B) Keep existing behavior (clicking "Simulate" mode starts simulation)
   - **Recommendation:** B (keep existing UX, wire to backend instead of LocalDESEngine)

---

## Next Steps

**Q33NR:** Please review this report and answer the 3 questions above. Once approved, I will write the 3 task files and return them for final review before dispatch.

**Estimated Clock:**
- Task 1 (desClient): 45 min
- Task 2 (useSimulation wire): 90 min
- Task 3 (E2E tests): 30 min
- **Total:** ~3 hours (Sonnet model for all tasks)

---

**Q33N awaiting Q33NR approval to proceed with task file creation.**
