# SPEC-HYG-008D-ts-2740

**Spec ID:** SPEC-HYG-008D-ts-2740
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

Fix TS2740 errors: "Type 'X' is missing the following properties from type 'Y': ..."

**Current count:** 29
**Target:** 14 or fewer (50% reduction)

TS2740 occurs when assigning an object that's missing required properties from the target type. This is similar to TS2741 but applies to type assignments rather than object literals.

Common causes:
- Incomplete object creation in tests
- Missing fields when creating state objects
- Partial objects passed where complete ones are expected

---

## Files to Read First

Top 5 files by TS2740 error count:

1. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\components\__tests__\Shell.responsive.test.tsx` (12 errors)
2. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\components\__tests__\Shell.settings.test.tsx` (7 errors)
3. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\components\__tests__\ShellChromeIntegration.test.tsx` (6 errors)
4. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\components\__tests__\Shell.legacy-cleanup.test.tsx` (3 errors)
5. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\components\__tests__\Shell.test.tsx` (1 error)

**Pattern:** ALL errors are in Shell component test files. These are test state objects missing required fields.

---

## Strategy

1. **Focus on Shell test files** — All errors are concentrated in 5 test files
2. **Identify missing properties** — TypeScript error messages list exactly which properties are missing
3. **Add missing fields to test mocks** — Provide sensible default values for test scenarios
4. **Check for recent type changes** — Some properties may be newly required post-flatten

**Common patterns:**
- Test state objects missing newly required fields
- Mock objects that were valid pre-flatten but now incomplete
- Partial state creation in test setup

**DO NOT:**
- Use `Partial<T>` to make all properties optional
- Use type assertions to bypass checking
- Use `@ts-ignore`

**PREFER:**
- Adding all required properties to test mocks
- Using complete state objects in tests
- Creating test helper functions for common mock objects

---

## Acceptance Criteria

- [ ] TS2740 error count reduced from 29 to 14 or fewer (50% reduction)
- [ ] No new TypeScript errors introduced (any category)
- [ ] All modified test files pass their tests
- [ ] Test mocks include all required properties
- [ ] No use of `@ts-ignore`, `Partial<T>` shortcuts, or `as any`
- [ ] No files exceed 500 lines

---

## Smoke Test

```bash
cd browser && npx tsc --noEmit 2>&1 | grep -c "TS2740"
# Expected: <= 14
```

---

## Constraints

- **No `@ts-ignore`** — Add the missing properties
- **No `as any`** — Use complete types
- **No stubs** — Every fix must be complete
- **Add all required fields** — Don't use `Partial<T>` to shortcut
- **Tests must be meaningful** — Don't just add empty/null values; use sensible defaults
- **No file over 500 lines** — Modularize if needed
- **Tests must pass** — Run test suite for modified files

---

## Response File

`C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\responses\20260414-HYG-008D-TS2740-RESPONSE.md`

---

*SPEC-HYG-008D-ts-2740 — Q88NR — 2026-04-14*
