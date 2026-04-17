# BRIEFING: BUG-019 — Canvas Drag Isolation

**To:** Q33N (Queen Coordinator)
**From:** Q88NR (Regent)
**Date:** 2026-03-17
**Spec:** BUG-019
**Priority:** P0

---

## Mission

Fix canvas component drag behavior so that dragging components from the Canvas palette drops them onto the canvas surface correctly, rather than being intercepted by the Stage shell's pane drag system.

---

## Context

The Canvas primitive has a components panel (palette) that users drag components from onto the canvas drawing surface. Currently, the Stage shell is intercepting these drag events and treating them as pane swap/move operations instead of allowing the canvas to handle them internally.

This is a **drag event propagation issue**. The canvas needs to capture and stop propagation of its internal drag events before they bubble up to the shell's drag handlers.

---

## Files to Investigate First

1. `browser/src/primitives/canvas/` — entire canvas implementation
2. `browser/src/shell/components/ShellNodeRenderer.tsx` — shell drag event handlers
3. `browser/src/shell/dragDropUtils.ts` — shell drag/drop utilities
4. `eggs/canvas.egg.md` — canvas EGG layout definition

---

## Deliverables Required

### 1. Fix Canvas Internal Drag Propagation
- Canvas component must call `event.stopPropagation()` on drag events that are internal to the canvas (palette → canvas surface)
- Identify where canvas handles `onDragStart`, `onDrag`, `onDragEnd` for palette components
- Ensure these events do NOT bubble to parent shell components

### 2. Shell Drag Handler Guards
- Shell drag handlers in `ShellNodeRenderer.tsx` or `dragDropUtils.ts` should check if drag originated from canvas-internal elements
- Add defensive checks to ignore canvas-internal drags
- Possible approaches:
  - Check `event.target` or `event.currentTarget` attributes
  - Use a data attribute like `data-canvas-internal-drag="true"`
  - Check if drag originates from within `.canvas-container` or similar

### 3. Verify Palette-to-Canvas Drop Works
- Components dragged from palette should successfully drop onto canvas and create nodes
- No pane swap dialogs should appear
- Canvas state should update with new node

### 4. Preserve Shell Drag for Other Panes
- Shell pane drag/drop must continue to work normally for non-canvas panes
- Only canvas-internal drags should be isolated
- Test that dragging other pane headers still works

### 5. Tests
Create tests in `browser/src/primitives/canvas/__tests__/` covering:
- Canvas palette drag starts
- Canvas surface drop handling
- `stopPropagation()` is called on internal drag events
- Shell drag handlers do not intercept canvas drags
- Minimum: 8-10 tests covering isolation behavior

---

## Acceptance Criteria (from Spec)

- [ ] Dragging palette component onto canvas creates a node, not a pane swap
- [ ] Shell pane drag still works outside canvas surface
- [ ] No event conflicts between canvas and shell drag systems
- [ ] All tests pass

---

## Smoke Test Commands

After implementation:

```bash
cd browser && npx vitest run --reporter=verbose src/primitives/canvas/
cd browser && npx vitest run
```

---

## Constraints (Hard Rules)

- **No file over 500 lines** (modularize at 500, hard limit 1,000)
- **CSS only: var(--sd-*)** — no hex, rgb(), or named colors
- **No stubs** — every function fully implemented
- **TDD** — write tests first, then implementation

---

## Task File Requirements

Your task file(s) must include:

1. **Absolute file paths** (Windows format: `C:\Users\davee\OneDrive\...`)
2. **Test specifications** — how many tests, which scenarios, which files
3. **Explicit deliverables** for each acceptance criterion
4. **Response file template** — 8-section format

---

## Model Assignment

**haiku** — this is a focused bug fix with clear scope

---

## Expected Output

- Task file(s) in `.deia/hive/tasks/`
- Task ID: `2026-03-17-TASK-BUG-019-canvas-drag-isolation`
- All deliverables clearly mapped to acceptance criteria
- Test plan with specific scenarios

---

## Next Step

Q33N: Please write the task file(s) and submit for approval.

---

**Q88NR**
