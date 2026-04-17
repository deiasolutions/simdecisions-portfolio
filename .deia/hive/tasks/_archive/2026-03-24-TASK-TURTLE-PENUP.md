# TASK-TURTLE-PENUP: Fix turtle circle/rect pen state bug

**Bug ID:** BUG-049
**Priority:** P1
**Model:** haiku
**Date:** 2026-03-24

## Objective

Fix the turtle drawing canvas so that `circle` and `rect` commands respect pen state (`penup`/`pendown`) and only draw when the pen is down.

## Context

The DrawingCanvasApp primitive implements Logo-style turtle graphics with commands like `penup`, `pendown`, `forward`, `back`, `circle`, and `rect`.

**Current behavior:**
- `forward` and `back` commands correctly check `t.penDown` before drawing lines
- `circle` and `rect` commands ALWAYS draw, ignoring `t.penDown` state

**Root cause:**
The `circle` and `rect` handlers (lines 242-253 in DrawingCanvasApp.tsx) do not check `t.penDown` before calling p5 drawing functions.

**Pattern to follow:**
Lines 174-195 show the correct pattern for `forward` and `back`:
```typescript
if (t.penDown) {
  p.stroke(t.penColor[0], t.penColor[1], t.penColor[2])
  p.strokeWeight(t.penWidth)
  p.line(t.x, t.y, x2, y2)
}
// Always update position, only draw if pen is down
```

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\drawing-canvas\DrawingCanvasApp.tsx`
  - Lines 66-88: command parsing (`penup`/`pu` → `{ type: 'penup' }`)
  - Lines 203-207: penup/pendown execution (sets `t.penDown = false/true`)
  - Lines 174-195: forward/back correctly check `if (t.penDown)` before drawing ← **USE THIS PATTERN**
  - Lines 242-253: `circle` and `rect` handlers ← **FIX THESE**

## Deliverables

- [ ] Test file created: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\drawing-canvas\__tests__\DrawingCanvasApp.penstate.test.tsx`
- [ ] 6+ tests written for pen state handling (TDD — write tests first)
- [ ] `circle` handler modified to check `t.penDown` before drawing
- [ ] `rect` handler modified to check `t.penDown` before drawing
- [ ] All 6+ tests passing
- [ ] No stubs: all drawing command handlers fully implemented

## Test Requirements

Create test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\drawing-canvas\__tests__\DrawingCanvasApp.penstate.test.tsx`

**Required tests (minimum 6):**
1. `penup` command sets `t.penDown = false`
2. `pendown` command sets `t.penDown = true`
3. `forward` while pen up moves position but does NOT draw line
4. `circle` while pen up does NOT draw circle
5. `rect` while pen up does NOT draw rectangle
6. `circle` and `rect` while pen down draw correctly

**Test strategy:**
- Mock p5 instance to track drawing calls (p.line, p.circle, p.rect)
- Use `parseCommand()` and `executeParsed()` to verify pen state changes
- Verify pen state changes after `penup`/`pendown`
- Verify position updates happen regardless of pen state
- Verify drawing function calls only occur when pen is down

**Test pattern example:**
```typescript
import { describe, it, expect, vi } from 'vitest'
import { parseCommand } from '../DrawingCanvasApp'

describe('DrawingCanvasApp pen state', () => {
  it('penup command sets penDown to false', () => {
    const cmd = parseCommand('penup')
    expect(cmd).toEqual({ type: 'penup' })
    // Test execution sets t.penDown = false
  })

  it('circle while pen up does NOT draw', () => {
    // Set t.penDown = false
    // Execute circle command
    // Verify p.circle was NOT called
  })
})
```

## Code Changes Required

**In `DrawingCanvasApp.tsx`, modify lines 242-253:**

**Before (circle):**
```typescript
case 'circle':
  p.noFill()
  p.stroke(t.penColor[0], t.penColor[1], t.penColor[2])
  p.strokeWeight(t.penWidth)
  p.circle(t.x, t.y, cmd.r * 2)
  break
```

**After (circle):**
```typescript
case 'circle':
  if (t.penDown) {
    p.noFill()
    p.stroke(t.penColor[0], t.penColor[1], t.penColor[2])
    p.strokeWeight(t.penWidth)
    p.circle(t.x, t.y, cmd.r * 2)
  }
  break
```

**Before (rect):**
```typescript
case 'rect':
  p.noFill()
  p.stroke(t.penColor[0], t.penColor[1], t.penColor[2])
  p.strokeWeight(t.penWidth)
  p.rectMode(p.CENTER)
  p.rect(t.x, t.y, cmd.w, cmd.h)
  break
```

**After (rect):**
```typescript
case 'rect':
  if (t.penDown) {
    p.noFill()
    p.stroke(t.penColor[0], t.penColor[1], t.penColor[2])
    p.strokeWeight(t.penWidth)
    p.rectMode(p.CENTER)
    p.rect(t.x, t.y, cmd.w, cmd.h)
  }
  break
```

## Constraints

- **Rule 3:** No hardcoded colors (not applicable to this fix — no new colors)
- **Rule 4:** No file over 500 lines (DrawingCanvasApp.tsx is currently 458 lines — well under limit)
- **Rule 5:** TDD — write tests first, then fix the code
- **Rule 6:** No stubs — all handlers must be fully implemented

## Acceptance Criteria

- [ ] `penup` command sets `t.penDown = false`
- [ ] `pendown` command sets `t.penDown = true`
- [ ] `forward` command while pen up moves position without drawing line (already works, verify with test)
- [ ] `circle` command while pen up does NOT draw circle (check `t.penDown` before drawing)
- [ ] `rect` command while pen up does NOT draw rectangle (check `t.penDown` before drawing)
- [ ] `circle` and `rect` commands while pen down draw correctly
- [ ] All 6+ tests passing for pen state and conditional drawing
- [ ] No stubs: all drawing command handlers fully implemented

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-TURTLE-PENUP-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
