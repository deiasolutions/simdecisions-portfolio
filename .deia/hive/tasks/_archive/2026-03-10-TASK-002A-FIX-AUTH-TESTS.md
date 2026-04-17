# TASK-002A: Fix ra96it Auth Test Failures (14 of 65)

## Objective

Fix the 14 failing tests in `tests/ra96it/`. The auth service code is 95% correct — these are test infrastructure issues and 2 minor route bugs.

## Dependencies

- TASK-002 must be complete (it is).

## Root Cause Analysis — 4 Distinct Issues

### Issue 1: Settings patch doesn't reach imported references (7+ failures)

**Files affected:** `tests/ra96it/conftest.py`

The `client` fixture patches `ra96it.config.settings` but several modules import settings with `from ra96it.config import settings`, creating local bindings that don't update when the module attribute is patched.

**Modules that need patching:**
- `ra96it.services.jwt` (line 6: `from ra96it.config import settings`)
- `ra96it.routes.mfa` (line 14: `from ra96it.config import settings`)
- `ra96it.routes.token` (line 16: `from ra96it.config import settings`)

**Fix:** In `conftest.py`, expand the `client` fixture's `patch` block:

```python
with patch("ra96it.config.settings", test_settings), \
     patch("ra96it.services.jwt.settings", test_settings), \
     patch("ra96it.routes.mfa.settings", test_settings), \
     patch("ra96it.routes.token.settings", test_settings), \
     patch("ra96it.services.audit.LEDGER_PATH", test_ledger_db):
```

### Issue 2: MissingGreenlet in MFA route (3 failures)

**File:** `ra96it/routes/mfa.py`, line 86

Current code accesses lazy-loaded relationship in async context:
```python
user = await session.get(type(login_session.user), login_session.user_id)
```

`type(login_session.user)` triggers a sync SQL query (MissingGreenlet).

**Fix:** Import User model directly:
```python
from ra96it.models import User
user = await session.get(User, login_session.user_id)
```

### Issue 3: Test sends invalid code format (2 failures)

**Files:** `tests/ra96it/test_mfa.py` (test_mfa_verify_wrong_code) and `tests/ra96it/test_audit.py` (test_mfa_failure_emits_event)

The Pydantic schema enforces `code: str = Field(..., min_length=6, max_length=6)`. Tests send `"wrong_code"` (10 chars), which fails Pydantic validation (422) before reaching the auth check (401).

**Fix:** Change `"code": "wrong_code"` to `"code": "000000"` in both test files.

### Issue 4: Datetime microsecond precision (1 failure)

**File:** `tests/ra96it/test_jwt.py` (test_token_expiry_time)

The assertion `exp <= expected_exp` fails because `create_access_token` calls `datetime.now(UTC)` slightly after the test captures `expected_exp`, adding microseconds.

**Fix:** Add 2-second tolerance to the comparison:
```python
assert expected - timedelta(seconds=2) <= exp <= expected + timedelta(seconds=2)
```

## What to Do

1. Apply all 4 fixes above
2. Run `python -m pytest tests/ra96it/ -v` and verify all 65 tests pass
3. If any test still fails, debug and fix it

## Constraints

- Do NOT restructure or refactor any code beyond the specific fixes
- Do NOT add new tests
- Do NOT change any passing test behavior
- Keep all files under 500 lines
- Python 3.13 (currently running 3.12, that's fine)

## Files to Modify

- `tests/ra96it/conftest.py` — add settings patches
- `ra96it/routes/mfa.py` — fix MissingGreenlet
- `tests/ra96it/test_mfa.py` — fix wrong_code format
- `tests/ra96it/test_audit.py` — fix wrong_code format
- `tests/ra96it/test_jwt.py` — fix datetime precision

## Deliverables

- [ ] All 65 tests pass
- [ ] No regressions in passing tests

## Response Requirements -- MANDATORY

Write response to: `.deia/hive/responses/YYYYMMDD-TASK-002A-RESPONSE.md`

Sections: Header, Files Modified, What Was Done, Test Results, Build Verification, Acceptance Criteria, Clock/Cost/Carbon, Issues/Follow-ups.
