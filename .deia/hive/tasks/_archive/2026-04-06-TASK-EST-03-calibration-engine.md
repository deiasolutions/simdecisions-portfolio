# TASK-EST-03: Calibration Engine + CLI Commands

## Objective
Add calibration logic (compute factors, apply to estimates) and CLI report commands (calibration, compare, budget, trend) to `_tools/estimates.py`.

## Context
This is Phase 3 of the estimation calibration ledger system. After EST-02 imported estimates and actuals, this task computes calibration factors (mean of actual/estimate per task type), applies them to new estimates, and provides CLI reports to answer:
- What are the current calibration factors? (how much do we underestimate?)
- How do original vs calibrated vs actual compare per task?
- What is the budget projection for remaining work?
- Is estimation accuracy improving over time?

**Design doc:** `.deia/hive/responses/20260406-BRIEFING-ESTIMATION-CALIBRATION-LEDGER-RESPONSE.md`

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\inventory\store.py`
  Schema definitions for inv_estimates and inv_calibration (EST-01 created these).
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\estimates.py`
  CLI script (EST-02 created this). You'll add 4 new commands here.
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260406-BRIEFING-ESTIMATION-CALIBRATION-LEDGER-RESPONSE.md`
  Full design doc with calibration algorithm, CLI output formats, report specs.

## Deliverables
- [ ] `update_calibration(task_type)` function:
  - Query all completed tasks of this type (actual_hours IS NOT NULL)
  - Compute mean ratio: clock_factor = mean(actual_hours / est_hours)
  - Compute mean ratio: cost_factor = mean(actual_cost_usd / est_cost_usd)
  - Compute mean ratio: carbon_factor = mean(actual_carbon_g / est_carbon_g)
  - Upsert into inv_calibration (delete + insert, or use ON CONFLICT UPDATE for PostgreSQL)
  - Update sample_count, last_updated
- [ ] `apply_calibration(task_type, est_hours, est_cost, est_carbon)` function:
  - Look up calibration factor for this task type
  - If not found, return original estimates (no calibration data yet)
  - Return (est_hours × clock_factor, est_cost × cost_factor, est_carbon × carbon_factor)
- [ ] Automatic calibration update: call `update_calibration(task_type)` after `import-actuals` and `actual` commands
- [ ] `estimates.py calibration` command:
  - Query inv_calibration, show table: Type | Clock | Cost | Carbon | Samples | Last Updated
  - Format factors as "1.200x" (3 decimal places)
  - Include interpretation notes (e.g., "build tasks take 20% longer than estimated")
- [ ] `estimates.py compare` command:
  - Query inv_estimates, show table: Task | Type | Est→Cal→Act (Hours) | Est→Cal→Act (Cost) | Est→Cal→Act (Carbon) | Δ%
  - Format: "8.0 → 9.6 → 11.2 (+40%)"
  - Delta % = (actual - original_estimate) / original_estimate × 100
  - Mark tasks within 10% of estimate with ✓
  - Filters: `--type`, `--model`, `--phase`
- [ ] `estimates.py budget --remaining` command:
  - Query inv_estimates WHERE actual_hours IS NULL (remaining tasks)
  - Sum original estimates (total_est_hours, total_est_cost, total_est_carbon)
  - Sum calibrated estimates (total_cal_hours, total_cal_cost, total_cal_carbon)
  - Show delta: "(+24%)"
  - Group by type: show per-type subtotals
  - Estimate completion date (assuming 10 parallel bees, 8h/day)
- [ ] `estimates.py trend` command:
  - Query inv_estimates WHERE actual_hours IS NOT NULL, group by week (completed_at)
  - Compute avg delta % per week: mean((actual - est) / est × 100)
  - Show table: Week | Completed | Avg Δ Clock | Avg Δ Cost | Avg Δ Carbon
  - Show trend: "✓ Improving" if delta decreasing, "⚠ Degrading" if increasing
  - Show recent tasks (last 10): Task | Completed | Clock Δ | Cost Δ | Carbon Δ

## Algorithm Details

### Calibration Factor Computation (rolling average)

```python
def update_calibration(task_type: str):
    # Get all completed tasks of this type
    rows = db.execute(
        select(inv_estimates).where(
            and_(
                inv_estimates.c.task_type == task_type,
                inv_estimates.c.actual_hours.isnot(None),
                inv_estimates.c.actual_cost_usd.isnot(None),
                inv_estimates.c.actual_carbon_g.isnot(None),
            )
        )
    ).fetchall()

    if not rows:
        return  # No data yet

    # Compute mean ratio (actual / estimate) for each dimension
    clock_ratios = [r.actual_hours / r.est_hours for r in rows if r.est_hours > 0]
    cost_ratios = [r.actual_cost_usd / r.est_cost_usd for r in rows if r.est_cost_usd > 0]
    carbon_ratios = [r.actual_carbon_g / r.est_carbon_g for r in rows if r.est_carbon_g > 0]

    clock_factor = sum(clock_ratios) / len(clock_ratios) if clock_ratios else 1.0
    cost_factor = sum(cost_ratios) / len(cost_ratios) if cost_ratios else 1.0
    carbon_factor = sum(carbon_ratios) / len(carbon_ratios) if carbon_ratios else 1.0

    # Upsert into inv_calibration
    db.execute(
        inv_calibration.delete().where(inv_calibration.c.task_type == task_type)
    )
    db.execute(inv_calibration.insert().values(
        task_type=task_type,
        clock_factor=round(clock_factor, 3),
        cost_factor=round(cost_factor, 3),
        carbon_factor=round(carbon_factor, 3),
        sample_count=len(rows),
        last_updated=_now(),
        created_at=_now(),
    ))
```

### Apply Calibration (to new estimates)

```python
def apply_calibration(task_type, est_hours, est_cost, est_carbon):
    # Look up calibration factor for this task type
    row = db.execute(
        select(inv_calibration).where(inv_calibration.c.task_type == task_type)
    ).fetchone()

    if not row:
        # No calibration data yet — use original estimates
        return est_hours, est_cost, est_carbon

    calibrated_hours = est_hours * row.clock_factor
    calibrated_cost = est_cost * row.cost_factor
    calibrated_carbon = est_carbon * row.carbon_factor

    return calibrated_hours, calibrated_cost, calibrated_carbon
```

### Budget Projection (remaining work)

```python
# Query remaining tasks
remaining = db.execute(
    select(inv_estimates).where(inv_estimates.c.actual_hours.is_(None))
).fetchall()

# Sum original estimates
total_est_hours = sum(r.est_hours for r in remaining)
total_est_cost = sum(r.est_cost_usd for r in remaining)
total_est_carbon = sum(r.est_carbon_g for r in remaining)

# Sum calibrated estimates
total_cal_hours = sum(r.calibrated_hours or r.est_hours for r in remaining)
total_cal_cost = sum(r.calibrated_cost_usd or r.est_cost_usd for r in remaining)
total_cal_carbon = sum(r.calibrated_carbon_g or r.est_carbon_g for r in remaining)

# Delta
delta_pct = ((total_cal_hours - total_est_hours) / total_est_hours * 100) if total_est_hours > 0 else 0
```

## CLI Output Formats (from design doc)

### `estimates.py calibration` output:
```
Calibration Factors (Mobile Workdesk Build)

Type       Clock    Cost     Carbon   Samples  Last Updated
─────────  ───────  ───────  ───────  ───────  ────────────
spec       0.920x   1.050x   1.050x   8        2026-04-06
test       1.120x   1.080x   1.080x   8        2026-04-06
build      1.350x   1.200x   1.200x   12       2026-04-06
verify     0.850x   0.920x   0.920x   3        2026-04-06
css        1.100x   N/A      N/A      5        2026-04-06

Interpretation:
- spec tasks finish 8% faster than estimated (good!)
- build tasks take 35% longer than estimated (recalibrate)
- verify tasks finish 15% faster (good!)
```

### `estimates.py compare` output:
```
Task       Type   Est→Cal→Act (Hours)     Est→Cal→Act (Cost)      Δ%
─────────  ─────  ──────────────────────  ──────────────────────  ──────
MW-S01     spec   3.0 → 2.8 → 2.5 ✓       $2.40 → $2.52 → $2.10   -17%
MW-001     build  8.0 → 10.8 → 11.2       $24.00 → $28.80 → $30.5 +40%
MW-031     css    6.0 → 6.6 → 7.1         N/A                     +18%
```

### `estimates.py budget --remaining` output:
```
Mobile Workdesk Build Budget (Remaining Tasks: 54)

Total Remaining: 54 tasks

Original Estimates:
- Clock:  180 hours
- Cost:   $540 USD
- Carbon: 75,600g CO2e (75.6 kg)

Calibrated Estimates (with learned factors):
- Clock:  224 hours (+24%)
- Cost:   $648 USD (+20%)
- Carbon: 90,720g CO2e (+20%)

By Type:
Type       Tasks  Calibrated Hours  Calibrated Cost  Calibrated Carbon
─────────  ─────  ────────────────  ───────────────  ─────────────────
spec       5      12.5h             $12.60           1,764g
test       5      17.5h             $15.12           2,117g
build      30     180.0h            $540.00          75,600g
verify     5      8.5h              $27.60           3,864g
css        9      5.5h              N/A              N/A

Estimated Completion: 2026-04-12 (assuming 10 parallel bees)
```

### `estimates.py trend` output:
```
Estimation Accuracy Trend (by completion date)

Week      Completed  Avg Δ Clock  Avg Δ Cost  Avg Δ Carbon
────────  ─────────  ───────────  ──────────  ────────────
2026-W14  8          +28%         +32%        +32%
2026-W15  12         +18%         +22%        +22%
2026-W16  20         +12%         +15%        +15%

Trend: ✓ Improving (delta decreasing over time)
```

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass (`python -m pytest tests/hivenode/inventory/test_estimates_calibration.py -v`)
- [ ] Edge cases:
  - No completed tasks yet (calibration returns 1.0x factors)
  - Division by zero (est_hours=0, handle gracefully)
  - CSS tasks have no cost/carbon actuals (show "N/A")
  - Filters with no matching tasks (empty result, not error)
  - Week grouping at year boundary (2026-W53 → 2027-W01)

## Test Coverage (minimum 10 tests)
Create `tests/hivenode/inventory/test_estimates_calibration.py` with:
1. `test_update_calibration_computes_mean_ratio()` — 5 tasks, clock_factor = mean(actual/est)
2. `test_update_calibration_handles_zero_est()` — est_hours=0, skip this task (don't divide by zero)
3. `test_apply_calibration_returns_calibrated_values()` — verify multiplication works
4. `test_apply_calibration_returns_original_if_no_data()` — no calibration row, return original
5. `test_calibration_updates_after_import_actuals()` — import actuals, verify calibration updated
6. `test_cli_calibration_shows_factors()` — run CLI, verify output format
7. `test_cli_compare_shows_per_task()` — run CLI, verify table format
8. `test_cli_budget_shows_remaining()` — run CLI, verify totals and delta %
9. `test_cli_trend_groups_by_week()` — run CLI, verify week grouping
10. `test_filters_work_on_compare()` — `--type build` filters correctly
11. `test_budget_handles_no_remaining()` — all tasks complete, budget = 0

## Constraints
- No file over 500 lines (split into `estimates.py` + `estimates_db.py` if needed)
- CSS: var(--sd-*) only (N/A for this task)
- No stubs (all functions fully implemented)
- Use SQLAlchemy Core for queries (no ORM)
- Format output with fixed-width columns (use f-strings or tabulate library)
- Handle missing calibration_factor gracefully (fall back to est_*)
- Round percentages to 0 decimal places (+24%, not +23.789%)
- Round factors to 3 decimal places (1.200x, not 1.2x or 1.20000x)

## Acceptance Criteria
- [ ] `estimates.py calibration` shows table with per-type factors (clock, cost, carbon), sample counts
- [ ] `estimates.py compare` shows per-task comparison (est → cal → actual), delta % for all 3 Cs
- [ ] `estimates.py budget --remaining` projects remaining work with calibrated estimates
- [ ] `estimates.py trend` shows accuracy improvement over time (weekly grouping)
- [ ] Calibration factors update automatically after recording actuals (import-actuals, actual commands)
- [ ] Filters work: `--type build`, `--model sonnet`, `--phase "Phase 2"` on compare/budget/trend
- [ ] Division by zero handled gracefully (est_hours=0 → skip task in calibration, log warning)
- [ ] CSS tasks show "N/A" for cost/carbon (front-end only, no API calls)
- [ ] Tests: 11+ tests covering calibration math, budget projection, trend computation, CLI output
- [ ] No file over 500 lines (split if needed)
- [ ] All tests pass: `python -m pytest tests/hivenode/inventory/test_estimates_calibration.py -v`

## Smoke Test
```bash
# Show calibration factors
python _tools/estimates.py calibration

# Per-task comparison
python _tools/estimates.py compare

# Per-task comparison (filtered)
python _tools/estimates.py compare --type build --model sonnet

# Budget projection (remaining work)
python _tools/estimates.py budget --remaining

# Accuracy trend
python _tools/estimates.py trend
```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260406-TASK-EST-03-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test output summary
6. **Acceptance Criteria** — copy from above, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
