# SPEC: Canvas App — ReactFlow Canvas EGG

## Priority
P0

## Objective
Port the SimDecisions ReactFlow canvas into ShiftCenter as a canvas.egg.md app. Survey old repo first, then build. Full spec at `C:\Users\davee\Downloads\SPEC-CANVAS-APP-001.md`.

## Context
Old repo: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\`
- Check Canvas/, CanvasChatbot/, PropertiesPanel/, ToolBar/ directories
- Check old package.json for reactflow version

New repo destinations:
- `browser/src/primitives/canvas/CanvasApp.tsx` — ReactFlow wrapper
- `browser/src/apps/canvasAdapter.tsx` — app registry adapter
- `eggs/canvas.egg.md` — EGG layout config

Files to read first:
- `C:\Users\davee\Downloads\SPEC-CANVAS-APP-001.md` — full spec with layout, bus integration, palette, properties
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\index.ts` — app registration
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\terminalResponseRouter.ts` — envelope routing (to_ir handler)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\package.json` — check if reactflow already installed

## Acceptance Criteria
- [ ] ReactFlow canvas renders with zero nodes (empty state)
- [ ] Canvas renders with sample IR data (5 nodes, 4 edges)
- [ ] Canvas registered as appType `canvas` in app registry
- [ ] Bus integration: `terminal:ir-deposit` adds nodes, `canvas:node-selected` publishes on click
- [ ] `canvas.egg.md` defines the 5-pane layout (palette, canvas, terminal, properties)
- [ ] Palette adapter for tree-browser shows draggable node types
- [ ] Properties adapter for tree-browser shows selected node properties
- [ ] `to_ir` handler wired in terminalResponseRouter.ts
- [ ] CSS: var(--sd-*) only
- [ ] 20+ tests across canvas, palette adapter, properties adapter, envelope wiring
- [ ] No file over 500 lines
- [ ] Add reactflow, dagre to browser/package.json

## Model Assignment
sonnet

## Constraints
- Survey old repo FIRST to determine what to port vs build fresh
- Do NOT build: simulation execution, optimization, persistence, multi-user, undo/redo
- Each sub-component in its own file (CanvasApp.tsx, canvasAdapter.tsx, paletteAdapter.tsx, propertiesAdapter.tsx)
