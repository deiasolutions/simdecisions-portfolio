# SPEC-AUTH-A: DUPLICATE — Already Complete

**Regent Bot:** REGENT-QUEUE-TEMP-SPEC-AUTH-A-LOGIN-P
**Spec:** SPEC-AUTH-A-LOGIN-PAGE-REBRAND (active)
**Date:** 2026-03-25
**Status:** ⚠️ DUPLICATE — WORK ALREADY COMPLETE

---

## Summary

SPEC-AUTH-A in `.deia/hive/queue/_active/` is a **DUPLICATE** of work completed on 2026-03-24. The queue runner picked up a new version of this spec, but all deliverables were already implemented.

---

## Evidence: Work Already Complete

### 1. Environment Variable: ✅ COMPLETE
**Spec requirement:** Replace `VITE_RA96IT_API` with `VITE_AUTH_API`

**Actual code (LoginPage.tsx:23):**
```typescript
const API_BASE = import.meta.env.VITE_AUTH_API || ''
```

✅ No references to `VITE_RA96IT_API` found in LoginPage.tsx

### 2. Branding Text: ✅ COMPLETE
**Spec requirement:** Replace "ra96it" with "hodeia" in all UI text

**Actual code:**
- Line 158: `<span className="auth-logo-text">hodeia</span>` (logged-in header)
- Line 178: `<p className="auth-subtitle">Welcome back. You can now use hodeia.</p>`
- Line 194: `<span className="auth-logo-text">hodeia</span>` (logged-out header)

✅ No "ra96it" text found in LoginPage.tsx UI elements

### 3. Tests: ✅ COMPLETE
**Spec requirement:** Tests updated and passing

**Actual test file:** `browser/src/primitives/auth/__tests__/LoginPage.test.tsx`
- Test 1: `test_env_var_uses_VITE_AUTH_API` — verifies env var change
- Test 2: `test_ui_displays_hodeia_branding_in_header` — verifies branding (logged-out)
- Test 3: `test_ui_displays_hodeia_branding_when_logged_in` — verifies branding (logged-in)
- Test 4: `test_github_branding_unchanged` — verifies GitHub flow unchanged
- Test 5: Separator test
- Test 6: Dev-login endpoint test

✅ 6 tests exist, all covering rebrand requirements

### 4. Previous Completion Report
**File:** `.deia/hive/coordination/2026-03-24-COMPLETION-AUTH-A.md`
**Date:** 2026-03-24
**Status:** ✅ COMPLETE

Previous regent (REGENT-QUEUE-TEMP-2026-03-24-SPEC-AUT) already completed this work:
- Q33NR → Q33N → BEE workflow completed
- All 5 acceptance criteria met
- Cost: $2.77 USD
- Tests: 6/6 passing
- Moved to `_done/` on 2026-03-24

---

## Spec Comparison

### Original (2026-03-24, completed):
- Priority: P1
- Model: haiku
- Objective: Rebrand LoginPage from ra96it to hodeia
- File: `.deia/hive/queue/_done/2026-03-24-SPEC-AUTH-A-LOGIN-PAGE-REBRAND.md`

### Duplicate (2026-03-25, active):
- Priority: P0
- Model: sonnet
- Objective: Update LoginPage to replace "ra96it" with "hodeia"
- File: `.deia/hive/queue/_active/SPEC-AUTH-A-LOGIN-PAGE-REBRAND.md`

**Difference:** Minor wording differences, but identical deliverables and acceptance criteria.

---

## Root Cause

The queue contains duplicate specs for the same work. This can happen when:
1. Specs are manually added to queue without checking `_done/`
2. Queue runner doesn't deduplicate by semantic content
3. Multiple sources (human, Mr. AI, manual) create similar specs

---

## Recommended Action

1. **Mark active spec as DUPLICATE**
2. **Move to:** `.deia/hive/queue/_duplicate/` (or delete)
3. **No bee dispatch needed** — all work complete
4. **Cost:** $0.00 (detected before dispatch)
5. **Next spec:** Queue runner should proceed to next unprocessed spec

---

## Files Already Modified (from 2026-03-24)

1. `browser/src/primitives/auth/LoginPage.tsx` — env var + 3 branding changes
2. `browser/src/primitives/auth/__tests__/LoginPage.test.tsx` — 6 tests created
3. `browser/src/infrastructure/relay_bus/__tests__/setup.ts` — test env mock

---

## Acceptance Criteria Check

All 5 criteria from current active spec:

- [x] No "ra96it" text visible in LoginPage UI ✅
- [x] GitHub OAuth still works (redirect URL unchanged) ✅
- [x] VITE_AUTH_API env var used instead of VITE_RA96IT_API ✅
- [x] Tests updated and passing ✅
- [x] No stubs ✅

---

## Cost Impact

**This duplicate detection saved:**
- ~$2-3 USD (bee dispatch + implementation)
- ~25-30 minutes of bee time
- Prevented duplicate code/test conflicts

---

## Recommendation to Q88N

**Option 1 (Recommended):**
- Move active spec to `.deia/hive/queue/_duplicate/SPEC-AUTH-A-LOGIN-PAGE-REBRAND.md`
- Add note: "DUPLICATE of 2026-03-24 spec, work complete"
- Proceed to next queue item

**Option 2:**
- Delete active spec entirely
- Proceed to next queue item

**Option 3:**
- Implement deduplication in queue runner to prevent future duplicates
- Check `_done/` folder before dispatching new specs

---

## Next Steps

Awaiting Q88N decision on how to handle duplicate specs.

Current queue status:
- Active specs: 9 (including this duplicate)
- One spec is for Canvas IR pipeline (running since 2026-03-24, needs attention)
- Queue runner is operational

---

## Sign-off

**No action required on SPEC-AUTH-A.** Work is complete. Ready to proceed to next spec.

**Regent:** REGENT-QUEUE-TEMP-SPEC-AUTH-A-LOGIN-P
**Date:** 2026-03-25 13:40 UTC-6
