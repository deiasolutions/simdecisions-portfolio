# BL-121 (RE-QUEUE): Properties panel doesn't show when selecting canvas item

## Priority
P0

## Background
Selecting a node on the canvas should show its properties in the properties pane. This is not working. A properties adapter exists at `browser/src/primitives/tree-browser/adapters/propertiesAdapter.ts` and a PropertyPanel exists at `browser/src/apps/sim/components/flow-designer/properties/PropertyPanel.tsx` but the wiring between canvas selection and properties display is broken or missing.

## Problem
When a user selects a node on the canvas, the properties pane (configured in canvas.egg.md) does not populate with the node's properties. The bus event flow from canvas selection → properties pane is not working.

## What Needs to Happen
1. Read the canvas EGG to understand the properties pane configuration
2. Check what bus event CanvasApp.tsx sends when a node is selected (e.g. `node:selected`)
3. Check what the propertiesAdapter listens for
4. Wire the selection event to the properties adapter
5. Ensure PropertyPanel renders the selected node's data

## Files to Read First
- `eggs/canvas.egg.md` (properties pane config)
- `browser/src/primitives/canvas/CanvasApp.tsx` (node selection handling)
- `browser/src/primitives/tree-browser/adapters/propertiesAdapter.ts`
- `browser/src/primitives/tree-browser/adapters/simPropertiesAdapter.ts`
- `browser/src/apps/sim/components/flow-designer/properties/PropertyPanel.tsx`
- `browser/src/infrastructure/relay_bus/busTypes.ts` (bus event types for selection)

## Deliverables
- [ ] Selecting a canvas node sends a bus event with node data
- [ ] Properties pane receives the event and displays node properties
- [ ] Deselecting clears the properties pane
- [ ] Tests for selection → properties flow
- [ ] No regressions in canvas or tree-browser tests

## Smoke Test
```bash
cd browser && npx vitest run --reporter=verbose src/primitives/canvas/
cd browser && npx vitest run --reporter=verbose src/primitives/tree-browser/
cd browser && npx vitest run
```

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- MUST modify source code, not just tests

## Model Assignment
sonnet
