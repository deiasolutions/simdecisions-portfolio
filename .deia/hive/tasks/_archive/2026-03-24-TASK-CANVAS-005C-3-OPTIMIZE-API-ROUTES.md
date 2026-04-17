# TASK-CANVAS-005C-3: Add Optimize API Routes + Tests

**Priority:** HIGH
**Model:** sonnet
**Role:** bee
**Date:** 2026-03-24
**Depends on:** CANVAS-005C-1 (sweep) and CANVAS-005C-2 (pareto) must be complete

## What

Add 3 new API routes for the optimize mode: parameter sweep, Pareto frontier computation, and AI suggestion analysis.

## Routes to Add

Add to `hivenode/routes/des_routes.py` or create new `hivenode/routes/optimize_routes.py`:

### 1. POST /api/des/sweep
Run a full factorial parameter sweep over a flow.
```python
Body: { "flow": Flow, "config": SweepConfig }
Returns: SweepResults
```
- Calls `engine.des.sweep.parameter_sweep(flow, config)`
- Validates: non-empty parameters, valid ranges
- Returns 400 on invalid config

### 2. POST /api/des/pareto
Compute Pareto frontier from sweep results.
```python
Body: { "points": list[dict], "objectives": list[str], "directions": dict[str, str] }
Returns: ParetoFrontier JSON
```
- Calls `engine.optimization.pareto` solver
- Validates: non-empty points, valid objective names
- Returns frontier with dominated/non-dominated annotations

### 3. POST /api/des/optimize
Run AI suggestion analysis on execution ledger.
```python
Body: { "flow": Flow, "ledger": list[LedgerEntry], "constraints": OptConstraints }
Returns: { "suggestions": list[Suggestion] }
```
- This route is a placeholder that returns mock suggestions for now (actual OptimizationEngine is frontend-only)
- Validates: non-empty flow and ledger

Register all routes in `hivenode/routes/__init__.py`.

## Tests (TDD)

Create tests in `tests/hivenode/routes/test_optimize_routes.py`:

1. `test_sweep_valid_config` — 200 with valid sweep config
2. `test_sweep_empty_params` — 400 with empty parameters
3. `test_sweep_returns_sweep_results` — verify SweepResults structure
4. `test_pareto_two_objectives` — 200 with valid points
5. `test_pareto_empty_points` — 400 with no points
6. `test_pareto_frontier_non_dominated` — verify non-dominated flagging
7. `test_optimize_suggestions` — 200 with valid flow + ledger
8. `test_optimize_empty_ledger` — 400 with empty ledger
9. `test_optimize_returns_suggestions` — verify suggestion structure
10. `test_sweep_sensitivity` — sensitivity analysis endpoint works
11. `test_pareto_single_objective` — edge case, degenerates to sorted list
12. `test_auth_local_bypass` — verify_jwt_or_local works for these routes

## Rules

- TDD: write tests first
- Use existing patterns from `hivenode/routes/des_routes.py`
- `verify_jwt_or_local()` for auth
- Pydantic schemas for request/response models
- Read `.deia/BOOT.md` first

## Files to Read First

1. `.deia/BOOT.md`
2. `hivenode/routes/des_routes.py` — pattern reference
3. `hivenode/routes/__init__.py` — route registration
4. `engine/des/sweep.py` — sweep module (should exist after 005C-1)
5. `engine/optimization/` — pareto module (should exist after 005C-2)
