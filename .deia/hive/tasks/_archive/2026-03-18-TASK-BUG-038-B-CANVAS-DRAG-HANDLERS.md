# TASK-BUG-038-B: Fix CanvasApp Drag Handlers

## Objective

Add stopPropagation() to CanvasApp drag handlers and fix onDrop to parse JSON dragData from TreeNodeRow.

## Context

**Problem:** Dragging palette items to canvas doesn't work. Two issues in CanvasApp.tsx:

1. **Missing stopPropagation():** BUG-019 claimed to add these calls, but they were never committed. Without them, drag events bubble to shell's pane swap system.
2. **Wrong data format:** CanvasApp reads plain string from dataTransfer, but TreeNodeRow sets JSON via `JSON.stringify(dragData)`.

**Current code (lines 416-439):**
```typescript
const onDragOver = useCallback((event: React.DragEvent) => {
  event.preventDefault();  // ❌ No stopPropagation
  event.dataTransfer.dropEffect = 'move';
}, []);

const onDrop = useCallback((event: React.DragEvent) => {
  event.preventDefault();  // ❌ No stopPropagation
  const type = event.dataTransfer.getData('application/sd-node-type') as CanvasNodeType;
  // ❌ Assumes plain string, but TreeNodeRow sets JSON.stringify({ nodeType })
  if (!type || !reactFlow) return;
  // ... rest of handler
```

**Expected flow after fix:**
1. TreeNodeRow calls `setData('application/sd-node-type', JSON.stringify({ nodeType: 'Task' }))`
2. CanvasApp onDrop calls `getData('application/sd-node-type')` → returns `'{"nodeType":"Task"}'`
3. CanvasApp parses JSON → `{ nodeType: 'Task' }`
4. CanvasApp extracts `nodeType` field
5. Node created on canvas
6. stopPropagation prevents shell from seeing event

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx`
   - Read lines 414-440 (drag handlers)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx`
   - Read lines 95-110 (handleDragStart) — shows it sets JSON.stringify(dragData)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\canvas.dragDrop.test.tsx`
   - Existing tests (5 tests) — these tests ASSUME stopPropagation exists but code doesn't have it

## Deliverables

- [ ] **D1:** Write tests FIRST (TDD) — modify existing test file: `browser/src/primitives/canvas/__tests__/canvas.dragDrop.test.tsx`
  - Add test: onDrop correctly parses JSON dragData (`'{"nodeType":"Task"}'` → `'Task'`)
  - Add test: onDrop handles plain string fallback (for backwards compatibility)
  - Add test: onDrop returns early if JSON parse fails or no nodeType
  - Verify existing 5 tests still pass (they test stopPropagation, which we'll add)
  - Minimum 8 tests total (5 existing + 3 new)

- [ ] **D2:** Modify `CanvasApp.tsx` onDragOver handler (line ~416-419):
  ```typescript
  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.stopPropagation(); // ← ADD THIS — prevents shell pane drag system
    event.dataTransfer.dropEffect = 'move';
  }, []);
  ```

- [ ] **D3:** Modify `CanvasApp.tsx` onDrop handler (line ~421-439):
  ```typescript
  const onDrop = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.stopPropagation(); // ← ADD THIS — prevents shell pane drag system

    const rawData = event.dataTransfer.getData('application/sd-node-type');
    if (!rawData || !reactFlow) return;

    let nodeType: CanvasNodeType;
    try {
      // TreeNodeRow sets JSON.stringify({ nodeType: 'Task' })
      const parsed = JSON.parse(rawData);
      nodeType = parsed.nodeType;
    } catch {
      // Fallback: treat rawData as plain string (backwards compatibility)
      nodeType = rawData as CanvasNodeType;
    }

    if (!nodeType) return;

    const position = reactFlow.screenToFlowPosition({
      x: event.clientX,
      y: event.clientY,
    });

    const newNode: Node = {
      id: `${nodeType}-${Date.now()}`,
      type: mapIRType(nodeType),
      position,
      data: { label: `New ${nodeType}`, nodeType: mapIRType(nodeType) } satisfies NodeData,
    };

    setNodes(nds => [...nds, newNode]);
  }, [reactFlow, setNodes]);
  ```

- [ ] **D4:** All tests pass (existing 5 + new 3)

## Test Requirements

- [ ] **TDD:** Write new tests FIRST, then implementation
- [ ] **Test file:** `browser/src/primitives/canvas/__tests__/canvas.dragDrop.test.tsx` (modify existing)
- [ ] **New tests (minimum 3):**
  1. onDrop parses JSON dragData correctly: `'{"nodeType":"Task"}'` → creates Task node
  2. onDrop fallback to plain string: `'Decision'` → creates Decision node
  3. onDrop handles parse errors gracefully: invalid JSON → no node created
- [ ] **Existing tests (5):** All must still pass (they already test stopPropagation behavior)
- [ ] **Edge cases:**
  - Empty string from dataTransfer → no node created
  - Valid JSON but missing nodeType field → no node created
  - Valid nodeType but no reactFlow → no node created
- [ ] **Run:** `cd browser && npx vitest run src/primitives/canvas/__tests__/canvas.dragDrop.test.tsx`

## Constraints

- No file over 500 lines (CanvasApp.tsx is ~600 lines — do NOT add, only modify existing lines)
- CSS: var(--sd-*) only (N/A — no CSS changes)
- No stubs — fully implement all changes
- TDD — tests first, then implementation

## Acceptance Criteria

- [ ] **AC1:** onDragOver calls `event.stopPropagation()` (line ~418)
- [ ] **AC2:** onDrop calls `event.stopPropagation()` (line ~423)
- [ ] **AC3:** onDrop parses JSON dragData via `JSON.parse(rawData)`
- [ ] **AC4:** onDrop extracts `nodeType` from parsed object
- [ ] **AC5:** onDrop has fallback to treat rawData as plain string (backwards compatibility)
- [ ] **AC6:** All 8 tests pass (5 existing + 3 new)
- [ ] **AC7:** No TypeScript errors in CanvasApp.tsx
- [ ] **AC8:** Drag events do NOT bubble to shell pane drag system (verified by existing tests)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260318-TASK-BUG-038-B-RESPONSE.md`

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

## Notes

- This task is PART 2 of 3 for BUG-038
- PART 1 (TASK-BUG-038-A) fixes paletteAdapter drag metadata
- PART 3 (TASK-BUG-038-C) will write integration tests for full drag flow
- BUG-019 response claimed to add stopPropagation() but those changes were NEVER COMMITTED — you must add them now
- The existing test file (canvas.dragDrop.test.tsx) has 5 tests that ASSUME stopPropagation exists — they will pass once you add it
- Do NOT modify TreeNodeRow or paletteAdapter in this task
