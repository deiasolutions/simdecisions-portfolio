# Briefing: Fix TreeNodeRow Drag DataTransfer for Canvas Palette

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Queen Regent)
**Date:** 2026-03-16
**Spec ID:** 2026-03-16-1502-SPEC-w2-09-palette-drag-fix
**Priority:** P1
**Model Assignment:** Haiku

---

## Objective

Fix `TreeNodeRow.handleDragStart` to populate `dataTransfer` with node type data from `meta.dragMimeType` and `meta.dragData` so the canvas drop handler in FlowDesigner receives the node type info and creates the correct node at drop position. This is a 5-line fix.

---

## Context from Q88N

The spec states:
- TreeNodeRow needs to check for `node.meta.dragMimeType` and `node.meta.dragData`
- If present, call `e.dataTransfer.setData(mimeType, JSON.stringify(dragData))`
- Set `e.dataTransfer.effectAllowed = 'copy'`
- FlowDesigner.onDrop should receive the data and create node at drop position
- Existing drag behavior for non-palette items must be unaffected

Files referenced:
- `browser/src/primitives/tree-browser/TreeNodeRow.tsx` (handleDragStart — needs fix)
- `browser/src/primitives/tree-browser/adapters/simPaletteAdapter.ts` (sets meta.dragMimeType and meta.dragData)
- `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx` (onDrop handler at lines 302-358, reads application/phase-node)

---

## Your Task

Write ONE task file for a Haiku bee:
- Read the 3 files listed above
- Fix `TreeNodeRow.handleDragStart` to populate dataTransfer
- Write 3+ tests (TDD)
- Verify FlowDesigner.onDrop receives the data correctly
- Ensure non-palette drag behavior is unaffected

---

## Constraints

- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- File claims required (build monitor heartbeat + file claim protocol in spec)
- 3+ tests required

---

## Acceptance Criteria

From the spec:
- [ ] TreeNodeRow.handleDragStart checks for node.meta.dragMimeType and node.meta.dragData
- [ ] If present, calls e.dataTransfer.setData(mimeType, JSON.stringify(dragData))
- [ ] Sets e.dataTransfer.effectAllowed = 'copy'
- [ ] FlowDesigner.onDrop receives the data and creates node at drop position
- [ ] Existing drag behavior for non-palette items unaffected
- [ ] CSS uses var(--sd-*) only
- [ ] 3+ tests: drag from palette, drop on canvas, verify non-palette drag unaffected
- [ ] No file over 500 lines

---

## File Paths (Absolute)

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\simPaletteAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx`
- Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\TreeNodeRow.drag.test.tsx`
- Integration test: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\palette-to-canvas.test.tsx`

---

## Smoke Test

From the spec:
- Drag node type from palette tree → drop on canvas → node appears at drop position
- `cd browser && npx vitest run src/primitives/tree-browser/__tests__/TreeNodeRow.drag.test.tsx`
- `cd browser && npx vitest run src/apps/sim/components/flow-designer/__tests__/palette-to-canvas.test.tsx`
- No new test failures

---

## Build Monitor Protocol

From the spec:
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  ```json
  {"task_id": "2026-03-16-1502-SPEC-w2-09-palette-drag-fix", "status": "running", "model": "haiku", "message": "working"}
  ```
- File claims: POST http://localhost:8420/build/claim before modifying
- Release early: POST http://localhost:8420/build/release

---

## Next Steps

1. Read the codebase files listed above
2. Write ONE task file to `.deia/hive/tasks/`
3. Return to me (Q33NR) for review
4. Wait for my approval before dispatching
