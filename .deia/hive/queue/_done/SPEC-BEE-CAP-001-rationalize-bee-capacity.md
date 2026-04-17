# Rationalize bee capacity to single source of truth

## Objective

`max_parallel_bees` is currently defined in three places with no single source of truth. Make `queue.yml` the one authoritative value. Everything else reads from it.

## Problem Analysis

| Location | Field | Value | Role |
|----------|-------|-------|------|
| `.deia/config/queue.yml` | `budget.max_parallel_bees` | 10 | Actual enforcement — ThreadPoolExecutor cap |
| `.deia/hive/schedule.json` | `constraints.max_bees` | 10 | OR-Tools solver planning — not enforced |
| `hivenode/routes/build_monitor.py` | `slot_capacity` | 10 | Display only |

## Files to Read First

- .deia/config/queue.yml
- hivenode/routes/build_monitor.py
- hivenode/scheduler/scheduler_daemon.py
- .deia/hive/schedule.json

## Files to Modify

- .deia/config/queue.yml
- hivenode/routes/build_monitor.py
- hivenode/scheduler/scheduler_daemon.py
- .deia/hive/schedule.json

## Deliverables

- [ ] queue.yml has `max_parallel_bees: 15` and `min_parallel_bees: 5`
- [ ] scheduler_daemon.py reads constraints from queue.yml via `_load_bee_constraints()`
- [ ] build_monitor.py reads slot_capacity from queue.yml via `_load_capacity()`
- [ ] schedule.json constraints written by scheduler from queue.yml on startup
- [ ] No hardcoded `10` remaining for capacity values in scheduler_daemon.py or build_monitor.py

## Acceptance Criteria

- [ ] `queue.yml` has `max_parallel_bees: 15` and `min_parallel_bees: 5`
- [ ] Changing `max_parallel_bees` in queue.yml changes scheduler solver constraint within 30s, no restart
- [ ] `BuildState.slot_capacity` reads from queue.yml, not hardcoded
- [ ] `/build/claims` response shows capacity in "X/Y bees" format
- [ ] Both values clamped to valid range (1-20 for max, 1-max for min)
- [ ] If queue.yml unreadable, all three consumers fall back gracefully
- [ ] No hardcoded `10` remaining in scheduler_daemon.py or build_monitor.py for capacity values
- [ ] All existing tests pass

## Test Requirements

- [ ] Tests written FIRST (TDD) — before implementation
- [ ] Test file: tests/hivenode/test_bee_capacity_config.py
- [ ] Test: _load_capacity() returns value from queue.yml
- [ ] Test: _load_capacity() returns 10 on missing file
- [ ] Test: _load_capacity() clamps to 1-20 range
- [ ] Test: _load_bee_constraints() reads both max and min
- [ ] Test: _load_bee_constraints() clamps min <= max
- [ ] Test: _load_bee_constraints() falls back gracefully on bad YAML
- [ ] All tests pass
- [ ] Minimum 6 tests

## Smoke Test

- [ ] python -m pytest tests/hivenode/test_bee_capacity_config.py -v
- [ ] curl -s http://127.0.0.1:8420/build/claims | python -m json.tool

## Constraints

- No new dependencies
- No file over 500 lines
- No stubs
- No git operations
- Haiku is sufficient — do not escalate model unless blocked

## Model Assignment

haiku

## Priority

P2
