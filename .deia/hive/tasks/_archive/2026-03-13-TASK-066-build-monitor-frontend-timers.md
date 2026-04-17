# TASK-066: Build Monitor Frontend Elapsed Timers

**Spec ID:** QUEUE-TEMP-2026-03-13-2010-SPEC-build-monitor-fixes
**Model:** sonnet
**Priority:** P0

---

## Objective

Add live elapsed timers to RUNNING tasks in the left panel. Show duration + tokens for completed tasks.

---

## Files to Read

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\buildMonitorAdapter.tsx` — current UI

---

## Deliverables (absolute paths)

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\buildMonitorAdapter.tsx` — MODIFIED
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\buildMonitorAdapter.test.tsx` — MODIFIED

---

## Acceptance Criteria

### Elapsed time formatting helper (buildMonitorAdapter.tsx)
- [ ] Create `formatElapsed(milliseconds: number): string` function
- [ ] Return format: `"4m 32s"` (minutes + seconds)
- [ ] If < 60s: return `"32s"`
- [ ] If >= 60s: return `"4m 32s"`
- [ ] If >= 60m: return `"72m 15s"` (do NOT convert to hours)

### Live timer for RUNNING tasks (buildMonitorAdapter.tsx)
- [ ] Add `useEffect` hook that runs `setInterval()` every 1 second when `status` contains RUNNING tasks
- [ ] For each RUNNING task, calculate elapsed time from `task.first_seen` to `Date.now()`
- [ ] Display elapsed time in the task entry: `"RUNNING 4m 32s"`
- [ ] Timer updates every second (via state update or re-render)
- [ ] Clear interval on component unmount or when no tasks are RUNNING

### Duration display for COMPLETE/FAILED tasks (buildMonitorAdapter.tsx)
- [ ] For completed tasks, calculate duration from `task.first_seen` to `task.last_seen`
- [ ] Display duration in task entry metadata line
- [ ] Display tokens alongside duration: `"7m 14s, 12,430↑ 3,210↓"`

### Log entry completion display (buildMonitorAdapter.tsx)
- [ ] When a task completes (status = "complete"), the log entry should show duration + tokens
- [ ] Format: `"COMPLETE — 7m 14s, 12,430↑ 3,210↓"`
- [ ] Duration calculated from task's `first_seen` to heartbeat `timestamp`
- [ ] Tokens from heartbeat entry's `input_tokens` and `output_tokens`

---

## Tests (buildMonitorAdapter.test.tsx)

Add 3+ tests:
- [ ] Test `formatElapsed(32000)` returns `"32s"`
- [ ] Test `formatElapsed(272000)` returns `"4m 32s"` (4 * 60 + 32 = 272 seconds)
- [ ] Test `formatElapsed(4335000)` returns `"72m 15s"` (72 * 60 + 15 = 4335 seconds)

Run existing tests:
- [ ] All existing buildMonitorAdapter tests pass

---

## Constraints

- Keep buildMonitorAdapter.tsx under 500 lines — current is ~323, adding timers will push it higher. Extract helpers if needed.
- Do NOT change SSE event handling logic
- All colors use `var(--sd-*)` CSS variables

---

## TDD Protocol

1. Write 3+ tests for `formatElapsed()` helper
2. Run tests (should fail)
3. Implement `formatElapsed()` helper
4. Add `useEffect` + `setInterval` for live timers
5. Add duration display for completed tasks
6. Update log entry rendering for completion messages
7. Run tests (should pass)
8. Visual smoke test: verify live timers update every second

---

## Definition of Done

- [ ] All acceptance criteria met
- [ ] 3+ tests written and passing
- [ ] All colors use CSS variables
- [ ] Live timers for RUNNING tasks
- [ ] Duration + tokens for completed tasks
- [ ] Log entries show duration on completion
- [ ] Response file written to `.deia/hive/responses/`
