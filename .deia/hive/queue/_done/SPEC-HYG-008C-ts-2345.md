# SPEC-HYG-008C-ts-2345

**Spec ID:** SPEC-HYG-008C-ts-2345
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

Fix TS2345 errors: "Argument of type 'X' is not assignable to parameter of type 'Y'."

**Current count:** 60
**Target:** 30 or fewer (50% reduction)

TS2345 occurs when a function is called with arguments that don't match the function signature. This usually means:
- Wrong argument type passed to function
- Missing required properties in object arguments
- Extra properties in object arguments
- Incorrect number of arguments

---

## Files to Read First

Top 10 files by TS2345 error count:

1. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\apps\sim\components\flow-designer\__tests__\useNodeEditing.propertyChanged.test.ts` (9 errors)
2. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\primitives\canvas\CanvasApp.tsx` (8 errors)
3. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\actions\lifecycle.ts` (7 errors)
4. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\reducer.ts` (6 errors)
5. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\primitives\terminal\__tests__\useTerminal.chatPersist.test.ts` (6 errors)
6. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\primitives\canvas\__tests__\canvasDragIsolation.test.tsx` (6 errors)
7. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\primitives\apps-home\__tests__\AppsHome.test.tsx` (4 errors)
8. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\primitives\queue-pane\TaskContextMenu.tsx` (3 errors)
9. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\shell\actions\layout.ts` (2 errors)
10. `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\browser\src\primitives\terminal\TerminalApp.tsx` (2 errors)

**Pattern:** Many errors in test files (especially `useNodeEditing.propertyChanged.test.ts`) where mock objects don't match function signatures.

---

## Strategy

1. **Fix test mocks first** — Update mock objects to match actual function signatures
2. **Check function signatures** — Verify what types are actually expected
3. **Add missing properties** — Many errors are object arguments missing required fields
4. **Remove extra properties** — Some errors are extra fields in object arguments
5. **Fix type mismatches** — Correct cases where wrong primitive type is passed

**Common patterns:**
- Test mocks for `UseNodeEditingParams` missing required fields
- DOM elements typed as `Element` instead of `HTMLElement`
- Object arguments missing new required properties

**DO NOT:**
- Use type assertions (`as`) to bypass type checking
- Use `@ts-ignore` or `@ts-expect-error`
- Change function signatures to accept `any`

**PREFER:**
- Fixing the call site to pass correct arguments
- Updating test mocks to include all required fields
- Using proper TypeScript types throughout

---

## Acceptance Criteria

- [ ] TS2345 error count reduced from 60 to 30 or fewer (50% reduction)
- [ ] No new TypeScript errors introduced (any category)
- [ ] All modified files still pass their tests
- [ ] Test mocks properly match production types
- [ ] No use of `@ts-ignore`, `@ts-expect-error`, or `as any`
- [ ] No files exceed 500 lines

---

## Smoke Test

```bash
cd browser && npx tsc --noEmit 2>&1 | grep -c "TS2345"
# Expected: <= 30
```

---

## Constraints

- **No `@ts-ignore`** — Fix the function call arguments
- **No `as any`** — Use proper types
- **No stubs** — Every fix must be complete
- **Fix call sites** — Update arguments to match signatures
- **Prefer fixing test mocks** — Tests should match production signatures
- **No file over 500 lines** — Modularize if needed
- **Tests must pass** — Run test suite for modified files

---

## Response File

`C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\responses\20260414-HYG-008C-TS2345-RESPONSE.md`

---

*SPEC-HYG-008C-ts-2345 — Q88NR — 2026-04-14*
