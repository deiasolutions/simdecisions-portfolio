# TASK-SCHED-COMPLETION-FIX: Fix scheduler completion detection

**Bot ID:** QUEEN-2026-04-06-BRIEFING-SCHEDULER-
**Date:** 2026-04-06
**Priority:** P0

## Objective

Fix the scheduler daemon's completion detection logic to correctly identify completed tasks by matching spec filenames in `_done/` to task IDs using prefix matching.

## Context

The scheduler daemon reads `_done/` to determine which tasks have completed. Currently it's extracting task IDs incorrectly:
- **Filename:** `SPEC-MW-031-menu-bar-drawer.md`
- **What it extracts:** `MW-031-menu-bar-drawer` (wrong)
- **Task ID in schedule:** `MW-031` (correct)
- **Result:** No match, scheduler never sees completion

The dispatcher already solves this problem with `_find_spec_file()` in `dispatcher_daemon.py` (lines 260-330). The scheduler needs the same logic but in reverse: given a spec filename, extract the task ID.

After 19 tasks completed overnight, the scheduler still reports all 66 tasks with unchanged makespan because it's not detecting any completions.

## Files to Read First

- `hivenode/scheduler/scheduler_daemon.py` (lines 236-278 — the `compute_schedule()` method)
- `hivenode/scheduler/dispatcher_daemon.py` (lines 260-330 — the `_find_spec_file()` method for reference)
- `.deia/hive/queue/_done/SPEC-MW-031-menu-bar-drawer.md` (example completed spec)

## Root Cause

**Line 252 in `scheduler_daemon.py`:**

```python
done_specs = {f.stem.replace("SPEC-", "") for f in done_dir.glob("SPEC-*.md")}
```

This creates entries like `MW-031-menu-bar-drawer`, but task IDs are just `MW-031`. The `task.id in done_specs` check on line 262 never matches.

## Deliverables

- [ ] Add `_extract_task_id_from_spec()` method to `SchedulerDaemon` class
  - Input: spec filename (e.g., `SPEC-MW-031-menu-bar-drawer.md`)
  - Output: task ID (e.g., `MW-031`)
  - Support three formats:
    1. `SPEC-{ID}.md` → `{ID}`
    2. `SPEC-{ID}-{description}.md` → `{ID}` (extract prefix before second dash)
    3. Dated format: `{date}-SPEC-{ID}-{description}.md` → `{ID}`
  - Must handle edge cases like `MW-S01` (letter in ID) and `MW-033` (numeric)
- [ ] Update line 252 to use `_extract_task_id_from_spec()`
- [ ] After fix, scheduler detects all 19 completed MW tasks in `_done/`
- [ ] Scheduler recalculates schedule with reduced task count and makespan
- [ ] All scheduler tests pass

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] Add test file: `tests/hivenode/scheduler/test_scheduler_completion_detection.py`
- [ ] Test cases:
  - Extract task ID from `SPEC-MW-031-menu-bar-drawer.md` → `MW-031`
  - Extract task ID from `SPEC-MW-S01-command-interpreter.md` → `MW-S01`
  - Extract task ID from `SPEC-MW-033.md` → `MW-033`
  - Handle malformed filenames gracefully (return None, log warning)
  - Integration test: Scheduler detects completion when spec is in `_done/`
- [ ] Test against existing `_done/` files (19 MW specs should be detected)
- [ ] All tests pass

## Constraints

- No file over 500 lines
- Reuse the ID extraction pattern from dispatcher (but simpler, no file searching)
- Must work with all three naming conventions (exact, prefix, dated)
- Case-insensitive matching on task_id
- Must be backward compatible
- Log a warning if spec filename doesn't match expected pattern

## Implementation Notes

The task ID extraction logic should:
1. Remove file extension (`.md`)
2. Remove `SPEC-` prefix (or `{date}-SPEC-` for dated format)
3. Extract everything before the next dash (or end of string)
4. Uppercase for comparison

Example implementation:

```python
def _extract_task_id_from_spec(self, filename: str) -> Optional[str]:
    """Extract task ID from spec filename.

    Supports:
    - SPEC-MW-031.md → MW-031
    - SPEC-MW-031-menu-bar-drawer.md → MW-031
    - 2026-04-06-SPEC-MW-S01-command-interpreter.md → MW-S01

    Returns:
        Task ID (uppercase), or None if pattern not recognized
    """
    stem = Path(filename).stem  # Remove .md

    # Remove date prefix if present (YYYY-MM-DD- format)
    if re.match(r'^\d{4}-\d{2}-\d{2}-', stem):
        stem = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', stem)

    # Must start with SPEC-
    if not stem.upper().startswith("SPEC-"):
        logger.warning(f"Spec filename doesn't start with SPEC-: {filename}")
        return None

    # Remove SPEC- prefix
    rest = stem[5:]  # "MW-031-menu-bar-drawer" or "MW-031"

    # Extract task ID (everything before next dash, or whole string)
    # Need to handle IDs like MW-S01 (letter before number) and MW-031 (numeric)
    # Pattern: {prefix}-{id} where id may contain letters/numbers
    # Extract: {prefix}-{id} (without the description)

    # Split on dashes
    parts = rest.split('-')
    if len(parts) < 2:
        # Just "MW-031" format (already correct)
        return rest.upper()

    # Check if third part looks like a description (not part of ID)
    # IDs are: MW-S01, MW-031, MW-T01 (always {prefix}-{alphanumeric})
    # Descriptions are: menu-bar-drawer, command-interpreter (words)
    task_id = f"{parts[0]}-{parts[1]}"
    return task_id.upper()
```

## Acceptance Criteria

- [x] Scheduler daemon extracts task IDs correctly from all spec filename formats
- [x] Scheduler detects 19 completed MW specs in `_done/` on next cycle
- [x] Schedule output shows reduced task count (66 → 47) and lower makespan
- [x] All scheduler tests pass
- [x] Integration test verifies completion detection

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260406-TASK-SCHED-COMPLETION-FIX-RESPONSE.md`

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
