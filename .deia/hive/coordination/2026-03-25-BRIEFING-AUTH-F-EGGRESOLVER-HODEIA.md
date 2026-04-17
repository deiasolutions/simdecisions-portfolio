---
date: 2026-03-25
spec: SPEC-AUTH-F-EGGRESOLVER-HODEIA
priority: P1
model: haiku
role: queen
status: review_needed
---

# BRIEFING: eggResolver hodeia.me Mapping Verification

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Regent)
**Date:** 2026-03-25
**Spec:** SPEC-AUTH-F-EGGRESOLVER-HODEIA

---

## Objective

Verify that hodeia.me hostname mapping is correctly implemented in eggResolver, with ra96it.com kept as deprecated backwards compatibility, and both hostnames have test coverage.

---

## Initial Finding

After reading the codebase, **this spec appears to already be complete:**

### Evidence from `browser/src/eggs/eggResolver.ts`:
- Lines 126-128: `hodeia.me` and `www.hodeia.me` map to `'login'` EGG ✓
- Lines 140-143: `ra96it.com` variants map to `'login'` with clear "DEPRECATED: use hodeia.me" comments ✓

### Evidence from `browser/src/eggs/__tests__/eggResolver.test.ts`:
- Lines 84-86: Test for `hodeia.me` → `'login'` ✓
- Lines 116-126: Tests for all three `ra96it.com` variants → `'login'` ✓
- Line 112: Test for `www.hodeia.me` → `'login'` (in www.hodeia.* batch test) ✓

---

## Your Task

**Review the implementation and determine if this spec is complete.**

### Files to Read:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\__tests__\eggResolver.test.ts`

### Acceptance Criteria from Spec:
- [ ] hodeia.me resolves to login EGG
- [ ] ra96it.com still resolves to login EGG (backwards compat)
- [ ] ra96it.com mapping marked as deprecated in comments
- [ ] Tests cover both hostnames
- [ ] No stubs

### If Complete:
1. Run the tests to verify they pass: `cd browser && npx vitest run src/eggs/__tests__/eggResolver.test.ts`
2. If all tests pass and acceptance criteria met, write a verification response
3. **Do NOT create any task files** — this is verification only
4. Mark the spec as COMPLETE in your response
5. Return control to Q33NR for archival

### If Incomplete:
1. Document what's missing
2. Create task file(s) to complete the missing work
3. Return to Q33NR for review before dispatch

---

## Constraints

- No code changes unless something is actually missing
- TDD: tests first if any code needs to be written
- No file over 500 lines
- CSS: `var(--sd-*)` only (not applicable to this spec)
- No stubs

---

## Expected Response Format

Write a response to: `.deia/hive/responses/20260325-AUTH-F-EGGRESOLVER-HODEIA-Q33N-VERIFICATION.md`

Include:
1. **Status:** COMPLETE | INCOMPLETE
2. **Findings:** What you verified
3. **Test Results:** Output from vitest run
4. **Acceptance Criteria:** All 5 items checked [x] or [ ]
5. **Recommendation:** Archive spec OR task files needed

---

## Context

This is part of AUTH spec series transitioning from ra96it.com → hodeia.me branding. The login page rebrand (AUTH-A) and localStorage migration (AUTH-B) are separate specs. This spec is ONLY about the hostname → EGG resolver mapping.

---

## Notes

- The queue runner is active
- Session budget: $827.03 / ??? (check queue.yml for limit)
- This is a verification task, not a build task
- If verification confirms completion, this is a 5-minute task
