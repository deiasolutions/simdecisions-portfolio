# Briefing: TASK-W1-A (RE-QUEUE) — Slot Reservation System

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Queen Regent)
**Date:** 2026-03-18
**Priority:** P0
**Model:** sonnet

---

## Background

Original bee (TASK-W1-A, 2026-03-16 22:00) claimed COMPLETE with 26 tests passing, but the tests are actually all failing because `BuildState.reserve_slots()` method was never written. The bee only created the Pydantic schemas in `build_slots.py` but never implemented the actual slot reservation logic in `BuildState` class.

## Objective

Add slot reservation capabilities to the `BuildState` class in `build_monitor.py` so the hive can reserve bee slots before dispatching, preventing over-subscription.

## What Exists

1. **Tests:** `tests/hivenode/routes/test_build_monitor_slots.py` (26 tests, all currently failing)
   - These tests fully specify the expected API and behavior
   - Tests are TDD — they define what needs to be built

2. **Schemas:** `hivenode/routes/build_slots.py`
   - `SlotReservePayload(spec_id, bee_count)`
   - `SlotReleasePayload(spec_id, released)`

3. **Build monitor:** `hivenode/routes/build_monitor.py`
   - `BuildState` class exists (lines 71-498)
   - Has persistence via `monitor-state.json`
   - Has `_load_from_disk()` and `_save_to_disk()` methods

## What Is Missing

The `BuildState` class needs these additions:

1. **Attributes:**
   - `slot_capacity` (int) — should be 10 (from queue.yml max_parallel_bees)
   - `slot_reservations` (dict[str, int]) — spec_id → bee_count map

2. **Methods:**
   - `reserve_slots(spec_id: str, bee_count: int) -> dict`
   - `release_slots(spec_id: str, released: int) -> dict`
   - `get_slot_status() -> dict`

3. **Persistence:**
   - Load `slot_reservations` from disk in `_load_from_disk()`
   - Save `slot_reservations` to disk in `_save_to_disk()`

## Expected Behavior (from tests)

### `reserve_slots(spec_id, bee_count)`
Returns: `{"ok": bool, "total_reserved": int, "available": int}`

- Accepts bee_count (can be 0, negative, or > capacity)
- Overwrites previous reservation for same spec_id (not increment)
- Available can go negative (no hard rejection)
- Persists to disk after every call

### `release_slots(spec_id, released)`
Returns: `{"ok": bool, "remaining": int, "total_reserved": int, "available": int}`

- Reduces the reservation for spec_id by `released`
- Cannot go below 0 (graceful capping)
- Removes spec_id from dict when remaining == 0
- Unknown spec_id returns gracefully (no crash)
- Persists to disk after every call

### `get_slot_status()`
Returns: `{"capacity": int, "reserved": int, "available": int, "reservations": dict[str, int]}`

- `capacity` = 10
- `reserved` = sum of all reservations
- `available` = capacity - reserved (can be negative)
- `reservations` = copy of slot_reservations dict

## Files to Read First

1. `hivenode/routes/build_monitor.py` (BuildState class)
2. `tests/hivenode/routes/test_build_monitor_slots.py` (26 tests — these ARE the spec)
3. `hivenode/routes/build_slots.py` (Pydantic schemas)

## Constraints

- No file over 500 lines (build_monitor.py is currently 568 lines — keep additions minimal)
- No stubs — every method must be fully implemented
- All 26 tests must pass
- No regressions on existing build monitor tests

## Test Commands

```bash
# Run the failing tests
python -m pytest tests/hivenode/routes/test_build_monitor_slots.py -v

# Run all build monitor tests (ensure no regressions)
python -m pytest tests/hivenode/routes/ -k build_monitor -v
```

## Success Criteria

- [ ] All 26 tests in `test_build_monitor_slots.py` pass
- [ ] No regressions in other build_monitor tests
- [ ] `slot_reservations` persists across BuildState restart
- [ ] Slot capacity is 10
- [ ] No file exceeds 500 lines

## Notes

This is a re-queue because the original bee did not implement the methods. The tests are excellent TDD specs — read them first, implement exactly what they expect.

The slot reservation system is NOT connected to file claims. These are two separate systems:
- **File claims:** prevent two bees from modifying the same file simultaneously
- **Slot reservations:** prevent queue runner from dispatching more bees than hive can handle

---

**Q33N: Please write task file(s) for this work. Return to me for review before dispatching.**
