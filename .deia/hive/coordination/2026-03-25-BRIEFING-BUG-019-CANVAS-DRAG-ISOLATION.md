# BRIEFING: BUG-019 Canvas Drag Isolation (Stage Capture)

**From:** Q33NR (REGENT-QUEUE-TEMP-SPEC-BUG-019)
**To:** Q33N
**Date:** 2026-03-25
**Model Assignment:** sonnet
**Priority:** P0

---

## Objective

Fix canvas drag-drop from palette being captured by the Shell's drag-and-drop system instead of being isolated to the canvas pane. This requires setting a `canvasInternal: true` marker in paletteAdapter, propagating it as a `canvas/internal` dataTransfer type in TreeNodeRow, and making ShellNodeRenderer ignore these drags.

---

## Context from Q88N

The spec (SPEC-BUG-019) identifies that:
1. Palette nodes don't set the `canvasInternal: true` marker (tests expect it, grep finds none)
2. TreeNodeRow has `stopPropagation()` but palette nodes don't set the isolation marker
3. The test file uses source code reading instead of runtime behavior verification
4. The MIME type mismatch: test expects `application/sd-node-type`, but code uses `application/phase-node`

---

## Root Cause (from spec)

- **Missing:** `canvasInternal: true` marker in `paletteAdapter.ts`
- **Incomplete:** `stopPropagation()` exists in `CanvasApp.tsx` onDragOver/onDrop, but palette nodes don't set the isolation marker
- **Untested:** Tests use source code reading instead of runtime behavior verification

---

## Implementation Requirements

### 1. Update paletteAdapter.ts
In `itemToNode()` function, add `canvasInternal: true` to the `meta` object alongside existing `dragMimeType` and `dragData`.

### 2. Update TreeNodeRow.tsx
In `handleDragStart()`, after setting dragMimeType data:
- Check for `canvasInternal` in node.meta
- If true: set `e.dataTransfer.setData('canvas/internal', 'true')`
- Call `e.stopPropagation()`

### 3. Update ShellNodeRenderer.tsx
In both `onDragOver` and `onDrop` handlers:
- Add early return if `e.dataTransfer.types.includes('canvas/internal')`

### 4. Verify CanvasApp.tsx
Lines 467 and 473 already include `event.stopPropagation()` in onDragOver and onDrop. No changes needed, just verify.

### 5. Replace test file
Replace `canvasDragIsolation.test.tsx` with runtime behavior tests (not source code reading). Minimum 5 tests.

---

## Files to Read First

- browser/src/primitives/tree-browser/adapters/paletteAdapter.ts
- browser/src/primitives/tree-browser/TreeNodeRow.tsx
- browser/src/shell/components/ShellNodeRenderer.tsx
- browser/src/primitives/canvas/CanvasApp.tsx
- browser/src/primitives/canvas/__tests__/canvasDragIsolation.test.tsx

---

## Edge Cases to Handle

- Shell pane rearrangement: Verify `hhs/node-id` drags still work (don't add `canvas/internal` to those)
- Non-canvas adapters: Verify explorer/files/properties adapters don't get `canvasInternal` marker
- Broadcast drags: If palette node is dragged to non-canvas pane, Shell should still ignore (isolation is correct)
- Multiple canvas panes: Each canvas pane should accept drags from any palette

---

## Deliverables

- [ ] paletteAdapter.ts sets `canvasInternal: true` in node metadata
- [ ] TreeNodeRow.tsx sets `canvas/internal` dataTransfer type and calls stopPropagation for canvas-internal drags
- [ ] ShellNodeRenderer.tsx early-returns on `canvas/internal` marker in onDragOver and onDrop
- [ ] canvasDragIsolation.test.tsx replaced with runtime behavior tests (minimum 5 tests)
- [ ] CanvasApp.tsx verified to have stopPropagation (no changes needed)

---

## Acceptance Criteria

- [ ] Palette nodes can be dragged from tree-browser to canvas without Shell intercepting the drop
- [ ] paletteAdapter.ts sets `canvasInternal: true` in node metadata
- [ ] TreeNodeRow.tsx checks `canvasInternal` and sets `dataTransfer.setData('canvas/internal', 'true')`
- [ ] TreeNodeRow.tsx calls `stopPropagation()` for canvas-internal drags
- [ ] ShellNodeRenderer.tsx checks for `canvas/internal` marker and returns early
- [ ] Drag MIME type is `application/phase-node` (consistent with existing code)
- [ ] Shell still accepts `hhs/node-id` drags for pane rearrangement
- [ ] Tests verify runtime behavior, not source code reading
- [ ] 5+ runtime tests passing

---

## Smoke Test

- [ ] cd browser && npx vitest run src/primitives/canvas/__tests__/canvasDragIsolation.test.tsx
- [ ] cd browser && npx vitest run src/primitives/tree-browser/
- [ ] cd browser && npx vitest run src/shell/
- [ ] cd browser && npx vitest run

---

## Constraints

- No file over 500 lines
- CSS: var(--sd-*) only (no hardcoded colors)
- No stubs -- fully implement all functions
- TDD: write tests FIRST, then implementation
- Do NOT break existing drag-drop for Shell pane rearrangement
- Drag MIME type must be `application/phase-node` (not `application/sd-node-type`)

---

## Instructions for Q33N

1. **Read all 5 files listed** in "Files to Read First"
2. **Write task files** to `.deia/hive/tasks/` following HIVE.md task file template
3. **Break into logical units** (one task per file group, maximum 3 tasks total)
4. **Specify test requirements** (TDD, minimum 5 runtime tests for drag isolation)
5. **Include response file requirements** (all 8 sections mandatory)
6. **Return task files to Q33NR for review** (do NOT dispatch bees yet)

---

## Expected Task Breakdown

I expect 2-3 task files:

**TASK-A:** Update paletteAdapter + TreeNodeRow for canvas-internal marker
- Read: paletteAdapter.ts, TreeNodeRow.tsx
- Write tests first (minimum 3 tests for TreeNodeRow drag behavior)
- Update paletteAdapter to set `canvasInternal: true`
- Update TreeNodeRow to propagate `canvas/internal` marker

**TASK-B:** Update ShellNodeRenderer to ignore canvas-internal drags
- Read: ShellNodeRenderer.tsx
- Write tests first (minimum 2 tests for early return on canvas/internal)
- Add early return logic to onDragOver and onDrop

**TASK-C:** Replace canvasDragIsolation.test.tsx with runtime tests
- Read: existing canvasDragIsolation.test.tsx
- Replace with runtime behavior tests (minimum 5 tests)
- Test: palette drag to canvas (success), palette drag to shell (ignored), shell pane rearrangement (still works), multiple canvas panes, non-canvas adapters

---

## Notes

- The spec mentions MIME type mismatch: test expects `application/sd-node-type`, but code uses `application/phase-node`. Keep existing `application/phase-node` — don't change it.
- CanvasApp.tsx already has `stopPropagation()` on lines 467 and 473. No changes needed there.
- This is a P0 bug — it's blocking canvas usability. Prioritize correctness over speed.

---

**Q33N: Read this briefing, read the files, write task files, return for Q33NR review.**
