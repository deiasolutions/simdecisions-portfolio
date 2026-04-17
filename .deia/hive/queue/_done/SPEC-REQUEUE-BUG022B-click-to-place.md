# BUG-022-B (RE-QUEUE): Canvas click-to-place broken

## Priority
P0

## Background
Click-to-place was working yesterday. User confirms it stopped working. Multiple previous bees claimed COMPLETE or FALSE_POSITIVE but the feature is broken at runtime.

## Problem
Clicking a component in the canvas palette/components panel does NOT place it on the canvas. No palette component exists in `browser/src/primitives/canvas/` — there is no `Palette.tsx`, `ComponentsPanel.tsx`, or similar file.

## What Needs to Happen
1. Read the canvas EGG config (`eggs/canvas.egg.md`) to understand the palette pane setup
2. Read `browser/src/primitives/canvas/CanvasApp.tsx` to understand how nodes are added
3. Check if there's a bus event for adding nodes (e.g. `node:add`, `palette:select`, `component:place`)
4. Implement or fix the click-to-place flow: user clicks component in palette → node appears on canvas
5. If the palette adapter exists in tree-browser adapters, check `browser/src/primitives/tree-browser/adapters/` for palette-related files

## Files to Read First
- `eggs/canvas.egg.md` (palette pane config)
- `browser/src/primitives/canvas/CanvasApp.tsx`
- `browser/src/primitives/canvas/canvasTypes.ts`
- `browser/src/primitives/tree-browser/adapters/` (look for palette adapter)
- `browser/src/infrastructure/relay_bus/` (bus event types)

## Deliverables
- [ ] Clicking a palette item places a node on the canvas
- [ ] New node appears at a reasonable position (center of viewport or cursor)
- [ ] Tests for the click-to-place flow
- [ ] No regressions in canvas tests

## Smoke Test
```bash
cd browser && npx vitest run --reporter=verbose src/primitives/canvas/
cd browser && npx vitest run
```

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- MUST verify the fix works by checking bus event wiring end-to-end

## Model Assignment
sonnet
