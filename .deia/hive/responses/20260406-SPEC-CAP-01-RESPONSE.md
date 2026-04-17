# SPEC-CAP-01: Unified Bee Capacity from queue.yml -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku
**Date:** 2026-04-06

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\scheduler\dispatcher_daemon.py` (added `_load_max_bees_from_config()`, updated `__init__` and `_dispatch_cycle`, added `import yaml`)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\scheduler\test_dispatcher_daemon.py` (updated fixture to create queue.yml, fixed 3 tests to use config helper, added `mcp_enabled=False` to avoid port conflicts)

## Files Created

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\scheduler\tests\test_dispatcher_capacity_config.py` (19 tests, 446 lines)

## What Was Done

- Added `_load_max_bees_from_config()` function to `dispatcher_daemon.py` that reads `max_parallel_bees` from `.deia/config/queue.yml`
- Function matches scheduler's `_load_bee_constraints()` pattern: tries relative path from queue_dir, defaults to 10 if missing, clamps to 1-20 range
- Updated `DispatcherDaemon.__init__()` to read from queue.yml by default, with CLI override when explicitly set (not default value)
- Updated `_dispatch_cycle()` to hot-reload max_bees from queue.yml on each cycle (live updates within 30-60s)
- Added `import yaml` to dispatcher module
- Created comprehensive test suite with 19 tests covering:
  - Unit tests for `_load_max_bees_from_config()` (reads yml, defaults, clamps, handles errors)
  - Integration tests for `__init__` (reads config, CLI override, fallback)
  - Hot reload tests for `_dispatch_cycle()` (re-reads config, uses new value)
  - Daemon loop tests (hot-reloads while running)
  - Edge cases (missing budget section, non-integer values, CLI override)
  - All 7 acceptance criteria

## Tests Added

19 pytest tests in `test_dispatcher_capacity_config.py`:

- `test_load_max_bees_from_config_reads_queue_yml` — reads max_parallel_bees from queue.yml
- `test_load_max_bees_from_config_defaults_to_10_if_missing` — returns 10 if config missing
- `test_load_max_bees_from_config_clamps_to_1_20_range` — clamps to 1-20 range
- `test_load_max_bees_from_config_handles_malformed_yaml` — handles malformed yaml
- `test_dispatcher_init_reads_from_queue_yml_by_default` — uses queue.yml by default
- `test_dispatcher_init_cli_override_wins_if_not_default` — CLI override works
- `test_dispatcher_init_falls_back_to_10_if_no_config` — fallback to 10
- `test_dispatch_cycle_hot_reloads_max_bees` — hot reload on each cycle
- `test_dispatch_cycle_uses_hot_reloaded_capacity` — uses new value for slot calculation
- `test_dispatcher_daemon_hot_reloads_during_loop` — hot reload while daemon running
- `test_dispatcher_handles_missing_budget_section` — handles missing budget section
- `test_dispatcher_handles_non_integer_max_bees` — casts non-integer to int
- `test_dispatcher_cli_override_still_works` — CLI arg still works as override
- `test_acceptance_dispatcher_reads_queue_yml` — AC: reads queue.yml
- `test_acceptance_cli_override_works` — AC: CLI override works
- `test_acceptance_hot_reload_works` — AC: hot reload works
- `test_acceptance_missing_config_defaults_to_10` — AC: defaults to 10
- `test_acceptance_clamped_to_1_20` — AC: clamped to 1-20
- `test_acceptance_no_changes_to_other_consumers` — AC: other consumers unchanged

All tests pass.

## Test Results

New tests (test_dispatcher_capacity_config.py):
```
19 passed in 3.13s
```

Existing tests (test_dispatcher_daemon.py):
```
24 passed, 23 warnings in 1.52s
```

**Total: 43 tests pass** (19 new + 24 existing)

## Smoke Tests

✅ Dispatcher reads queue.yml value (15) without CLI override
✅ CLI override (--max-bees 7) takes precedence
✅ Falls back to 10 if queue.yml missing
✅ Hot reload works (changed from 10 → 18 during runtime)
✅ Scheduler's `_load_bee_constraints()` still works (no changes)

## Acceptance Criteria

- [x] Dispatcher reads `max_parallel_bees` from `.deia/config/queue.yml`
- [x] CLI `--max-bees` overrides queue.yml when explicitly provided (not default)
- [x] Dispatcher re-reads queue.yml on each cycle (hot reload)
- [x] If queue.yml is missing or malformed, defaults to 10
- [x] Value clamped to 1-20 range
- [x] Existing `--max-bees` CLI arg still works as override
- [x] No changes to scheduler, queue runner, or build monitor

## Pattern Match

Implementation matches scheduler's `_load_bee_constraints()` pattern:

| Feature | Scheduler | Dispatcher |
|---------|-----------|------------|
| Config path | `queue_dir.parent.parent / "config" / "queue.yml"` | ✓ Same |
| Default value | 10 | ✓ Same |
| Clamping | 1-20 | ✓ Same |
| Error handling | Return defaults | ✓ Same |
| Hot reload | Every cycle | ✓ Same |

## Notes

- Pattern is consistent across all 4 consumers (queue runner, scheduler, build monitor, dispatcher)
- CLI `--max-bees` arg behavior unchanged (still works as override)
- Hot reload enables live capacity adjustments without restarting daemons
- Tests use pytest fixtures to create isolated tmp directories with queue.yml
- Edge cases covered: missing config, malformed yaml, non-integer values, missing budget section
