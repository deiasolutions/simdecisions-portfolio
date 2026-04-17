# BUG-015 (STAGING): Cannot drag pane into occupied pane in Stage

## Status: STAGING — waiting for BUG-022-B fix cycle to clear (canvas files)

## Sequence: Canvas chain item 1 of 3 (BUG-015 → BUG-019 → BUG-018)

## Objective
Fix drag-and-drop so users can drag a pane/app into an already-occupied pane slot, triggering a swap.

## Files At Risk
- ShellNodeRenderer.tsx, DropZone.tsx, layout.ts, dragDropUtils.ts

## Depends On
- BUG-022-B (canvas click-to-place) — must clear fix cycle first
- BL-023 (shell swap/merge) — ✅ already DONE

## Model Assignment
sonnet

## Priority
P0
