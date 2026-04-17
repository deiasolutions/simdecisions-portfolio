# Q33N Briefing: SPEC-SYNC-AUTOSTART-FLUSH

**Date:** 2026-03-25
**From:** Q88NR (Regent)
**To:** Q33N (Queen Coordinator)
**Spec:** SPEC-SYNC-AUTOSTART-FLUSH
**Model Assignment:** sonnet

---

## Objective

Wire up the existing sync engine and worker so they auto-start with hivenode and automatically flush the SyncQueue to cloud when Railway is reachable.

---

## Context

The sync infrastructure exists:
- `hivenode/sync/engine.py` - sync engine
- `hivenode/sync/worker.py` - sync worker
- `hivenode/storage/adapters/sync_queue.py` - queue for pending sync operations

But they don't auto-start. Users must manually trigger sync. The goal is to make sync automatic:
1. Start sync worker as background task when hivenode starts
2. Flush SyncQueue to cloud on each sync cycle
3. Handle offline/online transitions gracefully
4. Surface conflicts via /sync/conflicts endpoint

---

## Files to Investigate

### Must Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\engine.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\sync\worker.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\sync_queue.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\sync_routes.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py`

### Likely Useful
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\home_adapter.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\cloud_adapter.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\event_ledger\writer.py`

---

## Deliverables Required

1. **Auto-start integration**
   - Modify `hivenode/main.py` to start sync worker as background task on startup
   - Must not block hivenode startup
   - Must not crash hivenode if Railway is down

2. **SyncQueue flush logic**
   - Integrate SyncQueue flush into each sync cycle
   - Log flush results (success count, failure count)
   - Handle offline mode: queue accumulates, flushes on reconnect

3. **Conflict handling**
   - Log conflicts to Event Ledger when last-write-wins resolves them
   - Surface conflicts via `/sync/conflicts` endpoint so users can review

4. **RTD events**
   - Emit sync status events for build monitor
   - Include sync cycle status, queue depth, conflicts

5. **Tests** (TDD)
   - Auto-start test: verify sync worker starts with hivenode
   - Flush test: verify SyncQueue flushes on each cycle
   - Offline/online transition tests
   - Conflict surfacing test
   - Graceful shutdown test

---

## Acceptance Criteria (from spec)

- [ ] Sync worker starts automatically with hivenode
- [ ] Sync runs on configurable interval (default 60s)
- [ ] SyncQueue flushes to cloud when reachable
- [ ] Offline mode: queue accumulates, flushes on reconnect
- [ ] Graceful shutdown (no orphan sync processes)
- [ ] Conflicts logged to Event Ledger
- [ ] Tests for auto-start, flush, offline/online transitions

---

## Constraints

- TDD: tests first, then implementation
- 500-line limit per file (hard limit: 1,000)
- Python 3.13
- Default sync interval: 60 seconds (configurable)
- Sync home:// <-> cloud:// by default
- Must not block hivenode startup
- Must not crash hivenode if Railway is down

---

## Dependencies

This spec depends on SPEC-CLOUD-STORAGE-RAILWAY being complete. The cloud storage adapter must be functional.

---

## Task File Requirements

Write task files to `.deia/hive/tasks/` following the standard format from HIVE.md:
- Absolute file paths only
- Specific test requirements (how many tests, which scenarios)
- 8-section response file requirement
- No stubs or TODOs allowed

Return task files to me (Q88NR) for review BEFORE dispatching bees.

---

## Model Assignment

Use **sonnet** for this work (as specified in the spec).

---

## Next Steps

1. Read the files listed above
2. Understand the current sync architecture
3. Design the integration approach
4. Write task files
5. Return to Q88NR (me) for review
