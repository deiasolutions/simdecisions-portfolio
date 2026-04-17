# Fix Hot Reload Tests (7 failing)

## Priority
P1

## Model Assignment
haiku

## Objective
Fix 7 failing hot reload tests. All fail with FileNotFoundError on fix spec path.

## What's Broken
- `test_hot_reload_detects_new_spec` — FileNotFoundError
- `test_hot_reload_skips_already_processed` — same
- `test_hot_reload_preserves_priority_order` — same
- `test_hot_reload_empty_rescan` — same
- `test_hot_reload_budget_tracking` — same
- `test_hot_reload_event_logged` — same
- `test_hot_reload_multiple_new_specs` — same

Pattern: Hot reload creates fix specs but doesn't write them to disk before trying to parse.

Reference: `.deia/hive/responses/20260318-FULL-TEST-SWEEP-REPORT.md` section "Hot reload tests (7)"

## Files to Read First
- `.deia/hive/scripts/queue/tests/` — find the hot reload test file
- `.deia/hive/scripts/queue/run_queue.py` — hot reload function

## What To Do
1. Find and read the hot reload test file
2. Run tests to see exact error
3. Fix the FileNotFoundError — likely test setup needs to create the fix spec file on disk
4. Confirm all 7 pass

## Response
Write response to: `.deia/hive/responses/20260318-FIX-HOT-RELOAD-TESTS.md`
