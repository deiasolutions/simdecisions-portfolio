# SPEC-HYG-008I-ts-2353

**Spec ID:** SPEC-HYG-008I-ts-2353
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

Fix TS2353 errors: "Object literal may only specify known properties, and 'X' does not exist in type 'Y'."

**Current count:** 15
**Target:** 7 or fewer (50% reduction)

TS2353 occurs when an object literal includes properties that aren't defined in the target type. This is TypeScript's excess property checking preventing typos and accidental extra data.

Common causes:
- Typos in property names
- Extra properties that shouldn't be there
- Properties that were removed from the type definition
- Type definitions that are too narrow

---

## Files to Read First

Run this command to identify the files with TS2353 errors:

```bash
cd browser && npx tsc --noEmit 2>&1 | grep "TS2353" | cut -d'(' -f1 | sort | uniq -c | sort -rn | head -10
```

Then read the top 5-8 files identified.

---

## Strategy

1. **Check property names** — Many errors are simply typos
2. **Remove extra properties** — Delete properties that don't belong
3. **Check type definitions** — Verify if the property should exist
4. **Update to renamed properties** — Some properties may have been renamed

**Common fixes:**
- Fix typos in property names (e.g., `backgroundColor` vs `background-color`)
- Remove properties that don't belong in the type
- Update to use renamed properties
- Only add to type definitions if the property truly should exist

**DO NOT:**
- Add arbitrary properties to type definitions just to silence errors
- Use `@ts-ignore` to suppress errors
- Use type assertions to bypass checking
- Make types too permissive (e.g., `[key: string]: any`)

**PREFER:**
- Fixing typos in property names
- Removing extra properties
- Using correct property names
- Only modifying type definitions when truly needed

---

## Acceptance Criteria

- [ ] TS2353 error count reduced from 15 to 7 or fewer (50% reduction)
- [ ] No new TypeScript errors introduced (any category)
- [ ] All modified files still pass their tests
- [ ] Property names are correct and consistent
- [ ] No use of `@ts-ignore` or `as any`
- [ ] Type definitions not polluted with unnecessary properties
- [ ] No files exceed 500 lines

---

## Smoke Test

```bash
cd browser && npx tsc --noEmit 2>&1 | grep -c "TS2353"
# Expected: <= 7
```

---

## Constraints

- **No `@ts-ignore`** — Fix the property name or remove it
- **No `as any`** — Use proper types
- **No stubs** — Every fix must be complete
- **Fix usage first** — Don't modify type definitions unless necessary
- **Don't pollute types** — Don't add properties that shouldn't exist
- **No file over 500 lines** — Modularize if needed
- **Tests must pass** — Run test suite for modified files

---

## Response File

`C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\responses\20260414-HYG-008I-TS2353-RESPONSE.md`

---

*SPEC-HYG-008I-ts-2353 — Q88NR — 2026-04-14*
