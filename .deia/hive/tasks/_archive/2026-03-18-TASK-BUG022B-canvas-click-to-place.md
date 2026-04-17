# TASK-BUG022B: Implement Canvas Palette Click-to-Place

## Objective
Wire the palette adapter so clicking a component in the components panel places it on the canvas at the viewport center.

## Context
This is a **re-queue** because previous attempts wrote tests but never modified the source code. The tests already exist and define the expected behavior:
- TreeBrowser publishes `palette:node-click` when a palette node (node with `meta.nodeType`) is clicked
- CanvasApp subscribes to `palette:node-click` and creates a new node on the canvas

**Architecture:**
- TreeBrowser already has `onSelect` handler that fires when a row is clicked
- CanvasApp already subscribes to bus messages via `bus.subscribe(nodeId, callback)`
- MessageBus is already set up and working (tested in BUG-024)
- The EGG config shows palette pane has nodeId `canvas-palette` and canvas has `canvas-editor`

**What's Missing:**
1. TreeBrowser's `onSelect` handler does NOT currently check if the node is a palette node and emit the bus event
2. CanvasApp does NOT currently subscribe to `palette:node-click` events

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeBrowser.tsx` (onSelect handler location)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx` (calls onSelect)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\types.ts` (TreeBrowserProps interface)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx` (bus subscription location)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\paletteClickToPlace.test.tsx` (10 tests — make these pass)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md` (EGG config showing pane IDs)

## Deliverables

### Part 1: TreeBrowser publishes palette:node-click
- [ ] Add `bus?: MessageBus | null` to TreeBrowserProps interface in `types.ts`
- [ ] Pass bus prop through TreeBrowser component to handleSelect function
- [ ] In TreeBrowser's handleSelect (or TreeNodeRow click handler), detect if node has `meta.nodeType`
- [ ] If nodeType exists, publish `palette:node-click` event via `bus.send()` with structure:
  ```ts
  {
    type: 'palette:node-click',
    sourcePane: '<paneId>',  // from props or context
    target: '*',
    nonce: `${Date.now()}-${Math.random()}`,
    timestamp: new Date().toISOString(),
    data: { nodeType: node.meta.nodeType }
  }
  ```
- [ ] Still call the original onSelect handler (don't break existing behavior)

### Part 2: CanvasApp subscribes to palette:node-click
- [ ] In CanvasApp's bus subscription useEffect, add a subscription to `'palette:node-click'`
- [ ] When received, extract `nodeType` from `msg.data.nodeType`
- [ ] Create a new node with:
  - Unique ID: `node-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
  - Type: `nodeType.toLowerCase()`
  - Position: viewport center (estimate x: 400, y: 300 or use reactFlow viewport if available)
  - Data: `{ label: nodeType, nodeType: nodeType.toLowerCase() }`
- [ ] Add node to canvas via `setNodes(prev => [...prev, newNode])`

### Part 3: Wire bus prop through component tree
- [ ] Identify where TreeBrowser is instantiated for palette (check EGG loader or pane registry)
- [ ] Pass bus prop to TreeBrowser when adapter is 'palette'
- [ ] If bus is not available at that level, document in response file (may need follow-up task)

## Test Requirements
- [ ] All paletteClickToPlace tests pass (10 tests in `paletteClickToPlace.test.tsx`)
- [ ] No regressions in TreeNodeRow icon tests (15 tests in `TreeNodeRow.icon.test.tsx`)
- [ ] No regressions in TreeNodeRow palette integration tests (`TreeNodeRow.palette-icons.integration.test.tsx`)
- [ ] Manual smoke test: clicking a palette item creates a node on canvas (if possible)

## Acceptance Criteria
- [ ] Click a palette item → component appears on canvas at viewport center
- [ ] All 10 paletteClickToPlace tests pass
- [ ] All 15 TreeNodeRow icon tests pass
- [ ] No new test failures in canvas/ or tree-browser/
- [ ] Bus event structure matches test expectations exactly

## Constraints
- **No file over 500 lines** (check TreeBrowser.tsx and CanvasApp.tsx after changes)
- **CSS: var(--sd-*) only** (no CSS changes expected, but verify)
- **No stubs** — full implementation required
- **Do NOT modify messageBus.ts core** (only add listeners/publishers in TreeBrowser and CanvasApp)
- **TDD:** Tests already exist — implement code to pass them
- **Type safety:** Ensure TypeScript compiles with no errors

## Smoke Test Commands
```bash
# Run palette click-to-place tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run src/primitives/canvas/__tests__/paletteClickToPlace.test.tsx

# Verify no regressions in icon tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run src/primitives/tree-browser/__tests__\TreeNodeRow.icon.test.tsx

# Verify no regressions in palette integration tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run src/primitives/tree-browser/__tests__\TreeNodeRow.palette-icons.integration.test.tsx

# Full tree-browser test suite
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run src/primitives/tree-browser/

# Full canvas test suite
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run src/primitives/canvas/
```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-TASK-BUG022B-RESPONSE.md`

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
**Sonnet** (as specified in spec)

## Priority
**P0** (blocking canvas usability)

## Implementation Notes

### Key Files and Line Numbers
Based on reading the codebase:
- **TreeBrowser.tsx:111** — `onSelect(currentNode.id, currentNode)` on Enter key
- **TreeBrowser.tsx:171** — `onSelect={onSelect}` passed to TreeNodeRow
- **TreeNodeRow.tsx:86** — `onSelect(node.id, node)` on click
- **CanvasApp.tsx:181-214** — Bus subscription useEffect block

### Recommended Approach
1. Start with TreeBrowser — add bus prop, detect palette nodes, publish event
2. Then CanvasApp — subscribe to palette:node-click, create nodes
3. Find where TreeBrowser is instantiated for palette and wire bus prop
4. Run tests incrementally as you implement each part

### Edge Cases (from tests)
- Handle null/undefined bus gracefully (early return)
- Handle missing nodeType in message data (guard clause)
- Handle null data in message (guard clause)
- Ensure message type is exactly 'palette:node-click' (subscription filter)
- Generate unique IDs for each node (timestamp + random)
- Support all node types: Task, Decision, Start, End, Checkpoint

---

**REMEMBER:** This is a re-queue because previous bees only wrote tests. You must modify BOTH TreeBrowser/TreeNodeRow AND CanvasApp source files. No more tests. Actual implementation code only.
