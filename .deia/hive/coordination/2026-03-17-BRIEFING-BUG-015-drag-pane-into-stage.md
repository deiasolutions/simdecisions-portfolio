# BRIEFING: BUG-015 — Cannot Drag Pane Into Occupied Slot

**To:** Q33N (Queen Coordinator)
**From:** Q88NR (Regent)
**Date:** 2026-03-17
**Spec File:** `.deia/hive/queue/2026-03-17-SPEC-TASK-BUG015-drag-pane-into-stage.md`

---

## Mission

Create task file(s) for fixing drag-and-drop behavior in Stage so users can drag a pane onto an already-occupied pane slot, triggering a swap instead of being rejected.

---

## Spec Summary

**Priority:** P0
**Model:** Haiku
**Depends On:** BL-023 (shell swap/merge) — ✅ COMPLETE

**Objective:** Fix drag-and-drop so dragging pane A onto occupied pane B triggers swap (A and B trade places).

**Current Problem:**
- Dragging a pane onto an occupied slot does nothing
- Drop zone detection in ShellNodeRenderer.tsx and DropZone.tsx reject drops onto occupied panes
- MOVE_APP action may need zone logic fixes

**Acceptance Criteria:**
- [ ] Dragging pane A onto occupied pane B triggers swap (A and B trade places)
- [ ] Drop zone visual indicators appear on hover over occupied panes
- [ ] Existing drag-to-empty-slot behavior unchanged
- [ ] All drag-drop tests pass

---

## Files to Investigate

**Per spec:**
- `browser/src/shell/components/ShellNodeRenderer.tsx` (lines ~146-178)
- `browser/src/shell/components/DropZone.tsx`
- `browser/src/shell/components/SwapTarget.tsx`
- `browser/src/shell/actions/layout.ts` (lines ~143-184 - MOVE_APP action)
- `browser/src/shell/dragDropUtils.ts`
- `browser/src/shell/__tests__/dragDropUtils.test.ts`

---

## Deliverables

- [ ] Fix ShellNodeRenderer drag event handlers to accept drops on occupied panes
- [ ] Update DropZone to show swap/split indicators on occupied panes
- [ ] Ensure MOVE_APP action handles occupied target correctly (swap or split)
- [ ] Tests for drag onto occupied pane scenarios

---

## Smoke Tests

Per spec:
```bash
cd browser && npx vitest run --reporter=verbose src/shell/__tests__/dragDropUtils.test.ts
cd browser && npx vitest run --reporter=verbose src/shell/__tests__/reducer.swap.test.ts
```

---

## Context from BL-023

BL-023 just completed. It verified that SWAP_CONTENTS action works correctly and added comprehensive tests. This means:
- The shell reducer SWAP_CONTENTS action is **ready to use**
- 14 swap tests exist in `reducer.swap.test.ts` and pass
- The implementation correctly swaps pane contents by ID

So BUG-015 can leverage the existing SWAP_CONTENTS action. The issue is purely in the **drag-drop detection layer** — not in the reducer.

---

## Task File Requirements

**Checklist (per HIVE.md):**
- [ ] Deliverables match spec acceptance criteria
- [ ] File paths are absolute (Windows format: `C:\Users\davee\...`)
- [ ] Test requirements specified (how many tests, which scenarios, which files)
- [ ] CSS uses var(--sd-*) only (if any CSS changes)
- [ ] No file over 500 lines
- [ ] No stubs or TODOs
- [ ] Response file template included (8 sections)

**Model:** Haiku (per spec)

---

## Suggested Breakdown

I recommend **1 task** (this is a focused fix):

**TASK-BUG-015: Fix drag onto occupied pane to trigger swap**
- Modify ShellNodeRenderer.tsx drag handlers to accept drops on occupied panes
- Update DropZone.tsx to show swap indicators on occupied panes
- Ensure MOVE_APP action dispatches SWAP_CONTENTS when target is occupied
- Add tests for drag-onto-occupied scenarios
- Run existing drag-drop tests to verify no regression

---

## Notes

- This is a **bug fix**, not a new feature. The swap mechanism already exists (BL-023). We're just wiring drag-drop to use it.
- Visual indicators (DropZone) should show "swap" when hovering over occupied pane.
- Existing drag-to-empty behavior must remain unchanged.
- Test files already exist — we're adding new test cases.

---

## Response Required

Please create task file(s) following the checklist. Submit to `.deia/hive/tasks/` with naming format:

`2026-03-17-TASK-BUG-015-drag-onto-occupied-pane.md`

Include full 8-section response file template in the task.

---

**Q88NR signature**
Briefing complete. Awaiting Q33N task files.
