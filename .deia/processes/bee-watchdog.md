# Bee Watchdog Process

## Summary

Bees report their activity to `localhost:8420/build/heartbeat` during execution. A watchdog monitors these heartbeats. If a bee goes silent for **8 minutes** (480 seconds), the watchdog kills it and dispatches a replacement bee with a resume instruction. Max 2 restart attempts per task.

## How It Works

### Heartbeat Flow

```
Bee (dispatch.py)                   Hivenode (port 8420)
  |                                      |
  |-- POST /build/heartbeat ------------>|  "dispatched"
  |        (fires on start)              |
  |                                      |
  |-- POST /build/heartbeat ------------>|  "in_progress"
  |        (fires every 5 min)           |
  |                                      |
  |-- POST /build/heartbeat ------------>|  "complete" or "failed"
  |        (fires on finish)             |
  |                                      |

Watchdog (bee_dispatch.py)
  |
  |-- GET /build/status ----------------->|  every 30s
  |        (check last_seen timestamps)   |
  |                                       |
  |  If (now - last_seen) > 480s:         |
  |    → kill bee process                 |
  |    → POST /build/heartbeat "timeout"  |
  |    → re-dispatch with resume header   |
```

### Heartbeat Payload

```json
{
  "task_id": "2026-03-14-TASK-110-INDEXER-MODELS-SCANNER",
  "status": "dispatched|in_progress|complete|failed|timeout",
  "model": "sonnet",
  "message": "role=bee",
  "cost_usd": 0.05,
  "tests_passed": 15,
  "tests_total": 15,
  "input_tokens": 50000,
  "output_tokens": 10000,
  "role": "B"
}
```

## Usage

### Standalone dispatch with watchdog

```bash
python .deia/hive/scripts/dispatch/bee_dispatch.py \
  .deia/hive/tasks/TASK-XXX.md \
  --model sonnet --role bee --inject-boot
```

### Custom stale threshold

```bash
python .deia/hive/scripts/dispatch/bee_dispatch.py \
  .deia/hive/tasks/TASK-XXX.md \
  --model sonnet --role bee --inject-boot \
  --stale-seconds 300
```

### Direct dispatch (no watchdog — legacy)

```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/TASK-XXX.md \
  --model sonnet --role bee --inject-boot --timeout 1200
```

## Configuration

| Parameter | Value | Location |
|-----------|-------|----------|
| Stale threshold | 480s (8 min) | `bee_dispatch.py:DEFAULT_STALE_SECONDS` |
| Poll interval | 30s | `bee_dispatch.py:POLL_SECONDS` |
| Max restarts | 2 | `bee_dispatch.py:MAX_RESTARTS` |
| Heartbeat URL | `http://localhost:8420/build/heartbeat` | `dispatch.py:HEARTBEAT_URL` |
| Status URL | `http://localhost:8420/build/status` | `bee_dispatch.py:BUILD_STATUS_URL` |
| Queue runner stale threshold | 480s (8 min) | `dispatch_handler.py:WATCHDOG_STALE_SECONDS` |

## Restart Behavior

When the watchdog kills a stale bee:

1. A `timeout` heartbeat is posted to the build monitor
2. The task file is prepended with a resume instruction:
   ```
   ## WATCHDOG RESTART — Attempt 1/2
   A previous bee timed out. You are the restart bee.
   Your job:
   1. Check what files already exist from the previous attempt
   2. Run existing tests to see what passes
   3. Finish any remaining work
   4. Do NOT redo work that is already done
   ```
3. A new bee is dispatched with the modified task file
4. After 2 failed restarts, the task is marked FAILED

## Prerequisites

- **Hivenode must be running** at `localhost:8420` for heartbeats to work
- If hivenode is down, the watchdog will NOT kill bees (fail-safe: no false kills)
- dispatch.py sends heartbeats regardless of whether a watchdog is monitoring

## Monitoring

Check active bees:
```bash
curl http://localhost:8420/build/status | python -m json.tool
```

Watch live heartbeats (SSE stream):
```bash
curl http://localhost:8420/build/stream
```

## Files

| File | Purpose |
|------|---------|
| `.deia/hive/scripts/dispatch/dispatch.py` | Core dispatcher, sends heartbeats |
| `.deia/hive/scripts/dispatch/bee_dispatch.py` | Standalone watchdog wrapper |
| `.deia/hive/scripts/queue/dispatch_handler.py` | Queue runner watchdog (same logic) |
| `hivenode/routes/build_monitor.py` | Heartbeat receiver + state tracking |
