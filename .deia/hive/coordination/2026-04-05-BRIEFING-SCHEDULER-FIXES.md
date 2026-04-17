# BRIEFING: Scheduler/Dispatcher Pipeline Fixes

**From:** Q33NR
**To:** Q33N
**Date:** 2026-04-05
**Priority:** P0 — pipeline is built but has a wiring bug, fix tonight

## Context

The scheduler_daemon.py + dispatcher_daemon.py pipeline was just built and tested. First live run revealed one bug and one housekeeping issue. Both need fixing before the pipeline can run unattended.

## Bug: Dispatcher Filename Mismatch

**What happens:** Dispatcher looks for `backlog/SPEC-{task_id}.md` (e.g., `SPEC-MW-S01.md`) but actual spec files in backlog are named `SPEC-{task_id}-{description}.md` (e.g., `SPEC-MW-S01-command-interpreter.md`).

**Dispatcher log evidence:**
```json
{"event": "spec_not_found", "task_id": "MW-S01", "expected_file": "SPEC-MW-S01.md"}
```

**Fix needed in:** `hivenode/scheduler/dispatcher_daemon.py`

The dispatcher's file lookup should match on task_id prefix, not exact name. When looking for task_id `MW-S01`, it should glob `backlog/SPEC-MW-S01*.md` and take the first match. If multiple matches, log a warning and take the first alphabetically.

**Also fix:** The dispatcher should handle the existing queue convention where spec files use various naming patterns:
- `SPEC-{ID}.md` (short form)
- `SPEC-{ID}-{description}.md` (long form)
- `2026-MM-DD-SPEC-{ID}-{description}.md` (dated form)

All should match on the task_id portion.

## Bug: Stale _done/ Spec Encoding

**What happens:** Scheduler logs warnings when parsing specs in `_done/`:
```
Failed to parse SPEC-CANVAS3-SVG-ICONS.md: 'charmap' codec can't decode byte 0x8f
Failed to parse SPEC-KB-001A-keyboard-primitive-core.md: 'charmap' codec can't decode byte 0x8f
```

**Fix needed in:** `hivenode/scheduler/scheduler_daemon.py`

When reading spec files in `_done/` for velocity updates, open with `encoding='utf-8', errors='replace'` instead of default encoding. These files may contain unicode characters (emoji, special chars from bee output).

## Deliverables

### Task 1: Fix dispatcher filename matching (sonnet bee)
- File: `hivenode/scheduler/dispatcher_daemon.py`
- Change file lookup from exact match to prefix glob
- Update existing tests that test file matching
- Add new test for prefix matching (e.g., `SPEC-MW-S01-command-interpreter.md` matches task_id `MW-S01`)
- Add test for dated prefix matching
- Add test for multiple matches (logs warning, takes first)

### Task 2: Fix scheduler encoding (haiku bee)
- File: `hivenode/scheduler/scheduler_daemon.py`
- Add `encoding='utf-8', errors='replace'` to all file reads in _done/ parsing
- Add test for unicode content in spec files

### Task 3: Queue housekeeping (haiku bee)
- Clean up `.deia/hive/queue/` state:
  - Verify `_active/` is empty (already cleaned by Q33NR)
  - Move CHROME-F2 from queue root back to `_active/` if queue-runner picks it up, or leave in queue root
  - Verify `_done/` has all completed specs
  - Write a status report of queue state to `.deia/hive/responses/`

## Constraints
- Tasks 1 and 2 can run in parallel (different files)
- Task 3 is independent
- All tasks: TDD, no stubs, no file over 500 lines
- Use sonnet for Task 1 (needs precision on glob logic), haiku for Tasks 2 and 3
