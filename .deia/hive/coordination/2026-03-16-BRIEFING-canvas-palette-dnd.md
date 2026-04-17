# BRIEFING: Wire canvas palette drag-and-drop node creation

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-16
**Priority:** P1.25
**Model Assignment:** Haiku

---

## Objective

Enable drag-and-drop node creation: user drags a node type from the tree-browser palette, drops on the canvas, and a new node is created at the drop position. Uses HTML5 drag/drop API.

---

## Context from Spec

**Spec ID:** 2026-03-16-1042-SPEC-w2-09-canvas-palette-dnd
**Queue file:** `.deia/hive/queue/2026-03-16-1042-SPEC-w2-09-canvas-palette-dnd.md`

The spec requires:
- Palette shows node types in tree-browser
- Drag from palette to canvas works
- Node created at drop position
- Tests written and passing
- TDD approach
- No stubs
- CSS: var(--sd-*) only
- File claims via build monitor (http://localhost:8420)
- Heartbeats every 3 minutes

---

## Relevant File Paths

### Canvas/Flow Designer
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\`
- Look for existing drag-and-drop handlers
- Look for node creation logic

### Tree Browser Palette
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\`
- Check if palette adapter exists
- Check how tree items are structured

### Recent related work
- TASK-174, TASK-175, TASK-176 (DES backend wiring, simulation wiring)
- Check `.deia/hive/responses/20260316-TASK-174-RESPONSE.md` and similar for context

---

## Constraints

1. Max 500 lines per file
2. TDD: tests first, then implementation
3. No stubs (fully implemented functions only)
4. CSS: var(--sd-*) only
5. File claims required before modifying files (build monitor at http://localhost:8420)
6. Heartbeats every 3 minutes during work
7. Smoke test: `cd browser && npx vitest run src/apps/sim/` — no new failures

---

## Your Task

1. **Read the codebase** to understand:
   - How the flow designer canvas currently creates nodes
   - Whether tree-browser has palette adapter or needs one
   - What node types exist and how they're defined
   - Existing drag/drop patterns in the codebase

2. **Write task file(s)** for bee(s):
   - Break down into testable units
   - Include file paths (absolute)
   - Include test requirements (specific scenarios)
   - Include file claim instructions
   - Include heartbeat instructions

3. **Return to Q33NR for review** — do NOT dispatch bees yet

---

## Expected Deliverables

Task files written to `.deia/hive/tasks/` covering:
- [ ] Tree-browser palette adapter (if needed)
- [ ] Canvas drag/drop handlers (dragOver, drop)
- [ ] Node creation from drop event
- [ ] Tests for drag/drop flow
- [ ] Integration test for end-to-end flow

---

## Notes

- The spec mentions "palette shows node types in tree-browser" — verify if this exists or needs to be built
- HTML5 drag/drop API: draggable=true, onDragStart, onDragOver, onDrop
- Drop position: calculate canvas coordinates from drop event
- May need to store dragged node type in event.dataTransfer
