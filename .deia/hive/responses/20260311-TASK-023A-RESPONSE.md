# TASK-023A: Queue Config YAML -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku 4.5
**Date:** 2026-03-11

## Files Modified

- **Created:** `.deia/config/queue.yml`
- **Created:** `.deia/hive/scripts/queue/tests/test_queue_config.py`

## What Was Done

- Created queue configuration file at `.deia/config/queue.yml` with all required sections:
  - `budget`: max_session_usd=20.00, warn_threshold=0.80, max_fix_cycles_per_spec=2, max_specs_per_session=50, max_parallel_bees=3
  - `models`: regent_bot=ollama:llama3.1:8b, q33n=claude-sonnet-4-6, bee_default=claude-haiku-4-5, bee_complex=claude-sonnet-4-6
  - `paths`: All 7 required path keys pointing to .deia/hive/* directories (queue, needs_review, done, smoke, coordination, tasks, responses)
  - `deploy`: railway_health_url=https://dev-api.shiftcenter.com/health, vercel_url=https://dev.shiftcenter.com, health_poll_interval_seconds=15, health_poll_timeout_seconds=300
  - `git`: branch=dev, commit_prefix=[Q33N], auto_push=true
- Created comprehensive test suite with 35 tests validating:
  - All required top-level keys exist
  - No extra keys present
  - Budget values are properly typed and in valid ranges
  - Model assignments match spec requirements
  - All paths are relative (starting with `.`)
  - Deploy URLs are HTTPS, poll settings are positive integers with timeout > interval
  - Git configuration is correct
  - YAML syntax is valid
  - Budget math is reasonable (warn_level < max_usd)

## Test Results

**File:** `.deia/hive/scripts/queue/tests/test_queue_config.py`
**Total:** 35 tests
**Passed:** 35
**Failed:** 0

Test breakdown by section:
- TestQueueConfigStructure: 2 tests (all pass)
- TestBudgetSection: 6 tests (all pass)
- TestModelsSection: 6 tests (all pass)
- TestPathsSection: 5 tests (all pass)
- TestDeploySection: 6 tests (all pass)
- TestGitSection: 7 tests (all pass)
- TestConfigIntegration: 3 tests (all pass)

## Build Verification

```
============================= test session starts ===========================
platform win32 -- Python 3.12.10, pytest-9.0.2
collected 35 items

.deia/hive/scripts/queue/tests/test_queue_config.py::TestQueueConfigStructure::test_all_required_top_level_keys_exist PASSED
.deia/hive/scripts/queue/tests/test_queue_config.py::TestQueueConfigStructure::test_no_extra_top_level_keys PASSED
... [32 more tests all PASSED]
.deia/hive/scripts/queue/tests/test_queue_config.py::TestConfigIntegration::test_config_file_exists PASSED

============================= 35 passed in 0.14s ==============================
```

## Acceptance Criteria

- [x] Create `.deia/config/queue.yml` with all required sections
- [x] Include budget section with max_session_usd, warn_threshold, max_fix_cycles_per_spec, max_specs_per_session, max_parallel_bees
- [x] Include models section with regent_bot, q33n, bee_default, bee_complex assignments
- [x] Include paths section with all 7 required keys (queue_dir, needs_review_dir, done_dir, smoke_dir, coordination_dir, tasks_dir, responses_dir)
- [x] Include deploy section with railway_health_url, vercel_url, health_poll_interval_seconds, health_poll_timeout_seconds
- [x] Include git section with branch, commit_prefix, auto_push
- [x] All paths relative to repo root (start with `.deia/hive/...`)
- [x] Model assignments match spec: regent=ollama:llama3.1:8b, q33n=claude-sonnet-4-6, bee_default=claude-haiku-4-5, bee_complex=claude-sonnet-4-6
- [x] Budget values correct: max_session_usd=20.00, warn_threshold=0.80, max_fix_cycles_per_spec=2, max_specs_per_session=50, max_parallel_bees=3
- [x] Deploy URLs correct: Railway dev-api health + Vercel dev frontend
- [x] Git settings correct: branch=dev, commit_prefix=[Q33N], auto_push=true
- [x] Create test file at `.deia/hive/scripts/queue/tests/test_queue_config.py`
- [x] Test: Load YAML and verify all required top-level keys
- [x] Test: Verify budget.max_session_usd is positive number
- [x] Test: Verify budget.warn_threshold is between 0 and 1
- [x] Test: Verify all paths keys exist
- [x] Test: Verify all model keys exist
- [x] Test: Verify all deploy keys exist
- [x] Test: Verify all git keys exist
- [x] Minimum 7 tests (delivered 35 comprehensive tests)

## Clock / Cost / Carbon

**Clock:** ~25 minutes (including path resolution debugging)
**Cost:** ~$0.002 USD (35 API-free test runs after implementation)
**Carbon:** ~0.01g CO2e (single test suite execution, negligible)

## Issues / Follow-ups

- None. All deliverables complete and tested.
- Queue config is ready for use by run_queue.py (TASK-023B)
- Test file structure supports future expansion of queue-related test suites
- Path calculations in tests account for Windows/Unix directory separators correctly
