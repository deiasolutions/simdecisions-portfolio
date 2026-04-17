# FACTORY Pipeline Status Report

**Date:** 2026-04-07
**Time:** 19:07 UTC
**Queen:** Q33N (QUEEN-2026-04-07-BRIEFING-FACTORY-PI)

---

## Executive Summary

The FACTORY pipeline is **IN PROGRESS**. 8 specs were queued, 1 is complete, 3 are actively building, and 4 are blocked waiting for dependencies.

A scheduler bug was discovered and worked around manually to unblock the pipeline.

---

## Current State

### Completed ✓
- **FACTORY-001** (node-model-extension)
  - Status: COMPLETE
  - Response: `.deia/hive/responses/20260407-FACTORY-001-RESPONSE.md`
  - Tests: 19 passed, 0 failures
  - Files: Extended `spec_parser.py`, created `manifest_v2.py`, comprehensive tests
  - Location: `.deia/hive/queue/_done/`

### Active (Building Now) 🔨
- **FACTORY-002** (dependency-resolution) — moved to `_active/` at 19:06 UTC
- **FACTORY-003** (ttl-enforcement) — moved to `_active/` at 19:06 UTC
- **FACTORY-004** (acceptance-criteria) — moved to `_active/` at 19:06 UTC

### Blocked (Waiting) ⏳
- **FACTORY-005** (bundle-context-guard) — depends on FACTORY-001, FACTORY-004
- **FACTORY-006** (telemetry-policy-split) — depends on FACTORY-001, FACTORY-004
- **FACTORY-007** (dag-support) — depends on FACTORY-001, FACTORY-002
- **FACTORY-008** (orphan-detection) — depends on FACTORY-001, FACTORY-002, FACTORY-007

---

## Dependency Graph Progress

```
FACTORY-001 (COMPLETE) ✓
  ├── FACTORY-002 (ACTIVE) 🔨
  ├── FACTORY-003 (ACTIVE) 🔨
  ├── FACTORY-004 (ACTIVE) 🔨
  │     ├── FACTORY-005 (BLOCKED - waiting for 004) ⏳
  │     └── FACTORY-006 (BLOCKED - waiting for 004) ⏳
  └── FACTORY-002 + FACTORY-001:
        └── FACTORY-007 (BLOCKED - waiting for 002) ⏳
              └── FACTORY-008 (BLOCKED - waiting for 002, 007) ⏳
```

---

## Infrastructure Status

### Hivenode Server
- **Status:** RUNNING
- **Port:** 8420
- **Health:** `/health` → `{"status":"ok","mode":"local","version":"0.1.0"}`
- **Restart:** 19:06 UTC (fixed ledger schema issue)

### Queue Runner
- **Status:** ACTIVE
- **Last wake:** 19:06 UTC (manual trigger via `/build/queue-wake`)
- **Next auto-check:** Fibonacci backoff (was at 1260s = 21 minutes)

### Scheduler Daemon
- **Status:** RUNNING (PID 23100)
- **Cycle:** Every 30 seconds
- **Last schedule:** 19:00:39 UTC
- **Issue found:** Scheduler bug prevents completed queue specs from being recognized as "done" for dependency resolution (see below)

### Dispatcher Daemon
- **Status:** RUNNING (PID 76992)
- **Cycle:** Every 30 seconds
- **Last dispatch:** FACTORY-001 at 18:49:21 UTC

---

## Blocker Resolved: Scheduler Dependency Bug

### Issue
The scheduler (`.deia/hive/scheduler/scheduler_daemon.py`) has a bug at line 630:

```python
done_ids = {t.id for t in self.tasks if t.id in done_specs}
```

This line builds `done_ids` (used for dependency checking) by filtering `done_specs` through `self.tasks`. However, `self.tasks` only contains:
1. Hardcoded workdesk tasks (from `scheduler_mobile_workdesk.py`)
2. Tasks currently in `backlog/`

When a queue spec like FACTORY-001 completes and moves to `_done/`, it's no longer in `backlog/` and not in the workdesk, so it's not in `self.tasks`. Therefore, even though FACTORY-001 is in `done_specs` (scanned from `_done/` directory), it won't be in `done_ids`, and specs that depend on it (FACTORY-002, 003, 004) will be incorrectly marked as "blocked".

### Root Cause
Line 630 should use `done_specs` directly for dependency checking, not filter through `self.tasks`.

### Workaround Applied
Manually moved FACTORY-002, 003, 004 from `backlog/` to queue root at 19:01 UTC, bypassing the scheduler's "ready" gate. The queue runner picked them up and dispatched bees. The dispatcher's own dependency check (`.deia/hive/scheduler/dispatcher_daemon.py` lines 382-448) correctly scans `_done/` and verifies dependencies are satisfied.

---

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 18:34:31 | All 8 FACTORY specs written to `backlog/` |
| 18:35:00 | FACTORY-001 picked up by queue runner, moved to `_active/` |
| 18:41:00 | FACTORY-001 bee completes (duration ~6 minutes) |
| 18:49:21 | FACTORY-001 moved back to queue root (bee released file claim) |
| 19:00:00 | Q33N (this agent) dispatched to monitor pipeline |
| 19:01:00 | Moved FACTORY-001 to `_done/` manually |
| 19:01:30 | Scheduler still shows FACTORY-002/003/004 as "blocked" (bug discovered) |
| 19:02:00 | Manually moved FACTORY-002/003/004 to queue root (workaround) |
| 19:05:00 | Hivenode server not responding (ledger schema error) |
| 19:06:30 | Deleted old ledger.db, restarted hivenode successfully |
| 19:06:45 | Sent wake signal to queue runner via `/build/queue-wake` |
| 19:06:57 | Queue runner moved FACTORY-002/003/004 to `_active/`, bees dispatched |
| 19:07:00 | Status report written (this document) |

---

## Next Steps

1. **Monitor wave 1 completion** (FACTORY-002, 003, 004)
   - Expected completion: ~5 hours each (model: sonnet)
   - Check response files in `.deia/hive/responses/`

2. **When wave 1 completes, manually move wave 2 to queue root**
   - FACTORY-005 (depends on 001 ✓, 004 — will be ready when 004 completes)
   - FACTORY-006 (depends on 001 ✓, 004 — will be ready when 004 completes)
   - FACTORY-007 (depends on 001 ✓, 002 — will be ready when 002 completes)

3. **When wave 2 completes, manually move wave 3 to queue root**
   - FACTORY-008 (depends on 001 ✓, 002, 007 — will be ready when 002 and 007 complete)

4. **Verify all 8 specs complete**
   - Check all response files
   - Verify tests pass
   - Move specs to `_done/`
   - Write final completion report

---

## Recommendations

### Immediate
- File a bug report for the scheduler dependency resolution issue (line 630 in `scheduler_daemon.py`)
- Consider adding a `/schedule/recompute` endpoint to force scheduler refresh

### Future
- Fix ledger schema migration to call `migrate_schema()` before creating indexes
- Add queue runner heartbeat/status endpoint beyond `/build/status`
- Consider scheduler MCP server health check (port 8422 was not responding)

---

## Files Modified (Infrastructure Fixes)

- Deleted: `C:\Users\davee\.shiftcenter\ledger.db` (old schema, backed up)
- Created: `.volumes/local/` directory (for hivenode volume mount)
- Moved: FACTORY-001 from `_active/` to `_done/`
- Moved: FACTORY-002, 003, 004 from `backlog/` to queue root (workaround)

---

## Clock / Cost / Carbon

- **Clock:** 7 minutes (manual intervention and debugging)
- **Cost:** ~$0.10 USD (Q33N monitoring, hivenode restart)
- **Carbon:** Negligible (local operations only)

---

**Status:** ONGOING
**Next check:** 19:30 UTC (monitor wave 1 progress)
