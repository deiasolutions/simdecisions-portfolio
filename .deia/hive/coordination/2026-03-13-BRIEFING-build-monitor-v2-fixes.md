# BRIEFING: Build Monitor v2 Fixes

**To:** Q33N (Coordinator)
**From:** Q88NR (Regent)
**Date:** 2026-03-13
**Priority:** P0
**Spec:** `.deia/hive/queue/2026-03-13-2100-SPEC-build-monitor-v2.md`

---

## Objective

Implement 7 independent fixes to the build monitor and queue infrastructure. Each fix is small, well-defined, and can be tested independently. Break these into separate task files for parallel or sequential execution.

---

## Context

The build monitor is a live dashboard that shows the state of the queue runner and dispatched bees. It receives heartbeats via POST /build/heartbeat, stores them in BuildState (in-memory), and streams them to the frontend via SSE.

The spec calls for 7 fixes. These are NOT all equal in size:

- **Small fixes (1-3 test cases, < 1 hour):** Fix 1, 2, 5, 8, 9, 13
- **Complex fix (5+ test cases, 2-4 hours):** Fix 11 (watchdog restart)

You should group small, related fixes into 1-2 task files. Fix 11 should be its own task file.

---

## Files to Read First

### Backend (Python)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` — heartbeat API, BuildState
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py` — send_heartbeat function
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\run_queue.py` — queue runner main loop
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\dispatch_handler.py` — watchdog, call_dispatch
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\spec_processor.py` — process_spec

### Frontend (TypeScript/React)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\buildMonitorAdapter.tsx` — monitor UI

### Tests
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_build_monitor.py` — backend heartbeat tests
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_run_queue.py` — queue runner tests
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\queue\tests\test_dispatch_handler.py` — watchdog tests
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\buildMonitorAdapter.test.tsx` — frontend tests

---

## Fix Grouping Strategy

I recommend **3 task files:**

### TASK-1: Backend heartbeat schema + Python buffering (Fixes 1, 5)
- Add `role` field to HeartbeatPayload (Fix 1)
- Add `flush=True` to all print() calls in run_queue.py, spec_processor.py, dispatch_handler.py (Fix 5)
- Test: heartbeat with role="B" stores role correctly
- Model: haiku

### TASK-2: Frontend display fixes (Fixes 2, 8, 9, 13)
- Role prefix in task entries + log entries (Fix 2)
- Total elapsed time in header (Fix 8)
- Duration display format: clock=X.Xm (Fix 9)
- Spec completion counter in header (Fix 13)
- Extract helper functions to a separate file if buildMonitorAdapter.tsx approaches 500 lines
- Test: render with mock data, verify all display formats
- Model: haiku

### TASK-3: Watchdog queen restart (Fix 11)
- When watchdog kills a stale queen, implement restart logic
- New queen polls /build/status to see completed tasks
- Max 2 restart attempts per queen session
- Add restart_count tracking in call_dispatch
- Test: mock stale heartbeat, verify process is killed and relaunched (mock the relaunch)
- Model: sonnet (most complex fix)

---

## Acceptance Criteria — Full Spec

Copy these into your task files as appropriate:

### Fix 1: Role labels in heartbeat messages
- [ ] `send_heartbeat()` in dispatch.py includes a `role` field: "Q" (queen), "B" (bee), or "QR" (queue runner)
- [ ] `HeartbeatPayload` in build_monitor.py gets `role: Optional[str]` field
- [ ] dispatch.py: pass role="B" for bee dispatches, role="Q" for queen dispatches
- [ ] run_queue.py: send heartbeats with role="QR" for queue-level events (wave_start, wave_end, budget warnings)
- [ ] Test: heartbeat with role="B" stores role in task state

### Fix 2: Role + task name display in monitor UI
- [ ] Left panel task entries show role prefix: "B: spec-name" or "Q: spec-name"
- [ ] Log entries show role prefix before the message: "[B] Writing: browser/src/foo.tsx"
- [ ] If role is null (legacy heartbeats), show no prefix
- [ ] Full spec/task name shown, not truncated
- [ ] Test: render with role="B", verify prefix appears

### Fix 5: Python stdout buffering fix
- [ ] All `print()` calls in `run_queue.py` use `flush=True`
- [ ] All `print()` calls in `spec_processor.py` use `flush=True`
- [ ] All `print()` calls in `dispatch_handler.py` use `flush=True`
- [ ] Test: not needed, this is a one-liner fix per print call

### Fix 8: Total elapsed time in header
- [ ] Build monitor header shows total elapsed time since first heartbeat in h:mm format (e.g. "1:04")
- [ ] Updates every second via setInterval
- [ ] Calculated from the earliest `first_seen` timestamp across all tasks
- [ ] Test: formatTotalTime helper returns "0:05" for 5 minutes, "1:30" for 90 minutes

### Fix 9: Duration display format
- [ ] Completion heartbeat message uses `clock=X.Xm` format instead of `duration=XXXs`
- [ ] In dispatch.py: change the completion heartbeat message from `f"duration={duration:.1f}s turns={turns}"` to `f"clock={duration/60:.1f}m turns={turns}"`
- [ ] In buildMonitorAdapter.tsx: completed task entries show duration in minutes (e.g. "7.2m")
- [ ] Test: formatClock helper returns "7.2m" for 432 seconds

### Fix 11: Watchdog queen restart
- [ ] In dispatch_handler.py: when watchdog kills a stale queen (no heartbeat for 15 min), instead of just returning TIMEOUT, implement restart logic
- [ ] On timeout: kill process, POST timeout heartbeat, then relaunch a NEW queen with the same queue directory
- [ ] New queen's task includes instruction: "Poll http://localhost:8420/build/status to see what tasks are already completed. Only process remaining work."
- [ ] Max 2 restart attempts per queen session. After 2 restarts, return TIMEOUT and let run_queue.py flag NEEDS_DAVE
- [ ] Add `restart_count` tracking in call_dispatch
- [ ] Test: mock stale heartbeat, verify process is killed and relaunched (mock the relaunch)

### Fix 13: Spec completion counter in header
- [ ] Build monitor header shows "3/20" style counter for queue progress
- [ ] In run_queue.py: send a heartbeat with message "queue_progress=3/20" (or similar) after each spec completes
- [ ] HeartbeatPayload gets `queue_total: Optional[int]` and `queue_completed: Optional[int]` fields
- [ ] BuildState tracks queue progress
- [ ] buildMonitorAdapter.tsx header shows "Specs: 3/20" next to cost and time
- [ ] Test: heartbeat with queue_total=20, queue_completed=3 shows in status

### General
- [ ] All existing tests still pass
- [ ] 10+ new tests across all fixes
- [ ] CSS uses `var(--sd-*)` only
- [ ] No file over 500 lines

---

## Smoke Test Plan

After all tasks complete, Q33N should verify:

- [ ] Run queue with 1 spec — monitor shows "B: spec-name" in entries
- [ ] Header shows total time in h:mm, spec counter "1/1"
- [ ] Completion message shows clock=X.Xm format
- [ ] No buffering issues in queue runner stdout

---

## Constraints

- **Do NOT break existing heartbeat API** — add new optional fields only
- **Do NOT modify buildMonitorAdapter.tsx beyond 500 lines** — extract helpers to a separate file if needed
- **Fix 11 (watchdog restart) is the most complex** — if it risks breaking the watchdog, implement it conservatively with good error handling
- **flush=True is a mechanical find-and-replace** — do not refactor the print statements, just add the kwarg

---

## Model Assignments

- TASK-1 (backend schema + buffering): **haiku**
- TASK-2 (frontend display): **haiku**
- TASK-3 (watchdog restart): **sonnet** (complex, needs careful error handling)

---

## Expected Task Files

Q33N should produce **3 task files**:

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-13-TASK-068-build-monitor-backend-role-buffering.md`
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-13-TASK-069-build-monitor-frontend-display.md`
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-13-TASK-070-watchdog-queen-restart.md`

---

## Test Requirements

Each task file must specify:

- Which test files to create/modify
- How many test cases to add
- Which scenarios to cover

Suggested test counts:

- TASK-068: 3 tests (role storage, role passthrough, flush behavior)
- TASK-069: 7 tests (role prefix, total time format, clock format, spec counter, legacy null role)
- TASK-070: 5 tests (stale detection, restart attempt 1, restart attempt 2, max retries, resume instruction)

Total: 15 new tests (meets "10+ new tests" requirement)

---

## What NOT To Do

- **Do NOT dispatch bees yet** — wait for Q33NR to review your task files first
- **Do NOT write code** — you are Q33N, not a bee (unless Q88N explicitly approves)
- **Do NOT create more than 3 task files** — the spec has 7 fixes, but they group naturally
- **Do NOT create task files for trivial changes** — Fix 5 (flush=True) is a 1-line change, but it's bundled with Fix 1 in TASK-068 for efficiency

---

## Next Steps

1. Read all the files listed in "Files to Read First"
2. Understand the current state of the build monitor and queue runner
3. Write the 3 task files to `.deia/hive/tasks/`
4. Return to Q33NR with a summary of the task files
5. Wait for Q33NR to review and approve
6. After approval, dispatch bees

---

## Questions?

If anything is unclear, ask Q33NR before writing task files. Do not proceed with assumptions.
