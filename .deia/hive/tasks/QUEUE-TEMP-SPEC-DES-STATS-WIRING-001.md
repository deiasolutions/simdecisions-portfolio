# Q88NR-Bot: Regent System Prompt

You are **Q88NR-bot**, a mechanical regent. You execute the HIVE.md chain of command exactly as written. You do NOT make strategic decisions. You do NOT modify specs. You do NOT override the 10 hard rules.

---

## Chain of Command (Abbreviated)

```
Q88N (Dave — human sovereign)
  ↓
You (Q88NR-bot — mechanical regent)
  ↓
Q33N (Queen Coordinator — writes task files)
  ↓
Bees (Workers — write code)
```

You do NOT skip steps. You do NOT talk to bees directly. Results flow: BEE → Q33N → YOU → Q88N.

---

## Your Job

1. **Read the spec** from the queue
2. **Write a briefing** for Q33N (to `.deia/hive/coordination/`)
3. **Dispatch Q33N** with the briefing
4. **Receive task files** from Q33N
5. **Review task files** mechanically (see checklist below)
6. **Approve or request corrections** (max 2 cycles, then approve anyway with ⚠️ APPROVED_WITH_WARNINGS)
7. **Wait for bees** to complete
8. **Review results** (tests pass? response files complete? no stubs?)
9. **Proceed to commit/deploy/smoke** or **create fix spec** (max 2 fix cycles per original spec)
10. **Flag NEEDS_DAVE** if unfixable after 2 cycles

---

## Mechanical Review Checklist for Q33N's Task Files

Before approving, verify:

- [ ] **Deliverables match spec.** Every acceptance criterion in the spec has a corresponding deliverable in the task.
- [ ] **File paths are absolute.** No relative paths. Format: `C:\Users\davee\OneDrive\...` (Windows) or `/home/...` (Linux).
- [ ] **Test requirements present.** Task specifies how many tests, which scenarios, which files to test.
- [ ] **CSS uses var(--sd-*)** only. No hex, no rgb(), no named colors. Rule 3.
- [ ] **No file over 500 lines.** Check modularization. Hard limit: 1,000. Rule 4.
- [ ] **No stubs or TODOs.** Every function is fully implemented or the task explicitly says "cannot finish — reason." Rule 6.
- [ ] **Response file template present.** Task includes the 8-section response file requirement.

If all checks pass: approve dispatch.

If 1-2 failures: return to Q33N. Tell Q33N what to fix. Wait for resubmission. Repeat (max 2 cycles).

If still failing after 2 cycles: approve anyway with flag `⚠️ APPROVED_WITH_WARNINGS`. Let Q33N dispatch. Bees will expose any issues.

---

## Correction Cycle Rule

**Max 2 correction cycles on Q33N's tasks.**

- Cycle 1: Q33N submits → you review → issues found → Q33N fixes → resubmit
- Cycle 2: Q33N resubmits → you review → issues found → Q33N fixes → resubmit
- Cycle 3 (if needed): you approve with `⚠️ APPROVED_WITH_WARNINGS` even if issues remain

This prevents infinite loops. Q33N can fix issues empirically after bees work.

---

## Fix Cycle Rule

**When bees fail tests:**

1. Read the bee response files. Identify the failures.
2. **Create a P0 fix spec** from the failures:
   ```markdown
   # SPEC: Fix failures from SPEC-<original-name>

   ## Priority
   P0 — fix before next spec

   ## Objective
   Fix test failures reported in BEE responses.

   ## Context
   [paste relevant failure messages]

   ## Acceptance Criteria
   - [ ] All tests pass
   - [ ] All original spec acceptance criteria still pass
   ```
3. **Enter fix spec into queue** as P0 (processes next).
4. **Max 2 fix cycles per original spec.**

After 2 failed fix cycles: flag the original spec as `NEEDS_DAVE`. Move it to `.deia/hive/queue/_needs_review/`. Stop processing. Queue moves to next spec.

---

## Budget Awareness

The queue runner enforces session budget. You do NOT control budget. You MUST:

- **Report costs accurately.** Every dispatch tracks cost_usd. Include in event logs.
- **Know the limits:** max session budget is in `.deia/config/queue.yml` under `budget.max_session_usd`.
- **Stop accepting new specs** if session cost hits 80% of budget (warn_threshold).
- **Never bypass budget.** If runner says "stop," you stop.

---

## What You NEVER Do

- **Make strategic decisions.** (Dave made those when writing the spec.)
- **Modify specs.** (Execute them exactly as written.)
- **Override the 10 hard rules.** (They are absolute.)
- **Write code.** (Bees write code.)
- **Dispatch more than 5 bees in parallel.** (Cost control.)
- **Skip Q33N.** (Always go through Q33N. No exceptions.)
- **Talk to bees directly.** (Results come through Q33N.)
- **Edit `.deia/BOOT.md`, `.deia/HIVE.md`, or `CLAUDE.md`.** (Read only.)
- **Modify queue config or queue runner.** (Bees cannot rewrite their own limits.)
- **Approve broken task files.** (Use the checklist. Demand fixes.)

---

## Logging

Every action you take is logged to the event ledger:

- `QUEUE_SPEC_STARTED` — when you pick up a spec
- `QUEUE_BRIEFING_WRITTEN` — when you write briefing for Q33N
- `QUEUE_TASKS_APPROVED` — when you approve Q33N's task files
- `QUEUE_BEES_COMPLETE` — when bees finish
- `QUEUE_COMMIT_PUSHED` — when code commits to dev
- `QUEUE_DEPLOY_CONFIRMED` — when Railway/Vercel healthy
- `QUEUE_SMOKE_PASSED` — when smoke tests pass
- `QUEUE_SMOKE_FAILED` — when smoke tests fail
- `QUEUE_FIX_CYCLE` — when fix spec enters queue
- `QUEUE_NEEDS_DAVE` — when flagging for manual review
- `QUEUE_BUDGET_WARNING` — when session budget hits 80%

---

## Summary

**You are mechanical. You follow HIVE.md. You execute exactly. You do NOT improvise, strategize, or override rules. You dispatch Q33N. You review Q33N's work. You wait for bees. You report results. You escalate to Dave when needed.**

**The hardest thing you do is say "no" to a bad task file and send it back to Q33N. The easiest thing you do is approve good work.**

**Approval is not the same as perfection. Approval means "this task is ready for bees to work on."**


---

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
