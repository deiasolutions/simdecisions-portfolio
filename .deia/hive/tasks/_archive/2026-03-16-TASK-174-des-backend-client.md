# TASK-174: Backend DES Client Service

## Objective
Create a TypeScript service that calls `/api/des/run` and `/api/des/validate` backend routes, with full test coverage.

## Context
The backend DES routes were ported in TASK-146 (`hivenode/routes/des_routes.py`). This task creates the frontend HTTP client to call those routes. The client must match the backend Pydantic schemas exactly.

**Backend Endpoints:**
- `POST /api/des/run` — Execute simulation, returns RunResponse with all events
- `POST /api/des/validate` — Validate flow schema, returns validation errors

**Backend Schemas (from des_routes.py):**
```python
class FlowSchema(BaseModel):
    id: str
    name: str = ""
    nodes: list[NodeSchema] = Field(default_factory=list)
    edges: list[EdgeSchema] = Field(default_factory=list)
    resources: list[ResourceSchema] = Field(default_factory=list)
    variables: list[VariableSchema] = Field(default_factory=list)

class SimConfigSchema(BaseModel):
    seed: Optional[int] = None
    time_horizon: float = 1000.0
    replications: int = 1

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

**Frontend Flow Format (from serialization.ts):**
The flow designer uses `PhaseFlow` from `toPhaseFlow()` which already exists in the codebase. This client must convert `PhaseFlow` to `FlowSchema` format.

**IMPORTANT API CORRECTION:**
- The spec says `/sim/start` but the actual backend route is `/api/des/run`
- Use `/api/des/run` in all code and tests

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py` — backend schemas
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_des_routes.py` — backend tests (22 passing)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\file-ops\serialization.ts` — PhaseFlow definition

## Deliverables

### 1. TypeScript Types
- [ ] `DESFlowSchema` (matches backend FlowSchema)
- [ ] `DESNodeSchema` (matches backend NodeSchema)
- [ ] `DESEdgeSchema` (matches backend EdgeSchema)
- [ ] `DESResourceSchema` (matches backend ResourceSchema)
- [ ] `DESVariableSchema` (matches backend VariableSchema)
- [ ] `DESSimConfig` (matches backend SimConfigSchema)
- [ ] `DESRunRequest` (matches backend RunRequest)
- [ ] `DESRunResponse` (matches backend RunResponse)
- [ ] `DESValidateResponse` (validation error format)

### 2. DES Client Service
- [ ] `desClient.run(flow, config?)` — POST /api/des/run
- [ ] `desClient.validate(flow)` — POST /api/des/validate
- [ ] Error handling for 400 (validation errors) and 500 (server errors)
- [ ] Convert `PhaseFlow` to `DESFlowSchema` internally
- [ ] Use `fetch()` with proper headers (`Content-Type: application/json`)

### 3. Test Coverage (TDD — Write Tests FIRST)
- [ ] Test: `run()` with valid flow → verify request format matches backend schema
- [ ] Test: `run()` with custom config → verify config passed correctly
- [ ] Test: `run()` with 400 error → verify error thrown with validation details
- [ ] Test: `run()` with 500 error → verify error thrown with server error message
- [ ] Test: `run()` network failure → verify error propagation
- [ ] Test: `validate()` with valid flow → verify success response
- [ ] Test: `validate()` with invalid flow → verify validation errors returned
- [ ] Test: `validate()` network failure → verify error propagation
- [ ] Mock `fetch()` for all tests (no real backend calls)
- [ ] Edge case: empty flow (no nodes) → backend returns 400, verify error handling
- [ ] Edge case: malformed edge references → backend returns 400, verify error handling

**Expected:** 8-10 tests, all passing

## File Structure

**New Files (create these):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\services\desClient.ts` (~150 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\services\__tests__\desClient.test.ts` (~200 lines)

**No modifications to existing files in this task.** This is an isolated API client.

## Test Requirements

### TDD Process
1. Write test file FIRST (`desClient.test.ts`)
2. Run tests (they should fail)
3. Implement `desClient.ts`
4. Run tests until all pass
5. No stubs — every function fully implemented

### Test Command
```bash
cd browser && npx vitest run src/apps/sim/services/__tests__/desClient.test.ts
```

### Smoke Test (verify no regressions)
```bash
cd browser && npx vitest run
```

All existing tests must still pass.

## Constraints

### Hard Rules
- **CSS:** var(--sd-*) only. No hex, rgb, or named colors. (N/A for this task — no UI)
- **File size:** No file over 500 lines. Modularize at 500.
- **No stubs:** Every function fully implemented. No `// TODO`, no empty bodies.
- **TDD:** Tests written FIRST, then implementation.

### API Contract
The client MUST match backend schemas EXACTLY. Any mismatch will cause 400 errors.

### Error Handling
- 400 errors: throw with validation error details
- 500 errors: throw with server error message
- Network errors: throw with network error message
- All errors should include enough context for debugging

## File Claims (IMPORTANT — parallel bees)

Before modifying any file, claim it:
```bash
curl -X POST http://localhost:8420/build/claim \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-174", "files": ["browser/src/apps/sim/services/desClient.ts"]}'
```

If response has conflicts (`ok: false`), you are queued FIFO. Poll every 30s until file is yours.

When done with a file, release it early:
```bash
curl -X POST http://localhost:8420/build/release \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-174", "files": ["browser/src/apps/sim/services/desClient.ts"]}'
```

On heartbeat complete/failed, all claims auto-release.

## Heartbeat

POST to build monitor every 3 minutes during work:
```bash
curl -X POST http://localhost:8420/build/heartbeat \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-174", "status": "running", "model": "sonnet", "message": "working on desClient implementation"}'
```

On completion:
```bash
curl -X POST http://localhost:8420/build/heartbeat \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-174", "status": "complete", "model": "sonnet", "message": "8 tests passing"}'
```

On failure:
```bash
curl -X POST http://localhost:8420/build/heartbeat \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-174", "status": "failed", "model": "sonnet", "message": "reason for failure"}'
```

## Acceptance Criteria

- [ ] `desClient.ts` implements `run()` and `validate()` methods
- [ ] All TypeScript types match backend Pydantic schemas exactly
- [ ] 8-10 tests written FIRST (TDD), all passing
- [ ] Error handling for 400, 500, and network errors
- [ ] No stubs — all functions fully implemented
- [ ] File size under 500 lines (both files)
- [ ] No regressions — all existing browser tests pass
- [ ] `PhaseFlow` → `DESFlowSchema` conversion works correctly

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-174-RESPONSE.md`

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

- This task is INDEPENDENT — can run in parallel with other tasks
- Next task (TASK-175) will wire this client into `useSimulation.ts`
- Keep error messages developer-friendly (include request details for debugging)
- Use TypeScript strict mode — no `any` types

**Estimated Clock:** 45 minutes
**Model:** Sonnet
**Priority:** P1.00 (part of flow-des-wire spec)
