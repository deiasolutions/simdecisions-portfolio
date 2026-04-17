# BUG-022-B (RE-QUEUE): Canvas palette click-to-place does nothing

## Background — Why Re-Queued
This was originally part of BUG-022 (2026-03-17). BUG-022-A (icons) was fixed by BUG-035 (isTextIcon function in TreeNodeRow.tsx). But BUG-022-B (click-to-place) was NEVER implemented — the bee wrote tests only, no source code changes. A subsequent FIX-BUG022B spec only fixed test infrastructure (_dispatch mock), not the actual feature. This is a re-queue to get the actual source code written.

## Objective
Wire the palette adapter so clicking a component in the components panel places it on the canvas. Currently clicking does nothing.

## Context
- Icons now show correctly (BUG-022-A fixed)
- The paletteAdapter provides component entries to the tree-browser
- Clicking a component entry should either place it at center of canvas viewport or initiate a drag-to-place
- The canvas uses a message bus pattern — palette click should emit a bus event that the canvas listens for

## Files to Read First
- `browser/src/primitives/tree-browser/adapters/paletteAdapter.ts`
- `browser/src/primitives/canvas/CanvasApp.tsx`
- `browser/src/primitives/canvas/__tests__/paletteClickToPlace.test.tsx` (existing tests — make these pass)
- `browser/src/infrastructure/relay_bus/messageBus.ts`
- `eggs/canvas.egg.md`

## Deliverables
- [ ] paletteAdapter click handler emits bus event (e.g. `canvas:place-component`)
- [ ] CanvasApp (or canvas hook) listens for placement event and adds node
- [ ] Clicking a palette item places a new component on the canvas
- [ ] Existing paletteClickToPlace tests pass (10 tests)
- [ ] No regressions in TreeNodeRow icon tests (15 tests)

## Acceptance Criteria
- [ ] Click a palette item → component appears on canvas
- [ ] All paletteClickToPlace tests pass
- [ ] All TreeNodeRow icon/palette tests pass
- [ ] No new test failures in canvas/ or tree-browser/

## Smoke Test
- [ ] `cd browser && npx vitest run src/primitives/canvas/__tests__/paletteClickToPlace.test.tsx`
- [ ] `cd browser && npx vitest run src/primitives/tree-browser/__tests__/TreeNodeRow.icon.test.tsx`
- [ ] `cd browser && npx vitest run src/primitives/tree-browser/__tests__/TreeNodeRow.palette-icons.integration.test.tsx`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs — real implementation required
- Do NOT modify messageBus.ts core (only add listeners/emitters in adapter and canvas code)

## Model Assignment
sonnet

## Priority
P0

## Re-Queue Metadata
- Original spec: `_done/2026-03-17-SPEC-TASK-BUG022-canvas-components-panel-plain.md`
- Previous attempt: `_done/2026-03-18-SPEC-TASK-FIX-BUG022B-palette-click-dispatch.md`
- Failure reason: Bees wrote tests but never modified source code (paletteAdapter.ts, CanvasApp.tsx)
