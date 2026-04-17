# BRIEFING: Wire properties panel to canvas (select → edit → update)

**Date:** 2026-03-15
**For:** Q33N
**From:** Q33NR
**Spec:** `.deia/hive/queue/2026-03-15-1558-SPEC-w2-03-properties-canvas-wire.md`
**Model Assignment:** sonnet
**Priority:** P0.95

---

## Objective

Wire properties panel to canvas via bus events:
1. Clicking a node on canvas opens properties in properties panel ✓ (ALREADY WORKS)
2. **NEW:** Editing a property in properties panel updates the canvas node in real-time
3. **NEW:** Use bus events: `node:property-changed` for property updates

---

## Current State

### What Already Works

**File:** `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx`
- Lines 111-133: Emits `sim:node-selected` and `sim:node-deselected` when nodes are clicked
- `selectedNodeProperties` tracked in state (from `useNodeEditing`)

**File:** `browser/src/primitives/tree-browser/adapters/simPropertiesAdapter.ts`
- Lines 111-119: Listens for `sim:node-selected` / `sim:node-deselected`
- Lines 94-104: Builds read-only property tree (General, Timing, Resources, Checkpoint, Group sections)
- Displays properties in tree browser (read-only)

**Tests:** `browser/src/primitives/tree-browser/adapters/__tests__/simPropertiesAdapter.test.ts`
- 7 passing tests for selection events

### What's Missing

1. **Properties are read-only.** TreeNodeData has no edit/input capabilities.
2. **No property editing UI.** Tree browser is display-only.
3. **No `node:property-changed` bus event.** Can't notify canvas when property changes.
4. **FlowDesigner doesn't listen for property updates.** Even if event fires, canvas won't update.

---

## Implementation Plan

### Option A: Editable Tree Nodes (Recommended)

Extend `TreeNodeData` to support inline editing:
- Add `editable?: boolean` field to `TreeNodeData` (types.ts)
- Add `onValueChange?: (nodeId: string, newValue: string) => void` to `TreeBrowserProps`
- Update `TreeNodeRow` to render `<input>` when `editable=true`
- simPropertiesAdapter builds editable nodes for properties (not sections)
- On value change → emit `sim:node-property-changed` → FlowDesigner updates node

### Option B: Property Panel Component (Heavier)

Create a dedicated PropertyPanel component (not in tree browser):
- New component: `browser/src/apps/sim/components/flow-designer/properties/PropertyPanelEdit.tsx`
- Renders form inputs (text, number, select) based on node kind
- Emits `sim:node-property-changed` on form field change
- FlowDesigner subscribes and updates node in real-time

---

## Recommendation

**Go with Option A** (editable tree nodes) because:
- Reuses existing tree-browser primitive
- Smaller surface area (no new component)
- Consistent with DEIA pane primitive philosophy
- Easier to test incrementally

---

## Technical Notes

### Bus Event Names

**Spec says:** `node:selected`, `node:property-changed`
**Current code uses:** `sim:node-selected`, `sim:node-deselected`

**Decision:** Keep `sim:*` namespace for consistency. The spec's event names are generic examples. Actual events should be:
- `sim:node-selected` (already exists)
- `sim:node-deselected` (already exists)
- `sim:node-property-changed` (NEW)

### Property Update Flow

```
User edits property in tree browser
  → TreeBrowser calls onValueChange(nodeId, newValue)
  → simPropertiesAdapter parses nodeId (e.g., "sim-prop-label")
  → Adapter emits: { type: 'sim:node-property-changed', data: { nodeId, field, value } }
  → FlowDesigner subscribes (new useEffect block)
  → FlowDesigner updates node in setNodes()
  → Canvas re-renders with updated node
```

### Which Properties Are Editable?

**Editable:**
- Label (General section)
- Description (General section)
- Duration value/min/max (Timing section)
- Resource capacity (Resources section)
- Checkpoint condition/trueLabel/falseLabel (Checkpoint section)

**NOT editable:**
- Kind (immutable after creation)
- Distribution type (requires dropdown, defer to future task)
- Group childNodeIds (managed by grouping operations, not direct edit)

---

## Files to Modify

1. `browser/src/primitives/tree-browser/types.ts` — add `editable`, `value`, `onValueChange` to `TreeNodeData`
2. `browser/src/primitives/tree-browser/TreeNodeRow.tsx` — render `<input>` when `editable=true`
3. `browser/src/primitives/tree-browser/TreeBrowser.tsx` — forward `onValueChange` from props to rows
4. `browser/src/primitives/tree-browser/adapters/simPropertiesAdapter.ts` — mark properties editable, handle value changes, emit bus event
5. `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx` — subscribe to `sim:node-property-changed`, update nodes
6. **Tests (TDD):**
   - `browser/src/primitives/tree-browser/__tests__/TreeNodeRow.test.tsx` (new) — test editable input rendering
   - `browser/src/primitives/tree-browser/adapters/__tests__/simPropertiesAdapter.test.ts` (extend) — test property change events
   - `browser/src/apps/sim/components/flow-designer/__tests__/FlowDesigner.properties.test.tsx` (new) — test canvas updates from property changes

---

## Acceptance Criteria (from spec)

- [ ] Clicking canvas node opens properties panel ✓ (already works)
- [ ] Editing property updates canvas node in real-time
- [ ] Bus events connected correctly (`sim:node-property-changed` emitted and handled)
- [ ] Tests written and passing (min 3 new tests)

---

## Constraints (from spec)

- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: `var(--sd-*)` only (applies to any new input styling)
- Heartbeat: POST to `http://localhost:8420/build/heartbeat` every 3 minutes
- File claims: Use build monitor API before modifying files

---

## Smoke Test

```bash
cd browser && npx vitest run src/apps/sim/
```

No new test failures.

---

## Questions for Q33N

1. **Do you agree with Option A (editable tree nodes)?** If not, justify Option B.
2. **Which properties should be editable in the first pass?** Recommend: label, description, duration value (defer dropdowns/enums).
3. **How should validation work?** E.g., duration must be a number. Emit error event? Show inline error? (Recommend: inline error state on input, don't emit invalid values.)

---

## Next Steps

Q33N: Read this briefing, explore the files listed, write task files for the implementation, return for Q33NR approval before dispatching bees.

---

**End of Briefing**
