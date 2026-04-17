# TASK-W1-A: Hivenode slot reservation endpoints

## Objective
Build 3 new HTTP endpoints in hivenode to manage bee slot reservations — allowing the regent to declare how many slots a spec will consume BEFORE dispatch, so the queue runner can gate spec submissions.

## Context
Today's queue runner treats 1 spec = 1 slot, but internally a spec can spawn N bees. This creates uncontrolled concurrency explosions (10 specs → 50+ bees). The new protocol adds a bidirectional handshake:

1. Regent reads spec → estimates N bees needed
2. Regent calls `POST /build/slot-reserve` with `bee_count: N`
3. Queue runner polls `GET /build/slot-status` → sees N slots reserved
4. Queue runner only submits new specs if `available >= 1`
5. As each bee completes → regent calls `POST /build/slot-release` with `released: 1`
6. Queue runner sees freed slot → can submit next spec

The slot state is **in-memory (dict)** — no database, resets on restart. This is intentional. The queue runner will gracefully handle hivenode restart (all slots freed → proceed).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` — existing `/build/heartbeat`, `/build/claim`, `/build/release` endpoints (extend this file)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\queue.yml` — `max_parallel_bees: 10` setting

## Deliverables

### 1. In-Memory Slot State
- [ ] Add to `BuildState` class (line 71 in build_monitor.py):
  - `self.slot_reservations: dict[str, int] = {}` — maps spec_id → reserved_slot_count
  - `self.total_capacity: int` — load from `queue.yml` (`max_parallel_bees`)
- [ ] Add methods to `BuildState`:
  - `reserve_slots(spec_id: str, bee_count: int) -> dict` — reserve N slots for a spec, return `{"ok": bool, "total_reserved": int, "available": int}`
  - `release_slots(spec_id: str, released: int) -> dict` — release N slots for a spec, return `{"ok": bool, "remaining": int, "available": int}`
  - `get_slot_status() -> dict` — return `{"total_capacity": int, "reserved": int, "available": int, "reservations": dict}`

### 2. Three New Endpoints
- [ ] `POST /build/slot-reserve` — regent calls after reading spec
  - Request: `{"spec_id": str, "bee_count": int}`
  - Validation: `bee_count >= 1`, `spec_id` not empty
  - Response: `{"ok": true, "total_reserved": N, "available": M}` or error 400
- [ ] `POST /build/slot-release` — regent calls as each bee completes
  - Request: `{"spec_id": str, "released": int}`
  - Validation: `released >= 1`, cannot release more than reserved
  - Response: `{"ok": true, "remaining": N, "available": M}` or error 400
- [ ] `GET /build/slot-status` — queue runner polls
  - No parameters
  - Response: `{"total_capacity": 10, "reserved": N, "available": M, "reservations": {"spec-id": count, ...}}`

### 3. Integration with `BuildState._load_from_disk()` and `_save_to_disk()`
- [ ] Persist `slot_reservations` and `total_capacity` to `monitor-state.json` (same file as heartbeat state)
- [ ] Load them on startup (graceful defaults: empty dict, capacity = 10 if missing)

## Test Requirements

Write tests FIRST (TDD). Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_build_monitor_slots.py`

### Minimum 15 tests:
- [ ] Reserve slots: valid request returns ok, total_reserved, available
- [ ] Reserve slots: double reserve for same spec_id (overwrite vs increment — choose ONE behavior and test it)
- [ ] Reserve slots: invalid bee_count (0, negative) returns 400
- [ ] Release slots: valid request returns ok, remaining, available
- [ ] Release slots: release more than reserved returns 400
- [ ] Release slots: release for unknown spec_id (graceful: no-op or error — choose ONE)
- [ ] Slot status: empty state returns capacity=10, reserved=0, available=10
- [ ] Slot status: after reserve, reserved count increases, available decreases
- [ ] Slot status: after release, reserved count decreases, available increases
- [ ] Slot status: reservations dict contains active specs
- [ ] Persistence: reserve slots, restart state (reload from disk), slot state preserved
- [ ] Persistence: release slots, restart state, slot state preserved
- [ ] Edge case: reserve 10 slots (full capacity), available = 0
- [ ] Edge case: reserve 15 slots (exceeds capacity), available = -5 (allowed, queue runner will wait)
- [ ] Edge case: release all slots for a spec, spec_id removed from reservations dict

## Constraints
- No file over 500 lines — if `build_monitor.py` approaches 500 lines after your changes, extract slot logic to a separate file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_slots.py` and register it in `hivenode/routes/__init__.py`
- TDD: tests first
- No stubs
- Hivenode slot state is in-memory (dict) — resets on restart (this is OK)
- Backward compatible: if regent does NOT call `/slot-reserve`, queue runner defaults to 1-slot-per-spec (no change in queue runner yet — that's TASK-W1-B)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-W1-A-RESPONSE.md`

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

## Model Assignment
**Haiku** — straightforward HTTP routes with in-memory state.

## Success Criteria
- All 15+ tests pass
- Hivenode can reserve and release slots via HTTP API
- Queue runner can poll slot status (though it doesn't use it yet — that's TASK-W1-B)
- Slot state persists across hivenode restarts
- No file exceeds 500 lines
