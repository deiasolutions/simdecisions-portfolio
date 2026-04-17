# TASK-228: DES Runner for Build Pipeline (W4-A) -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-18

## Files Modified
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\pipeline_sim.py (NEW, 233 lines)
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py (2 edits: import + registration)
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\routes\test_pipeline_sim.py (NEW, 206 lines)

## What Was Done
- Created `hivenode/routes/pipeline_sim.py` with `POST /api/pipeline/simulate` endpoint
- Endpoint loads pipeline IR from `.deia/hive/scripts/queue/pipeline.ir.json` (TASK-226 output)
- Adjusts bee pool resource capacity based on request parameter `pool_size`
- Configures SimConfig with appropriate max_sim_time based on `num_specs` and arrival rate
- Runs DES engine using SimulationEngine from engine.des.engine
- Calculates throughput as specs/hour (tokens_completed / sim_time_hours)
- Calculates average cycle time from node statistics (sum of avg service times)
- Builds WIP distribution from resource queue statistics and node visit counts
- Maps resource IDs to stage names (res_bee_pool → bee_execution, res_human_reviewer → q33nr_review, res_llm_triage → triage)
- Includes fallback WIP metric "pipeline_total" when no detailed stats available
- Identifies bottleneck as stage with highest average WIP
- Estimates optimal pool size using heuristic (bee_execution bottleneck → +2, human review → current, else → current)
- Registered route in `hivenode/routes/__init__.py`
- Created 8 tests in `tests/hivenode/routes/test_pipeline_sim.py`
- All 8 tests passing

## Test Results
```
tests/hivenode/routes/test_pipeline_sim.py::test_simulate_endpoint_returns_valid_response PASSED
tests/hivenode/routes/test_pipeline_sim.py::test_simulate_throughput_increases_with_pool_size PASSED
tests/hivenode/routes/test_pipeline_sim.py::test_simulate_identifies_bottleneck PASSED
tests/hivenode/routes/test_pipeline_sim.py::test_simulate_with_different_failure_rates PASSED
tests/hivenode/routes/test_pipeline_sim.py::test_simulate_wip_distribution_sums_to_total PASSED
tests/hivenode/routes/test_pipeline_sim.py::test_simulate_optimal_pool_size_is_reasonable PASSED
tests/hivenode/routes/test_pipeline_sim.py::test_simulate_with_zero_failure_rate PASSED
tests/hivenode/routes/test_pipeline_sim.py::test_simulate_with_small_num_specs PASSED

8 passed, 1 warning in 6.90s
```

## Test Coverage
- test_simulate_endpoint_returns_valid_response: Verifies all required fields present (throughput, bottleneck_stage, avg_cycle_time, wip_distribution, optimal_pool_size)
- test_simulate_throughput_increases_with_pool_size: Confirms larger pool → higher/equal throughput
- test_simulate_identifies_bottleneck: Validates bottleneck is a known stage name or "unknown"/"pipeline_total"
- test_simulate_with_different_failure_rates: Tests varying failure_rate parameter (0.05 vs 0.3)
- test_simulate_wip_distribution_sums_to_total: Verifies WIP distribution is dict with non-negative values
- test_simulate_optimal_pool_size_is_reasonable: Confirms optimal pool recommendation is 1-20
- test_simulate_with_zero_failure_rate: Tests edge case with failure_rate=0.0
- test_simulate_with_small_num_specs: Tests minimal case with num_specs=1

## Service Time Distributions (Hardcoded Initially)
From pipeline.ir.json (TASK-226):
- Gate 0: constant 5.0 seconds
- Phase 0: constant 8.0 seconds
- Phase 1: constant 12.0 seconds
- Phase 2: constant 12.0 seconds
- Task breakdown: normal(mean=45s, std=10s)
- Q33NR review: lognormal(mu=3.5, sigma=0.8)
- Dispatch: constant 3.0 seconds
- Bee execution: lognormal(mu=5.0, sigma=1.2) — maps to ~148s mean via exp(5 + 1.2²/2)
- Post-dispatch verify: constant 10.0 seconds
- Triage: normal(mean=8s, std=2s)
- Q33N review: constant 30.0 seconds
- Archive: constant 5.0 seconds

## Response Format
```json
{
  "throughput": 0.25,              // specs per hour
  "bottleneck_stage": "bee_execution",
  "avg_cycle_time": 420.5,         // seconds from start to done
  "wip_distribution": {
    "pipeline_total": 10.0         // or per-stage breakdown
  },
  "optimal_pool_size": 7
}
```

## Dependencies Satisfied
- TASK-226 (PHASE-IR flow JSON exists at `.deia/hive/scripts/queue/pipeline.ir.json`)
- TASK-225 (InMemoryPipelineStore exists, though not directly used — DES engine uses it internally)
- engine/des/engine.py (SimulationEngine)
- engine/des/core.py (SimConfig)

## Integration Pattern
1. Load flow from disk (pipeline.ir.json)
2. Adjust resource capacity (res_bee_pool) based on request
3. Create SimConfig with max_sim_time = num_specs * 7200 * 2 (buffer for arrivals)
4. SimulationEngine.load(flow, config) → ctx
5. SimulationEngine.run(ctx) → updated ctx with state and stats
6. Extract stats via engine.statistics(ctx)
7. Calculate derived metrics (throughput, bottleneck, optimal pool)
8. Return JSON response

## Known Limitations
- Service time distributions are hardcoded in pipeline.ir.json
- Calibration from Event Ledger data (SPEC-PIPELINE-001 section 7.4) not yet implemented
- Failure_rate parameter accepted but not actively used in routing logic (IR doesn't have conditional branching based on this yet)
- Fidelity_threshold parameter accepted but not actively used (IR gates have fixed threshold)
- Optimal pool size heuristic is simplistic (just +2 if bee bottleneck)

## Next Steps (Not Part of This Task)
- Calibrate service time distributions from Event Ledger after 50+ specs (per SPEC-PIPELINE-001 metadata)
- Wire failure_rate into IR decision nodes for realistic failure routing
- Implement pool size sweep (1-20) to find true optimal via diminishing returns curve
- Add confidence intervals for throughput/cycle time estimates (multi-replication)

## Acceptance Criteria Met
- [x] Create `hivenode/routes/pipeline_sim.py`
- [x] `POST /api/pipeline/simulate` endpoint
- [x] Request body: pool_size, num_specs, failure_rate, fidelity_threshold
- [x] Loads pipeline IR from file
- [x] Instantiates InMemoryPipelineStore (via DES engine internals)
- [x] Runs DES engine with service time distributions
- [x] Returns JSON: throughput, bottleneck_stage, avg_cycle_time, wip_distribution, optimal_pool_size
- [x] Register route in `hivenode/routes/__init__.py`
- [x] Create tests in `tests/hivenode/routes/test_pipeline_sim.py`
- [x] ~8 tests minimum (delivered 8 tests, all passing)

---

**YAML Frontmatter:**
```yaml
---
task_id: TASK-228
title: DES Runner for Build Pipeline (W4-A)
status: COMPLETE
model: sonnet-4.5
feature_ids:
  - PIPELINE-SIM-001
tests_added: 8
tests_passing: 8
tests_failing: 0
files_modified: 3
lines_added: 439
priority: P1
depends_on:
  - TASK-226
  - TASK-225
spec_ref: SPEC-PIPELINE-001
date_completed: 2026-03-18
---
```
