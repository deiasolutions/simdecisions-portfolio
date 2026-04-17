# TASK-EST-02: Data Collection (Import from Sources)

## Objective
Build `_tools/estimates.py` CLI with commands to import estimates from scheduler, actuals from build monitor, and Clock/Cost/Carbon data from response files, plus manual record/actual commands.

## Context
This is Phase 2 of the estimation calibration ledger system. After EST-01 created the schema, this task populates `inv_estimates` with data from three sources:
1. **Scheduler TASKS list** (original estimates)
2. **Build monitor API** (`GET /build/status` → actuals from tokens)
3. **Response files** (Clock/Cost/Carbon sections → actuals)

The CLI also provides manual `record` (new estimate) and `actual` (update actual) commands for one-off tasks or corrections.

**Design doc:** `.deia/hive/responses/20260406-BRIEFING-ESTIMATION-CALIBRATION-LEDGER-RESPONSE.md`

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\inventory\store.py`
  Schema definitions for inv_estimates (EST-01 created this).
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory.py`
  Example CLI structure (argparse, subcommands, database connection).
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\scheduler\scheduler_mobile_workdesk.py`
  Source of estimates (TASKS list with duration_hours, task_type, description).
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rate_loader\__init__.py`
  Token pricing (get_rate() function).
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\carbon.yml`
  Carbon factors (model_energy, region_intensity).
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260406-BRIEFING-ESTIMATION-CALIBRATION-LEDGER-RESPONSE.md`
  Full design doc with data sources, algorithms, CLI command specs.

## Deliverables
- [ ] `_tools/estimates.py` CLI script with argparse (commands: import-scheduler, import-actuals, import-responses, record, actual)
- [ ] `import-scheduler <path>` command:
  - Parse scheduler_mobile_workdesk.py TASKS list (or any scheduler file)
  - Extract: task_id (Task.id), task_type (Task.task_type), est_hours (Task.duration_hours), phase (from description)
  - Derive model: haiku for spec/test, sonnet for build/verify/css
  - Derive est_cost_usd: use expected turns × tokens × rate_loader.get_rate()
  - Derive est_carbon_g: use carbon.yml model_energy + region_intensity
  - Insert into inv_estimates (original estimates only, calibrated_* and actual_* are NULL)
- [ ] `import-actuals` command:
  - Fetch `GET http://127.0.0.1:8420/build/status`
  - For each task in `completed[]`: extract task_id, input_tokens, output_tokens, model, started_at, completed_at
  - Compute actual_cost_usd: (input_tokens / 1M) × rate["input"] + (output_tokens / 1M) × rate["output"]
  - Compute actual_carbon_g: tokens → energy (carbon.yml) → CO2e
  - Compute actual_hours: (completed_at - started_at).total_seconds() / 3600
  - Update inv_estimates (actual_hours, actual_cost_usd, actual_carbon_g, started_at, completed_at)
- [ ] `import-responses <dir>` command:
  - Scan `.deia/hive/responses/*-RESPONSE.md` files
  - Parse task_id from filename (e.g., "20260406-TASK-MW-031-RESPONSE.md" → "MW-031")
  - Parse Clock/Cost/Carbon section: `**Clock:** X hours`, `**Cost:** $Y USD`, `**Carbon:** Zg CO2e`
  - Update inv_estimates with parsed values (response file data overrides build monitor data if present)
- [ ] `record <task_id>` command:
  - Manual estimate recording: `--est-hours`, `--est-cost`, `--est-carbon`, `--type`, `--model`, `--phase`
  - Insert into inv_estimates
- [ ] `actual <task_id>` command:
  - Manual actual recording: `--actual-hours`, `--actual-cost`, `--actual-carbon`, `--completed-at`
  - Update inv_estimates
- [ ] Token→cost conversion via `hivenode/rate_loader.get_rate(model_id)`
- [ ] Token→carbon conversion via `.deia/config/carbon.yml` (model_energy × region_intensity)
- [ ] Fallback logic: if response file has complete Clock/Cost/Carbon, use it; else compute from build monitor; else mark incomplete (NULL)
- [ ] All commands use Railway PostgreSQL (via hivenode/inventory/store.py init_engine())

## Algorithm Details

### Cost Derivation (from scheduler estimates)

**Model assignment:**
```python
model_map = {
    "spec": "haiku",
    "test": "haiku",
    "build": "sonnet",
    "verify": "sonnet",
    "css": "sonnet",
}
model = model_map.get(task_type, "haiku")
```

**Expected token usage:**
```python
# Haiku tasks: 10 turns, 3k in + 1.5k out per turn
expected_turns_haiku = 10
tokens_in_haiku = 10 * 3000 = 30_000
tokens_out_haiku = 10 * 1500 = 15_000

# Sonnet tasks: 15 turns, 5k in + 2.5k out per turn
expected_turns_sonnet = 15
tokens_in_sonnet = 15 * 5000 = 75_000
tokens_out_sonnet = 15 * 2500 = 37_500
```

**Cost calculation:**
```python
from hivenode.rate_loader import get_rate

rate = get_rate(model_id)  # e.g., "claude-sonnet-4-5-20250929"
est_cost_usd = (
    (tokens_in / 1_000_000) * rate["input_per_million"] +
    (tokens_out / 1_000_000) * rate["output_per_million"]
)
```

### Carbon Derivation (from carbon.yml)

```python
import yaml

with open(".deia/config/carbon.yml") as f:
    carbon_yml = yaml.safe_load(f)

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

### Response File Parsing

**Filename → task_id:**
```python
# "20260406-TASK-MW-031-RESPONSE.md" → "MW-031"
# "20260406-MW-031-RESPONSE.md" → "MW-031"
import re
match = re.search(r'(MW-\d+|SPEC-[A-Z0-9-]+|TASK-[A-Z0-9-]+)', filename)
task_id = match.group(1) if match else None
```

**Clock/Cost/Carbon section:**
```python
# Parse lines like:
# - **Clock:** 2.5 hours
# - **Cost:** $0.42 USD
# - **Carbon:** 150g CO2e

clock_match = re.search(r'\*\*Clock:\*\*\s*([\d.]+)\s*hours?', content, re.IGNORECASE)
cost_match = re.search(r'\*\*Cost:\*\*\s*\$([\d.]+)', content, re.IGNORECASE)
carbon_match = re.search(r'\*\*Carbon:\*\*\s*([\d.]+)g?\s*CO2e?', content, re.IGNORECASE)

actual_hours = float(clock_match.group(1)) if clock_match else None
actual_cost_usd = float(cost_match.group(1)) if cost_match else None
actual_carbon_g = float(carbon_match.group(1)) if carbon_match else None
```

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass (`python -m pytest tests/hivenode/inventory/test_estimates_import.py -v`)
- [ ] Edge cases:
  - Scheduler file not found (graceful error)
  - Build monitor unreachable (connection error handling)
  - Response file with incomplete Clock/Cost/Carbon (partial import)
  - Response file with no task_id match (skip, log warning)
  - Duplicate task_id import (update existing row, not insert)
  - Manual commands with missing required args (argparse error)

## Test Coverage (minimum 12 tests)
Create `tests/hivenode/inventory/test_estimates_import.py` with:
1. `test_import_scheduler_parses_tasks()` — import 8 tasks, verify est_hours/cost/carbon
2. `test_import_scheduler_derives_model()` — spec→haiku, build→sonnet
3. `test_import_scheduler_computes_cost()` — verify rate_loader integration
4. `test_import_scheduler_computes_carbon()` — verify carbon.yml integration
5. `test_import_actuals_fetches_build_status()` — mock httpx response, verify actuals updated
6. `test_import_actuals_computes_cost_from_tokens()` — verify token→USD conversion
7. `test_import_actuals_computes_hours()` — verify (completed_at - started_at) / 3600
8. `test_import_responses_parses_clock_cost_carbon()` — parse sample response file
9. `test_import_responses_extracts_task_id()` — filename → task_id
10. `test_import_responses_handles_incomplete_sections()` — partial data, no crash
11. `test_record_inserts_new_estimate()` — manual record command
12. `test_actual_updates_existing_estimate()` — manual actual command
13. `test_import_responses_overrides_build_monitor()` — response file takes precedence
14. `test_import_scheduler_handles_missing_file()` — graceful error

## Constraints
- No file over 500 lines (split into `estimates.py` + `estimates_db.py` if needed)
- CSS: var(--sd-*) only (N/A for this task)
- No stubs (all functions fully implemented)
- Use argparse for CLI (match inventory.py pattern)
- Use httpx (not requests) for build monitor API
- Use yaml.safe_load() for carbon.yml
- Handle missing files/keys gracefully (no crashes, log warnings)

## Acceptance Criteria
- [ ] `estimates.py import-scheduler <path>` imports all TASKS, derives cost/carbon, writes to inv_estimates
- [ ] `estimates.py import-actuals` fetches build monitor status, updates actuals for completed tasks
- [ ] `estimates.py import-responses <dir>` parses response files, extracts Clock/Cost/Carbon, updates actuals
- [ ] `estimates.py record <task_id> --est-hours X --est-cost Y --est-carbon Z --type build --model sonnet` inserts row
- [ ] `estimates.py actual <task_id> --actual-hours X --actual-cost Y --actual-carbon Z --completed-at <ISO8601>` updates row
- [ ] Cost derivation uses rate_loader.get_rate() with correct model IDs (claude-sonnet-4-5-20250929, claude-haiku-4-5-20251001)
- [ ] Carbon derivation uses carbon.yml model_energy + region_intensity
- [ ] Response file parsing handles all 3 filename formats: "YYYYMMDD-TASK-ID-RESPONSE.md", "YYYYMMDD-ID-RESPONSE.md", "YYYYMMDD-SPEC-ID-RESPONSE.md"
- [ ] Tests: 14+ tests covering all import paths, rate_loader integration, carbon.yml integration, manual commands
- [ ] Handles missing files gracefully (no crashes, clear error messages)
- [ ] All tests pass: `python -m pytest tests/hivenode/inventory/test_estimates_import.py -v`

## Smoke Test
```bash
# Import estimates from scheduler
python _tools/estimates.py import-scheduler hivenode/scheduler/scheduler_mobile_workdesk.py

# Expected output:
# Imported 66 tasks from scheduler
# - 8 spec tasks (haiku, avg 2.5h, $0.10, 4500g CO2)
# - 8 test tasks (haiku, avg 3.5h, $0.14, 6300g CO2)
# - 42 build tasks (sonnet, avg 6.0h, $0.79, 158g CO2)
# - 8 verify tasks (sonnet, avg 2.0h, $0.26, 52g CO2)

# Import actuals from build monitor
python _tools/estimates.py import-actuals

# Import actuals from response files (bulk backfill)
python _tools/estimates.py import-responses .deia/hive/responses/

# Manual record
python _tools/estimates.py record TEST-001 --est-hours 2.0 --est-cost 0.08 --est-carbon 4500 --type test --model haiku

# Manual actual
python _tools/estimates.py actual TEST-001 --actual-hours 2.2 --actual-cost 0.09 --actual-carbon 4950 --completed-at "2026-04-06T12:00:00Z"
```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260406-TASK-EST-02-RESPONSE.md`

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
