# SPEC: Build Monitor v2 — Role Labels, Timing, Watchdog Restart, Buffering

## Priority
P0

## Objective
Seven fixes for the build monitor and queue infrastructure. Each is small and independent.

## Context
Files to read first:
- `browser/src/apps/buildMonitorAdapter.tsx` — monitor UI
- `hivenode/routes/build_monitor.py` — heartbeat API, BuildState
- `.deia/hive/scripts/dispatch/dispatch.py` — send_heartbeat function
- `.deia/hive/scripts/queue/run_queue.py` — queue runner main loop
- `.deia/hive/scripts/queue/dispatch_handler.py` — watchdog, call_dispatch
- `.deia/hive/scripts/queue/spec_processor.py` — process_spec

## Acceptance Criteria

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

## Smoke Test
- [ ] Run queue with 1 spec — monitor shows "B: spec-name" in entries
- [ ] Header shows total time in h:mm, spec counter "1/1"
- [ ] Completion message shows clock=X.Xm format
- [ ] No buffering issues in queue runner stdout

## Model Assignment
sonnet

## Constraints
- Do NOT break existing heartbeat API — add new optional fields only
- Do NOT modify buildMonitorAdapter.tsx beyond 500 lines — extract helpers to a separate file if needed
- Fix 11 (watchdog restart) is the most complex — if it risks breaking the watchdog, implement it conservatively with good error handling
- flush=True is a mechanical find-and-replace — do not refactor the print statements, just add the kwarg
