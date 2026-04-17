# BRIEFING: Estimation Calibration Ledger -- DESIGN COMPLETE

**From:** Q33N
**To:** Q33NR
**Date:** 2026-04-06
**Priority:** P1

## Executive Summary

I've designed a complete **estimation calibration ledger** system that tracks the Three Cs (Clock, Cost, Carbon) for every task, computes calibration factors by task type, and provides budget projections. The system uses the existing inventory database (Railway PostgreSQL), follows SQLAlchemy Core patterns, and integrates with the scheduler, build monitor, and response files.

## System Architecture

### Data Flow

```
┌────────────────────────────────────────────────────────────┐
│ DATA SOURCES                                                │
├────────────────────────────────────────────────────────────┤
│ 1. scheduler_mobile_workdesk.py TASKS → original estimates │
│ 2. /build/status API → actuals (tokens, timestamps)        │
│ 3. response files → actuals (Clock/Cost/Carbon sections)   │
│ 4. model_rates.yml → token pricing                         │
│ 5. carbon.yml → carbon factors                             │
└────────────────────────────────────────────────────────────┘
           │
           │ IMPORT + COMPUTE
           ↓
┌────────────────────────────────────────────────────────────┐
│ ESTIMATION LEDGER (inv_estimates table)                    │
├────────────────────────────────────────────────────────────┤
│ - task_id, task_type, phase, model                         │
│ - est_hours, est_cost_usd, est_carbon_g                    │
│ - calibrated_hours, calibrated_cost, calibrated_carbon     │
│ - actual_hours, actual_cost, actual_carbon                 │
│ - delta_% for each dimension                               │
│ - started_at, completed_at timestamps                      │
└────────────────────────────────────────────────────────────┘
           │
           │ AGGREGATE
           ↓
┌────────────────────────────────────────────────────────────┐
│ CALIBRATION FACTORS (inv_calibration table)                │
├────────────────────────────────────────────────────────────┤
│ - task_type (spec, build, test, verify, css)              │
│ - clock_factor, cost_factor, carbon_factor                 │
│ - sample_count, last_updated                               │
│ - Bayesian update: weighted average with priors           │
└────────────────────────────────────────────────────────────┘
           │
           │ REPORTS
           ↓
┌────────────────────────────────────────────────────────────┐
│ CLI OUTPUTS                                                 │
├────────────────────────────────────────────────────────────┤
│ - Per-task comparison (original vs calibrated vs actual)   │
│ - Per-type accuracy (which types are we good/bad at?)     │
│ - Budget projection (remaining work → $, hours, CO2)       │
│ - Calibration trend (accuracy over time)                   │
└────────────────────────────────────────────────────────────┘
```

## Database Schema

### Table 1: `inv_estimates` (per-task records)

Tracks original estimates, calibrated estimates, and actuals for every dispatched task.

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

**Key design choices:**
- `task_id` is unique — one row per task (not per attempt)
- `task_type` groups tasks for calibration (spec, build, test, verify, css, integration)
- `phase` tracks which build phase (for per-phase reports)
- Three sets of measurements: original estimates, calibrated estimates, actuals
- Delta percentages pre-computed for fast queries
- ISO 8601 timestamps (matches scheduler_daemon pattern)

### Table 2: `inv_calibration` (per-type factors)

Stores calibration factors computed from completed tasks, grouped by task type.

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

**Calibration algorithm:**

**Simple rolling average (Phase 1):**
```python
clock_factor = mean(actual_hours / est_hours) for all completed tasks of this type
```

**Bayesian update (Phase 2 — optional future upgrade):**
```python
# Prior: factor = 1.0, confidence = 3 samples
# Posterior: weighted average of prior and new data
weight_prior = 3
weight_data = sample_count
clock_factor = (weight_prior * 1.0 + weight_data * data_mean) / (weight_prior + weight_data)
```

For Phase 1 (this build), we use **simple rolling average** — proven, predictable, easy to debug.

## Data Collection

### 1. Estimates (from scheduler TASKS list)

**Source:** `hivenode/scheduler/scheduler_mobile_workdesk.py` → `TASKS` list

**Extract:**
- `task_id`: `Task.id`
- `task_type`: `Task.task_type` (SPEC, TEST, BUILD, VERIFY → lowercase)
- `est_hours`: `Task.duration_hours`
- `phase`: extract from `Task.description` (e.g., "Phase 2: Input surfaces BUILD" → "Phase 2")

**Derive est_cost_usd:**
```python
# Assumption: haiku for spec/test, sonnet for build/verify
model = "haiku" if task_type in ("spec", "test") else "sonnet"
expected_turns = 10  # average turns per task
tokens_per_turn = 4000 input + 2000 output  # rough average

rate = get_rate(model)  # from hivenode/rate_loader
est_cost_usd = (
    (expected_turns * 4000 / 1_000_000) * rate["input_per_million"] +
    (expected_turns * 2000 / 1_000_000) * rate["output_per_million"]
)
```

**Derive est_carbon_g:**
```python
# Option 1: From model_rates.yml carbon_per_million_tokens
carbon_g = (expected_turns * 6000 / 1_000_000) * carbon_per_million_tokens

# Option 2: From carbon.yml model_energy
energy_kwh = (
    (expected_turns * 4000 / 1000) * model_energy["input_kwh_per_1k"] +
    (expected_turns * 2000 / 1000) * model_energy["output_kwh_per_1k"]
)
carbon_g = energy_kwh * carbon_intensity_g_kwh
```

**CLI command:**
```bash
python _tools/estimates.py import-scheduler hivenode/scheduler/scheduler_mobile_workdesk.py
```

### 2. Actuals (from build monitor + response files)

**Source A: Build monitor API** (`GET /build/status`)

**Extract:**
- `task_id`: from `active[*].task_id` or `completed[*].task_id`
- `actual_cost_usd`: compute from `input_tokens` + `output_tokens` via rate_loader
- `actual_carbon_g`: compute from tokens via carbon.yml
- `started_at`: `first_seen`
- `completed_at`: `last_seen` (if status == "complete")
- `actual_hours`: `(completed_at - started_at).total_seconds() / 3600`

**Source B: Response files** (`.deia/hive/responses/*-RESPONSE.md`)

**Parse Clock/Cost/Carbon section:**
```markdown
## Clock / Cost / Carbon
- **Clock:** 2.5 hours
- **Cost:** $0.42 USD
- **Carbon:** 150g CO2e
```

**Fallback priority:**
1. If response file has all three Cs, use it (most reliable)
2. Else, compute from build monitor tokens (cost/carbon)
3. Else, mark as incomplete (wait for bee to finish)

**CLI commands:**
```bash
# Auto-pull actuals from build monitor
python _tools/estimates.py import-actuals

# Bulk import from response files (one-time backfill)
python _tools/estimates.py import-responses .deia/hive/responses/
```

## Calibration Engine

### Update calibration after each completed task

**Trigger:** When `actual_*` values are recorded for a task

**Algorithm:**
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

### Apply calibration to new estimates

**When:** During `import-scheduler` or when recording new estimates

**Algorithm:**
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

## CLI Interface

New script: `_tools/estimates.py` (or extend `_tools/inventory.py`)

### Commands

#### 1. Record estimates (manual)
```bash
python _tools/estimates.py record MW-031 \
  --est-hours 2.0 \
  --est-cost 3.00 \
  --est-carbon 4.0 \
  --type build \
  --model sonnet
```

#### 2. Import estimates from scheduler
```bash
python _tools/estimates.py import-scheduler hivenode/scheduler/scheduler_mobile_workdesk.py

# Output:
# Imported 66 tasks from scheduler
# - 8 spec tasks (haiku, avg 2.5h, $2.00, 280g CO2)
# - 8 test tasks (haiku, avg 3.5h, $2.80, 390g CO2)
# - 42 build tasks (sonnet, avg 6.0h, $18.00, 2500g CO2)
# - 8 verify tasks (sonnet, avg 2.0h, $6.00, 840g CO2)
```

#### 3. Import actuals (auto-pull from build monitor)
```bash
python _tools/estimates.py import-actuals

# Output:
# Fetched status from http://127.0.0.1:8420/build/status
# Updated 12 tasks with actuals
# - 3 complete (MW-031, MW-032, MW-033)
# - 9 in_progress (MW-034, ...)
# Calibration updated for: build, css
```

#### 4. Import actuals from response files (bulk backfill)
```bash
python _tools/estimates.py import-responses .deia/hive/responses/

# Output:
# Scanned 247 response files
# Updated 185 tasks with Clock/Cost/Carbon data
# - 142 had complete C3 sections
# - 43 had partial data (filled gaps from build monitor)
# - 19 missing (no task_id match)
# Calibration updated for: spec, build, test, verify, css
```

#### 5. Record actuals (manual)
```bash
python _tools/estimates.py actual MW-031 \
  --actual-hours 2.8 \
  --actual-cost 3.42 \
  --actual-carbon 4.8 \
  --completed-at "2026-04-06T14:30:00Z"
```

#### 6. Show calibration factors
```bash
python _tools/estimates.py calibration

# Output:
# Calibration Factors (Mobile Workdesk Build)
#
# Type       Clock    Cost     Carbon   Samples  Last Updated
# ─────────  ───────  ───────  ───────  ───────  ────────────
# spec       0.920x   1.050x   1.050x   8        2026-04-06
# test       1.120x   1.080x   1.080x   8        2026-04-06
# build      1.350x   1.200x   1.200x   12       2026-04-06
# verify     0.850x   0.920x   0.920x   3        2026-04-06
# css        1.100x   N/A      N/A      5        2026-04-06
#
# Interpretation:
# - spec tasks finish 8% faster than estimated (good!)
# - build tasks take 35% longer than estimated (recalibrate)
# - verify tasks finish 15% faster (good!)
```

#### 7. Per-task comparison
```bash
python _tools/estimates.py compare

# Output:
# Task       Type   Est→Cal→Act (Hours)     Est→Cal→Act (Cost)      Est→Cal→Act (Carbon)    Δ%
# ─────────  ─────  ──────────────────────  ──────────────────────  ──────────────────────  ──────
# MW-S01     spec   3.0 → 2.8 → 2.5 ✓       $2.40 → $2.52 → $2.10   340g → 357g → 294g      -17%
# MW-001     build  8.0 → 10.8 → 11.2       $24.00 → $28.80 → $30.5 3360g → 4032g → 4270g   +40%
# MW-031     css    6.0 → 6.6 → 7.1         N/A                     N/A                     +18%
# ...
#
# Filters: --type build --model sonnet --phase "Phase 2"
```

#### 8. Budget projection (remaining work)
```bash
python _tools/estimates.py budget --remaining

# Output:
# Mobile Workdesk Build Budget (Remaining Tasks)
#
# Total Remaining: 54 tasks
#
# Original Estimates:
# - Clock:  180 hours
# - Cost:   $540 USD
# - Carbon: 75,600g CO2e (75.6 kg)
#
# Calibrated Estimates (with learned factors):
# - Clock:  224 hours (+24%)
# - Cost:   $648 USD (+20%)
# - Carbon: 90,720g CO2e (+20%)
#
# By Type:
# Type       Tasks  Calibrated Hours  Calibrated Cost  Calibrated Carbon
# ─────────  ─────  ────────────────  ───────────────  ─────────────────
# spec       5      12.5h             $12.60           1,764g
# test       5      17.5h             $15.12           2,117g
# build      30     180.0h            $540.00          75,600g
# verify     5      8.5h              $27.60           3,864g
# css        9      5.5h              N/A              N/A
#
# Estimated Completion: 2026-04-12 (assuming 10 parallel bees)
#
# Notes:
# - Calibration improves accuracy by 40% vs original estimates
# - Build tasks are the largest uncertainty (1.35x underestimation)
# - Consider allocating 20% time buffer for unknowns
```

#### 9. Calibration trend (accuracy over time)
```bash
python _tools/estimates.py trend

# Output:
# Estimation Accuracy Trend (by completion date)
#
# Week      Completed  Avg Delta (Clock)  Avg Delta (Cost)  Avg Delta (Carbon)
# ────────  ─────────  ─────────────────  ────────────────  ──────────────────
# 2026-W14  8          +28%               +32%              +32%
# 2026-W15  12         +18%               +22%              +22%
# 2026-W16  20         +12%               +15%              +15%
#
# Trend: ✓ Improving (delta decreasing over time)
#
# Recent Tasks (last 10):
# Task       Completed    Clock Δ  Cost Δ   Carbon Δ
# ─────────  ───────────  ───────  ───────  ─────────
# MW-031     2026-04-06   +18%     N/A      N/A
# MW-032     2026-04-06   +10%     +12%     +12%
# MW-033     2026-04-06   +5%      +8%      +8%
# ...
```

## Task Breakdown (4 Tasks for Bee Dispatch)

### TASK-EST-01: Schema + Migration + Data Model
**Type:** BUILD
**Est Hours:** 3
**Model:** Haiku
**Dependencies:** None

**Deliverables:**
- Add `inv_estimates` and `inv_calibration` tables to `hivenode/inventory/store.py`
- Migration function `_migrate_estimates_tables()` (idempotent, defensive)
- Update `init_engine()` to call migration
- Indexes: task_id (unique), task_type, model
- Server defaults: calibration factors = 1.0, sample_count = 0
- No changes to existing tables (features, backlog, bugs, tests, stage_log remain unchanged)
- Tests: table creation, column types, indexes, migrations (SQLite + PostgreSQL)

**Acceptance Criteria:**
- [ ] `inv_estimates` table created with 19 columns (id, task_id, task_type, phase, model, 3 sets of Cs, 3 deltas, 4 timestamps)
- [ ] `inv_calibration` table created with 7 columns (id, task_type, 3 factors, sample_count, last_updated, created_at)
- [ ] Migration runs idempotently (safe to call multiple times)
- [ ] Tests: 10+ tests covering schema, migration, indexes
- [ ] Works on SQLite (local) and PostgreSQL (Railway)

---

### TASK-EST-02: Data Collection (Import from Sources)
**Type:** BUILD
**Est Hours:** 6
**Model:** Sonnet
**Dependencies:** TASK-EST-01

**Deliverables:**
- `_tools/estimates.py` CLI script (argparse, commands: import-scheduler, import-actuals, import-responses, record, actual)
- `import-scheduler`: parse `scheduler_mobile_workdesk.py` TASKS list, extract estimates, derive cost/carbon
- `import-actuals`: fetch `GET /build/status`, compute actuals from tokens
- `import-responses`: scan `.deia/hive/responses/*-RESPONSE.md`, parse Clock/Cost/Carbon sections
- `record`: manual estimate recording (task_id, type, model, est_hours, est_cost, est_carbon)
- `actual`: manual actual recording (task_id, actual_hours, actual_cost, actual_carbon, completed_at)
- Token→cost conversion via `hivenode/rate_loader/get_rate()`
- Token→carbon conversion via `.deia/config/carbon.yml` model_energy
- Fallback: if response file has Cs, use it; else compute from build monitor; else mark incomplete
- Tests: import from scheduler (8 specs, 42 builds), import from build monitor, import from response files, manual record

**Acceptance Criteria:**
- [ ] `estimates.py import-scheduler <path>` imports all TASKS, derives cost/carbon, writes to `inv_estimates`
- [ ] `estimates.py import-actuals` fetches build monitor status, updates actuals for completed tasks
- [ ] `estimates.py import-responses <dir>` parses response files, extracts Clock/Cost/Carbon, updates actuals
- [ ] `estimates.py record <task_id> --est-hours X --est-cost Y --est-carbon Z` inserts row
- [ ] `estimates.py actual <task_id> --actual-hours X --actual-cost Y --actual-carbon Z` updates row
- [ ] Tests: 12+ tests covering all import paths, rate_loader integration, carbon.yml integration, manual commands
- [ ] Handles missing files gracefully (no crashes)

---

### TASK-EST-03: Calibration Engine + CLI Commands
**Type:** BUILD
**Est Hours:** 5
**Model:** Sonnet
**Dependencies:** TASK-EST-02

**Deliverables:**
- `_tools/estimates.py` commands: calibration, compare, budget, trend
- `calibration`: show per-type factors, sample counts, last updated
- `compare`: per-task table (original → calibrated → actual, delta %)
- `budget --remaining`: sum remaining tasks, apply calibration factors, project totals
- `trend`: show accuracy over time (group by week, compute avg delta)
- Calibration update function: `update_calibration(task_type)` — compute mean(actual/estimate) for each C
- Apply calibration: `apply_calibration(task_type, est_*)` → calibrated_*
- Automatic calibration update on `import-actuals` and `actual` commands
- Tests: calibration computation, apply calibration, budget projection, trend analysis, CLI output formatting

**Acceptance Criteria:**
- [ ] `estimates.py calibration` shows table with per-type factors (clock, cost, carbon), sample counts
- [ ] `estimates.py compare` shows per-task comparison (est → cal → actual), delta % for all 3 Cs
- [ ] `estimates.py budget --remaining` projects remaining work with calibrated estimates
- [ ] `estimates.py trend` shows accuracy improvement over time (weekly grouping)
- [ ] Calibration factors update automatically after recording actuals
- [ ] Filters: `--type`, `--model`, `--phase` work on compare/budget/trend
- [ ] Tests: 10+ tests covering calibration math, budget projection, trend computation, CLI output
- [ ] No file over 500 lines (split into `estimates.py` + `estimates_db.py` if needed)

---

### TASK-EST-04: Integration Tests + Documentation
**Type:** TEST
**Est Hours:** 3
**Model:** Haiku
**Dependencies:** TASK-EST-03

**Deliverables:**
- Integration test: import scheduler → import actuals → calibration → budget projection (end-to-end)
- Integration test: import response files → compare actuals vs computed-from-tokens (validation)
- Integration test: record 10 manual tasks → compute calibration → apply to 10 new tasks → verify accuracy
- CLI help text (`--help` for all commands)
- README section: "Estimation Calibration" (how to use, what it does, why it matters)
- Example workflow: bootstrap new build, import estimates, track actuals, project budget
- Tests: 8+ integration tests covering full workflows
- Smoke test: run all CLI commands with `--dry-run` or on test data, verify no crashes

**Acceptance Criteria:**
- [ ] End-to-end test: import scheduler → simulate completed tasks → calibration updates → budget projection changes
- [ ] Validation test: compare response file Cs vs build monitor token-computed Cs (within 10% tolerance)
- [ ] Manual workflow test: record 10 tasks manually, compute calibration, verify factors are reasonable
- [ ] `--help` text exists for all commands (record, actual, import-scheduler, import-actuals, import-responses, calibration, compare, budget, trend)
- [ ] README.md has "Estimation Calibration" section (200-300 words, examples)
- [ ] Smoke test passes (all commands execute without errors on test data)
- [ ] Tests: 8+ integration tests
- [ ] All tests pass: `python -m pytest tests/inventory/test_estimates*.py -v`

---

## Migration Strategy

### Backward Compatibility

**No breaking changes:**
- New tables: `inv_estimates`, `inv_calibration` (do not modify existing tables)
- Existing inventory commands (`inventory.py add`, `stats`, `export-md`) unchanged
- New commands in separate `estimates.py` script (or as `inventory.py estimates <subcommand>`)

**Optional integration points:**
- `inventory.py export-md` could append an "## Estimation Accuracy" section (future)
- `scheduler_mobile_workdesk.py` could auto-call `estimates.py import-scheduler` on first run (future)

### Deployment Steps

1. Deploy TASK-EST-01: schema + migration (Railway PG auto-creates tables)
2. Bootstrap: `python _tools/estimates.py import-scheduler hivenode/scheduler/scheduler_mobile_workdesk.py`
3. Backfill actuals: `python _tools/estimates.py import-responses .deia/hive/responses/`
4. Monitor: `python _tools/estimates.py calibration` (check factors daily)
5. Budget: `python _tools/estimates.py budget --remaining` (project remaining work)

## Cost Derivation Details

### From Scheduler Estimates (est_cost_usd)

**Inputs:**
- `task_type`: spec, test, build, verify, css
- `est_hours`: from scheduler TASKS list

**Model assignment heuristic:**
```python
model_map = {
    "spec": "haiku",
    "test": "haiku",
    "build": "sonnet",
    "verify": "sonnet",
    "css": "sonnet",  # CSS often needs multimodal understanding
}
model = model_map.get(task_type, "haiku")
```

**Expected token usage:**
```python
# Haiku tasks (spec, test): 10 turns avg, 3k in + 1.5k out per turn
expected_turns_haiku = 10
tokens_in_haiku = 10 * 3000 = 30,000
tokens_out_haiku = 10 * 1500 = 15,000

# Sonnet tasks (build, verify): 15 turns avg, 5k in + 2.5k out per turn
expected_turns_sonnet = 15
tokens_in_sonnet = 15 * 5000 = 75,000
tokens_out_sonnet = 15 * 2500 = 37,500
```

**Cost calculation:**
```python
rate = get_rate(model)  # from hivenode/rate_loader
est_cost_usd = (
    (tokens_in / 1_000_000) * rate["input_per_million"] +
    (tokens_out / 1_000_000) * rate["output_per_million"]
)
```

**Example (haiku spec task, 3 hours):**
```python
model = "claude-haiku-4-5-20251001"
rate = {"input_per_million": 0.80, "output_per_million": 4.00}
tokens_in = 30,000
tokens_out = 15,000

est_cost_usd = (30 / 1000) * 0.80 + (15 / 1000) * 4.00
             = 0.024 + 0.060
             = $0.084
```

**Example (sonnet build task, 8 hours):**
```python
model = "claude-sonnet-4-5-20250929"
rate = {"input_per_million": 3.00, "output_per_million": 15.00}
tokens_in = 75,000
tokens_out = 37,500

est_cost_usd = (75 / 1000) * 3.00 + (37.5 / 1000) * 15.00
             = 0.225 + 0.5625
             = $0.7875
```

### From Actuals (actual_cost_usd)

**Source: Build monitor `/build/status`**

```python
task = completed[0]  # from API response
input_tokens = task["input_tokens"]
output_tokens = task["output_tokens"]
model = task["model"]  # "sonnet", "haiku", "opus"

# Map short names to full IDs
model_id = {
    "sonnet": "claude-sonnet-4-5-20250929",
    "haiku": "claude-haiku-4-5-20251001",
    "opus": "claude-opus-4-6",
}.get(model, "claude-sonnet-4-5-20250929")

rate = get_rate(model_id)
actual_cost_usd = (
    (input_tokens / 1_000_000) * rate["input_per_million"] +
    (output_tokens / 1_000_000) * rate["output_per_million"]
)
```

## Carbon Derivation Details

### Method 1: From model_rates.yml (simple)

`model_rates.yml` has:
```yaml
carbon_per_million_tokens: 100.0  # kg CO2e per million tokens
```

**Calculation:**
```python
total_tokens = input_tokens + output_tokens
est_carbon_g = (total_tokens / 1_000_000) * 100 * 1000  # convert kg to grams
```

**Example (30k in + 15k out = 45k total):**
```python
est_carbon_g = (45 / 1000) * 100 * 1000 = 4500g = 4.5 kg CO2e
```

### Method 2: From carbon.yml (accurate)

`.deia/config/carbon.yml` has energy per 1k tokens + region carbon intensity.

**Calculation:**
```python
model_short = "sonnet"  # from task
model_full = "claude-sonnet-4"  # map to carbon.yml key

energy_config = carbon_yml["model_energy"][model_full]
kwh_input = (input_tokens / 1000) * energy_config["input_kwh_per_1k"]
kwh_output = (output_tokens / 1000) * energy_config["output_kwh_per_1k"]
total_kwh = kwh_input + kwh_output

region = carbon_yml.get("default_region", "us_average")
carbon_intensity = carbon_yml["region_intensity"][region]  # g CO2e per kWh

est_carbon_g = total_kwh * carbon_intensity
```

**Example (sonnet, 75k in + 37.5k out, us_average):**
```python
kwh_input = (75 / 1) * 0.0030 = 0.225 kWh
kwh_output = (37.5 / 1) * 0.0045 = 0.169 kWh
total_kwh = 0.394 kWh

carbon_intensity = 400 g/kWh
est_carbon_g = 0.394 * 400 = 157.6g CO2e
```

**Recommendation:** Use Method 2 (carbon.yml) for actuals, Method 1 (model_rates.yml) for quick estimates.

## Reports

### Per-Task Comparison Table

```
Task       Type   Model   Est→Cal→Act (Hours)     Est→Cal→Act (Cost)      Est→Cal→Act (Carbon)    Δ%
─────────  ─────  ──────  ──────────────────────  ──────────────────────  ──────────────────────  ──────
MW-S01     spec   haiku   3.0 → 2.8 → 2.5 ✓       $0.08 → $0.08 → $0.07   4500g → 4725g → 3920g   -17%
MW-001     build  sonnet  8.0 → 10.8 → 11.2       $0.79 → $0.95 → $1.02   158g → 190g → 204g      +40%
MW-031     css    sonnet  6.0 → 6.6 → 7.1         N/A                     N/A                     +18%
```

**Key:**
- ✓ = within 10% of estimate (good)
- Δ% = `(actual - original_estimate) / original_estimate * 100`
- N/A = CSS tasks have no cost/carbon (front-end only, no API calls)

### Budget Projection

```
Mobile Workdesk Build Budget (Remaining Tasks: 54)

                  Original    Calibrated    Δ
─────────────────────────────────────────────
Clock (hours)     180.0       224.0        +24%
Cost (USD)        $540        $648         +20%
Carbon (g CO2e)   75,600      90,720       +20%

Estimated Completion: 2026-04-12 (assuming 10 parallel bees, 8h/day)

By Type:
Type       Tasks  Cal Hours  Cal Cost    Cal Carbon
─────────  ─────  ─────────  ──────────  ──────────
spec       5      12.5h      $0.42       2,250g
test       5      17.5h      $0.38       2,025g
build      30     180.0h     $594.00     84,240g
verify     5      8.5h       $3.22       456g
css        9      5.5h       N/A         N/A
```

### Calibration Trend

```
Estimation Accuracy Trend (by completion date)

Week      Completed  Avg Δ Clock  Avg Δ Cost  Avg Δ Carbon
────────  ─────────  ───────────  ──────────  ────────────
2026-W14  8          +28%         +32%        +32%
2026-W15  12         +18%         +22%        +22%
2026-W16  20         +12%         +15%        +15%

Trend: ✓ Improving (delta decreasing over time)
```

**Interpretation:** As bees complete more tasks, our estimates improve (delta shrinks).

## Open Questions for Q33NR

1. **Cost derivation precision:** Should we use fixed token estimates (e.g., 10 turns × 4k tokens) or make them proportional to `est_hours` (e.g., `est_hours * 5000 tokens/hour`)?

   **Recommendation:** Start with fixed estimates per task_type (simple, predictable). Add proportional scaling in Phase 2 if needed.

2. **Calibration update frequency:** Should calibration factors update after every completed task, or batch-update daily/weekly?

   **Recommendation:** Update after every completed task (real-time feedback). Batch mode is optional optimization.

3. **Bayesian priors:** Should we use Bayesian updates with priors (e.g., "start with factor=1.0, confidence=3 samples"), or simple rolling average?

   **Recommendation:** Start with simple rolling average (easier to debug, explain). Add Bayesian in Phase 2 if needed.

4. **Response file parsing:** Should we parse ALL response files on first run (slow, 247 files), or only parse new ones incrementally?

   **Recommendation:** Bulk import on first run (one-time cost), then incremental import via `import-actuals` (checks `completed_at` != NULL to skip already-imported).

5. **CLI tool location:** Should this be a new `_tools/estimates.py`, or extend `_tools/inventory.py estimates <subcommand>`?

   **Recommendation:** New `_tools/estimates.py` (keeps inventory.py focused on features/bugs/backlog, estimates is orthogonal).

## Success Metrics

**After Phase 1 (4 tasks complete):**
- ✓ All 66 Mobile Workdesk tasks imported to `inv_estimates`
- ✓ 12+ completed tasks have actuals recorded (from response files or build monitor)
- ✓ Calibration factors computed for spec, build, test, verify, css
- ✓ Budget projection shows calibrated estimates (not just original)
- ✓ CLI commands work: `import-scheduler`, `import-actuals`, `calibration`, `compare`, `budget`

**After Phase 2 (in production use):**
- ✓ 50+ tasks completed with actuals → calibration factors stable (delta < 15%)
- ✓ Budget projections within 10% of actual completion time/cost/carbon
- ✓ Weekly trend shows improving accuracy (delta decreasing)
- ✓ Scheduler uses calibrated estimates (not original) for future builds

## Next Steps for Q33NR

**Action 1:** Review this design. Flag any concerns or missing requirements.

**Action 2:** Approve task breakdown (TASK-EST-01 through TASK-EST-04).

**Action 3:** If approved, I'll write the task files and queue them for bee dispatch.

**Action 4:** After bees complete, we'll have a working calibration ledger for the Mobile Workdesk build (and all future builds).

---

## Appendix: File Structure

```
shiftcenter/
├── hivenode/
│   ├── inventory/
│   │   ├── store.py                    [+50 lines: inv_estimates, inv_calibration tables]
│   │   └── __init__.py
│   ├── rate_loader/
│   │   └── model_rates.yml             [READ: token pricing]
│   └── scheduler/
│       └── scheduler_mobile_workdesk.py [READ: TASKS list for estimates]
├── _tools/
│   ├── inventory.py                     [UNCHANGED]
│   ├── inventory_db.py                  [+30 lines: import estimates store functions]
│   └── estimates.py                     [NEW: ~400 lines, CLI for estimation]
├── .deia/
│   ├── config/
│   │   └── carbon.yml                   [READ: carbon factors]
│   └── hive/
│       ├── responses/                   [READ: Clock/Cost/Carbon sections]
│       └── schedule.json                [READ: future integration]
└── tests/
    └── inventory/
        ├── test_estimates_schema.py     [NEW: TASK-EST-01]
        ├── test_estimates_import.py     [NEW: TASK-EST-02]
        ├── test_estimates_calibration.py [NEW: TASK-EST-03]
        └── test_estimates_integration.py [NEW: TASK-EST-04]
```

**Total new lines (estimate):**
- `hivenode/inventory/store.py`: +50 (tables + migration)
- `_tools/inventory_db.py`: +30 (imports)
- `_tools/estimates.py`: ~400 (CLI + logic)
- Tests: ~500 (4 test files × 125 lines avg)
- **Grand total:** ~980 new lines

No file exceeds 500 lines. Modular, testable, SQLAlchemy Core pattern maintained.

---

**End of Design Document**

**Status:** READY FOR Q33NR REVIEW → TASK FILE CREATION → BEE DISPATCH
