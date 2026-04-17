# BUG-019 (STAGING): Canvas drag captured by Stage instead of canvas surface

## Status: STAGING — waiting for BUG-015 (canvas chain item 2 of 3)

## Sequence: Canvas chain item 2 of 3 (BUG-015 → BUG-019 → BUG-018)

## Objective
Fix drag so palette components drop onto canvas surface, not intercepted by Stage shell's pane drag system. Canvas needs stopPropagation on internal drags.

## Files At Risk
- Canvas primitives, ShellNodeRenderer.tsx, dragDropUtils.ts

## Depends On
- BUG-022-B — must be done
- BUG-015 — must be done (both touch ShellNodeRenderer drag handlers)

## Model Assignment
sonnet

## Priority
P0
