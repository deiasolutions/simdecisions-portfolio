# BRIEFING: AUTH-A — LoginPage Rebrand from ra96it to hodeia

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Regent)
**Date:** 2026-03-24
**Priority:** P1
**Model Assignment:** haiku

---

## Objective

Rebrand LoginPage.tsx from ra96it branding to hodeia branding. This is a pure branding change: rename the environment variable from `VITE_RA96IT_API` to `VITE_AUTH_API` (generic), and replace all UI text references to "ra96it" with "hodeia" or neutral language.

## Context

The LoginPage currently uses:
- Environment variable: `VITE_RA96IT_API` (line 23)
- UI branding: "ra96it" appears 4 times in the UI (lines 158, 178, 194)
- localStorage keys: `ra96it_token` and `ra96it_user` (authStore.test.ts, lines 12-13)

**IMPORTANT:** This spec is ONLY for LoginPage.tsx changes. The localStorage keys will be handled in a separate spec (AUTH-B). Do NOT change localStorage keys in this task.

The OAuth flow is already domain-agnostic (GitHub-based). This is purely cosmetic: env var name + UI text.

## Files to Read

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\LoginPage.tsx` (275 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\authStore.test.ts` (136 lines, for reference only)

## Deliverables Required

Your bee must deliver:

1. **LoginPage.tsx changes:**
   - Line 23: Replace `VITE_RA96IT_API` with `VITE_AUTH_API`
   - Line 158: Replace "ra96it" with "hodeia"
   - Line 178: Replace "ra96it" with "hodeia"
   - Line 194: Replace "ra96it" with "hodeia"
   - GitHub branding (badge, logo, consent) unchanged
   - OAuth flow logic unchanged

2. **Test coverage:**
   - Create `LoginPage.test.tsx` in `__tests__/` directory
   - Test 1: Verify `VITE_AUTH_API` env var is used correctly
   - Test 2: Verify UI displays "hodeia" instead of "ra96it"
   - Test 3: Verify logged-in state displays "hodeia" branding
   - Test 4: Verify GitHub branding remains intact
   - All tests must pass

3. **No localStorage changes:**
   - Do NOT modify `authStore.ts`
   - Do NOT change `ra96it_token` or `ra96it_user` key names
   - Those are handled in AUTH-B spec

## Acceptance Criteria

- [ ] `VITE_RA96IT_API` replaced with `VITE_AUTH_API` everywhere in LoginPage.tsx
- [ ] All 4 instances of "ra96it" in UI text replaced with "hodeia"
- [ ] GitHub branding unchanged (logo, badge, consent flow)
- [ ] OAuth flow logic unchanged
- [ ] Tests created and passing (minimum 4 test cases)
- [ ] No changes to authStore.ts or localStorage key names

## Constraints (10 Hard Rules Apply)

- No file over 500 lines (LoginPage.tsx is 275 lines, safe)
- CSS: `var(--sd-*)` only (already compliant)
- No stubs (full implementation required)
- TDD (tests first, then implementation)
- Do NOT change OAuth flow logic — only env var name and UI text
- Do NOT change localStorage keys (separate task AUTH-B)

## Model Assignment

**Haiku** — This is a straightforward find-replace + test task.

---

## Your Task, Q33N

1. Read the files listed above
2. Write a single task file: `2026-03-24-TASK-AUTH-A-LOGIN-REBRAND.md`
3. Return the task file to Q33NR for review
4. After Q33NR approval, dispatch the bee (haiku model)
5. Review bee response file
6. Report results to Q33NR

Do NOT dispatch the bee until Q33NR reviews and approves the task file.
