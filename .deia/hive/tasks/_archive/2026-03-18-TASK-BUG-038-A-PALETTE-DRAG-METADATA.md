# TASK-BUG-038-A: Add Drag Metadata to paletteAdapter

## Objective

Fix paletteAdapter to set dragMimeType and dragData in node.meta so TreeNodeRow can populate dataTransfer during drag operations.

## Context

**Problem:** Users cannot drag palette items onto canvas. Root cause: paletteAdapter creates nodes with `draggable: true` but doesn't provide the drag metadata that TreeNodeRow expects.

**Current behavior:**
- paletteAdapter.ts (line 56-59): Sets `meta: { nodeType, description }` but NOT dragMimeType/dragData
- TreeNodeRow.tsx (line 99-107): Reads `meta.dragMimeType` and `meta.dragData`, but paletteAdapter never sets them
- Result: dataTransfer is never populated, so canvas receives no data on drop

**Expected flow:**
1. paletteAdapter sets `meta.dragMimeType = 'application/sd-node-type'` and `meta.dragData = { nodeType }`
2. TreeNodeRow reads these fields in handleDragStart (line 104)
3. TreeNodeRow calls `e.dataTransfer.setData(dragMimeType, JSON.stringify(dragData))`
4. CanvasApp onDrop reads `getData('application/sd-node-type')` and parses JSON
5. Node created on canvas

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\paletteAdapter.ts` (96 lines)
   - Current: `entryToNode()` function (lines 50-61) — missing dragMimeType/dragData
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx` (169 lines)
   - Read: handleDragStart (lines 95-110) — shows what metadata it expects
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\types.ts` (82 lines)
   - Read: TreeNodeData.meta type definition (line 13)

## Deliverables

- [ ] **D1:** Write tests FIRST (TDD) — new file: `browser/src/primitives/tree-browser/adapters/__tests__/paletteAdapter.test.ts`
  - Test: `entryToNode()` sets `meta.dragMimeType = 'application/sd-node-type'`
  - Test: `entryToNode()` sets `meta.dragData = { nodeType: <entry.nodeType> }`
  - Test: All palette entries have draggable=true
  - Test: dragData.nodeType matches entry.nodeType exactly
  - Minimum 4 tests

- [ ] **D2:** Modify `paletteAdapter.ts` line 56-59 to add drag metadata:
  ```typescript
  function entryToNode(entry: PaletteEntry): TreeNodeData {
    return {
      id: `palette-node-${entry.nodeType.toLowerCase().replace(/\s+/g, '-')}`,
      label: entry.label,
      icon: entry.icon,
      draggable: true,
      meta: {
        nodeType: entry.nodeType,
        description: entry.description,
        dragMimeType: 'application/sd-node-type',  // ← ADD THIS
        dragData: { nodeType: entry.nodeType },    // ← ADD THIS
      },
    }
  }
  ```

- [ ] **D3:** All tests pass (new + existing)

## Test Requirements

- [ ] **TDD:** Write tests FIRST, then implementation
- [ ] **New test file:** `browser/src/primitives/tree-browser/adapters/__tests__/paletteAdapter.test.ts`
- [ ] **Minimum 4 tests:**
  1. `entryToNode` sets `meta.dragMimeType` correctly
  2. `entryToNode` sets `meta.dragData` with correct nodeType
  3. All palette nodes have `draggable: true`
  4. Drag metadata is JSON-serializable (matches TreeNodeRow expectations)
- [ ] **Edge cases:**
  - Verify dragData.nodeType matches entry.nodeType exactly (no transforms)
  - Verify dragMimeType is constant string `'application/sd-node-type'`
- [ ] **Existing tests pass:** All tree-browser tests must still pass
- [ ] **Run:** `cd browser && npx vitest run src/primitives/tree-browser/adapters/__tests__/paletteAdapter.test.ts`

## Constraints

- No file over 500 lines (paletteAdapter.ts is 96 lines, adding tests is fine)
- CSS: var(--sd-*) only (N/A — no CSS changes)
- No stubs — fully implement all changes
- TDD — tests first, then implementation

## Acceptance Criteria

- [ ] **AC1:** paletteAdapter `entryToNode()` function sets `meta.dragMimeType = 'application/sd-node-type'`
- [ ] **AC2:** paletteAdapter `entryToNode()` function sets `meta.dragData = { nodeType: entry.nodeType }`
- [ ] **AC3:** All palette node types (Task, Queue, Start, End, Decision, etc.) have correct drag metadata
- [ ] **AC4:** Drag metadata format matches TreeNodeRow expectations (JSON-serializable object)
- [ ] **AC5:** New test file created with minimum 4 passing tests
- [ ] **AC6:** All existing tree-browser tests still pass
- [ ] **AC7:** No TypeScript errors in paletteAdapter.ts

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260318-TASK-BUG-038-A-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Notes

- This task is PART 1 of 3 for BUG-038
- PART 2 (TASK-BUG-038-B) will fix CanvasApp to add stopPropagation and parse JSON
- PART 3 (TASK-BUG-038-C) will write integration tests for full drag flow
- This task ONLY fixes paletteAdapter — do NOT modify CanvasApp or TreeNodeRow
- TreeNodeRow is already correct (it reads meta fields) — it just needs paletteAdapter to provide them
