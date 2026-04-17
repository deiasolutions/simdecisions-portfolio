# TASK-BL207-RUNTIME-VERIFY: Complete and verify showChrome implementation

## Objective
Complete the showChrome implementation in eggToShell.ts (currently hardcoded to true) and verify MenuBar syndication. Previous bee wrote tests but never actually implemented the code changes.

## Context

**Current State:**
- `eggToShell.ts` line 33: **HARDCODED** `chrome: true` (does NOT read from EGG config)
- Test files exist and claim implementation is done, but code doesn't match tests
- Previous bee response says "Changed line 33" but git history shows no such commit
- MenuBar.tsx has TODO comment about "future focused-pane menu syndication"
- PaneChrome.tsx already handles `chrome: false` correctly (lines 28-38)

**What's Missing:**
1. eggToShell.ts does NOT read `showChrome` from EGG config
2. MenuBar syndication is stubbed with TODO comment

**Dependencies:** Both COMPLETE
- BL-204 (hamburger menu) ✅
- BUG-029 (app-add flow) ✅

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts` (line 33 needs fix)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\MenuBar.tsx` (line 34 has focusedPaneId, check TODO)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx` (already enforces chrome:false)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\types.ts` (EggLayoutNode interface)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\eggToShell.showChrome.test.ts` (tests expect showChrome to work)

## Deliverables

### 1. Fix eggToShell.ts showChrome Reading
- [ ] Change line 33 from `chrome: true,` to read from `eggNode.showChrome`
- [ ] Default to `true` if `showChrome` is undefined
- [ ] Respect explicit `showChrome: false` from EGG config
- [ ] Also fix line 115 (fallback pane) to use same logic

### 2. Verify MenuBar Syndication
- [ ] Read MenuBar.tsx implementation (line 34 has focusedPaneId access)
- [ ] Check if active pane menu items already syndicate (Edit menu has conditional enable)
- [ ] **If already working:** Remove TODO comment, document how it works
- [ ] **If stubbed:** Complete the syndication (focused pane's menu items appear in master menu)

### 3. Runtime Verification
- [ ] Run existing tests to verify implementation matches test expectations
- [ ] Add integration test if missing: EGG with `showChrome: false` → renders without title bar
- [ ] Smoke test canvas.egg.md if it has `chrome: false` panes

### 4. Update EGG Type Definition (if needed)
- [ ] If `showChrome` field not in EggLayoutNode interface, add it
- [ ] Add JSDoc comment explaining default behavior

## Test Requirements

**Existing tests MUST pass:**
- [ ] `cd browser && npx vitest run src/shell/__tests__/eggToShell.showChrome.test.ts` (5 tests)
- [ ] `cd browser && npx vitest run src/shell/__tests__/showChrome.integration.test.tsx` (4 tests)
- [ ] `cd browser && npx vitest run src/shell/components/__tests__/PaneChrome.test.tsx` (47 tests)
- [ ] `cd browser && npx vitest run src/shell/__tests__/eggToShell.test.ts` (15 tests)

**Full suite:**
- [ ] `cd browser && npx vitest run` (all browser tests)

## Acceptance Criteria
- [ ] eggToShell.ts line 33 reads `showChrome` from EGG config, defaults to true
- [ ] eggToShell.ts line 115 uses same showChrome logic
- [ ] All 5 showChrome.test.ts tests pass
- [ ] All 4 showChrome.integration.test.tsx tests pass
- [ ] All 47 PaneChrome tests pass (no regression)
- [ ] MenuBar syndication verified as working OR completed
- [ ] No TODO comments in MenuBar.tsx or eggToShell.ts
- [ ] No hardcoded colors
- [ ] No files over 500 lines

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (no changes to CSS in this task, just verify)
- No stubs or TODO comments
- TDD: tests already exist, make them pass

## Expected Code Change (eggToShell.ts line 33)

**Current (WRONG):**
```typescript
chrome: true,
```

**Expected (CORRECT):**
```typescript
chrome: eggNode.showChrome !== undefined ? eggNode.showChrome as boolean : true,
```

**Also fix line 115 (fallback pane)** with same logic.

## MenuBar Syndication Guidance

Check MenuBar.tsx:
- Line 34 already has `focusedPaneId` from shell context
- Lines 241-257: Edit menu items already conditionally enable based on `isHivePaneActive`
- **Question:** Is this the "syndication" the spec requires, or is a full menu item registration system needed?
- **If existing implementation is sufficient:** Remove TODO, document it in response
- **If more is needed:** Implement pane menu item registration and syndication

## Response Requirements — MANDATORY

When you finish, write: `.deia/hive/responses/20260318-TASK-BL207-RUNTIME-VERIFY-RESPONSE.md`

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

## Model Assignment
sonnet

## Priority
P0
