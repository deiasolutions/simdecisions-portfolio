# SPEC: Estimation Calibration — Data Collection CLI

## Priority
P1

## Depends On
EST-01

## Objective
Build `_tools/estimates.py` CLI with commands to import estimates from scheduler, actuals from build monitor, and Clock/Cost/Carbon data from response files, plus manual record/actual commands.

## Context
Phase 2 of the estimation calibration ledger. After EST-01 created the schema (`inv_estimates`, `inv_calibration`), this task populates data from three sources:
1. Scheduler TASKS list (original estimates)
2. Build monitor API (`GET /build/status` → actuals from tokens)
3. Response files (Clock/Cost/Carbon sections → actuals)

Design doc: `.deia/hive/responses/20260406-BRIEFING-ESTIMATION-CALIBRATION-LEDGER-RESPONSE.md`
Task file: `.deia/hive/tasks/2026-04-06-TASK-EST-02-data-collection.md`

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/inventory/store.py` — inv_estimates schema (EST-01)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/_tools/inventory.py` — CLI pattern (argparse)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py` — TASKS list
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/rate_loader/__init__.py` — get_rate()
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/config/carbon.yml` — carbon factors
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/tasks/2026-04-06-TASK-EST-02-data-collection.md` — full task spec with algorithm code

## Acceptance Criteria
- [ ] `estimates.py import-scheduler <path>` imports all TASKS, derives cost/carbon, writes to inv_estimates
- [ ] `estimates.py import-actuals` fetches build monitor status, updates actuals for completed tasks
- [ ] `estimates.py import-responses <dir>` parses response files, extracts Clock/Cost/Carbon, updates actuals
- [ ] `estimates.py record <task_id> --est-hours X --est-cost Y --est-carbon Z --type build --model sonnet` inserts row
- [ ] `estimates.py actual <task_id> --actual-hours X --actual-cost Y --actual-carbon Z` updates row
- [ ] Cost derivation uses rate_loader.get_rate() with correct model IDs
- [ ] Carbon derivation uses carbon.yml model_energy + region_intensity
- [ ] Response file parsing handles multiple filename formats
- [ ] 14+ tests covering all import paths, rate_loader, carbon.yml, manual commands
- [ ] Handles missing files gracefully (no crashes, clear error messages)
- [ ] All tests pass: `python -m pytest tests/hivenode/inventory/test_estimates_import.py -v`

## Smoke Test
- [ ] `python _tools/estimates.py import-scheduler hivenode/scheduler/scheduler_mobile_workdesk.py` imports tasks
- [ ] `python _tools/estimates.py import-actuals` fetches from build monitor
- [ ] `python _tools/estimates.py import-responses .deia/hive/responses/` parses response files
- [ ] `python _tools/estimates.py record TEST-001 --est-hours 2.0 --est-cost 0.08 --est-carbon 4500 --type test --model haiku`
- [ ] `python _tools/estimates.py actual TEST-001 --actual-hours 2.2 --actual-cost 0.09 --actual-carbon 4950`

## Model Assignment
sonnet

## Constraints
- No file over 500 lines (split into estimates.py + estimates_db.py if needed)
- No stubs — all functions fully implemented
- Use argparse for CLI (match inventory.py pattern)
- Use httpx (not requests) for build monitor API
- Use yaml.safe_load() for carbon.yml
- TDD — tests first
- Response file: `.deia/hive/responses/20260406-TASK-EST-02-RESPONSE.md`
