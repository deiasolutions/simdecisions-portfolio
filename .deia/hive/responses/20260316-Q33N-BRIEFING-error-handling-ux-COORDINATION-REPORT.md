# Q33N Coordination Report: User-Facing Error Handling

**Date:** 2026-03-16
**From:** Q33N (Bot ID: QUEEN-2026-03-16-BRIEFING-error-hand)
**To:** Q33NR
**Status:** TASK FILES READY FOR REVIEW

---

## Summary

I have analyzed the codebase and created **5 task files** to implement user-facing error handling across the shell and terminal. The tasks cover:
1. React error boundaries for pane isolation
2. Terminal error message classification and rendering
3. Applet load failure UX with retry
4. Enhanced LLM provider error detection
5. E2E smoke tests for error scenarios

All tasks follow TDD, use CSS variables, and include 5+ tests as required by the spec.

---

## Task Files Created

### TASK-186: React Error Boundary for Pane Isolation
**File:** `.deia/hive/tasks/2026-03-16-TASK-186-pane-error-boundary.md`
**Model:** Haiku
**Deliverables:**
- PaneErrorBoundary.tsx (class component with componentDidCatch)
- Wraps pane content in PaneContent.tsx
- Error UI with retry button
- CSS styling with var(--sd-*) colors
- 6+ tests

**Dependencies:** None (can run immediately)

---

### TASK-187: Terminal Error Message Rendering (User-Friendly)
**File:** `.deia/hive/tasks/2026-03-16-TASK-187-terminal-error-messages.md`
**Model:** Haiku
**Deliverables:**
- errorClassifier.ts (classifies errors by type)
- errorMessages.ts (maps error types to user-friendly messages)
- Updated useTerminal.ts catch blocks to use classifier
- terminal.css error styling (var(--sd-red), var(--sd-yellow))
- Enhanced TerminalEntry type with optional level field
- 8+ tests (5 classifier, 3 message formatter)

**Dependencies:** None (can run in parallel with TASK-186)

---

### TASK-188: Applet Load Failure UX with Retry
**File:** `.deia/hive/tasks/2026-03-16-TASK-188-applet-load-failure-ux.md`
**Model:** Haiku
**Deliverables:**
- AppletLoadError.tsx (load failure UI component)
- Updated PaneContent.tsx to detect load failures
- CSS styling for load error UI
- 5+ tests

**Dependencies:** TASK-186 (PaneErrorBoundary) should run first for consistency

---

### TASK-189: Enhanced Error Detection in LLM Providers
**File:** `.deia/hive/tasks/2026-03-16-TASK-189-llm-provider-error-detection.md`
**Model:** Haiku
**Deliverables:**
- errors.ts (ProviderError class and factory functions)
- Updated anthropic.ts, groq.ts, openai-compatible.ts catch blocks
- Preserves HTTP status codes and error types
- 8+ tests

**Dependencies:** None (can run in parallel with TASK-186, TASK-187)

---

### TASK-190: E2E Error Handling Smoke Tests
**File:** `.deia/hive/tasks/2026-03-16-TASK-190-error-handling-e2e-tests.md`
**Model:** Haiku
**Deliverables:**
- terminal-error-e2e.test.tsx (6 terminal error scenarios)
- pane-error-e2e.test.tsx (3 pane error scenarios)
- 9+ tests total

**Dependencies:** MUST run AFTER TASK-186, TASK-187, TASK-188, TASK-189 are complete

---

## Coverage vs Spec Acceptance Criteria

| Spec Requirement | Covered By | Status |
|-----------------|------------|--------|
| Applet load failure UI | TASK-188 | ✅ |
| API unreachable error | TASK-187, TASK-189, TASK-190 | ✅ |
| LLM error (bad key, rate limit) | TASK-187, TASK-189, TASK-190 | ✅ |
| 500 error from hivenode | TASK-187, TASK-189, TASK-190 | ✅ |
| Network timeout | TASK-187, TASK-189, TASK-190 | ✅ |
| React error boundary per pane | TASK-186 | ✅ |
| CSS var(--sd-*) colors only | All tasks | ✅ |
| 5+ tests | TASK-190 (9 tests) + others = 32+ total | ✅ |
| Smoke: No API key | TASK-190 test 1 | ✅ |
| Smoke: Kill hivenode | TASK-190 test 2 | ✅ |

---

## Execution Plan (After Approval)

**Sequential execution order:**

1. **Wave 1 (parallel):**
   - TASK-186 (PaneErrorBoundary)
   - TASK-187 (Terminal error messages)
   - TASK-189 (Provider error detection)

2. **Wave 2 (depends on TASK-186):**
   - TASK-188 (Applet load failure UX)

3. **Wave 3 (integration verification):**
   - TASK-190 (E2E smoke tests)

Total estimated time: ~2-3 hours (Haiku execution)

---

## Test Count Summary

| Task | Test Count |
|------|-----------|
| TASK-186 | 6+ |
| TASK-187 | 8+ |
| TASK-188 | 5+ |
| TASK-189 | 8+ |
| TASK-190 | 9+ |
| **TOTAL** | **36+ tests** |

This exceeds the spec requirement of 5+ tests.

---

## Files That Will Be Modified/Created

**New files:**
- `browser/src/shell/components/PaneErrorBoundary.tsx`
- `browser/src/shell/components/AppletLoadError.tsx`
- `browser/src/primitives/terminal/errorClassifier.ts`
- `browser/src/primitives/terminal/errorMessages.ts`
- `browser/src/services/terminal/providers/errors.ts`
- `browser/src/shell/components/__tests__/PaneErrorBoundary.test.tsx`
- `browser/src/shell/components/__tests__/AppletLoadError.test.tsx`
- `browser/src/shell/components/__tests__/pane-error-e2e.test.tsx`
- `browser/src/primitives/terminal/__tests__/errorClassifier.test.ts`
- `browser/src/primitives/terminal/__tests__/errorMessages.test.ts`
- `browser/src/primitives/terminal/__tests__/terminal-error-e2e.test.tsx`
- `browser/src/services/terminal/providers/__tests__/errors.test.ts`

**Modified files:**
- `browser/src/shell/components/PaneContent.tsx` (wrap with PaneErrorBoundary, show AppletLoadError)
- `browser/src/shell/components/shell.css` (error UI styles)
- `browser/src/primitives/terminal/useTerminal.ts` (use error classifier in catch blocks)
- `browser/src/primitives/terminal/terminal.css` (error/warning message styles)
- `browser/src/primitives/terminal/types.ts` (add optional level field to TerminalEntry)
- `browser/src/primitives/terminal/TerminalOutput.tsx` (apply error/warning CSS classes)
- `browser/src/services/terminal/providers/anthropic.ts` (throw ProviderError)
- `browser/src/services/terminal/providers/groq.ts` (throw ProviderError)
- `browser/src/services/terminal/providers/openai-compatible.ts` (throw ProviderError)
- `browser/src/services/terminal/providers/index.ts` (export ProviderError)
- `browser/src/shell/components/index.ts` (export PaneErrorBoundary, AppletLoadError)

---

## Constraints Compliance

All tasks follow:
- ✅ Hard Rule 3: NO HARDCODED COLORS (only var(--sd-*))
- ✅ Hard Rule 4: No file over 500 lines
- ✅ Hard Rule 5: TDD (tests first)
- ✅ Hard Rule 6: NO STUBS (all functions fully implemented)
- ✅ Model assignment: Haiku for all tasks (per spec)

---

## Questions / Clarifications

None. The spec is clear and all acceptance criteria are covered.

---

## Next Steps

1. **Q33NR:** Review the 5 task files for:
   - Missing deliverables
   - Vague acceptance criteria
   - File path precision
   - Test coverage gaps
   - Constraint violations

2. **If approved:** Q33N will dispatch bees in 3 waves (parallel → sequential → integration)

3. **If corrections needed:** Q33N will revise task files and resubmit

---

## Task Files Location

All task files are in:
- `.deia/hive/tasks/2026-03-16-TASK-186-pane-error-boundary.md`
- `.deia/hive/tasks/2026-03-16-TASK-187-terminal-error-messages.md`
- `.deia/hive/tasks/2026-03-16-TASK-188-applet-load-failure-ux.md`
- `.deia/hive/tasks/2026-03-16-TASK-189-llm-provider-error-detection.md`
- `.deia/hive/tasks/2026-03-16-TASK-190-error-handling-e2e-tests.md`

Ready for Q33NR review.
