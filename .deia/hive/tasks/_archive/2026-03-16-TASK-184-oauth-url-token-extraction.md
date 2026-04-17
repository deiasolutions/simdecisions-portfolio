# TASK-184: OAuth URL token extraction and origin parameter

## Objective
Add URL token extraction to LoginPage on mount that reads `?token=` and `?error=` query parameters, decodes JWT payload, calls `onAuthSuccess` with extracted data, and cleans the URL. Also add `?origin=` parameter to `/auth/github/login` fetch call.

## Context
After GitHub OAuth completes, the backend redirects to `{origin}?token={jwt}` but LoginPage.tsx never reads the token from the URL. Additionally, LoginPage doesn't pass `?origin=` to the `/auth/github/login` endpoint, causing the backend to fall back to `settings.frontend_url`.

The JWT payload structure (base64-encoded middle segment):
```json
{
  "sub": "user-id",
  "email": "user@example.com",
  "display_name": "User Name",
  "scope": "chat",
  "exp": 1234567890
}
```

When the backend OAuth callback completes, it redirects to:
- Success: `{origin}?token=eyJhbG...`
- Error: `{origin}?error=access_denied` (or other OAuth error codes)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\LoginPage.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\authStore.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\LoginPage.test.tsx`

## Deliverables
- [ ] Add `useEffect` hook to LoginPage that runs on mount (empty dependency array)
- [ ] Extract `?token=` from `window.location.search` using URLSearchParams
- [ ] Decode JWT payload (base64-decode middle segment between dots)
- [ ] Extract user info from payload: `sub` (or `id`) → id, `email`, `display_name`
- [ ] Call `onAuthSuccess(token, user)` when token is found
- [ ] Clean URL after extraction using `window.history.replaceState({}, '', window.location.pathname)`
- [ ] Extract `?error=` from URLSearchParams and store in state
- [ ] Display error message to user when error param present
- [ ] Add `?origin=${encodeURIComponent(window.location.origin)}` to `/auth/github/login` fetch call (line 43)
- [ ] Handle edge cases: malformed JWT, missing user fields, invalid base64

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing LoginPage tests pass
- [ ] New test: `test_extracts_token_from_url_on_mount` — mock URL with `?token=`, verify `onAuthSuccess` called
- [ ] New test: `test_decodes_jwt_payload_correctly` — verify user fields extracted from JWT
- [ ] New test: `test_cleans_url_after_token_extraction` — verify `history.replaceState` called
- [ ] New test: `test_handles_error_param` — mock URL with `?error=access_denied`, verify error shown
- [ ] New test: `test_handles_malformed_jwt` — invalid JWT format, verify graceful handling (no crash)
- [ ] New test: `test_passes_origin_to_github_login` — verify fetch includes `?origin=` param
- [ ] Edge case: `?token=` with missing user fields in payload — verify graceful fallback
- [ ] Edge case: No query params — verify no errors, normal flow

## Constraints
- No file over 500 lines (LoginPage.tsx currently ~168 lines)
- CSS: var(--sd-*) only
- No stubs — full implementation of JWT decoding and error handling
- Use try/catch for JWT decoding (malformed tokens should not crash the app)
- Error message should use existing CSS classes (auth-* prefix) for consistency

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-184-RESPONSE.md`

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
cd browser && npx vitest run src/primitives/auth/__tests__/LoginPage.test.tsx
cd browser && npx vitest run src/primitives/auth/__tests__/
```
