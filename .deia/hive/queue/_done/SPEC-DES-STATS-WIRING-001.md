# SPEC-DES-STATS-WIRING-001: Wire Statistics Collection into DES Event Loop

**Created:** 2026-04-13
**Priority:** P0
**Model:** sonnet
**Role:** bee
**Estimated Cost:** $3.00

---

## Objective

Wire the existing `StatisticsCollector` methods into the DES event handlers in `core.py` so that simulations produce real statistics instead of zeros.

---

## Files to Read First

- `simdecisions/des/core.py`
- `simdecisions/des/statistics.py`
- `simdecisions/des/engine.py`
- `simdecisions/des/tokens.py`
- `.deia/hive/responses/20260413-TASK-DES-INVESTIGATE-001-RESPONSE.md`

---

## Deliverables

### 1. Attach stats to EngineState

| File | Location | Change |
|------|----------|--------|
| `simdecisions/des/core.py` | `EngineState` class (~line 214) | Add field `_stats: Optional[StatisticsCollector] = None` |
| `simdecisions/des/engine.py` | `SimulationEngine.load()` after line 89 | Add `state._stats = ctx["stats"]` |

### 2. Track token arrival time

| File | Location | Change |
|------|----------|--------|
| `simdecisions/des/core.py` | `handle_token_create()` (~line 326) | Store `_arrival_time = state.clock.sim_time` in token properties |
| `simdecisions/des/core.py` | `handle_generator_arrival()` (~line 585) | Store `_arrival_time = state.clock.sim_time` in token properties |

### 3. Wire record calls into event handlers

All calls guarded by `if state._stats:` to match existing `state._ledger` pattern.

| File | Handler | Location | Stats Call |
|------|---------|----------|------------|
| `simdecisions/des/core.py` | `handle_token_create()` | After `state.tokens_created += 1` (~line 326) | `state._stats.record_arrival()` |
| `simdecisions/des/core.py` | `handle_generator_arrival()` | After `state.tokens_created += 1` (~line 585) | `state._stats.record_arrival()` |
| `simdecisions/des/core.py` | `handle_node_start()` | After duration determined (~line 446, ~line 472) | `state._stats.record_service(node_id, duration)` |
| `simdecisions/des/core.py` | `handle_node_end()` | Sink path after `state.tokens_completed += 1` (~line 503) | `state._stats.record_node_throughput(node_id)` then `state._stats.record_completion(cycle_time)` |
| `simdecisions/des/core.py` | `handle_node_end()` | Non-sink path before routing (~line 529) | `state._stats.record_node_throughput(node_id)` |
| `simdecisions/des/core.py` | `handle_renege_timeout()` | After `state.tokens_completed += 1` (~line 557) | `state._stats.record_abandonment()` |

### 4. WIP tracking

| File | Location | Stats Call |
|------|----------|------------|
| `simdecisions/des/core.py` | After every `tokens_created += 1` | `state._stats.update_wip(state.tokens_created - state.tokens_completed, state.clock.sim_time)` |
| `simdecisions/des/core.py` | After every `tokens_completed += 1` | `state._stats.update_wip(state.tokens_created - state.tokens_completed, state.clock.sim_time)` |

### 5. Cycle time computation at sink

| File | Location | Change |
|------|----------|--------|
| `simdecisions/des/core.py` | `handle_node_end()` sink path (~line 503) | Retrieve `_arrival_time` from token properties, compute `cycle_time = state.clock.sim_time - arrival_time` |

---

## Test Requirements

- [ ] Create `tests/simdecisions/des/test_stats_wiring.py`

| # | Test | Assertion |
|---|------|-----------|
| 1 | Simple flow (Source → Queue → Service → Sink) | `summary()["cycle_time"]["mean"] > 0` |
| 2 | Simple flow throughput | `summary()["throughput"] > 0` |
| 3 | Arrivals counter | `summary()["arrivals"] == state.tokens_created` |
| 4 | Completions counter | `summary()["completions"] == state.tokens_completed` |
| 5 | Per-node service time | `summary()["node_service_time"][service_node_id]["mean"] > 0` |
| 6 | Per-node throughput | `summary()["node_throughput"][sink_node_id] > 0` |
| 7 | Abandonment counter | `summary()["abandonments"] > 0` (flow with renege timeout) |
| 8 | WIP tracking | `summary()["wip"]["mean"] > 0` |
| 9 | Multi-server flow (3 servers) | Per-node throughput for each server node |
| 10 | Summary dict keys | All expected keys present and non-zero |
| 11 | Replication (5 runs) | Confidence interval width > 0 |
| 12 | Parameter sweep | Non-zero metrics in sweep results |

**Total:** 12 tests minimum. TDD required.

---

## Acceptance Criteria

- [ ] `_stats` field added to `EngineState` in `simdecisions/des/core.py`
- [ ] `state._stats = ctx["stats"]` added in `simdecisions/des/engine.py`
- [ ] `handle_token_create()` calls `state._stats.record_arrival()`
- [ ] `handle_generator_arrival()` calls `state._stats.record_arrival()`
- [ ] `handle_node_start()` calls `state._stats.record_service(node_id, duration)`
- [ ] `handle_node_end()` sink path calls `state._stats.record_completion(cycle_time)`
- [ ] `handle_node_end()` sink path calls `state._stats.record_node_throughput(node_id)`
- [ ] `handle_node_end()` non-sink path calls `state._stats.record_node_throughput(node_id)`
- [ ] `handle_renege_timeout()` calls `state._stats.record_abandonment()`
- [ ] WIP tracking via `state._stats.update_wip()` after token count changes
- [ ] Token arrival time stored for cycle_time computation
- [ ] All stats calls guarded by `if state._stats:`
- [ ] `tests/simdecisions/des/test_stats_wiring.py` has 12+ passing tests
- [ ] Existing tests in `tests/simdecisions/des/` still pass (no regressions)
- [ ] `stats.summary()` returns non-zero values for basic simulation
- [ ] No file exceeds 500 lines

---

## Constraints

- Guard all stats calls with `if state._stats:`
- Do NOT modify `StatisticsCollector` class itself
- Do NOT create new files except `tests/simdecisions/des/test_stats_wiring.py`
- Do NOT add API routes
- Follow existing `state._ledger` injection pattern
- No stubs

---

## Response Requirements — MANDATORY

Write response to: `.deia/hive/responses/20260413-SPEC-DES-STATS-WIRING-001-RESPONSE.md`

1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full absolute paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — pass/fail counts, pytest output summary
5. **Build Verification** — last 5 lines of pytest output
6. **Acceptance Criteria** — mark [x] or [ ] for each item above
7. **Clock / Cost / Carbon** — all three currencies
8. **Issues / Follow-ups** — edge cases, recommended next tasks
