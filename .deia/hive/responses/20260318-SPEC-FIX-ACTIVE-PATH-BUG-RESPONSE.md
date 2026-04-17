# SPEC-FIX-ACTIVE-PATH-BUG: Fix cycle specs reference _done/ path -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-18

## Files Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\fix_cycle.py` (lines 89, 168)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_fix_cycle.py` (lines 88-113)

## What Was Done
- Fixed `generate_fix_spec()` to reference `_done/` path instead of `_active/` path (line 89)
- Fixed `generate_q33n_fix_spec()` to reference `_done/` path instead of `_active/` path (line 168)
- Updated test `test_generate_fix_spec_references_original_spec()` to expect the `_done/` path
- Computation: `done_path = original_spec.path.parent.parent / "_done" / original_spec.path.name`

## Test Results
- Test file: `.deia/hive/scripts/queue/tests/test_fix_cycle.py`
- All 16 tests passing
- Relevant tests run: 45 (test_fix_cycle.py + test_run_queue.py)
- Pass/fail: 45 passed, 0 failed

## Build Verification
```
============================= 45 passed in 4.32s ==============================
```

All queue runner and fix cycle tests pass with no regressions.

## Acceptance Criteria
- [x] Fix specs reference _done/ path, not _active/ path
- [x] Fix cycle still works end-to-end (fix spec can find the original)
- [x] No regressions in queue runner tests
- [x] Smoke tests: test_fix_cycle.py passes (16/16)
- [x] Smoke tests: test_run_queue.py passes (29/29)

## Clock / Cost / Carbon
- **Clock:** 8 minutes
- **Cost:** $0.02 USD (estimated)
- **Carbon:** 0.5g CO2e (estimated)

## Issues / Follow-ups
None. The fix is complete and all tests pass. The queue runner will now correctly reference specs in the `_done/` directory when generating fix specs.

## Technical Details
The bug occurred because `generate_fix_spec()` and `generate_q33n_fix_spec()` were called **before** the original spec was moved from `_active/` to `_done/`. The functions used `original_spec.path` directly, which pointed to the `_active/` location. By the time the fix spec was processed, the original had been moved to `_done/`, making the reference invalid.

The fix computes the `_done/` path at generation time using: `original_spec.path.parent.parent / "_done" / original_spec.path.name`

This works because:
- `original_spec.path` = `.deia/hive/queue/_active/2026-03-18-SPEC-foo.md`
- `original_spec.path.parent` = `.deia/hive/queue/_active/`
- `original_spec.path.parent.parent` = `.deia/hive/queue/`
- `original_spec.path.parent.parent / "_done"` = `.deia/hive/queue/_done/`
- Final: `.deia/hive/queue/_done/2026-03-18-SPEC-foo.md`
