# TASK-BUG037: Palette Click-to-Place Broken

## Objective
Restore palette click-to-place functionality so clicking a palette item in TreeBrowser immediately adds that component to the canvas at a default position.

## Context

**Root cause:** CanvasApp.tsx does NOT subscribe to `palette:node-click` messages, so clicks never trigger node creation. TreeBrowserAdapter publishes `palette:node-drag-start` when a palette node is selected, but the test expects `palette:node-click`, and CanvasApp has no subscription for either.

**Current flow:**
1. ✅ TreeBrowserAdapter (line 209-218) broadcasts `palette:node-drag-start` when palette node selected
2. ✅ Palette nodes have `meta.nodeType` (Task, Queue, Start, etc.)
3. ❌ CanvasApp NEVER subscribes to this message
4. ✅ Drag-and-drop (onDrop handler line 421-439) works via physical drag events

**Expected flow (after this fix):**
1. User clicks palette item
2. TreeBrowserAdapter publishes `palette:node-click` message with `{ nodeType: 'Task' }`
3. CanvasApp subscribes to `palette:node-click`, receives message
4. CanvasApp creates node at canvas center position
5. Node appears immediately on canvas

**Design decision:** Use `palette:node-click` (not `palette:node-drag-start`) for semantic clarity. This is a click action, not a drag action.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx` (lines 179-215 for bus subscription, lines 421-439 for onDrop pattern, lines 147-149 for mapIRType)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx` (lines 208-218 for message publication)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\paletteClickToPlace.test.tsx` (existing test file — MUST PASS without modification)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\canvasTypes.ts` (line 9 for CanvasNodeType)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts` (message types registry)

## Deliverables

### 1. Add palette:node-click message type to types/messages.ts

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts`

Add interface and union member:

```typescript
export interface PaletteNodeClickData {
  nodeType: string
}
```

Add to ShellMessage union (around line 179):
```typescript
| MessageEnvelope<PaletteNodeClickData> & { type: 'palette:node-click' }
```

### 2. Update TreeBrowserAdapter to publish palette:node-click

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx`

Change line 211 from:
```typescript
type: 'palette:node-drag-start',
```

To:
```typescript
type: 'palette:node-click',
```

### 3. Add palette:node-click subscription to CanvasApp

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx`

In the `useEffect` bus subscription (lines 181-215), add a new condition BEFORE the flow data check:

```typescript
// Palette click-to-place — user clicked a palette item
if (msg.type === 'palette:node-click' && d.nodeType) {
  const nodeType = d.nodeType as string;

  // Calculate canvas center position
  const viewport = reactFlow.getViewport();
  const canvasCenter = reactFlow.screenToFlowPosition({
    x: window.innerWidth / 2,
    y: window.innerHeight / 2,
  });

  const newNode: Node = {
    id: `${nodeType.toLowerCase()}-${Date.now()}`,
    type: mapIRType(nodeType.toLowerCase()),
    position: canvasCenter,
    data: {
      label: `New ${nodeType}`,
      nodeType: mapIRType(nodeType.toLowerCase())
    } satisfies NodeData,
  };

  setNodes(nds => [...nds, newNode]);
  return;
}
```

**Placement:** Insert this block immediately after line 186 (after the `if (!msg.data) return;` guard), BEFORE the flow data check (line 189).

**Why this approach:**
- Uses existing `reactFlow.screenToFlowPosition()` API (same as onDrop handler)
- Calculates viewport center for intuitive placement
- Uses same node creation pattern as onDrop (lines 431-438)
- Uses `mapIRType()` to normalize type string (line 147-149)
- Early return prevents fallthrough to other handlers

### 4. Verify existing tests pass

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\paletteClickToPlace.test.tsx`

Run tests WITHOUT modifying this file. All tests MUST pass:
- TreeBrowser publishes palette:node-click ✓
- Does NOT publish for non-palette nodes ✓
- CanvasApp creates node with correct type ✓
- Creates nodes with unique IDs ✓
- Full integration flow ✓
- Supports all major PHASE-IR node types ✓
- Edge cases (null bus, missing nodeType, null data, wrong message type) ✓

## Test Requirements

- [ ] Write NO NEW tests (existing test file MUST pass as-is)
- [ ] Run: `cd browser && npx vitest run src/primitives/canvas/__tests__/paletteClickToPlace.test.tsx`
- [ ] All 12 tests in paletteClickToPlace.test.tsx MUST pass
- [ ] Run full canvas test suite: `cd browser && npx vitest run src/primitives/canvas/`
- [ ] No regressions in existing canvas tests
- [ ] Manual verification: Open canvas.egg.md, click palette Task node, see node appear on canvas

## Constraints

- No file over 500 lines (CanvasApp.tsx is currently 525 lines — DO NOT make it longer; if needed, refactor)
- CSS: var(--sd-*) only (not applicable to this task)
- No stubs
- TDD: Existing tests MUST pass without modification
- Do NOT break drag-and-drop functionality (onDrop handler must remain unchanged)
- Message type MUST be `palette:node-click` (not `palette:node-drag-start`)

## Acceptance Criteria

- [ ] `palette:node-click` message type added to `messages.ts` with `PaletteNodeClickData` interface
- [ ] TreeBrowserAdapter publishes `palette:node-click` (not `palette:node-drag-start`) on palette node selection
- [ ] CanvasApp subscribes to `palette:node-click` in existing bus subscription useEffect
- [ ] Clicking palette item creates node at canvas center (calculated via `reactFlow.screenToFlowPosition()`)
- [ ] Node has correct type (via `mapIRType()`), unique ID, and label
- [ ] All 12 tests in `paletteClickToPlace.test.tsx` pass WITHOUT modification to test file
- [ ] All existing canvas tests pass (no regressions)
- [ ] Drag-and-drop still works (onDrop handler unchanged)
- [ ] Multiple clicks create multiple nodes (not replace)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-BUG037-RESPONSE.md`

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

**Sonnet** — Requires careful integration with existing bus subscription logic

## Success Criteria

User clicks a palette item → node immediately appears on canvas at center position. All existing tests pass. No regressions.
