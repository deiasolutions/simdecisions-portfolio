# TASK-BUG-019-C: Replace Drag Isolation Tests with Runtime Behavior Tests

## Objective
Replace the existing canvasDragIsolation.test.tsx file (which uses source code reading) with runtime behavior tests that verify the actual drag-drop isolation mechanism works correctly.

## Context
The current test file (`browser/src/primitives/canvas/__tests__/canvasDragIsolation.test.tsx`) uses `fs.readFileSync()` to read source code and check for string patterns. This is brittle and doesn't verify runtime behavior.

After TASK-BUG-019-A and TASK-BUG-019-B are complete, the full drag isolation pattern will be in place:
1. paletteAdapter sets `canvasInternal: true`
2. TreeNodeRow sets `canvas/internal` dataTransfer type and calls stopPropagation
3. ShellNodeRenderer checks for `canvas/internal` and returns early

This task replaces the source-reading tests with runtime tests that:
- Mock drag events
- Verify dataTransfer types are set correctly
- Verify event handlers return early or process as expected
- Test integration between all three layers

## Files to Read First
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\canvasDragIsolation.test.tsx (current implementation)
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\paletteAdapter.ts (after TASK-BUG-019-A)
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx (after TASK-BUG-019-A)
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx (after TASK-BUG-019-B)
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx

## Deliverables
- [ ] Replace `browser/src/primitives/canvas/__tests__/canvasDragIsolation.test.tsx` with runtime behavior tests
- [ ] Minimum 8 runtime tests (no source code reading)
- [ ] All tests pass
- [ ] Test coverage includes:
  - Palette node drag creates `canvas/internal` marker
  - Shell ignores drags with `canvas/internal` marker
  - Shell accepts `hhs/node-id` drags (pane rearrangement still works)
  - Canvas accepts drags with `application/phase-node` MIME type
  - Multiple canvas panes each accept palette drags independently
  - Non-canvas adapters (explorer, files) do NOT get `canvasInternal` marker

## Test Requirements
- [ ] Tests written FIRST (TDD) — BUT this task REPLACES existing tests, so implementation is already done
- [ ] All tests pass
- [ ] NO source code reading (NO `fs.readFileSync()`)
- [ ] Use runtime mocking: mock drag events, dataTransfer objects, event handlers

### Test Coverage Requirements

**canvasDragIsolation.test.tsx** (minimum 8 runtime tests):

1. **Palette drag simulation:**
   - Create palette node via `createPaletteAdapter()`
   - Verify node has `canvasInternal: true` in meta

2. **TreeNodeRow drag event:**
   - Render TreeNodeRow with palette node
   - Simulate dragStart event
   - Verify `dataTransfer.setData('canvas/internal', 'true')` was called
   - Verify `stopPropagation()` was called

3. **ShellNodeRenderer ignores canvas/internal:**
   - Render ShellNodeRenderer with app node
   - Simulate dragOver with `canvas/internal` in dataTransfer.types
   - Verify `preventDefault()` was NOT called (early return)

4. **ShellNodeRenderer accepts hhs/node-id:**
   - Render ShellNodeRenderer with app node
   - Simulate dragOver with `hhs/node-id` in dataTransfer.types (NO `canvas/internal`)
   - Verify `preventDefault()` WAS called (shell accepts drag)

5. **Canvas accepts application/phase-node:**
   - Render CanvasApp
   - Simulate drop with `application/phase-node` in dataTransfer
   - Verify new node was added to canvas

6. **Multiple canvas panes:**
   - Render two CanvasApp instances with different nodeIds
   - Verify each has its own bus subscription
   - Verify palette drag to canvas-1 does NOT affect canvas-2

7. **Non-canvas adapter does NOT get canvasInternal:**
   - Create nodes from non-palette adapters (e.g., explorerAdapter stub)
   - Verify `canvasInternal` is NOT in meta

8. **Integration test: palette → canvas end-to-end:**
   - Create palette node
   - Render TreeNodeRow with palette node
   - Simulate dragStart
   - Render ShellNodeRenderer
   - Simulate dragOver with both `application/phase-node` and `canvas/internal`
   - Verify Shell returned early (did not intercept)
   - Render CanvasApp
   - Simulate drop
   - Verify new node appeared on canvas

## Implementation Details

### Test file structure

```typescript
/**
 * canvasDragIsolation.test.tsx
 * Runtime behavior tests for canvas drag isolation from shell pane drag system
 * Tests the full pipeline: paletteAdapter → TreeNodeRow → ShellNodeRenderer → CanvasApp
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, fireEvent } from '@testing-library/react';
import { createPaletteAdapter } from '../../../primitives/tree-browser/adapters/paletteAdapter';
import { TreeNodeRow } from '../../../primitives/tree-browser/TreeNodeRow';
import { ShellNodeRenderer } from '../../../shell/components/ShellNodeRenderer';
import { CanvasApp } from '../CanvasApp';
import type { TreeNodeData } from '../../../primitives/tree-browser/types';

describe('Canvas Drag Isolation - Runtime Behavior', () => {
  describe('Palette Adapter', () => {
    it('should set canvasInternal: true on all palette nodes', async () => {
      // Test implementation
    });
  });

  describe('TreeNodeRow Drag Handling', () => {
    it('should set canvas/internal dataTransfer type for palette nodes', () => {
      // Test implementation
    });

    it('should call stopPropagation for canvas-internal drags', () => {
      // Test implementation
    });
  });

  describe('ShellNodeRenderer Canvas Drag Filtering', () => {
    it('should return early on dragOver when canvas/internal is present', () => {
      // Test implementation
    });

    it('should accept hhs/node-id drags (shell pane rearrangement)', () => {
      // Test implementation
    });
  });

  describe('CanvasApp Drop Handling', () => {
    it('should accept application/phase-node drags', () => {
      // Test implementation
    });
  });

  describe('Integration Tests', () => {
    it('should isolate palette drag from shell interception', () => {
      // End-to-end test
    });

    it('should support multiple canvas panes independently', () => {
      // Multiple canvas test
    });

    it('should NOT set canvasInternal on non-canvas adapters', () => {
      // Non-canvas adapter test
    });
  });
});
```

### Mock dataTransfer helper

Create a mock dataTransfer object for drag events:

```typescript
function createMockDataTransfer(types: string[] = [], data: Record<string, string> = {}) {
  const store = new Map<string, string>(Object.entries(data));
  return {
    types,
    effectAllowed: 'none' as DataTransfer['effectAllowed'],
    dropEffect: 'none' as DataTransfer['dropEffect'],
    setData: vi.fn((type: string, value: string) => {
      store.set(type, value);
      if (!types.includes(type)) types.push(type);
    }),
    getData: vi.fn((type: string) => store.get(type) || ''),
    clearData: vi.fn(() => store.clear()),
  } as unknown as DataTransfer;
}
```

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (no hardcoded colors)
- No stubs — fully implement all test functions
- NO source code reading (NO `fs.readFileSync()`)
- All tests must use runtime mocking and rendering
- Drag MIME type is `application/phase-node` (not `application/sd-node-type`)

## Acceptance Criteria
- [ ] canvasDragIsolation.test.tsx replaced with runtime behavior tests
- [ ] NO source code reading (NO `fs.readFileSync()`)
- [ ] Minimum 8 runtime tests passing
- [ ] Tests verify palette → TreeNodeRow → ShellNodeRenderer → CanvasApp integration
- [ ] Tests verify Shell still accepts `hhs/node-id` drags
- [ ] Tests verify non-canvas adapters do NOT get `canvasInternal` marker
- [ ] Drag MIME type is `application/phase-node` (verified at runtime, not in source code)
- [ ] All existing canvas tests still pass

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260325-TASK-BUG-019-C-RESPONSE.md`

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
