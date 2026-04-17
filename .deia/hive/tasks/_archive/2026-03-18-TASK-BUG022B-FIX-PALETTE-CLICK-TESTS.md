# TASK-BUG022B: Fix MessageBus mock in paletteClickToPlace tests

## Objective

Fix 8 failing tests in `paletteClickToPlace.test.tsx` by updating MessageBus construction to match current constructor signature (requires dispatch function).

## Context

The MessageBus constructor was updated to require a `_dispatch` function as its first parameter for event ledger integration. The paletteClickToPlace test file still uses the old pattern:

```typescript
// ❌ OLD (currently in file, causes TypeError)
const bus = new MessageBus('canvas-palette')

// ✅ NEW (correct pattern)
const mockDispatch = vi.fn()
const bus = new MessageBus(mockDispatch)
```

The reference implementation is in `messageBus.crossWindow.test.ts` lines 24-30, which shows the correct mock pattern.

**Error:** `TypeError: this._dispatch is not a function` at `messageBus.ts:217`

**Root cause:** MessageBus expects `_dispatch` to be a function, but the test is passing a string (or nothing).

## Files to Read First

1. **Test file to fix:**
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\paletteClickToPlace.test.tsx`

2. **Reference implementation:**
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\__tests__\messageBus.crossWindow.test.ts` (lines 24-30 show correct pattern)

3. **MessageBus implementation (context only, do NOT modify):**
   - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\messageBus.ts` (line 217)

## Deliverables

- [ ] **Update all MessageBus instantiations in paletteClickToPlace.test.tsx**
  - Replace ALL instances of `new MessageBus('pane-id')` with `new MessageBus(mockDispatch)`
  - Add `const mockDispatch = vi.fn()` in beforeEach block OR at the start of each test
  - Count: 10 MessageBus instantiations need fixing (lines 17, 60, 96, 139, 175, 212, 266, 289, 312)

- [ ] **Do NOT modify any production code**
  - Do NOT touch `messageBus.ts` or any other non-test files
  - This is a test-only fix

- [ ] **Verify all 10 tests pass**
  - 8 currently failing tests must pass
  - 2 currently passing tests must still pass

## Test Requirements

- [ ] **Run test suite for paletteClickToPlace:**
  ```bash
  cd browser && npx vitest run src/primitives/canvas/__tests__/paletteClickToPlace.test.tsx
  ```
  - All 10 tests must pass

- [ ] **Run regression test for TreeNodeRow icon tests:**
  ```bash
  cd browser && npx vitest run src/primitives/tree-browser/__tests__/TreeNodeRow.icon.test.tsx
  ```
  - All 15 tests must still pass

- [ ] **Combined test command (paste full output):**
  ```bash
  cd browser && npx vitest run src/primitives/canvas/__tests__/paletteClickToPlace.test.tsx src/primitives/tree-browser/__tests__/TreeNodeRow.icon.test.tsx
  ```
  - Expected: 25 tests passing (10 + 15)

## Constraints

- **Rule 2:** Test-only fix. Do NOT modify production code.
- **Rule 3:** Not applicable (test file only, no CSS changes).
- **Rule 4:** Current file is 334 lines, well under 500-line limit.
- **Rule 6:** No stubs. Complete implementation only.

## Acceptance Criteria

- [ ] All 10 tests in `paletteClickToPlace.test.tsx` pass
- [ ] All 15 tests in `TreeNodeRow.icon.test.tsx` still pass
- [ ] No production code modified (only test file changed)
- [ ] Test output shows 25/25 passing tests
- [ ] No hardcoded colors introduced (verify via grep if any CSS touched)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260318-TASK-BUG022B-RESPONSE.md`

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
