# TASK-236 (RE-QUEUE): Error states — integrate error classifier across terminal

## Background — Why Re-Queued
Previous bee created errorClassifier.ts and errorMessages.ts but only wired them into ONE place (relay error handling in useTerminal.ts line ~483). PaneErrorBoundary was untouched. The error infrastructure exists but is underutilized.

## Objective
Integrate the error classifier and error message formatter throughout the terminal component and PaneErrorBoundary so all error paths produce user-friendly categorized messages.

## What Already Exists (DO NOT recreate)
- `browser/src/primitives/terminal/errorClassifier.ts` (88 lines) — classifies errors into categories
- `browser/src/primitives/terminal/errorMessages.ts` (68 lines) — generates friendly messages
- Both imported in useTerminal.ts (lines 22-23)
- Used at useTerminal.ts line ~483 (relay error only)

## What Is Missing
1. Error classifier not used in other terminal error paths (timeout, parse, network)
2. PaneErrorBoundary.tsx doesn't use error classifier for categorized display
3. Terminal error display doesn't show categorized/friendly messages in most error cases

## Files to Read First
- `browser/src/primitives/terminal/errorClassifier.ts` (existing)
- `browser/src/primitives/terminal/errorMessages.ts` (existing)
- `browser/src/primitives/terminal/useTerminal.ts` (find all error handling paths)
- `browser/src/shell/components/PaneErrorBoundary.tsx` (needs integration)

## Files to Modify
- `browser/src/primitives/terminal/useTerminal.ts` — wire classifier into all error paths
- `browser/src/shell/components/PaneErrorBoundary.tsx` — use classifier for categorized display

## Deliverables
- [ ] All terminal error paths use errorClassifier + errorMessages
- [ ] PaneErrorBoundary shows categorized error messages
- [ ] Existing error tests still pass
- [ ] New tests for additional error path coverage

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/terminal/__tests__/errorClassifier.test.ts`
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/terminal/__tests__/errorMessages.test.ts`
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/terminal/__tests__/errorIntegration.test.tsx`
- [ ] `cd browser && npx vitest run --reporter=verbose src/shell/components/__tests__/PaneErrorBoundary.test.tsx`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- Do NOT recreate errorClassifier.ts or errorMessages.ts

## Model Assignment
sonnet

## Priority
P1

## Re-Queue Metadata
- Original spec: `_done/2026-03-16-SPEC-TASK-236-error-states.md`
- Failure reason: Infrastructure created but only integrated in 1 of ~5 error paths
