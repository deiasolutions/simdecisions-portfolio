# SPEC-METRICS-001: Factory Throughput Audit — Last 24 Hours

**Priority:** P1
**Complexity:** Sonnet
**Estimate:** 1 hour
**Dependencies:** None

---

## Objective

Research and report only. No code changes.

Produce real throughput data to calibrate bee-time estimates. Right now there is no reliable way to plan overnight runs because we don't know what the factory actually produces per hour. This audit gives us that baseline.

---

## Queries to Run

### 1. Task Volume

From the build monitor, ledger, and response files — how many tasks completed in the last 24 hours? How many are currently in-flight? How many failed or stalled?

Report:
- Total tasks dispatched
- Total tasks completed
- Total tasks failed / stalled / abandoned
- Completion rate (%)

### 2. Wall-Clock Timing

For each completed task in the last 24 hours:
- Task ID
- Model used (Haiku / Sonnet / Opus)
- Wall-clock start time
- Wall-clock end time
- Duration in minutes
- Input tokens
- Output tokens
- Cost USD

If exact timestamps aren't in the ledger, approximate from response file timestamps and heartbeat records.

Data sources:
- `curl -s http://127.0.0.1:8420/build/status` — active/completed/failed with first_seen, last_seen, cost_usd, model, input_tokens, output_tokens
- `.deia/hive/responses/` — response file timestamps
- `.deia/hive/queue/_done/` — completed spec files

### 3. Concurrency

What was peak concurrent bee count over the last 24 hours? What was average concurrency? Were there periods where the factory was idle — no bees running? How long were those idle windows?

Look at:
- `/build/status` task intervals (first_seen to last_seen)
- Heartbeat timestamps to reconstruct concurrency timeline
- Queue drain times — how long between a task entering the queue and a bee claiming it?

### 4. Throughput Peaks

Find the window in the last 24 hours where the factory was running hottest. What was the tasks-per-hour rate during that window? How many bees were concurrent? What models were running?

This is the "factory humming" baseline — the number we plan overnight runs against.

### 5. Human-Hours Equivalent

For each completed task, estimate the equivalent human developer time. Use this heuristic:

- A task that produces < 50 lines of code = 30 min human time
- 50-200 lines = 1-2 hours
- 200-500 lines = 3-5 hours
- A spec or research task = 1-2 hours
- A multi-file integration task = 4-8 hours

Sum across all completed tasks. Report:
- Total estimated human-hours produced in last 24 hours
- Human-hours per actual hour of factory runtime
- Human-hours per dollar spent

### 6. Idle Time Analysis

How much of the last 24 hours was the factory idle vs active? What caused idle periods — queue empty, hivenode down, waiting on human input, rate limits?

Report idle % and the primary causes.

### 7. Cost Summary

Total spend in the last 24 hours across all models. Break down by model. Cost per completed task average. Cost per estimated human-hour produced.

---

## Deliverable

A single response file (`.deia/hive/responses/YYYYMMDD-SPEC-METRICS-001-RESPONSE.md`) with 8 sections:

1. **Factory scorecard** — tasks, completion rate, peak concurrency, total cost, total human-hours equivalent
2. **Throughput table** — one row per completed task with timing, model, tokens, cost, lines produced, estimated human-hours
3. **Peak window** — the best hour of the last 24, annotated
4. **Idle analysis** — where time was lost
5. **Calibration numbers** — the three numbers needed for planning: tasks per hour at peak, human-hours per factory-hour, cost per human-hour
6. **Overnight run recommendation** — how many tasks, which models, at what concurrency, to fill 10 hours of factory runtime
7. **Instrumentation gaps** — what's missing that would make this report auto-generate on demand (becomes TASK-METRICS-002)
8. **Raw data appendix** — full task list with all fields

---

## Files to Read First

- `hivenode/routes/build_monitor.py`
- `.deia/config/queue.yml`

## Acceptance Criteria

- [ ] All 8 sections present in response file
- [ ] Throughput table has one row per completed task (last 24h)
- [ ] Concurrency chart reconstructed from task intervals
- [ ] Peak window identified with tasks-per-hour rate
- [ ] Human-hours estimates use the specified heuristic
- [ ] Calibration numbers clearly stated for planning use
- [ ] Overnight run recommendation is concrete (task count, models, concurrency, duration)
- [ ] Instrumentation gap list identifies what's missing for auto-generation

## Smoke Test

- [ ] Response file exists in `.deia/hive/responses/`
- [ ] Factory scorecard section has numeric values (not placeholders)
- [ ] Calibration numbers section has exactly 3 numbers

## Model Assignment

sonnet

## Constraints

- NO code changes — research and report only
- All data from build monitor API and local files
- Response file follows standard 8-section format
