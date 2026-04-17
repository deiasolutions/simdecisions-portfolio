# SPEC-HYG-008A-ts-2322

**Created:** 2026-04-14
**Author:** BEE-QUEUE-TEMP-SPEC-HYG-008-SPLIT-001
**Type:** HYGIENE — Fix TS2322 type assignment errors
**Status:** READY

---

## Priority
P2

## Depends On
None

## Model Assignment
haiku

## Objective

Fix TS2322 errors: "Type 'X' is not assignable to type 'Y'". This is the most common TypeScript error in the codebase.

**Current count:** 294 errors
**Target:** 147 errors (50% reduction)

This error occurs when attempting to assign a value to a variable, parameter, or property where the types don't match. Common causes:
- Incorrect mock object structures in tests
- Missing or incorrect type annotations
- Mismatched function return types
- Incorrect prop types in React components

## Files to Read First

Top 10 files with TS2322 errors (read these to understand patterns):
1. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/primitives/text-pane/__tests__/SDEditor.test.tsx` (39 errors)
2. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/primitives/text-pane/__tests__/SDEditor.efemera.test.tsx` (22 errors)
3. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/primitives/text-pane/__tests__/SDEditor.integration.test.tsx` (19 errors)
4. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/apps/sim/components/flow-designer/__tests__/annotation-nodes-rich.test.tsx` (19 errors)
5. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/apps/sim/components/flow-designer/nodes/__tests__/processFlowNodes.test.tsx` (16 errors)
6. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/apps/sim/components/flow-designer/NodePalette.tsx` (14 errors)
7. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/shell/reducer.ts` (13 errors)
8. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/apps/sim/components/flow-designer/modes/__tests__/SuggestionsTab.test.tsx` (11 errors)
9. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/shell/actions/lifecycle.ts` (10 errors)
10. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/primitives/menu-bar/MenuBarPrimitive.tsx` (10 errors)

## Strategy

1. **Focus on test files first** — Most TS2322 errors are in test files with incorrect mock structures
2. **Fix mock objects** — Ensure test mocks match the actual type definitions
3. **Update type annotations** — Add or correct type annotations where inferred types don't match
4. **Fix function return types** — Ensure functions return the types their signatures promise
5. **Prioritize high-error files** — Start with files that have >10 errors for maximum impact

## Acceptance Criteria

- [ ] TS2322 error count reduced from 294 to ≤147
- [ ] No new TypeScript errors introduced
- [ ] All existing tests still pass: `cd browser && npm test`
- [ ] No `@ts-ignore` or `as any` used
- [ ] Fixed root causes, not symptoms

## Smoke Test

```bash
cd browser && npx tsc --noEmit 2>&1 | grep -c "TS2322"
# Expected: ≤147 (down from 294)
```

## Constraints

- NO `@ts-ignore` — fix the actual type mismatch
- NO `as any` — provide correct types
- NO stubs — every fix must be complete
- Prefer fixing test mocks over changing production types (tests should match reality)
- No file over 500 lines (modularize if needed)
- If a mock object is wrong, fix the mock to match the real type — don't weaken the real type

## Response File

`.deia/hive/responses/YYYYMMDD-HYG-008A-TS2322-RESPONSE.md`

---

*SPEC-HYG-008A-ts-2322 — Q88N via BEE-SPLIT — 2026-04-14*
