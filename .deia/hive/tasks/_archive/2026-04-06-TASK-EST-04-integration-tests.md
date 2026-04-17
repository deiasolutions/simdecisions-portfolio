# TASK-EST-04: Integration Tests + Documentation

## Objective
Write end-to-end integration tests covering full estimation workflows (import → calibrate → budget), add CLI help text, and document the estimation calibration system in README.

## Context
This is Phase 4 (final) of the estimation calibration ledger system. After EST-01/02/03 built the schema, data import, and calibration engine, this task validates the full system with integration tests and ensures it's documented for human users.

**Design doc:** `.deia/hive/responses/20260406-BRIEFING-ESTIMATION-CALIBRATION-LEDGER-RESPONSE.md`

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\estimates.py`
  CLI script (EST-02/03 created this). You'll add --help text and verify all commands work.
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\README.md`
  Project README. You'll add a new "Estimation Calibration" section.
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260406-BRIEFING-ESTIMATION-CALIBRATION-LEDGER-RESPONSE.md`
  Full design doc with workflow examples, CLI output formats.

## Deliverables
- [ ] Integration test: import scheduler → import actuals → calibration updates → budget projection changes (end-to-end)
- [ ] Integration test: import response files → compare actuals vs computed-from-tokens (validation)
- [ ] Integration test: record 10 manual tasks → compute calibration → apply to 10 new tasks → verify accuracy
- [ ] Integration test: trend report groups by week correctly (test with 3 weeks of data)
- [ ] Integration test: filters work on compare/budget/trend (--type, --model, --phase)
- [ ] Integration test: handle edge cases (no data, division by zero, missing files)
- [ ] CLI help text (`--help`) for all commands: record, actual, import-scheduler, import-actuals, import-responses, calibration, compare, budget, trend
- [ ] README section: "Estimation Calibration" (200-300 words, how to use, what it does, why it matters)
- [ ] Example workflow: bootstrap new build, import estimates, track actuals, project budget
- [ ] Smoke test: run all CLI commands with test data, verify no crashes

## Integration Test Scenarios

### Test 1: End-to-End Workflow
```python
def test_full_estimation_workflow():
    """
    Simulate a full estimation lifecycle:
    1. Import estimates from scheduler (10 tasks)
    2. No calibration data yet (factors = 1.0x)
    3. Simulate 5 tasks completing (import actuals)
    4. Calibration factors update (e.g., build → 1.2x)
    5. Budget projection changes (remaining 5 tasks use 1.2x)
    6. Verify budget increased by ~20%
    """
```

### Test 2: Response File Validation
```python
def test_response_file_vs_build_monitor():
    """
    Compare actuals from two sources:
    1. Import actuals from build monitor (token-based)
    2. Import actuals from response files (Clock/Cost/Carbon sections)
    3. Verify they're within 10% tolerance (close enough)
    4. Verify response file data overrides build monitor data
    """
```

### Test 3: Manual Calibration Workflow
```python
def test_manual_task_calibration():
    """
    Record 10 tasks manually, compute calibration:
    1. Record 10 spec tasks (est_hours=3.0 each)
    2. Record actuals for all 10 (actual_hours=2.7 each)
    3. Compute calibration (clock_factor = 2.7 / 3.0 = 0.9)
    4. Record 10 new spec tasks (est_hours=3.0 each)
    5. Verify calibrated_hours = 2.7 for all new tasks
    """
```

### Test 4: Trend Analysis
```python
def test_trend_groups_by_week():
    """
    Create tasks completed over 3 weeks, verify trend report:
    1. Week 1: 5 tasks, avg delta +30%
    2. Week 2: 5 tasks, avg delta +20%
    3. Week 3: 5 tasks, avg delta +10%
    4. Verify trend shows "✓ Improving"
    """
```

### Test 5: Filter Validation
```python
def test_filters_on_reports():
    """
    Create 20 tasks (10 spec haiku, 10 build sonnet), verify filters:
    1. compare --type spec (shows 10 spec tasks only)
    2. compare --model sonnet (shows 10 build tasks only)
    3. budget --remaining --type build (sums build tasks only)
    4. trend --type spec (groups spec tasks only)
    """
```

### Test 6: Edge Cases
```python
def test_edge_cases():
    """
    Handle corner cases gracefully:
    1. No completed tasks yet (calibration shows 1.0x)
    2. est_hours=0 (skip in calibration, don't divide by zero)
    3. Missing response files (import-responses logs warning, continues)
    4. Build monitor unreachable (import-actuals fails gracefully)
    5. All tasks complete (budget --remaining shows 0)
    """
```

## CLI Help Text Requirements

Each command must have `--help` text with:
- Brief description (one sentence)
- Usage examples
- Required arguments
- Optional arguments with defaults
- Example output (abbreviated)

**Example (import-scheduler):**
```
usage: estimates.py import-scheduler [-h] scheduler_file

Import estimates from a scheduler TASKS list.

Parses the scheduler file, extracts task_id, task_type, est_hours,
derives cost/carbon estimates, and writes to inv_estimates table.

positional arguments:
  scheduler_file  Path to scheduler file (e.g., hivenode/scheduler/scheduler_mobile_workdesk.py)

optional arguments:
  -h, --help      show this help message and exit

Example:
  python _tools/estimates.py import-scheduler hivenode/scheduler/scheduler_mobile_workdesk.py

Output:
  Imported 66 tasks from scheduler
  - 8 spec tasks (haiku, avg 2.5h, $0.10, 4500g CO2)
  - 42 build tasks (sonnet, avg 6.0h, $0.79, 158g CO2)
```

## README Section (to add)

Add this section to `README.md` after the "Testing" section:

```markdown
## Estimation Calibration

The estimation calibration ledger tracks the Three Cs (Clock, Cost, Carbon) for every dispatched task, learns calibration factors from completed work, and projects accurate budgets for remaining tasks.

### Why This Matters

Initial estimates are often wrong. Build tasks might take 35% longer than estimated, while spec tasks finish 8% faster. The calibration system learns these patterns and adjusts future estimates automatically, improving budget accuracy by 40%.

### Quick Start

1. **Import estimates from scheduler:**
   ```bash
   python _tools/estimates.py import-scheduler hivenode/scheduler/scheduler_mobile_workdesk.py
   ```

2. **Import actuals as tasks complete:**
   ```bash
   python _tools/estimates.py import-actuals  # fetches from build monitor
   python _tools/estimates.py import-responses .deia/hive/responses/  # backfill from response files
   ```

3. **View calibration factors:**
   ```bash
   python _tools/estimates.py calibration
   ```

4. **Project remaining work:**
   ```bash
   python _tools/estimates.py budget --remaining
   ```

5. **Track accuracy over time:**
   ```bash
   python _tools/estimates.py trend
   ```

### Commands

- `import-scheduler <file>` — import estimates from scheduler TASKS list
- `import-actuals` — fetch actuals from build monitor API
- `import-responses <dir>` — parse Clock/Cost/Carbon from response files
- `record <task_id> ...` — manually record an estimate
- `actual <task_id> ...` — manually record actuals
- `calibration` — show per-type calibration factors
- `compare` — per-task comparison (original → calibrated → actual)
- `budget --remaining` — project remaining work with calibrated estimates
- `trend` — show accuracy improvement over time

### Data Sources

- **Estimates:** Scheduler TASKS list (duration_hours → est_hours, derived cost/carbon)
- **Actuals (cost/carbon):** Build monitor API (tokens → USD via rate_loader, tokens → CO2e via carbon.yml)
- **Actuals (clock):** Build monitor timestamps (completed_at - started_at)
- **Actuals (override):** Response files (Clock/Cost/Carbon sections take precedence)

### Architecture

- **Tables:** `inv_estimates` (per-task records), `inv_calibration` (per-type factors)
- **Database:** Railway PostgreSQL (same as inventory)
- **Calibration:** Rolling average of (actual / estimate) for each task type
- **Reports:** CLI commands format output as fixed-width tables
```

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass (`python -m pytest tests/hivenode/inventory/test_estimates_integration.py -v`)
- [ ] Edge cases:
  - No data (empty database, all commands return gracefully)
  - Build monitor unreachable (connection timeout, clear error)
  - Response file malformed (missing sections, skip and log warning)
  - All tasks complete (budget shows 0, not error)
  - Filters with no matches (empty result, not error)

## Test Coverage (minimum 8 tests)
Create `tests/hivenode/inventory/test_estimates_integration.py` with:
1. `test_full_estimation_workflow()` — import scheduler → actuals → calibration → budget
2. `test_response_file_vs_build_monitor()` — validate two data sources match (within 10%)
3. `test_manual_task_calibration()` — record 10 manual, compute calibration, apply to 10 new
4. `test_trend_groups_by_week()` — 3 weeks of data, verify trend shows improving
5. `test_filters_on_compare()` — --type, --model filters work
6. `test_filters_on_budget()` — --type filter works on budget
7. `test_edge_case_no_data()` — all commands run on empty DB, no crashes
8. `test_edge_case_all_complete()` — budget --remaining shows 0 when all done
9. `test_help_text_exists()` — verify --help works for all 9 commands
10. `test_smoke_all_commands()` — run all commands with test data, verify no crashes

## Constraints
- No file over 500 lines (integration tests can be in one file, ~300 lines expected)
- CSS: var(--sd-*) only (N/A for this task)
- No stubs (all tests fully implemented)
- Use pytest fixtures for test database setup/teardown
- Integration tests use real database (Railway PG or temp SQLite)
- Mock httpx for build monitor API (don't require running server)

## Acceptance Criteria
- [ ] End-to-end test: import scheduler → simulate completed tasks → calibration updates → budget projection changes
- [ ] Validation test: compare response file Cs vs build monitor token-computed Cs (within 10% tolerance)
- [ ] Manual workflow test: record 10 tasks manually, compute calibration, verify factors are reasonable
- [ ] Trend test: 3 weeks of data, verify weekly grouping and "Improving" trend
- [ ] Filter tests: --type, --model, --phase work on compare/budget/trend
- [ ] Edge case tests: no data, all complete, division by zero, missing files
- [ ] `--help` text exists for all 9 commands (record, actual, import-scheduler, import-actuals, import-responses, calibration, compare, budget, trend)
- [ ] README.md has "Estimation Calibration" section (200-300 words, examples, architecture)
- [ ] Smoke test passes (all commands execute without errors on test data)
- [ ] Tests: 10+ integration tests
- [ ] All tests pass: `python -m pytest tests/hivenode/inventory/test_estimates_integration.py -v`

## Smoke Test
```bash
# Run all commands on test data (no crashes)
python _tools/estimates.py import-scheduler hivenode/scheduler/scheduler_mobile_workdesk.py
python _tools/estimates.py import-actuals  # may fail if build monitor not running, that's OK
python _tools/estimates.py import-responses .deia/hive/responses/
python _tools/estimates.py calibration
python _tools/estimates.py compare
python _tools/estimates.py budget --remaining
python _tools/estimates.py trend

# Verify help text
python _tools/estimates.py --help
python _tools/estimates.py import-scheduler --help
python _tools/estimates.py calibration --help

# Run integration tests
python -m pytest tests/hivenode/inventory/test_estimates_integration.py -v
```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260406-TASK-EST-04-RESPONSE.md`

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
