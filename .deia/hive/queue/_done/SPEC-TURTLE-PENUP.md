# SPEC-TURTLE-PENUP

## Bugs
BUG-049

## Priority
P1

## Model
haiku

## Summary
Turtle draw pen up command does not work. The `circle` and `rect` commands ignore pen state and always draw.

## Key Files
- `browser/src/primitives/drawing-canvas/DrawingCanvasApp.tsx`
  - Lines 66-88: command parsing (`penup`/`pu` → `{ type: 'penup' }`)
  - Lines 203-207: penup/pendown execution (sets `t.penDown = false/true`)
  - Lines 174-195: forward/back correctly check `if (t.penDown)` before drawing
  - Lines 242-253: `circle` and `rect` ALWAYS stroke regardless of `penDown` — THIS IS THE BUG

## Root Cause
`circle` and `rect` command handlers do not check `t.penDown` before drawing. They always call `p.circle()` / `p.rect()` with stroke.

## Required Fix
Wrap `circle` and `rect` drawing in `if (t.penDown)` check, same pattern as forward/back handlers.

## Tests Required
1. `penup` sets `t.penDown = false`
2. `pendown` sets `t.penDown = true`
3. `forward` while pen up moves position but does not draw line
4. `circle` while pen up does NOT draw circle
5. `rect` while pen up does NOT draw rectangle
6. `circle` while pen down draws correctly

## Depends On
Nothing

## Acceptance Criteria
- [ ] `penup` command sets `t.penDown = false`
- [ ] `pendown` command sets `t.penDown = true`
- [ ] `forward` command while pen up moves position without drawing line
- [ ] `circle` command while pen up does NOT draw circle (checks `t.penDown` before drawing)
- [ ] `rect` command while pen up does NOT draw rectangle (checks `t.penDown` before drawing)
- [ ] `circle` and `rect` commands while pen down draw correctly
- [ ] All 6 tests passing for pen state and conditional drawing
- [ ] No stubs: all drawing command handlers fully implemented
