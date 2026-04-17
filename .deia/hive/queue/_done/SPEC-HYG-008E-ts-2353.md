# SPEC-HYG-008E-ts-2353

**Created:** 2026-04-14
**Author:** BEE-QUEUE-TEMP-SPEC-HYG-008-SPLIT-001
**Type:** HYGIENE — Fix TS2353 unknown property errors
**Status:** READY

---

## Priority
P2

## Depends On
None

## Model Assignment
haiku

## Objective

Fix TS2353 errors: "Object literal may only specify known properties, and 'X' does not exist in type 'Y'". This error indicates object literals with extra/unknown properties.

**Current count:** 64 errors
**Target:** 32 errors (50% reduction)

This error occurs when creating objects with properties that aren't defined in the target type. Common causes:
- Test mocks with extra properties not in interface
- Typos in property names
- Properties that were removed from type but still used
- Incorrect object shape assumptions

## Files to Read First

Top 10 files with TS2353 errors (read these to understand patterns):
1. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/primitives/conversation-pane/__tests__/ConversationPane.test.tsx` (18 errors)
2. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/apps/__tests__/efemera.channels.integration.test.tsx` (12 errors)
3. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/shell/components/__tests__/GovernanceProxy.test.tsx` (10 errors)
4. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/primitives/conversation-pane/__tests__/ConversationPane.e2e.test.tsx` (6 errors)
5. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/apps/sim/adapters/__tests__/simProgressPaneAdapter.test.tsx` (4 errors)
6. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/__tests__/smoke.test.tsx` (2 errors)
7. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/shell/components/ImmersiveNavigator.tsx` (1 error)
8. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/shell/components/__tests__/ShellChromeIntegration.test.tsx` (1 error)
9. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/shell/__tests__/reducer.lifecycle-events.test.ts` (1 error)
10. `/c/Users/davee/OneDrive/Documents/GitHub/simdecisions/browser/src/primitives/toolbar/FloatingToolbar.tsx` (1 error)

## Strategy

1. **Focus on ConversationPane tests** — 18 errors suggests mock messages have extra properties
2. **Remove extra properties** — Delete properties that don't exist in the target type
3. **Fix typos** — Check for misspelled property names
4. **Update type definitions** — If property should exist, add it to the interface (only if legitimate)
5. **Verify against actual interfaces** — Read the type definition to see what properties are valid

## Acceptance Criteria

- [ ] TS2353 error count reduced from 64 to ≤32
- [ ] No new TypeScript errors introduced
- [ ] All existing tests still pass: `cd browser && npm test`
- [ ] No `@ts-ignore` or `as any` used
- [ ] Object literals only contain known properties from their types

## Smoke Test

```bash
cd browser && npx tsc --noEmit 2>&1 | grep -c "TS2353"
# Expected: ≤32 (down from 64)
```

## Constraints

- NO `@ts-ignore` — remove the extra property or add it to the type definition
- NO `as any` — use correct object shape
- NO stubs — every fix must be complete
- Prefer removing extra properties over adding to interface (tests should match reality)
- No file over 500 lines (modularize if needed)
- Only add properties to interfaces if they're genuinely needed by production code

## Response File

`.deia/hive/responses/YYYYMMDD-HYG-008E-TS2353-RESPONSE.md`

---

*SPEC-HYG-008E-ts-2353 — Q88N via BEE-SPLIT — 2026-04-14*
