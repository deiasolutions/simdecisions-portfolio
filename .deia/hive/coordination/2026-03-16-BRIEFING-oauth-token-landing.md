# BRIEFING: Wire GitHub OAuth token landing — extract token from URL, store, show logged-in state

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-16
**Spec:** SPEC-auth-01-oauth-token-landing
**Priority:** P0
**Model Assignment:** sonnet

---

## Objective

Complete the GitHub OAuth flow end-to-end. Currently the backend redirects to `{origin}?token={jwt}` but the frontend ignores the token in the URL. Fix both token extraction and storage so users see logged-in state after OAuth completes.

---

## Context from Q88N

The backend OAuth flow (oauth.py) works correctly — it exchanges the GitHub code, creates the user, mints a JWT, and redirects to `{origin}?token={jwt_token}`. The problem is entirely frontend.

**Three bugs to fix:**

1. **No URL token extraction (LoginPage.tsx)** — After OAuth redirect, browser loads `ra96it.com?token=eyJhbG...` but LoginPage never checks `window.location.search` for `?token=` or `?error=`

2. **onAuthSuccess doesn't store anything (authAdapter.tsx)** — The `handleAuthSuccess` callback in AuthAdapter just console.logs instead of calling `setToken()` and `setUser()` from authStore

3. **No `origin` param passed (LoginPage.tsx:43)** — `fetch(\`${API_BASE}/auth/github/login\`)` doesn't pass `?origin=` so the backend falls back to `settings.frontend_url`

---

## Files Involved

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\LoginPage.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\authAdapter.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\authStore.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\LoginPage.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\authStore.test.ts`

---

## Recommended Task Breakdown

**TASK A (haiku):** LoginPage token extraction
- Add `useEffect` to LoginPage that reads `?token=` and `?error=` from URL on mount
- Decode JWT payload to extract user info (sub/id, email, display_name)
- Call `onAuthSuccess(token, user)` when token found
- Clean URL after extraction (remove `?token=` from address bar via `history.replaceState`)
- Handle `?error=` — show error message to user
- Add `?origin=` to the `/auth/github/login` fetch call (pass `window.location.origin`)
- Write tests for all scenarios

**TASK B (haiku):** AuthAdapter storage wiring
- Wire `AuthAdapter.handleAuthSuccess` to call `setToken(token)` and `setUser(user)` from authStore
- Add minimal "logged in" state to LoginPage (show user email, hide login button when `isAuthenticated()` returns true)
- Write tests for auth success flow and logged-in UI

---

## Acceptance Criteria (from spec)

- [ ] `?token=` query parameter extracted from URL on LoginPage mount
- [ ] JWT payload decoded to get user info (sub/id, email, display_name)
- [ ] `onAuthSuccess(token, user)` called with extracted data
- [ ] URL cleaned after token extraction (no `?token=` in address bar)
- [ ] `?error=` query parameter handled — user sees error message
- [ ] `AuthAdapter.handleAuthSuccess` calls `setToken()` and `setUser()` from authStore
- [ ] LoginPage shows logged-in state when `isAuthenticated()` returns true
- [ ] `origin` parameter passed to `/auth/github/login` fetch call
- [ ] All existing LoginPage and authStore tests still pass
- [ ] New tests cover: token extraction, error handling, auth success storage, logged-in UI

---

## Constraints

- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- All file paths absolute in task files

---

## Smoke Test

```bash
cd browser && npx vitest run src/primitives/auth/__tests__/
cd browser && npx vitest run src/apps/__tests__/
cd browser && npx vitest run
```

No new test failures.

---

## Instructions for Q33N

1. Read the files listed above
2. Write 2 task files (TASK A and TASK B as outlined)
3. Return task files to Q33NR for review
4. Do NOT dispatch bees until Q33NR approves
5. Ensure all task files include absolute paths and the 8-section response template requirement
