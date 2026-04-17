# RB-2: BUG-026 Kanban Items Filter Fix

## YOUR ROLE
You are a BEE. Read `.deia/BOOT.md` for your rules.

## Context
You are on the `browser-recovery` branch. The browser/ directory has been reset to the March 16 baseline (commit ad06402). You are rebuilding a feature that was lost during a tangled period.

## Objective
Fix the Kanban EGG so it loads without the "items.filter is not a function" error. When loading `?egg=kanban`, the app crashes because the kanban primitive receives items in the wrong format (object instead of array, or undefined).

## What To Do
1. Read `eggs/kanban.egg.md` to understand the EGG config
2. Read the kanban primitive in `browser/src/primitives/kanban/`
3. Read the app registry in `browser/src/shell/components/appRegistry.ts`
4. Read the tree-browser adapter layer in `browser/src/apps/`
5. Trace the kanban data flow from adapter → primitive
6. Fix the items data shape (ensure it's always an array)
7. Add defensive check for non-array items
8. Test with empty data, valid data, and malformed data

## Files You May Modify
- `browser/src/App.tsx`
- `browser/src/apps/treeBrowserAdapter.tsx`
- `browser/src/primitives/apps-home/AppCard.tsx`
- `browser/src/primitives/apps-home/AppsHome.css`
- `browser/src/primitives/apps-home/AppsHome.tsx`
- `browser/src/primitives/tree-browser/TreeBrowser.tsx`
- `browser/src/primitives/tree-browser/types.ts`
- `browser/src/primitives/kanban/` (any file)
- Test files in the same directories

## Files You Must NOT Modify
- Anything in `browser/src/primitives/canvas/`
- Anything in `browser/src/shell/` (shell layer is handled by RB-1)
- `browser/src/infrastructure/relay_bus/types/messages.ts` (already cherry-picked)
- Anything outside `browser/`

## Smoke Test
```bash
cd browser && npx vitest run --reporter=verbose src/primitives/kanban/
cd browser && npx vitest run --reporter=verbose src/primitives/apps-home/
cd browser && npx vitest run --reporter=verbose src/primitives/tree-browser/
```

## Build Verification
```bash
cd browser && npx vite build
```

## Acceptance Criteria
- [ ] ?egg=kanban loads without errors
- [ ] Kanban board renders (even if empty)
- [ ] No "items.filter is not a function" error
- [ ] Defensive checks for non-array items
- [ ] Tests pass

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Response Requirements — MANDATORY
Write response to `.deia/hive/responses/20260319-TASK-RB2-BUG026-KANBAN-RESPONSE.md` with all 8 sections per BOOT.md.
