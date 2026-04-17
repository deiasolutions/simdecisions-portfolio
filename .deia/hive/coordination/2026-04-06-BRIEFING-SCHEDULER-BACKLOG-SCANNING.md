# BRIEFING: Scheduler Backlog Scanning

**From:** Q33NR
**To:** Q33N
**Date:** 2026-04-06
**Priority:** P0

## Problem

The scheduler daemon only reads tasks from a hardcoded Python workdesk file (`scheduler_mobile_workdesk.py` → `TASKS` list). It does not scan `backlog/` for new spec files. This means:

1. Specs added to `backlog/` by Q33NR or other processes are **invisible** to the scheduler
2. The dispatcher only dispatches tasks in `schedule.json`, which only contains workdesk tasks
3. New workstreams (EST, IRD, MCP-QUEUE) require manual intervention to dispatch — defeating the purpose of the pipeline

**Root cause:** Line 553 of `scheduler_daemon.py`:
```python
tasks = [Task(**t.__dict__) for t in TASKS]  # copy from hardcoded workdesk
```

## Expected Behavior

The scheduler should:
1. Read tasks from the workdesk file (existing behavior, keep it)
2. **Also scan `backlog/` for SPEC-*.md files** on every cycle
3. Parse each spec's metadata: task_id, depends_on, model, priority, estimated hours
4. Merge backlog specs into the task list (workdesk tasks + backlog specs)
5. Recompute schedule when new specs appear in backlog/
6. The MCP watcher (queue_watcher.py) already detects new files in backlog/ — wire the `queue.spec_queued` event to trigger a rescan

## Design

### Spec Metadata Extraction

Use the existing `spec_parser.py` to extract fields from backlog specs:

```python
from spec_parser import SpecFile

def scan_backlog(backlog_dir: Path) -> list[Task]:
    """Scan backlog/ for SPEC-*.md files, convert to Task objects."""
    tasks = []
    for spec_path in backlog_dir.glob("SPEC-*.md"):
        spec = SpecFile.from_path(spec_path)
        task = Task(
            id=extract_task_id(spec_path.stem),  # SPEC-EST-02-data-collection → EST-02
            task_type=guess_task_type(spec),       # build, test, spec, verify, css
            description=spec.objective or spec_path.stem,
            duration_hours=estimate_hours(spec),   # from spec or default by type
            dependencies=parse_depends_on(spec),   # from ## Depends On section
            model=spec.model_assignment or "sonnet",
        )
        tasks.append(task)
    return tasks
```

### Task ID Extraction

```python
def extract_task_id(stem: str) -> str:
    """SPEC-EST-02-data-collection → EST-02"""
    # Remove SPEC- prefix
    name = stem.replace("SPEC-", "")
    # Extract ID pattern: letters-digits (e.g., EST-02, IRD-01, MCP-QUEUE-05, MW-031)
    match = re.match(r'([A-Z]+-(?:QUEUE-)?[A-Z]*\d+)', name)
    return match.group(1) if match else name
```

### Duration Estimation

If spec doesn't have explicit hours, use defaults by model:
- haiku: 3 hours
- sonnet: 5 hours
- opus: 8 hours

### Merge Strategy

```python
def build_task_list(workdesk_tasks, backlog_dir):
    """Merge workdesk tasks with backlog specs."""
    backlog_tasks = scan_backlog(backlog_dir)

    # Workdesk tasks have priority — if same task_id exists in both, keep workdesk version
    known_ids = {t.id for t in workdesk_tasks}
    new_tasks = [t for t in backlog_tasks if t.id not in known_ids]

    return workdesk_tasks + new_tasks
```

### Daemon Loop Change

In `_daemon_loop()`, rescan backlog on every cycle (or on MCP event):

```python
def _daemon_loop(self):
    while not self._stop_event.is_set():
        # Rescan backlog for new specs
        backlog_tasks = scan_backlog(self.queue_dir / "backlog")
        self._merge_tasks(backlog_tasks)

        # Detect completions (existing)
        completed = self._detect_completions()

        # Recompute schedule if tasks changed
        if self._tasks_changed(backlog_tasks, completed):
            self.compute_schedule()
            self._write_schedule()

        self._wait_for_next_cycle()
```

### Completion Detection for Non-Workdesk Tasks

The existing `_extract_task_id_from_spec()` method already handles multiple filename formats. When a spec moves to `_done/`, the scheduler detects it and marks the task complete. This works for backlog-originated specs too — no changes needed.

### Dependency Resolution

The `## Depends On` section lists task IDs. The scheduler's OR-Tools solver already handles dependencies. Backlog specs with `Depends On: EST-01` will be scheduled after EST-01 completes, just like workdesk tasks.

Key: dependency IDs must match between specs. If `SPEC-EST-02` says `Depends On: EST-01`, and `SPEC-EST-01` is in `_done/` with filename `SPEC-EST-01-schema-migration.md`, the scheduler must extract `EST-01` from both and match them.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\scheduler\scheduler_daemon.py` — current daemon (line 553 is the gap)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\scheduler\scheduler_mobile_workdesk.py` — current workdesk (TASKS list, Task dataclass)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_parser.py` — spec file parser (sections, fields)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\queue_watcher.py` — MCP watcher (queue.spec_queued events)

## Deliverables

This is a DESIGN + BUILD task. The Q33N should:

1. **Implement `scan_backlog()`** — parse SPEC-*.md files from backlog/, convert to Task objects
2. **Implement `extract_task_id()`** — handle all filename formats (EST-02, IRD-01, MCP-QUEUE-05, MW-031)
3. **Modify `_daemon_loop()`** — rescan backlog on every cycle, merge with workdesk tasks
4. **Modify `compute_schedule()`** — accept merged task list (workdesk + backlog)
5. **Wire MCP event** — `queue.spec_queued` triggers immediate rescan (not wait for next cycle)
6. **Tests** — 10+ tests covering scanning, ID extraction, merging, dependency resolution
7. **Create task files** for bee dispatch (1-2 tasks):
   - Task 1: Backlog scanning + merge + tests (sonnet)
   - Task 2 (optional): MCP event wiring for immediate rescan (depends on QUEUE-03)

## Constraints

- Do NOT remove workdesk support — keep it as primary source, backlog as supplementary
- Do NOT change spec file format — parse existing sections
- spec_parser.py is the source of truth for parsing — use it, don't reinvent
- No file over 500 lines
- TDD where applicable
- The backlog scan should be fast (< 100ms for 100 specs) — no LLM calls
- Handle gracefully: missing sections, malformed specs, duplicate task IDs

## Open Questions for Q33N

1. Should the scheduler log when it discovers new backlog specs? Recommendation: yes, `logger.info(f"Discovered {len(new)} new specs in backlog/")`
2. Should backlog specs have lower priority than workdesk specs in the solver? Recommendation: no — use the spec's own Priority field (P0/P1/P2/P3)
3. Should we create a generic workdesk format (YAML/JSON) that replaces the Python TASKS list? Recommendation: defer — keep Python workdesk for MW, backlog scanning for everything else
