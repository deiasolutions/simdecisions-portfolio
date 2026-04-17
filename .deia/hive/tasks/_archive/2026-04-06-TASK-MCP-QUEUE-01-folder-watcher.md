# TASK-MCP-QUEUE-01: Implement Folder Watcher in Hivenode

## Objective

Implement a Python `watchdog`-based folder watcher in hivenode that monitors queue directories and emits MCP events when specs move between folders.

## Context

Currently 3 services (queue-runner, scheduler, dispatcher) independently poll queue directories, causing redundant I/O and bugs. This task creates a single watcher that emits events to consolidate monitoring.

**Design:** `.deia/hive/responses/20260406-MCP-QUEUE-NOTIFICATIONS-DESIGN.md`

## Files to Read First

- `hivenode/scheduler/scheduler_daemon.py` (lines 236-291)
  - Contains `_extract_task_id_from_spec()` logic to reuse
- `hivenode/hive_mcp/state.py`
  - StateManager pattern for thread-safe state
- `.deia/hive/scripts/queue/run_queue.py`
  - Queue directory structure reference

## Deliverables

- [ ] `hivenode/queue_watcher.py` — WatchdogObserver + QueueEventHandler
  - QueueEventHandler class (extends FileSystemEventHandler)
  - `_extract_task_id_from_spec()` function (from scheduler_daemon.py)
  - `_should_emit()` debouncing logic (500ms window)
  - Event emission to `.deia/hive/queue_events.jsonl`
  - MCP event payload generation (spec_file, task_id, directory, timestamp)
- [ ] `hivenode/routes/queue_events.py` — FastAPI route for event broadcasting
  - `POST /mcp/queue/notify` endpoint
  - Receives events from watcher, broadcasts to subscribers
- [ ] `hivenode/main.py` modifications
  - Start WatchdogObserver on app startup (lifespan)
  - Stop observer on shutdown
- [ ] Unit tests: `tests/hivenode/test_queue_watcher.py`
  - Test event detection (create, move)
  - Test debouncing (duplicates within 500ms suppressed)
  - Test task ID extraction (all 3 naming conventions)
  - Test filter rules (ignore non-SPEC files, temp files)

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases covered:
  - Rapid file moves (queue → _active → _done within 1s)
  - Malformed spec filenames (no task ID)
  - Temp files (`.tmp`, `.swp`) ignored
  - Windows file paths work correctly

## Acceptance Criteria

- [ ] Watcher starts on hivenode startup via FastAPI lifespan
- [ ] Events logged to `.deia/hive/queue_events.jsonl` with correct schema
- [ ] Task IDs extracted correctly for all 3 naming conventions:
  1. `SPEC-{ID}.md` → `{ID}`
  2. `SPEC-{ID}-{description}.md` → `{ID}`
  3. `YYYY-MM-DD-SPEC-{ID}-{description}.md` → `{ID}`
- [ ] Debouncing prevents duplicates (no events within 500ms of same spec+dir)
- [ ] All 5 directories watched: `queue/`, `_active/`, `_done/`, `_needs_review/`, `backlog/`
- [ ] Non-SPEC files ignored (no events for non-.md or non-SPEC files)
- [ ] Thread-safe event map (uses threading.Lock)
- [ ] Unit tests: 12+ tests, all passing
- [ ] No file over 500 lines

## Implementation Notes

### Task ID Extraction (Single Source of Truth)

Use scheduler's regex from `scheduler_daemon.py:236-291`. Do NOT reimplement.

```python
# Copy this function verbatim
def _extract_task_id_from_spec(filename: str | Path) -> Optional[str]:
    """Extract task ID from spec filename (supports 3 naming conventions)."""
    # [Copy full implementation from scheduler_daemon.py]
```

### Debouncing Strategy

```python
class QueueEventHandler:
    def __init__(self):
        self._recent_events: dict[tuple[str, str], float] = {}  # (spec_file, dir) -> timestamp
        self._lock = threading.Lock()

    def _should_emit(self, spec_file: str, directory: str) -> bool:
        """Check if event should be emitted (debouncing)."""
        key = (spec_file, directory)
        now = time.time()
        with self._lock:
            last_emit = self._recent_events.get(key, 0)
            if now - last_emit < 0.5:  # 500ms debounce
                return False
            self._recent_events[key] = now
            return True
```

### Event Log Format

Write to `.deia/hive/queue_events.jsonl` (JSONL, one event per line):

```json
{"event":"queue.spec_active","spec_file":"SPEC-MW-031-menu-bar-drawer.md","task_id":"MW-031","directory":"_active","timestamp":"2026-04-06T12:34:56Z"}
{"event":"queue.spec_done","spec_file":"SPEC-MW-031-menu-bar-drawer.md","task_id":"MW-031","directory":"_done","timestamp":"2026-04-06T12:45:12Z"}
```

### Watched Directories Mapping

| Directory | Event Type |
|-----------|------------|
| `.deia/hive/queue/` (root only, not subdirs) | `queue.spec_queued` |
| `.deia/hive/queue/_active/` | `queue.spec_active` |
| `.deia/hive/queue/_done/` | `queue.spec_done` |
| `.deia/hive/queue/_needs_review/` | `queue.spec_dead` |
| `.deia/hive/queue/backlog/` | `queue.spec_backlog` |

## Constraints

- No file over 500 lines (split watcher + event handler if needed)
- Use `watchdog` library (add to requirements.txt)
- Thread-safe (watcher runs in separate thread)
- No hardcoded paths (detect `.deia/` via repo root search)
- Windows 11 compatible (watchdog handles this)
- No stubs — fully implemented

## Dependencies

None (foundation task)

## Estimated Duration

1.5-2 hours (Sonnet)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260406-TASK-MCP-QUEUE-01-RESPONSE.md`

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
