# TASK-064: Build Monitor Frontend Layout Fixes

**Spec ID:** QUEUE-TEMP-2026-03-13-2010-SPEC-build-monitor-fixes
**Model:** sonnet
**Priority:** P0

---

## Objective

Fix build monitor UI layout: log panel fills all remaining width, no truncation, timestamps show HH:MM:SS only. All colors use CSS variables.

---

## Files to Read

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\buildMonitorAdapter.tsx` — current UI (task list left, log right)

---

## Deliverables (absolute paths)

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\buildMonitorAdapter.tsx` — MODIFIED
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\buildMonitorAdapter.test.tsx` — NEW (if no test file exists, create it)

---

## Acceptance Criteria

### Layout fixes (buildMonitorAdapter.tsx)
- [ ] Log panel (`logStyle`) has `flex: 1` (fills remaining width)
- [ ] Task list panel (`tasksStyle`) has fixed width (280px) and `flexShrink: 0`
- [ ] Panel container (`panelStyle`) uses `display: flex`, no hardcoded widths on children
- [ ] Log panel goes all the way to the right edge — no wasted space

### Truncation fixes (buildMonitorAdapter.tsx)
- [ ] Log message text does NOT truncate — no `text-overflow: ellipsis` on message spans
- [ ] Log message text does NOT clip — no `overflow: hidden` on message spans
- [ ] Log message text wraps if needed — add `word-wrap: break-word` or `white-space: pre-wrap` if needed
- [ ] Task ID in left panel shows FULL text (remove the `.slice(0, 30) + '...'` logic)
- [ ] Task ID in log shows FULL text (remove the `.slice(0, 25) + '...'` logic)

### Timestamp formatting (buildMonitorAdapter.tsx)
- [ ] `formatTime()` function shows HH:MM:SS only — no date
- [ ] Use `toLocaleTimeString('en-US', { hour12: false })` or equivalent
- [ ] All log entry timestamps use `formatTime()`

### CSS variables (buildMonitorAdapter.tsx)
- [ ] All inline styles use `var(--sd-*)` for colors
- [ ] No hardcoded hex, rgb, or named colors
- [ ] Verify: `statusColor()` already returns CSS variables — no changes needed
- [ ] Verify all existing colors already use CSS vars — if any don't, fix them

---

## Tests (buildMonitorAdapter.test.tsx)

Add 3+ tests:
- [ ] Test `formatTime()` returns HH:MM:SS format (no date)
- [ ] Test log panel has `flex: 1` style
- [ ] Test task list panel has fixed width + `flexShrink: 0`

Run existing tests if any:
- [ ] All existing buildMonitorAdapter tests pass (if file exists)

---

## Constraints

- Keep buildMonitorAdapter.tsx under 500 lines — extract helpers if needed (not needed yet, current is 323 lines)
- Do NOT change SSE event handling logic — only layout/rendering

---

## TDD Protocol

1. Create test file if it doesn't exist
2. Write 3+ tests for formatting and layout
3. Run tests (should fail)
4. Implement changes in buildMonitorAdapter.tsx
5. Run tests (should pass)
6. Visual smoke test: load `localhost:5173?egg=monitor`, verify layout

---

## Definition of Done

- [ ] All acceptance criteria met
- [ ] 3+ tests written and passing
- [ ] All colors use CSS variables
- [ ] Log panel fills full width
- [ ] No truncation on messages or task IDs
- [ ] Timestamps show HH:MM:SS only
- [ ] Response file written to `.deia/hive/responses/`
