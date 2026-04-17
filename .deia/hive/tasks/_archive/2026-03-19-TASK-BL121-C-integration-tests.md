# TASK-BL121-C: Canvas Properties Integration Tests

## Objective

Write end-to-end integration tests that verify the complete flow from canvas node selection to properties panel display and back.

## Context

**What this tests:** The integration between CanvasApp and propertiesAdapter through the message bus.

**Flow to verify:**
1. User clicks canvas node → CanvasApp publishes canvas:node-selected
2. propertiesAdapter receives event → maps node data → updates tree-browser
3. Properties panel displays node properties (General, Timing, Operator sections)
4. User clicks canvas background or presses ESC → CanvasApp publishes canvas:node-deselected
5. propertiesAdapter receives deselect event → clears properties panel

**This is an integration test** — it tests the interaction between components, not individual unit behavior.

## Files to Read First

**Components to integrate:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\propertiesAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeBrowser.tsx`

**Bus infrastructure:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\busTypes.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\MessageBus.tsx`

**Test utilities:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\test\setup.ts`

**Reference integration tests:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\canvas-properties-integration.test.tsx` (if exists)

## Files You May Modify

**Maximum 1 file:**

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\canvas-properties-integration.test.tsx` (NEW)
   - Create integration test file only

## Files You Must NOT Modify

- **NO modifications to CanvasApp.tsx** — implementation is complete (from TASK-BL121-A)
- **NO modifications to propertiesAdapter.ts** — implementation is complete (from TASK-BL121-B)
- **NO modifications to TreeBrowser.tsx** — existing component
- **NO modifications to MessageBus or busTypes** — infrastructure is stable
- **NO modifications to any source files** — this is a TEST-ONLY task

## Deliverables

- [ ] **Create integration test file:**
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\canvas-properties-integration.test.tsx`

- [ ] **Test: Select node → properties display**
  - Render CanvasApp + TreeBrowser with propertiesAdapter
  - Simulate node selection (click or programmatic)
  - Assert: canvas:node-selected event published
  - Assert: properties panel shows node properties (check for node ID, label, type)
  - Assert: properties organized in accordion sections (General, Timing, Operator)

- [ ] **Test: Deselect node → properties clear**
  - Select a node (properties visible)
  - Simulate background click or ESC press
  - Assert: canvas:node-deselected event published
  - Assert: properties panel clears (empty or shows "No node selected")

- [ ] **Test: Switch selection → properties update**
  - Select node A (properties show node A data)
  - Select node B (properties show node B data)
  - Assert: properties panel switches from A to B
  - Assert: no stale data from node A

- [ ] **Test: Deselect → re-select → properties restore**
  - Select node → deselect → select same node again
  - Assert: properties restore correctly
  - Assert: no state corruption

- [ ] **Test: Missing node data → graceful fallback**
  - Select node with incomplete/null data
  - Assert: properties panel shows defaults or "N/A"
  - Assert: no crash, no console errors

- [ ] **Test: Bus event payload structure**
  - Select node
  - Capture canvas:node-selected event
  - Assert: payload structure matches CanvasNodeSelectedData type
  - Assert: all required fields present (nodeId, node.id, node.type, node.position, node.data)

- [ ] **Test: Full regression smoke test**
  - Run all canvas tests
  - Run all tree-browser tests
  - Assert: no regressions (all existing tests still pass)

## Test Requirements

**Create:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\canvas-properties-integration.test.tsx`

- [ ] **Tests written FIRST** (TDD)
- [ ] Minimum 7 integration tests (as listed above)
- [ ] All tests use React Testing Library + Vitest
- [ ] Mock MessageBus or use real instance (decide based on test complexity)
- [ ] All tests pass
- [ ] Test file under 500 lines
- [ ] No stubs — every test fully implemented

**Minimum: 7 integration tests**

## Constraints

- **No file over 500 lines** — modularize if test file grows large
- **No stubs** — every test must be fully implemented and passing
- **Absolute paths** in all file references
- **TDD** — write tests first (they will fail until TASK-BL121-A and TASK-BL121-B are complete)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260319-TASK-BL121-C-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy deliverables from above, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Acceptance Criteria

- [ ] 7+ integration tests written and passing
- [ ] Test file created at correct path
- [ ] Select → properties display test passes
- [ ] Deselect → properties clear test passes
- [ ] Switch selection test passes
- [ ] Re-select test passes
- [ ] Missing data test passes
- [ ] Event payload structure test passes
- [ ] Regression smoke test passes (all existing tests still pass)
- [ ] No file over 500 lines
- [ ] No stubs or TODO comments

## Smoke Test Commands

```bash
# Run integration tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run --reporter=verbose src/primitives/canvas/__tests__/canvas-properties-integration.test.tsx

# Run all canvas tests (regression check)
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run --reporter=verbose src/primitives/canvas/

# Run all tree-browser tests (regression check)
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run --reporter=verbose src/primitives/tree-browser/

# Full browser test suite
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run
```

## Dependencies

- **Depends on:** TASK-BL121-A (canvas selection payload) AND TASK-BL121-B (properties adapter data handling)
- **Run after:** Both A and B are complete
- **Can run in parallel:** No — this depends on A and B completing first

## Notes for Bee

1. **Integration test pattern:**
   ```typescript
   import { render, screen, fireEvent } from '@testing-library/react';
   import { vi } from 'vitest';
   import CanvasApp from '../CanvasApp';
   import TreeBrowser from '../../tree-browser/TreeBrowser';
   import { propertiesAdapter } from '../../tree-browser/adapters/propertiesAdapter';

   describe('Canvas Properties Integration', () => {
     it('should display properties when node is selected', () => {
       // Render components with shared bus
       // Simulate node selection
       // Assert properties display
     });
   });
   ```

2. **MessageBus setup:** You may need a shared MessageBus instance between CanvasApp and TreeBrowser in your tests. Check existing test patterns for how to do this.

3. **ReactFlow mocking:** CanvasApp uses ReactFlow, which may need mocking in tests. Check CanvasApp.test.tsx for the mock pattern.

4. **Test data:** Create sample NodeData objects for testing. Include all required fields (id, type, label, timing, operator, etc.).

5. **Async handling:** Bus events are async. Use `waitFor()` from React Testing Library to wait for state updates.

6. **Don't duplicate unit tests** — these are integration tests. Focus on the interaction between components, not individual unit behavior (that's covered in TASK-BL121-A and TASK-BL121-B).

7. **Expected failures** — if TASK-BL121-A and TASK-BL121-B are not complete yet, these tests WILL fail. That's expected. Write them to pass once A and B are done.

---

**End of Task File**
