# BRIEFING: TASK-236 Error States — Pane Error Messages for Failed Applets

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-17
**Priority:** P1
**Model:** sonnet

---

## Objective

Wire the existing error classifier and error message system into the terminal UI. Ensure PaneErrorBoundary catches applet load failures gracefully. Users should see helpful error messages, not blank screens or raw stack traces.

---

## Context

This is **Wave 4 Product Polish** (Task 4.8 from `docs/specs/WAVE-4-PRODUCT-POLISH.md`).

Three error systems exist but are NOT fully wired together:
1. `PaneErrorBoundary.tsx` (158 lines) — catches React render errors, shows retry button
2. `errorClassifier.ts` — classifies 7 error types (api_unreachable, timeout, auth_failure, rate_limit, server_error, network_error, unknown)
3. `errorMessages.ts` — user-friendly messages with actionable suggestions

The classifier and message modules exist but are NOT integrated into the terminal output display.

---

## Source Spec

`docs/specs/WAVE-4-PRODUCT-POLISH.md` — Task 4.8

---

## Files to Reference

**Terminal primitives:**
- `browser/src/primitives/terminal/errorClassifier.ts` — Error type classification (already exists)
- `browser/src/primitives/terminal/errorMessages.ts` — User-friendly messages (already exists)
- `browser/src/primitives/terminal/terminal-errors.css` — Error styling (already exists)
- `browser/src/primitives/terminal/TerminalOutput.tsx` — Where errors render
- `browser/src/primitives/terminal/useTerminal.ts` — Terminal state management

**Shell components:**
- `browser/src/shell/components/PaneErrorBoundary.tsx` — Error boundary (158 lines, already exists)

**Theme:**
- `browser/src/styles/shell-themes.css` — Should contain `--sd-yellow` (added by TASK-233, or fallback needed)

---

## Deliverables

### 1. Wire error classifier into terminal error handling
When terminal receives an error response:
- Classify it using `errorClassifier.ts`
- Display the user-friendly message from `errorMessages.ts` instead of raw error text
- Show actionable suggestion (e.g., "Check your API key" for auth_failure)

### 2. CSS variable for warnings
- Add `--sd-yellow` to `shell-themes.css` if not already added by TASK-233
- Fallback: define it locally in `terminal-errors.css` with a comment referencing TASK-233

### 3. Verify PaneErrorBoundary behavior
- Ensure PaneErrorBoundary catches component crashes
- Ensure retry button shows and works

### 4. Tests
- Add test: error classifier returns correct type for each error pattern
- Add test: terminal displays friendly message instead of raw error

### 5. Test command
Run: `cd browser && npx vitest run src/primitives/terminal/ && npx vitest run src/shell/`

---

## Acceptance Criteria

- [ ] Terminal uses `errorClassifier.ts` to classify errors
- [ ] Terminal displays user-friendly messages from `errorMessages.ts`
- [ ] PaneErrorBoundary catches component crashes and shows retry button
- [ ] `--sd-yellow` is available in CSS (either from TASK-233 or local fallback)
- [ ] Test: error classifier returns correct type for each error pattern
- [ ] Test: terminal displays friendly message instead of raw error
- [ ] All terminal and shell tests pass

---

## Constraints

- **Rule 3:** CSS variables only (`var(--sd-*)`), no hardcoded colors
- **Rule 4:** No file over 500 lines (hard limit: 1,000)
- **Rule 5:** TDD — tests first, then implementation
- **Rule 6:** NO STUBS — every function fully implemented

---

## What Q33N Should Do

1. **Read the existing error modules** to understand the classification and message format
2. **Write a task file** for a Bee (use haiku model) with:
   - Clear integration steps for wiring errorClassifier into terminal error handling
   - Test requirements for error classification and message display
   - Verification steps for PaneErrorBoundary
   - Absolute file paths for all files to modify
3. **Return the task file to Q33NR for review** before dispatching
4. **After Q33NR approval:** dispatch the bee
5. **When bee completes:** review the response file and report results to Q33NR

---

## Notes

- The error classifier and message modules already exist — this is an INTEGRATION task, not a new feature
- PaneErrorBoundary already exists — we just need to verify it works as expected
- The CSS variable `--sd-yellow` may have been added by TASK-233 (theme verification) — check first before adding fallback
- This is a small, focused task suitable for a Haiku bee

---

**Q33N: Write the task file and return for review. Do NOT dispatch yet.**
