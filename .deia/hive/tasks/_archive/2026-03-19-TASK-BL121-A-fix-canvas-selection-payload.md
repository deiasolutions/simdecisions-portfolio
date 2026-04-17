# TASK-BL121-A: Fix Canvas Selection Event Payload

## Objective

Fix the data payload sent by CanvasApp when a node is selected, so that the properties panel receives the correct data shape.

## Context

**Problem:** CanvasApp.tsx currently sends `data: node.data` (just the NodeData) when publishing `canvas:node-selected` events. The properties adapter expects a wrapped object with the full node structure.

**Root Cause:** Line 415 in CanvasApp.tsx sends:
```typescript
data: node.data  // This is NodeData (label, nodeType, operator, timing, etc.)
```

But propertiesAdapter.ts expects:
```typescript
data: { node: Node }  // Wrapped in object, expects full node
```

**What needs to happen:**
1. Update CanvasApp to send the correct data shape
2. Add proper TypeScript types for the canvas:node-selected event payload
3. Add deselection handling (canvas background click, ESC key)
4. Add tests for selection and deselection flows

## Files to Read First

**Canvas:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\types.ts`

**Bus Types:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\busTypes.ts`

**Tests (reference):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\CanvasApp.test.tsx`

## Deliverables

- [ ] **Add TypeScript type** for canvas:node-selected payload to busTypes.ts:
  ```typescript
  export interface CanvasNodeSelectedData {
    nodeId: string;
    node: {
      id: string;
      type: string;
      position: { x: number; y: number };
      data: NodeData;
    };
  }
  ```

- [ ] **Update CanvasApp.tsx line 410-415** to send correct payload:
  ```typescript
  publish('canvas:node-selected', {
    nodeId: node.id,
    node: {
      id: node.id,
      type: node.type || 'default',
      position: node.position,
      data: node.data,
    },
  });
  ```

- [ ] **Add deselection handler** for canvas background clicks:
  - Subscribe to ReactFlow's onPaneClick event
  - Publish `canvas:node-deselected` with empty payload
  - Clear selected nodes in state

- [ ] **Add ESC key handler** for deselection:
  - Add keyboard event listener
  - On ESC: clear selection, publish deselect event
  - Clean up listener in useEffect

- [ ] **Add TypeScript type** for canvas:node-deselected to busTypes.ts

- [ ] **CSS** (if any changes): use `var(--sd-*)` only, no hardcoded colors

## Test Requirements

**Create/update:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\CanvasApp.test.tsx`

- [ ] **Tests written FIRST** (TDD)
- [ ] Test: selecting a node publishes canvas:node-selected with correct payload structure
- [ ] Test: canvas:node-selected payload includes nodeId, node.id, node.type, node.position, node.data
- [ ] Test: clicking canvas background publishes canvas:node-deselected
- [ ] Test: pressing ESC publishes canvas:node-deselected
- [ ] Test: deselection clears selected nodes in CanvasApp state
- [ ] Test: deselection event has empty/null payload
- [ ] Test: multiple selection → deselection flow works
- [ ] **All existing CanvasApp tests still pass** (no regressions)
- [ ] All new tests pass

**Minimum: 8 new tests**

## Constraints

- **No file over 500 lines** — if CanvasApp.tsx approaches 500 lines after changes, extract handlers to separate file
- **CSS: var(--sd-*) only** — no hardcoded colors
- **No stubs** — every handler fully implemented
- **Absolute paths** in all file references
- **TDD** — write tests first, verify they fail, then implement

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260319-TASK-BL121-A-RESPONSE.md`

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

- [ ] CanvasApp sends correct data shape on node selection (nodeId + full node object)
- [ ] Canvas background click triggers deselection
- [ ] ESC key triggers deselection
- [ ] TypeScript types added for both events
- [ ] 8+ new tests written and passing
- [ ] No regressions in existing canvas tests
- [ ] No hardcoded colors
- [ ] No file over 500 lines
- [ ] No stubs or TODO comments

## Smoke Test Commands

```bash
# Run canvas tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run --reporter=verbose src/primitives/canvas/__tests__/CanvasApp.test.tsx

# Run all canvas tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run --reporter=verbose src/primitives/canvas/

# Full browser test suite (regression check)
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run
```

## Dependencies

- None (this task is independent and can run in parallel with TASK-BL121-B)

## Notes for Bee

1. **ReactFlow onPaneClick** is the background click handler. Add it to the ReactFlow component props.

2. **Keyboard listener** should be added in useEffect with proper cleanup:
   ```typescript
   useEffect(() => {
     const handleKeyDown = (e: KeyboardEvent) => {
       if (e.key === 'Escape') { /* deselect */ }
     };
     window.addEventListener('keydown', handleKeyDown);
     return () => window.removeEventListener('keydown', handleKeyDown);
   }, []);
   ```

3. **Mock the bus** in tests using the existing pattern from CanvasApp.test.tsx.

4. **Don't break existing selection behavior** — this is additive only. Selection should still work exactly as before, just with correct data shape.

5. **busTypes.ts** — add new types to the existing bus event type unions.

---

**End of Task File**
