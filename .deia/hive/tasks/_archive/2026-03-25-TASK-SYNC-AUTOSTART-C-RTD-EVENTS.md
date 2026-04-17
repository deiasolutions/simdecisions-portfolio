# TASK-SYNC-AUTOSTART-C: Add RTD Events for Sync Status

## Objective

Emit RTD (Real-Time Data) events during sync cycles so the build monitor can display sync status, queue depth, and conflicts.

## Context

The build monitor (`/build/status` endpoint) serves RTD events for real-time UI updates. Currently, sync cycles run silently — no events are emitted to indicate:
- Sync cycle started
- Sync cycle completed (with stats: pushed, pulled, conflicts, skipped)
- Queue flush results (flushed count, pending count)
- Conflict count

**Desired RTD events**:
1. `sync:cycle:started` — when PeriodicSyncWorker starts a sync cycle
2. `sync:cycle:completed` — when cycle finishes, payload: `{pushed, pulled, conflicts, skipped}`
3. `sync:queue:flushed` — when SyncQueue flush completes, payload: `{flushed, pending}`
4. `sync:conflict:detected` — when SyncEngine detects a conflict, payload: `{path, winner, loser}`

**Where to emit**:
- `PeriodicSyncWorker._run()` — emit `sync:cycle:started` before `await engine.sync()`
- `PeriodicSyncWorker._run()` — emit `sync:cycle:completed` after engine.sync() with stats
- `PeriodicSyncWorker._run()` — emit `sync:queue:flushed` after sync_queue.flush() with results
- `SyncEngine.sync()` — already emits LEDGER events (`SYNC_CONFLICT`), keep those, add RTD events

**RTD event format** (example):
```python
{
    "event_type": "sync:cycle:completed",
    "timestamp": "2026-03-25T10:30:00Z",
    "payload": {
        "pushed": 5,
        "pulled": 3,
        "conflicts": 1,
        "skipped": 12
    }
}
```

RTD events are stored in memory (not ledger) and served via SSE (`/build/status` endpoint).

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\worker.py` (lines 78-117)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\engine.py` (lines 112-299)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_routes.py` (RTD event mechanism)

## Deliverables

- [ ] Import RTD event emitter in `worker.py` and `engine.py`
- [ ] Emit `sync:cycle:started` at start of `PeriodicSyncWorker._run()`
- [ ] Emit `sync:cycle:completed` after `engine.sync()` with stats
- [ ] Emit `sync:queue:flushed` after `sync_queue.flush()` with results
- [ ] Emit `sync:conflict:detected` when SyncEngine detects conflict (in addition to existing ledger event)
- [ ] Tests verify RTD events are emitted with correct payloads

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Sync cycle with no changes → `sync:cycle:completed` with all zeros
  - Sync cycle with conflict → `sync:conflict:detected` event emitted
  - Queue flush with 5 pending → `sync:queue:flushed` with `{flushed: 5, pending: 0}`
  - Queue flush with 3 success, 2 fail → `sync:queue:flushed` with `{flushed: 3, pending: 2}`
  - Sync error → `sync:cycle:started` emitted, no `sync:cycle:completed` (error logged)

## Constraints

- No file over 500 lines
- TDD
- Python 3.13
- RTD events are **in-memory** (not written to ledger)
- RTD event format: `{"event_type": str, "timestamp": ISO8601, "payload": dict}`
- Do NOT remove existing ledger events (`SYNC_STARTED`, `SYNC_COMPLETED`, `SYNC_CONFLICT`) — keep those
- RTD events are additive, not replacements

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260325-TASK-SYNC-AUTOSTART-C-RESPONSE.md`

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
