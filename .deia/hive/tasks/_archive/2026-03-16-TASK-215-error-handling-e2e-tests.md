# TASK-215: E2E Error Handling Smoke Tests

## Objective
Write end-to-end tests that verify error handling works across the full stack: missing API key, server unreachable, bad responses, pane crashes.

## Context
This task validates that all previous error handling tasks (TASK-211, TASK-212, TASK-213, TASK-214) work together. The smoke tests from the spec:
- Remove API key → send message → terminal shows "No API key configured" with link to settings
- Kill hivenode → send message → terminal shows connection error, not crash

These tests verify the complete error flow from provider → terminal → UI.

**Dependencies:** This task MUST run AFTER TASK-211, TASK-212, TASK-213, TASK-214 are complete.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\terminal-canvas-e2e.test.tsx` (example E2E test structure)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalApp.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneContent.tsx`
- Test files from TASK-211, TASK-212, TASK-213, TASK-214

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\terminal-error-e2e.test.tsx`
  - Test 1: No API key → submit message → "No API key configured" shown with settings link
  - Test 2: API key present, mock fetch to fail with network error → "Cannot reach server" shown
  - Test 3: API key present, mock fetch to return 401 → "Authentication failed" shown with API key suggestion
  - Test 4: API key present, mock fetch to return 429 → "Rate limit exceeded" shown
  - Test 5: API key present, mock fetch to return 500 → "Something went wrong" shown
  - Test 6: API key present, mock fetch to timeout → "Request timed out" shown
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\pane-error-e2e.test.tsx`
  - Test 1: Pane component throws during render → error boundary catches → error UI shown in pane
  - Test 2: Retry button in error boundary → error cleared → component remounts successfully
  - Test 3: Multiple panes crash → each shows own error (no cross-contamination)
- [ ] Update existing terminal tests to verify error styling
  - System messages with level='error' → rendered with `.terminal-error` class
  - Error messages use var(--sd-red) color
  - Warning messages use var(--sd-yellow) color

## Test Requirements
- [ ] Tests written FIRST (TDD) — NOTE: This task is exception, tests come AFTER implementation tasks
- [ ] All tests pass
- [ ] Edge cases:
  - No onOpenSettings callback → error message shown without link (graceful degradation)
  - Fetch throws non-standard error → classified as unknown, generic message shown
  - Error boundary retry throws again → error UI shown again (no infinite loop)
  - Provider error without statusCode → falls back to error message classification

## Expected Test Count
**9+ tests total** (6 terminal error scenarios + 3 pane error scenarios)

## Constraints
- No file over 500 lines
- No stubs
- Must use vitest mocking (`vi.mock`) for fetch and component errors
- Tests must verify both error detection AND user-facing message
- Tests must verify CSS classes applied (terminal-error, terminal-warning)
- Don't test internal implementation details, test observable behavior

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-215-RESPONSE.md`

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
