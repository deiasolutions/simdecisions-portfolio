# SPEC-HYG-008E-ts-2339

**Spec ID:** SPEC-HYG-008E-ts-2339
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

Fix TS2339 errors: "Property 'X' does not exist on type 'Y'."

**Current count:** 28
**Target:** 14 or fewer (50% reduction)

TS2339 occurs when trying to access a property that TypeScript doesn't know exists on the type. This usually means:
- Typo in property name
- Property was removed/renamed
- Accessing property that doesn't exist on all union members
- Type definition is incomplete

---

## Files to Read First

Top 8 files by TS2339 error count:

1. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\primitives\canvas\CanvasApp.tsx` (10 errors)
2. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\apps\sim\components\flow-designer\__tests__\ir-deposit-integration.test.tsx` (6 errors)
3. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\__tests__\eggToShell.multiChild.test.ts` (5 errors)
4. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\components\__tests__\Shell.compact.test.tsx` (3 errors)
5. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\actions\layout.ts` (1 error)
6. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\primitives\status-bar\StatusBar.tsx` (1 error)
7. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\primitives\settings\settingsStore.ts` (1 error)
8. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\apps\sim\components\flow-designer\useNodeEditing.ts` (1 error)

**Pattern:** 10 errors in `CanvasApp.tsx`, likely accessing properties that don't exist on all canvas event types or node types.

---

## Strategy

1. **Start with CanvasApp.tsx** — 10 errors concentrated in one file
2. **Check property names** — Verify spelling and case
3. **Check type definitions** — Look for properties that were renamed or removed
4. **Handle union types** — Use type guards to narrow unions before accessing properties
5. **Check post-flatten changes** — Some properties may have moved or been renamed

**Common fixes:**
- Add type guards before accessing union-specific properties
- Fix typos in property names
- Update to use renamed properties
- Add missing properties to type definitions (only if truly needed)

**DO NOT:**
- Use `as any` to access arbitrary properties
- Use `@ts-ignore` to suppress errors
- Add properties to types without verifying they should exist

**PREFER:**
- Type narrowing with type guards
- Fixing typos
- Using correct property names
- Accessing only properties that exist on the type

---

## Acceptance Criteria

- [ ] TS2339 error count reduced from 28 to 14 or fewer (50% reduction)
- [ ] No new TypeScript errors introduced (any category)
- [ ] All modified files still pass their tests
- [ ] Type guards used where appropriate for union types
- [ ] No use of `@ts-ignore` or `as any`
- [ ] No files exceed 500 lines

---

## Smoke Test

```bash
cd browser && npx tsc --noEmit 2>&1 | grep -c "TS2339"
# Expected: <= 14
```

---

## Constraints

- **No `@ts-ignore`** — Fix the property access
- **No `as any`** — Use proper type narrowing
- **No stubs** — Every fix must be complete
- **Use type guards** — Narrow unions before accessing specific properties
- **Don't add fake properties** — Only fix usage, don't pollute type definitions
- **No file over 500 lines** — Modularize if needed
- **Tests must pass** — Run test suite for modified files

---

## Response File

`C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\responses\20260414-HYG-008E-TS2339-RESPONSE.md`

---

*SPEC-HYG-008E-ts-2339 — Q88NR — 2026-04-14*
