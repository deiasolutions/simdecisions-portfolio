# QUEUE-TEMP-SPEC-FACTORY-WAKE-001-fix-wake-events -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-04-14

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\main.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\scripts\queue\run_queue.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\scripts\queue\dispatch_handler.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\tests\hivenode\test_queue_watcher_wake.py` (new test file)

## What Was Done

**Issue 1: Queue watcher only wakes on spec_backlog, not spec_queued**
- Modified `_on_queue_event` callback in `hivenode/main.py` line 403
- Changed condition from `event_type == "queue.spec_backlog"` to `event_type in ("queue.spec_backlog", "queue.spec_queued")`
- Queue runner now wakes when dispatcher daemon moves specs to queue root (spec_queued events)

**Issue 2: send_liveness_ping() defined but never called**
- Removed `send_liveness_ping()` function from `run_queue.py` (lines 169-193)
- Updated `send_heartbeat()` docstring to remove reference to `send_liveness_ping()`
- Cleaner than adding threading/timing logic to call it every 30s

**Issue 3: Timeout message says "15 minutes" but constant is 480 seconds (8 minutes)**
- Fixed docstring in `dispatch_handler.py` line 126: "15 minutes" → "8 minutes"
- Fixed timeout message in `dispatch_handler.py` line 302: "15 minutes" → "8 minutes"
- Messages now match `WATCHDOG_STALE_SECONDS = 480` constant

## Tests Run

**Existing tests (all pass):**
- `test_dispatch_handler.py`: 21 tests including watchdog timeout tests
- `test_detect_role.py`: 14 tests for role detection from specs
- Total: 35 existing tests passing

**New tests (all pass):**
- `test_queue_watcher_wake.py`: 4 new tests
  - `test_queue_event_callback_wakes_on_spec_backlog`
  - `test_queue_event_callback_wakes_on_spec_queued`
  - `test_queue_event_callback_ignores_other_events`
  - `test_queue_event_callback_handles_none_bridge`

## Acceptance Criteria

- ✅ `_on_queue_event` callback checks for both `"queue.spec_backlog"` and `"queue.spec_queued"`
- ✅ `send_liveness_ping()` removed from `run_queue.py` (cleaner than wiring on 30s interval)
- ✅ Timeout messages in `dispatch_handler.py` now say "8 minutes" (matching 480 second constant)
- ✅ All existing tests still pass (35 tests)
- ✅ New tests added to verify wake event behavior (4 tests)

## Smoke Test Status

Manual smoke test required: Drop a spec in queue root (not backlog) and verify queue runner wakes.

**How to test:**
1. Start queue runner in watch mode: `python .deia/hive/scripts/queue/run_queue.py --watch`
2. Drop a test spec in `.deia/hive/queue/` (not `backlog/`)
3. Check logs for "Waking queue runner for <spec-file>" message
4. Verify spec is picked up and processed

## Notes

- No file over 500 lines (constraint satisfied)
- No stubs - all changes are complete implementations
- No git operations performed (per hard rule 10)
- All changes are targeted fixes with no refactoring of surrounding code
