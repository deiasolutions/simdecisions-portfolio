# BUG-015: Cannot drag pane into an open pane in Stage

## Objective
Fix drag-and-drop so users can drag a pane/app into an already-occupied pane slot in Stage, triggering a swap or split instead of being rejected.

## Context
In Stage (multi-pane layout), dragging a pane onto an occupied slot does nothing. The drop zone detection in ShellNodeRenderer.tsx (lines ~146-178) and DropZone.tsx reject drops onto occupied panes. The MOVE_APP action in layout.ts (lines ~143-184) may also need zone logic fixes.

## Files to Read First
- `browser/src/shell/components/ShellNodeRenderer.tsx`
- `browser/src/shell/components/DropZone.tsx`
- `browser/src/shell/components/SwapTarget.tsx`
- `browser/src/shell/actions/layout.ts`
- `browser/src/shell/dragDropUtils.ts`
- `browser/src/shell/__tests__/dragDropUtils.test.ts`

## Deliverables
- [ ] Fix ShellNodeRenderer drag event handlers to accept drops on occupied panes
- [ ] Update DropZone to show swap/split indicators on occupied panes
- [ ] Ensure MOVE_APP action handles occupied target correctly (swap or split)
- [ ] Tests for drag onto occupied pane scenarios

## Acceptance Criteria
- [ ] Dragging pane A onto occupied pane B triggers swap (A and B trade places)
- [ ] Drop zone visual indicators appear on hover over occupied panes
- [ ] Existing drag-to-empty-slot behavior unchanged
- [ ] All drag-drop tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/shell/__tests__/dragDropUtils.test.ts`
- [ ] `cd browser && npx vitest run --reporter=verbose src/shell/__tests__/reducer.swap.test.ts`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Depends On
- BL023 (shell swap/merge must be fixed first since this uses SWAP_CONTENTS)

## Model Assignment
haiku

## Priority
P0
