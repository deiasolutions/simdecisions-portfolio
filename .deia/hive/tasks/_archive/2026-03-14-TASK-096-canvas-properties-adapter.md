# TASK-096: Build Canvas Properties Adapter

## Objective
Create a tree-browser adapter that displays properties of the currently selected canvas node in an accordion-style panel.

## Context
When a user clicks a node on the canvas, the canvas publishes `canvas:node-selected` with the IRNode payload. The properties adapter listens for this event and displays the node's properties in the right sidebar.

The old repo had `PropertiesPanelContent.tsx` (~600 lines) with 6 accordion sections. We simplify to 4 sections for ShiftCenter.

## Dependencies
- **TASK-092 must be complete** (provides `browser/src/types/ir.ts`)
- **TASK-093 should be complete** (publishes `canvas:node-selected`)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\channelsAdapter.ts` (pattern reference)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\types\ir.ts` (from TASK-092)

## Deliverables
- [ ] Create `browser/src/primitives/tree-browser/adapters/propertiesAdapter.ts` (~200 lines)
  - Export `createPropertiesAdapter()` following channelsAdapter pattern
  - Listen for `canvas:node-selected` bus event
  - When a node is selected, return TreeNodeData[] as 4 accordion sections:
    - **General**: id, type, label
    - **Timing**: distribution, params (from TimingConfig)
    - **Operator**: type, count, skills (from OperatorConfig)
    - **Connections**: inbound edges, outbound edges (edge count + labels)
  - When no node selected, return empty state with message "Select a node on the canvas"
  - Publish `properties:value-changed` when user edits a property (payload: { nodeId, field, value })
- [ ] Create `browser/src/primitives/tree-browser/adapters/__tests__/propertiesAdapter.test.ts` — 7+ tests:
  - Empty state when no node selected
  - Listens for canvas:node-selected
  - Renders 4 accordion sections for selected node
  - General section shows id, type, label
  - Timing section shows distribution + params
  - Operator section shows type + count
  - Publishes properties:value-changed on edit

## Constraints
- No file over 500 lines
- CSS: `var(--sd-*)` only
- Follow the channelsAdapter pattern
- Properties are READ-ONLY for now — the edit publish is wired but no backend mutation

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260314-TASK-096-RESPONSE.md`

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

## Model Assignment
sonnet
