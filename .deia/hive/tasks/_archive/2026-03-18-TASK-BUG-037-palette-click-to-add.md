# TASK-BUG-037: Palette Click-to-Add Broken

## Objective

Fix the palette click-to-place functionality so clicking on a component in the palette tree-view adds that component to the canvas at the viewport center.

## Context

**Root Cause:**
The architecture is partially wired. `treeBrowserAdapter.tsx` broadcasts `palette:node-drag-start` when a palette node is selected (line 211), but:

1. CanvasApp does NOT subscribe to this message type
2. The test file expects `palette:node-click` (line 37, 311, 322)
3. There's a naming mismatch: implementation sends `palette:node-drag-start`, tests expect `palette:node-click`
4. CanvasApp has drag-and-drop handlers but no click-to-place subscription

**What Broke:**
BUG-022 fixed icon rendering and drag metadata but claimed "Click handling already wired" — this was incorrect. TreeBrowserAdapter broadcasts the message, but CanvasApp never listens.

**Node Creation Pattern:**
The existing `onDrop` handler (lines 421-439) shows the correct pattern:
- Get node type from data
- Calculate position using `reactFlow.screenToFlowPosition()`
- Create node with `mapIRType()` for type mapping
- Add to canvas via `setNodes(nds => [...nds, newNode])`

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx` (lines 179-215 for bus subscription, lines 421-439 for onDrop pattern, line 147-149 for mapIRType)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx` (lines 208-218 for message broadcast)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\paletteClickToPlace.test.tsx` (existing test file, shows expected behavior)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts` (for adding new message type)

## Deliverables

### 1. Update message type in treeBrowserAdapter.tsx
- [ ] Change line 211 from `palette:node-drag-start` to `palette:node-click`
- [ ] Keep data payload the same: `{ nodeType: node.meta.nodeType }`

### 2. Add palette:node-click type to messages.ts
- [ ] Add `PaletteNodeClickData` interface with `{ nodeType: string }`
- [ ] Add to `ShellMessage` union type

### 3. Add click-to-place handler to CanvasApp.tsx
- [ ] In existing bus subscription (lines 181-215), add handler for `palette:node-click`
- [ ] Extract `nodeType` from `msg.data.nodeType`
- [ ] Calculate center position using `reactFlow.getViewport()` to get canvas center
- [ ] Create node using same pattern as `onDrop` handler:
  - ID: `${type}-${Date.now()}`
  - Type: `mapIRType(nodeType.toLowerCase())`
  - Position: canvas center (not mouse position)
  - Data: `{ label: \`New ${nodeType}\`, nodeType: mapIRType(nodeType.toLowerCase()) }`
- [ ] Add to canvas: `setNodes(nds => [...nds, newNode])`
- [ ] Guard: return early if `!msg.data || !msg.data.nodeType`

### 4. Verify existing tests pass
- [ ] Run `cd browser && npx vitest run src/primitives/canvas/__tests__/paletteClickToPlace.test.tsx`
- [ ] All existing tests should pass without modification

## Test Requirements

### Tests Written FIRST (TDD)
The test file already exists with comprehensive coverage:
- [ ] `paletteClickToPlace.test.tsx` — 13 tests covering:
  - TreeBrowser publishes `palette:node-click` with nodeType
  - Non-palette nodes don't publish
  - CanvasApp receives and creates node
  - Unique IDs for multiple clicks
  - Full integration flow
  - All PHASE-IR node types (Task, Decision, Start, End, Checkpoint)
  - Edge cases: null bus, missing nodeType, null data, wrong message type

### All Tests Pass
- [ ] All 13 existing tests in `paletteClickToPlace.test.tsx` must pass
- [ ] No regressions in other canvas tests
- [ ] Run full canvas test suite: `cd browser && npx vitest run src/primitives/canvas`

### Edge Cases
- [ ] Missing nodeType in message → no node created
- [ ] Null data in message → no crash
- [ ] Bus is null → no crash (early return)
- [ ] Wrong message type → subscription doesn't match
- [ ] Multiple clicks → multiple nodes with unique IDs

## Constraints

- **No file over 500 lines** — CanvasApp.tsx is currently 525 lines (grandfathered, don't make it larger)
- **CSS: var(--sd-*) only** — Not applicable (no CSS changes)
- **No stubs** — All functions fully implemented
- **TDD** — Tests already exist, implementation must pass them

## Acceptance Criteria

- [ ] Clicking palette Task node creates Task node at canvas center
- [ ] Clicking palette Queue node creates Queue node at canvas center
- [ ] Clicking palette Start node creates Start node at canvas center
- [ ] Multiple clicks create multiple nodes (not replace)
- [ ] Existing drag-and-drop functionality still works (don't break `onDrop`)
- [ ] All 13 tests in `paletteClickToPlace.test.tsx` pass
- [ ] No regressions in other canvas tests
- [ ] No hardcoded colors introduced
- [ ] No files exceed 500 lines

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260318-TASK-BUG-037-RESPONSE.md`

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

**Sonnet** — This requires careful integration with existing bus subscription logic and understanding of ReactFlow position calculation.
