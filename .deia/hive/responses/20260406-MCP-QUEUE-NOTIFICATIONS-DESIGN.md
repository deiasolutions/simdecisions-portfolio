# MCP Queue Notification Architecture — Design Document

**Status:** DESIGN_COMPLETE
**Date:** 2026-04-06
**Author:** Q33N (QUEEN-2026-04-06-BRIEFING-MCP-QUEUE-)

---

## Executive Summary

This design consolidates queue directory watching from 3 independent polling daemons into a single hivenode folder watcher that emits MCP events. Scheduler and dispatcher become event-driven consumers, speeding up completions detection from 30s to near-instant while maintaining fallback polling for resilience.

**Impact:** Reduces detection latency by ~90%, eliminates redundant I/O, prevents filename extraction mismatches.

---

## Current State Analysis

### Problem

Three services independently poll the same queue directories:

1. **Queue-runner** (hivenode:8420) — polls `queue/` every ~30s (Fibonacci backoff), moves specs to `_active/`, `_done/`, `_dead/`
2. **Scheduler daemon** — polls `_done/` every 30s to detect completions, recalculates schedule
3. **Dispatcher daemon** — polls `_active/`, `queue/`, `backlog/` every 10s to count slots

**Bugs caused:**
- **Bug 1:** Scheduler filename extraction mismatch — scheduler's regex didn't match dispatcher's spec naming convention
- **Bug 2:** Stale slot detection — dispatcher counted 30-minute-old specs as active, blocking new dispatches

**I/O waste:** 3 services reading same directories 100+ times/hour = ~300 filesystem scans/hour

---

## MCP Event Contract

### Event Types

All events emitted by hivenode, consumed by scheduler/dispatcher via MCP.

| Event Name | Payload | Emitter | Consumers | Trigger |
|------------|---------|---------|-----------|---------|
| `queue.spec_queued` | `{spec_file, task_id, priority, timestamp}` | hivenode | dispatcher | Spec lands in `queue/` root |
| `queue.spec_active` | `{spec_file, task_id, timestamp}` | hivenode | dispatcher | Spec moves to `_active/` |
| `queue.spec_done` | `{spec_file, task_id, timestamp}` | hivenode | scheduler, dispatcher | Spec moves to `_done/` |
| `queue.spec_dead` | `{spec_file, task_id, timestamp}` | hivenode | (log only) | Spec moves to `_needs_review/` |
| `queue.spec_backlog` | `{spec_file, task_id, timestamp}` | hivenode | dispatcher | Spec added to `backlog/` |

### Payload Schema (all events)

```json
{
  "event": "queue.spec_done",
  "spec_file": "SPEC-MW-031-menu-bar-drawer.md",
  "task_id": "MW-031",
  "timestamp": "2026-04-06T12:34:56Z",
  "directory": "_done"
}
```

**Fields:**
- `event` (string): Event type (e.g., `queue.spec_done`)
- `spec_file` (string): Full filename (e.g., `SPEC-MW-031-menu-bar-drawer.md`)
- `task_id` (string): Extracted task ID (e.g., `MW-031`)
- `timestamp` (string): ISO 8601 UTC timestamp
- `directory` (string): Destination directory (`queue`, `_active`, `_done`, `_dead`, `backlog`)

### Consumer Actions

| Consumer | Event | Action |
|----------|-------|--------|
| **Scheduler** | `queue.spec_done` | Recalculate schedule, write `schedule.json`, log to `schedule_log.jsonl` |
| **Dispatcher** | `queue.spec_done` | Check for newly unblocked tasks, move from `backlog/` to `queue/` |
| **Dispatcher** | `queue.spec_active` | Update active count, calculate available slots |
| **Dispatcher** | `queue.spec_backlog` | (optional) Track backlog inventory for reporting |

---

## Folder Watcher Design

### Technology Choice: Python `watchdog`

**Rationale:**
- ✅ Windows 11 compatible (uses `ReadDirectoryChangesW` on Windows)
- ✅ Cross-platform (Linux inotify, macOS FSEvents)
- ✅ Mature library (14k+ stars, actively maintained)
- ✅ Debouncing built-in via `FileSystemEventHandler` + time-based filtering
- ✅ Pure Python, no OS-specific syscalls in user code

**Alternatives rejected:**
- ~~`asyncio` polling~~ — still polling, not event-driven
- ~~OS-native (inotify/ReadDirectoryChanges)~~ — platform-specific, more code

### Architecture

```
[hivenode FastAPI app (port 8420)]
    │
    ├── [WatchdogObserver thread]
    │   ├── FileSystemEventHandler (queue/)
    │   ├── FileSystemEventHandler (_active/)
    │   ├── FileSystemEventHandler (_done/)
    │   ├── FileSystemEventHandler (_dead/)
    │   └── FileSystemEventHandler (backlog/)
    │
    └── [MCP event broadcaster]
        ├── POST to scheduler (http://localhost:????)
        ├── POST to dispatcher (http://localhost:????)
        └── Log to .deia/hive/queue_events.jsonl
```

**Components:**

1. **WatchdogObserver** — Background thread managed by FastAPI lifespan
2. **QueueEventHandler** — `watchdog.events.FileSystemEventHandler` subclass
3. **MCP Event Broadcaster** — Maps filesystem events → MCP payloads, delivers to consumers

### Watched Directories

| Directory | Watch Pattern | Event Trigger |
|-----------|---------------|---------------|
| `.deia/hive/queue/` | `SPEC-*.md` (created/moved) | `queue.spec_queued` |
| `.deia/hive/queue/_active/` | `SPEC-*.md` (created/moved) | `queue.spec_active` |
| `.deia/hive/queue/_done/` | `SPEC-*.md` (created/moved) | `queue.spec_done` |
| `.deia/hive/queue/_needs_review/` | `SPEC-*.md` (created/moved) | `queue.spec_dead` |
| `.deia/hive/queue/backlog/` | `SPEC-*.md` (created) | `queue.spec_backlog` |

**Filter rules:**
- Ignore non-`.md` files
- Ignore filenames without `SPEC-` prefix
- Ignore `modified` events (only `created` and `moved`)
- Ignore temp files (`.tmp`, `.swp`, etc.)

### Debouncing Strategy

**Problem:** Rapid file moves (e.g., `queue/` → `_active/` → `_done/`) within milliseconds can cause duplicate events.

**Solution: Time-based deduplication**

- Track last event per `(spec_file, directory)` pair
- Suppress duplicate events within 500ms window
- Use `threading.Lock` for thread-safe event map

**Example:**
```python
# In-memory event cache
self._recent_events: dict[tuple[str, str], float] = {}  # (spec_file, dir) -> timestamp
self._lock = threading.Lock()

def _should_emit(spec_file: str, directory: str) -> bool:
    key = (spec_file, directory)
    now = time.time()
    with self._lock:
        last_emit = self._recent_events.get(key, 0)
        if now - last_emit < 0.5:  # 500ms debounce
            return False
        self._recent_events[key] = now
        return True
```

### Task ID Extraction (Single Source of Truth)

Use scheduler's existing `_extract_task_id_from_spec()` logic (lines 236-291 in `scheduler_daemon.py`). This avoids mismatches.

**Supports three naming conventions:**
1. `SPEC-{ID}.md` → `{ID}`
2. `SPEC-{ID}-{description}.md` → `{ID}`
3. `YYYY-MM-DD-SPEC-{ID}-{description}.md` → `{ID}`

Task ID format: `{PREFIX}-{IDENTIFIER}` (e.g., `MW-031`, `MW-S01`, `CONN-05`)

---

## Scheduler Refactor Plan

### Current Implementation (scheduler_daemon.py)

**Polling loop (lines 426-442):**
- Runs every 30s (`interval_seconds`)
- Scans `_done/` directory for `SPEC-*.md` files
- Extracts task IDs, recalculates schedule
- Writes `schedule.json`

### Proposed Implementation

**Event-driven architecture with fallback:**

```python
class SchedulerDaemon:
    def __init__(self, ..., mcp_enabled: bool = True):
        self.mcp_enabled = mcp_enabled
        self.mcp_client = MCPClient("http://localhost:8420/mcp") if mcp_enabled else None
        self.wake_event = threading.Event()  # Signals immediate recalculation

    def _daemon_loop(self):
        while self.running:
            # Wait for wake event (from MCP) or timeout (fallback)
            woken = self.wake_event.wait(timeout=60)  # 60s fallback

            if woken:
                print("[SCHEDULER] Woken by MCP event, recalculating...")
                self.wake_event.clear()
            else:
                print("[SCHEDULER] Fallback poll (60s timeout)")

            # Always recalculate on wake (event or timeout)
            self.compute_and_write_schedule()

    def on_mcp_event(self, event: dict):
        """Handle MCP queue.spec_done event."""
        if event["event"] == "queue.spec_done":
            print(f"[SCHEDULER] MCP: spec completed: {event['spec_file']}")
            self.wake_event.set()  # Wake daemon immediately
```

**MCP event subscription:**
- Scheduler registers as MCP consumer for `queue.spec_done`
- Hivenode POSTs event to scheduler's HTTP endpoint (e.g., `:8422/mcp/event`)
- Scheduler's FastAPI app handles POST, calls `daemon.on_mcp_event()`

**Fallback behavior:**
- If MCP server down, `wake_event.wait(timeout=60)` times out
- Daemon falls back to 60s polling (2x slower than current 30s, but acceptable)
- No hard dependency on MCP

---

## Dispatcher Refactor Plan

### Current Implementation (dispatcher_daemon.py)

**Polling loop (lines 128-243):**
- Runs every 10s
- Counts specs in `_active/`, `queue/`, `backlog/`
- Calculates available slots: `max_bees - active - queued`
- Moves specs from `backlog/` to `queue/`

### Proposed Implementation

**Event-driven slot management:**

```python
class DispatcherDaemon:
    def __init__(self, ..., mcp_enabled: bool = True):
        self.mcp_enabled = mcp_enabled
        self.mcp_client = MCPClient("http://localhost:8420/mcp") if mcp_enabled else None
        self.wake_event = threading.Event()

        # In-memory counters (updated by MCP events)
        self.active_count = 0
        self.queued_count = 0
        self._lock = threading.Lock()

    def _daemon_loop(self):
        # Initial count (on startup)
        self._refresh_counts()

        while self.running:
            woken = self.wake_event.wait(timeout=60)  # 60s fallback

            if woken:
                print("[DISPATCHER] Woken by MCP event, checking slots...")
                self.wake_event.clear()
            else:
                print("[DISPATCHER] Fallback poll, refreshing counts")
                self._refresh_counts()  # Re-sync from disk

            self._dispatch_cycle()

    def on_mcp_event(self, event: dict):
        """Handle MCP events (spec_done, spec_active, spec_queued)."""
        with self._lock:
            if event["event"] == "queue.spec_active":
                self.active_count += 1
            elif event["event"] == "queue.spec_done":
                self.active_count = max(0, self.active_count - 1)
                # Wake to check if slots freed
                self.wake_event.set()
            elif event["event"] == "queue.spec_queued":
                self.queued_count += 1

        print(f"[DISPATCHER] MCP: {event['event']}, active={self.active_count}, queued={self.queued_count}")

    def _refresh_counts(self):
        """Fallback: count specs on disk (used on startup and fallback polls)."""
        with self._lock:
            self.active_count = self._count_specs_in(self.active_dir)
            self.queued_count = self._count_specs_in(self.queue_dir, pattern="SPEC-*.md")
```

**Key changes:**
1. **Remove direct file counting from dispatch cycle** — use in-memory counters updated by MCP
2. **Fallback refresh** — re-count from disk every 60s if MCP unavailable
3. **Immediate dispatch on slot freed** — `queue.spec_done` wakes dispatcher instantly

---

## Backward Compatibility Strategy

### Graceful Degradation

Both scheduler and dispatcher MUST work standalone if MCP is unavailable.

**Fallback behavior:**

| Service | MCP Available | MCP Unavailable |
|---------|---------------|-----------------|
| **Scheduler** | Event-driven (instant) + 60s fallback poll | 60s polling only |
| **Dispatcher** | Event-driven counters + 60s fallback poll | 10s polling (current behavior) |

**Implementation:**

```python
# Constructor flag
def __init__(self, ..., mcp_enabled: bool = True):
    self.mcp_enabled = mcp_enabled

# Startup check
try:
    resp = requests.get("http://localhost:8420/health", timeout=2)
    if resp.status_code == 200:
        self.mcp_enabled = True
except:
    print("[WARN] MCP server unavailable, falling back to polling")
    self.mcp_enabled = False
```

**No breaking changes:**
- CLI flags unchanged
- Config files unchanged
- Existing deployments work without MCP (just slower)

---

## Task Breakdown

### Phase 1: Foundation (Tasks 1-2)

**TASK-MCP-QUEUE-01: Implement folder watcher in hivenode**
- **Deliverables:**
  - `hivenode/queue_watcher.py` — Watchdog observer + event handler
  - Emit MCP events via FastAPI SSE endpoint
  - Log events to `.deia/hive/queue_events.jsonl`
  - Unit tests (watchdog event handling, debouncing, task ID extraction)
- **Dependencies:** None
- **Model:** Sonnet
- **Acceptance:**
  - Watcher starts on hivenode startup
  - Events logged on file moves
  - Task IDs extracted correctly (all 3 naming conventions)
  - Debouncing works (no duplicates within 500ms)

**TASK-MCP-QUEUE-02: Add MCP event HTTP endpoints**
- **Deliverables:**
  - `POST /mcp/queue/notify` endpoint in hivenode (broadcasts events)
  - `POST /scheduler/mcp/event` endpoint in scheduler daemon
  - `POST /dispatcher/mcp/event` endpoint in dispatcher daemon
  - Integration tests (send event via HTTP, verify handling)
- **Dependencies:** TASK-MCP-QUEUE-01
- **Model:** Sonnet
- **Acceptance:**
  - Hivenode broadcasts events to scheduler/dispatcher
  - Events trigger wake signals
  - Errors logged, not fatal

### Phase 2: Scheduler Integration (Task 3)

**TASK-MCP-QUEUE-03: Refactor scheduler for event-driven operation**
- **Deliverables:**
  - Modify `scheduler_daemon.py`: add MCP client, wake event, event handler
  - Change polling interval from 30s → 60s
  - Add `--mcp-enabled` CLI flag (default True)
  - E2E test: move spec to `_done/`, verify instant schedule recalculation
- **Dependencies:** TASK-MCP-QUEUE-02
- **Model:** Sonnet
- **Acceptance:**
  - Scheduler wakes on `queue.spec_done` event (<1s latency)
  - Fallback polling works if MCP down (60s interval)
  - All existing tests pass

### Phase 3: Dispatcher Integration (Task 4)

**TASK-MCP-QUEUE-04: Refactor dispatcher for event-driven slot management**
- **Deliverables:**
  - Modify `dispatcher_daemon.py`: add in-memory counters, MCP event handler
  - Remove direct file counting from hot path (use counters)
  - Fallback: re-count from disk every 60s
  - E2E test: move spec to `_done/`, verify dispatcher wakes and dispatches from backlog
- **Dependencies:** TASK-MCP-QUEUE-02
- **Model:** Sonnet
- **Acceptance:**
  - Dispatcher updates counters on MCP events
  - Dispatcher wakes on `queue.spec_done` (<1s latency)
  - Fallback polling works (60s refresh)
  - All existing tests pass

### Phase 4: Testing & Documentation (Tasks 5-6)

**TASK-MCP-QUEUE-05: Integration testing suite**
- **Deliverables:**
  - E2E test: full pipeline (spec queued → active → done → scheduler/dispatcher reaction)
  - Failure tests: MCP server down, network timeout, malformed events
  - Performance test: 100 specs moved rapidly, verify no duplicates
  - Test report in `.deia/hive/responses/`
- **Dependencies:** TASK-MCP-QUEUE-03, TASK-MCP-QUEUE-04
- **Model:** Sonnet
- **Acceptance:**
  - All E2E tests pass
  - Fallback behavior verified
  - No event loss under load

**TASK-MCP-QUEUE-06: Update documentation**
- **Deliverables:**
  - Update `.deia/processes/P-SCHEDULER.md` with MCP event flow
  - Update `.deia/processes/P-DISPATCHER.md` with MCP event flow
  - Add `.deia/specs/SPEC-MCP-QUEUE-NOTIFICATIONS.md` (this design doc)
  - Update deployment guide (Railway, local dev)
- **Dependencies:** TASK-MCP-QUEUE-05
- **Model:** Haiku
- **Acceptance:**
  - All docs accurate
  - Deployment steps validated
  - Q88N approves

---

## File Structure

```
hivenode/
  queue_watcher.py              # NEW: Watchdog observer + event handler
  routes/
    queue_events.py             # NEW: POST /mcp/queue/notify endpoint

scheduler/
  scheduler_daemon.py           # MODIFIED: Add MCP client, wake event
  scheduler_mcp_server.py       # NEW: FastAPI app for POST /scheduler/mcp/event
  dispatcher_daemon.py          # MODIFIED: Add MCP client, counters, wake event
  dispatcher_mcp_server.py      # NEW: FastAPI app for POST /dispatcher/mcp/event

.deia/hive/
  queue_events.jsonl            # NEW: Event log (all queue state changes)

tests/
  hivenode/
    test_queue_watcher.py       # NEW: Unit tests for watcher
  scheduler/
    test_scheduler_mcp.py       # NEW: Integration tests
    test_dispatcher_mcp.py      # NEW: Integration tests
  integration/
    test_mcp_e2e.py             # NEW: Full pipeline test
```

---

## Deployment Strategy

### Local Dev (No Changes)

```bash
# Terminal 1: Hivenode (includes watcher)
python -m hivenode.main

# Terminal 2: Scheduler
python hivenode/scheduler/scheduler_daemon.py --mcp-enabled

# Terminal 3: Dispatcher
python hivenode/scheduler/dispatcher_daemon.py --mcp-enabled
```

### Railway (Production)

**Option 1: All-in-one (Recommended)**
- Run scheduler + dispatcher as background threads in hivenode process
- Single container, single Railway service
- Watcher + scheduler + dispatcher all in-process

**Option 2: Separate services**
- 3 Railway services: hivenode, scheduler, dispatcher
- Hivenode broadcasts events via HTTP to scheduler/dispatcher public URLs
- Higher cost, but more resilience

**Config env vars:**
- `MCP_ENABLED=true` (default)
- `SCHEDULER_MCP_URL=http://localhost:8422/mcp/event`
- `DISPATCHER_MCP_URL=http://localhost:8423/mcp/event`

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Watchdog misses events** | Specs stuck in `_active/`, never move | Fallback polling every 60s catches missed events |
| **MCP server down** | No event delivery | Scheduler/dispatcher fall back to 60s polling |
| **Event duplication** | Double-processing, wasted work | 500ms debouncing + idempotent handlers |
| **Network latency (Railway)** | Events delayed by ~100ms | Acceptable (still faster than 30s polling) |
| **Task ID extraction mismatch** | Scheduler/dispatcher see different IDs | Use single extraction function (scheduler's regex) |

---

## Success Metrics

| Metric | Before | After | Target |
|--------|--------|-------|--------|
| **Completion detection latency** | 30s (avg) | <1s | <2s |
| **Dispatcher slot recalculation** | 10s (avg) | <1s | <2s |
| **Filesystem I/O (scans/hour)** | ~300 | ~20 (fallback only) | <50 |
| **Bug recurrence** | 2 bugs in 2 weeks | 0 | 0 |

---

## Implementation Order

1. **TASK-MCP-QUEUE-01** — Folder watcher (foundation)
2. **TASK-MCP-QUEUE-02** — HTTP endpoints (transport)
3. **TASK-MCP-QUEUE-03 + TASK-MCP-QUEUE-04** — Scheduler + Dispatcher (parallel)
4. **TASK-MCP-QUEUE-05** — Integration testing
5. **TASK-MCP-QUEUE-06** — Documentation

**Estimated total time:** 4-6 hours (1-2h per task for sonnet)

---

## Open Questions for Q88N

1. **Scheduler/dispatcher HTTP ports:** Use 8422/8423, or embed in hivenode?
2. **Railway deployment:** All-in-one container or separate services?
3. **Event log retention:** Keep `queue_events.jsonl` forever, or rotate after 7 days?
4. **Priority:** Should this block Mobile Workdesk Phase 1, or run in parallel?

---

## References

- **Briefing:** `.deia/hive/coordination/2026-04-06-BRIEFING-MCP-QUEUE-NOTIFICATIONS.md`
- **Scheduler source:** `hivenode/scheduler/scheduler_daemon.py` (lines 1-534)
- **Dispatcher source:** `hivenode/scheduler/dispatcher_daemon.py` (lines 1-476)
- **Queue runner:** `.deia/hive/scripts/queue/run_queue.py` (lines 1-961)
- **MCP infrastructure:** `hivenode/hive_mcp/` (existing tools, state, transport)

---

**END OF DESIGN DOCUMENT**
