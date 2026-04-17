# TASK-002A: Fix ra96it Auth Test Failures -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-03-10

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\ra96it\conftest.py` — Added settings patches for imported module references
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\routes\mfa.py` — Fixed MissingGreenlet error by importing User model directly
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\ra96it\test_mfa.py` — Fixed invalid code format (10 chars → 6 chars)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\ra96it\test_audit.py` — Fixed invalid code format (10 chars → 6 chars)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\ra96it\test_jwt.py` — Added datetime tolerance for precision issues
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\ra96it\test_token_refresh.py` — Fixed session isolation issue in replay attack test

## What Was Done

**Issue 1: Settings patch didn't reach imported references (7+ failures)**
- Expanded `conftest.py` client fixture to patch settings in all modules that use `from ra96it.config import settings`
- Added patches for: `ra96it.services.jwt.settings`, `ra96it.routes.mfa.settings`, `ra96it.routes.token.settings`
- This fixed failures where test settings (ephemeral RSA keys) weren't being used by the service code

**Issue 2: MissingGreenlet in MFA route (3 failures)**
- Fixed `ra96it/routes/mfa.py` line 86 where `type(login_session.user)` triggered lazy SQL load in async context
- Changed to import User model directly and use `await session.get(User, login_session.user_id)`
- This avoids accessing the lazy-loaded relationship attribute

**Issue 3: Test sends invalid code format (2 failures)**
- Changed test code from `"wrong_code"` (10 chars) to `"000000"` (6 chars) in 2 test files
- Pydantic schema enforces `code: str = Field(..., min_length=6, max_length=6)`
- Tests were failing validation (422) before reaching auth logic (401)

**Issue 4: Datetime microsecond precision (1 failure)**
- Added 2-second tolerance to JWT expiry time assertion
- Changed from exact equality to range check: `expected - 2s <= exp <= expected + 2s`
- Also added tolerance to `iat` time check to handle microsecond differences

**Issue 5: Session isolation in replay attack test (1 failure - discovered during fix)**
- Test and client use separate database sessions despite sharing same in-memory DB
- Test session was seeing stale data after client revoked tokens
- Fixed by closing test session and capturing `user_id` before the close, then querying fresh data
- This ensures the test sees the token revocations made by the client's session

## Test Results

```
============================= 65 passed in 13.16s =============================
```

All 65 tests in `tests/ra96it/` now pass.

**Before:** 14 failures, 51 passed
**After:** 0 failures, 65 passed

## Build Verification

Not applicable - no build step required for Python test-only changes.

## Acceptance Criteria

- [x] All 65 tests pass
- [x] No regressions in passing tests
- [x] Only modified test infrastructure and 1 minor route bug (MissingGreenlet)
- [x] No refactoring or restructuring beyond specific fixes
- [x] All files under 500 lines (no files modified exceeded this)

## Clock/Cost/Carbon

- **Wall time:** ~15 minutes
- **Model:** Sonnet 4.5
- **Turns:** 1 session
- **Cost:** Negligible (test fixes only, no production code changes beyond MissingGreenlet fix)

## Issues/Follow-ups

None. All 14 failures resolved. The auth service code was indeed 95% correct as stated in the task description. All issues were test infrastructure problems except for the MissingGreenlet bug in the MFA route.

---

**Task complete. All deliverables met.**
