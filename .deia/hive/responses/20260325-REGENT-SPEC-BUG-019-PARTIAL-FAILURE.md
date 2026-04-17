# SPEC-BUG-019: Canvas Drag Isolation -- PARTIAL FAILURE

**From:** Q33NR (REGENT-QUEUE-TEMP-SPEC-BUG-019)
**To:** Q88N (Dave)
**Date:** 2026-03-25 14:08
**Status:** ⚠️ PARTIAL FAILURE — NEEDS REVIEW

---

## Summary

SPEC-BUG-019 (Canvas Drag Isolation) has been processed with mixed results:

- ✅ **TASK-BUG-019-A** — COMPLETE (7/7 tests passing)
- ❌ **TASK-BUG-019-B** — FAILED (5/5 tests failing, `DragEvent is not defined`)
- ⏸️ **TASK-BUG-019-C** — NOT DISPATCHED (depends on A and B)

---

## What Worked

### TASK-BUG-019-A: Palette and TreeNode Canvas Internal Marker ✅

**BEE:** BEE-HAIKU
**Duration:** ~45 minutes
**Cost:** $1.99 USD
**Response File:** `.deia/hive/responses/20260325-TASK-BUG-019-A-RESPONSE.md`

**Deliverables:**
- ✅ paletteAdapter.ts: Added `canvasInternal: true` to meta object
- ✅ TreeNodeRow.tsx: Check `canvasInternal` and set `canvas/internal` dataTransfer type
- ✅ TreeNodeRow.tsx: Call `stopPropagation()` for canvas-internal drags
- ✅ 7/7 tests passing (3 paletteAdapter + 4 TreeNodeRow)
- ✅ No regressions (6 existing drag tests still passing)

**Test Results:**
```
✓ paletteAdapter.canvasInternal.test.ts: 3/3 passed
✓ TreeNodeRow.canvasInternal.test.tsx: 4/4 passed
✓ TreeNodeRow.drag.test.tsx: 6/6 passed (no regressions)
```

**Files Modified:**
- `browser/src/primitives/tree-browser/adapters/paletteAdapter.ts` (line 68)
- `browser/src/primitives/tree-browser/TreeNodeRow.tsx` (lines 70-77)
- `browser/src/primitives/tree-browser/adapters/__tests__/paletteAdapter.canvasInternal.test.ts` (new, 75 lines)
- `browser/src/primitives/tree-browser/__tests__/TreeNodeRow.canvasInternal.test.tsx` (new, 206 lines)

---

## What Failed

### TASK-BUG-019-B: Shell Early Return for Canvas Internal Drags ❌

**BEE:** BEE-HAIKU
**Duration:** ~13 minutes
**Cost:** $1.99 USD
**Response File:** MISSING (stub violation — bee claimed to create it but didn't)
**RAW File:** `.deia/hive/responses/20260325-1344-BEE-HAIKU-2026-03-25-TASK-BUG-019-B-SHELL-EARLY-RETURN-RAW.txt`

**Failures:**
1. **Missing response file** — Bee claimed to create `.deia/hive/responses/20260325-TASK-BUG-019-B-RESPONSE.md` but file does not exist. **STUB VIOLATION (Rule 6).**
2. **All tests failing** — 5/5 tests fail with `ReferenceError: DragEvent is not defined`
3. **Test environment issue** — Tests use `new DragEvent()` which is not available in vitest/jsdom environment

**Test Results:**
```
❌ ShellNodeRenderer.canvasDrag.test.tsx: 0/5 passed
   - onDragOver: return early when canvas/internal → DragEvent is not defined
   - onDragOver: still process hhs/node-id drags → DragEvent is not defined
   - onDragOver: canvas/internal takes precedence → DragEvent is not defined
   - onDrop: return early when canvas/internal → DragEvent is not defined
   - onDrop: still process hhs/node-id drops → DragEvent is not defined
```

**Files Modified:**
- `browser/src/shell/components/ShellNodeRenderer.tsx` (added early return checks at lines 163 and 181)
- `browser/src/shell/components/__tests__/ShellNodeRenderer.canvasDrag.test.tsx` (new, 174 lines, **ALL TESTS BROKEN**)

**Root Cause:**
The test file uses `new DragEvent()` constructor which is not available in vitest's jsdom environment. The bee should have used `fireEvent.dragOver()` from `@testing-library/react` or created a mock DragEvent using `Object.assign(new Event('dragover'), { dataTransfer: mockDataTransfer })`.

---

## What Wasn't Done

### TASK-BUG-019-C: Replace Drag Isolation Tests with Runtime Behavior Tests ⏸️

**Status:** NOT DISPATCHED
**Reason:** TASK-BUG-019-C depends on both A and B completing successfully. Since B failed, C was not dispatched.

---

## Mechanical Review Violations

### TASK-BUG-019-B Violations

1. **Response file missing** — Bee claimed to create it but didn't (STUB VIOLATION, Rule 6)
2. **Tests not passing** — All 5 tests fail due to environment issue
3. **TDD not followed** — Tests were written but don't work (broken tests are worse than no tests)

---

## Next Steps

### Option 1: Create P0 Fix Spec for TASK-BUG-019-B

Create `.deia/hive/queue/SPEC-FIX-BUG-019-B-DRAG-EVENT-TESTS.md`:
- Fix the 5 failing tests in `ShellNodeRenderer.canvasDrag.test.tsx`
- Replace `new DragEvent()` with proper mocking
- Verify all 5 tests pass
- Create the missing response file

Then dispatch TASK-BUG-019-C after fix completes.

### Option 2: Manual Fix (Q33NR-direct)

With Q88N approval, I can:
1. Fix the test file directly (replace `new DragEvent()` with proper mocking)
2. Verify tests pass
3. Dispatch TASK-BUG-019-C

### Option 3: Flag NEEDS_DAVE

If fix attempts exceed 2 cycles, flag this spec as NEEDS_DAVE and move on.

---

## Cost Summary

- **TASK-BUG-019-A:** $1.99 USD (COMPLETE)
- **TASK-BUG-019-B:** $1.99 USD (FAILED)
- **Total Spent:** $3.98 USD
- **Work Remaining:** TASK-BUG-019-B fix + TASK-BUG-019-C

---

## Recommendation

**I recommend Option 1:** Create a P0 fix spec for TASK-BUG-019-B. The code changes in ShellNodeRenderer.tsx are correct (early return logic). Only the tests are broken due to environment issues. A quick fix spec can resolve this.

---

**Q88N: What would you like me to do?**

1. Create P0 fix spec for TASK-BUG-019-B tests
2. Approve Q33NR-direct fix (I fix the tests manually)
3. Flag NEEDS_DAVE and move on

---

**Awaiting Q88N direction.**
