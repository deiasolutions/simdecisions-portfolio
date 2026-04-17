# BRIEFING: Split Heartbeat into Liveness Ping + State Transition Log

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-16
**Priority:** P0
**BL:** BL-203

## Problem

Bee heartbeats currently serve three purposes with one mechanism: they prove liveness, populate the build log UI, and track active bees. This causes monitor-state.json to bloat (17K+ lines of repeated "running" entries in the log array). We need to separate these concerns.

## Design (approved by Q88N)

Two paths, both active simultaneously:

### Path A — Silent Liveness Ping

- Bee sends heartbeat as before (no bee-side changes needed)
- Backend receives heartbeat and updates ONLY `tasks[task_id].last_heartbeat` (ISO timestamp) on the task entry in monitor-state.json
- Does NOT append to the `log[]` array
- Does NOT write to the event ledger
- Queue runner checks `last_heartbeat` for liveness: if `now - last_heartbeat > TIMEOUT` (e.g. 60s), bee is considered dead
- The Active Bees pane (build monitor left column) shows tasks where status=running/dispatched AND last_heartbeat is fresh

### Path B — State Transition Events (logged)

- Only meaningful state changes get written to `log[]`: dispatched, first running, complete, failed, timeout
- Real messages from bees also get logged (e.g. "Dispatching sub-bee", "Tests: 12/12 passed")
- Repeated "Processing..." or "running" status pings do NOT get logged
- These entries show up in Build Log pane and optionally the event ledger

### Detection Logic

A heartbeat is a STATE TRANSITION if:
1. The task's status changed (e.g. dispatched → running), OR
2. The heartbeat contains a message that differs from the last logged message for that task, AND the message is not "Processing..."

Otherwise it's a SILENT PING — just update last_heartbeat timestamp.

## Files to Read First

Backend (heartbeat receiver + state management):
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\monitor-state.json` (structure reference only — do NOT modify directly)

Queue runner (liveness check):
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py`

Frontend (Active Bees pane — already uses task entries, not log):
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\buildStatusMapper.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\buildDataService.tsx`

## Scope

1. **Backend `build_monitor.py`**: Modify heartbeat handler to:
   - Always update `tasks[task_id].last_heartbeat` on every heartbeat
   - Only append to `log[]` on state transitions (status change or new meaningful message)
   - Add `last_heartbeat` field to task entries

2. **Queue runner `run_queue.py`**: Update liveness check to use `last_heartbeat` timestamp instead of relying on log entries. Dead bee = `now - last_heartbeat > 60s`.

3. **Frontend `buildStatusMapper.ts`**: `mapActiveBees()` already reads from task entries (not log), so it should mostly work. May need to incorporate `last_heartbeat` freshness check to distinguish truly active bees from stale entries.

4. **SSE stream**: The `snapshot` event should include `last_heartbeat` in task data so the frontend can use it.

5. **Tests**: TDD. Cover:
   - Silent ping updates last_heartbeat but does NOT grow log
   - State transition appends to log
   - Repeated same-status heartbeat does NOT append to log
   - New message (not "Processing...") appends to log
   - Queue runner detects dead bee via stale last_heartbeat
   - Queue runner considers bee alive with fresh last_heartbeat

## Acceptance Criteria

- [ ] Heartbeats update `last_heartbeat` timestamp on every ping
- [ ] Log array only grows on state transitions and real messages
- [ ] Repeated "running" / "Processing..." heartbeats do NOT add log entries
- [ ] Queue runner uses `last_heartbeat` for liveness detection
- [ ] Active Bees pane shows correct live bees
- [ ] Build Log pane shows only meaningful events
- [ ] Existing tests still pass
- [ ] New tests cover all detection logic

## Model Assignment

Use sonnet for task files. Use haiku for implementation bees.

## Constraints

- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- TDD
