# BRIEFING: MCP Queue Notification Architecture

**From:** Q33NR
**To:** Q33N
**Date:** 2026-04-06
**Priority:** P1

## Context

We currently have 3 services independently polling the same queue directories:

1. **Queue-runner** (hivenode, :8420) — polls `queue/` for new specs, moves to `_active/`, `_done/`, `_dead/`
2. **Scheduler daemon** — polls `_done/` every 30s to detect completions and recalculate schedule
3. **Dispatcher daemon** — polls `_active/`, `queue/`, `backlog/` every 10s to count slots and move specs

This caused two bugs already (filename extraction mismatch, stale slot detection) and wastes I/O on redundant polling. We want to consolidate folder watching into hivenode and have it notify the other services via MCP when changes occur.

## Goal

Design an MCP-based notification system where:
- **Hivenode** is the single watcher for all queue directories
- When folder state changes, hivenode emits MCP events
- **Scheduler** and **dispatcher** become event-driven consumers — they receive notifications, verify the change, and act
- Polling loops become fallback-only (heartbeat interval, e.g., 60s) for resilience

## Architecture

```
[hivenode folder watcher]
   │
   ├── spec lands in queue/     → MCP event: queue.spec_queued
   ├── spec moves to _active/   → MCP event: queue.spec_active
   ├── spec moves to _done/     → MCP event: queue.spec_done
   ├── spec moves to _dead/     → MCP event: queue.spec_dead
   └── spec added to backlog/   → MCP event: queue.spec_backlog
```

## Deliverables

This is a DESIGN task — produce a spec, not code. The Q33N should:

### 1. Read existing code to understand current state
- `hivenode/hive_mcp/` — existing MCP infrastructure, tools, transport
- `hivenode/scheduler/scheduler_daemon.py` — current polling logic, completion detection
- `hivenode/scheduler/dispatcher_daemon.py` — current polling logic, slot counting
- `.deia/hive/scripts/queue/run_queue.py` — queue-runner file movement logic
- `.deia/hive/scripts/queue/spec_processor.py` — spec processing lifecycle

### 2. Design the MCP event contract
For each event type, specify:
- Event name (e.g., `queue.spec_done`)
- Payload schema (task_id, spec_file, timestamp, metadata)
- Who emits it (hivenode)
- Who consumes it (scheduler, dispatcher, or both)
- What the consumer does on receipt

### 3. Design the folder watcher
- Single watcher process inside hivenode
- Technology choice: Python `watchdog` library, or `asyncio` filesystem polling, or OS-native (inotify/ReadDirectoryChanges)
- Which directories to watch: `queue/`, `_active/`, `_done/`, `_dead/`, `backlog/`
- Debouncing strategy (avoid duplicate events for rapid moves)
- Windows compatibility (this runs on Windows 11)

### 4. Design the scheduler/dispatcher refactor
- Convert polling loops to MCP event handlers
- Keep a fallback poll (60s heartbeat) for resilience if MCP connection drops
- Scheduler: on `queue.spec_done` → recalculate schedule, write schedule.json
- Dispatcher: on `queue.spec_done` → check for newly unblocked tasks, move from backlog/ to queue/
- Dispatcher: on `queue.spec_active` → update active count
- Remove direct file counting from dispatcher (get counts from hivenode API instead)

### 5. Design backward compatibility
- If MCP is not available, fall back to current polling behavior
- Scheduler and dispatcher should work standalone (no hard dependency on MCP)
- Graceful degradation: MCP speeds things up, polling is the safety net

### 6. Produce task breakdown
- Split the implementation into 4-6 tasks for bee dispatch
- Each task: concrete deliverable, files to modify, tests, acceptance criteria
- Dependency order for implementation

## Output

Write a design doc to `.deia/hive/responses/20260406-MCP-QUEUE-NOTIFICATIONS-DESIGN.md` containing:
1. MCP event schema (all event types, payloads)
2. Folder watcher design (technology, architecture)
3. Scheduler refactor plan
4. Dispatcher refactor plan
5. Backward compatibility strategy
6. Task breakdown (4-6 tasks with dependencies)

Also create task files in `.deia/hive/tasks/` for each implementation task.

## Constraints
- Design only — no code changes in this task
- Must work on Windows 11 (no Linux-only watchers)
- MCP transport: use existing hivenode MCP infrastructure
- Keep it simple — don't over-engineer the event system
- Each implementation task should be completable by a single sonnet bee
