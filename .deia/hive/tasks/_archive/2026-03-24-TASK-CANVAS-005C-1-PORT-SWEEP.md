# TASK-CANVAS-005C-1: Port Sweep Module + Tests

**Priority:** HIGH
**Model:** sonnet
**Role:** bee
**Date:** 2026-03-24

## What

Port the parameter sweep module from old platform to shiftcenter engine.

## Source

`platform/efemera/src/efemera/des/sweep.py` (543 lines)

## Target

`engine/des/sweep.py` (modularize if needed — 500 line limit per file)

## What to Port

- `SweepParameter` dataclass: name, path, values (list of floats)
- `SweepConfig` dataclass: parameters list, replications per point, metric names
- `SweepPoint` dataclass: parameter values dict, metrics dict (mean, ci_low, ci_high)
- `SweepResults` dataclass: config, points list, elapsed time
- `parameter_sweep(flow, config)` — full factorial sweep over parameter space
- `sensitivity_analysis(flow, base_config)` — OAT (one-at-a-time) elasticity + correlation
- Metric extraction helpers: throughput, cycle_time, completions, utilization

## Dependencies

- `engine/des/` directory (may need to create it)
- The DES engine itself (`engine/des/engine.py` or similar) — if it doesn't exist yet, mock the simulation runner interface

## Tests (TDD — write first)

Create `tests/engine/des/test_sweep.py`:

1. `test_sweep_parameter_creation` — create SweepParameter with name/values
2. `test_sweep_config_full_factorial_count` — 2 params × 3 values = 6 points
3. `test_sweep_config_single_param` — 1 param × 5 values = 5 points
4. `test_parameter_sweep_returns_results` — mock DES engine, verify SweepResults structure
5. `test_sweep_point_has_metrics` — each point has mean/ci_low/ci_high for each metric
6. `test_sweep_point_parameter_values` — verify parameter values in each point
7. `test_sensitivity_analysis_elasticity` — verify elasticity calculation
8. `test_sensitivity_analysis_correlation` — verify correlation computation
9. `test_empty_parameters_raises` — empty param list raises ValueError
10. `test_single_value_parameter` — param with 1 value produces 1 point
11. `test_metric_extraction` — verify throughput/cycle_time/completions extracted
12. `test_sweep_elapsed_time` — verify elapsed time recorded
13. `test_large_parameter_space` — 3 params × 4 values = 64 points (verify count)
14. `test_replications` — 3 replications per point → CI values narrower than with 1
15. `test_sweep_results_serializable` — results can be JSON serialized

## Rules

- All files under 500 lines
- No stubs — every function fully implemented
- TDD: write tests first
- If DES engine doesn't exist yet, create a simple mock interface that sweep.py calls
- Read `.deia/BOOT.md` first

## Files to Read First

1. `.deia/BOOT.md`
2. `platform/efemera/src/efemera/des/sweep.py` — the source to port
3. `engine/` — check what exists already
4. `hivenode/routes/des_routes.py` — existing DES API for reference
