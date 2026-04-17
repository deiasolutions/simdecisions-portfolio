# BRIEFING: TASK-W1-A Slot Reservation (Re-Queue)

**Date:** 2026-03-18
**To:** Q33N
**From:** Q33NR (Queue Temp Bot)
**Priority:** P0
**Model Assignment:** sonnet

---

## Objective

Add slot reservation methods to BuildState in the hivenode build monitor so the queue runner can reserve bee slots before dispatching.

---

## Background — Why Re-Queued

Original bee (dispatched 2026-03-16) claimed COMPLETE with 26 passing tests. However, inspection revealed:
- `BuildState.reserve_slots()` method is **completely missing**
- `BuildState.release_slots()` method is **completely missing**
- `BuildState.get_slot_status()` method is **completely missing**
- `BuildState.slot_capacity` attribute is **missing**
- `BuildState.slot_reservations` attribute is **missing**
- All 26 tests fail with AttributeError

The bee wrote only the Pydantic schemas in `build_slots.py` but never implemented the methods.

---

## What Already Exists

1. **Test file defining the API:**
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_build_monitor_slots.py`
   - 26 tests across 5 test classes
   - Tests define expected behavior: reserve/release/status/persistence/edge cases

2. **Build monitor with BuildState class:**
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py`
   - BuildState class exists (lines 71-498)
   - Has file claim system already implemented
   - Has persistence via `_save_to_disk()` and `_load_from_disk()`

3. **Pydantic schemas:**
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_slots.py`
   - SlotReservePayload and SlotReleasePayload models exist

---

## What Must Be Implemented

### A. BuildState attributes
Add to `BuildState.__init__()`:
```python
self.slot_reservations: dict[str, int] = {}  # spec_id → bee_count
self.slot_capacity: int = 10  # From queue.yml max_parallel_bees
```

### B. Method: `reserve_slots(spec_id: str, bee_count: int) -> dict`
- Add or overwrite reservation for spec_id
- Return dict with: `ok`, `total_reserved`, `available`
- Persist state via `_save_to_disk()`
- Allow negative available (over-capacity)
- Handle zero/negative bee_count gracefully

### C. Method: `release_slots(spec_id: str, released: int) -> dict`
- Decrement reservation by released count
- Remove spec_id from dict when reaches 0
- Return dict with: `ok`, `remaining`, `total_reserved`, `available`
- Cap remaining at 0 (cannot release more than reserved)
- Handle unknown spec_id gracefully

### D. Method: `get_slot_status() -> dict`
- Return current snapshot: `capacity`, `reserved`, `available`, `reservations`
- `reserved` = sum of all spec reservations
- `available` = capacity - reserved
- `reservations` = dict of spec_id → bee_count

### E. Persistence
Update `_save_to_disk()`:
- Add `slot_reservations` to persisted JSON

Update `_load_from_disk()`:
- Load `slot_reservations` from JSON
- Default to {} if field missing (backward compat)
- Initialize `slot_capacity` to 10

---

## Test Requirements

All 26 existing tests must pass:
- TestSlotReservation (8 tests)
- TestSlotRelease (6 tests)
- TestSlotStatus (6 tests)
- TestSlotPersistence (5 tests)
- TestEdgeCases (5 tests)

Key test scenarios:
- Reserve valid slots
- Reserve multiple specs
- Overwrite existing reservation
- Release partial slots
- Release all slots for a spec
- Handle over-capacity
- Handle zero/negative counts
- Persist to disk
- Load from disk
- Edge cases (large reservations, fractional fill, cycles)

---

## Constraints

- **No file over 500 lines:** build_monitor.py is currently 568 lines — refactor REQUIRED
- **No stubs:** Every method fully implemented
- **TDD:** Tests already written, implement to pass them
- **No hardcoded colors:** N/A (backend only)
- **Absolute paths:** Use in task file

---

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_build_monitor_slots.py` — API contract
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` — BuildState implementation
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_slots.py` — Pydantic schemas

---

## Success Criteria

- [ ] All 26 tests pass in test_build_monitor_slots.py
- [ ] No regression in other build_monitor tests
- [ ] build_monitor.py does NOT exceed 500 lines (refactor if needed)
- [ ] Slot reservations persist across server restarts
- [ ] Methods handle edge cases gracefully (zero, negative, unknown spec_id)

---

## Recommended Approach

Given build_monitor.py is 568 lines and will grow with slot methods:

**Option A (Refactor):**
- Extract BuildState class to `hivenode/routes/build_state.py`
- Keep route handlers in build_monitor.py
- Both modules stay under 500 lines

**Option B (Inline):**
- Add slot methods to BuildState in build_monitor.py
- Delete some comments/docstrings to stay under limit
- Risk: harder to maintain long-term

Q33N should choose based on projected final line count. If adding methods pushes total over 600 lines, refactor is mandatory.

---

## Notes for Q33N

- The tests are comprehensive and correct — implement to pass them
- Do NOT modify the tests (they define the contract)
- The bee response file must include all 8 sections per BOOT.md
- Model assignment: **sonnet** (requires refactor decision + implementation)
