# RB-1: Shell Foundation Rebuild — Error States + Layout Actions

## YOUR ROLE
You are a BEE. Read `.deia/BOOT.md` for your rules.

## Context
You are on the `browser-recovery` branch. The browser/ directory has been reset to the March 16 baseline (commit ad06402). You are rebuilding features that were lost during a tangled period.

## Objective
Implement two independent fixes in the shell layer:

### Fix A: Error States Integration (TASK-236)
Wire the existing error classifier throughout terminal error paths and PaneErrorBoundary.

**What already exists (DO NOT recreate):**
- `browser/src/primitives/terminal/errorClassifier.ts` (~88 lines) — classifies errors
- `browser/src/primitives/terminal/errorMessages.ts` (~68 lines) — friendly messages
- Both imported in useTerminal.ts

**What to do:**
1. Read errorClassifier.ts and errorMessages.ts to understand the API
2. Wire error classifier into ALL terminal error paths in useTerminal.ts (not just relay)
3. Update PaneErrorBoundary.tsx to use errorClassifier for categorized error display
4. Add tests for the new error path coverage

### Fix B: moveAppOntoOccupied Layout Actions (FIX-MOVEAPP)
Fix 7 failing shell layout tests for move-app-onto-occupied-pane actions.

**What to do:**
1. Find the test file (search for `moveAppOntoOccupied` in browser/src/shell/)
2. Run the tests, read the errors
3. Fix the layout.ts implementation to handle: center zone (tabs), left/right/top/bottom zones (splits), already-tabbed containers, split parent nesting
4. All 7 tests must pass

## Files You May Modify
- `browser/src/shell/components/PaneErrorBoundary.tsx`
- `browser/src/shell/actions/layout.ts`
- `browser/src/shell/eggToShell.ts` (ONLY if needed for error state changes)
- `browser/src/primitives/terminal/useTerminal.ts` (ONLY for wiring error classifier)
- Test files in the same directories

## Files You Must NOT Modify
- Anything in `browser/src/primitives/canvas/`
- Anything in `browser/src/primitives/tree-browser/`
- Anything in `browser/src/primitives/apps-home/`
- `browser/src/App.tsx`
- `browser/src/shell/components/AppFrame.tsx`
- Anything outside `browser/`

## Smoke Test
```bash
cd browser && npx vitest run --reporter=verbose src/shell/actions/
cd browser && npx vitest run --reporter=verbose src/shell/components/__tests__/PaneErrorBoundary.test.tsx
cd browser && npx vitest run --reporter=verbose src/primitives/terminal/__tests__/errorClassifier.test.ts
cd browser && npx vitest run --reporter=verbose src/primitives/terminal/__tests__/errorMessages.test.ts
```

## Build Verification
```bash
cd browser && npx vite build
```

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- Do NOT recreate errorClassifier.ts or errorMessages.ts — they already exist

## Response Requirements — MANDATORY
Write response to `.deia/hive/responses/20260319-TASK-RB1-SHELL-FOUNDATION-RESPONSE.md` with all 8 sections per BOOT.md.
