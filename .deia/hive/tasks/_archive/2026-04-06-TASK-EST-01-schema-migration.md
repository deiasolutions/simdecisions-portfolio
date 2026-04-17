# TASK-EST-01: Schema + Migration + Data Model

## Objective
Create `inv_estimates` and `inv_calibration` tables in the inventory database with migration support, enabling the Three C (Clock, Cost, Carbon) calibration ledger.

## Context
This is Phase 1 of the estimation calibration ledger system. The system tracks original estimates, calibrated estimates (using learned factors), and actuals for every dispatched task. It computes calibration factors by task type and provides budget projections.

The existing inventory database lives on Railway PostgreSQL (not local SQLite). Connection is handled via `hivenode/inventory/store.py` using SQLAlchemy Core (no ORM). This task adds 2 new tables without modifying the existing 6 tables (inv_features, inv_backlog, inv_bugs, inv_tests, inv_stage_log, inv_early_access).

**Design doc:** `.deia/hive/responses/20260406-BRIEFING-ESTIMATION-CALIBRATION-LEDGER-RESPONSE.md`

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\inventory\store.py`
  Existing inventory schema (6 tables). You'll add 2 new tables here.
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\inventory\tests\test_inventory_schema_columns.py`
  Example test patterns for schema verification.
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260406-BRIEFING-ESTIMATION-CALIBRATION-LEDGER-RESPONSE.md`
  Full design doc with schema definitions.

## Schema Definitions

### Table 1: `inv_estimates` (per-task records)

```python
inv_estimates = Table(
    "inv_estimates", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("task_id", Text, nullable=False, unique=True),  # e.g., "MW-031", "SPEC-EFEMERA-CONN-05"
    Column("task_type", Text, nullable=False),  # spec, build, test, verify, css, integration
    Column("phase", Text),  # e.g., "Phase 0", "Phase 2", from scheduler or spec
    Column("model", Text),  # haiku, sonnet, opus (assigned model)

    # Original estimates (from scheduler TASKS list or spec)
    Column("est_hours", Float, nullable=False),
    Column("est_cost_usd", Float, nullable=False),
    Column("est_carbon_g", Float, nullable=False),

    # Calibrated estimates (original × calibration_factor)
    Column("calibrated_hours", Float),
    Column("calibrated_cost_usd", Float),
    Column("calibrated_carbon_g", Float),

    # Actuals (from build monitor + response files)
    Column("actual_hours", Float),
    Column("actual_cost_usd", Float),
    Column("actual_carbon_g", Float),

    # Deltas (percentage error: (actual - estimate) / estimate * 100)
    Column("delta_hours_pct", Float),
    Column("delta_cost_pct", Float),
    Column("delta_carbon_pct", Float),

    # Timestamps
    Column("started_at", Text),  # ISO 8601
    Column("completed_at", Text),  # ISO 8601
    Column("created_at", Text, nullable=False),  # when estimate was recorded
    Column("updated_at", Text, nullable=False),  # last update
)
Index("ix_inv_est_task_id", inv_estimates.c.task_id)
Index("ix_inv_est_task_type", inv_estimates.c.task_type)
Index("ix_inv_est_model", inv_estimates.c.model)
```

### Table 2: `inv_calibration` (per-type factors)

```python
inv_calibration = Table(
    "inv_calibration", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("task_type", Text, nullable=False, unique=True),  # spec, build, test, verify, css

    # Calibration factors (mean of actual/estimate for all completed tasks of this type)
    Column("clock_factor", Float, nullable=False, server_default="1.0"),
    Column("cost_factor", Float, nullable=False, server_default="1.0"),
    Column("carbon_factor", Float, nullable=False, server_default="1.0"),

    # Metadata
    Column("sample_count", Integer, nullable=False, server_default="0"),  # how many tasks contributed
    Column("last_updated", Text, nullable=False),  # ISO 8601
    Column("created_at", Text, nullable=False),
)
Index("ix_inv_calib_type", inv_calibration.c.task_type)
```

## Deliverables
- [ ] Add `inv_estimates` table to `hivenode/inventory/store.py` (19 columns as specified above)
- [ ] Add `inv_calibration` table to `hivenode/inventory/store.py` (7 columns as specified above)
- [ ] Add 3 indexes for `inv_estimates`: task_id (unique), task_type, model
- [ ] Add 1 index for `inv_calibration`: task_type (unique)
- [ ] Migration function `_migrate_estimates_tables(conn)` that:
  - Checks if `inv_estimates` and `inv_calibration` exist
  - Creates them if missing (idempotent)
  - Uses defensive SQL (IF NOT EXISTS pattern or try/except)
  - Works on both SQLite (local) and PostgreSQL (Railway)
- [ ] Update `init_engine()` to call `_migrate_estimates_tables()` after existing migrations
- [ ] No changes to existing 6 tables (features, backlog, bugs, tests, stage_log, early_access)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass (`python -m pytest tests/hivenode/inventory/test_estimates_schema.py -v`)
- [ ] Edge cases:
  - Migration runs twice (idempotent check)
  - SQLite: server defaults become literal values (clock_factor=1.0, sample_count=0)
  - PostgreSQL: server defaults work via DEFAULT clause
  - task_id unique constraint enforced
  - task_type unique constraint enforced (in inv_calibration)
  - All indexes created and usable

## Test Coverage (minimum 10 tests)
Create `tests/hivenode/inventory/test_estimates_schema.py` with:
1. `test_inv_estimates_table_created()` — table exists after migration
2. `test_inv_estimates_has_19_columns()` — column count and names
3. `test_inv_estimates_column_types()` — id=Integer, task_id=Text, est_hours=Float, etc.
4. `test_inv_estimates_task_id_unique()` — insert duplicate task_id fails
5. `test_inv_estimates_indexes_exist()` — 3 indexes created
6. `test_inv_calibration_table_created()` — table exists after migration
7. `test_inv_calibration_has_7_columns()` — column count and names
8. `test_inv_calibration_server_defaults()` — clock_factor defaults to 1.0, sample_count to 0
9. `test_inv_calibration_task_type_unique()` — insert duplicate task_type fails
10. `test_migration_idempotent()` — run migration twice, no errors
11. `test_both_tables_on_postgresql()` — connect to Railway PG, verify tables exist
12. `test_both_tables_on_sqlite()` — create temp SQLite DB, verify tables exist

## Constraints
- No file over 500 lines (`store.py` is currently ~350 lines, adding ~50 lines OK)
- CSS: var(--sd-*) only (N/A for this task)
- No stubs (all functions fully implemented)
- Follow SQLAlchemy Core pattern (no ORM)
- Use `text()` for raw SQL in migrations (matches existing pattern in store.py)
- Defensive migrations: check table existence before CREATE TABLE

## Acceptance Criteria
- [ ] `inv_estimates` table created with 19 columns (id, task_id, task_type, phase, model, 3 sets of Cs, 3 deltas, 4 timestamps)
- [ ] `inv_calibration` table created with 7 columns (id, task_type, 3 factors, sample_count, last_updated, created_at)
- [ ] Migration runs idempotently (safe to call multiple times, no errors)
- [ ] Server defaults work: clock_factor=1.0, cost_factor=1.0, carbon_factor=1.0, sample_count=0
- [ ] task_id unique constraint enforced (insert duplicate raises IntegrityError)
- [ ] task_type unique constraint enforced in inv_calibration
- [ ] Tests: 12+ tests covering schema, migration, indexes, both SQLite and PostgreSQL
- [ ] All tests pass: `python -m pytest tests/hivenode/inventory/test_estimates_schema.py -v`
- [ ] Works on SQLite (local) and PostgreSQL (Railway)

## Smoke Test
```bash
# Local SQLite test
cd hivenode
python -c "from inventory.store import init_engine; init_engine('sqlite:///[REDACTED].db'); print('Migration OK')"

# Railway PostgreSQL test (requires INVENTORY_DATABASE_URL)
python -c "from inventory.store import init_engine; init_engine(); print('Migration OK on Railway PG')"

# Run tests
python -m pytest tests/hivenode/inventory/test_estimates_schema.py -v
```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260406-TASK-EST-01-RESPONSE.md`

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
