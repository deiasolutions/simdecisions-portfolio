# TASK-A: Fix Dispatcher Stale Slot Detection

## Objective
Fix the dispatcher daemon to correctly count only active (non-stale) specs in `_active/` directory by ignoring files that haven't been modified in the last 30 minutes.

## Context
**Problem:** The dispatcher uses `_count_specs_in(queue_dir / "_active")` which counts ALL spec files in `_active/`, including stale specs from crashed/restarted queue-runner sessions. This causes negative slot counts:

```json
{"event": "cycle_start", "active": 13, "queued": 1, "slots": -4, "max_bees": 10}
```

**Root cause:** Old specs sit in `_active/` indefinitely after queue-runner crashes. The dispatcher has no way to distinguish between truly running bees and stale files.

**Solution:** Use file modification time (mtime). If a spec in `_active/` hasn't been modified in 30+ minutes, it's stale and shouldn't count toward active slots.

**Why 30 minutes:** Queue runner updates spec files periodically (heartbeats, status). A bee that's actually running will touch its spec file. 30 minutes is long enough to avoid false positives during long-running tasks, but short enough to detect crashes quickly.

## Files to Read First
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/dispatcher_daemon.py` — current implementation
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/test_dispatcher.py` — existing tests (if any)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/responses/20260405-TASK-SD-02-RESPONSE.md` — original dispatcher implementation context

## Deliverables
- [ ] Modify `_count_specs_in()` method to accept optional `stale_threshold_minutes` parameter (default: 30)
- [ ] Add logic to check file mtime and exclude files older than threshold
- [ ] Update `_dispatch_cycle()` to pass stale threshold when counting active specs
- [ ] Add unit tests for stale detection (3+ test cases: fresh file, stale file, edge cases)
- [ ] Verify existing dispatcher tests still pass
- [ ] Add test case that simulates stale specs in `_active/` and verifies they're not counted

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing tests pass
- [ ] New tests cover:
  - Fresh spec (modified 5 minutes ago) — should count
  - Stale spec (modified 45 minutes ago) — should NOT count
  - Edge case: spec modified exactly 30 minutes ago — should NOT count (use >=)
  - Empty `_active/` directory — should return 0
  - `_active/` directory doesn't exist — should return 0

## Acceptance Criteria
- [ ] `_count_specs_in()` method signature: `_count_specs_in(directory: Path, pattern: str = "SPEC-*.md", stale_threshold_minutes: Optional[int] = None) -> int`
- [ ] If `stale_threshold_minutes` is None, count all files (backward compatible)
- [ ] If `stale_threshold_minutes` is set, only count files modified within threshold
- [ ] `_dispatch_cycle()` calls `_count_specs_in(self.active_dir, stale_threshold_minutes=30)`
- [ ] All existing dispatcher tests pass
- [ ] 3+ new tests pass for stale detection logic
- [ ] No hardcoded time values — use parameter

## Smoke Test
- Create test spec in `_active/` with mtime 45 minutes ago
- Run dispatcher
- Verify active count does NOT include the stale spec
- Verify log shows correct active count (excluding stale)
- Touch the spec file (update mtime to now)
- Run dispatcher again
- Verify active count now INCLUDES the fresh spec

## Constraints
- No file over 500 lines (dispatcher_daemon.py is 440 lines, should stay under)
- TDD: Write tests first
- No stubs
- Use `Path.stat().st_mtime` for file modification time
- Use `datetime.now(UTC)` for current time comparison
- All time comparisons in UTC
- Preserve existing behavior when `stale_threshold_minutes=None`

## Response Requirements — MANDATORY
When you finish your work, write a response file:
  `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/responses/20260405-TASK-A-DISPATCHER-STALE-FIX-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
