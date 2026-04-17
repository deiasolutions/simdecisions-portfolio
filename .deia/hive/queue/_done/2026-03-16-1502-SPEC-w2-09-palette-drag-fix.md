# SPEC: Fix TreeNodeRow Drag DataTransfer for Canvas Palette

## Priority
P1

## Objective
TreeNodeRow.handleDragStart needs to populate dataTransfer with node type data from meta.dragMimeType and meta.dragData so the canvas drop handler in FlowDesigner receives the node type info and creates the correct node at drop position. This is a 5-line fix.

## Context
Files to read first:
- `browser/src/primitives/tree-browser/TreeNodeRow.tsx` (handleDragStart function — needs fix)
- `browser/src/primitives/tree-browser/adapters/simPaletteAdapter.ts` (sets meta.dragMimeType and meta.dragData)
- `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx` (onDrop handler at lines 302-358, reads application/phase-node)

## Acceptance Criteria
- [ ] TreeNodeRow.handleDragStart checks for node.meta.dragMimeType and node.meta.dragData
- [ ] If present, calls e.dataTransfer.setData(mimeType, JSON.stringify(dragData))
- [ ] Sets e.dataTransfer.effectAllowed = 'copy'
- [ ] FlowDesigner.onDrop receives the data and creates node at drop position
- [ ] Existing drag behavior for non-palette items unaffected
- [ ] CSS uses var(--sd-*) only
- [ ] 3+ tests: drag from palette, drop on canvas, verify non-palette drag unaffected
- [ ] No file over 500 lines

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-16-1502-SPEC-w2-09-palette-drag-fix", "status": "running", "model": "haiku", "message": "working"}

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it to prevent conflicts with other bees:
1. POST http://localhost:8420/build/claim with JSON:
   {"task_id": "2026-03-16-1502-SPEC-w2-09-palette-drag-fix", "files": ["browser/src/primitives/tree-browser/TreeNodeRow.tsx"]}
2. If response has conflicts (ok=false), poll GET http://localhost:8420/build/claims every 30s until the file is yours.
3. When done, release early: POST http://localhost:8420/build/release

## Smoke Test
- [ ] Drag node type from palette tree → drop on canvas → node appears at drop position
- [ ] cd browser && npx vitest run src/primitives/tree-browser/__tests__/TreeNodeRow.drag.test.tsx
- [ ] cd browser && npx vitest run src/apps/sim/components/flow-designer/__tests__/palette-to-canvas.test.tsx
- [ ] No new test failures

## Model Assignment
haiku
