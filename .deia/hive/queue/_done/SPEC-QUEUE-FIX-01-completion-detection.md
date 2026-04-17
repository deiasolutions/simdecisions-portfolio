# SPEC-QUEUE-FIX-01: Fix Queue Runner Completion Detection

**Priority:** P1
**Complexity:** Haiku
**Estimate:** 30 minutes
**Dependencies:** None

---

## Problem

The queue runner does not recognize `ALREADY_COMPLETE` as a valid success status. When a bee reports that work was already done by a dependency, the queue runner:
1. Marks the task as failed
2. Generates a spurious fix spec
3. Dispatches another bee to "fix" a non-existent problem

This wastes bee cycles and pollutes the failed list. Confirmed by MW-T06 (notification pane tests already existed from MW-S06).

## Solution

Update `spec_processor.py` completion detection to treat `ALREADY_COMPLETE` and `NO_ACTION_NEEDED` as success statuses alongside `COMPLETE`.

---

## Implementation

### 1. Update completion detection in spec_processor.py

Find the response status parsing logic. Update it to recognize additional success statuses:

```python
SUCCESS_STATUSES = {"COMPLETE", "ALREADY_COMPLETE", "NO_ACTION_NEEDED"}

# In the completion check:
if status.upper() in SUCCESS_STATUSES:
    move_to_done()
```

### 2. Update filename filter (secondary fix)

The queue runner should reject files that don't match the `SPEC-*.md` pattern. Briefings and task files should never be executed:

```python
def is_valid_spec(filename: str) -> bool:
    """Only SPEC-*.md files are valid queue items."""
    return filename.startswith("SPEC-") and filename.endswith(".md")
```

## Files to Read First

- `.deia/hive/scripts/queue/spec_processor.py`
- `.deia/hive/scripts/queue/run_queue.py`

## Files to Modify

| File | Change |
|------|--------|
| `.deia/hive/scripts/queue/spec_processor.py` | Add SUCCESS_STATUSES set, update completion check |
| `.deia/hive/scripts/queue/run_queue.py` | Add `is_valid_spec()` filename filter before processing |

## Acceptance Criteria

- [ ] `ALREADY_COMPLETE` status moves spec to `_done/` (not `_failed`)
- [ ] `NO_ACTION_NEEDED` status moves spec to `_done/` (not `_failed`)
- [ ] `COMPLETE` status still works as before
- [ ] `FAILED` status still triggers fix cycle as before
- [ ] Non-SPEC files in queue/ are skipped with a warning log
- [ ] No fix spec is generated for ALREADY_COMPLETE items

## Smoke Test

- [ ] Place a mock spec in queue/ that will return ALREADY_COMPLETE
- [ ] Verify it ends up in `_done/`, not failed
- [ ] Place a file named `BRIEFING-test.md` in queue/ → verify it's skipped
- [ ] Existing COMPLETE/FAILED flow unchanged

## Model Assignment

haiku

## Constraints

- Do NOT change the response file format
- Do NOT change how bees report status
- Only change queue runner's interpretation of status
