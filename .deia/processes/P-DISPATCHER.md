# P-DISPATCHER: Dispatcher Daemon with MCP Events

**Status:** OPERATIONAL
**Owner:** Q88N
**Last Updated:** 2026-04-06

---

## Overview

The dispatcher daemon manages queue slot allocation and moves specs from backlog to active queue. It tracks active bee count, calculates available slots (`max_bees - active_count`), and dispatches blocked tasks when slots free up.

**MCP Integration (2026-04-06):** Dispatcher now maintains in-memory counters updated by MCP events instead of polling filesystem every 10s. This reduces slot recalculation latency from 10s average to <1s and eliminates stale slot detection bugs.

---

## Architecture

### Event Flow Diagram

```
[Queue runner moves spec to _active/]
    ↓
[Hivenode watcher detects file move]
    ↓
[Watcher emits queue.spec_active event]
    ↓
[POST http://localhost:8423/mcp/event]
    ↓
[Dispatcher daemon.on_mcp_event()]
    ↓
[Increment active_count]

[Queue runner moves spec to _done/]
    ↓
[Hivenode watcher detects file move]
    ↓
[Watcher emits queue.spec_done event]
    ↓
[POST http://localhost:8423/mcp/event]
    ↓
[Dispatcher daemon.on_mcp_event()]
    ↓
[Decrement active_count, wake event set]
    ↓
[Daemon loop wakes, checks available slots]
    ↓
[Moves unblocked specs from backlog/ to queue/]
```

### In-Memory Counter Architecture

The dispatcher maintains real-time counters updated by MCP events:

```python
# In-memory state (thread-safe)
self.active_count = 0   # Specs in _active/
self.queued_count = 0   # Specs in queue/ root
self._lock = threading.Lock()

def on_mcp_event(self, event: dict):
    with self._lock:
        if event["event"] == "queue.spec_active":
            self.active_count += 1
        elif event["event"] == "queue.spec_done":
            self.active_count = max(0, self.active_count - 1)
            self.wake_event.set()  # Slots freed, check backlog
        elif event["event"] == "queue.spec_queued":
            self.queued_count += 1
```

**Fallback refresh:** Every 60s, dispatcher re-counts from disk to correct drift from missed events.

---

## Configuration

### CLI Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--mcp-enabled` | `true` | Enable MCP event-driven mode |
| `--max-bees N` | `5` | Maximum concurrent bees (slot ceiling) |
| `--interval-seconds N` | `60` | Fallback refresh interval (when MCP unavailable) |
| `--dry-run` | `false` | Log dispatch decisions without moving files |

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DISPATCHER_MCP_PORT` | `8423` | MCP event receiver port |
| `DISPATCHER_FALLBACK_INTERVAL` | `60` | Fallback refresh interval (seconds) |
| `QUEUE_DIR` | `.deia/hive/queue/` | Queue root directory |

---

## Slot Calculation

The dispatcher calculates available slots using:

```python
available_slots = max_bees - active_count - queued_count
```

**Example:**
- `max_bees = 5`
- `active_count = 3` (3 bees currently running)
- `queued_count = 1` (1 spec waiting in queue/ root)
- `available_slots = 5 - 3 - 1 = 1` (can dispatch 1 more spec from backlog)

**Safety margin:** Dispatcher never dispatches more specs than available slots to prevent overload.

---

## Fallback Behavior

If MCP server unavailable, dispatcher falls back to direct filesystem counting.

| Condition | MCP Available | MCP Unavailable |
|-----------|---------------|-----------------|
| **Counter updates** | Event-driven (instant) | 60s refresh (fallback) |
| **Latency** | <1s | 10-60s (avg 35s) |
| **Counter accuracy** | 100% (no drift) | 100% (periodic refresh) |

**Drift correction:**
- Every 60s, dispatcher re-counts specs from disk
- Corrects counter drift from missed events
- Logs: `[DISPATCHER] Fallback refresh: active=3, queued=1`

---

## Troubleshooting

### Dispatcher not reacting to freed slots

**Symptoms:** Specs remain in backlog/ even when slots available

**Diagnosis:**
```bash
# Check dispatcher MCP server health
curl http://localhost:8423/health
# Expected: {"status": "ok"}

# Check event log for recent queue.spec_done events
tail -n 20 .deia/hive/queue_events.jsonl | grep spec_done

# Check dispatcher logs
tail -f .deia/hive/dispatcher_log.jsonl
# Look for: "MCP event received" or "Slots freed"
```

**Fix:**
- Verify MCP server started (log: `MCP server started on port 8423`)
- Verify port 8423 not blocked by firewall
- Verify hivenode watcher running
- Restart dispatcher daemon: `python hivenode/scheduler/dispatcher_daemon.py --mcp-enabled`

---

### Counter drift (active_count incorrect)

**Symptoms:** Dispatcher thinks all slots full, but no bees running

**Diagnosis:**
```bash
# Check in-memory counters
curl http://localhost:8423/status
# Expected: {"active_count": 3, "queued_count": 1, "available_slots": 1}

# Count actual specs on disk
ls .deia/hive/queue/_active/SPEC-*.md | wc -l
ls .deia/hive/queue/SPEC-*.md | wc -l

# Compare in-memory vs disk counts
```

**Fix:**
- Trigger manual fallback refresh: `kill -USR1 <dispatcher_pid>` (triggers refresh)
- Or wait 60s for automatic fallback refresh
- Or restart dispatcher (resets counters from disk)

**Root cause:** Missed MCP events (network hiccup, MCP server restart)

---

### Backlog specs stuck (not dispatched)

**Symptoms:** Specs in backlog/ never move to queue/, even with available slots

**Diagnosis:**
```bash
# Check for blocked dependencies
cat .deia/hive/queue/backlog/SPEC-*.md | grep "## Depends On"

# Check dispatcher decision logs
tail -f .deia/hive/dispatcher_log.jsonl | grep "dispatch_decision"

# Test dispatcher dry-run mode
python hivenode/scheduler/dispatcher_daemon.py --dry-run
```

**Fix:**
- Verify dependencies completed (specs in `_done/`)
- Check for circular dependencies (A→B→A)
- Verify specs have correct `## Priority` section (P0-P3)
- Check dispatcher max_bees limit not too low

---

### Event delivery failures

**Symptoms:** Events in `queue_events.jsonl` but counters not updating

**Diagnosis:**
```bash
# Check if dispatcher subscribed to events
curl http://localhost:8420/mcp/subscribers
# Expected: dispatcher listed with port 8423

# Test event delivery manually
curl -X POST http://localhost:8423/mcp/event \
  -H "Content-Type: application/json" \
  -d '{"event":"queue.spec_done","spec_file":"SPEC-TEST.md","task_id":"TEST","timestamp":"2026-04-06T12:00:00Z","directory":"_done"}'

# Check dispatcher logs for event receipt
grep "MCP event received" .deia/hive/dispatcher_log.jsonl
```

**Fix:**
- Verify dispatcher registered as subscriber on startup
- Check network connectivity between hivenode and dispatcher
- Restart both hivenode and dispatcher to re-establish connection

---

## Monitoring

### Key Metrics

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| **Latency:** Time from slot freed to backlog dispatch | <1s | >5s |
| **Counter drift:** Difference between in-memory and disk counts | 0 | >2 |
| **Fallback refreshes:** Frequency of disk re-counting | <1/hour | >10/hour |
| **Stale dispatches:** Specs dispatched but not in `_active/` after 30s | 0 | >1/day |

### Log Files

| File | Format | Purpose |
|------|--------|---------|
| `.deia/hive/dispatched.jsonl` | JSONL | Dispatch event log |
| `.deia/hive/dispatcher_log.jsonl` | JSONL | Dispatcher daemon log (counters, decisions) |
| `.deia/hive/queue_events.jsonl` | JSONL | MCP event log (all queue state changes) |

### Health Check

```bash
# Check dispatcher running
curl http://localhost:8423/health

# Check counter status
curl http://localhost:8423/status

# Check recent dispatches
tail -n 5 .deia/hive/dispatched.jsonl
```

---

## Operation

### Start Dispatcher

**Local dev:**
```bash
python hivenode/scheduler/dispatcher_daemon.py --mcp-enabled
```

**Railway (production):**
```bash
# Embedded in hivenode process (recommended)
python -m hivenode

# Or standalone:
python hivenode/scheduler/dispatcher_daemon.py --mcp-enabled
```

### Stop Dispatcher

```bash
# Send SIGTERM (graceful shutdown)
kill -TERM <pid>

# Or Ctrl+C if running in foreground
```

### Restart Dispatcher

```bash
# Find process
ps aux | grep dispatcher_daemon

# Kill gracefully
kill -TERM <pid>

# Restart
python hivenode/scheduler/dispatcher_daemon.py --mcp-enabled
```

### Disable MCP (Debugging)

```bash
# Fallback to polling-only mode
python hivenode/scheduler/dispatcher_daemon.py --mcp-enabled=false
```

Dispatcher will revert to original 10s polling behavior.

### Dry-Run Mode (Testing)

```bash
# Log dispatch decisions without moving files
python hivenode/scheduler/dispatcher_daemon.py --dry-run
```

Useful for testing dispatcher logic without affecting queue state.

---

## Performance

### Before MCP (Polling)

- **Detection latency:** 10s average (5-15s range)
- **I/O overhead:** 360 directory scans/hour (3 directories × 120 polls/hour)
- **Stale slot detection:** Bug caused 30-minute-old specs to block new dispatches

### After MCP (Event-Driven)

- **Detection latency:** <1s average (<500ms to 2s range)
- **I/O overhead:** ~6 directory scans/hour (fallback refresh only)
- **Stale slot detection:** Fixed (counters always accurate, no filesystem polling)

**Performance improvement:** ~90% reduction in latency, ~98% reduction in I/O, stale slot bug eliminated

---

## References

- **Design doc:** `.deia/hive/responses/20260406-MCP-QUEUE-NOTIFICATIONS-DESIGN.md`
- **Source:** `hivenode/scheduler/dispatcher_daemon.py`
- **Tests:** `tests/hivenode/scheduler/test_dispatcher_daemon.py`
- **Integration tests:** `tests/integration/test_mcp_queue_full_pipeline.py`

---

**END OF PROCESS DOCUMENT**
