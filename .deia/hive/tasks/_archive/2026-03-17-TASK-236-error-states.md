# TASK-236: Error States — Wire error classifier and messages into terminal UI

## Objective

Integrate the existing `errorClassifier.ts` and `errorMessages.ts` modules into `TerminalOutput.tsx` so that system error entries display user-friendly messages instead of raw error text. Ensure PaneErrorBoundary catches component crashes gracefully.

## Context

Three error modules exist but are NOT connected:
1. `errorClassifier.ts` — classifies 7 error types (api_unreachable, timeout, auth_failure, rate_limit, server_error, network_error, unknown)
2. `errorMessages.ts` — user-friendly messages with actionable suggestions
3. `terminal-errors.css` — CSS classes for error, warning, and suggestion styling

The terminal currently displays raw error text. The classifier and message modules exist but are not used.

**This is an INTEGRATION task, NOT a new feature.**

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\errorClassifier.ts` (88 lines) — error classification logic
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\errorMessages.ts` (68 lines) — user-friendly message formatter
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminal-errors.css` (31 lines) — error styling
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalOutput.tsx` (283 lines) — terminal output rendering
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\types.ts` (131 lines) — TerminalEntry type includes `suggestion` field
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneErrorBoundary.tsx` (158 lines) — React error boundary
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css` — global CSS variables (check for `--sd-yellow`)

## Deliverables

### 1. Wire error classifier into terminal error handling (INTEGRATION)

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalOutput.tsx`

When a TerminalEntry with `type: 'system'` and `level: 'error'` is rendered:
- Import and use `classifyError()` from `errorClassifier.ts`
- Import and use `getErrorMessage()` from `errorMessages.ts`
- Display the user-friendly message instead of raw error content
- Display the suggestion text using `.terminal-error-suggestion` class (already rendered on line 137-139)

**Implementation:**
- For entries with `level: 'error'`, pass `entry.content` to `classifyError()`
- Get the `ErrorMessageResult` from `getErrorMessage(errorType)`
- Display `ErrorMessageResult.message` as the main error text
- Display `ErrorMessageResult.suggestion` (if present) as the suggestion text

### 2. Add `--sd-yellow` CSS variable

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css`

TASK-233 was supposed to add this, but it's not present. Add it now:

```css
/* In both light and dark theme sections */
--sd-yellow: #f59e0b; /* Amber-500 for warnings */
```

Add this variable to BOTH the light and dark theme sections in `shell-themes.css`.

### 3. Verify PaneErrorBoundary behavior (TEST)

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\PaneErrorBoundary.test.tsx` (NEW)

Write tests to verify:
- Component crashes are caught
- Error message is displayed
- Retry button shows and works (resets error state)

### 4. Add tests for error integration

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\errorIntegration.test.tsx` (NEW)

Tests:
- Error classifier returns correct type for each error pattern (7 patterns)
- Terminal renders user-friendly message for error entries (not raw error text)
- Terminal displays suggestion text when provided

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All terminal and shell tests pass
- [ ] Edge cases covered:
  - System entry with `level: 'error'` — shows friendly message
  - System entry with `level: 'warning'` — shows original content (no classification)
  - System entry with `level: 'info'` — shows original content (no classification)
  - PaneErrorBoundary catches component crash
  - PaneErrorBoundary retry button resets state

## Acceptance Criteria

- [ ] `errorClassifier.ts` is imported and used in `TerminalOutput.tsx`
- [ ] `errorMessages.ts` is imported and used in `TerminalOutput.tsx`
- [ ] System entries with `level: 'error'` display user-friendly messages
- [ ] System entries with `level: 'error'` display actionable suggestions
- [ ] `--sd-yellow` is available in `shell-themes.css` (both light and dark themes)
- [ ] PaneErrorBoundary test file created with 3+ tests
- [ ] Error integration test file created with 7+ tests
- [ ] All terminal tests pass: `cd browser && npx vitest run src/primitives/terminal/`
- [ ] All shell tests pass: `cd browser && npx vitest run src/shell/`
- [ ] No hardcoded colors (Rule 3)
- [ ] No file over 500 lines (Rule 4)

## Constraints

- **Rule 3:** CSS variables only (`var(--sd-*)`), no hardcoded colors
- **Rule 4:** No file over 500 lines (hard limit: 1,000)
- **Rule 5:** TDD — tests first, then implementation
- **Rule 6:** NO STUBS — every function fully implemented

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260317-TASK-236-RESPONSE.md`

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

## Implementation Notes

1. **Only modify entries with `level: 'error'`** — do NOT classify warnings or info messages
2. **The `suggestion` field already exists** in the TerminalEntry type and is already rendered in TerminalOutput.tsx (lines 136-139)
3. **This is NOT a new feature** — you are wiring together existing modules
4. **PaneErrorBoundary is already working** — just write tests to verify it
5. **Import at the top of TerminalOutput.tsx:**
   ```typescript
   import { classifyError } from './errorClassifier';
   import { getErrorMessage } from './errorMessages';
   ```
6. **Use the classified message in the TerminalLine component** (around line 130-141)

## Test Command

```bash
cd browser && npx vitest run src/primitives/terminal/ && npx vitest run src/shell/
```
