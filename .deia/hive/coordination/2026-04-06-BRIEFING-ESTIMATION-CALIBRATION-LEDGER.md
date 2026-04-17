# BRIEFING: Estimation Calibration Ledger

**From:** Q33NR
**To:** Q33N
**Date:** 2026-04-06
**Priority:** P1

## Context

We run builds with estimated hours per task (from OR-Tools scheduler) but have no system to:
1. Record original estimates for all three Cs (Clock, Cost, Carbon)
2. Record actuals for all three Cs after completion
3. Compare estimate vs actual
4. Feed a calibration model that improves future estimates

We need a central data collection and calibration system.

## The Three Cs

Every task in the hive tracks three dimensions:
- **Clock** — wall-clock hours (time to complete)
- **Cost** — USD spent on API calls (model tokens)
- **Carbon** — CO2 emissions (grams)

Currently:
- **Clock estimates** exist in `scheduler_mobile_workdesk.py` TASKS list (`hours` field)
- **Cost estimates** don't exist — but can be derived from model × expected turns × token rates (`hivenode/rate_loader/model_rates.yml`)
- **Carbon estimates** don't exist — but can be derived from cost × carbon factor (`.deia/config/carbon.yml`)
- **Actuals** are scattered: build monitor (`/build/status`), response files (Clock/Cost/Carbon sections), `dispatched.jsonl`

## Goal

Design and build an **estimation calibration ledger** that:

### 1. Records per-task data
For every dispatched task, record:
- `task_id`, `task_type` (spec/build/css/verify/test/integration), `phase`, `model`
- `est_hours`, `est_cost_usd`, `est_carbon_g` — original estimates
- `calibrated_hours`, `calibrated_cost_usd`, `calibrated_carbon_g` — model-adjusted estimates
- `actual_hours`, `actual_cost_usd`, `actual_carbon_g` — real measured values
- `delta_hours`, `delta_cost`, `delta_carbon` — percentage error
- `started_at`, `completed_at` — ISO timestamps

### 2. Collects data from existing sources
- Pull estimates from scheduler TASKS list
- Pull actuals from build monitor API (`GET /build/status`)
- Pull actuals from response files (parse Clock/Cost/Carbon sections)
- Pull token rates from `model_rates.yml`
- Pull carbon factors from `carbon.yml`

### 3. Computes calibration factors
- Group tasks by `task_type` (css, build, spec, verify, test)
- Per group: `calibration_factor = mean(actual / estimate)` for each of the 3 Cs
- Store calibration factors, update after each completed task
- Apply calibration to future estimates: `calibrated = original × calibration_factor`

### 4. Produces reports
- Per-task comparison: original vs calibrated vs actual (all 3 Cs)
- Per-phase summary: total estimated vs actual (Clock, Cost, Carbon)
- Per-type accuracy: which task types are we best/worst at estimating?
- Build budget projection: "66 tasks will cost ~$X, take ~Y hours, emit ~Zg CO2"
- Calibration trend: how accuracy improves over time

## Storage

Use the inventory database (same as `inv_features`, `inv_stage_log`, etc.):
- New table: `inv_estimates` or `est_calibration`
- SQLAlchemy Core pattern (matches existing inventory tables)
- Works on both SQLite (local) and PostgreSQL (Railway)

## CLI Interface

Extend `_tools/inventory.py` or create `_tools/estimates.py`:
```bash
# Record estimates for a task
python _tools/estimates.py record MW-031 --est-hours 2.0 --est-cost 3.00 --est-carbon 4.0

# Record actuals (or auto-pull from build monitor)
python _tools/estimates.py actual MW-031 --pull-from-monitor

# Bulk import estimates from scheduler TASKS list
python _tools/estimates.py import-scheduler hivenode/scheduler/scheduler_mobile_workdesk.py

# Bulk import actuals from build monitor
python _tools/estimates.py import-actuals

# Show calibration factors
python _tools/estimates.py calibration

# Show per-task comparison
python _tools/estimates.py compare

# Show build budget projection
python _tools/estimates.py budget --remaining
```

## Files to Read First

- `hivenode/scheduler/scheduler_mobile_workdesk.py` — TASKS list with hours estimates
- `hivenode/rate_loader/model_rates.yml` — token pricing per model
- `.deia/config/carbon.yml` — carbon emission factors
- `hivenode/routes/build_monitor.py` — build status API (actuals source)
- `hivenode/inventory/schema.py` — existing inventory table patterns
- `_tools/inventory.py` — existing CLI tool patterns
- `.deia/hive/responses/` — response files with Clock/Cost/Carbon sections

## Deliverables

This is a DESIGN + BUILD task. The Q33N should:

1. **Design the schema** — table definition, columns, types, indexes
2. **Design the calibration algorithm** — per-type grouping, factor computation, Bayesian update or simple rolling average
3. **Create task files** for bee dispatch (3-4 tasks):
   - Task 1: Schema + migration + data model
   - Task 2: Data collection (import from scheduler, build monitor, response files)
   - Task 3: Calibration engine + CLI commands
   - Task 4: Budget projection + reporting

## Constraints
- SQLAlchemy Core pattern (not ORM) — matches existing inventory code
- Works on SQLite and PostgreSQL
- CLI via `_tools/estimates.py`
- No file over 500 lines
- TDD where applicable
