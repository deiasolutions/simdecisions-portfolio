# SPEC: Wire GitHub OAuth token landing — extract token from URL, store, show logged-in state

## Priority
P0

## Model Assignment
sonnet

## Objective
After GitHub OAuth completes, the backend redirects to `{origin}?token={jwt}`. The frontend currently ignores this — no code reads the `?token=` query parameter from the URL. Additionally, the `AuthAdapter.onAuthSuccess` callback only console.logs instead of storing the token. Fix both so the full GitHub OAuth flow works end-to-end: user clicks "Continue with GitHub" → authenticates → returns to ra96it.com logged in.

## Context for Q33NR

The full diagnostic: the backend OAuth flow (oauth.py) works correctly — it exchanges the GitHub code, creates the user, mints a JWT, and redirects to `{origin}?token={jwt_token}`. The problem is entirely frontend.

**Bug 1 — No URL token extraction (LoginPage.tsx)**
After the OAuth redirect, the browser loads `ra96it.com?token=eyJhbG...` but LoginPage never checks `window.location.search` for `?token=` or `?error=`. Needs a `useEffect` on mount that:
1. Reads `?token=` from URLSearchParams
2. Decodes the JWT payload to extract user info (sub, email, display_name)
3. Calls `onAuthSuccess(token, user)`
4. Cleans the URL (removes `?token=` from address bar via `history.replaceState`)
5. Also handles `?error=` — shows error message to user

**Bug 2 — onAuthSuccess doesn't store anything (authAdapter.tsx)**
The `handleAuthSuccess` callback in AuthAdapter just console.logs. It needs to:
1. Call `setToken(token)` from authStore
2. Call `setUser(user)` from authStore
3. Show a "logged in" state (or redirect — at minimum, stop showing the login button)

**Bug 3 — No `origin` param passed (LoginPage.tsx:43)**
`fetch(\`${API_BASE}/auth/github/login\`)` doesn't pass `?origin=` so the backend falls back to `settings.frontend_url`. Should pass `window.location.origin` so the redirect goes back to wherever the user actually is.

**Recommended task breakdown:**
- TASK A (haiku): Add `useEffect` to LoginPage that reads `?token=` and `?error=` from URL on mount, calls `onAuthSuccess` or shows error. Add `?origin=` to the `/auth/github/login` fetch. Write tests.
- TASK B (haiku): Wire `AuthAdapter.handleAuthSuccess` to call `setToken()` + `setUser()` from authStore. Add a minimal "logged in" state to LoginPage (show user email, hide login button). Write tests.

**Files involved:**
- `browser/src/primitives/auth/LoginPage.tsx`
- `browser/src/apps/authAdapter.tsx`
- `browser/src/primitives/auth/authStore.ts`
- `browser/src/primitives/auth/__tests__/LoginPage.test.tsx`
- `browser/src/primitives/auth/__tests__/authStore.test.ts`

## Acceptance Criteria
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

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only

## Smoke Test
- [ ] cd browser && npx vitest run src/primitives/auth/__tests__/
- [ ] cd browser && npx vitest run src/apps/__tests__/
- [ ] No new test failures in: cd browser && npx vitest run
