# BRIEFING: BUG-054 Deep Dive — Pane Drag Into Empty Area

**Date:** 2026-03-25
**From:** Q33NR
**To:** Q33N
**Model:** sonnet
**Role:** queen
**Type:** Research (no code changes)

## Objective

BUG-054 is confirmed still broken as of 2026-03-25. The user cannot drag a pane into an open/empty area in Stage. Prior research found that the MOVE_APP handler in `layout.ts:193` checks for empty panes and test coverage exists, yet the feature does not work in practice. Find the root cause.

## What We Know

- MOVE_APP handler (layout.ts:165-232) has code to handle dragging onto empty panes (line 193)
- Test coverage exists in `moveAppOntoOccupied.test.ts:274-353`
- ShellNodeRenderer.tsx:146-189 has drag handlers
- PaneChrome.tsx:152-160 has drag handle
- Commit 11b2fb7 fixed "BUG-015 pane drag visual feedback" but did NOT fix this
- The code LOOKS like it should work, but it DOESN'T — so the bug is in the gap between what the code says and what actually happens in the browser

## Research Tasks

1. **Trace the full drag flow end-to-end:**
   - Where does the drag start? (PaneChrome drag handle)
   - What data is set on the drag event? (dataTransfer)
   - What drop targets exist? (ShellNodeRenderer onDragOver/onDrop)
   - What conditions must be true for the drop to be accepted?
   - What happens when the drop fires? (dispatch MOVE_APP)

2. **Find the gap — why doesn't it work?**
   - Is the empty pane even rendering a drop target?
   - Does EmptyPane have onDragOver/onDrop handlers?
   - Is there a CSS `pointer-events: none` or `z-index` issue blocking the drop target?
   - Does the drag data format match what the drop handler expects?
   - Is there an `e.preventDefault()` missing in onDragOver (required for HTML5 DnD)?
   - Are there competing drag handlers (canvas, kanban) swallowing the event?

3. **Check EmptyPane specifically:**
   - Does EmptyPane.tsx render inside ShellNodeRenderer?
   - Does it have its own drag handlers or rely on ShellNodeRenderer's?
   - Is there a case where an "empty area" is NOT an EmptyPane node in the tree?

4. **Identify the fix:**
   - What specific code change would make drag-to-empty-area work?
   - Is it a missing handler, a missing preventDefault, a CSS issue, or a tree structure issue?

## Key Files

- `browser/src/shell/components/ShellNodeRenderer.tsx` — drag/drop handlers
- `browser/src/shell/components/PaneChrome.tsx` — drag handle (drag start)
- `browser/src/shell/components/EmptyPane.tsx` — empty pane component
- `browser/src/shell/actions/layout.ts` — MOVE_APP action handler
- `browser/src/shell/reducer.ts` — state management
- `browser/src/shell/dragDropUtils.ts` — drag utilities
- `browser/src/shell/components/FloatPaneWrapper.tsx` — float handling
- `browser/src/shell/types.ts` — AppNode, SplitNode types

## Deliverables

Write a response file with:
1. The exact root cause of BUG-054
2. The specific files and line numbers that need to change
3. A description of the fix (what code to add/modify)
4. Whether this fix would also resolve BUG-059 and BUG-066

## Constraints

- **Read-only research.** Do NOT write code or modify files.
- **Do NOT dispatch bees.**
- Write your response to `.deia/hive/responses/`
