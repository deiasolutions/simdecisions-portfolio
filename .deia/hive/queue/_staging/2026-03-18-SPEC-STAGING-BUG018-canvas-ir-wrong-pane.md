# BUG-018 (STAGING): Canvas IR response appears in wrong pane (Code egg instead of Canvas)

## Status: STAGING — waiting for BUG-019 (canvas chain item 3 of 3)

## Sequence: Canvas chain item 3 of 3 (BUG-015 → BUG-019 → BUG-018)

## Objective
Fix Canvas IR generation so response routes to Canvas terminal pane, not Code egg's chat pane. This is a bus routing/scoping issue.

## Files At Risk
- Canvas primitives, useTerminal.ts, relayBus.ts

## Depends On
- BUG-022-B, BUG-015, BUG-019 — all must clear first

## Model Assignment
sonnet

## Priority
P0
