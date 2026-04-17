# Q33N Report: TASK-BUG022B Ready for Review

**Status:** Task file written, awaiting Q33NR review
**Date:** 2026-03-18
**Bot ID:** QUEEN-2026-03-18-BRIEFING-FIX-BUG022

---

## Task File Created

**Location:** `.deia/hive/tasks/2026-03-18-TASK-BUG022B-FIX-PALETTE-CLICK-TESTS.md`

**Objective:** Fix 8 failing tests in paletteClickToPlace.test.tsx by updating MessageBus constructor calls to match current signature (requires dispatch function as first parameter).

---

## What the Task File Specifies

### Problem
- MessageBus constructor changed to require `_dispatch` function as first parameter
- Test file still uses old pattern: `new MessageBus('pane-id')` instead of `new MessageBus(mockDispatch)`
- Error: `TypeError: this._dispatch is not a function` at messageBus.ts:217

### Solution
- Update all 10 MessageBus instantiations in the test file
- Add `mockDispatch = vi.fn()` in beforeEach or at test start
- Pattern: copy from messageBus.crossWindow.test.ts lines 24-30

### Files to Modify
- **Only:** `browser/src/primitives/canvas/__tests__/paletteClickToPlace.test.tsx`
- **Reference:** `browser/src/infrastructure/relay_bus/__tests__/messageBus.crossWindow.test.ts`
- **Do NOT modify:** Any production code

### Test Requirements
1. Run paletteClickToPlace.test.tsx → 10 tests must pass
2. Run TreeNodeRow.icon.test.tsx → 15 tests must still pass
3. Combined: 25/25 passing

### Constraints
- Test-only fix (Rule 2)
- No stubs (Rule 6)
- File is 334 lines, under 500-line limit (Rule 4)

---

## Deliverables Checklist (from briefing)

Task file includes:

- [x] **Objective:** Fix MessageBus mock in paletteClickToPlace.test.tsx
- [x] **Files to modify:** Only `paletteClickToPlace.test.tsx`
- [x] **Acceptance criteria:**
  - [x] All 10 tests in paletteClickToPlace.test.tsx pass
  - [x] All 15 tests in TreeNodeRow.icon.test.tsx still pass
  - [x] No production code modified
  - [x] No hardcoded colors (verify via grep if any CSS is touched)
- [x] **Test requirements:**
  - [x] Run test command provided
  - [x] Paste full test output showing 25/25 passing (10 + 15)
- [x] **Response file:** 8-section format as per BOOT.md

---

## Analysis

### Root Cause Verified
I read all three files referenced in the briefing:
1. **paletteClickToPlace.test.tsx** — Contains 10 MessageBus instantiations using old pattern (lines 17, 60, 96, 139, 175, 212, 266, 289, 312)
2. **messageBus.crossWindow.test.ts** — Shows correct pattern (lines 24-30): `mockDispatch = vi.fn()`, `new MessageBus(mockDispatch)`
3. **messageBus.ts** — Line 217 calls `this._dispatch()`, which fails when _dispatch is undefined

### Scope Verification
- **Test file only:** No production code changes required
- **Simple pattern fix:** Replace constructor calls, add mock dispatch
- **No architecture changes:** MessageBus implementation is correct, tests just need updating
- **Regression risk:** Low (isolated test file, regression test included)

### Model Assignment
- **Haiku is appropriate** for this fix (simple pattern replacement)
- **Estimated time:** < 5 minutes
- **No timeout needed** (should complete quickly)

---

## Ready for Q33NR Review

The task file is complete and follows all BOOT.md requirements:
- Absolute file paths
- All 8 response sections specified
- Test commands provided
- Acceptance criteria clear
- Constraints listed
- No stubs allowed

**Next step:** Q33NR reviews this task file and approves dispatch, or requests corrections.

---

## Files in This Report

1. **Task file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-18-TASK-BUG022B-FIX-PALETTE-CLICK-TESTS.md`
2. **This report:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-Q33N-TASK-BUG022B-READY.md`
