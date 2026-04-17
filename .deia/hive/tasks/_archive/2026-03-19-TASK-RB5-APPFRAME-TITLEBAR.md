# RB-5: AppFrame Unified Title Bar — BL-207

## YOUR ROLE
You are a BEE. Read `.deia/BOOT.md` for your rules.

## Context
You are on the `browser-recovery` branch. The browser/ directory has been reset to the March 16 baseline (commit ad06402). You are rebuilding a feature that was lost during a tangled period.

**IMPORTANT:** RB-1 may have already modified `eggToShell.ts`. Read the CURRENT version of that file before making changes. If eggToShell.ts already passes showChrome through, do NOT duplicate that work.

## Objective
Implement unified title bar behavior: per-pane title bars default to ON unless the EGG config explicitly says `showChrome: false`.

## What To Do
1. Read `browser/src/shell/components/PaneChrome.tsx` — understand chrome enforcement
2. Read `browser/src/shell/components/AppFrame.tsx` — the component to modify
3. Read `browser/src/shell/components/MenuBar.tsx` — top-level menu
4. Read `browser/src/shell/types.ts` — shell tree node types
5. Read `browser/src/shell/eggToShell.ts` — EGG config → shell tree
6. Read `eggs/canvas.egg.md` and `eggs/chat.egg.md` for EGG config examples

**Changes needed:**
- AppFrame.tsx: Per-pane title bars show by default
- eggToShell.ts: Pass `showChrome` from EGG config to shell tree nodes (if not already done by RB-1)
- PaneChrome defaults showChrome to true
- EGGs can opt out with `showChrome: false`

## Files You May Modify
- `browser/src/shell/components/AppFrame.tsx`
- `browser/src/shell/eggToShell.ts` (ONLY for showChrome passthrough, coordinate with RB-1)
- `browser/src/shell/components/PaneChrome.tsx` (if needed for default behavior)
- `browser/src/shell/types.ts` (if showChrome field needed)
- Test files for these components

## Files You Must NOT Modify
- Anything in `browser/src/primitives/`
- `browser/src/App.tsx`
- `browser/src/infrastructure/relay_bus/types/messages.ts`
- Anything outside `browser/`

## Smoke Test
```bash
cd browser && npx vitest run --reporter=verbose src/shell/components/__tests__/
cd browser && npx vitest run --reporter=verbose src/shell/__tests__/eggToShell.test.ts
```

## Build Verification
```bash
cd browser && npx vite build
```

## Acceptance Criteria
- [ ] Per-pane title bars visible by default on all panes
- [ ] EGG with showChrome: false hides its pane title bar
- [ ] No hardcoded colors
- [ ] All tests pass
- [ ] Build passes

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- Do NOT remove per-pane title bars entirely — just make them default ON

## Response Requirements — MANDATORY
Write response to `.deia/hive/responses/20260319-TASK-RB5-APPFRAME-TITLEBAR-RESPONSE.md` with all 8 sections per BOOT.md.
