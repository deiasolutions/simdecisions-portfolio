# SPEC-HYG-008B-ts-2304

**Spec ID:** SPEC-HYG-008B-ts-2304
**Created:** 2026-04-14
**Author:** Q88NR (via BEE split from SPEC-HYG-008)
**Type:** HYGIENE — TypeScript error reduction
**Status:** READY

---

## Priority
P2

## Depends On
None

## Model Assignment
haiku

## Objective

Fix TS2304 errors: "Cannot find name 'X'."

**Current count:** 65
**Target:** 32 or fewer (50% reduction)

TS2304 occurs when TypeScript cannot find a referenced identifier. This usually means:
- Missing imports
- Undefined variables
- Typos in identifiers
- Incorrect scope references
- Missing type definitions

---

## Files to Read First

Top 10 files by TS2304 error count:

1. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\components\__tests__\GestureLayer.test.tsx` (7 errors)
2. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\components\__tests__\WorkspaceBar.test.tsx` (6 errors)
3. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\components\__tests__\PaneChrome.e2e.test.tsx` (6 errors)
4. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\components\__tests__\ShellNodeRenderer.drag-to-cold.test.tsx` (4 errors)
5. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\components\__tests__\Shell.responsive.test.tsx` (4 errors)
6. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\components\__tests__\FloatPaneWrapper.test.tsx` (4 errors)
7. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\components\__tests__\TripleSplitContainer.test.tsx` (3 errors)
8. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\components\__tests__\SplitTree.test.tsx` (3 errors)
9. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\components\__tests__\SplitDivider.test.tsx` (3 errors)
10. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\components\__tests__\Shell.test.tsx` (3 errors)

**Pattern:** Most TS2304 errors are in test files in `shell/components/__tests__/`. Common missing names: `ShellNodeType`, `LoadState`, `container`.

---

## Strategy

1. **Check for missing imports** — Most TS2304 errors are just missing import statements
2. **Verify type definitions exist** — Look for enums and types that should be imported
3. **Fix test file references** — Many errors reference `container` or other test variables
4. **Check for renamed exports** — Post-flatten, some exports may have moved

**Common fixes:**
- Add missing `import { ShellNodeType } from '../types'`
- Add missing `import { LoadState } from '../types'`
- Fix undefined test variables like `container`
- Import types from correct post-flatten paths

**DO NOT:**
- Declare variables as `any` to silence errors
- Comment out failing code
- Use `@ts-ignore`

**PREFER:**
- Adding proper imports
- Defining missing test variables
- Using correct import paths post-flatten

---

## Acceptance Criteria

- [ ] TS2304 error count reduced from 65 to 32 or fewer (50% reduction)
- [ ] No new TypeScript errors introduced (any category)
- [ ] All modified files still pass their tests
- [ ] All imports use correct post-flatten paths
- [ ] No use of `@ts-ignore` or `any`
- [ ] No files exceed 500 lines

---

## Smoke Test

```bash
cd browser && npx tsc --noEmit 2>&1 | grep -c "TS2304"
# Expected: <= 32
```

---

## Constraints

- **No `@ts-ignore`** — Fix the root cause
- **No `any`** — Properly import or define the type
- **No stubs** — Every fix must be complete
- **Fix imports first** — Most errors are just missing imports
- **Use correct post-flatten paths** — No references to old `packages/` structure
- **No file over 500 lines** — Modularize if needed
- **Tests must pass** — Run test suite for modified files

---

## Response File

`C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\responses\20260414-HYG-008B-TS2304-RESPONSE.md`

---

*SPEC-HYG-008B-ts-2304 — Q88NR — 2026-04-14*
