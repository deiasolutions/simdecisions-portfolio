# BL-207: Unified title bar with per-pane title bars default ON

## Objective
Implement unified title bar behavior: one master menu bar at the top with syndicated pane items, and per-pane title bars that default to ON unless the EGG config explicitly says NO (showChrome: false).

## Context
Currently PaneChrome.tsx (lines ~28-38) has chrome enforcement logic and title bar rendering (lines ~106-218). MenuBar.tsx handles the top-level menu. The goal: per-pane title bars show by default, EGGs can opt out with showChrome: false. The master menu bar should syndicate active pane menu items.

## Files to Read First
- `browser/src/shell/components/PaneChrome.tsx`
- `browser/src/shell/components/MenuBar.tsx`
- `browser/src/shell/components/Shell.tsx`
- `browser/src/shell/types.ts`
- `eggs/canvas.egg.md`
- `eggs/chat.egg.md`
- `browser/src/shell/eggToShell.ts`

## Deliverables
- [ ] PaneChrome defaults to showing title bar (showChrome defaults to true)
- [ ] EGG config can set showChrome: false to hide per-pane title bar
- [ ] eggToShell.ts passes showChrome from EGG config to shell tree nodes
- [ ] MenuBar syndicates menu items from active/focused pane
- [ ] Update existing EGG files that need explicit showChrome values
- [ ] Tests for default-on behavior, opt-out behavior, and syndication

## Acceptance Criteria
- [ ] Per-pane title bars visible by default on all panes
- [ ] EGG with showChrome: false hides its pane title bar
- [ ] Master menu bar shows items from focused pane
- [ ] No hardcoded colors
- [ ] All tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/shell/components/__tests__/PaneChrome.test.tsx`
- [ ] `cd browser && npx vitest run --reporter=verbose src/shell/__tests__/eggToShell.test.ts`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- Do NOT remove per-pane title bars entirely - just make them default ON

## Depends On
- BL204 (hamburger menu must be fixed before title bar changes)
- BUG029 (app-add flow must be fixed before Shell.tsx changes)

## Model Assignment
sonnet

## Priority
P0
