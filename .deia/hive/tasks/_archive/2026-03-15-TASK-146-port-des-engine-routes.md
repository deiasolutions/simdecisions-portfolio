# TASK-146: Port DES Engine Routes

## Objective

Port DES engine routes from platform repo (`engine_routes.py` ~265 lines). Create FastAPI endpoints in `hivenode/routes/des_routes.py` that expose simulation control: `/sim/start`, `/sim/step`, `/sim/status`, `/sim/results`. Register routes in `hivenode/routes/__init__.py`.

## Context

This is part of W1 (Week 1) sprint to port DES simulation engine components. The DES engine itself is already ported to `engine/des/`. We now need HTTP routes to expose it via FastAPI.

**Source file:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\des\engine_routes.py`

**Target location:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py`

**Existing patterns:**
- `hivenode/routes/sim.py` — existing simulation routes (487 lines, many endpoints for load/pause/step/fork/checkpoint/inject/tokens/resources/statistics/events/sweep)
- The platform `engine_routes.py` has 4 simpler endpoints: `/run`, `/validate`, `/replicate`, `/status`

**Key differences:**
- Platform routes use `/api/des` prefix
- Platform routes are simpler — `/run` runs to completion, no pause/step/fork complexity
- Platform uses Pydantic schemas for PHASE-IR Flow objects
- Platform uses `engine.des.engine.SimulationEngine` (same as shiftcenter's `engine.des.engine.SimulationEngine`)

**Note:** The existing `hivenode/routes/sim.py` has MORE advanced control endpoints (pause/resume/step/fork/checkpoint/inject). The platform `engine_routes.py` is SIMPLER. You must decide:
1. Port the platform routes as-is (simpler endpoints, different prefix like `/api/des`)
2. OR merge/replace with existing sim.py routes (already more advanced)

**Recommendation from Q33N:** Port as-is to `/api/des` prefix to match platform. This gives us both the simple "run-to-completion" API (DES routes) AND the advanced "interactive control" API (sim routes). They serve different use cases.

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\des\engine_routes.py` — source routes (265 lines)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\sim.py` — existing sim routes pattern (487 lines)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` — registration pattern
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\des\engine.py` — SimulationEngine class (understand the API)
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\des\core.py` — SimConfig dataclass
6. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\des\replication.py` — replication support
7. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\primitives.py` — Flow, Node, Edge, Resource, Variable dataclasses

## Deliverables

- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py`
- [ ] Port 4 endpoints from platform:
  - `POST /api/des/run` — run flow to completion, return results
  - `POST /api/des/validate` — validate flow structure without running
  - `POST /api/des/replicate` — run multiple replications with confidence intervals
  - `GET /api/des/status` — engine health check
- [ ] Port Pydantic schemas from platform:
  - `NodeSchema`, `EdgeSchema`, `ResourceSchema`, `VariableSchema`, `FlowSchema`
  - `SimConfigSchema`, `RunRequest`, `RunResponse`
  - `ValidateResponse`, `ReplicateConfigSchema`, `ReplicateRequest`, `ReplicateResponse`
  - `StatusResponse`
- [ ] Port helper functions:
  - `_schema_to_flow()` — convert Pydantic FlowSchema to PHASE-IR Flow dataclass
  - `_schema_to_sim_config()` — convert Pydantic SimConfigSchema to SimConfig dataclass
- [ ] Register routes in `hivenode/routes/__init__.py`:
  - Import: `from hivenode.routes import des_routes`
  - Mount: `router.include_router(des_routes.router, tags=['des-engine'])`
- [ ] Write comprehensive tests in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_des_routes.py`:
  - Test `/run` endpoint with minimal flow
  - Test `/run` endpoint with full flow (nodes, edges, resources, variables)
  - Test `/validate` endpoint with valid flow
  - Test `/validate` endpoint with invalid flows (no nodes, bad edge refs, no source nodes)
  - Test `/replicate` endpoint (multiple runs)
  - Test `/status` endpoint (health check)
  - Test error handling (400 on invalid flow)
  - All tests use TestClient with mock transport for thread safety

## Test Requirements

- [ ] **Tests written FIRST (TDD)**
- [ ] All 4 endpoints covered:
  - `/api/des/run` — happy path + error case
  - `/api/des/validate` — valid + invalid flows (at least 3 invalid cases: no nodes, bad edge ref, no source node)
  - `/api/des/replicate` — multi-run aggregation
  - `/api/des/status` — uptime check
- [ ] Edge cases:
  - Empty flow (should fail validation)
  - Flow with orphaned nodes (edges referencing non-existent nodes)
  - Flow with no source nodes (all nodes have incoming edges)
  - SimConfig with different seeds
  - Replication with custom confidence level
- [ ] **Minimum 15 tests** (4 endpoints × ~4 test cases each, rounded up)
- [ ] All tests pass
- [ ] Use `TestClient` with `mock_transport` for SQLite thread safety (pattern from existing hivenode tests)

## Constraints

- **No file over 500 lines** (source is ~265, target should be similar)
- **TDD:** Write tests first, then implementation
- **No stubs:** Every function fully implemented
- **No hardcoded colors** (not applicable for backend routes)
- **Heartbeat:** POST to `http://localhost:8420/build/heartbeat` every 3 minutes with JSON:
  ```json
  {"task_id": "TASK-146", "status": "running", "model": "haiku", "message": "working on des_routes.py"}
  ```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-146-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Smoke Test

```bash
cd hivenode && python -m pytest tests/hivenode/test_des_routes.py -v
```

Expected: 15+ tests pass, 0 failures.

## Notes for Implementation

1. **Use existing patterns:** Follow the structure from `sim.py` for FastAPI router setup
2. **Thread safety:** Use TestClient with `mock_transport` in tests (SQLite constraint)
3. **Import paths:** Use `from engine.des.engine import SimulationEngine` (already ported)
4. **Prefix:** Use `/api/des` to match platform (different from sim.py which uses `/sim`)
5. **Validation logic:** Port the validation checks from platform (no nodes, bad edge refs, no source nodes)
6. **Replication:** Use `from engine.des.replication import run_replications, ReplicationConfig`
7. **Uptime tracking:** Use module-level `_start_time = time.time()` pattern from platform
8. **Error handling:** Wrap engine calls in try/except, raise HTTPException(400) on errors
9. **Statistics:** Use `engine.statistics(ctx)` method to get stats dict for RunResponse

## Success Criteria

- All 15+ tests green
- No stubs
- No file over 500 lines (target: ~300 lines for routes + ~200 lines for tests)
- Response file complete (8 sections)
- Routes callable via HTTP
- No new test failures in other test suites
