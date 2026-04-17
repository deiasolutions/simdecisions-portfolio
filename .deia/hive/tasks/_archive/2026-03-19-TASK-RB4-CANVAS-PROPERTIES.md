# RB-4: Canvas + Properties Panel Rebuild — BUG021 + BL121

## YOUR ROLE
You are a BEE. Read `.deia/BOOT.md` for your rules.

## Context
You are on the `browser-recovery` branch. The browser/ directory has been reset to the March 16 baseline (commit ad06402), then 3 clean files were cherry-picked:
- `messages.ts` — added `canvas:node-selected` and `canvas:node-deselected` message types
- `canvas.css` — added minimap viewport stroke styling
- `sim.egg.md` — added defaultDocuments

You are rebuilding features that depend on these cherry-picked types.

## Objective
Implement two related canvas features:

### Feature A: BUG-021 Canvas Minimap (JS changes)
The CSS fix is already cherry-picked. Now wire the JavaScript changes:
1. Read the current CanvasApp.tsx on the baseline
2. Ensure the minimap component uses theme-appropriate rendering
3. Fix any JS-level minimap configuration issues
4. The CSS is already correct (cherry-picked), focus on component wiring

### Feature B: BL-121 Properties Panel Wiring
Wire the canvas node selection to the properties panel adapter:
1. Read `browser/src/primitives/tree-browser/adapters/propertiesAdapter.ts`
2. Read `eggs/canvas.egg.md` to understand properties pane config
3. When a canvas node is selected, publish `canvas:node-selected` on the bus (type already exists in messages.ts)
4. propertiesAdapter should subscribe to `canvas:node-selected` and display node properties
5. Deselecting should publish `canvas:node-deselected` and clear the panel
6. Editing a property should update the canvas node

## Files You May Modify
- `browser/src/primitives/canvas/CanvasApp.tsx`
- `browser/src/primitives/tree-browser/adapters/propertiesAdapter.ts`
- Test files for these components

## Files You Must NOT Modify
- `browser/src/infrastructure/relay_bus/types/messages.ts` (already has the types)
- `browser/src/primitives/canvas/canvas.css` (already cherry-picked)
- Anything in `browser/src/shell/`
- Anything in `browser/src/primitives/apps-home/`
- `browser/src/App.tsx`
- Anything outside `browser/`

## Smoke Test
```bash
cd browser && npx vitest run --reporter=verbose src/primitives/canvas/
cd browser && npx vitest run --reporter=verbose src/primitives/tree-browser/adapters/__tests__/propertiesAdapter
```

## Build Verification
```bash
cd browser && npx vite build
```

## Acceptance Criteria
- [ ] Selecting a canvas node publishes canvas:node-selected on the bus
- [ ] Properties panel shows properties for selected node
- [ ] Deselecting clears the properties panel
- [ ] Editing a property updates the canvas node
- [ ] Minimap renders correctly (CSS already handled)
- [ ] Tests pass
- [ ] Build passes

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Response Requirements — MANDATORY
Write response to `.deia/hive/responses/20260319-TASK-RB4-CANVAS-PROPERTIES-RESPONSE.md` with all 8 sections per BOOT.md.
