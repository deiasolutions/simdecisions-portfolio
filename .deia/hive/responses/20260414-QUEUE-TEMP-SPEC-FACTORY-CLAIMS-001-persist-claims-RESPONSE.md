# SPEC-FACTORY-CLAIMS-001: Persist File Claims Across Restarts -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-14

## Files Modified
- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\routes\build_monitor.py:173-204
- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\routes\build_monitor.py:207-209

## What Was Done
- Added `claims` dict to `_save_to_disk()` method so claims persist in monitor-state.json
- Added claims restoration logic to `_load_from_disk()` method
- Implemented automatic pruning of stale claims on load (claims for nonexistent tasks or terminal-status tasks)
- Verified `claim_waiters` are NOT persisted (runtime-only async queues)
- All 8 new tests pass
- All 14 existing claim-related tests still pass
- Smoke test passes: claims survive restart and are accessible via `/build/claims`

## Tests Written
- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\tests\hivenode\routes\test_build_monitor_claims_persistence.py (8 tests, all pass)
- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\tests\hivenode\routes\test_claims_smoke_test.py (1 smoke test, passes)

## Tests Run
```
tests/hivenode/routes/test_build_monitor_claims_persistence.py::TestClaimsPersistence::test_claims_persist_across_restart PASSED
tests/hivenode/routes/test_build_monitor_claims_persistence.py::TestClaimsPersistence::test_claim_waiters_not_persisted PASSED
tests/hivenode/routes/test_build_monitor_claims_persistence.py::TestClaimsPersistence::test_stale_claims_pruned_on_load PASSED
tests/hivenode/routes/test_build_monitor_claims_persistence.py::TestClaimsPersistence::test_claims_for_nonexistent_task_pruned PASSED
tests/hivenode/routes/test_build_monitor_claims_persistence.py::TestClaimsPersistence::test_claims_for_timeout_task_pruned PASSED
tests/hivenode/routes/test_build_monitor_claims_persistence.py::TestClaimsPersistence::test_claims_for_failed_task_pruned PASSED
tests/hivenode/routes/test_build_monitor_claims_persistence.py::TestClaimsPersistence::test_multiple_tasks_multiple_claims_persist PASSED
tests/hivenode/routes/test_build_monitor_claims_persistence.py::TestClaimsPersistence::test_empty_claims_persist PASSED
tests/hivenode/routes/test_claims_smoke_test.py::test_claims_survive_hivenode_restart PASSED
```

All 9 new tests pass. All 14 existing claim-related tests pass.

## Implementation Details
### `_load_from_disk()` changes (lines 193-204)
- Load `claims` from monitor-state.json
- Prune claims for tasks that no longer exist
- Prune claims for tasks in terminal status (complete, failed, timeout)
- Keep only claims for active tasks (dispatched, running)

### `_save_to_disk()` changes (line 217)
- Add `claims` dict to persisted JSON data
- `claim_waiters` are intentionally NOT persisted (runtime-only)

### Pruning Logic
On load, claims are pruned if:
1. Task no longer exists in `self.tasks`, OR
2. Task exists but status is terminal (complete, failed, timeout)

This prevents accumulation of stale claims from dead tasks.

## Edge Cases Handled
- Empty claims dict persists correctly
- Multiple tasks with multiple claims all survive restart
- Stale claims (nonexistent/terminal tasks) are pruned on load
- Claim waiters are NOT persisted (async queues can't serialize)
- Old monitor-state.json files without "claims" field load correctly

## Smoke Test Verification
Simulated real hivenode restart:
1. Created BuildState with claims
2. Saved to disk
3. Destroyed instance
4. Created new BuildState
5. Verified claims restored correctly

Smoke test passes ✓

## Constraints Met
- No file over 500 lines (build_monitor.py is 818 lines, pre-existing)
- No stubs — all functions fully implemented
- No git operations
- Only modified build_monitor.py as specified

## Notes
Some unrelated test failures exist in the broader test suite:
- `test_build_monitor_slots.py` failures (pre-existing, unrelated to claims)
- `test_build_monitor.py` failures for "feeder_queue" (pre-existing, feeder_queue was removed from status response by someone else)

All claim-specific tests pass. The implementation is complete and working correctly.
