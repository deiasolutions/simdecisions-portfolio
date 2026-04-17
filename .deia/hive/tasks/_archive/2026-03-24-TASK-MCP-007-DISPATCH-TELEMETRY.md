# TASK-MCP-007: Dispatch, Heartbeat, Telemetry, Sync Queue

## Objective
Implement `dispatch_bee`, `heartbeat`, `status_report`, `cost_summary` MCP tools and the sync queue writer for future cloud sync.

## Context
Phase 1 of SPEC-HIVE-MCP-001-v2. `dispatch_bee` wraps the existing `.deia/hive/scripts/dispatch/dispatch.py`. Heartbeat enables opt-in bee-initiated telemetry (dispatch.py's existing heartbeat continues as fallback). Sync queue writes state to `~/.shiftcenter/sync_queue/` for future Phase 3 cloud sync.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py` (existing dispatch)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\local_server.py` (tool registration)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\state.py` (state storage)
- `C:\Users\davee\Downloads\SPEC-HIVE-MCP-001-v2.md` (sections 4.2, 4.4, 3.4.3)

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tools\dispatch.py`:
  - `dispatch_bee(task_file: str, model: str, role: str, inject_boot: bool = True)` — wraps `.deia/hive/scripts/dispatch/dispatch.py`
  - Runs dispatch as subprocess (background by default)
  - Returns PID and confirmation
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tools\telemetry.py`:
  - `heartbeat(bee_id: str, task_id: str, status: str, model: str, input_tokens: Optional[int], output_tokens: Optional[int], cost_usd: Optional[float], message: Optional[str])` — wraps existing `/build/heartbeat` POST endpoint
  - `status_report()` — returns all active bees, tasks, liveness, costs from state manager
  - `cost_summary()` — aggregated CLOCK/COIN/CARBON for current sprint
  - Heartbeat is opt-in for bees (dispatch.py continues its own heartbeat as fallback)
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\sync.py`:
  - Sync queue writer — writes JSON messages to `~/.shiftcenter/sync_queue/`
  - Message types: claims, heartbeats, tool log entries
  - One JSON file per message (timestamp-based naming)
  - Queue is read by future Phase 3 cloud sync flusher (not implemented yet)
- [ ] Register tools in `local_server.py`
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tests\test_tools_dispatch.py`
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\hive_mcp\tests\test_tools_telemetry.py`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass (15+ tests minimum)
- [ ] Edge cases tested:
  - dispatch_bee subprocess spawning
  - dispatch_bee returns PID
  - heartbeat stores data in state manager
  - heartbeat POSTs to /build/heartbeat
  - status_report aggregates active bees
  - cost_summary calculates totals
  - sync queue writes JSON files to correct directory

## Constraints
- No file over 500 lines
- No stubs
- Python 3.13
- dispatch_bee must not block (subprocess, background)
- Sync queue dir: `~/.shiftcenter/sync_queue/` (outside OneDrive)
- heartbeat wraps existing `/build/heartbeat` endpoint, does not replace dispatch.py's heartbeat
- Existing dispatch.py location: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py`
- Existing heartbeat endpoint: `POST http://localhost:8420/build/heartbeat`

## Acceptance Criteria
- [ ] dispatch_bee runs dispatch.py as subprocess and returns PID
- [ ] dispatch_bee passes all args correctly (task_file, model, role, inject_boot)
- [ ] heartbeat stores data in state manager
- [ ] heartbeat POSTs to /build/heartbeat endpoint
- [ ] status_report returns all active bees and tasks from state
- [ ] cost_summary returns aggregated CLOCK/COIN/CARBON
- [ ] Sync queue writes JSON files to `~/.shiftcenter/sync_queue/`
- [ ] Sync queue creates directory if it doesn't exist
- [ ] 15+ tests passing
- [ ] No stubs

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-MCP-007-RESPONSE.md`

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
