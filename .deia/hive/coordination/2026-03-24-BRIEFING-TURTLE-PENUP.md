# BRIEFING: Fix Turtle Pen Up Bug (BUG-049)

**To:** Q33N
**From:** Q33NR
**Date:** 2026-03-24
**Spec:** SPEC-TURTLE-PENUP
**Priority:** P1
**Model:** haiku

---

## Objective

Fix BUG-049: The turtle drawing canvas's `circle` and `rect` commands ignore pen state and always draw, even when `penup` has been called.

---

## Context

The DrawingCanvasApp primitive implements Logo-style turtle graphics. Commands like `penup`/`pendown` control whether the turtle draws as it moves.

**Current behavior:**
- `forward` and `back` commands correctly check `t.penDown` before drawing
- `circle` and `rect` commands ALWAYS draw, ignoring `t.penDown`

**Root cause:**
The `circle` and `rect` handlers (lines 242-253 in DrawingCanvasApp.tsx) do not check `t.penDown` before calling p5 drawing functions.

---

## Key Files

**Primary file to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\drawing-canvas\DrawingCanvasApp.tsx`
  - Lines 66-88: command parsing (`penup`/`pu` → `{ type: 'penup' }`)
  - Lines 203-207: penup/pendown execution (sets `t.penDown = false/true`)
  - Lines 174-195: forward/back correctly check `if (t.penDown)` before drawing ← **USE THIS PATTERN**
  - Lines 242-253: `circle` and `rect` handlers ← **FIX THESE**

---

## Required Fix

Wrap `circle` and `rect` drawing operations in `if (t.penDown)` checks, matching the pattern used in `forward`/`back` handlers.

**Pattern to follow (from forward handler):**
```typescript
if (t.penDown) {
  p.line(t.x, t.y, nx, ny);
}
// Always update position, only draw if pen is down
```

**Apply to circle:**
```typescript
case 'circle': {
  const radius = cmd.radius || 50;
  if (t.penDown) {  // ← ADD THIS CHECK
    p.circle(t.x, t.y, radius * 2);
  }
  break;
}
```

**Apply to rect:**
```typescript
case 'rect': {
  const w = cmd.width || 50;
  const h = cmd.height || 50;
  if (t.penDown) {  // ← ADD THIS CHECK
    p.rect(t.x - w / 2, t.y - h / 2, w, h);
  }
  break;
}
```

---

## Test Requirements

Create test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\drawing-canvas\__tests__\DrawingCanvasApp.penstate.test.tsx`

**Required tests (6 minimum):**
1. `penup` command sets `t.penDown = false`
2. `pendown` command sets `t.penDown = true`
3. `forward` while pen up moves position but does NOT draw line
4. `circle` while pen up does NOT draw circle
5. `rect` while pen up does NOT draw rectangle
6. `circle` and `rect` while pen down draw correctly

**Test strategy:**
- Mock p5 instance to track drawing calls
- Verify pen state changes after `penup`/`pendown`
- Verify position updates happen regardless of pen state
- Verify drawing function calls (p.line, p.circle, p.rect) only occur when pen is down

---

## Acceptance Criteria (from spec)

- [ ] `penup` command sets `t.penDown = false`
- [ ] `pendown` command sets `t.penDown = true`
- [ ] `forward` command while pen up moves position without drawing line
- [ ] `circle` command while pen up does NOT draw circle (checks `t.penDown` before drawing)
- [ ] `rect` command while pen up does NOT draw rectangle (checks `t.penDown` before drawing)
- [ ] `circle` and `rect` commands while pen down draw correctly
- [ ] All 6 tests passing for pen state and conditional drawing
- [ ] No stubs: all drawing command handlers fully implemented

---

## Constraints

- **Rule 3:** No hardcoded colors (not applicable to this fix)
- **Rule 4:** No file over 500 lines (DrawingCanvasApp.tsx is currently well under this)
- **Rule 5:** TDD — write tests first
- **Rule 6:** No stubs — all handlers must be fully implemented

---

## Task Breakdown

I recommend **ONE task** for a single Haiku bee:

**TASK-TURTLE-PENUP:** Fix circle/rect pen state bug in DrawingCanvasApp
- Read DrawingCanvasApp.tsx (especially forward/back pattern)
- Write 6 tests for pen state handling
- Fix `circle` and `rect` handlers to check `t.penDown`
- Verify all tests pass
- Write response file

---

## Next Steps

1. Read the DrawingCanvasApp.tsx file
2. Write task file(s)
3. Return task files to me (Q33NR) for review
4. After I approve: dispatch bee(s)
5. After bee completes: review response file and report results to me

---

**Q33N: Please read the key file, write the task file, and return it for my review. Do NOT dispatch the bee yet.**
