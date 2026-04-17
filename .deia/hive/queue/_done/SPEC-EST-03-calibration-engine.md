# SPEC: Estimation Calibration — Calibration Engine + CLI Reports

## Priority
P1

## Depends On
EST-02

## Objective
Add calibration logic (compute factors, apply to estimates) and CLI report commands (calibration, compare, budget, trend) to `_tools/estimates.py`.

## Context
Phase 3 of the estimation calibration ledger. After EST-02 imported estimates and actuals, this task computes calibration factors (mean of actual/estimate per task type), applies them to new estimates, and provides CLI reports.

Design doc: `.deia/hive/responses/20260406-BRIEFING-ESTIMATION-CALIBRATION-LEDGER-RESPONSE.md`
Task file: `.deia/hive/tasks/2026-04-06-TASK-EST-03-calibration-engine.md`

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/inventory/store.py` — inv_estimates + inv_calibration schema
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/_tools/estimates.py` — CLI (EST-02 created this)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/tasks/2026-04-06-TASK-EST-03-calibration-engine.md` — full task spec with algorithm code and output formats

## Acceptance Criteria
- [ ] `update_calibration(task_type)` computes mean(actual/estimate) per type, upserts inv_calibration
- [ ] `apply_calibration(task_type, est_hours, est_cost, est_carbon)` returns calibrated values
- [ ] Calibration factors update automatically after `import-actuals` and `actual` commands
- [ ] `estimates.py calibration` shows per-type factors table (clock, cost, carbon, samples)
- [ ] `estimates.py compare` shows per-task comparison (est -> cal -> actual), delta % for all 3 Cs
- [ ] `estimates.py budget --remaining` projects remaining work with calibrated estimates
- [ ] `estimates.py trend` shows accuracy improvement over time (weekly grouping)
- [ ] Filters work: `--type build`, `--model sonnet`, `--phase "Phase 2"` on compare/budget/trend
- [ ] Division by zero handled gracefully (est_hours=0 -> skip, log warning)
- [ ] 11+ tests covering calibration math, budget projection, trend, CLI output
- [ ] All tests pass: `python -m pytest tests/hivenode/inventory/test_estimates_calibration.py -v`

## Smoke Test
- [ ] `python _tools/estimates.py calibration` shows factor table
- [ ] `python _tools/estimates.py compare` shows per-task comparison
- [ ] `python _tools/estimates.py compare --type build` filters correctly
- [ ] `python _tools/estimates.py budget --remaining` shows calibrated projection
- [ ] `python _tools/estimates.py trend` shows weekly accuracy trend

## Model Assignment
sonnet

## Constraints
- No file over 500 lines (split if needed)
- No stubs — all functions fully implemented
- SQLAlchemy Core for queries (no ORM)
- Format output with fixed-width columns
- Round percentages to 0 decimal places, factors to 3 decimal places
- TDD — tests first
- Response file: `.deia/hive/responses/20260406-TASK-EST-03-RESPONSE.md`
