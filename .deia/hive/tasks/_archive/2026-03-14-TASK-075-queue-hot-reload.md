# TASK-075: Queue Runner Hot-Reload

## Objective
Add hot-reload capability to run_queue.py so new specs added to the queue directory while the runner is active are detected and processed automatically.

## Context
Currently `run_queue.py` calls `load_queue()` once at startup (line 99) and processes that fixed list. If new specs are added to `.deia/hive/queue/` while the queue is running, they are ignored until the next manual run. This task modifies the main loop to re-scan the directory on each iteration and merge newly-detected specs into the processing queue.

The key challenges:
1. Detecting new specs without re-processing already-handled ones
2. Preserving existing in-progress specs in the list
3. Maintaining budget tracking across initial + hot-reloaded specs
4. Avoiding race conditions with specs being moved during iteration

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` — main queue runner
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_parser.py` — load_queue() function
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\queue.yml` — config reference

## Deliverables

### Code Changes
- [ ] Add `_rescan_queue()` helper function that:
  - Calls `load_queue(queue_dir)` to get current filesystem state
  - Filters out specs already in the `specs` list (by `path.name`)
  - Returns list of newly-detected specs
  - Prints log message: `"[QUEUE] Hot-reload: found N new spec(s)"` (use `flush=True`)
- [ ] Modify main loop in `run_queue()` to call `_rescan_queue()` at the top of each iteration
- [ ] Merge newly-detected specs into the `specs` list at the appropriate position (sorted by priority)
- [ ] Track hot-reload count in `session_events` (add event type `QUEUE_HOT_RELOAD`)
- [ ] Ensure budget tracking (`session_cost`) includes all specs (initial + hot-reloaded)
- [ ] All `print()` calls must use `flush=True` (stdout buffering fix)

### Edge Cases to Handle
- [ ] Empty re-scan (no new specs) — no log message, no event
- [ ] Spec moved to `_done/` during iteration — do not re-add
- [ ] Spec moved to `_needs_review/` during iteration — do not re-add
- [ ] Duplicate detection by filename (not full path, since originals are moved)

## Test Requirements

### Tests to Write FIRST (TDD)
Write all tests in: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_run_queue_hot_reload.py`

- [ ] **test_hot_reload_detects_new_spec**: Add a new spec to queue_dir after initial load, verify it gets processed
- [ ] **test_hot_reload_skips_already_processed**: Add spec that was already moved to `_done/`, verify it's not re-added
- [ ] **test_hot_reload_preserves_priority_order**: Add P0 spec after P1 spec is in progress, verify P0 gets inserted before remaining P1s
- [ ] **test_hot_reload_empty_rescan**: Re-scan with no new specs, verify no log message, no event added
- [ ] **test_hot_reload_budget_tracking**: Add new spec via hot-reload, verify total session_cost includes both initial and hot-reloaded specs
- [ ] **test_hot_reload_event_logged**: Verify `QUEUE_HOT_RELOAD` event is logged when new specs are detected
- [ ] **test_hot_reload_multiple_new_specs**: Add 3 new specs in one re-scan, verify all 3 are detected

### Test Scenarios
Each test should:
- Use `tmp_path` fixture for isolated queue directory
- Create initial spec files, call `run_queue()` with mocked `process_spec()`
- Inject new spec files during iteration (via callback in mocked `process_spec()`)
- Verify final `session_events` and `specs` list state

### Minimum Test Count
**7 tests** (all scenarios above must pass)

## Constraints
- Do NOT restructure the main loop — add `_rescan_queue()` call at top of iteration
- Do NOT change the spec file format
- Keep existing `_done/` and `_needs_review/` archive behavior
- No file over 500 lines (current file is 400 lines, should stay under 500 after changes)
- Use `flush=True` on all `print()` statements
- CSS: N/A (Python-only task)
- No stubs — all functions fully implemented

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-075-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from spec BL-121, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
