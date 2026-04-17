# BL-207 (RE-QUEUE): Unified title bar — per-pane chrome default ON

## Background — Why Re-Queued
Previous bee modified eggToShell.ts (19/19 tests) but the changes need runtime verification. eggToShell.ts currently hardcodes `chrome: true` but doesn't respect EGG `showChrome: false` opt-out, and MenuBar syndication of active pane items is not wired.

## Objective
Per-pane title bars default ON. EGGs can opt out with `chrome: false` in their layout config. Master menu bar syndicates items from focused pane.

## Current State
- eggToShell.ts sets `chrome: true` on all nodes (lines 33, 115)
- chromeOptions exist: close, pin, collapsible
- No `showChrome` field read from EGG config
- MenuBar.tsx exists but doesn't syndicate per-pane items

## Dependencies (both already DONE)
- BL-204 (hamburger menu) — ✅ FIXED
- BUG-029 (app-add flow) — ✅ FIXED

## Files to Read First
- `browser/src/shell/eggToShell.ts` (current chrome handling)
- `browser/src/shell/components/PaneChrome.tsx` (title bar rendering)
- `browser/src/shell/components/MenuBar.tsx` (master menu)
- `browser/src/shell/types.ts` (shell node types)
- `eggs/canvas.egg.md` (has `chrome: false` on some panes)

## Deliverables
- [ ] eggToShell.ts reads `chrome` field from EGG pane config (defaults to true)
- [ ] PaneChrome respects chrome=false to hide title bar
- [ ] MenuBar syndicates menu items from focused/active pane
- [ ] Tests for default-on, opt-out, and syndication

## Acceptance Criteria
- [ ] Per-pane title bars visible by default
- [ ] EGG panes with `chrome: false` hide their title bar
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
- Do NOT remove per-pane title bars — make them default ON with opt-out

## Model Assignment
sonnet

## Priority
P0

## Re-Queue Metadata
- Original spec: `_done/2026-03-17-SPEC-TASK-BL207-unified-title-bar.md`
- Previous response: `20260317-BL-207-RESPONSE.md`
- Failure reason: Needs runtime verification; showChrome opt-out and MenuBar syndication unconfirmed
