# TASK-236-REQUEUE: Error States Integration (PaneErrorBoundary + Tests)

**Assigned to:** BEE (Sonnet)
**Priority:** P1
**Created:** 2026-03-18
**Depends on:** TASK-236 (error classifier infrastructure)

---

## Objective

Integrate the existing error classifier (`errorClassifier.ts`) and error message formatter (`errorMessages.ts`) into PaneErrorBoundary, and add test coverage for the existing useTerminal.ts integration points.

---

## Context

**CORRECTION TO BRIEFING:** The briefing stated that only 1 out of 5 error paths uses the classifier. This is INCORRECT. After reading `useTerminal.ts`, I found:

- ✅ Line 413-419: Shell execution errors — ALREADY uses `classifyError()` + `getErrorMessage()`
- ✅ Line 560-567: Canvas routing errors — ALREADY uses `classifyError()` + `getErrorMessage()`
- ✅ Line 764-780: Main LLM request errors — ALREADY uses `classifyError()` + `getErrorMessage()`

**3 out of 4 critical error paths already integrated.** The briefing was based on outdated line numbers.

**What's actually missing:**

1. **PaneErrorBoundary** (`browser/src/shell/components/PaneErrorBoundary.tsx`) — still shows raw `error.message` instead of categorized friendly messages
2. **Test coverage** for the existing useTerminal.ts integration points (shell execution, canvas routing)

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\errorClassifier.ts` (88 lines, exports `classifyError()`)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\errorMessages.ts` (68 lines, exports `getErrorMessage()`)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneErrorBoundary.tsx` (158 lines, needs classifier integration)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\errorClassifier.test.ts` (test pattern to follow)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\errorMessages.test.ts` (test pattern to follow)

---

## Deliverables

### 1. Integrate error classifier into PaneErrorBoundary

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneErrorBoundary.tsx`

- [ ] Import `classifyError` and `getErrorMessage` from `../../primitives/terminal/errorClassifier` and `../../primitives/terminal/errorMessages`
- [ ] In the render method (line ~60), classify the error: `const errorType = classifyError(error);`
- [ ] Generate friendly message: `const { message, suggestion } = getErrorMessage(errorType);`
- [ ] Replace the raw `error.message` display (line 125) with the friendly `message`
- [ ] Display the `suggestion` below the message if it exists (as a separate paragraph, use `var(--sd-text-muted)` color)
- [ ] Keep the existing retry button (lines 133-150)
- [ ] Keep the pane ID display (line 129-131)
- [ ] All styles use CSS variables (`var(--sd-*)`)

### 2. Add test coverage for useTerminal.ts error paths

**File to create:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\useTerminal.errorPaths.test.tsx`

Write tests for:

- [ ] **Shell execution errors** (line ~413 in useTerminal.ts)
  - Mock `executeShellCommand` to throw an error
  - Verify error is classified correctly
  - Verify friendly message appears in terminal entries
  - Verify suggestion is included

- [ ] **Canvas routing errors** (line ~560 in useTerminal.ts)
  - Mock canvas route to throw an error
  - Verify error is classified correctly
  - Verify "Canvas error:" prefix is present
  - Verify suggestion is included

- [ ] **Test multiple error types:**
  - Connection error (ECONNREFUSED) → `api_unreachable`
  - Timeout error → `timeout`
  - Auth error (401) → `auth_failure`
  - Unknown error → `unknown`

### 3. Add test coverage for PaneErrorBoundary

**File to create:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\PaneErrorBoundary.errorClassifier.test.tsx`

Write tests for:

- [ ] Component that throws an error is caught by boundary
- [ ] Error is classified correctly
- [ ] Friendly message is displayed (not raw error.message)
- [ ] Suggestion is displayed when available
- [ ] Retry button works (resets error state)
- [ ] Different error types show different messages (api_unreachable, timeout, auth_failure, unknown)

---

## Test Requirements

- [ ] **TDD approach:** Write tests FIRST, then implementation
- [ ] All existing error tests still pass:
  - `errorClassifier.test.ts`
  - `errorMessages.test.ts`
  - `errorIntegration.test.tsx`
- [ ] New test files have 100% coverage for:
  - useTerminal.ts error path integration (shell + canvas)
  - PaneErrorBoundary error classification
- [ ] Minimum 8 tests in `useTerminal.errorPaths.test.tsx`
- [ ] Minimum 6 tests in `PaneErrorBoundary.errorClassifier.test.tsx`
- [ ] All tests use proper mocking patterns (no real API calls)
- [ ] All tests verify both message AND suggestion fields

---

## Constraints

- **No file over 500 lines** (modularize if needed)
- **CSS:** Use `var(--sd-*)` only — no hardcoded colors
- **No stubs** — every function fully implemented
- **TDD** — tests first, then implementation
- **Do NOT modify** `errorClassifier.ts` or `errorMessages.ts` — they already exist and work
- **Do NOT modify** the error classification logic in useTerminal.ts (lines 413, 560, 764) — it's already correct

---

## Smoke Test Commands

```bash
# Existing error classifier tests (must still pass)
cd browser && npx vitest run --reporter=verbose src/primitives/terminal/__tests__/errorClassifier.test.ts

# Existing error message formatter tests (must still pass)
cd browser && npx vitest run --reporter=verbose src/primitives/terminal/__tests__/errorMessages.test.ts

# Existing error integration tests (must still pass)
cd browser && npx vitest run --reporter=verbose src/primitives/terminal/__tests__/errorIntegration.test.tsx

# NEW: useTerminal error path tests
cd browser && npx vitest run --reporter=verbose src/primitives/terminal/__tests__/useTerminal.errorPaths.test.tsx

# NEW: PaneErrorBoundary error classifier tests
cd browser && npx vitest run --reporter=verbose src/shell/components/__tests__/PaneErrorBoundary.errorClassifier.test.tsx
```

---

## Success Criteria

When complete:

- [ ] PaneErrorBoundary shows categorized, user-friendly error messages
- [ ] PaneErrorBoundary displays actionable suggestions when available
- [ ] All existing error tests pass (3 test files)
- [ ] New tests cover useTerminal.ts error paths (8+ tests)
- [ ] New tests cover PaneErrorBoundary error categorization (6+ tests)
- [ ] No hardcoded colors in PaneErrorBoundary
- [ ] Retry button still works in PaneErrorBoundary
- [ ] Total new test count: 14+ tests passing

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-TASK-236-REQUEUE-RESPONSE.md`

The response MUST contain these 8 sections:

1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full absolute paths
3. **What Was Done** — bullet list of concrete changes (not intent)
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

---

## Additional Context

**Error types supported (from errorClassifier.ts):**
- `api_unreachable` — ECONNREFUSED, ENOTFOUND, connection errors
- `timeout` — timeout, timed out, abort
- `auth_failure` — 401, 403, "No API key"
- `rate_limit` — 429, rate limit exceeded
- `server_error` — 5xx status codes
- `network_error` — network offline, failed to fetch
- `unknown` — fallback for unrecognized errors

**Error message format (from errorMessages.ts):**
```typescript
interface ErrorMessageResult {
  message: string;      // User-friendly description
  suggestion?: string;  // Actionable recommendation
}
```

**Integration pattern (already used in useTerminal.ts):**
```typescript
const errorType = classifyError(error);
const { message, suggestion } = getErrorMessage(errorType, error);
setEntries((prev) => [
  ...prev,
  { type: 'system', content: message, level: 'error', suggestion }
]);
```

---

## End of Task File
