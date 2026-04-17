# SPEC: Re-Queue TASK-W1-A — BuildState Slot Reservation Implementation

**Date:** 2026-03-18
**Priority:** P0
**Model Assignment:** sonnet

---

## Objective

Implement slot reservation methods in BuildState (build_monitor.py) to support bee concurrency control for the queue runner. All 26 existing tests must pass without modification.

---

## Why Re-Queued

Original bee (dispatched 2026-03-16) claimed COMPLETE with 26 passing tests, but inspection revealed:
- `BuildState.reserve_slots()` method **completely missing** (AttributeError on all tests)
- `BuildState.release_slots()` method **completely missing**
- `BuildState.get_slot_status()` method **completely missing**
- `BuildState.slot_capacity` attribute **missing**
- `BuildState.slot_reservations` attribute **missing**

The bee wrote only the Pydantic schemas (`build_slots.py`) but never implemented the actual methods.

---

## Context

The build monitor tracks bee heartbeats, file claims, and now needs to track slot reservations. The queue runner will reserve slots before dispatching bees to prevent over-parallelization.

Key facts:
- Build monitor already has BuildState class with persistence
- File claims system already exists (similar pattern)
- All tests are already written (TDD complete, implementation missing)
- Tests define the exact API contract

---

## Files to Read First

**CRITICAL — Read in this order:**

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_build_monitor_slots.py` (265 lines, 26 tests)
   - **THIS IS YOUR CONTRACT.** Every test must pass as-is.
   - Defines exact behavior for reserve, release, status, persistence, edge cases

2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` (568 lines)
   - BuildState class (lines 71-498)
   - Existing file claim system (lines 419-488) — similar pattern to follow
   - Persistence methods: `_save_to_disk()` (lines 110-124), `_load_from_disk()` (lines 90-108)

3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_slots.py` (19 lines)
   - Pydantic schemas for endpoints (already written, DO NOT modify)

---

## Deliverables

### A. BuildState Attributes (in `__init__`)

Add to `BuildState.__init__()` (currently line 74):

```python
self.slot_reservations: dict[str, int] = {}  # spec_id → bee_count
self.slot_capacity: int = 10  # From queue.yml max_parallel_bees
```

### B. Method: `reserve_slots(spec_id: str, bee_count: int) -> dict`

**Signature:**
```python
def reserve_slots(self, spec_id: str, bee_count: int) -> dict:
```

**Behavior:**
- Add or **overwrite** reservation for `spec_id` (not increment)
- Return dict with keys: `ok`, `total_reserved`, `available`
  - `ok`: Always `True` (graceful handling)
  - `total_reserved`: Sum of all spec reservations after this operation
  - `available`: `slot_capacity - total_reserved` (can be negative)
- Handle edge cases:
  - `bee_count == 0`: Accept, but don't add to dict (or set to 0)
  - `bee_count < 0`: Accept gracefully (either ignore or allow negative)
- Persist state via `self._save_to_disk()` after updating
- Allow over-capacity (available can go negative)

**Test contract (from test file):**
- `test_reserve_slots_valid_request`: Reserve 3 slots → total_reserved=3, available=7
- `test_reserve_slots_multiple_specs`: Two specs (3+2) → total_reserved=5, available=5
- `test_reserve_slots_overwrite_behavior`: Same spec_id twice (3→5) → total_reserved=5 (overwrite)
- `test_reserve_slots_invalid_bee_count_zero`: bee_count=0 → graceful (not crash)
- `test_reserve_slots_negative_bee_count`: bee_count=-5 → graceful (not crash)
- `test_reserve_slots_full_capacity`: Reserve 10 → available=0
- `test_reserve_slots_exceeds_capacity`: Reserve 15 → available=-5 (negative OK)

### C. Method: `release_slots(spec_id: str, released: int) -> dict`

**Signature:**
```python
def release_slots(self, spec_id: str, released: int) -> dict:
```

**Behavior:**
- Decrement reservation for `spec_id` by `released` count
- If reservation reaches 0, **remove `spec_id` from dict**
- Return dict with keys: `ok`, `remaining`, `total_reserved`, `available`
  - `ok`: Always `True`
  - `remaining`: Slots still reserved for this spec after release (capped at 0)
  - `total_reserved`: Sum of all spec reservations after release
  - `available`: `slot_capacity - total_reserved`
- Handle edge cases:
  - `spec_id` not in dict: Return gracefully (remaining=0, no crash)
  - `released > current_reservation`: Cap `remaining` at 0 (cannot go negative)
- Persist state via `self._save_to_disk()` after updating

**Test contract:**
- `test_release_slots_valid_request`: Reserve 3, release 1 → remaining=2
- `test_release_slots_all_for_spec`: Reserve 5, release 5 → remaining=0, spec removed from dict
- `test_release_slots_more_than_reserved`: Reserve 3, release 10 → remaining=0 (cap)
- `test_release_slots_unknown_spec_id`: Release unknown spec → graceful (not crash)
- `test_release_slots_removes_from_dict_when_zero`: After full release, spec not in dict

### D. Method: `get_slot_status() -> dict`

**Signature:**
```python
def get_slot_status(self) -> dict:
```

**Behavior:**
- Return current snapshot with keys: `capacity`, `reserved`, `available`, `reservations`
  - `capacity`: Always 10 (from `self.slot_capacity`)
  - `reserved`: Sum of all values in `self.slot_reservations`
  - `available`: `capacity - reserved`
  - `reservations`: Copy of `self.slot_reservations` dict

**Test contract:**
- `test_slot_status_empty_state`: capacity=10, reserved=0, available=10, reservations={}
- `test_slot_status_after_reserve`: Reserve 3 → reserved=3, available=7, reservations={'spec-001': 3}
- `test_slot_status_after_release`: Reserve 5, release 2 → reserved=3, available=7
- `test_slot_status_multiple_specs`: 3 specs (3+2+1) → reserved=6, available=4, len(reservations)=3
- `test_slot_status_after_release_all_spec`: After full release → spec removed from reservations

### E. Persistence Updates

**Update `_save_to_disk()` (line 110):**

Add `slot_reservations` to persisted JSON:

```python
data = {
    "tasks": self.tasks,
    "log": self.log,
    "total_cost": self.total_cost,
    "total_input_tokens": self.total_input_tokens,
    "total_output_tokens": self.total_output_tokens,
    "last_task_id": self._last_task_id,
    "slot_reservations": self.slot_reservations,  # ADD THIS LINE
}
```

**Update `_load_from_disk()` (line 90):**

Load `slot_reservations` with backward compat:

```python
# After loading other fields, add:
self.slot_reservations = data.get("slot_reservations", {})
self.slot_capacity = 10  # Initialize capacity
```

**Test contract:**
- `test_persistence_reserve_slots`: Reserve 2 specs → file contains both in JSON
- `test_persistence_load_on_startup`: Pre-write state file → fresh BuildState loads reservations
- `test_persistence_release_slots`: Release decrements → persisted to disk
- `test_persistence_missing_field_defaults`: Old state file (no slot_reservations) → loads with {}

### F. File Refactor (MANDATORY)

Current state:
- `build_monitor.py`: 568 lines
- Adding slot methods will push to ~650+ lines

**REQUIRED ACTION: Extract BuildState class to separate file**

Create new file:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_state.py`
- Move BuildState class (lines 71-498) to this file
- Import all dependencies (Path, datetime, json, asyncio, etc.)
- Keep route handlers in `build_monitor.py`

Update `build_monitor.py`:
- Import BuildState: `from .build_state import BuildState`
- Keep all route handlers (`@router.post`, `@router.get`)
- Keep singleton `_state = BuildState()`
- File should be ~100-150 lines after refactor

**Both files MUST stay under 500 lines.**

---

## Test Requirements

### Primary Tests (26 total)

Run: `cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter && python -m pytest tests/hivenode/routes/test_build_monitor_slots.py -v`

**ALL 26 tests MUST pass:**

- `TestSlotReservation`: 8 tests
  - valid request, multiple specs, overwrite, zero, negative, full capacity, exceeds capacity, capacity value

- `TestSlotRelease`: 6 tests
  - valid request, all for spec, more than reserved, unknown spec, removes from dict when zero

- `TestSlotStatus`: 6 tests
  - empty state, after reserve, after release, multiple specs, after release all spec

- `TestSlotPersistence`: 5 tests
  - reserve persists, load on startup, release persists, missing field defaults

- `TestEdgeCases`: 5 tests
  - large reservation, fractional fill, reserve/release cycle, partial release multiple times

### Regression Tests

Run: `cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter && python -m pytest tests/hivenode/routes/test_build_monitor.py -v`

**All existing build_monitor tests MUST still pass** (currently ~15-20 tests for heartbeat, file claims, status).

### Build Verification

After refactor:
```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode
python -m pytest tests/routes/ -v
```

All route tests must pass (build_monitor + build_monitor_slots combined).

---

## Constraints

- **No file over 500 lines:** MANDATORY refactor to separate BuildState
- **No stubs:** Every method fully implemented (no `pass`, no `# TODO`)
- **TDD:** Tests already written, implement to pass them
- **No test modifications:** DO NOT change test file at all
- **CSS:** N/A (backend only)
- **Absolute paths:** Use in response file

---

## Acceptance Criteria

- [ ] `BuildState.slot_reservations` attribute initialized in `__init__`
- [ ] `BuildState.slot_capacity` attribute initialized to 10
- [ ] `reserve_slots()` method implemented with correct signature and return dict
- [ ] `release_slots()` method implemented with correct signature and return dict
- [ ] `get_slot_status()` method implemented with correct signature and return dict
- [ ] Persistence: `_save_to_disk()` writes `slot_reservations` to JSON
- [ ] Persistence: `_load_from_disk()` reads `slot_reservations` with backward compat
- [ ] Refactor: BuildState class moved to `build_state.py`
- [ ] Refactor: `build_monitor.py` imports BuildState and stays under 500 lines
- [ ] Refactor: `build_state.py` stays under 500 lines
- [ ] All 26 tests in `test_build_monitor_slots.py` pass
- [ ] All existing tests in `test_build_monitor.py` still pass (no regression)
- [ ] No modifications to test files
- [ ] No stubs in implementation

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-TASK-W1-A-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full absolute paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts with full output
5. **Build Verification** — test output summary (show all 26 pass)
6. **Acceptance Criteria** — copy from this spec, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

---

## Implementation Notes

### Pattern to Follow (from file claims)

The file claims system (lines 419-488) provides a good reference:

```python
# Attributes in __init__:
self.claims: dict[str, dict] = {}
self.claim_waiters: dict[str, list[str]] = {}

# Method example:
def claim_files(self, task_id: str, files: list[str]) -> dict:
    # ... implementation ...
    return {"claimed": claimed, "conflicts": conflicts, "queued": queued}
```

Slot reservations follow a simpler pattern:
- No waiters (just reserve/release)
- Simpler data structure (spec_id → count)
- Similar persistence pattern

### Edge Case Handling

From test inspection:

1. **Zero/negative bee_count**: Don't crash, return gracefully
2. **Overwrite behavior**: `reserve_slots("spec-001", 5)` twice sets to 5, not 10
3. **Over-capacity**: Allowed, available goes negative
4. **Release more than reserved**: Cap remaining at 0
5. **Unknown spec_id on release**: Return graceful no-op
6. **Remove from dict when zero**: Clean up completed specs

### Refactor Strategy

**Step 1:** Create `build_state.py`
- Copy BuildState class definition (lines 71-498)
- Copy all class-level constants used by BuildState
- Copy imports needed by BuildState
- Add new slot methods to BuildState

**Step 2:** Update `build_monitor.py`
- Replace BuildState class with import: `from .build_state import BuildState`
- Keep all route handlers
- Keep singleton `_state = BuildState()`
- Verify line count < 500

**Step 3:** Test both files
- Run slot tests: All 26 pass
- Run existing tests: No regression
- Verify line counts

---

## Success Criteria Summary

**Code:**
- BuildState extracted to separate file (both < 500 lines)
- All 3 methods implemented (reserve, release, status)
- Persistence fully wired (save + load)

**Tests:**
- 26/26 slot tests pass
- 0 regressions in existing build_monitor tests

**Quality:**
- No stubs, no TODOs, no placeholder code
- Graceful edge case handling
- Clean refactor with proper imports

---

## Files Touched (Expected)

**Created:**
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_state.py` (NEW, ~450-480 lines)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-TASK-W1-A-RESPONSE.md` (NEW)

**Modified:**
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` (refactor to ~100-150 lines)

**NOT Modified:**
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_build_monitor_slots.py` (DO NOT TOUCH)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_slots.py` (schemas already written)

---

## End of Spec

Bot: Read all three files listed in "Files to Read First" BEFORE writing any code. The tests define your contract — implement exactly what they expect.
