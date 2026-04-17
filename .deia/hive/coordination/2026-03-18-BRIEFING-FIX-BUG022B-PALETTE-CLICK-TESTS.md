# BRIEFING: Fix BUG-022-B paletteClickToPlace tests

**Date:** 2026-03-18
**From:** Q33NR
**To:** Q33N
**Priority:** P0
**Model:** Haiku

---

## Objective

Fix 8 failing tests in `browser/src/primitives/canvas/__tests__/paletteClickToPlace.test.tsx`. All fail with `TypeError: this._dispatch is not a function` at `messageBus.ts:217`.

---

## Root Cause Analysis

The test file creates MessageBus instances like this:
```typescript
const bus = new MessageBus('canvas-palette');  // ❌ Missing _dispatch argument
```

But the MessageBus constructor now requires a dispatch function as its first argument (for event ledger integration):
```typescript
constructor(_dispatch: Dispatch<ShellAction>) {
  this._dispatch = _dispatch
  // ...
}
```

The crossWindow test file shows the correct pattern:
```typescript
const mockDispatch = vi.fn()
const bus = new MessageBus(mockDispatch)  // ✅ Correct
```

---

## Files to Read First

1. **Test file to fix:**
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\paletteClickToPlace.test.tsx`

2. **Reference for correct MessageBus mock:**
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\__tests__\messageBus.crossWindow.test.ts` (lines 24-30)

3. **MessageBus implementation (for context):**
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\messageBus.ts` (line 217 is where _dispatch is called)

---

## Task Requirements

**Create ONE task file** for a bee to:

1. **Fix the MessageBus construction pattern** in paletteClickToPlace.test.tsx
   - Add `mockDispatch = vi.fn()` in the beforeEach or at the start of each test
   - Change all `new MessageBus('pane-id')` to `new MessageBus(mockDispatch)`
   - Do NOT modify any MessageBus production code
   - Do NOT modify any other test files

2. **Verify all 10 tests pass** after the fix
   - 8 currently failing tests
   - 2 currently passing tests
   - All should pass after fix

3. **Run regression tests** to ensure no impact on related icon tests
   - `browser/src/primitives/tree-browser/__tests__/TreeNodeRow.icon.test.tsx` (15 tests must still pass)
   - `browser/src/primitives/tree-browser/__tests__/TreeNodeRow.palette-icons.integration.test.tsx` (if exists)

4. **Test command:**
   ```bash
   cd browser && npx vitest run src/primitives/canvas/__tests__/paletteClickToPlace.test.tsx src/primitives/tree-browser/__tests__/TreeNodeRow.icon.test.tsx
   ```

---

## Constraints

- **Rule 2:** This is a test-only fix. Do NOT modify any production code.
- **Rule 3:** No hardcoded colors (not applicable here, test file only).
- **Rule 4:** No file over 500 lines (current file is 334 lines, well under limit).
- **Rule 6:** No stubs. Complete implementation only.

---

## Deliverables Checklist

The task file must specify:

- [ ] **Objective:** Fix MessageBus mock in paletteClickToPlace.test.tsx
- [ ] **Files to modify:** Only `paletteClickToPlace.test.tsx`
- [ ] **Acceptance criteria:**
  - [ ] All 10 tests in paletteClickToPlace.test.tsx pass
  - [ ] All 15 tests in TreeNodeRow.icon.test.tsx still pass
  - [ ] No production code modified
  - [ ] No hardcoded colors (verify via grep if any CSS is touched)
- [ ] **Test requirements:**
  - [ ] Run test command provided above
  - [ ] Paste full test output showing 25/25 passing (10 + 15)
- [ ] **Response file:** 8-section format as per BOOT.md

---

## Success Criteria

When the bee completes, we should have:
- ✅ All 10 paletteClickToPlace tests passing
- ✅ All 15 TreeNodeRow icon tests still passing
- ✅ No production code changes
- ✅ Complete response file with test output showing 25/25 passing

---

## Notes

- This is a simple fix. Pattern: copy the mockDispatch setup from crossWindow.test.ts.
- Haiku model is sufficient for this test-only fix.
- No timeouts needed. Should complete in under 5 minutes.
- No follow-up tasks expected unless tests reveal deeper issues.

---

## Q33N — Next Steps

1. Read the three files listed in "Files to Read First"
2. Write ONE task file to `.deia/hive/tasks/`
   - File name: `2026-03-18-TASK-BUG022B-FIX-PALETTE-CLICK-TESTS.md`
3. Verify task file includes all checklist items above
4. Return to Q33NR for review before dispatching
