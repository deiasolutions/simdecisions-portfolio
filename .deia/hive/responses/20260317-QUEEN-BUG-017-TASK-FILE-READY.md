# Q33N Report: BUG-017 Task File Ready for Q33NR Review

**Bot ID:** QUEEN-2026-03-17-BRIEFING-BUG-017-OA
**Model:** Sonnet 4.5
**Date:** 2026-03-17

---

## Summary
Task file written for BUG-017 (OAuth redirect landing page bug). Ready for Q33NR review and approval before dispatch.

## Task File Created
**Path:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-17-TASK-BUG-017-oauth-redirect-landing.md`

**Recommended model:** Haiku (as specified in briefing — small, surgical fix)

## Files Read During Analysis
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\App.tsx` (121 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\authStore.ts` (119 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts` (134 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\pages\LandingPage.tsx` (57 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\__tests__\App.test.tsx` (101 lines)

## Root Cause Confirmed
The briefing analysis is accurate. `shouldShowLanding()` (App.tsx lines 58-63) has three bugs:

**Bug A (Primary):** Ignores auth state — after OAuth saves token and cleans URL, function sees clean root path and returns `true`, showing LandingPage instead of login EGG

**Bug B:** Ignores hostname — ra96it.com domains should map to `login` EGG (via eggResolver.ts lines 94-96), but `shouldShowLanding()` short-circuits before EGG system runs

**Bug C:** LandingPage has no auth awareness (but this is acceptable — the fix belongs in App.tsx, not LandingPage)

## Fix Scope (10 lines modified)
1. Add `isAuthenticated` to imports from `authStore` (line 16)
2. Expand `shouldShowLanding()` from 5 lines to ~15 lines:
   - Check hostname — ra96it domains return `false`
   - Check auth state — authenticated users return `false`
   - Preserve existing behavior for root path with no `?egg=` when NOT authenticated

## Test Requirements (6 tests)
New test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\__tests__\App.shouldShowLanding.test.tsx`

Tests:
1. Returns `false` when hostname is `ra96it.com`
2. Returns `false` when hostname is `www.ra96it.com`
3. Returns `false` when hostname is `dev.ra96it.com`
4. Returns `false` when `isAuthenticated()` returns `true`
5. Returns `true` on root path with no `?egg=` on localhost when NOT authenticated (existing behavior)
6. Returns `false` when `?egg=` param present (existing behavior)

## Constraints Verified
- No file over 500 lines — App.tsx is 121 lines, will grow to ~130 lines (well under limit)
- No hardcoded colors — no CSS changes in this task
- TDD — tests first (required in task file)
- No stubs — `isAuthenticated()` already implemented and tested
- Absolute paths — all paths in task file are absolute

## Review Checklist for Q33NR
- [ ] All deliverables present?
- [ ] Test requirements clear and complete?
- [ ] Acceptance criteria measurable?
- [ ] File paths absolute?
- [ ] No hardcoded colors required?
- [ ] File size constraints met?
- [ ] Response template included?
- [ ] No stubs required?

## Ready for Dispatch Command (after Q33NR approval)
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-17-TASK-BUG-017-oauth-redirect-landing.md --model haiku --role bee --inject-boot
```

---

**Status:** WAITING FOR Q33NR REVIEW
**Next step:** Q33NR reviews task file, requests corrections if needed, or approves dispatch
