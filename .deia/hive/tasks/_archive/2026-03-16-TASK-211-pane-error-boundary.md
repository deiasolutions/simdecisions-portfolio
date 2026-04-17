# TASK-211: React Error Boundary for Pane Isolation

## Objective
Wrap each pane in a React error boundary so that one crashing pane doesn't take down the whole app.

## Context
Currently, if a pane throws an uncaught error during rendering, the entire shell crashes. We need a React error boundary component that:
- Catches errors thrown by child components
- Displays a user-friendly error message in the pane
- Logs the error for debugging
- Provides a retry/refresh button
- Uses CSS variables for styling (var(--sd-*))

React error boundaries use `componentDidCatch` and `getDerivedStateFromError` lifecycle methods, which are only available in class components.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneContent.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts`

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneErrorBoundary.tsx`
  - Class component with `componentDidCatch` and `getDerivedStateFromError`
  - State: `{ hasError: boolean, error: Error | null, errorInfo: ErrorInfo | null }`
  - Error UI: shows pane name, error message (user-friendly), retry button
  - Retry button clears error state and remounts children
  - Console.error logs full error + errorInfo for debugging
- [ ] Wrap pane content in PaneContent.tsx with PaneErrorBoundary
  - Pass paneId and appType to error boundary for error message
- [ ] Create CSS styles in `shell.css` for error boundary UI
  - Use var(--sd-red), var(--sd-text-primary), var(--sd-text-secondary)
  - Center error message in pane
  - Make retry button use var(--sd-orange) hover
- [ ] Export PaneErrorBoundary from `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\index.ts`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Component throws error during render → error boundary catches and shows UI
  - Retry button click → error state cleared, component remounts
  - Multiple panes crash → each shows its own error (no cross-pane contamination)
  - Error in error boundary itself → fallback to browser error page (document in test comments)
  - Error info logged to console with full stack trace

## Test File
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\PaneErrorBoundary.test.tsx`

Expected test count: **6+ tests**

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (no hex, no rgb(), no named colors)
- No stubs
- Class component required (React error boundaries can't be hooks)
- Error message must be user-friendly (no raw stack traces in UI)
- Preserve full error info in console.error for debugging

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-211-RESPONSE.md`

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
