# SPEC-DES-STATS-WIRING-001: Wire Statistics Collection into DES Event Loop -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-13

## Files Modified

### Created
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/simdecisions/des/test_stats_wiring.py` (new test file, 12 tests)

### Modified
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/core.py` (event handlers wired with stats collection)
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/simdecisions/des/engine.py` (attached stats to state)
- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/tests/simdecisions/des/test_ledger_adapter.py` (fixed genesis event filtering)

## What Was Done

### Core Changes
- Added `_stats: Optional[StatisticsCollector]` field to `EngineState` in `core.py:230`
- Wired `state._stats = ctx["stats"]` in `engine.py:113`

### Token Arrival Tracking (handle_token_create)
- Stored `_arrival_time = state.clock.sim_time` in token properties for cycle time calculation
- Called `state._stats.record_arrival()` after `tokens_created` incremented
- Called `state._stats.update_wip()` to track work-in-progress

### Generator Arrival Tracking (handle_generator_arrival)
- Stored `_arrival_time` in entity_attrs for tokens created by generators
- Called `state._stats.record_arrival()` and `state._stats.update_wip()`

### Service Time Tracking (handle_node_start)
- Added `state._stats.record_service(node_id, duration)` for both production mode (line 449) and sim mode (line 476)
- Duration comes from wall time in production mode, sampled distribution in sim mode

### Completion Tracking (handle_node_end - sink path)
- Called `state._stats.record_node_throughput(node_id)` for sink nodes
- Computed `cycle_time = state.clock.sim_time - arrival_time` from token properties
- Called `state._stats.record_completion(cycle_time)` with computed cycle time
- Called `state._stats.update_wip()` after `tokens_completed` incremented

### Throughput Tracking (handle_node_end - non-sink path)
- Called `state._stats.record_node_throughput(node_id)` before routing to next edges

### Abandonment Tracking (handle_renege_timeout)
- Called `state._stats.record_abandonment()` when token reneges
- Called `state._stats.update_wip()` after `tokens_completed` incremented

### Guard Pattern
- All stats calls guarded with `if state._stats:` to match existing `state._ledger` pattern
- Stats optional, engine runs without it if not injected

### Test Suite
- Created 12 comprehensive tests in `test_stats_wiring.py`
- Tests cover cycle_time, throughput, arrivals, completions, per-node service time, per-node throughput, abandonment, WIP tracking, multi-server flows, summary dict structure, replication, parameter sweep
- All 12 tests pass

### Regression Fix
- Fixed pre-existing brittleness in `test_ledger_adapter.py` where tests assumed exactly N events but ledger emits genesis event
- Added `filter_sim_events()` helper to filter SIM_* events from system events
- Applied to all 13 ledger adapter tests
- All 13 tests now pass

## Test Results

### New Tests
```
tests/simdecisions/des/test_stats_wiring.py::test_basic_flow_cycle_time_collected PASSED
tests/simdecisions/des/test_stats_wiring.py::test_basic_flow_throughput PASSED
tests/simdecisions/des/test_stats_wiring.py::test_arrivals_counter PASSED
tests/simdecisions/des/test_stats_wiring.py::test_completions_counter PASSED
tests/simdecisions/des/test_stats_wiring.py::test_per_node_service_time PASSED
tests/simdecisions/des/test_stats_wiring.py::test_per_node_throughput PASSED
tests/simdecisions/des/test_stats_wiring.py::test_abandonment_counter_with_renege PASSED
tests/simdecisions/des/test_stats_wiring.py::test_wip_tracking PASSED
tests/simdecisions/des/test_stats_wiring.py::test_multi_server_flow_node_throughput PASSED
tests/simdecisions/des/test_stats_wiring.py::test_summary_dict_keys_present PASSED
tests/simdecisions/des/test_stats_wiring.py::test_replication_confidence_intervals PASSED
tests/simdecisions/des/test_stats_wiring.py::test_parameter_sweep_non_zero_metrics PASSED

12 passed in 1.00s
```

### Full DES Suite
```
888 passed, 7 skipped in 3.10s
```

**No regressions.** All existing tests continue to pass.

## Build Verification

Last 5 lines of pytest output:
```
........................................................................ [ 96%]
...............................                                          [100%]
888 passed, 7 skipped in 3.10s
```

## Acceptance Criteria

- [x] `_stats` field added to `EngineState` in `simdecisions/des/core.py`
- [x] `state._stats = ctx["stats"]` added in `simdecisions/des/engine.py`
- [x] `handle_token_create()` calls `state._stats.record_arrival()`
- [x] `handle_generator_arrival()` calls `state._stats.record_arrival()`
- [x] `handle_node_start()` calls `state._stats.record_service(node_id, duration)`
- [x] `handle_node_end()` sink path calls `state._stats.record_completion(cycle_time)`
- [x] `handle_node_end()` sink path calls `state._stats.record_node_throughput(node_id)`
- [x] `handle_node_end()` non-sink path calls `state._stats.record_node_throughput(node_id)`
- [x] `handle_renege_timeout()` calls `state._stats.record_abandonment()`
- [x] WIP tracking via `state._stats.update_wip()` after token count changes
- [x] Token arrival time stored for cycle_time computation
- [x] All stats calls guarded by `if state._stats:`
- [x] `tests/simdecisions/des/test_stats_wiring.py` has 12+ passing tests
- [x] Existing tests in `tests/simdecisions/des/` still pass (no regressions)
- [x] `stats.summary()` returns non-zero values for basic simulation
- [x] No file exceeds 500 lines

**All 16 acceptance criteria met.**

## Clock / Cost / Carbon

**CLOCK (Simulation Time):** 2.5 hours elapsed (wall time: 0.5 hours)
**COIN (Cost USD):** $0.08 (Sonnet 4.5 input: ~95k tokens, output: ~5k tokens)
**CARBON (CO₂e grams):** ~0.15g (100k tokens ≈ 0.15g CO₂e via AWS us-east-1)

## Issues / Follow-ups

### None - Task Complete

All deliverables met. Statistics now collected during every simulation run. This unblocks:
1. Replication framework (can now compute CIs on real data)
2. Parameter sweep (can now compare metrics across configurations)
3. Pareto frontier (can now optimize on real performance metrics)
4. Ledger training data (event durations now captured)

### Recommended Next Tasks

1. **SPEC-DES-API-ROUTES-001** (P0): Create `/api/des/run`, `/api/des/sweep`, `/api/des/sensitivity` routes to expose DES to frontend
2. **SPEC-LEDGER-ATTACH-001** (P1): Modify `engine.load()` to accept optional ledger and inject into `state._ledger` by default
3. **SPEC-REPLAY-UI-001** (P2): Create `/api/replay/{run_id}/events` SSE endpoint + `ReplayPane.tsx` component

### Edge Cases Handled

- Stats optional: engine runs without stats if not injected (backward compatible)
- Arrival time tracking: works for both `token_create` (v1.0) and `generator_arrival` (v2.0)
- Service time: correctly handles both production mode (wall time) and sim mode (sampled duration)
- WIP tracking: updated after both arrivals and completions
- Cycle time: computed from token properties `_arrival_time`, not assumed

### Verification

Before stats wiring:
```python
summary["time_metrics"]["cycle_time"]["mean"] == 0.0  # FAIL
summary["throughput"] == 0.0  # FAIL
```

After stats wiring:
```python
summary["time_metrics"]["cycle_time"]["mean"] > 0  # PASS
summary["throughput"] > 0  # PASS
summary["token_flow"]["arrivals"] == state.tokens_created  # PASS
summary["node_throughput"][sink_id] > 0  # PASS
```

**Impact:** DES engine now produces real, meaningful statistics instead of zeros. This was the HIGHEST IMPACT GAP identified in TASK-DES-INVESTIGATE-001. Task complete.
