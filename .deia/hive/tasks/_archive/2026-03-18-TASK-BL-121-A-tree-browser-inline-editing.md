# TASK-BL-121-A: Add Inline Editing UI to Tree Browser

## Objective

Extend TreeBrowser to support inline property editing by adding editable input controls that detect the property type and render appropriate UI (text, number, dropdown).

## Context

The properties adapter (propertiesAdapter.ts) already publishes `properties:value-changed` events via `updateProperty()`, but the TreeBrowser renders all properties as read-only labels. This task adds the UI layer to make properties editable.

The TreeNodeRow component needs to detect when a node has editable metadata, render an appropriate input control based on value type, and call the adapter's `updateProperty()` method on save.

**Editing flow:**
1. User clicks on a property row that has `meta: { value: X, editable: true }`
2. TreeNodeRow switches from label display to inline edit mode
3. User edits the value
4. On blur or Enter → save via `adapter.updateProperty(nodeId, field, value)`
5. On Escape → cancel edit and revert to original value

**Input type inference:**
- `typeof value === 'string'` → text input
- `typeof value === 'number'` → number input
- Array/object values → JSON text input (for now)

**Properties that should be editable:**
- `name` (string)
- `timing.distribution` (string)
- `timing.params` (object, JSON edit)
- `operator.type` (string)
- `operator.count` (number)
- `operator.skills` (array, JSON edit)

**Properties that should be read-only:**
- `id` (never editable)
- `type` (read-only)

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeBrowser.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\propertiesAdapter.ts`

## Deliverables

### 1. Update TreeNodeData type to support editable metadata

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\types.ts`

- [ ] Add optional `editable: boolean` flag to `TreeNodeData.meta` type hint (keep meta as `Record<string, unknown>` but document the convention)
- [ ] Add comment documenting the `meta.editable` and `meta.value` pattern for inline editing

### 2. Add inline editing to TreeNodeRow

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx`

- [ ] Add state: `isEditing: boolean`, `editValue: string`
- [ ] Detect editable nodes: check `node.meta?.editable === true`
- [ ] On click (if editable): enter edit mode, focus input
- [ ] Render input control based on value type:
  - String → `<input type="text">`
  - Number → `<input type="number">`
  - Object/Array → `<input type="text">` (JSON stringified)
- [ ] On blur or Enter: save via callback prop `onPropertyChange(nodeId, field, value)`
- [ ] On Escape: cancel edit, revert to original value
- [ ] CSS classes for edit mode: `.tree-node-row.editing`, `.tree-node-input`
- [ ] CSS using `var(--sd-*)` only, no hardcoded colors

**Props addition:**
```typescript
export interface TreeNodeRowProps {
  // ... existing props
  onPropertyChange?: (nodeId: string, field: string, value: any) => void;
}
```

**State additions:**
```typescript
const [isEditing, setIsEditing] = useState(false);
const [editValue, setEditValue] = useState<string>('');
```

**Edit mode detection:**
```typescript
const isEditable = node.meta?.editable === true && node.meta?.value !== undefined;
const displayValue = node.meta?.value;
```

**Keyboard handlers:**
- Enter → save and exit edit mode
- Escape → cancel and exit edit mode
- Blur → save and exit edit mode

### 3. Update TreeBrowser to pass onPropertyChange callback

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeBrowser.tsx`

- [ ] Accept `onPropertyChange?: (nodeId: string, field: string, value: any) => void` prop
- [ ] Pass it through to all TreeNodeRow instances
- [ ] Update TreeBrowserProps interface

### 4. Update propertiesAdapter to mark properties as editable

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\propertiesAdapter.ts`

- [ ] In `buildGeneralSection()`: mark `name` as editable (`meta: { value: node.name, editable: true, field: 'name' }`)
- [ ] In `buildGeneralSection()`: mark `id` and `type` as read-only (`meta: { value: node.id, editable: false }`)
- [ ] In `buildTimingSection()`: mark `distribution` and `params` as editable
- [ ] In `buildOperatorSection()`: mark `type`, `count`, `skills` as editable
- [ ] Add `field` to meta so TreeNodeRow knows which field path to publish (e.g., `"name"`, `"config.timing.distribution"`)

### 5. Wire adapter.updateProperty to TreeBrowser

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeBrowser.tsx` (if using adapter pattern)

OR create a wrapper component that:
- [ ] Receives `adapter` prop
- [ ] Passes `onPropertyChange={(nodeId, field, value) => adapter.updateProperty(nodeId, field, value)}` to TreeBrowser

### 6. CSS for inline editing

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\tree-browser.css`

- [ ] Add styles for `.tree-node-row.editing`
- [ ] Add styles for `.tree-node-input` (text/number inputs)
- [ ] Use `var(--sd-input-bg)`, `var(--sd-input-border)`, `var(--sd-text)` only
- [ ] Focus state: `var(--sd-focus-ring)`
- [ ] No hardcoded colors

Example CSS:
```css
.tree-node-row.editing {
  background: var(--sd-surface-hover);
}

.tree-node-input {
  background: var(--sd-input-bg);
  border: 1px solid var(--sd-input-border);
  color: var(--sd-text);
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 12px;
  font-family: inherit;
  width: 100%;
  max-width: 200px;
}

.tree-node-input:focus {
  outline: none;
  border-color: var(--sd-focus-ring);
}
```

## Test Requirements

**All tests MUST be written FIRST (TDD).**

### Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\TreeNodeRow.test.tsx`

- [ ] Test: read-only property (editable: false) renders as label
- [ ] Test: editable string property renders as text input on click
- [ ] Test: editable number property renders as number input on click
- [ ] Test: editing string property + blur saves value
- [ ] Test: editing number property + Enter saves value
- [ ] Test: editing property + Escape cancels and reverts
- [ ] Test: onPropertyChange callback receives correct nodeId, field, value
- [ ] Test: empty value does not save
- [ ] Test: JSON parse error on object/array edit shows validation error (optional stretch goal)
- [ ] All tests pass

### Run tests with:

```bash
cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser" && npx vitest run --reporter=verbose src/primitives/tree-browser/__tests__/TreeNodeRow.test.tsx
```

### Regression test:

```bash
cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser" && npx vitest run --reporter=verbose src/primitives/tree-browser/
```

## Constraints

- **No file over 500 lines.** If TreeNodeRow grows beyond 500 lines, extract edit logic into a separate component (e.g., `InlinePropertyEdit.tsx`).
- **CSS: `var(--sd-*)` only.** No hex, no rgb(), no named colors.
- **No stubs.** All functionality fully implemented.
- **TDD.** Tests written FIRST, then implementation.
- **No git operations** without Q88N approval.

## Acceptance Criteria

- [ ] Editable properties show text/number input on click
- [ ] Blur saves the value
- [ ] Enter saves the value
- [ ] Escape cancels the edit
- [ ] onPropertyChange callback is invoked with correct parameters
- [ ] Read-only properties do not become editable
- [ ] All CSS uses `var(--sd-*)` variables
- [ ] No file exceeds 500 lines
- [ ] At least 9 tests pass (one per scenario above)
- [ ] No regressions on existing tree-browser tests

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-TASK-BL-121-A-RESPONSE.md`

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
