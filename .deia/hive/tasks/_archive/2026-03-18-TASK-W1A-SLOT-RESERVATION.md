# TASK-W1A: Slot Reservation System

## Objective
Add slot reservation capabilities to the `BuildState` class in `build_monitor.py` so the hive can reserve bee slots before dispatching, preventing over-subscription.

## Context
The slot reservation system prevents the queue runner from dispatching more bees than the hive can handle. This is separate from file claims (which prevent two bees from modifying the same file). The tests exist and fully specify the expected behavior via TDD.

**Key facts:**
- Slot capacity is 10 (from queue.yml max_parallel_bees)
- Reservations are per spec_id (not per bee)
- Reserving for the same spec_id OVERWRITES the previous reservation (not increment)
- Available slots can go negative (no hard rejection)
- Slot state must persist across BuildState restarts

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_build_monitor_slots.py` (26 tests — read ALL tests, they ARE the spec)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` (BuildState class, lines 71-498)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_slots.py` (Pydantic schemas)

## Deliverables

### 1. Add Attributes to BuildState Class
- [ ] `slot_capacity: int = 10` (class attribute or instance var)
- [ ] `slot_reservations: dict[str, int] = {}` (spec_id → bee_count map)

### 2. Implement Methods
- [ ] `reserve_slots(spec_id: str, bee_count: int) -> dict`
  - Returns: `{"ok": bool, "total_reserved": int, "available": int}`
  - OVERWRITES previous reservation for same spec_id (not increment)
  - Accepts any bee_count value (0, negative, or > capacity)
  - Available can go negative
  - Persists to disk after every call

- [ ] `release_slots(spec_id: str, released: int) -> dict`
  - Returns: `{"ok": bool, "remaining": int, "total_reserved": int, "available": int}`
  - Reduces reservation for spec_id by `released`
  - Cannot go below 0 (cap at 0 gracefully)
  - Removes spec_id from dict when remaining == 0
  - Unknown spec_id returns gracefully (no crash)
  - Persists to disk after every call

- [ ] `get_slot_status() -> dict`
  - Returns: `{"capacity": int, "reserved": int, "available": int, "reservations": dict[str, int]}`
  - `capacity` = 10
  - `reserved` = sum of all reservations
  - `available` = capacity - reserved (can be negative)
  - `reservations` = copy of slot_reservations dict

### 3. Add Persistence
- [ ] Load `slot_reservations` from disk in `_load_from_disk()` method
  - If field missing from old state file, default to `{}`
- [ ] Save `slot_reservations` to disk in `_save_to_disk()` method
  - Add to the data dict that gets written to JSON

## Test Requirements
- [ ] All 26 tests in `test_build_monitor_slots.py` MUST pass
- [ ] No regressions in other build_monitor tests
- [ ] Test reserve/release behavior
- [ ] Test persistence (save + reload)
- [ ] Test edge cases (negative, zero, over-capacity)

## Constraints
- No file over 500 lines (build_monitor.py is currently 568 lines — be surgical)
- No stubs — every method fully implemented
- No hardcoded colors (N/A for backend)
- Follow existing patterns in BuildState class

## Test Commands

```bash
# Run the slot reservation tests
python -m pytest tests/hivenode/routes/test_build_monitor_slots.py -v

# Ensure no regressions
python -m pytest tests/hivenode/routes/ -k build_monitor -v

# Run all hivenode tests
cd hivenode && python -m pytest tests/ -v
```

## Success Criteria
- [ ] All 26 tests in `test_build_monitor_slots.py` pass
- [ ] No regressions in other build_monitor tests
- [ ] `slot_reservations` persists across BuildState restart
- [ ] Slot capacity is 10
- [ ] No file exceeds 500 lines
- [ ] All methods fully implemented (no stubs)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-TASK-W1A-RESPONSE.md`

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
