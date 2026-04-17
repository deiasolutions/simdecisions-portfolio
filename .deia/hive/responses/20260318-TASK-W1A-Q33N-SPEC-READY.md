# TASK-W1-A Slot Reservation Re-Queue Spec — READY FOR QUEUE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-18
**Bot ID:** Q33N (QUEEN-2026-03-18-BRIEFING-TASK-W1A-s)

---

## What Was Done

I have updated the spec file for TASK-W1-A (slot reservation) with comprehensive implementation guidance based on the re-queue briefing from Q33NR.

### Spec File Updated

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-18-SPEC-REQUEUE-TASKW1A-slot-reservation.md`

**Changes:**
- Replaced 51-line stub spec with 462-line comprehensive spec
- Added detailed method signatures and behavior specifications for all 3 methods (reserve_slots, release_slots, get_slot_status)
- Documented all 26 test requirements with expected behavior
- Specified exact persistence changes needed (save + load)
- Added mandatory refactor instructions (extract BuildState to separate file)
- Included line-by-line test contract expectations
- Added implementation notes with patterns to follow
- Specified edge case handling (zero/negative counts, over-capacity, unknown spec_id)
- Listed all expected files touched (created + modified)

---

## Spec Contents Summary

### Core Deliverables Defined

**A. BuildState Attributes:**
- `self.slot_reservations: dict[str, int]` (spec_id → bee_count)
- `self.slot_capacity: int = 10`

**B. Method: reserve_slots(spec_id, bee_count) → dict**
- Returns: `{ok, total_reserved, available}`
- Overwrite behavior (not increment)
- Allows over-capacity (available can go negative)
- Handles zero/negative bee_count gracefully

**C. Method: release_slots(spec_id, released) → dict**
- Returns: `{ok, remaining, total_reserved, available}`
- Decrements reservation, removes spec_id when reaches 0
- Caps remaining at 0 (cannot release more than reserved)
- Handles unknown spec_id gracefully

**D. Method: get_slot_status() → dict**
- Returns: `{capacity, reserved, available, reservations}`
- Current snapshot of slot allocation

**E. Persistence:**
- Update `_save_to_disk()` to write `slot_reservations`
- Update `_load_from_disk()` to read with backward compat

**F. Refactor (MANDATORY):**
- Extract BuildState to `build_state.py` (~450-480 lines)
- Update `build_monitor.py` to import BuildState (~100-150 lines)
- Both files MUST stay under 500 lines

### Test Requirements

**Primary:** 26 tests in `test_build_monitor_slots.py` (ALL must pass)
- 8 TestSlotReservation tests
- 6 TestSlotRelease tests (note: spec counted wrong, actually 5 based on test file)
- 6 TestSlotStatus tests (note: spec counted wrong, actually 5 based on test file)
- 5 TestSlotPersistence tests
- 5 TestEdgeCases tests

**Regression:** All existing `test_build_monitor.py` tests must still pass

### Files Touched (Expected)

**Created:**
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_state.py`
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-TASK-W1-A-RESPONSE.md`

**Modified:**
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py`

**NOT Modified:**
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_build_monitor_slots.py`
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_slots.py`

---

## Key Guidance for Bee

1. **Read tests FIRST** — The 26 tests define the exact contract
2. **Refactor is mandatory** — build_monitor.py is 568 lines, will exceed 600+ with new methods
3. **Follow file claims pattern** — Similar structure already exists (lines 419-488)
4. **No test modifications** — Implement to pass tests as-is
5. **Persistence critical** — Must survive server restarts
6. **Edge cases matter** — Zero/negative counts, over-capacity, unknown specs

---

## Differences from Original Spec

The original stub spec (51 lines) was missing:
- Exact method signatures and return types
- Detailed behavior specifications for each method
- All 26 test requirements mapped to expected behavior
- Persistence implementation details
- Mandatory refactor requirement (file size issue)
- Edge case handling specifications
- Implementation notes and patterns to follow

The new spec (462 lines) provides complete implementation guidance so the bee can succeed without guessing.

---

## Spec Quality Check

- [x] All 3 methods documented with signatures
- [x] All 26 tests mapped to expected behavior
- [x] Persistence changes specified (save + load)
- [x] Refactor strategy detailed (step-by-step)
- [x] Edge cases enumerated
- [x] Absolute file paths used throughout
- [x] No stubs allowed (explicitly stated)
- [x] Response file requirements (8 sections)
- [x] Success criteria clear (26/26 tests pass, no regressions)

---

## Ready for Queue Runner

The spec file is now in `.deia/hive/queue/` and ready for the queue runner to pick up. The queue runner will:
1. Parse the spec
2. Dispatch a sonnet bee with this spec
3. Monitor progress via build monitor
4. Auto-commit bee output on completion

No manual dispatch needed.

---

## Clock / Cost / Carbon

- **Clock:** 8 minutes (reading briefing + test file + build_monitor + writing comprehensive spec)
- **Cost:** ~$0.03 USD (sonnet, ~6K input + ~4K output tokens)
- **Carbon:** ~0.2g CO2e

---

## Next Steps

For Q33NR:
1. Review this completion report
2. Check that spec file is comprehensive
3. Confirm queue runner will process it (or manually dispatch if queue not running)
4. Wait for bee completion
5. Review bee response file when done

For Q88N (if queue not running):
- Decision needed: Wait for queue runner OR manually dispatch now?

---

## Notes

- The briefing was excellent — provided all context needed
- Test file inspection was critical to understand exact expectations
- File refactor is mandatory (build_monitor.py already 568 lines)
- Previous bee's failure was complete (wrote schemas only, zero implementation)
- This spec should prevent re-queue cycle (all edge cases documented)

---

**Q33N (Coordinator) — Work complete, awaiting Q33NR review**
