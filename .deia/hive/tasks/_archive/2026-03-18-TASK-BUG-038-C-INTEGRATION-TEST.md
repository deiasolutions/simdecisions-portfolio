# TASK-BUG-038-C: Integration Test for Full Palette Drag Flow

## Objective

Write an integration test that verifies the complete drag-and-drop flow from paletteAdapter through TreeNodeRow to CanvasApp.

## Context

**Problem:** TASK-BUG-038-A and TASK-BUG-038-B fix individual components (paletteAdapter, CanvasApp), but we need an integration test to verify the FULL chain works end-to-end.

**Test scope:**
1. paletteAdapter creates node with dragMimeType and dragData
2. TreeNodeRow reads metadata and populates dataTransfer
3. CanvasApp reads dataTransfer and creates canvas node
4. stopPropagation prevents shell interference

**Why integration test needed:**
- Unit tests verify each component in isolation
- Integration test verifies they work together
- Real drag events flow through React event system
- Verifies dataTransfer is correctly passed between components

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\paletteAdapter.ts`
   - Read: `createPaletteAdapter()` and `entryToNode()`
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx`
   - Read: handleDragStart (lines 95-110)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx`
   - Read: onDragOver and onDrop handlers (lines 416-439)
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\__tests__\canvasEgg.test.ts`
   - Reference: Good example of integration test pattern (31 tests, 1164 lines)

## Deliverables

- [ ] **D1:** Create new integration test file: `browser/src/primitives/canvas/__tests__/canvas.paletteIntegration.test.tsx`
  - Test full drag flow: palette → tree-browser → canvas
  - Minimum 6 integration tests (see Test Requirements)

- [ ] **D2:** Tests verify:
  - paletteAdapter nodes have correct dragMimeType/dragData
  - TreeNodeRow populates dataTransfer on dragStart
  - CanvasApp receives correct data on drop
  - Canvas creates node at drop position
  - stopPropagation prevents shell interference
  - Multiple node types work (Task, Decision, Queue, etc.)

- [ ] **D3:** All tests pass (new integration tests + existing unit tests)

## Test Requirements

- [ ] **New test file:** `browser/src/primitives/canvas/__tests__/canvas.paletteIntegration.test.tsx`
- [ ] **Minimum 6 tests:**
  1. **Palette metadata test:** paletteAdapter nodes have dragMimeType and dragData
  2. **TreeNodeRow drag test:** TreeNodeRow sets dataTransfer correctly on drag
  3. **CanvasApp drop test:** CanvasApp reads dataTransfer and creates node
  4. **Full flow test:** Complete drag from palette to canvas (mock React DragEvent)
  5. **Multiple node types test:** Verify all palette node types work (Task, Queue, Start, End, Decision)
  6. **Isolation test:** Verify stopPropagation prevents shell from seeing events

- [ ] **Test pattern:**
  ```typescript
  import { describe, it, expect, vi, beforeEach } from 'vitest';
  import { render, fireEvent } from '@testing-library/react';
  import { createPaletteAdapter } from '../adapters/paletteAdapter';
  import { TreeNodeRow } from '../../tree-browser/TreeNodeRow';
  import CanvasApp from '../CanvasApp';

  describe('Palette to Canvas Integration', () => {
    it('should populate dataTransfer with correct MIME type and data', async () => {
      const nodes = await createPaletteAdapter();
      const taskNode = nodes[0].children?.[0]; // First palette entry (Task)

      expect(taskNode?.meta?.dragMimeType).toBe('application/sd-node-type');
      expect(taskNode?.meta?.dragData).toEqual({ nodeType: 'Task' });
    });

    it('should transfer drag data from palette to canvas', () => {
      // Mock dataTransfer
      const dataTransfer = new DataTransfer();
      const dragEvent = new DragEvent('dragstart', { dataTransfer });

      // Simulate TreeNodeRow setting data
      dataTransfer.setData('application/sd-node-type', JSON.stringify({ nodeType: 'Task' }));

      // Simulate CanvasApp reading data
      const rawData = dataTransfer.getData('application/sd-node-type');
      const parsed = JSON.parse(rawData);

      expect(parsed.nodeType).toBe('Task');
    });

    // ... more tests
  });
  ```

- [ ] **Edge cases:**
  - Empty palette (no nodes to drag)
  - Invalid node type in dragData
  - Missing dragMimeType or dragData
  - Drop outside canvas bounds
  - Multiple simultaneous drags

- [ ] **Run:** `cd browser && npx vitest run src/primitives/canvas/__tests__/canvas.paletteIntegration.test.tsx`

## Constraints

- No file over 500 lines (new test file should be ~200-300 lines)
- CSS: var(--sd-*) only (N/A — no CSS changes)
- No stubs — fully implement all tests
- TDD — this IS the test, no implementation code

## Acceptance Criteria

- [ ] **AC1:** New test file created at correct path
- [ ] **AC2:** Minimum 6 integration tests, all passing
- [ ] **AC3:** Tests verify paletteAdapter provides drag metadata
- [ ] **AC4:** Tests verify TreeNodeRow sets dataTransfer correctly
- [ ] **AC5:** Tests verify CanvasApp reads dataTransfer and creates nodes
- [ ] **AC6:** Tests verify full drag flow works end-to-end
- [ ] **AC7:** Tests verify all palette node types work (Task, Queue, Start, End, Decision, etc.)
- [ ] **AC8:** Tests verify stopPropagation prevents shell interference
- [ ] **AC9:** All existing tests still pass (paletteAdapter, TreeNodeRow, CanvasApp unit tests)
- [ ] **AC10:** No TypeScript errors in test file

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260318-TASK-BUG-038-C-RESPONSE.md`

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

- This task is PART 3 of 3 for BUG-038
- PART 1 (TASK-BUG-038-A) fixes paletteAdapter drag metadata
- PART 2 (TASK-BUG-038-B) fixes CanvasApp drag handlers
- This task ONLY writes tests — no implementation code
- Tests should use real React components (not mocks) where possible
- Tests should verify the complete data flow: palette → TreeNodeRow → CanvasApp
- Reference canvasEgg.test.ts for good integration test patterns
- If any test fails, it indicates a bug in PART 1 or PART 2 — report it in Issues section
