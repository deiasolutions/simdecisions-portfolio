# BRIEFING: Scheduler Completion Detection — DIAGNOSED

**From:** Q33N
**To:** Q33NR
**Date:** 2026-04-06
**Status:** TASK FILE READY FOR REVIEW

---

## Diagnosis Complete

Found the root cause. The scheduler daemon is not detecting completions because of a **task ID extraction bug** on line 252 of `scheduler_daemon.py`.

### The Bug

**Current code (line 252):**
```python
done_specs = {f.stem.replace("SPEC-", "") for f in done_dir.glob("SPEC-*.md")}
```

**What it produces:**
- Filename: `SPEC-MW-031-menu-bar-drawer.md`
- Stem: `SPEC-MW-031-menu-bar-drawer`
- After replace: `MW-031-menu-bar-drawer`
- Stored in set: `{"MW-031-menu-bar-drawer", ...}`

**What the schedule expects:**
- Task ID: `MW-031`

**Result:**
- `task.id in done_specs` → `"MW-031" in {"MW-031-menu-bar-drawer"}` → **False**
- Scheduler never sees any completions

### The Fix

Extract just the task ID from the spec filename, not the entire stem. This is the same problem the dispatcher had, and we fixed it in TASK-SD-02 with prefix matching in `_find_spec_file()`.

The scheduler needs the reverse operation:
- **Dispatcher:** task_id → find spec file in backlog/
- **Scheduler:** spec file in _done/ → extract task_id

### Evidence

**19 completed specs in `_done/`:**
```
SPEC-MW-023-text-pane-mobile-css.md
SPEC-MW-024-terminal-mobile-css.md
SPEC-MW-025-tree-browser-mobile-css.md
SPEC-MW-026-efemera-connector-mobile-css.md
SPEC-MW-027-settings-mobile-css.md
SPEC-MW-028-dashboard-mobile-css.md
SPEC-MW-029-progress-pane-polish.md
SPEC-MW-030-top-bar-mobile-css.md
SPEC-MW-031-menu-bar-drawer.md
SPEC-MW-032-status-bar-mobile-css.md
SPEC-MW-033-command-palette-mobile.md
SPEC-MW-034-tfidf-index.md
SPEC-MW-S01-command-interpreter.md
SPEC-MW-S02-voice-input.md
SPEC-MW-S03-quick-actions.md
SPEC-MW-S04-conversation-pane.md
SPEC-MW-S05-mobile-nav.md
SPEC-MW-S06-notification-pane.md
SPEC-MW-S07-queue-pane.md
```

**Task IDs in schedule.json:**
```
MW-023, MW-024, MW-025, ..., MW-034, MW-S01, MW-S02, ..., MW-S07
```

**Mismatch:** Scheduler looks for `MW-031-menu-bar-drawer` but should look for just `MW-031`.

### Current State

**Schedule stats (unchanged for hours):**
- 66 tasks
- 95h makespan
- All 19 root tasks showing status: `"unknown"`

**After fix, expected:**
- 47 tasks (66 - 19)
- ~75h makespan (reduced)
- Phase 0.5 tests (MW-T01 through MW-T08) should show status: `"ready"` and move from backlog/ to queue/

---

## Task File Written

**File:** `.deia/hive/tasks/2026-04-06-TASK-SCHED-COMPLETION-FIX.md`

**Deliverable:**
- Add `_extract_task_id_from_spec()` method to extract task ID from spec filename
- Support all three naming formats (exact, prefix, dated)
- Update line 252 to use the new method
- Tests for all edge cases
- Integration test with real `_done/` files

**Assigned model:** Sonnet (P0, critical path blocker)

**Test requirements:**
- Test file: `tests/hivenode/scheduler/test_scheduler_completion_detection.py`
- Test cases: exact match, prefix match, dated format, malformed names
- Integration test: scheduler detects all 19 completions

---

## Awaiting Q33NR Review

Ready to dispatch after you review the task file. This is the blocker for the entire dependency-blocked task wave (Phase 0.5 tests + Phase 1-7 builds).

Once this bee completes:
1. Scheduler will detect 19 completions
2. Schedule recalculates (66 → 47 tasks, 95h → ~75h)
3. Dispatcher sees 8 ready tasks (MW-T01 through MW-T08)
4. Dispatcher moves them from backlog/ to queue/
5. Queue-runner dispatches test-writing bees
6. Build pipeline unblocks

---

## Files Referenced

- **Scheduler daemon:** `hivenode/scheduler/scheduler_daemon.py` (line 252 — the bug)
- **Dispatcher daemon:** `hivenode/scheduler/dispatcher_daemon.py` (lines 260-330 — reference for ID extraction)
- **Task list:** `hivenode/scheduler/scheduler_mobile_workdesk.py` (task ID definitions)
- **Done directory:** `.deia/hive/queue/_done/` (19 completed specs)
- **Schedule state:** `.deia/hive/schedule.json` (shows 66 tasks, unchanged)
- **Dispatch log:** `.deia/hive/dispatched.jsonl` (5 dispatches, but no status updates)

---

## Recommendation

Approve task file and dispatch immediately. This is a 30-minute fix that unblocks the entire build pipeline.
