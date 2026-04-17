# BRIEFING: User-Facing Error Handling

**Date:** 2026-03-16
**From:** Q33NR
**To:** Q33N
**Priority:** P1
**Model Assignment:** Haiku (per spec)

---

## Objective

Users see helpful error messages, not stack traces or blank screens. Every failure state has a UI.

---

## Context from Q88N (Spec)

This is spec `2026-03-16-3009-SPEC-w3-10-error-handling-ux.md` from the queue.

Files to read first:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneContent.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\AppletShell.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\`

---

## Acceptance Criteria from Spec

- [ ] Applet load failure: pane shows "Failed to load [applet name]. Try refreshing." with retry button
- [ ] API unreachable: terminal shows "Cannot reach server. Check your connection." (not a stack trace)
- [ ] LLM error (bad API key, rate limit, model down): terminal shows human-readable message with suggestion ("Check your API key in Settings")
- [ ] 500 error from hivenode: user sees "Something went wrong. Error logged." (not the raw JSON error)
- [ ] Network timeout: terminal shows "Request timed out. Try again."
- [ ] React error boundary wraps every pane -- one crashing pane doesn't take down the whole app
- [ ] All error messages use var(--sd-*) colors (red accent for errors, yellow for warnings)
- [ ] 5+ tests

---

## Smoke Test Requirements

- [ ] Remove API key -> send message -> terminal shows "No API key configured" with link to settings
- [ ] Kill hivenode -> send message -> terminal shows connection error, not crash

---

## Constraints

1. **Hard Rule 3:** NO hardcoded colors. Only `var(--sd-*)` CSS variables.
2. **Hard Rule 4:** No file over 500 lines. Modularize if needed.
3. **Hard Rule 5:** TDD. Tests first, then implementation.
4. **Hard Rule 6:** NO STUBS. Every function fully implemented.

---

## Your Job (Q33N)

1. Read the files listed above
2. Identify where error handling is missing or incomplete
3. Write task files to `.deia/hive/tasks/` for each component that needs error UX
4. Return task files to me (Q33NR) for review — DO NOT dispatch bees yet
5. Wait for my approval before dispatching

---

## Model Assignment

**Haiku** for all tasks (per spec).

---

## Notes

- Focus on **user-facing error messages**, not backend logging or exception handling architecture
- The goal is **helpful messages** that guide users to fix the problem
- React error boundaries must catch errors without crashing the whole app
- This is a UX layer on top of existing error handling — not a rewrite of error handling itself

---

## Expected Deliverables

Task files that cover:
- Error boundary component(s) for pane-level isolation
- Error message rendering in terminal (no stack traces)
- Retry/recovery UX for applet load failures
- Human-readable messages for API errors (unreachable, 500, timeout, LLM errors)
- Tests for all error scenarios (5+ total)

Return the task files to me for review before dispatching.
