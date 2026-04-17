# TASK BUG-019: Canvas Drag Isolation

**Task ID:** 2026-03-17-TASK-BUG-019-canvas-drag-isolation
**Model:** haiku
**Priority:** P0
**Created:** 2026-03-17
**Coordinator:** Q33N

---

## Mission

Fix drag event propagation so that dragging components from the Canvas palette drops them onto the canvas surface correctly, rather than being intercepted by the Stage shell's pane drag system.

---

## Problem Analysis

**Current Behavior:**
- User drags a component from the Canvas components panel (tree-browser with palette adapter)
- The drag event bubbles up to `ShellNodeRenderer.tsx`
- Shell's `onDragOver` and `onDrop` handlers intercept the event
- Shell treats it as a pane swap/move operation instead of a canvas node drop

**Root Cause:**
1. Canvas `onDrop` handler (CanvasApp.tsx line 421) does not call `stopPropagation()`
2. Tree browser drag start (TreeNodeRow.tsx line 46-61) does not mark drags as canvas-internal
3. Shell drag handlers (ShellNodeRenderer.tsx line 146-178) do not check if drag originated from canvas-internal elements

**Required Fix:**
- Add `stopPropagation()` to canvas drag event handlers
- Add data attribute to identify canvas-internal drags
- Add defensive checks in shell drag handlers to ignore canvas-internal drags

---

## Files to Modify

### 1. Canvas App Drag Handlers
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx`

**Location:** Lines 416-439 (onDragOver and onDrop callbacks)

**Changes:**
```typescript
// Line 416-419: Add stopPropagation to onDragOver
const onDragOver = useCallback((event: React.DragEvent) => {
  event.preventDefault();
  event.stopPropagation(); // ADD THIS
  event.dataTransfer.dropEffect = 'move';
}, []);

// Line 421-439: Add stopPropagation to onDrop
const onDrop = useCallback((event: React.DragEvent) => {
  event.preventDefault();
  event.stopPropagation(); // ADD THIS
  const type = event.dataTransfer.getData('application/sd-node-type') as CanvasNodeType;
  // ... rest of handler
}, [reactFlow, setNodes]);
```

### 2. Tree Browser Drag Metadata
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\paletteAdapter.ts`

**Location:** Lines 50-61 (entryToNode function)

**Changes:**
```typescript
function entryToNode(entry: PaletteEntry): TreeNodeData {
  return {
    id: `palette-node-${entry.nodeType.toLowerCase().replace(/\s+/g, '-')}`,
    label: entry.label,
    icon: entry.icon,
    draggable: true,
    meta: {
      nodeType: entry.nodeType,
      description: entry.description,
      // ADD THESE TWO FIELDS:
      dragMimeType: 'application/sd-node-type',
      dragData: entry.nodeType,
      canvasInternal: true, // Mark as canvas-internal drag
    },
  }
}
```

### 3. Tree Browser Drag Handler
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx`

**Location:** Lines 46-61 (handleDragStart function)

**Changes:**
```typescript
const handleDragStart = (e: React.DragEvent) => {
  if (node.disabled || !node.draggable) return;

  // Set dataTransfer if node has drag metadata
  if (node.meta) {
    const dragMimeType = node.meta.dragMimeType as string | undefined;
    const dragData = node.meta.dragData;
    const canvasInternal = node.meta.canvasInternal as boolean | undefined;

    if (dragMimeType && dragData) {
      e.dataTransfer.setData(dragMimeType, JSON.stringify(dragData));
      e.dataTransfer.effectAllowed = 'copy';
    }

    // ADD THIS: Mark canvas-internal drags with data attribute
    if (canvasInternal) {
      e.dataTransfer.setData('canvas/internal', 'true');
      e.stopPropagation(); // Prevent shell from seeing this event
    }
  }

  onDragStart?.(node.id, node);
};
```

### 4. Shell Drag Handler Guards
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx`

**Location:** Lines 146-178 (onDragOver and onDrop handlers)

**Changes:**
```typescript
// Line 146-155: Add canvas-internal check to onDragOver
const onDragOver = (e: React.DragEvent) => {
  if (node.type === 'app' && (node as AppNode).chrome === false) return;

  // ADD THIS: Ignore canvas-internal drags
  if (e.dataTransfer.types.includes('canvas/internal')) {
    return; // Let canvas handle it
  }

  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  // ... rest of handler
};

// Line 157-178: Add canvas-internal check to onDrop
const onDrop = (e: React.DragEvent) => {
  if (node.type === 'app' && (node as AppNode).chrome === false) return;

  // ADD THIS: Ignore canvas-internal drags
  if (e.dataTransfer.types.includes('canvas/internal')) {
    return; // Let canvas handle it
  }

  e.preventDefault();
  // ... rest of handler
};
```

### 5. PaneChrome Drag Handle
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx`

**Location:** Lines 118-126 (Drag handle in title bar)

**Changes:**
```typescript
// Line 120-123: Ensure pane drags don't interfere with canvas
onDragStart={(e) => {
  e.dataTransfer.setData('hhs/node-id', node.id);
  e.dataTransfer.effectAllowed = 'move';
  // Do NOT set 'canvas/internal' here - this is a shell-level drag
}}
```

**No changes needed here, but verify this doesn't conflict with canvas drags.**

---

## Test Plan

### Test File Location
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\canvasDragIsolation.test.tsx`

### Test Scenarios (10 tests)

1. **Canvas drag events call stopPropagation**
   - Simulate drag over canvas surface
   - Verify `event.stopPropagation()` is called
   - Verify shell handlers do not execute

2. **Palette drag sets canvas/internal marker**
   - Simulate drag start from palette node
   - Verify `dataTransfer` contains 'canvas/internal' type
   - Verify `dataTransfer` contains 'application/sd-node-type' data

3. **Canvas drop creates node successfully**
   - Simulate drop of 'task' node onto canvas
   - Verify new node is added to canvas state
   - Verify node has correct type and position

4. **Shell ignores canvas-internal drags (onDragOver)**
   - Simulate drag over shell with 'canvas/internal' marker
   - Verify shell `onDragOver` returns early
   - Verify no drop zone indicators appear

5. **Shell ignores canvas-internal drags (onDrop)**
   - Simulate drop on shell with 'canvas/internal' marker
   - Verify shell `onDrop` returns early
   - Verify no pane swap occurs

6. **Shell accepts pane drags normally**
   - Simulate drag with 'hhs/node-id' (pane drag)
   - Verify shell `onDragOver` executes normally
   - Verify drop zones appear

7. **Palette drag includes correct node type**
   - Drag 'decision' node from palette
   - Verify dataTransfer contains correct node type
   - Verify canvas receives correct type on drop

8. **Multiple canvas drops work sequentially**
   - Drop 'start' node onto canvas
   - Drop 'task' node onto canvas
   - Drop 'end' node onto canvas
   - Verify all three nodes are present

9. **Canvas drop outside canvas surface fails gracefully**
   - Simulate drop event with invalid coordinates
   - Verify no error is thrown
   - Verify no node is created

10. **Palette drag from different categories**
    - Drag node from 'Process' category
    - Drag node from 'Flow Control' category
    - Drag node from 'Parallel' category
    - Verify all work correctly with canvas-internal marker

---

## Acceptance Criteria

- [ ] **AC1:** Dragging a palette component onto canvas creates a node (not a pane swap)
  - **Deliverable:** Canvas onDrop handler creates node and calls stopPropagation
  - **Test:** Test scenario #3

- [ ] **AC2:** Shell pane drag still works outside canvas surface
  - **Deliverable:** Shell handlers ignore 'canvas/internal' marker, accept 'hhs/node-id'
  - **Test:** Test scenario #6

- [ ] **AC3:** No event conflicts between canvas and shell drag systems
  - **Deliverable:** All drag handlers check for 'canvas/internal' marker before proceeding
  - **Test:** Test scenarios #4, #5

- [ ] **AC4:** All tests pass
  - **Deliverable:** 10 tests in canvasDragIsolation.test.tsx, all passing
  - **Test:** Run full test suite

---

## Implementation Notes

### Event Propagation Strategy
- Canvas uses `stopPropagation()` to prevent bubbling
- Tree browser marks palette drags with `canvas/internal` data type
- Shell checks for `canvas/internal` and returns early if present

### Data Transfer Types
- `canvas/internal`: marker for canvas-internal drags (no data, just type)
- `application/sd-node-type`: actual node type data for canvas drop
- `hhs/node-id`: shell pane drag identifier (do not mix with canvas drags)

### Edge Cases
- If canvas drag fails, event should not fall through to shell
- If user drags palette item outside canvas bounds, no node should be created
- If user drags pane header inside canvas EGG, shell drag should still work (chrome is outside canvas surface)

---

## Constraints (Hard Rules)

1. **No file over 500 lines** — modularize at 500, hard limit 1,000
2. **CSS only: var(--sd-*)** — no hex, rgb(), or named colors
3. **No stubs** — every function fully implemented
4. **TDD** — write tests first, then implementation

---

## Smoke Test Commands

```bash
# Test canvas drag isolation
cd browser && npx vitest run --reporter=verbose src/primitives/canvas/__tests__/canvasDragIsolation.test.tsx

# Test all canvas tests
cd browser && npx vitest run --reporter=verbose src/primitives/canvas/

# Run full test suite
cd browser && npx vitest run
```

---

## Response File Template

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-BUG-019-RESPONSE.md`

### Section 1: Executive Summary
- What was changed (2-3 sentences)
- Files modified count
- Test results summary

### Section 2: Changes Made
- List each file modified with line numbers
- Describe what was added/changed in each location
- Include code snippets for key changes

### Section 3: Test Results
- Test file created with X tests
- All tests passing (yes/no)
- Test output summary

### Section 4: Acceptance Criteria Verification
- AC1: [PASS/FAIL] — evidence
- AC2: [PASS/FAIL] — evidence
- AC3: [PASS/FAIL] — evidence
- AC4: [PASS/FAIL] — evidence

### Section 5: Edge Cases Handled
- List any edge cases discovered and handled
- Document any assumptions made

### Section 6: Manual Testing
- Describe manual testing performed (if any)
- Screenshots or observations

### Section 7: Known Limitations
- Any limitations or future improvements needed
- Technical debt incurred (if any)

### Section 8: Ready for Review
- Confirmation that all deliverables are complete
- Smoke test commands executed successfully
- Task ready for Q33N review

---

## File Paths Summary

**Files to Modify (4):**
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx`
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\paletteAdapter.ts`
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx`
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx`

**Test File to Create (1):**
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\canvasDragIsolation.test.tsx`

**Response File (1):**
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-BUG-019-RESPONSE.md`

---

## Line Counts (Pre-Implementation)

- **CanvasApp.tsx:** 525 lines (under 1,000 limit)
- **paletteAdapter.ts:** 96 lines (well under limit)
- **TreeNodeRow.tsx:** 114 lines (well under limit)
- **ShellNodeRenderer.tsx:** 316 lines (well under limit)
- **canvasDragIsolation.test.tsx:** NEW FILE (estimate 250-300 lines)

All files are within constraints.

---

## Definition of Done

- [ ] All 4 source files modified with stopPropagation and guards
- [ ] Test file created with 10 passing tests
- [ ] Smoke test commands executed successfully
- [ ] Response file created with all 8 sections
- [ ] All acceptance criteria verified
- [ ] No new TypeScript errors introduced
- [ ] No new console warnings introduced

---

**END OF TASK FILE**
