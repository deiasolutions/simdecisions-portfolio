# SPEC-HYG-008G-ts-2739

**Spec ID:** SPEC-HYG-008G-ts-2739
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

Fix TS2739 errors: "Type 'X' is missing the following properties from type 'Y': ..."

**Current count:** 20
**Target:** 10 or fewer (50% reduction)

TS2739 is similar to TS2740 and TS2741 but occurs in different contexts - typically when a type lacks required properties when implementing an interface or extending a type.

Common causes:
- Incomplete interface implementations
- Missing properties in type definitions
- Object literals missing required fields
- Mock objects in tests missing properties

---

## Files to Read First

Run this command to identify the files with TS2739 errors:

```bash
cd browser && npx tsc --noEmit 2>&1 | grep "TS2739" | cut -d'(' -f1 | sort | uniq -c | sort -rn | head -10
```

Then read the top 5-8 files identified.

---

## Strategy

1. **Identify missing properties** — TypeScript error messages list exactly which properties are missing
2. **Add required properties** — Provide appropriate values for all required fields
3. **Check interface definitions** — Verify what the interface actually requires
4. **Update test mocks** — Ensure test objects match production types

**Common fixes:**
- Add all required properties to object literals
- Complete interface implementations
- Update test mocks to include newly required fields
- Ensure types match their definitions

**DO NOT:**
- Use `Partial<T>` to make properties optional
- Use `@ts-ignore` to suppress errors
- Use `as any` to bypass checking

**PREFER:**
- Adding all required properties with sensible values
- Creating complete type implementations
- Updating test fixtures to match production types

---

## Acceptance Criteria

- [ ] TS2739 error count reduced from 20 to 10 or fewer (50% reduction)
- [ ] No new TypeScript errors introduced (any category)
- [ ] All modified files still pass their tests
- [ ] All types properly implement their interfaces
- [ ] No use of `@ts-ignore`, `Partial<T>` shortcuts, or `as any`
- [ ] No files exceed 500 lines

---

## Smoke Test

```bash
cd browser && npx tsc --noEmit 2>&1 | grep -c "TS2739"
# Expected: <= 10
```

---

## Constraints

- **No `@ts-ignore`** — Add the missing properties
- **No `as any`** — Use complete types
- **No stubs** — Every fix must be complete
- **Add all required fields** — Don't use `Partial<T>` to shortcut
- **Complete implementations** — Ensure all interface requirements are met
- **No file over 500 lines** — Modularize if needed
- **Tests must pass** — Run test suite for modified files

---

## Response File

`C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\responses\20260414-HYG-008G-TS2739-RESPONSE.md`

---

*SPEC-HYG-008G-ts-2739 — Q88NR — 2026-04-14*
