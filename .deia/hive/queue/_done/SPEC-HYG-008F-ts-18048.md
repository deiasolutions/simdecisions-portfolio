# SPEC-HYG-008F-ts-18048

**Spec ID:** SPEC-HYG-008F-ts-18048
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

Fix TS18048 errors: "'X' is possibly 'undefined'."

**Current count:** 27
**Target:** 13 or fewer (50% reduction)

TS18048 occurs when accessing a value that might be undefined without proper null checking. This is TypeScript's strict null checking at work, preventing potential runtime errors.

Common causes:
- Accessing array elements without bounds checking
- Using optional properties without checking if they exist
- Using nullish values without guards
- Accessing properties of potentially undefined objects

---

## Files to Read First

Top 5 files by TS18048 error count:

1. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\types\__tests__\ir.test.ts` (17 errors)
2. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\apps\sim\components\flow-designer\playback\__tests__\playback-backend.test.tsx` (4 errors)
3. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\primitives\top-bar\__tests__\TopBar.test.tsx` (3 errors)
4. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\sets\__tests__\sdkExamples.test.ts` (2 errors)
5. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\apps\sim\components\flow-designer\useNodeEditing.ts` (1 error)

**Pattern:** 17 errors concentrated in `ir.test.ts` — likely accessing test data without null checks.

---

## Strategy

1. **Start with ir.test.ts** — 17 errors (63% of total) in one file
2. **Add null checks** — Use optional chaining (`?.`) or explicit checks
3. **Use nullish coalescing** — Provide defaults with `??`
4. **Assert non-null in tests** — Use `!` operator ONLY in test files where you control the data
5. **Add guards in production code** — Never use `!` in production; use proper guards

**Common patterns in tests:**
- Array access: `array[0]` → add assertion `expect(array.length).toBeGreaterThan(0)` first
- Property access: `obj.prop` → use `obj?.prop` or check `if (obj.prop)`
- Test data: In tests only, use `!` after verifying the value exists in an assertion

**Common patterns in production:**
- Optional chaining: `value?.property`
- Nullish coalescing: `value ?? defaultValue`
- Type guards: `if (value !== undefined) { ... }`
- Early returns: `if (!value) return;`

**DO NOT:**
- Use `!` (non-null assertion) in production code
- Use `@ts-ignore` to suppress warnings
- Remove necessary null checks

**PREFER:**
- Optional chaining and nullish coalescing
- Explicit null/undefined checks
- Early returns for guard clauses
- In tests: assertions before `!` usage

---

## Acceptance Criteria

- [ ] TS18048 error count reduced from 27 to 13 or fewer (50% reduction)
- [ ] No new TypeScript errors introduced (any category)
- [ ] All modified files still pass their tests
- [ ] No use of `!` in production code (tests OK with proper assertions)
- [ ] No use of `@ts-ignore` or `as any`
- [ ] No files exceed 500 lines

---

## Smoke Test

```bash
cd browser && npx tsc --noEmit 2>&1 | grep -c "TS18048"
# Expected: <= 13
```

---

## Constraints

- **No `@ts-ignore`** — Add proper null checks
- **No `!` in production code** — Use optional chaining or guards
- **`!` in tests OK** — But only after assertions that verify the value exists
- **No stubs** — Every fix must be complete
- **Prefer optional chaining** — `value?.prop` over `value && value.prop`
- **No file over 500 lines** — Modularize if needed
- **Tests must pass** — Run test suite for modified files

---

## Response File

`C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\responses\20260414-HYG-008F-TS18048-RESPONSE.md`

---

*SPEC-HYG-008F-ts-18048 — Q88NR — 2026-04-14*
