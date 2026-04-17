# BRIEFING: BL-121 — Port Properties Panel Editing UI

**Date:** 2026-03-18
**From:** Q88NR (Regent)
**To:** Q33N (Queen Coordinator)
**Spec:** BL-121 (P0)
**Model:** sonnet

---

## Objective

Complete the properties panel editing UI for the Canvas EGG. The properties adapter exists and displays read-only properties. The task is to:

1. **Make properties editable** — add inline editing UI to the tree-browser
2. **Wire property changes back to canvas** — update canvas state when properties change
3. **Test the full round-trip** — select node → edit property → canvas updates

---

## Context

### What Already Exists

The properties adapter (`browser/src/primitives/tree-browser/adapters/propertiesAdapter.ts`) is implemented and working:

- ✅ Listens to `canvas:node-selected` bus events
- ✅ Displays node properties in accordion sections (General, Timing, Operator, Connections)
- ✅ Has an `updateProperty()` method that publishes `properties:value-changed` bus events
- ✅ Is wired to the Canvas EGG (canvas.egg.md line 109-116)
- ✅ Tests exist: `browser/src/primitives/tree-browser/adapters/__tests__/propertiesAdapter.test.ts`

### What's Missing

1. **Inline editing UI in TreeBrowser** — Currently, tree-browser renders properties as read-only labels. No input fields, no edit controls.
2. **Canvas subscription to property changes** — CanvasApp does NOT subscribe to `properties:value-changed` events. Property changes are published but ignored.
3. **Test coverage for editing** — Existing tests verify display, not editing.

---

## Files to Read First

### Properties Adapter (already implemented)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\propertiesAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\propertiesAdapter.test.ts`

### Tree Browser (needs editing UI)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeBrowser.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\types.ts`

### Canvas App (needs to subscribe to property changes)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx`

### EGG Config
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md`

### Reference Implementation (simPropertiesAdapter for comparison)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\simPropertiesAdapter.ts`

---

## Deliverables

This is a **2-task breakdown**:

### TASK A: Add Inline Editing UI to Tree Browser
**Objective:** Extend TreeBrowser to support inline property editing.

**Deliverables:**
- [ ] Add `editable: boolean` flag to `TreeNodeData` meta (types.ts)
- [ ] Update `TreeNodeRow.tsx` to detect editable nodes and render input fields
- [ ] Support text inputs (string), number inputs (number), and dropdowns (enum)
- [ ] Call `adapter.updateProperty()` on blur/enter
- [ ] CSS for inline edit controls using `var(--sd-*)` only
- [ ] Tests for TreeNodeRow editing behavior (click to edit, blur saves, enter saves, escape cancels)

**Test Requirements:**
- [ ] Tests written FIRST (TDD)
- [ ] Tests for text input edit
- [ ] Tests for number input edit
- [ ] Tests for dropdown edit (if applicable)
- [ ] Tests for blur save
- [ ] Tests for enter save
- [ ] Tests for escape cancel
- [ ] All tests pass

**Constraints:**
- No file over 500 lines (modularize if TreeNodeRow grows)
- CSS: `var(--sd-*)` only
- No stubs

**Files to modify:**
- `browser/src/primitives/tree-browser/types.ts`
- `browser/src/primitives/tree-browser/TreeNodeRow.tsx`
- `browser/src/primitives/tree-browser/__tests__/TreeNodeRow.test.tsx` (create if missing)

---

### TASK B: Wire Property Changes to Canvas
**Objective:** Subscribe to `properties:value-changed` events in CanvasApp and update node data.

**Deliverables:**
- [ ] Subscribe to `properties:value-changed` in CanvasApp's bus effect
- [ ] On property change, find the node by ID and update its data
- [ ] Use `setNodes()` to apply the update reactively
- [ ] Handle nested properties (e.g., `config.timing.distribution`)
- [ ] Publish `canvas:node-updated` after applying the change
- [ ] Tests for property update flow (mock bus, publish property-changed, verify node updated)

**Test Requirements:**
- [ ] Tests written FIRST (TDD)
- [ ] Test: property change updates node data
- [ ] Test: nested property change works (e.g., timing.distribution)
- [ ] Test: invalid node ID is ignored
- [ ] Test: canvas:node-updated is published after update
- [ ] All tests pass

**Constraints:**
- No file over 500 lines
- CSS: `var(--sd-*)` only (if any CSS changes)
- No stubs

**Files to modify:**
- `browser/src/primitives/canvas/CanvasApp.tsx`
- `browser/src/primitives/canvas/__tests__/CanvasApp.test.tsx` (add property change tests)

---

### TASK C: Integration Test
**Objective:** End-to-end test for the full flow.

**Deliverables:**
- [ ] Integration test file: `browser/src/primitives/canvas/__tests__/canvas-properties-integration.test.tsx`
- [ ] Test: select node → properties panel shows properties → edit property → canvas node updates
- [ ] Test: deselect node → properties panel clears
- [ ] Test: select different node → properties panel switches
- [ ] All tests pass

**Test Requirements:**
- [ ] Tests written FIRST (TDD)
- [ ] At least 4 scenarios (select, edit, deselect, switch)
- [ ] All tests pass

**Constraints:**
- File must be under 500 lines
- No stubs

**Files to create:**
- `browser/src/primitives/canvas/__tests__/canvas-properties-integration.test.tsx`

---

## Acceptance Criteria

From BL-121 spec:
- [ ] Selecting a canvas node shows its properties in the panel
- [ ] Editing a property updates the canvas node
- [ ] Deselecting clears the panel
- [ ] Tests pass

**Additional:**
- [ ] No hardcoded colors (all CSS uses `var(--sd-*)`)
- [ ] No file over 500 lines
- [ ] No stubs or TODO comments shipped

---

## Smoke Test

After all tasks complete:

```bash
# Run tree-browser tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run --reporter=verbose src/primitives/tree-browser/

# Run canvas tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run --reporter=verbose src/primitives/canvas/

# Run all browser tests (full regression)
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run
```

---

## Notes for Q33N

1. **Mark properties as editable in the adapter.** Update `propertiesAdapter.ts` to set `meta: { value: X, editable: true }` for properties that should be editable. ID and Type are typically read-only. Name, timing, operator fields should be editable.

2. **Input type inference.** Use the value type to determine input control:
   - `typeof value === 'string'` → text input
   - `typeof value === 'number'` → number input
   - Array of strings → dropdown (if enum-like)

3. **Nested property updates.** When `properties:value-changed` publishes `{ nodeId, field, value }`, the field may be a dot path (e.g., `"config.timing.distribution"`). Use a helper to set nested values.

4. **Don't break existing behavior.** The properties adapter already works for display. Ensure your changes are additive and don't break the read-only display mode.

5. **Refer to platform repo if needed.** The platform repo (`platform/simdecisions-2/`) may have a similar properties panel implementation. Check there for patterns.

---

## Task Breakdown Summary

| Task | Deliverable | Files Modified | Test Files |
|------|-------------|----------------|------------|
| **TASK-BL-121-A** | Inline editing UI in TreeBrowser | types.ts, TreeNodeRow.tsx | TreeNodeRow.test.tsx |
| **TASK-BL-121-B** | Wire property changes to Canvas | CanvasApp.tsx | CanvasApp.test.tsx |
| **TASK-BL-121-C** | Integration test | (none) | canvas-properties-integration.test.tsx |

---

## Next Steps for Q33N

1. Read all files listed in "Files to Read First"
2. Write three task files (TASK-BL-121-A, TASK-BL-121-B, TASK-BL-121-C)
3. Return to Q88NR for review
4. After approval, dispatch bees to all three tasks in parallel (they are independent)
5. Monitor bee responses
6. Report completion to Q88NR

---

**End of Briefing**
