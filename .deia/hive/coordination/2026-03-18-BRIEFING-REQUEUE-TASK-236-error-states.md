# BRIEFING: TASK-236 RE-QUEUE — Error States Integration

**From:** Q33NR (REGENT-QUEUE-TEMP-2026-03-18-SPEC-REQ)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-18
**Model Assignment:** sonnet
**Priority:** P1

---

## Objective

Integrate the existing error classifier and error message formatter throughout the terminal component and PaneErrorBoundary so all error paths produce user-friendly categorized messages.

## Why This Is a Re-Queue

The previous bee (TASK-236) created excellent error infrastructure (`errorClassifier.ts` and `errorMessages.ts`) but only wired it into **ONE** error path out of ~5. The infrastructure exists and is tested, but it's underutilized.

**What exists:**
- `browser/src/primitives/terminal/errorClassifier.ts` (88 lines) — categorizes errors into 7 types
- `browser/src/primitives/terminal/errorMessages.ts` (68 lines) — generates friendly messages with suggestions
- Both imported in `useTerminal.ts` (lines 22-23)
- Used at line ~483 (relay error handling only)
- Tests exist and pass: `errorClassifier.test.ts`, `errorMessages.test.ts`, `errorIntegration.test.tsx`

**What's missing:**
1. Error classifier not used in other terminal error paths (shell execution errors, canvas routing errors, main LLM request errors)
2. PaneErrorBoundary doesn't use error classifier for categorized display
3. Terminal error display doesn't show categorized/friendly messages in most error cases

---

## Context from Codebase

### Current Error Paths in useTerminal.ts

I've identified **5 error catch blocks** in `useTerminal.ts`:

1. **Line 413** — Shell command execution errors
   - Currently: Basic error string display
   - Should use: `classifyError()` + `getErrorMessage()`

2. **Line 483** — Relay message sending errors
   - ✅ ALREADY USES classifier and formatter (this is the only one done)

3. **Line 560** — Canvas routing errors (IR mode)
   - Currently: Basic error string display
   - Should use: `classifyError()` + `getErrorMessage()`

4. **Line 764** — Main LLM request errors
   - Currently: Uses `classifyError()` and `getErrorMessage()`
   - ✅ ALREADY INTEGRATED

5. **Parse errors** (lines 667-674, 679-681) — envelope parsing warnings
   - Currently: Console warnings only
   - Consider: Should these surface to user?

**So actually 2 out of 4 critical paths already use the classifier.** Need to integrate into shell execution (line 413) and canvas routing (line 560).

### PaneErrorBoundary Current State

File: `browser/src/shell/components/PaneErrorBoundary.tsx` (158 lines)

Currently shows:
- Generic "Something went wrong" message
- App type + pane ID
- Raw `error.message` in red box
- Retry button

Should show:
- Categorized error message using `classifyError()`
- Friendly user message using `getErrorMessage()`
- Actionable suggestion if available
- Still include retry button

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\errorClassifier.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\errorMessages.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (lines 400-420, 550-570)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneErrorBoundary.tsx`

## Files to Modify

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts`
   - Wire classifier into shell execution error path (line ~413)
   - Wire classifier into canvas routing error path (line ~560)

2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneErrorBoundary.tsx`
   - Import `classifyError` and `getErrorMessage`
   - Use classifier in render method to show categorized errors
   - Display suggestion if available

---

## Deliverables

Write ONE task file for a sonnet bee to:

1. **Integrate error classifier into remaining useTerminal.ts error paths:**
   - [ ] Shell execution errors (line ~413) use classifier + formatter
   - [ ] Canvas routing errors (line ~560) use classifier + formatter
   - [ ] Both display error message + suggestion in terminal entries

2. **Integrate error classifier into PaneErrorBoundary:**
   - [ ] Import and use `classifyError()` and `getErrorMessage()`
   - [ ] Display categorized error type
   - [ ] Show friendly message instead of raw `error.message`
   - [ ] Display actionable suggestion if available
   - [ ] Keep existing retry button

3. **Tests:**
   - [ ] All existing error tests still pass (`errorClassifier.test.ts`, `errorMessages.test.ts`, `errorIntegration.test.tsx`)
   - [ ] Add test coverage for shell execution error path
   - [ ] Add test coverage for canvas routing error path
   - [ ] Add tests for PaneErrorBoundary error categorization

4. **No stubs, no hardcoded colors, no files over 500 lines**

---

## Smoke Test Commands

```bash
# Terminal error classifier tests
cd browser && npx vitest run --reporter=verbose src/primitives/terminal/__tests__/errorClassifier.test.ts

# Error message formatter tests
cd browser && npx vitest run --reporter=verbose src/primitives/terminal/__tests__/errorMessages.test.ts

# Error integration tests
cd browser && npx vitest run --reporter=verbose src/primitives/terminal/__tests__/errorIntegration.test.tsx

# PaneErrorBoundary tests
cd browser && npx vitest run --reporter=verbose src/shell/components/__tests__/PaneErrorBoundary.test.tsx
```

---

## Constraints

- No file over 500 lines (modularize if needed)
- CSS: `var(--sd-*)` only — no hardcoded colors
- No stubs — every function fully implemented
- TDD — tests first, then implementation
- Do NOT recreate `errorClassifier.ts` or `errorMessages.ts` — they already exist
- Do NOT modify the classifier logic — only integrate it into more places

---

## Success Criteria

When complete:
- All terminal error paths use error classifier + formatter
- PaneErrorBoundary shows categorized, user-friendly error messages
- All existing error tests pass
- New tests cover the additional integration points
- Error suggestions are visible and helpful

---

## Response Requirements

The bee MUST write a response file to `.deia/hive/responses/20260318-TASK-236-REQUEUE-RESPONSE.md` with all 8 required sections:

1. Header (status, model, date)
2. Files Modified (absolute paths)
3. What Was Done (concrete changes)
4. Test Results (pass/fail counts)
5. Build Verification (test/build output)
6. Acceptance Criteria (from task, marked [x] or [ ])
7. Clock / Cost / Carbon (all three)
8. Issues / Follow-ups (edge cases, next tasks)

---

## Next Steps for Q33N

1. Read the 4 files listed in "Files to Read First"
2. Write ONE task file to `.deia/hive/tasks/` with:
   - Clear objective
   - Specific file paths (absolute)
   - Concrete deliverables
   - Test requirements
   - Smoke test commands
   - Response file requirements
3. Return task file to Q33NR for review
4. After Q33NR approval, dispatch sonnet bee
5. Review bee response for completeness
6. Report results to Q33NR

---

**Q33NR will review your task file before you dispatch. Do NOT dispatch until approved.**
