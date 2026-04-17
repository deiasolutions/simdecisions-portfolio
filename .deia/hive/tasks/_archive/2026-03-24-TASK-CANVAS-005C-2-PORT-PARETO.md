# TASK-CANVAS-005C-2: Port Pareto Module + Tests

**Priority:** HIGH
**Model:** sonnet
**Role:** bee
**Date:** 2026-03-24

## What

Port the Pareto frontier solver from old platform to shiftcenter engine. The source is 967 lines — **must modularize** into 3-4 files (500 line limit per file).

## Source

`platform/efemera/src/efemera/optimization/pareto.py` (967 lines)

## Target

Split into multiple files under `engine/optimization/`:
- `engine/optimization/__init__.py` — public exports
- `engine/optimization/core.py` — ParetoSolution, ParetoFrontier, DominanceChecker
- `engine/optimization/solver.py` — ParetoSolver, weighted-sum method
- `engine/optimization/analyzer.py` — spread, hypervolume, spacing, trade_off_ratio, knee point

## What to Port

### core.py:
- `ParetoSolution` dataclass: objectives dict, parameters dict, is_dominated bool
- `ParetoFrontier` dataclass: solutions list, non_dominated list
- `DominanceChecker` class: check if solution A dominates B across all objectives

### solver.py:
- `ParetoSolver` class: solve(solutions, objectives, minimize/maximize per objective)
- Weighted-sum method for multi-objective optimization
- `select_by_weights(weights)` — select solution closest to weighted ideal
- `select_where(constraints)` — filter by constraints
- `get_knee_point()` — find maximum curvature point on frontier

### analyzer.py:
- `spread()` — measure diversity of frontier
- `hypervolume()` — compute hypervolume indicator
- `spacing()` — measure evenness of distribution
- `trade_off_ratio(obj_a, obj_b)` — marginal rate of substitution
- `to_table_text()` — text table representation
- `to_trade_off_text()` — trade-off analysis text

## Tests (TDD — write first)

Create `tests/engine/optimization/test_pareto.py`:

1. `test_solution_creation` — create ParetoSolution with objectives
2. `test_dominance_a_dominates_b` — A better in all objectives → A dominates B
3. `test_dominance_neither` — A better in some, B in others → neither dominates
4. `test_dominance_equal` — same objectives → neither dominates
5. `test_solver_two_objectives` — 5 solutions, 2 objectives → correct frontier
6. `test_solver_three_objectives` — 5 solutions, 3 objectives → correct frontier
7. `test_non_dominated_count` — verify only non-dominated in frontier
8. `test_select_by_weights` — weighted selection returns expected solution
9. `test_select_where` — constraint filter returns matching solutions
10. `test_knee_point` — knee point on 3-point frontier
11. `test_spread` — spread metric for evenly vs unevenly distributed
12. `test_hypervolume` — hypervolume for known 2D case
13. `test_spacing` — spacing for perfectly even distribution
14. `test_trade_off_ratio` — ratio between two objectives
15. `test_single_solution` — frontier with 1 solution (edge case)
16. `test_all_dominated` — all solutions dominated except 1
17. `test_minimize_vs_maximize` — correct handling of direction
18. `test_frontier_serializable` — can JSON serialize results
19. `test_to_table_text` — generates valid text table
20. `test_empty_solutions_raises` — empty input raises ValueError

## Rules

- **Critical:** Split into 3-4 files. No file over 500 lines.
- No stubs — every function fully implemented
- TDD: write tests first
- Read `.deia/BOOT.md` first

## Files to Read First

1. `.deia/BOOT.md`
2. `platform/efemera/src/efemera/optimization/pareto.py` — the source to port
3. `engine/` — check what exists already
