# TASK-SD-FIX-01: Fix Dispatcher Filename Prefix Matching

## Objective
Fix the dispatcher's spec file lookup to match on task_id prefix rather than exact filename, supporting multiple naming conventions: `SPEC-{ID}.md`, `SPEC-{ID}-{description}.md`, and `2026-MM-DD-SPEC-{ID}-{description}.md`.

## Context
The dispatcher daemon currently looks for exact filename matches (`SPEC-{task_id}.md`) but actual spec files in backlog/ use descriptive names like `SPEC-MW-S01-command-interpreter.md`. This causes the dispatcher to skip tasks with "spec_not_found" errors.

**Dispatcher log evidence:**
```json
{"event": "spec_not_found", "task_id": "MW-S01", "expected_file": "SPEC-MW-S01.md"}
```

**Actual backlog files:**
- `SPEC-MW-S01-command-interpreter.md`
- `SPEC-MW-S02-voice-input.md`
- `SPEC-MW-S03-quick-actions.md`

The `_find_spec_file()` method (line 256) exists but only does case-insensitive exact match, not prefix matching.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\scheduler\dispatcher_daemon.py`
  Lines 256-284 contain the current `_find_spec_file()` implementation
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\scheduler\test_dispatcher_daemon.py`
  Existing tests that need to be updated

## Deliverables
- [ ] Update `_find_spec_file()` method to match on task_id prefix using glob patterns
- [ ] Support all three naming conventions:
  - `SPEC-{ID}.md` (short form)
  - `SPEC-{ID}-{description}.md` (long form)
  - `2026-MM-DD-SPEC-{ID}-{description}.md` (dated form)
- [ ] When multiple matches exist, log a warning and take the first alphabetically
- [ ] Update existing tests that test file matching behavior
- [ ] Add new test: `test_dispatcher_prefix_matching_with_description()`
- [ ] Add new test: `test_dispatcher_dated_prefix_matching()`
- [ ] Add new test: `test_dispatcher_multiple_matches_logs_warning()`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing dispatcher tests still pass
- [ ] New tests pass
- [ ] Edge cases covered:
  - Task ID "MW-S01" matches "SPEC-MW-S01-command-interpreter.md"
  - Task ID "MW-S01" matches "2026-04-05-SPEC-MW-S01-command-interpreter.md"
  - Multiple matches (e.g., both "SPEC-MW-S01.md" and "SPEC-MW-S01-v2.md" exist) → log warning, take first
  - No match → existing "spec_not_found" behavior preserved
  - Case-insensitive matching still works (MW-S01 matches SPEC-mw-s01.md)

## Constraints
- No file over 500 lines
- TDD: write failing tests first, then fix implementation
- No stubs
- Preserve existing case-insensitive matching behavior
- Do not break existing test suite
- The method should prefer exact matches over prefix matches (e.g., if both `SPEC-MW-S01.md` and `SPEC-MW-S01-v2.md` exist, prefer the exact match)

## Implementation Notes
The fix should modify `_find_spec_file()` to:
1. Try exact match first (existing behavior)
2. If no exact match, glob for `SPEC-{task_id}*.md` in backlog/
3. If still no match, glob for `*SPEC-{task_id}*.md` (dated form)
4. If multiple matches, log warning to dispatcher_log.jsonl and take first alphabetically
5. Return None if no matches (existing behavior)

Example glob patterns:
```python
# Try exact match first
exact = backlog_dir / f"SPEC-{task_id}.md"
if exact.exists():
    return exact

# Try standard prefix match
matches = sorted(backlog_dir.glob(f"SPEC-{task_id}-*.md"))
if matches:
    if len(matches) > 1:
        # Log warning
        pass
    return matches[0]

# Try dated prefix match
matches = sorted(backlog_dir.glob(f"*-SPEC-{task_id}-*.md"))
if matches:
    if len(matches) > 1:
        # Log warning
        pass
    return matches[0]

return None
```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260405-TASK-SD-FIX-01-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — platform-populated from build monitor telemetry (do not estimate manually)
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
