# SPEC-FACTORY-CLAIMS-001-persist-claims: Persist File Claims Across Restarts

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

File claims in `BuildState` are in-memory only and lost on hivenode restart. This means two bees could claim the same files after a restart if specs are still active. Add claims to the `_save_to_disk()` and `_load_from_disk()` methods so they survive restarts.

## Files to Read First

- hivenode/routes/build_monitor.py
- hivenode/routes/build_monitor_claims.py

## Acceptance Criteria

- [ ] `_save_to_disk()` in `build_monitor.py` includes `claims` dict in `monitor-state.json`
- [ ] `_load_from_disk()` in `build_monitor.py` restores `claims` dict from `monitor-state.json`
- [ ] Claims for tasks that are no longer in `self.tasks` (or whose status is terminal) are pruned on load
- [ ] `claim_waiters` are NOT persisted (they are runtime-only async queues)
- [ ] On load, if a claimed task no longer exists, the claim is released
- [ ] All existing tests still pass
- [ ] 3+ new tests: claims survive restart, stale claims pruned on load, claim_waiters not persisted

## Smoke Test

- [ ] Start hivenode, create a claim via API, restart hivenode, verify claim still exists via `/build/status`

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Only modify build_monitor.py — do not change the claims API surface
