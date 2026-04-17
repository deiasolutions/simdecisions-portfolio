# TASK-065: Build Monitor Frontend Token Display

**Spec ID:** QUEUE-TEMP-2026-03-13-2010-SPEC-build-monitor-fixes
**Model:** sonnet
**Priority:** P0
**Depends on:** TASK-063 (backend token tracking)

---

## Objective

Display token data in the build monitor UI: header totals, log entries, task list. Format: "12,430↑ 3,210↓" (↑ = input, ↓ = output).

---

## Files to Read

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\buildMonitorAdapter.tsx` — current UI

---

## Deliverables (absolute paths)

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\buildMonitorAdapter.tsx` — MODIFIED
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\buildMonitorAdapter.test.tsx` — MODIFIED

---

## Acceptance Criteria

### Interfaces (buildMonitorAdapter.tsx)
- [ ] `HeartbeatEntry` interface includes `input_tokens?: number` and `output_tokens?: number`
- [ ] `TaskState` interface includes `input_tokens?: number` and `output_tokens?: number`
- [ ] `BuildStatus` interface includes `total_input_tokens?: number` and `total_output_tokens?: number`

### Token formatting helper (buildMonitorAdapter.tsx)
- [ ] Create `formatTokens(inputTokens: number | null | undefined, outputTokens: number | null | undefined): string | null` function
- [ ] Return `null` if both inputs are null/undefined/zero
- [ ] Format input as `"12,430↑"` (comma-separated thousands + up arrow)
- [ ] Format output as `"3,210↓"` (comma-separated thousands + down arrow)
- [ ] Combine as `"12,430↑ 3,210↓"` if both present
- [ ] If only input: return `"12,430↑"` (no down arrow)
- [ ] If only output: return `"3,210↓"` (no up arrow)

### Header display (buildMonitorAdapter.tsx)
- [ ] Add token display next to cost in header: `"12,430↑ 3,210↓"`
- [ ] Show `status.total_input_tokens` and `status.total_output_tokens` via `formatTokens()`
- [ ] Color: `var(--sd-cyan)` or `var(--sd-blue)`

### Log entry display (buildMonitorAdapter.tsx)
- [ ] Each log entry appends tokens if available: `formatTokens(entry.input_tokens, entry.output_tokens)`
- [ ] Display after message text, same color as message (or slightly dimmed)

### Task list display (buildMonitorAdapter.tsx)
- [ ] Each task in left panel shows tokens if available: `formatTokens(task.input_tokens, task.output_tokens)`
- [ ] Display on the metadata line (alongside model, cost, tests)

---

## Tests (buildMonitorAdapter.test.tsx)

Add 6+ tests:
- [ ] Test `formatTokens(1000, 2000)` returns `"1,000↑ 2,000↓"`
- [ ] Test `formatTokens(12430, 3210)` returns `"12,430↑ 3,210↓"`
- [ ] Test `formatTokens(500, 0)` returns `"500↑"` (no down arrow)
- [ ] Test `formatTokens(0, 800)` returns `"800↓"` (no up arrow)
- [ ] Test `formatTokens(null, null)` returns `null`
- [ ] Test `formatTokens(undefined, undefined)` returns `null`

Run existing tests:
- [ ] All existing buildMonitorAdapter tests pass

---

## Constraints

- Keep buildMonitorAdapter.tsx under 500 lines — extract `formatTokens()` helper if needed
- Do NOT change SSE event handling logic
- All colors use `var(--sd-*)` CSS variables

---

## TDD Protocol

1. Write 6+ tests for `formatTokens()` helper
2. Run tests (should fail)
3. Implement `formatTokens()` helper
4. Update interfaces (HeartbeatEntry, TaskState, BuildStatus)
5. Add token display to header, log entries, task list
6. Run tests (should pass)
7. Visual smoke test: verify tokens appear in UI

---

## Definition of Done

- [ ] All acceptance criteria met
- [ ] 6+ tests written and passing
- [ ] All colors use CSS variables
- [ ] Token display in header, log, and task list
- [ ] Formatting matches spec: "12,430↑ 3,210↓"
- [ ] Response file written to `.deia/hive/responses/`
