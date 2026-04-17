# TASK-141: SimDecisions Engine Integration (Phase 2)

## Objective
Wire the DES SimulationEngine into `hivenode/routes/sim.py` to replace all 503 stubs with real engine calls, enabling live simulation via backend API.

## Context
The backend sim routes (`hivenode/routes/sim.py`, 479 lines) define 13 endpoints but currently return 503 ("pending engine integration"). The DES engine is fully ported at `engine/des/engine.py` with a SimulationEngine class that has: load(), run(), pause(), resume(), step(), status(), tokens(), resources(), statistics(), checkpoint(), restore(), fork(), sweep().

The engine uses a context dict pattern: `ctx = engine.load(flow)` returns a dict with state, tokens, resources, RNG, stats, joins, trace, checkpoints, and variables. All subsequent calls pass ctx: `engine.run(ctx)`, `engine.pause(ctx)`, etc.

The LedgerAdapter at `engine/des/ledger_adapter.py` bridges DES events to the hivenode event ledger. Each engine instance needs an adapter attached.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\sim.py` (all 479 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\des\engine.py` (first 200 lines for API)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\des\core.py` (first 100 lines for EngineState, SimConfig)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\des\ledger_adapter.py` (full file)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\schemas_sim.py` (all 215 lines for request/response types)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py` (get_ledger_writer function)

## Deliverables
- [ ] Edit `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\sim.py`
  - `POST /sim/load` endpoint:
    - Import SimulationEngine from `engine.des.engine`
    - Generate run_id with `uuid.uuid4()`
    - Instantiate `engine = SimulationEngine()`
    - Call `ctx = engine.load(request.flow)` (request.flow is dict from LoadFlowRequest)
    - Store ctx in `_engines[run_id] = ctx` (already has _engines dict at top)
    - Create LedgerAdapter: `adapter = LedgerAdapter(dependencies.get_ledger_writer())`
    - Store adapter in `_engine_ledger_adapters[run_id] = adapter`
    - Emit flow_loaded event via adapter
    - Return `LoadFlowResponse(run_id=run_id, status="loaded")`
  - `POST /sim/start` endpoint:
    - Get ctx via `_get_engine(request.run_id)`
    - Call `engine.run(ctx)` in a background task (use `asyncio.create_task`)
    - Store task reference in `_running_tasks[run_id] = task`
    - Return `StartSimResponse(run_id=request.run_id, status="running")`
  - `POST /sim/pause` endpoint:
    - Get ctx via `_get_engine(request.run_id)`
    - Call `engine.pause(ctx)`
    - Return `PauseSimResponse(run_id=request.run_id, status="paused")`
  - `POST /sim/resume` endpoint:
    - Get ctx via `_get_engine(request.run_id)`
    - Call `engine.resume(ctx)` in background task
    - Return `ResumeSimResponse(run_id=request.run_id, status="running")`
  - `POST /sim/step` endpoint:
    - Get ctx via `_get_engine(request.run_id)`
    - Call `engine.step(ctx)`
    - Return `StepSimResponse(run_id=request.run_id, current_time=ctx['state'].sim_time)`
  - `GET /sim/status` endpoint:
    - Get ctx via `_get_engine(run_id)`
    - Return `SimStatusResponse(run_id=run_id, status=ctx['state'].status, current_time=ctx['state'].sim_time)`
  - `GET /sim/tokens` endpoint:
    - Get ctx via `_get_engine(run_id)`
    - Call `ctx['tokens'].all()` to get list of tokens
    - Map to `TokenInfo` objects
    - Return `TokensResponse(tokens=...)`
  - `GET /sim/resources` endpoint:
    - Get ctx via `_get_engine(run_id)`
    - Call `ctx['resources'].all()` to get list of resources
    - Map to `ResourceInfo` objects
    - Return `ResourcesResponse(resources=...)`
  - `GET /sim/statistics` endpoint:
    - Get ctx via `_get_engine(run_id)`
    - Call `ctx['stats'].summary()` to get stats dict
    - Return `StatisticsResponse(statistics=...)`
  - `POST /sim/checkpoint` endpoint:
    - Get ctx via `_get_engine(request.run_id)`
    - Call `checkpoint = engine.checkpoint(ctx)`
    - Return `CheckpointResponse(checkpoint_id=checkpoint.id)`
  - `POST /sim/restore` endpoint:
    - Get ctx via `_get_engine(request.run_id)`
    - Call `engine.restore(ctx, request.checkpoint_id)`
    - Return `RestoreResponse(run_id=request.run_id, status="restored")`
  - `POST /sim/fork` endpoint:
    - Get ctx via `_get_engine(request.run_id)`
    - Call `new_ctx = engine.fork(ctx)`
    - Generate new_run_id, store new_ctx in _engines
    - Return `ForkResponse(new_run_id=new_run_id)`
  - `POST /sim/sweep` endpoint:
    - For each param_set in request.parameters: fork, run, collect results
    - Return `SweepResponse(results=[...])`
  - `GET /sim/events` endpoint:
    - Get adapter via `_get_adapter(run_id)`
    - Read events from trace buffer or ledger
    - Map to `EventInfo` objects
    - Return `EventsResponse(events=...)`
- [ ] Add `_running_tasks: Dict[str, Any] = {}` global dict at top of file (for background task tracking)
- [ ] All 503 stubs removed — every endpoint returns real data or raises HTTPException

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_sim_engine_integration.py`
  - Test: `POST /sim/load` with valid PHASE-IR flow returns 200 + run_id
  - Test: `POST /sim/load` creates engine context in _engines dict
  - Test: `POST /sim/load` creates ledger adapter in _engine_ledger_adapters
  - Test: `POST /sim/start` returns 200 + status=running
  - Test: `POST /sim/pause` returns 200 + status=paused
  - Test: `POST /sim/resume` returns 200 + status=running
  - Test: `POST /sim/step` advances sim_time
  - Test: `GET /sim/status` returns current status + sim_time
  - Test: `GET /sim/tokens` returns list of tokens
  - Test: `GET /sim/resources` returns list of resources
  - Test: `GET /sim/statistics` returns stats dict
  - Test: `POST /sim/checkpoint` returns checkpoint_id
  - Test: `POST /sim/restore` restores from checkpoint
  - Test: `POST /sim/fork` creates new run_id
  - Test: `POST /sim/sweep` runs parameter sweep
  - Test: `GET /sim/events` returns event list
  - Test: Invalid run_id raises 404
- [ ] Unskip existing tests in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_sim_routes.py`
  - Find all tests with `@pytest.mark.skip(reason="TASK-071")` or similar
  - Remove skip decorators
  - Fix any broken assertions (engine integration changes response structure)
- [ ] All tests pass
- [ ] Edge cases: missing run_id (404), invalid flow schema (400), engine errors propagate

## Constraints
- No file over 500 lines (sim.py is 479 lines, stay under 500 after edits)
- CSS: N/A (backend only)
- No stubs — every endpoint fully implemented
- Do NOT modify `engine/des/` files — only import and call from routes
- Keep `_engines` dict pattern (production state manager is future work)
- Background tasks: use `asyncio.create_task` for run/resume

## Acceptance Criteria
After this task:
- [ ] `POST /sim/load` with demo PHASE-IR flow returns 200 + run_id
- [ ] `POST /sim/start` starts simulation, status changes to "running"
- [ ] `GET /sim/status` returns current status + sim_time
- [ ] Pause/resume cycle works: start → pause → status=paused → resume → status=running
- [ ] All 13 endpoints return real data (no 503s)
- [ ] All new tests pass (minimum 17 tests)
- [ ] All existing sim route tests pass (previously skipped tests now run)
- [ ] No hivenode test regressions

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-141-RESPONSE.md`

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
