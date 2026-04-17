# TASK-072: Hivenode Sim Routes + Ledger Adapter

## Objective

Write the ledger adapter to bridge DES simulation events to the shiftcenter Event Ledger, write 16 FastAPI routes for sim control, write Pydantic schemas, register routes, and write E2E tests. Target: 20+ new tests passing.

## Context

TASK-071 ports the DES engine to `engine/des/`. This task wires the DES engine to the existing hivenode infrastructure:
1. **Ledger Adapter:** Translate DES events → Event Ledger format (emit to existing `hivenode/ledger/writer.py`)
2. **Sim Routes:** 16 FastAPI routes for simulation control (load, start, pause, step, checkpoint, fork, inject, etc.)
3. **Schemas:** Pydantic models for request/response
4. **Tests:** Adapter tests + E2E integration tests

The DES engine emits simulation events. The ledger adapter converts these to `SIM_*` event types and writes them to the Event Ledger via `LedgerWriter.write_event()`. The browser can then subscribe to these events and visualize the simulation.

## Files to Read First

1. `C:\Users\davee\Downloads\SPEC-PHASE-IR-PORT-001.md` — full technical spec (sections 5-7)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\writer.py` — existing ledger writer interface
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` — route registration pattern
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` — app structure and lifespan
5. `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\des\engine.py` — SimulationEngine interface (after TASK-071 ports it, or read from old repo)
6. `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\des\core.py` — event types and structure

## Deliverables

### Phase 1: Ledger Adapter
- [ ] Write `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\des\ledger_adapter.py`
- [ ] Class: `LedgerAdapter` with method `emit_event(event_type, payload, sim_time, run_id)`
- [ ] Map DES event types to Event Ledger event types:
  - `token_create` → `SIM_TOKEN_CREATED`
  - `token_arrive` → `SIM_TOKEN_ARRIVED`
  - `node_start` → `SIM_NODE_STARTED`
  - `node_end` → `SIM_NODE_COMPLETED`
  - `resource_acquired` → `SIM_RESOURCE_ACQUIRED`
  - `resource_released` → `SIM_RESOURCE_RELEASED`
  - `checkpoint` → `SIM_CHECKPOINT`
  - `fork` → `SIM_FORK`
  - `flow_complete` → `SIM_FLOW_COMPLETED`
- [ ] Every event includes:
  - `actor`: `f"sim:{run_id}"` (universal entity ID format)
  - `target`: entity affected (e.g., `f"token:{token_id}"`, `f"node:{node_id}"`)
  - `domain`: `"simulation"`
  - `payload_json`: dict with event-specific fields (token_id, node_id, duration, wait_time, etc.)
  - Three currencies (CLOCK, COIN, CARBON):
    - `cost_tokens`: `sim_time` (CLOCK in simulation time units)
    - `cost_usd`: `0.0` (COIN — no real cost for simulation)
    - `cost_carbon`: estimated compute cost (use `0.001 * num_events` kg CO2e as simple heuristic)
- [ ] Must call `hivenode.ledger.writer.LedgerWriter.write_event()` with correct signature
- [ ] No hardcoded event list — use a mapping dict or match-case for event translation
- [ ] File size: < 200 lines (simple adapter)

### Phase 2: Sim Routes
- [ ] Write `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\sim.py`
- [ ] Import: `from fastapi import APIRouter, HTTPException`
- [ ] Create router: `router = APIRouter()`
- [ ] Implement 16 routes (see spec section 5 for full details):

**Route 1: Load Flow**
```python
@router.post("/sim/load")
async def load_flow(request: LoadFlowRequest) -> LoadFlowResponse:
    """Load a PHASE-IR flow, return run_id."""
    # Instantiate SimulationEngine
    # Call engine.load_flow(flow_dict)
    # Generate run_id (use uuid4)
    # Store engine instance in global dict keyed by run_id
    # Emit SIM_FLOW_LOADED event to ledger
    # Return LoadFlowResponse(run_id=run_id, status="loaded")
```

**Route 2: Start Simulation**
```python
@router.post("/sim/start")
async def start_sim(request: StartSimRequest) -> StartSimResponse:
    """Start simulation for run_id."""
    # Lookup engine by run_id
    # Call engine.run() (blocking — may need asyncio.to_thread for long sims)
    # Emit SIM_FLOW_COMPLETED when done
    # Return StartSimResponse(run_id=run_id, status="completed", final_time=engine.clock.now)
```

**Route 3: Pause Simulation**
```python
@router.post("/sim/pause")
async def pause_sim(request: PauseSimRequest) -> PauseSimResponse:
    """Pause running simulation."""
    # Lookup engine by run_id
    # Call engine.pause()
    # Return PauseSimResponse(run_id=run_id, status="paused", current_time=engine.clock.now)
```

**Route 4: Resume Simulation**
```python
@router.post("/sim/resume")
async def resume_sim(request: ResumeSimRequest) -> ResumeSimResponse:
    """Resume paused simulation."""
    # Lookup engine by run_id
    # Call engine.resume()
    # Return ResumeSimResponse(run_id=run_id, status="running")
```

**Route 5: Step One Event**
```python
@router.post("/sim/step")
async def step_sim(request: StepSimRequest) -> StepSimResponse:
    """Advance simulation by one event."""
    # Lookup engine by run_id
    # Call engine.step()
    # Return StepSimResponse(run_id=run_id, events_processed=1, current_time=engine.clock.now)
```

**Route 6: Step N Events**
```python
@router.post("/sim/step/{n}")
async def step_n_sim(n: int, request: StepSimRequest) -> StepSimResponse:
    """Advance simulation by N events."""
    # Lookup engine by run_id
    # Call engine.step(n)
    # Return StepSimResponse(run_id=run_id, events_processed=n, current_time=engine.clock.now)
```

**Route 7: Get Status**
```python
@router.get("/sim/status")
async def get_status(run_id: str) -> SimStatusResponse:
    """Current sim state (time, tokens, status)."""
    # Lookup engine by run_id
    # Return SimStatusResponse(run_id, status=engine.state, current_time=engine.clock.now, active_tokens=len(engine.tokens.active))
```

**Route 8: Inject Token**
```python
@router.post("/sim/inject")
async def inject_token(request: InjectTokenRequest) -> InjectTokenResponse:
    """Inject token at runtime."""
    # Lookup engine by run_id
    # Call engine.inject_token(node_id, entity_data)
    # Emit SIM_TOKEN_INJECTED to ledger
    # Return InjectTokenResponse(run_id, token_id)
```

**Route 9: Save Checkpoint**
```python
@router.post("/sim/checkpoint")
async def save_checkpoint(request: CheckpointRequest) -> CheckpointResponse:
    """Save checkpoint."""
    # Lookup engine by run_id
    # Call engine.checkpoint() → returns checkpoint_id and state_snapshot
    # Emit SIM_CHECKPOINT to ledger with state_snapshot in payload
    # Return CheckpointResponse(run_id, checkpoint_id)
```

**Route 10: Restore Checkpoint**
```python
@router.post("/sim/restore")
async def restore_checkpoint(request: RestoreRequest) -> RestoreResponse:
    """Restore from checkpoint."""
    # Lookup engine by run_id
    # Call engine.restore(checkpoint_id)
    # Emit SIM_RESTORED to ledger
    # Return RestoreResponse(run_id, restored_time=engine.clock.now)
```

**Route 11: Fork Simulation (Alterverse)**
```python
@router.post("/sim/fork")
async def fork_sim(request: ForkRequest) -> ForkResponse:
    """Fork simulation (Alterverse branch)."""
    # Lookup engine by run_id
    # Call engine.fork() → returns new_run_id and branch_id
    # Store forked engine in global dict
    # Emit SIM_FORK to ledger
    # Return ForkResponse(parent_run_id=run_id, branch_run_id=new_run_id, branch_id=branch_id)
```

**Route 12: List Active Tokens**
```python
@router.get("/sim/tokens")
async def get_tokens(run_id: str) -> TokensResponse:
    """List active tokens."""
    # Lookup engine by run_id
    # Return TokensResponse(run_id, tokens=[...engine.tokens.active...])
```

**Route 13: Get Resource Utilization**
```python
@router.get("/sim/resources")
async def get_resources(run_id: str) -> ResourcesResponse:
    """Resource utilization."""
    # Lookup engine by run_id
    # Return ResourcesResponse(run_id, resources=[...engine.resources.all...])
```

**Route 14: Get Statistics**
```python
@router.get("/sim/statistics")
async def get_statistics(run_id: str) -> StatisticsResponse:
    """Current stats snapshot."""
    # Lookup engine by run_id
    # Return StatisticsResponse(run_id, stats=engine.statistics.summary())
```

**Route 15: Get Recent Events**
```python
@router.get("/sim/events")
async def get_events(run_id: str, limit: int = 100) -> EventsResponse:
    """Recent sim events (from ledger)."""
    # Query ledger for events where actor=f"sim:{run_id}"
    # Use LedgerReader to fetch events
    # Return EventsResponse(run_id, events=[...])
```

**Route 16: Parameter Sweep**
```python
@router.post("/sim/sweep")
async def sweep_sim(request: SweepRequest) -> SweepResponse:
    """Run parameter sweep."""
    # Lookup engine by run_id
    # Call engine.sweep(param_ranges) → returns sweep_results
    # Emit SIM_SWEEP_COMPLETED to ledger
    # Return SweepResponse(run_id, sweep_id, results=sweep_results)
```

- [ ] All routes scoped to `run_id` (multiple sims can run concurrently)
- [ ] Use global dict `_engines: dict[str, SimulationEngine] = {}` to store engine instances
- [ ] All routes must handle `KeyError` if `run_id` not found → raise `HTTPException(404, "Simulation not found")`
- [ ] File size: < 500 lines (if exceeds, split into `sim.py` and `sim_helpers.py`)

### Phase 3: Pydantic Schemas
- [ ] Write `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\schemas_sim.py`
- [ ] Define all request/response models (16 routes × ~2 models each = ~32 models)
- [ ] All models inherit from `BaseModel` (from pydantic)
- [ ] Example schemas:
  - `LoadFlowRequest(BaseModel)`: `flow: dict`
  - `LoadFlowResponse(BaseModel)`: `run_id: str, status: str`
  - `StartSimRequest(BaseModel)`: `run_id: str`
  - `StartSimResponse(BaseModel)`: `run_id: str, status: str, final_time: float`
  - etc. (see spec for full list)
- [ ] File size: < 300 lines

### Phase 4: Route Registration
- [ ] Edit `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py`
- [ ] Add import: `from hivenode.routes import sim`
- [ ] Add line in `create_router()`:
  ```python
  router.include_router(sim.router, prefix='/sim', tags=['simulation'])
  ```

### Phase 5: Tests — Ledger Adapter
- [ ] Write `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\engine\des\test_ledger_adapter.py`
- [ ] Test 1: `test_adapter_emit_token_created()` — verify SIM_TOKEN_CREATED event written to ledger
- [ ] Test 2: `test_adapter_emit_node_started()` — verify SIM_NODE_STARTED event
- [ ] Test 3: `test_adapter_emit_resource_acquired()` — verify SIM_RESOURCE_ACQUIRED event
- [ ] Test 4: `test_adapter_currencies()` — verify CLOCK=sim_time, COIN=0, CARBON=0.001*events
- [ ] Test 5: `test_adapter_universal_entity_id_format()` — verify actor is `sim:{run_id}`, target is `{type}:{id}`
- [ ] Test 6: `test_adapter_missing_run_id()` — verify raises error if run_id not provided
- [ ] Test 7-10: Test each event type mapping (9 event types → at least 9 tests total)
- [ ] Use `tmp_path` fixture for ledger DB path
- [ ] Use `LedgerWriter` and `LedgerReader` to verify events
- [ ] Target: **10+ tests passing**

### Phase 6: Tests — Sim Routes (E2E)
- [ ] Write `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_sim_routes.py`
- [ ] Use `TestClient` from FastAPI
- [ ] Test 1: `test_load_flow()` — POST /sim/load with simple 3-node flow, verify 200 response, verify run_id returned
- [ ] Test 2: `test_start_sim()` — POST /sim/load, then POST /sim/start, verify simulation completes
- [ ] Test 3: `test_get_status()` — load + start, then GET /sim/status, verify status="completed"
- [ ] Test 4: `test_inject_token()` — load + start + pause, then POST /sim/inject, verify token injected
- [ ] Test 5: `test_checkpoint_restore()` — load + start + pause, POST /sim/checkpoint, POST /sim/restore, verify state restored
- [ ] Test 6: `test_fork_sim()` — load + start + pause, POST /sim/fork, verify new run_id returned
- [ ] Test 7: `test_get_tokens()` — load + start + pause, GET /sim/tokens, verify token list
- [ ] Test 8: `test_get_resources()` — load + start + pause, GET /sim/resources, verify resource list
- [ ] Test 9: `test_get_statistics()` — load + start, GET /sim/statistics, verify stats snapshot
- [ ] Test 10: `test_get_events()` — load + start, GET /sim/events, verify Event Ledger contains SIM_* events
- [ ] Test 11: `test_404_invalid_run_id()` — GET /sim/status with invalid run_id, verify 404
- [ ] Use a minimal 3-node IR flow fixture (source → process → sink)
- [ ] Target: **10+ E2E tests passing**

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass (20+ total: 10 adapter tests + 10 E2E tests)
- [ ] Edge cases:
  - Invalid run_id (404)
  - Missing flow data (400)
  - Checkpoint restore with invalid checkpoint_id (404)
  - Fork from non-existent run_id (404)
  - Inject token into completed simulation (400 or 409)

## Constraints

- **No file over 500 lines:** If `sim.py` exceeds 500 lines, split into `sim.py` (routes) and `sim_helpers.py` (engine management).
- **Hard limit: 1,000 lines:** Do NOT exceed 1,000 lines in any file.
- **No hardcoded colors:** N/A (backend only)
- **No stubs:** Every route fully implemented. If a route is complex, implement a simplified version but make it functional.
- **TDD:** Write adapter tests first, then adapter. Write route tests first, then routes.
- **Three currencies:** Every ledger event MUST include CLOCK, COIN, CARBON. No exceptions.

## Acceptance Criteria

- [ ] `engine/des/ledger_adapter.py` exists and emits events to hivenode ledger
- [ ] `hivenode/routes/sim.py` exists with 16 routes
- [ ] `hivenode/schemas_sim.py` exists with ~32 Pydantic models
- [ ] Routes registered in `hivenode/routes/__init__.py`
- [ ] 10+ adapter tests pass (`tests/engine/des/test_ledger_adapter.py`)
- [ ] 10+ E2E route tests pass (`tests/hivenode/test_sim_routes.py`)
- [ ] POST /sim/load + POST /sim/start + GET /sim/status E2E test passes
- [ ] GET /sim/events returns SIM_* events from Event Ledger
- [ ] All events include three currencies (CLOCK, COIN, CARBON)
- [ ] No file over 500 lines (flag in response if any file 400-500 lines)
- [ ] No stubs shipped

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-072-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts, failure details
5. **Build Verification** — pytest output summary (last 10 lines)
6. **Acceptance Criteria** — copy from above, mark [x] or [ ] with explanation
7. **Clock / Cost / Carbon** — all three currencies
8. **Issues / Follow-ups** — any route simplifications, any missing edge cases, integration with TASK-071

DO NOT skip any section.

## Notes

- **Parallel with TASK-071:** This task depends on TASK-071 completing the engine port. However, you can start writing tests and schemas while TASK-071 is running. If TASK-071 is not done, read the old repo's engine files to understand the interface.
- **Global engine dict:** For MVP, use a module-level dict to store engine instances. In production, this should use a proper state manager (Redis, DB, etc.), but that's a future task.
- **Blocking I/O:** `engine.run()` is blocking. For long simulations, use `asyncio.to_thread()` or mark the route as sync (remove `async`).
- **Event Ledger integration:** This is the first feature to write `SIM_*` events to the ledger. Verify events appear in GET /ledger/events after simulation runs.
- **Currencies:** CLOCK uses sim_time (not wall_time). COIN is 0 (no real cost). CARBON is estimated compute (simple heuristic: 0.001 kg CO2e per 1000 events).
