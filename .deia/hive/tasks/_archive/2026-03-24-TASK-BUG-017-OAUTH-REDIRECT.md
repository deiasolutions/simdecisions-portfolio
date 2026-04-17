# TASK-BUG-017: Fix OAuth Redirect to ra96it.com Shows LandingPage

## Objective

Fix OAuth redirect issue where after successful OAuth authentication at ra96it.com, the redirect back to ShiftCenter shows LandingPage instead of recognizing the authenticated state and loading the Shell.

## Context — WORK ALREADY DONE

✅ **Already created:**
- Test file: `App.oauthRedirect.test.tsx` (comprehensive test suite, 20+ tests)

❌ **What's BROKEN:**
- Test file crashes on initialization: `ReferenceError: Cannot access 'mockResolveCurrentEgg' before initialization`
- The mock setup is broken — `mockResolveCurrentEgg` is used before it's defined
- OAuth redirect logic NOT yet implemented in App.tsx

**Expected flow:**
1. User authenticates via ra96it.com OAuth
2. ra96it redirects to ShiftCenter with `?token=<JWT>` in URL
3. ShiftCenter should:
   - Extract token from URL query param or hash
   - Save token to localStorage via `authStore.setToken()`
   - Clean URL (remove token from query string)
   - Recognize authenticated state via `authStore.isAuthenticated()`
   - Load Shell with authenticated session (NOT LandingPage)

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\App.tsx` — main app component, decides LandingPage vs Shell
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\authStore.ts` — token storage and auth state
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\__tests__\App.oauthRedirect.test.tsx` — existing test (may be incomplete)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\pages\LandingPage.tsx` — landing page component
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\__tests__\App.shouldShowLanding.test.tsx` — test for landing page logic

## Deliverables

**Step 1: Fix the test mock (FIRST):**
- [ ] Fix `mockResolveCurrentEgg` initialization error in `App.oauthRedirect.test.tsx`
- [ ] Move mock declaration before first use OR use different mock pattern
- [ ] Verify all tests can run without crashes

**Step 2: Implement OAuth redirect logic:**
- [ ] Token extraction from URL query string (`?token=xxx`)
- [ ] Token extraction from URL hash (`#token=xxx`) — some OAuth flows use hash
- [ ] Token validation (must be valid JWT with 3 parts)
- [ ] Token saved to localStorage via `setToken()` on redirect
- [ ] URL cleaned (token removed from query string) for security
- [ ] Preserve other query params (e.g., `?egg=code&token=xxx` → `?egg=code`)
- [ ] App.tsx recognizes authenticated state and loads Shell (NOT LandingPage)

**Step 3: Tests pass:**
- [ ] All 20+ OAuth redirect tests pass
- [ ] No existing tests broken

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases covered:
  - Token in URL query string (`?token=xxx`)
  - Token in URL hash (`#token=xxx`) — should also work
  - Invalid token format (not a valid JWT)
  - Expired token (exp claim in past)
  - Missing token (no query param)
  - Token already in localStorage (skip extraction)
  - URL cleaning (token removed after extraction)
  - Multiple query params (`?egg=code&token=xxx` → `?egg=code`)
- [ ] Minimum 8 test cases covering success path + edge cases
- [ ] No existing tests broken

## Constraints

- No file over 500 lines
- CSS: `var(--sd-*)` only — no hardcoded colors
- No stubs — fully implement all functions
- Do NOT modify ra96it backend — this is a browser-side fix only
- Do NOT change token format or JWT structure — work with existing format

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260324-TASK-BUG-017-RESPONSE.md`

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

## Bug Details (from inventory)

- **ID:** BUG-017
- **Severity:** P0
- **Component:** ra96it
- **Title:** OAuth redirect to ra96it.com shows LandingPage instead of logged-in state
- **Status:** OPEN
- **Description:** After OAuth redirect back from provider, app shows LandingPage instead of recognizing auth token and loading Shell

## Manual Verification Steps (to include in response)

After implementation, verify manually:
1. Clear localStorage
2. Navigate to ShiftCenter landing page
3. Click "Sign in" (if button exists) or manually navigate to ra96it OAuth URL
4. Complete OAuth flow at provider
5. Observe redirect back to ShiftCenter with `?token=xxx` in URL
6. **Expected:** Shell loads with authenticated session
7. **NOT expected:** LandingPage shows again

Document these steps in the response with actual URLs and expected vs actual behavior.
