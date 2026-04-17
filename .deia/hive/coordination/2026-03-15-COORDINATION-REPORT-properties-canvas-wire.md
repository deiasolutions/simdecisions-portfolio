# COORDINATION REPORT: Wire Properties Panel to Canvas

**Date:** 2026-03-15
**Q33N Bot:** QUEEN-2026-03-15-BRIEFING-properties
**Model:** Sonnet
**Briefing:** `.deia/hive/coordination/2026-03-15-BRIEFING-properties-canvas-wire.md`
**Spec:** `.deia/hive/queue/2026-03-15-1558-SPEC-w2-03-properties-canvas-wire.md`

---

## Status

**READY FOR REVIEW**

I have analyzed the codebase and the briefing. The current implementation already handles node selection → properties display. What's missing is the reverse flow: property edit → canvas update.

---

## Analysis

### What Already Works

1. **Node selection → Properties display** (FlowDesigner.tsx lines 111-133, simPropertiesAdapter.ts lines 111-119)
   - Clicking canvas node emits `sim:node-selected` bus event
   - simPropertiesAdapter subscribes and updates `selectedNodeData`
   - Properties panel displays read-only tree of node properties

2. **Bus infrastructure** (infrastructure/relay_bus/)
   - Bus events working end-to-end
   - External panes pattern established

### What's Missing

1. **Editable tree nodes** — TreeNodeData has no `editable` field or value editing capability
2. **Property change event** — No `sim:node-property-changed` event defined
3. **Canvas subscription** — FlowDesigner doesn't listen for property updates from bus

---

## Recommendation

**APPROVE Option A from briefing** (editable tree nodes via TreeBrowser primitive).

### Why Option A?

- Reuses existing tree-browser primitive (no new component)
- Smaller surface area (3 file modifications + 3 test files)
- Consistent with DEIA pane primitive philosophy
- Easier to test incrementally via TDD

### Which Properties to Make Editable?

**First pass (recommended):**
- `label` (General section)
- `description` (General section)
- `duration.value` (Timing section)

**Defer to future tasks:**
- `duration.kind` (requires dropdown)
- `duration.min` / `duration.max` (requires validation)
- `resource.capacity` (requires number validation)
- `checkpoint` fields (requires conditional logic)
- `group.childNodeIds` (managed by grouping operations)

### Validation Strategy

**Inline validation on input blur:**
- Empty label → restore previous value
- Invalid number (duration) → restore previous value
- Show inline error state on input (red border)
- Do NOT emit bus event for invalid values

---

## Task Breakdown

I propose **3 sequential tasks** (TDD approach):

### TASK-165: Add editable fields to TreeNodeData + TreeBrowser (HAIKU)

**Deliverables:**
- Extend `TreeNodeData` interface with `editable?: boolean`, `value?: string`, `onValueChange?: (value: string) => void`
- Extend `TreeBrowserProps` with `onValueChange?: (nodeId: string, newValue: string) => void`
- Update `TreeNodeRow` to render `<input>` when `editable=true`
- Forward `onValueChange` from TreeBrowser → TreeNodeRow
- CSS: input field styling using `var(--sd-*)` only

**Test requirements:**
- 5 tests in `browser/src/primitives/tree-browser/__tests__/TreeNodeRow.test.tsx`:
  1. Renders static label when `editable=false` (or undefined)
  2. Renders input when `editable=true`
  3. Input shows `value` prop
  4. Calls `node.onValueChange` when input blur
  5. Handles Enter key to commit value

**Files modified:**
- `browser/src/primitives/tree-browser/types.ts`
- `browser/src/primitives/tree-browser/TreeBrowser.tsx`
- `browser/src/primitives/tree-browser/TreeNodeRow.tsx`
- `browser/src/primitives/tree-browser/tree-browser.css`

**Tests created:**
- `browser/src/primitives/tree-browser/__tests__/TreeNodeRow.test.tsx` (new file)

**Acceptance criteria:**
- [ ] TreeNodeData has `editable`, `value`, `onValueChange` fields
- [ ] TreeNodeRow renders input when `editable=true`
- [ ] Input commits value on blur and Enter key
- [ ] All 5 tests pass
- [ ] No new CSS violations (only `var(--sd-*)`)

**Smoke test:**
```bash
cd browser && npx vitest run src/primitives/tree-browser/
```

---

### TASK-166: Wire simPropertiesAdapter to emit property-change events (HAIKU)

**Deliverables:**
- Add `sim:node-property-changed` to bus constants
- Update `simPropertiesAdapter.ts` to mark `label` and `description` as editable
- Implement `onValueChange` handler that parses node ID, emits bus event
- Parse property ID format: `sim-prop-label` → `{ field: 'label' }`
- Emit bus event with shape: `{ type: 'sim:node-property-changed', data: { nodeId, field, value } }`

**Test requirements:**
- 3 new tests in `browser/src/primitives/tree-browser/adapters/__tests__/simPropertiesAdapter.test.ts`:
  1. Label property node has `editable=true`
  2. Description property node has `editable=true`
  3. Changing label emits `sim:node-property-changed` with correct data

**Files modified:**
- `browser/src/infrastructure/relay_bus/constants.ts`
- `browser/src/primitives/tree-browser/adapters/simPropertiesAdapter.ts`

**Tests extended:**
- `browser/src/primitives/tree-browser/adapters/__tests__/simPropertiesAdapter.test.ts`

**Acceptance criteria:**
- [ ] `SIM_NODE_PROPERTY_CHANGED` constant added to bus constants
- [ ] Label and description nodes have `editable=true`
- [ ] Editing label/description emits correct bus event
- [ ] All existing + 3 new tests pass

**Smoke test:**
```bash
cd browser && npx vitest run src/primitives/tree-browser/adapters/
```

---

### TASK-167: FlowDesigner subscribes to property-changed events (HAIKU)

**Deliverables:**
- Add `useEffect` in FlowDesigner to subscribe to `sim:node-property-changed`
- On event, find node in `nodes` state by ID, update field, call `setNodes`
- Support updating: `label`, `description`
- Call `pushHistory()` before updating (for undo/redo)

**Test requirements:**
- 4 new tests in `browser/src/apps/sim/components/flow-designer/__tests__/FlowDesigner.properties.test.tsx`:
  1. Emitting `sim:node-property-changed` with `label` updates node label
  2. Emitting `sim:node-property-changed` with `description` updates node description
  3. Property change pushes history (undo/redo stack)
  4. Property change emits `sim:node-selected` with updated nodeData (so properties panel refreshes)

**Files modified:**
- `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx`

**Tests created:**
- `browser/src/apps/sim/components/flow-designer/__tests__/FlowDesigner.properties.test.tsx` (new file)

**Acceptance criteria:**
- [ ] FlowDesigner subscribes to `sim:node-property-changed`
- [ ] Editing label in properties updates canvas node
- [ ] Editing description in properties updates canvas node
- [ ] History pushed before update (undo works)
- [ ] All 4 tests pass

**Smoke test:**
```bash
cd browser && npx vitest run src/apps/sim/components/flow-designer/
```

---

## Dispatch Plan

**Sequential execution** (each task depends on previous):

1. Dispatch TASK-165 (editable tree nodes) → wait for completion
2. Dispatch TASK-166 (adapter emits events) → wait for completion
3. Dispatch TASK-167 (FlowDesigner subscribes) → wait for completion

**Model:** All 3 tasks → HAIKU (small, focused, TDD-friendly)

**Estimated clock:** 45-60 minutes total (15-20 min per task)

---

## Files Inventory

### Modified (6 files)
- `browser/src/primitives/tree-browser/types.ts`
- `browser/src/primitives/tree-browser/TreeBrowser.tsx`
- `browser/src/primitives/tree-browser/TreeNodeRow.tsx`
- `browser/src/primitives/tree-browser/tree-browser.css`
- `browser/src/infrastructure/relay_bus/constants.ts`
- `browser/src/primitives/tree-browser/adapters/simPropertiesAdapter.ts`
- `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx`

### Created (2 files)
- `browser/src/primitives/tree-browser/__tests__/TreeNodeRow.test.tsx`
- `browser/src/apps/sim/components/flow-designer/__tests__/FlowDesigner.properties.test.tsx`

### Tests Extended (1 file)
- `browser/src/primitives/tree-browser/adapters/__tests__/simPropertiesAdapter.test.ts`

**Total:** 9 files touched, 12 new tests

---

## Edge Cases Identified

1. **What if user edits label to empty string?**
   → Restore previous value on blur (don't allow empty labels)

2. **What if selected node is deleted while properties panel open?**
   → Already handled by `sim:node-deselected` event

3. **What if node type changes (e.g., node → checkpoint)?**
   → Properties panel rebuilds on next `sim:node-selected` (already works)

4. **What if user spams Enter key in input?**
   → Event deduplication: only emit if value actually changed

---

## Questions for Q33NR

1. **Approve Option A (editable tree nodes)?** Or prefer Option B (dedicated PropertyPanel component)?

2. **Approve 3-task breakdown?** Or consolidate into fewer tasks?

3. **Approve label + description only for first pass?** Or include duration.value?

4. **Approve inline validation strategy?** Or prefer bus-level validation?

---

## Next Steps

Awaiting Q33NR approval to:
1. Write task files (TASK-165, TASK-166, TASK-167)
2. Return for final review
3. Dispatch bees sequentially

---

**End of Coordination Report**
