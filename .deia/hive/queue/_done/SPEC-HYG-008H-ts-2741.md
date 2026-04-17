# SPEC-HYG-008H-ts-2741

**Spec ID:** SPEC-HYG-008H-ts-2741
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

Fix TS2741 errors: "Property 'X' is missing in type 'Y' but required in type 'Z'."

**Current count:** 16
**Target:** 8 or fewer (50% reduction)

TS2741 occurs when an object literal is missing required properties. This is similar to TS2739 and TS2740 but specifically applies to object literals.

**Note:** The original SPEC-HYG-008 reduced this from 32 to 16, so we're picking up where it left off.

Common causes:
- Object literals missing required fields
- Test mock data incomplete
- Config objects missing properties
- State objects missing required fields

---

## Files to Read First

Run this command to identify the files with TS2741 errors:

```bash
cd browser && npx tsc --noEmit 2>&1 | grep "TS2741" | cut -d'(' -f1 | sort | uniq -c | sort -rn | head -10
```

Then read the top 5-8 files identified.

---

## Strategy

1. **Identify missing properties** — TypeScript error messages list exactly which properties are missing
2. **Add required properties** — Provide appropriate values in object literals
3. **Check type definitions** — Verify what properties are actually required
4. **Update test fixtures** — Ensure test data includes all required fields

**Common fixes:**
- Add missing properties to object literals
- Update test mock data to include all required fields
- Complete config objects
- Ensure all required state fields are initialized

**DO NOT:**
- Use `Partial<T>` to make properties optional
- Use `@ts-ignore` to suppress errors
- Use `as any` to bypass checking
- Make properties optional in type definitions unless they truly are optional

**PREFER:**
- Adding all required properties with sensible values
- Creating complete object literals
- Using helper functions to create valid objects
- Updating test fixtures to match production types

---

## Acceptance Criteria

- [ ] TS2741 error count reduced from 16 to 8 or fewer (50% reduction)
- [ ] No new TypeScript errors introduced (any category)
- [ ] All modified files still pass their tests
- [ ] All object literals include required properties
- [ ] No use of `@ts-ignore`, `Partial<T>` shortcuts, or `as any`
- [ ] No files exceed 500 lines

---

## Smoke Test

```bash
cd browser && npx tsc --noEmit 2>&1 | grep -c "TS2741"
# Expected: <= 8
```

---

## Constraints

- **No `@ts-ignore`** — Add the missing properties
- **No `as any`** — Use complete types
- **No stubs** — Every fix must be complete
- **Add all required fields** — Don't use `Partial<T>` to shortcut
- **Complete object literals** — Ensure all required properties are present
- **No file over 500 lines** — Modularize if needed
- **Tests must pass** — Run test suite for modified files

---

## Response File

`C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\responses\20260414-HYG-008H-TS2741-RESPONSE.md`

---

*SPEC-HYG-008H-ts-2741 — Q88NR — 2026-04-14*
