# TASK-185: Wire AuthAdapter storage and add logged-in UI state

## Objective
Wire `AuthAdapter.handleAuthSuccess` to call `setToken()` and `setUser()` from authStore instead of just console.logging. Add minimal "logged in" state to LoginPage that hides login UI when `isAuthenticated()` returns true and shows user email.

## Context
Currently `authAdapter.tsx` only console.logs on auth success. It needs to persist the token and user data to localStorage via authStore functions. Additionally, LoginPage has no logged-in state — it always shows the login button even after successful auth.

The auth flow:
1. LoginPage extracts token from URL (TASK-184)
2. LoginPage calls `onAuthSuccess(token, user)`
3. AuthAdapter receives callback → calls `setToken()` + `setUser()`
4. LoginPage re-renders → `isAuthenticated()` returns true → shows logged-in UI

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\authAdapter.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\authStore.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\LoginPage.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\authAdapter.test.tsx` (if exists)

## Deliverables
- [ ] Import `setToken` and `setUser` from authStore in `authAdapter.tsx`
- [ ] Call `setToken(token)` in `handleAuthSuccess`
- [ ] Call `setUser(user)` in `handleAuthSuccess`
- [ ] Keep console.log for debugging (not a stub, just observability)
- [ ] Add new prop to LoginPage: `isLoggedIn?: boolean` (optional, default false)
- [ ] LoginPage: import `isAuthenticated` and `getUser` from authStore
- [ ] LoginPage: add `useEffect` to detect auth state changes (watches localStorage)
- [ ] LoginPage: when `isAuthenticated()` returns true, render logged-in UI instead of login form
- [ ] Logged-in UI shows: user email, "You're logged in" message, minimal styling
- [ ] Logged-in UI uses existing CSS classes (auth-* prefix) or add new minimal CSS
- [ ] AuthAdapter passes `isLoggedIn={isAuthenticated()}` to LoginPage (optional enhancement)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] New test: `test_auth_adapter_calls_setToken` — verify `setToken()` called with token
- [ ] New test: `test_auth_adapter_calls_setUser` — verify `setUser()` called with user object
- [ ] New test: `test_login_page_shows_logged_in_ui_when_authenticated` — mock `isAuthenticated()` → true, verify login button hidden
- [ ] New test: `test_login_page_shows_user_email_when_authenticated` — verify user email displayed
- [ ] New test: `test_login_page_hides_consent_section_when_authenticated` — verify consent card hidden
- [ ] Edge case: `isAuthenticated()` returns false after initial true — verify UI reverts to login form
- [ ] All existing tests still pass

## Constraints
- No file over 500 lines (authAdapter.tsx currently ~21 lines, LoginPage.tsx ~168 lines)
- CSS: var(--sd-*) only (if adding new styles)
- No stubs
- Do NOT remove console.log — it's useful for debugging, not a stub
- Logged-in UI should be minimal — just enough to prove the flow works (not a full dashboard)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-185-RESPONSE.md`

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

## Smoke Test Commands
```bash
cd browser && npx vitest run src/apps/__tests__/authAdapter.test.tsx
cd browser && npx vitest run src/primitives/auth/__tests__/LoginPage.test.tsx
cd browser && npx vitest run src/primitives/auth/__tests__/
cd browser && npx vitest run src/apps/__tests__/
```
