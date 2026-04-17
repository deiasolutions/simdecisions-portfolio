# BRIEFING: Wire Flow Designer to DES Engine

**Date:** 2026-03-16
**From:** Q33NR (REGENT-QUEUE-TEMP-2026-03-16-1022-SPE)
**To:** Q33N
**Model Assignment:** Sonnet
**Priority:** P1.00

---

## Objective

Wire the flow designer "Run" button to the DES simulation engine. When a user clicks "Run":
1. Current flow is sent to `/api/des/run`
2. Simulation starts
3. Events stream back to browser
4. Results display in a results pane

This connects the visual flow designer to the backend DES engine that was ported in TASK-146.

---

## Context from Q88N (via Queue Spec)

**Spec ID:** `2026-03-16-1022-SPEC-w2-04-flow-des-wire`

**Acceptance Criteria:**
- [ ] Run button calls `/api/des/start` with current flow
- [ ] Simulation events stream to browser
- [ ] Results displayed in pane
- [ ] Tests written and passing

**Constraints:**
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- Heartbeat to build monitor every 3 minutes
- File claim system ACTIVE (http://localhost:8420/build/claim)

**Smoke Test:**
```bash
python -m pytest tests/hivenode/test_des_routes.py -v
```

---

## Relevant Files and Code References

### Backend (DES Routes — Already Built)

**From MEMORY.md:**
> DES Routes Port — COMPLETE (2026-03-15 / TASK-146)
> - Source: platform/efemera/src/efemera/des/engine_routes.py (265 lines)
> - Target: hivenode/routes/des_routes.py (276 lines) + tests (471 lines)
> - 4 endpoints: /api/des/run, /api/des/validate, /api/des/replicate, /api/des/status
> - 9 Pydantic schemas: Node, Edge, Resource, Variable, Flow, SimConfig, RunRequest/Response, etc.
> - Validation: empty flows, bad edge refs, no source nodes — all caught with 400 errors
> - Routes registered in hivenode/routes/__init__.py
> - Tests: 22 tests, all passing (TDD approach)

**Key file paths (absolute):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_des_routes.py`

**API Contract (from des_routes.py):**
- POST `/api/des/run` — accepts `RunRequest`, returns `RunResponse`
- POST `/api/des/validate` — accepts `Flow`, returns validation errors
- POST `/api/des/replicate` — accepts `Flow`, returns replicated flow
- GET `/api/des/status/{run_id}` — returns simulation status

**RunRequest schema:**
```python
class RunRequest(BaseModel):
    flow: Flow
    config: SimConfig
```

**RunResponse schema:**
```python
class RunResponse(BaseModel):
    run_id: str
    status: str
    events: List[SimEvent]
    metrics: Dict[str, Any]
```

### Frontend (Flow Designer — Location TBD)

**Expected location (verify):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\`

**From git status (recent changes):**
- `browser/src/apps/sim/components/flow-designer/animation/` (multiple files modified)

**Key components to wire:**
- Run button (likely in a toolbar component)
- Flow state (likely in a reducer or context)
- Results pane (may need to be created or identified)

### Related Patterns

**From MEMORY.md — Efemera EGG (similar streaming pattern):**
> - Terminal `routeTarget: 'relay'` added (types + useTerminal)
> - Relay poller: `browser/src/services/efemera/relayPoller.ts`
> - Bus events: `channel:selected`, `channel:message-sent`, `channel:message-received`

**Pattern to follow:**
1. Define `routeTarget: 'sim'` or similar
2. Create a poller service for `/api/des/status/{run_id}`
3. Emit bus events for simulation lifecycle: `sim:started`, `sim:event`, `sim:completed`
4. Results pane subscribes to bus events

---

## Files Q33N Must Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py` — understand API contract
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_des_routes.py` — understand request/response format
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\` — find run button, flow state
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\efemera\relayPoller.ts` — pattern for polling service
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\markdownRenderer.tsx` — pattern for results display (if text-based)

---

## Task Breakdown (Suggested — Q33N Decides)

### Task 1: Wire Run Button to API
- **Scope:** Flow designer run button calls POST `/api/des/run`
- **Deliverables:**
  - Run button handler
  - HTTP client call to `/api/des/run`
  - Error handling (validation errors, network errors)
  - Loading state during simulation
- **Tests:**
  - Mock API call, verify request format
  - Verify error handling (400, 500)
  - Verify loading state transitions

### Task 2: Simulation Status Poller
- **Scope:** Poll GET `/api/des/status/{run_id}` until complete
- **Deliverables:**
  - Poller service (similar to relayPoller.ts)
  - Start polling on `sim:started`
  - Stop polling on `sim:completed` or error
  - Emit bus events for each status update
- **Tests:**
  - Mock polling with setTimeout
  - Verify polling stops on completion
  - Verify error handling (network failure)

### Task 3: Results Pane Display
- **Scope:** Display simulation events and metrics in a pane
- **Deliverables:**
  - Results pane component (or reuse existing pane)
  - Subscribe to `sim:event` bus events
  - Render event list and metrics
  - CSS: var(--sd-*) only
- **Tests:**
  - Mock events, verify rendering
  - Verify scrolling (if many events)
  - Verify CSS variables

### Task 4: E2E Integration Test
- **Scope:** Full flow from run button to results display
- **Deliverables:**
  - E2E test with real flow
  - Verify API call happens
  - Verify results display
  - Smoke test passes
- **Tests:**
  - Run `python -m pytest tests/hivenode/test_des_routes.py -v`
  - Verify no regressions

---

## Critical Rules (from BOOT.md)

1. **TDD:** Tests first, then implementation
2. **No file over 500 lines** (hard limit: 1,000)
3. **No stubs:** Every function fully implemented
4. **CSS:** var(--sd-*) only (no hex, rgb, named colors)
5. **File claims:** Bees MUST claim files before modifying (parallel work protection)
6. **Heartbeat:** POST to build monitor every 3 minutes
7. **Response file:** All 8 sections, no omissions

---

## Model Assignment Rationale

**Sonnet assigned** because:
- Integration task (frontend ↔ backend)
- Multiple components to wire
- Requires understanding existing patterns
- Not trivial (P1.00)

---

## Q33N Instructions

1. Read all files listed in "Files Q33N Must Read First"
2. Identify exact locations of:
   - Run button component
   - Flow state (reducer, context, or store)
   - Pane where results should display (or create new one)
3. Write task files (one per bee-sized unit)
4. Return to Q33NR for review
5. **DO NOT dispatch bees yet** — wait for Q33NR approval

---

## Success Criteria for Task Files

When Q33N returns task files, Q33NR will verify:

- [ ] Every acceptance criterion from the spec has a corresponding deliverable in a task
- [ ] All file paths are absolute (Windows format: `C:\Users\davee\...`)
- [ ] Test requirements are specific (how many tests, which scenarios)
- [ ] No file would exceed 500 lines (check existing file sizes + planned additions)
- [ ] CSS rules specified (var(--sd-*) only)
- [ ] No stubs allowed
- [ ] Response file template included in every task
- [ ] File claim instructions included (task_id: `2026-03-16-1022-SPEC-w2-04-flow-des-wire`)
- [ ] Heartbeat instructions included (build monitor URL)

---

**Q33NR will review task files before approving dispatch. Max 2 correction cycles.**
