# TASK-069: Build Monitor Frontend — Display Fixes

## Objective
Add role prefixes to task/log entries, total elapsed time in header, duration format changes, and spec completion counter.

## Context
The build monitor UI needs four display improvements:
1. **Role prefix** — Show "B:", "Q:", "QR:" before task names and log entries
2. **Total elapsed time** — Show "1:04" style time in header (h:mm format)
3. **Duration format** — Show "7.2m" instead of "432s" for completed tasks
4. **Spec completion counter** — Show "3/20" in header for queue progress

All fixes are frontend-only. Backend changes are in TASK-068 (role field) and will be available when this task runs.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\buildMonitorAdapter.tsx` — monitor UI
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` — backend schema reference
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py` — heartbeat message format

## Deliverables

### Role Prefix Display (Fix 2)
- [ ] Left panel task entries show role prefix: "B: spec-name" or "Q: spec-name"
- [ ] Log entries show role prefix before the message: "[B] Writing: browser/src/foo.tsx"
- [ ] If role is null (legacy heartbeats), show no prefix
- [ ] Full spec/task name shown, not truncated

### Total Elapsed Time (Fix 8)
- [ ] Build monitor header shows total elapsed time since first heartbeat in h:mm format (e.g. "1:04")
- [ ] Updates every second via setInterval
- [ ] Calculated from the earliest `first_seen` timestamp across all tasks
- [ ] Helper function: `formatTotalTime(milliseconds: number): string` returns "0:05" for 5 minutes, "1:30" for 90 minutes

### Duration Display Format (Fix 9)
- [ ] Completed task entries show duration in minutes (e.g. "7.2m")
- [ ] Change from existing formatElapsed() to new formatClock() helper
- [ ] Helper function: `formatClock(seconds: number): string` returns "7.2m" for 432 seconds
- [ ] Use formatClock for completed task duration display

### Spec Completion Counter (Fix 13)
- [ ] Build monitor header shows "Specs: 3/20" next to cost and time
- [ ] Read from BuildStatus.queue_total and BuildStatus.queue_completed (added by backend in TASK-068)
- [ ] If queue_total is null/undefined, don't show counter
- [ ] Counter updates when new heartbeats arrive with queue progress data

### Modularization (if needed)
- [ ] If buildMonitorAdapter.tsx exceeds 500 lines after changes, extract helpers to separate file
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\buildMonitorHelpers.ts`
- [ ] Export formatClock, formatTotalTime, formatTokens, formatElapsed, formatTime, formatCost

## Test Requirements

### Test File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\buildMonitorAdapter.test.tsx`
Create new test file with test cases:
- [ ] `test_role_prefix_bee` — Render with task.role="B", verify "B: task-name" appears
- [ ] `test_role_prefix_queen` — Render with task.role="Q", verify "Q: task-name" appears
- [ ] `test_role_prefix_null` — Render with task.role=null, verify no prefix appears
- [ ] `test_total_time_format` — formatTotalTime(300000) returns "0:05", formatTotalTime(5400000) returns "1:30"
- [ ] `test_clock_format` — formatClock(432) returns "7.2m", formatClock(60) returns "1.0m"
- [ ] `test_spec_counter_display` — Render with queue_total=20, queue_completed=3, verify "Specs: 3/20" appears
- [ ] `test_spec_counter_null` — Render with queue_total=null, verify counter doesn't appear

### Edge Cases
- [ ] Role is null/undefined (legacy heartbeats)
- [ ] queue_total is null/undefined (no queue context)
- [ ] Total elapsed time updates every second (verify setInterval works)
- [ ] Duration format handles fractional minutes correctly

## Constraints
- **No file over 500 lines** — extract helpers if buildMonitorAdapter.tsx exceeds 500 lines
- **CSS: var(--sd-*) only** — all colors must use CSS variables
- **No stubs** — all functions fully implemented
- **Do NOT break existing display** — all current features still work

## Acceptance Criteria

### Fix 2: Role + task name display in monitor UI
- [ ] Left panel task entries show role prefix: "B: spec-name" or "Q: spec-name"
- [ ] Log entries show role prefix before the message: "[B] Writing: browser/src/foo.tsx"
- [ ] If role is null (legacy heartbeats), show no prefix
- [ ] Full spec/task name shown, not truncated
- [ ] Test: render with role="B", verify prefix appears

### Fix 8: Total elapsed time in header
- [ ] Build monitor header shows total elapsed time since first heartbeat in h:mm format (e.g. "1:04")
- [ ] Updates every second via setInterval
- [ ] Calculated from the earliest `first_seen` timestamp across all tasks
- [ ] Test: formatTotalTime helper returns "0:05" for 5 minutes, "1:30" for 90 minutes

### Fix 9: Duration display format
- [ ] Completed task entries show duration in minutes (e.g. "7.2m")
- [ ] Test: formatClock helper returns "7.2m" for 432 seconds

### Fix 13: Spec completion counter in header
- [ ] Build monitor header shows "Specs: 3/20" next to cost and time
- [ ] Counter updates when queue progress heartbeats arrive
- [ ] If queue_total is null, counter doesn't appear
- [ ] Test: render with queue_total=20, queue_completed=3, verify "Specs: 3/20" appears

### General
- [ ] All existing tests still pass
- [ ] CSS uses `var(--sd-*)` only
- [ ] No file over 500 lines

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260313-TASK-069-RESPONSE.md`

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

## Model Assignment
haiku

## Test Commands
```bash
# Frontend tests
cd browser && npx vitest run src/apps/__tests__/buildMonitorAdapter.test.tsx
```

## Notes
- Backend changes (role field, queue_total/queue_completed fields) are in TASK-068
- This task assumes TASK-068 is complete and backend schema includes role field
- If backend fields are not yet available, mock them in tests and add TODO comments
