# SPEC-HYG-008D-ts-2741

**Created:** 2026-04-14
**Author:** BEE-QUEUE-TEMP-SPEC-HYG-008-SPLIT-001
**Type:** HYGIENE — Fix TS2741 missing property errors
**Status:** READY

---

## Priority
P2

## Depends On
None

## Model Assignment
haiku

## Objective

Fix TS2741 errors: "Property 'X' is missing in type 'Y' but required in type 'Z'". This error indicates object literals missing required properties.

**Current count:** 77 errors
**Target:** 38 errors (50% reduction)

This error occurs when creating objects that don't include all required properties. Common causes:
- Incomplete mock objects in tests
- Missing required fields when creating instances
- Partial type usage where full type expected
- Object literals missing newly added required fields

## Files to Read First

Top 10 files with TS2741 errors (read these to understand patterns):
1. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/shell/__tests__/utils.test.ts` (16 errors)
2. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/shell/components/__tests__/MaximizedOverlay.test.tsx` (10 errors)
3. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/sets/__tests__/eggWiring.test.ts` (6 errors)
4. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/primitives/tree-browser/__tests__/volume-integration.test.tsx` (6 errors)
5. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/shell/components/__tests__/PaneMenu.test.tsx` (4 errors)
6. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/shell/components/__tests__/PaneChrome.e2e.test.tsx` (4 errors)
7. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/sets/__tests__/index.test.ts` (4 errors)
8. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/primitives/text-pane/__tests__/SDEditor.fileLoading.test.tsx` (4 errors)
9. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/shell/__tests__/moveAppOntoOccupied.test.ts` (3 errors)
10. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/shell/components/__tests__/WorkspaceBar.test.tsx` (2 errors)

## Strategy

1. **Focus on test utils** — 16 errors in utils.test.ts suggests incomplete test helper objects
2. **Add missing properties to mocks** — Complete all mock object structures
3. **Use correct builder patterns** — If builder/factory functions exist, use them instead of raw objects
4. **Identify common missing fields** — Look for patterns in which properties are missing
5. **Prefer complete objects** — Don't use `Partial<T>` where full `T` is required

## Acceptance Criteria

- [ ] TS2741 error count reduced from 77 to ≤38
- [ ] No new TypeScript errors introduced
- [ ] All existing tests still pass: `cd browser && npm test`
- [ ] No `@ts-ignore` or `as any` used
- [ ] All required properties present in object literals and mocks

## Smoke Test

```bash
cd browser && npx tsc --noEmit 2>&1 | grep -c "TS2741"
# Expected: ≤38 (down from 77)
```

## Constraints

- NO `@ts-ignore` — add the missing required property
- NO `as any` — provide complete object with all required fields
- NO stubs — every fix must be complete
- Prefer adding missing properties over making them optional (tests should be complete)
- No file over 500 lines (modularize if needed)
- Use default/sensible values for test data (e.g., empty string for required string fields)

## Response File

`.deia/hive/responses/YYYYMMDD-HYG-008D-TS2741-RESPONSE.md`

---

*SPEC-HYG-008D-ts-2741 — Q88N via BEE-SPLIT — 2026-04-14*
