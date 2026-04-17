# Fix Pipeline Simulation Tests (6 failing)

## Priority
P2

## Model Assignment
haiku

## Objective
Fix 6 failing pipeline simulation tests in `tests/hivenode/test_pipeline_sim.py`.

## What's Broken
- `test_simulate_detects_pool_starvation`
- `test_simulate_optimal_pool_size_is_reasonable`
- `test_simulate_with_zero_failure_rate`
- `test_simulate_with_small_num_specs`
- `test_simulate_handles_fix_cycles`
- `test_simulate_budget_exhaustion`

Reference: `.deia/hive/responses/20260318-FULL-TEST-SWEEP-REPORT.md` section "Pipeline simulation (6)"

## Files to Read First
- `tests/hivenode/test_pipeline_sim.py`
- `hivenode/routes/pipeline_sim.py`

## What To Do
1. Read the test file and route file
2. Run the tests to see exact errors
3. Fix the tests or implementation
4. Confirm all 6 pass

## Response
Write response to: `.deia/hive/responses/20260318-FIX-PIPELINE-SIM-TESTS.md`
