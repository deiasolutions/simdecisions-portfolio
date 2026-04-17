# TASK-245A: Add E2E Test for ra96it Sign-Up Flow

**Parent:** TASK-245 (ra96it Sign-Up Flow Verified)
**Wave:** 5 (Ship)
**Model:** haiku
**Est:** 30 minutes

---

## Objective

Add an end-to-end integration test that simulates the full ra96it sign-up flow from the frontend perspective: user clicks "Continue with GitHub" → redirects to mock OAuth URL → lands back with token → token stored in localStorage → user is authenticated.

---

## Context

The ra96it sign-up flow is fully implemented (TASK-136, TASK-137, TASK-138) but has never been tested end-to-end. Existing tests are unit tests that mock individual components.

**What exists:**
- `LoginPage.test.tsx` — 19 unit tests for token extraction, decoding, UI states (mocks fetch)
- `test_oauth.py` — 14 backend tests for OAuth routes (mocks GitHub API)

**What's missing:**
- An E2E test that wires the entire frontend flow together, verifying:
  1. Click "Continue with GitHub" → fetch called with correct origin
  2. GitHub OAuth URL returned → redirect initiated
  3. User lands back with `?token=<jwt>` in URL
  4. Token extracted and decoded
  5. `onAuthSuccess` called with correct token + user
  6. Token stored in localStorage under `ra96it_token`
  7. User stored in localStorage under `ra96it_user`
  8. `isAuthenticated()` returns true

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\LoginPage.tsx` — OAuth UI and redirect handler
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\authStore.ts` — Token storage and validation
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\authAdapter.tsx` — Wires LoginPage to authStore
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\LoginPage.test.tsx` — Existing unit tests (reference for patterns)

---

## Deliverables

- [ ] Create new test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\LoginPage.integration.test.tsx`
- [ ] Write E2E test: `test_full_signup_flow_stores_token_and_authenticates_user`
  - Mock `fetch` for `/auth/github/login` → return mock GitHub URL
  - Simulate click on "Continue with GitHub" button
  - Verify fetch called with correct origin parameter
  - Simulate GitHub callback by setting `window.location.search = '?token=<mock_jwt>'`
  - Verify `onAuthSuccess` called with correct token + user
  - Verify token stored in localStorage under `ra96it_token`
  - Verify user stored in localStorage under `ra96it_user`
  - Verify `isAuthenticated()` returns true
- [ ] Write E2E test: `test_signup_flow_handles_github_error_gracefully`
  - Simulate GitHub error by setting `window.location.search = '?error=access_denied'`
  - Verify error message displayed
  - Verify `onAuthSuccess` NOT called
  - Verify token NOT stored
- [ ] Write E2E test: `test_signup_flow_cleans_url_after_token_extraction`
  - Simulate callback with token in URL
  - Verify `window.history.replaceState` called to clean URL
  - Verify URL no longer contains `?token=`
- [ ] Run all tests: `cd browser && npx vitest run`
- [ ] All tests pass (including new E2E tests)

---

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Valid JWT with all required claims
  - Valid JWT with missing optional claims (display_name)
  - Malformed JWT (should not crash)
  - GitHub error in callback
  - Missing token in callback
  - URL cleaned after token extraction

---

## Mocking Strategy

**Mock external calls:**
- `fetch('/auth/github/login')` → return `{url: "https://github.com/login/oauth/authorize?..."}`
- `fetch('/dev-login/available')` → return `{available: false}` (hide dev-login button for simplicity)

**Do NOT mock:**
- `authStore.ts` functions (setToken, setUser, getToken, isAuthenticated)
- localStorage (use real localStorage, clear in beforeEach/afterEach)
- `decodeJwtPayload()` in LoginPage.tsx (use real JWT decoding)

**Simulate GitHub callback:**
- Instead of navigating to GitHub and back, set `window.location.search = '?token=<mock_jwt>'` and re-render component
- Use a real JWT payload (base64-encoded JSON) so decoding works

**Example mock JWT:**
```js
const payload = {
  sub: 'test-user-id',
  email: 'test@example.com',
  display_name: 'Test User',
  scope: 'chat',
  exp: Math.floor(Date.now() / 1000) + 3600,
  iat: Math.floor(Date.now() / 1000),
  iss: 'ra96it.com',
  aud: 'ra96it.com',
}
const encodedPayload = btoa(JSON.stringify(payload))
const mockJWT = `eyJhbGc.${encodedPayload}.signature`
```

---

## Constraints

- No file over 500 lines
- CSS: var(--sd-*) only (N/A for tests)
- No stubs — every function fully implemented
- TDD — tests first, then implementation (tests only, no implementation needed)
- No hardcoded colors (N/A for tests)

---

## Acceptance Criteria

- [ ] New file created: `LoginPage.integration.test.tsx`
- [ ] At least 3 E2E tests written:
  1. Full signup flow (click → redirect → callback → storage → auth)
  2. Error handling (GitHub error in callback)
  3. URL cleaning (replaceState called)
- [ ] All tests use real authStore functions (no mocking localStorage operations)
- [ ] Mock JWT has valid base64-encoded payload
- [ ] Run: `cd browser && npx vitest run` — all tests pass (existing + new)
- [ ] Test output shows new tests in passing count

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-245A-RESPONSE.md`

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

---

## Example Test Structure

```tsx
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import LoginPage from '../LoginPage'
import { getToken, getUser, isAuthenticated, setToken, setUser } from '../authStore'

global.fetch = vi.fn()

describe('LoginPage E2E', () => {
  const mockOnAuthSuccess = vi.fn()

  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
    window.location = {
      ...window.location,
      search: '',
      pathname: '/',
      origin: 'http://localhost:3000',
      href: 'http://localhost:3000/',
    } as any
  })

  afterEach(() => {
    localStorage.clear()
  })

  it('test_full_signup_flow_stores_token_and_authenticates_user', async () => {
    // Step 1: Mock /auth/github/login response
    ;(global.fetch as any)
      .mockResolvedValueOnce({ json: async () => ({ available: false }) }) // /dev-login/available
      .mockResolvedValueOnce({ json: async () => ({ url: 'https://github.com/...' }) }) // /auth/github/login

    // Step 2: Render LoginPage
    const { rerender } = render(<LoginPage onAuthSuccess={mockOnAuthSuccess} />)

    // Step 3: Click "Continue with GitHub"
    const githubButton = screen.getByRole('button', { name: /continue with github/i })
    fireEvent.click(githubButton)

    // Step 4: Verify fetch called with origin
    await waitFor(() => {
      const calls = (global.fetch as any).mock.calls
      const githubLoginCall = calls.find((c: any) => c[0].includes('/auth/github/login'))
      expect(githubLoginCall).toBeDefined()
      expect(githubLoginCall[0]).toContain('?origin=http%3A%2F%2Flocalhost%3A3000')
    })

    // Step 5: Simulate GitHub callback (user lands back with token)
    const payload = {
      sub: 'user-123',
      email: 'user@example.com',
      display_name: 'Test User',
      scope: 'chat',
      exp: Math.floor(Date.now() / 1000) + 3600,
    }
    const encodedPayload = btoa(JSON.stringify(payload))
    const mockToken = `eyJhbGc.${encodedPayload}.signature`

    window.location.search = `?token=${mockToken}`
    rerender(<LoginPage onAuthSuccess={mockOnAuthSuccess} />)

    // Step 6: Verify onAuthSuccess called
    await waitFor(() => {
      expect(mockOnAuthSuccess).toHaveBeenCalledWith(mockToken, {
        id: 'user-123',
        email: 'user@example.com',
        display_name: 'Test User',
      })
    })

    // Step 7: Manually call authStore functions (simulating authAdapter)
    setToken(mockToken)
    setUser({ id: 'user-123', email: 'user@example.com', display_name: 'Test User' })

    // Step 8: Verify token stored
    expect(getToken()).toBe(mockToken)
    expect(getUser()).toEqual({
      id: 'user-123',
      email: 'user@example.com',
      display_name: 'Test User',
    })

    // Step 9: Verify authenticated
    expect(isAuthenticated()).toBe(true)
  })

  // Additional tests: error handling, URL cleaning, etc.
})
```

---

## References

- Existing unit tests: `LoginPage.test.tsx` (patterns for mocking fetch, window.location)
- authStore: `authStore.ts` (getToken, setToken, isAuthenticated)
- Flow trace: `.deia/hive/responses/20260317-TASK-245-FLOW-TRACE.md`
