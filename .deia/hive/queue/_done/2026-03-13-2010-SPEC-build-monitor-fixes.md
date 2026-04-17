# SPEC: Build Monitor UI Fixes + Token/Timing Display

## Priority
P0

## Objective
Fix the build monitor UI layout and add token/timing data to heartbeats and display.

## Context
The build monitor lives at:
- Backend: `hivenode/routes/build_monitor.py` — heartbeat API, SSE stream, in-memory state
- Frontend: `browser/src/apps/buildMonitorAdapter.tsx` — EventSource SSE client, task list + log feed
- Dispatch: `.deia/hive/scripts/dispatch/dispatch.py` — sends heartbeats on dispatch/complete, parses adapter results

Files to read first:
- `browser/src/apps/buildMonitorAdapter.tsx` — current UI (task list left, log right)
- `hivenode/routes/build_monitor.py` — HeartbeatPayload model, BuildState, SSE endpoint
- `.deia/hive/scripts/dispatch/dispatch.py` — send_heartbeat function, result parsing after adapter.send_task()

## Acceptance Criteria

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

## Smoke Test
- [ ] Load `localhost:5173?egg=monitor` — log panel fills full width
- [ ] Log messages wrap, no truncation
- [ ] Timestamps show HH:MM:SS only
- [ ] Running tasks show live elapsed timer
- [ ] Completed tasks show duration + tokens

## Model Assignment
sonnet

## Constraints
- Do NOT change the heartbeat API contract in a breaking way — add new optional fields only
- Do NOT change the SSE event format — same event types, just richer data in the payload
- Keep buildMonitorAdapter.tsx under 500 lines — extract formatting helpers if needed
