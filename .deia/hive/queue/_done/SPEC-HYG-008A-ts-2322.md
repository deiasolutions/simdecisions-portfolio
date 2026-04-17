# SPEC-HYG-008A-ts-2322

**Spec ID:** SPEC-HYG-008A-ts-2322
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

Fix TS2322 errors: "Type 'X' is not assignable to type 'Y'."

**Current count:** 195
**Target:** 97 or fewer (50% reduction)

This is the most common TypeScript error in the codebase. TS2322 occurs when a value of one type is assigned to a variable, property, or parameter expecting a different type.

Common patterns:
- Incorrect literal types (e.g., `number` assigned to `string`)
- Missing or extra properties in object types
- Enum vs string literal mismatches
- Incompatible union types

---

## Files to Read First

Top 10 files by TS2322 error count:

1. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\apps\sim\components\flow-designer\__tests__\annotation-nodes-rich.test.tsx` (19 errors)
2. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\apps\sim\components\flow-designer\nodes\__tests__\processFlowNodes.test.tsx` (16 errors)
3. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\apps\sim\components\flow-designer\NodePalette.tsx` (14 errors)
4. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\reducer.ts` (12 errors)
5. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\primitives\menu-bar\MenuBarPrimitive.tsx` (10 errors)
6. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\primitives\canvas\CanvasApp.tsx` (9 errors)
7. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\primitives\conversation-pane\__tests__\ConversationPane.e2e.test.tsx` (8 errors)
8. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\apps\sim\adapters\playbackControlsPaneAdapter.tsx` (7 errors)
9. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\apps\__tests__\efemera.channels.integration.test.tsx` (7 errors)
10. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\actions\lifecycle.ts` (6 errors)

---

## Strategy

1. **Start with test files** — Fix test mocks and assertions before production code
2. **Fix literal type mismatches** — These are mechanical (number vs string, etc.)
3. **Fix object shape mismatches** — Add/remove properties to match interfaces
4. **Verify no new errors introduced** — Run `npx tsc --noEmit` after each file

**DO NOT:**
- Use `@ts-ignore` or `@ts-expect-error`
- Use `as any` or type assertions to silence errors
- Create overly broad union types as shortcuts
- Modify type definitions unless absolutely necessary (prefer fixing usage)

**PREFER:**
- Fixing test mock data to match actual types
- Correcting literal values (e.g., string to number)
- Adding missing properties to object literals
- Narrowing types where appropriate

---

## Acceptance Criteria

- [ ] TS2322 error count reduced from 195 to 97 or fewer (50% reduction)
- [ ] No new TypeScript errors introduced (any category)
- [ ] All modified files still pass their tests
- [ ] No use of `@ts-ignore`, `@ts-expect-error`, or `as any`
- [ ] No files exceed 500 lines

---

## Smoke Test

```bash
cd browser && npx tsc --noEmit 2>&1 | grep -c "TS2322"
# Expected: <= 97
```

---

## Constraints

- **No `@ts-ignore`** — Fix the root cause
- **No `as any`** — Properly type the value
- **No stubs** — Every fix must be complete
- **Fix root cause** — Don't just change types to silence errors
- **Prefer fixing test mocks** — Tests should match production types, not vice versa
- **No file over 500 lines** — Modularize if needed
- **Tests must pass** — Run test suite for modified files

---

## Response File

`C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\responses\20260414-HYG-008A-TS2322-RESPONSE.md`

---

*SPEC-HYG-008A-ts-2322 — Q88NR — 2026-04-14*
