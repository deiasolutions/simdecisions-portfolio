# TASK-184: OAuth URL token extraction and origin parameter -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku 4.5
**Date:** 2026-03-16

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\LoginPage.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\LoginPage.css`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\LoginPage.test.tsx`

## What Was Done

### LoginPage.tsx (237 lines, +71 from original)
- **Added `decodeJwtPayload()` helper function** (lines 28-41)
  - Splits JWT into 3 parts (header.payload.signature)
  - Base64-decodes the middle segment
  - Parses JSON payload
  - Returns null on any error (malformed JWT)
  - No throw statements — graceful error handling

- **Added `errorMessage` state** (line 47)
  - Stores OAuth error messages
  - Null by default

- **Rewrote mount useEffect** (lines 49-89)
  - Extracts `?token=` and `?error=` from URL using URLSearchParams
  - If error param: sets error message and cleans URL (history.replaceState)
  - If token param: decodes JWT, extracts user fields (sub/id, email, display_name), calls onAuthSuccess, cleans URL
  - If malformed JWT: silently ignores and continues normal flow
  - If neither: proceeds to dev-login availability check

- **Updated handleGitHubLogin()** (lines 91-102)
  - Gets origin from `window.location.origin`
  - URL-encodes origin using `encodeURIComponent()`
  - Appends `?origin=${origin}` to `/auth/github/login` endpoint
  - Preserves existing error handling

- **Added error display UI** (lines 128-144)
  - Shows error card when errorMessage is set
  - Displays "Authentication Error" title
  - Shows error message text (includes OAuth error code)
  - "Try Again" button clears error and returns to consent screen

### LoginPage.css (+27 lines, new error styles)
- **.auth-error-card** — surface background with red border, centered padding
- **.auth-error-title** — red text, bold, 1.4rem
- **.auth-error-message** — primary text color, 0.95rem, line-height 1.6
- All use CSS variables (var(--sd-*)) only, no hardcoded colors

### LoginPage.test.tsx (+150 lines, 16 tests total)
**Existing tests (8) — all passing:**
- test_renders_github_button
- test_renders_consent_section
- test_dev_login_button_shown_when_available
- test_dev_login_button_hidden_when_unavailable
- test_github_login_fetches_url_with_origin (renamed/updated)
- test_dev_login_posts_and_calls_onAuthSuccess
- test_loading_spinner_shown_during_github_redirect
- test_no_hardcoded_colors_in_inline_styles

**New tests (8) — all passing:**
- **test_extracts_token_from_url_on_mount** — mocks URL with valid JWT, verifies onAuthSuccess called with token + user
- **test_decodes_jwt_payload_correctly** — verifies JWT payload decoding extracts correct user fields
- **test_cleans_url_after_token_extraction** — mocks URL with token, verifies history.replaceState called
- **test_handles_error_param_in_url** — mocks URL with `?error=access_denied`, verifies error displayed
- **test_handles_malformed_jwt_gracefully** — invalid JWT token, verifies no crash + normal render
- **test_passes_origin_to_github_login** — verifies fetch includes `?origin=http%3A%2F%2Flocalhost%3A3000`
- **test_handles_missing_user_fields_in_jwt** — JWT with missing display_name, verifies graceful fallback to empty string
- **test_no_token_in_url_renders_normally** — no query params, verifies normal flow

**Test infrastructure improvements:**
- Added proper beforeEach/afterEach to reset window.location and clear mocks
- Removed problematic delete (window as any).location pattern; use direct assignment
- All tests use waitFor() for async operations

## Test Results

```
✓ src/primitives/auth/__tests__/LoginPage.test.tsx (16 tests)

Test Files: 1 passed
Tests: 16 passed (16)
Duration: 55.22s
```

All 16 tests passing (8 existing + 8 new).

## Build Verification

**Auth test suite:**
```bash
cd browser && npx vitest run src/primitives/auth/__tests__/LoginPage.test.tsx
✓ 16 passed
```

**File sizes:**
- LoginPage.tsx: 237 lines (within 500 limit) ✓
- LoginPage.css: 253 lines (under 500 limit) ✓
- LoginPage.test.tsx: 362 lines (test file, appropriate) ✓

**Code quality checks:**
- ✓ No hardcoded colors (all CSS variables)
- ✓ No stubs or TODO comments
- ✓ Try/catch for JWT decoding
- ✓ Graceful error handling for malformed tokens
- ✓ TDD: all tests written before implementation

## Acceptance Criteria

- [x] Add `useEffect` hook to LoginPage that runs on mount (empty dependency array)
- [x] Extract `?token=` from `window.location.search` using URLSearchParams
- [x] Decode JWT payload (base64-decode middle segment between dots)
- [x] Extract user info from payload: `sub` (or `id`) → id, `email`, `display_name`
- [x] Call `onAuthSuccess(token, user)` when token is found
- [x] Clean URL after extraction using `window.history.replaceState({}, '', window.location.pathname)`
- [x] Extract `?error=` from URLSearchParams and store in state
- [x] Display error message to user when error param present
- [x] Add `?origin=${encodeURIComponent(window.location.origin)}` to `/auth/github/login` fetch call
- [x] Handle edge cases: malformed JWT, missing user fields, invalid base64
- [x] Tests written FIRST (TDD) ✓
- [x] All existing LoginPage tests pass ✓
- [x] New test: extract_token_from_url_on_mount ✓
- [x] New test: decodes_jwt_payload_correctly ✓
- [x] New test: cleans_url_after_token_extraction ✓
- [x] New test: handles_error_param ✓
- [x] New test: handles_malformed_jwt ✓
- [x] New test: passes_origin_to_github_login ✓
- [x] Edge case: missing user fields ✓
- [x] Edge case: no query params ✓

## Clock / Cost / Carbon

- **Clock:** 55.22s (test execution) + ~15 min (implementation & testing)
- **Cost:** Haiku model, ~20 API calls (Read/Edit/Write/Bash)
- **Carbon:** Minimal footprint (local test execution only)

## Issues / Follow-ups

**None.** All deliverables complete and tested.

### Notes for Future Work
- OAuth callback backend must redirect to `{origin}?token={jwt}` (implementation already done)
- JWT payload must include: `sub` (or `id`), `email`, `display_name`, `scope`, `exp`
- Error codes from GitHub OAuth: `access_denied`, `invalid_scope`, etc. (error param captures these)
- Token scope validation happens elsewhere (authStore.ts has isAuthenticated() that checks scope="chat")

---

**READY FOR MERGE**
