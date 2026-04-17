# SPEC-BENCH-009: PRISM-bench Adapter Wiring -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-13

## Files Modified

- simdecisions/benchmark/adapters/prism_bench.py
- tests/simdecisions/benchmark/test_prism_bench_adapter.py

## What Was Done

### Updated prism_bench.py (real DES execution)

1. **load_tasks()** - Changed workflow directory from `test_workflows/` to `prism_bench_tasks/`, now loads all 20 PRISM-bench tasks
2. **run_baseline()** - Replaced placeholder with real DES execution:
   - Creates SimulationEngine instance
   - Loads workflow with SimConfig(seed=42, max_sim_time=1000.0)
   - Runs simulation and measures wall clock time
   - Extracts DES statistics from StatisticsCollector
   - Computes CARBON using carbon.compute_carbon()
   - Returns BaselineResult with complete currencies and metadata
3. **run_simdecisions()** - Delegates to run_baseline() (real DEF→SIM→BRA→COMP loop deferred to later wave)
   - Converts BaselineResult to SimResult with ir_used field
4. **evaluate()** - Replaced placeholder with PRISMBenchHarness integration:
   - Builds result dict with currencies, recovery, metadata
   - Calls PRISMBenchHarness.evaluate() with workflow and result
   - Returns EvalResult with score, partial_credit, and category metrics

### Updated test_prism_bench_adapter.py (integration tests)

Replaced Wave A placeholder tests with Wave B integration tests:

1. **test_load_tasks_from_prism_bench_tasks()** - Verifies 20 tasks loaded
2. **test_load_tasks_has_correct_ids()** - Verifies task IDs match workflow files
3. **test_baseline_execution()** - Verifies baseline track execution with DES stats
4. **test_simdecisions_execution()** - Verifies simdecisions track execution
5. **test_evaluate_returns_eval_result()** - Verifies PRISMBenchHarness integration
6. **test_des_statistics_captured()** - Verifies DES stats in result.metadata
7. **test_all_tasks_load_and_execute()** - Smoke test for all 20 tasks
8. **test_result_currencies_complete()** - Verifies all 6 currency fields present

All 11 tests pass.

## Tests Written

- 11 integration tests in test_prism_bench_adapter.py
- Tests verify: task loading, DES execution, statistics capture, evaluation, currency fields

## Tests Run

```
pytest tests/simdecisions/benchmark/test_prism_bench_adapter.py -v
============================= 11 passed in 0.89s ==============================
```

All smoke tests pass:
- ✓ Load 20 tasks
- ✓ All integration tests pass
- ✓ Baseline execution test passes
- ✓ SimDecisions execution test passes

## Acceptance Criteria

- [x] Method `PRISMBenchAdapter.load_tasks()` loads from `simdecisions/benchmark/prism_bench_tasks/` (not test_workflows)
- [x] Method `PRISMBenchAdapter.load_tasks()` returns 20 BenchmarkTask objects (one per JSON file in prism_bench_tasks/)
- [x] Method `PRISMBenchAdapter.run_baseline(task, model)` executes workflow using SimulationEngine in sim mode with no production executors
- [x] Method `PRISMBenchAdapter.run_simdecisions(task, ir, model)` executes workflow using SimulationEngine (placeholder for now, delegates to baseline)
- [x] Both run methods capture wall time (CLOCK)
- [x] Both run methods compute CARBON using carbon.compute_carbon() from tokens_in/tokens_out
- [x] Method `PRISMBenchAdapter.evaluate(task, output)` calls PRISMBenchHarness.evaluate() with workflow metadata and result dict
- [x] Adapter extracts DES statistics from SimulationEngine context after run
- [x] BaselineResult and SimResult objects include all fields from types.py: task_id, track, output, currencies, started_at, completed_at, metadata
- [x] Integration test `tests/simdecisions/benchmark/test_prism_bench_adapter.py` runs one task through both tracks and verifies result format
- [x] Integration test verifies result.currencies has all 6 fields: clock_seconds, coin_usd, carbon_kg, tokens_in, tokens_out, model_calls
- [x] Integration test verifies DES statistics are captured in result.metadata
- [x] Test loads all 20 tasks and verifies each has task_id matching workflow id
- [x] Test verifies evaluate() returns EvalResult with score, partial_credit, score_metadata

## Notes

- COIN and model_calls are 0 in sim mode (no Event Ledger integration yet, deferred to later wave)
- run_simdecisions() uses same execution path as run_baseline() for Wave B (real DEF→SIM→BRA→COMP loop will be implemented in later wave as specified in spec)
- Join-fork workflows may not complete within max_sim_time if join is waiting for all branches - this is expected DES behavior
- All constraints followed: no file over 500 lines, no stubs, TDD with tests first

## Implementation Details

The adapter now:
1. Loads 20 real PRISM-bench tasks from prism_bench_tasks/
2. Executes workflows through DES engine with statistics collection
3. Captures wall clock time, DES stats, and computes CARBON
4. Evaluates results using category-specific harness (multi-step, recovery, multi-agent, branch-comparison, governance)
5. Returns complete BenchmarkResult objects matching the results schema

Wave B complete. Ready for Wave C (SWE-bench integration).
