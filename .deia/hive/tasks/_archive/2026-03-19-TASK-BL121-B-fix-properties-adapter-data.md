# TASK-BL121-B: Fix Properties Adapter Data Handling

## Objective

Update the properties adapter to correctly process the canvas node data from `canvas:node-selected` events and display properties in the properties pane.

## Context

**Problem:** The properties adapter currently expects an IR Node type, but receives a ReactFlow Node with Canvas NodeData. This causes a type mismatch and the properties pane fails to display.

**What needs to happen:**
1. Update propertiesAdapter to handle the new canvas:node-selected payload structure
2. Map Canvas NodeData → displayable property tree
3. Handle deselection (clear properties pane on canvas:node-deselected)
4. Update existing tests and add deselection tests

**Current code** (propertiesAdapter.ts line 206):
```typescript
const event = data as { node: Node };  // Expects IR Node
```

**Needs to become:**
```typescript
const event = data as CanvasNodeSelectedData;  // Handle canvas node structure
```

## Files to Read First

**Properties Adapter:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\propertiesAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\propertiesAdapter.test.ts`

**Canvas Types:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\types.ts`

**Bus Types:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\busTypes.ts`

**Reference (similar adapter):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\simPropertiesAdapter.ts`

## Deliverables

- [ ] **Update propertiesAdapter.ts** to handle new canvas:node-selected payload:
  - Import CanvasNodeSelectedData type from busTypes.ts
  - Update event handler (line 204-230) to process canvas node structure
  - Map canvas NodeData fields to tree-browser items

- [ ] **Add mapping function** to transform Canvas NodeData → property tree:
  ```typescript
  function mapCanvasNodeToProperties(node: CanvasNodeSelectedData['node']): TreeNodeData[] {
    // Map node.data (NodeData) to accordion sections:
    // - General: id, type, label
    // - Timing: distribution, mean, std, min, max
    // - Operator: operator type, params
    // - Connections: edges (if available)
  }
  ```

- [ ] **Subscribe to canvas:node-deselected** event:
  - When deselect event fires, clear properties pane
  - Set tree root to empty array
  - Publish properties:cleared bus event (if needed)

- [ ] **Handle missing/null data** gracefully:
  - If node.data is missing fields, show defaults or "N/A"
  - If node.data is null, show empty state
  - Don't crash on unexpected data shapes

- [ ] **Update existing tests** in propertiesAdapter.test.ts:
  - Update test payloads to match new CanvasNodeSelectedData structure
  - Ensure all existing tests still pass

- [ ] **Add new tests** for deselection and edge cases (minimum 5 new tests)

- [ ] **CSS** (if any changes): use `var(--sd-*)` only, no hardcoded colors

## Test Requirements

**Update/create:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\propertiesAdapter.test.ts`

- [ ] **Tests written FIRST** (TDD)
- [ ] Test: canvas:node-selected with new payload structure displays properties
- [ ] Test: NodeData.label → General section displays correct label
- [ ] Test: NodeData.timing → Timing section displays timing properties
- [ ] Test: NodeData.operator → Operator section displays operator properties
- [ ] Test: canvas:node-deselected clears properties pane
- [ ] Test: deselection publishes properties:cleared (if applicable)
- [ ] Test: missing NodeData fields don't crash (shows defaults/N/A)
- [ ] Test: null node.data shows empty state
- [ ] **All existing propertiesAdapter tests still pass** (no regressions)
- [ ] All new tests pass

**Minimum: 5 new tests, all existing tests passing**

## Constraints

- **No file over 500 lines** — if propertiesAdapter.ts approaches 500 lines, extract mapping logic to separate file
- **CSS: var(--sd-*) only** — no hardcoded colors
- **No stubs** — all mapping functions fully implemented
- **Absolute paths** in all file references
- **TDD** — write tests first, verify they fail, then implement

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260319-TASK-BL121-B-RESPONSE.md`

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

- [ ] propertiesAdapter handles new CanvasNodeSelectedData payload
- [ ] Canvas NodeData correctly mapped to property tree (General, Timing, Operator sections)
- [ ] Deselection event clears properties pane
- [ ] Missing/null data handled gracefully (no crashes)
- [ ] 5+ new tests written and passing
- [ ] All existing tests still pass (no regressions)
- [ ] No hardcoded colors
- [ ] No file over 500 lines
- [ ] No stubs or TODO comments

## Smoke Test Commands

```bash
# Run propertiesAdapter tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run --reporter=verbose src/primitives/tree-browser/adapters/__tests__/propertiesAdapter.test.ts

# Run all tree-browser adapter tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run --reporter=verbose src/primitives/tree-browser/adapters/

# Full browser test suite (regression check)
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run
```

## Dependencies

- None (this task is independent and can run in parallel with TASK-BL121-A)

## Notes for Bee

1. **Accordion structure:** The properties pane uses tree-browser with accordion sections. Each top-level node is a section (General, Timing, Operator, Connections). Each section has children (individual properties).

2. **TreeNodeData structure:**
   ```typescript
   {
     id: string;        // e.g., "section-general"
     label: string;     // e.g., "General"
     type: 'accordion' | 'property';
     children?: TreeNodeData[];
     meta?: {
       value: string | number;  // property value
       editable?: boolean;      // future: make editable
     };
   }
   ```

3. **Reference simPropertiesAdapter.ts** for the pattern of building property trees from node data.

4. **Don't break existing tests** — update test payloads to match new structure, but ensure all existing assertions still pass.

5. **Handle undefined gracefully** — if node.data.timing is undefined, show "Timing" section with "No timing data" or similar.

6. **Bus event naming** — follow existing patterns from busTypes.ts. If adding properties:cleared event, add type to busTypes.ts.

---

**End of Task File**
