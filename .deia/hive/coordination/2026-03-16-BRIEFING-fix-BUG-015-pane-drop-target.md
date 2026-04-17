# BRIEFING: Fix BUG-015 — Pane Drop Target Not Working

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-16
**Spec:** `2026-03-16-SPEC-fix-BUG-015-pane-drop-target.md`
**Priority:** P0
**Model Assignment:** Sonnet

---

## Objective

Fix the drag-and-drop system in the shell so users can drag a pane and drop it into another open pane to create a split or replace content. Currently the drop target is not recognized or the drop handler is not firing.

---

## Context from Q88N

This is the first real UAT of pane composition in the Stage runtime. The drag/drop infrastructure exists but may not be fully wired or may have been broken during recent ports.

The shell has:
- `PaneChrome.tsx` (drag/drop handlers on pane chrome)
- `ShellNodeRenderer.tsx` (renders split/pane tree, may have drop zones)
- `reducer.ts` (shell state reducer — MOVE_PANE, SPLIT_PANE actions)
- `types.ts` (shell state types)
- `eggToShell.ts` (EGG layout → shell state)

---

## Files to Read First

Before writing task files, read these:

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\reducer.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts`

---

## Investigation Steps (from Spec)

1. Check if PaneChrome has onDragOver + onDrop handlers
2. Check if drop events set correct dataTransfer MIME types
3. Check if reducer handles MOVE_PANE or equivalent action
4. Check if drop zones render correctly (visual feedback on dragover)
5. Check browser console for errors during drag/drop

---

## Acceptance Criteria (from Spec)

- [ ] User can drag a pane tab/chrome and drop it onto another open pane
- [ ] Drop creates a split (left/right or top/bottom) or replaces pane content
- [ ] Visual drop zone indicator appears on dragover
- [ ] Existing pane tests still pass
- [ ] New tests cover drag-drop pane composition

---

## Constraints

- **No file over 500 lines.** Modularize at 500. Hard limit: 1,000.
- **CSS:** var(--sd-*) only. No hex, no rgb(), no named colors.
- **TDD:** Tests first, then implementation.
- **No stubs.** Every function fully implemented.
- **Model:** Sonnet (complexity warrants it)

---

## Your Task

1. Read the files listed above
2. Identify the bug (missing handlers, broken wiring, etc.)
3. Write a task file for a bee to fix it
4. Return the task file to me for review
5. Do NOT dispatch the bee yet — wait for my approval

---

## Notes

This is a shell-level bug. The fix may touch:
- PaneChrome (add/fix drag handlers)
- ShellNodeRenderer (add/fix drop zones)
- reducer.ts (add/fix MOVE_PANE or SPLIT_PANE actions)
- CSS for drop zone visuals

All changes must have tests. TDD applies.

---

**End of Briefing**
