# SPEC-APPLY-CAP-01: Apply Unified Bee Capacity Config

## Priority
P1

## Model Assignment
haiku

## Depends On
None

## Intent
Verify and apply the code changes from SPEC-CAP-01 (Unified Bee Capacity). A bee already wrote the code — this spec verifies it works, runs the tests, and confirms the changes are correct. The bee added `_load_max_bees_from_config()` to dispatcher_daemon.py so it reads `max_parallel_bees` from queue.yml with hot-reload, CLI override, and 1-20 clamping.

## Files to Read First
.deia/hive/responses/20260406-SPEC-CAP-01-RESPONSE.md
hivenode/scheduler/dispatcher_daemon.py
hivenode/scheduler/tests/test_dispatcher_capacity_config.py
tests/hivenode/scheduler/test_dispatcher_daemon.py
.deia/config/queue.yml

## Acceptance Criteria
- [ ] `dispatcher_daemon.py` contains `_load_max_bees_from_config()` function
- [ ] Function reads `max_parallel_bees` from `.deia/config/queue.yml`
- [ ] `__init__` uses queue.yml by default, CLI arg overrides when explicitly set
- [ ] `_dispatch_cycle` hot-reloads max_bees from queue.yml each cycle
- [ ] All 19 tests in `test_dispatcher_capacity_config.py` pass
- [ ] All existing tests in `test_dispatcher_daemon.py` still pass
- [ ] No import errors or missing dependencies

## Constraints
- Do NOT modify any code. Verification only.
- If tests fail, document the failures in your response but do NOT attempt fixes.
- No git operations.

## Smoke Test
Run `python -m pytest hivenode/scheduler/tests/test_dispatcher_capacity_config.py -v` and verify 19 tests pass. Run `python -m pytest tests/hivenode/scheduler/test_dispatcher_daemon.py -v` and verify existing tests still pass.
