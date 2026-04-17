# Q33N Report: Build Monitor v2 Task Files Created

**To:** Q33NR (Regent)
**From:** Q33N (Coordinator)
**Date:** 2026-03-13
**Briefing:** Build Monitor v2 Fixes
**Status:** Task files ready for review

---

## Summary

I have created **3 task files** to implement the 7 fixes specified in the build monitor v2 briefing. The fixes are grouped by complexity and dependency:

1. **TASK-068** (Backend) — Role labels + Python buffering (Fixes 1, 5)
2. **TASK-069** (Frontend) — Display improvements (Fixes 2, 8, 9, 13)
3. **TASK-070** (Watchdog) — Queen restart logic (Fix 11)

All task files follow the standard format with:
- Absolute file paths
- Test requirements with specific test counts
- 8-section response template
- Model assignments (haiku for 068/069, sonnet for 070)
- No stubs allowed
- 500-line file limit enforced

---

## Task File Breakdown

### TASK-068: Build Monitor Backend — Role Labels + Python Buffering
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-13-TASK-068-build-monitor-backend-role-buffering.md`
**Model:** haiku
**Fixes:** 1, 5
**Estimated Tests:** 3 new tests

**What it does:**
- Adds `role: Optional[str]` field to HeartbeatPayload schema
- Updates send_heartbeat() in dispatch.py to accept and pass role parameter
- Updates dispatch_bee() to send role="B" for bees, role="Q" for queens
- Adds queue runner heartbeats with role="QR" for queue-level events
- Adds flush=True to all print() calls in run_queue.py, spec_processor.py, dispatch_handler.py

**Test coverage:**
- Heartbeat with role="B" stores role in task state
- Heartbeat without role (legacy) still works
- Role appears in /build/status response

**Files modified:**
- hivenode/routes/build_monitor.py (schema + storage)
- .deia/hive/scripts/dispatch/dispatch.py (send_heartbeat signature)
- .deia/hive/scripts/queue/run_queue.py (flush=True, queue heartbeats)
- .deia/hive/scripts/queue/spec_processor.py (flush=True)
- .deia/hive/scripts/queue/dispatch_handler.py (flush=True)
- tests/hivenode/test_build_monitor.py (3 new tests)

---

### TASK-069: Build Monitor Frontend — Display Fixes
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-13-TASK-069-build-monitor-frontend-display.md`
**Model:** haiku
**Fixes:** 2, 8, 9, 13
**Estimated Tests:** 7 new tests

**What it does:**
- Shows role prefix in task entries: "B: task-name", "Q: task-name"
- Shows role prefix in log entries: "[B] message text"
- Adds total elapsed time in header (h:mm format, updates every second)
- Changes duration format from "432s" to "7.2m" for completed tasks
- Adds spec completion counter in header: "Specs: 3/20"
- Extracts helpers to separate file if buildMonitorAdapter.tsx exceeds 500 lines

**Test coverage:**
- Role prefix rendering (bee, queen, null)
- Total time format (formatTotalTime helper)
- Clock format (formatClock helper)
- Spec counter display
- Spec counter hidden when queue_total is null

**Files modified:**
- browser/src/apps/buildMonitorAdapter.tsx (display logic)
- browser/src/apps/buildMonitorHelpers.ts (helpers, if extracted)
- browser/src/apps/__tests__/buildMonitorAdapter.test.tsx (7 new tests)

**Dependency:** Assumes TASK-068 is complete (role field available in backend)

---

### TASK-070: Watchdog Queen Restart Logic
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-13-TASK-070-watchdog-queen-restart.md`
**Model:** sonnet
**Fixes:** 11
**Estimated Tests:** 5 new tests

**What it does:**
- When watchdog kills a stale queen (no heartbeat for 15 min), automatically restart the queen
- New queen receives resume instruction: "Poll /build/status to see completed tasks, finish remaining work"
- Max 2 restart attempts per queen session
- After 2 restarts, return TIMEOUT and let run_queue.py flag NEEDS_DAVE
- Adds restart_count tracking to call_dispatch()

**Test coverage:**
- Watchdog detects stale heartbeat
- Process is killed on timeout
- First restart attempt with resume instruction
- Second restart attempt
- Max retries (3rd timeout returns TIMEOUT without restart)
- Resume instruction format

**Files modified:**
- .deia/hive/scripts/queue/dispatch_handler.py (restart logic)
- .deia/hive/scripts/queue/tests/test_dispatch_handler.py (5 new tests)

**Complexity:** This is the most complex fix. Uses sonnet model for careful error handling.

---

## Total Test Count

- TASK-068: 3 tests
- TASK-069: 7 tests
- TASK-070: 5 tests
- **Total: 15 new tests** ✓ (meets "10+ new tests" requirement)

---

## Grouping Rationale

### Why 3 task files instead of 7?

**Original briefing suggested 3 task files:**
1. Backend schema + buffering (Fixes 1, 5)
2. Frontend display (Fixes 2, 8, 9, 13)
3. Watchdog restart (Fix 11)

This grouping makes sense because:

**TASK-068 (Backend):** Fixes 1 and 5 both touch Python backend code. Fix 5 (flush=True) is trivial, but bundling it with Fix 1 (role field) means we test the backend changes together in one pass.

**TASK-069 (Frontend):** Fixes 2, 8, 9, 13 are all UI display changes in buildMonitorAdapter.tsx. They share the same test file and can be implemented together without conflicts.

**TASK-070 (Watchdog):** Fix 11 is complex and risky. It touches watchdog logic, which is critical for queue runner stability. Needs its own task file, sonnet model, and thorough testing.

**Alternative grouping (rejected):**
- 7 separate task files (one per fix) would be overkill. Fixes 2, 8, 9, 13 are all small UI changes.
- 1 giant task file would be too large and hard to test atomically.

---

## Dispatch Order

I recommend **sequential dispatch** in this order:

1. **TASK-068** (backend) first — establishes role field and queue heartbeats
2. **TASK-069** (frontend) second — depends on role field from TASK-068
3. **TASK-070** (watchdog) third — independent, can run last

**Rationale:** TASK-069 expects role field to exist in backend. If we dispatch TASK-069 before TASK-068 completes, the frontend tests will fail because role is undefined. Sequential dispatch avoids this.

---

## Constraints Compliance

All task files enforce:
- ✓ No file over 500 lines (modularize if needed)
- ✓ CSS: var(--sd-*) only
- ✓ No stubs
- ✓ TDD (tests first)
- ✓ All file paths absolute
- ✓ 8-section response template
- ✓ Model assignments (haiku/sonnet)

---

## Smoke Test Plan (After All Tasks Complete)

When all 3 tasks are COMPLETE, Q33N should verify:

- [ ] Run queue with 1 spec — monitor shows "B: spec-name" in entries
- [ ] Header shows total time in h:mm format (e.g. "1:04")
- [ ] Header shows spec counter "1/1"
- [ ] Completion message shows clock=7.2m format (not duration=432s)
- [ ] No buffering issues in queue runner stdout (prints appear immediately)
- [ ] If a queen stalls for 15 min, watchdog restarts it (manual test)

---

## Next Steps

1. **Q33NR reviews these task files**
2. **Q33NR approves or requests corrections**
3. **Q33N dispatches bees after approval**

---

## Questions for Q33NR

1. **Dispatch order:** Should I dispatch TASK-068 → TASK-069 → TASK-070 sequentially, or can TASK-068 and TASK-070 run in parallel (both are backend)?
2. **Fix 13 (spec counter):** The spec says run_queue.py should send heartbeats with queue_total/queue_completed. Should this be in TASK-068 (backend) or is it okay to leave it in the frontend task as a note that backend changes are needed?
3. **Watchdog restart:** Fix 11 is complex. Should we implement it conservatively (fallback to old behavior on error) or aggressively (always try restart)?

---

**Q33N awaiting Q33NR review and approval to dispatch bees.**
