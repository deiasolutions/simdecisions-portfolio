# Q33N BRIEFING: Build Monitor UI Fixes + Token/Timing Display

**From:** Q88NR-bot (regent)
**To:** Q33N (coordinator)
**Date:** 2026-03-13
**Spec ID:** QUEUE-TEMP-2026-03-13-2010-SPEC-build-monitor-fixes
**Priority:** P0

---

## Objective

Fix build monitor UI layout issues and add token/timing telemetry display throughout the stack.

---

## Context

The build monitor is a live SSE-based dashboard showing dispatch activity. Current issues:
- Log panel doesn't fill width (wasted space)
- Log messages truncate
- No token usage display
- No timing display for running tasks

The spec calls for:
1. **Layout fixes** — log panel fills all remaining width, no truncation
2. **Token tracking** — dispatch.py → build_monitor.py → buildMonitorAdapter.tsx
3. **Elapsed timers** — live countdown for RUNNING tasks
4. **Completion display** — show duration + tokens on COMPLETE

---

## Key Files

**Backend:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` — HeartbeatPayload model, BuildState class, SSE endpoint
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\dispatch\dispatch.py` — send_heartbeat function, result parsing after adapter.send_task()

**Frontend:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\buildMonitorAdapter.tsx` — SSE client, task list + log feed

---

## Acceptance Criteria (from spec)

### Layout fixes (buildMonitorAdapter.tsx)
- [ ] Log panel fills ALL remaining width to the right edge of the pane. No wasted space. Left panel is fixed-width, log panel is flex-grow.
- [ ] Log messages do NOT truncate. Full text, word-wrap if needed. No `text-overflow: ellipsis`, no `overflow: hidden` on message text.
- [ ] Each log entry shows the FULL spec name (not truncated) and the FULL message text.
- [ ] Timestamps in log entries show HH:MM:SS only. No date. Use `toLocaleTimeString()` or equivalent.

### Token data (dispatch.py → build_monitor.py → buildMonitorAdapter.tsx)
- [ ] In `dispatch.py`, after `adapter.send_task()` returns, parse `input_tokens` and `output_tokens` from the result/usage dict. Pass both to `send_heartbeat()` on completion.
- [ ] Update `send_heartbeat()` function signature to accept `input_tokens` and `output_tokens` (integers).
- [ ] Update `HeartbeatPayload` in `build_monitor.py` to include `input_tokens: Optional[int]` and `output_tokens: Optional[int]` fields.
- [ ] Update `BuildState.record_heartbeat()` to accumulate `input_tokens` and `output_tokens` per task and in totals.
- [ ] Build monitor header shows running token totals: "12,430↑ 3,210↓" format (↑ = input/up, ↓ = output/down).
- [ ] Each log entry shows tokens if available: "12,430↑ 3,210↓" appended to the message.

### Elapsed time (buildMonitorAdapter.tsx)
- [ ] Each RUNNING task in the left panel shows a live elapsed timer: "RUNNING 4m 32s". Updates every second via setInterval.
- [ ] Timer starts from the task's `first_seen` timestamp.
- [ ] Timer stops when task status changes from "running" to "complete" or "failed".

### Bee completion display
- [ ] When a bee completes, the log entry message includes duration and tokens: "COMPLETE — 7m 14s, 12,430↑ 3,210↓"
- [ ] The left panel task entry for completed tasks also shows duration and tokens in the same format.
- [ ] Duration is calculated from `first_seen` to `last_seen` timestamps.

### Token display format (everywhere)
- [ ] Input tokens displayed as number + ↑ (e.g. "12,430↑")
- [ ] Output tokens displayed as number + ↓ (e.g. "3,210↓")
- [ ] Numbers use comma formatting for thousands (e.g. 12430 → "12,430")
- [ ] Format used consistently in: header totals, log entries, left panel task entries

### CSS
- [ ] All colors use `var(--sd-*)` CSS variables only
- [ ] No hardcoded hex, rgb, or named colors

### Tests
- [ ] 5+ tests for token formatting helper (commas, ↑↓ symbols, zero handling, null handling)
- [ ] 2+ tests for timestamp formatting (HH:MM:SS only)
- [ ] 1+ test for elapsed time formatting (minutes + seconds)
- [ ] All existing build monitor tests still pass

---

## Constraints

- Do NOT change the heartbeat API contract in a breaking way — add new optional fields only
- Do NOT change the SSE event format — same event types, just richer data in the payload
- Keep buildMonitorAdapter.tsx under 500 lines — extract formatting helpers if needed
- Model assignment: **sonnet**

---

## Tasks for Q33N

1. **Break down into BEE tasks** — separate tasks for backend (dispatch.py + build_monitor.py), frontend (buildMonitorAdapter.tsx), and tests.
2. **Create task files** — one task per file or logical unit (backend token wiring, frontend layout fixes, frontend timers, tests).
3. **Specify test requirements** — number of tests, which files, which scenarios.
4. **Review against checklist** — ensure all acceptance criteria are covered by task deliverables.
5. **Submit tasks for approval** — I'll review before dispatching bees.

---

## Expected Output

- 3-5 task files in `.deia/hive/tasks/`
- Each task specifies:
  - Files to read
  - Deliverables (absolute paths)
  - Test requirements (count, files, scenarios)
  - Acceptance criteria from spec
- All tasks reference the spec ID: `QUEUE-TEMP-2026-03-13-2010-SPEC-build-monitor-fixes`

---

## Next Steps

1. Q33N reads this briefing
2. Q33N creates task files
3. Q33N reports completion
4. Q88NR reviews tasks (mechanical checklist)
5. Approve → dispatch bees

---

**Q88NR-bot**
