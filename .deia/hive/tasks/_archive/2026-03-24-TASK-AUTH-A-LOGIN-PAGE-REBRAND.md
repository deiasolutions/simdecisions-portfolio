# TASK-AUTH-A: LoginPage rebrand — ra96it → hodeia

## Objective
Rebrand LoginPage.tsx from ra96it to hodeia: replace VITE_RA96IT_API env var with VITE_AUTH_API, update all UI text from "ra96it" to "hodeia" or neutral language, and update tests to verify new env var usage.

## Context
The LoginPage currently references `VITE_RA96IT_API` and displays "ra96it" branding throughout the UI (logo text, subtitles, logged-in messages). The OAuth flow itself is already domain-agnostic and works for any EGG. This task is purely branding: renaming the env var to be generic and replacing ra96it text with hodeia.

The goal is to make the auth system brand-neutral at the configuration level (using `VITE_AUTH_API` instead of `VITE_RA96IT_API`) while updating the visible UI text to reflect the new hodeia brand.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\LoginPage.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\authStore.test.ts` (for test patterns)

## Deliverables
- [ ] Replace `VITE_RA96IT_API` with `VITE_AUTH_API` in LoginPage.tsx
- [ ] Update all UI text: "ra96it" → "hodeia" (logo text, subtitles, logged-in messages)
- [ ] Keep GitHub branding and consent flow unchanged (these are product-neutral)
- [ ] Update LoginPage tests to verify new env var name
- [ ] Add test cases verifying UI displays "hodeia" instead of "ra96it"

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing LoginPage tests pass with new env var
- [ ] Add test case: verify `VITE_AUTH_API` is used in API calls
- [ ] Add test case: verify UI text contains "hodeia" not "ra96it"
- [ ] Edge case: env var not set → should fall back to empty string (existing behavior)

## Constraints
- No file over 500 lines (LoginPage.tsx is 276 lines, test file will be under 300)
- CSS: `var(--sd-*)` only (no style changes expected, but if any, follow this)
- No stubs
- Do NOT change the OAuth flow logic — only env var name and UI text
- Do NOT change localStorage keys (that's TASK-AUTH-B)

## Acceptance Criteria
1. [ ] `VITE_RA96IT_API` replaced with `VITE_AUTH_API` in LoginPage.tsx
2. [ ] All instances of "ra96it" in UI text replaced with "hodeia" or neutral language
3. [ ] GitHub branding unchanged (GitHub OAuth is product-neutral)
4. [ ] Tests pass: existing + new test cases for env var and UI text
5. [ ] No references to `VITE_RA96IT_API` remain in LoginPage.tsx or its tests

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-AUTH-A-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
