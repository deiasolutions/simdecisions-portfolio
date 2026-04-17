# SPEC: Hodeia Auth Hardening

## Priority
P1

## Model Assignment
sonnet

## Summary
Fix security concerns and add missing features identified in the 2026-03-28 code review of `hodeia_auth/`. Three fixes are blocking public launch. Five features are enhancements.

## Depends On
None

## Scope

### Fix 1: Rate Limiting (BLOCKING)
Add `slowapi` rate limiting to auth endpoints.

**Install:** Add `slowapi` to `hodeia_auth/requirements.txt`

**Apply limits:**
- `POST /login` — 5 attempts/minute per IP
- `POST /register` — 10 attempts/hour per IP
- `POST /mfa/verify` — 3 attempts/minute per session
- `POST /token/refresh` — 10 attempts/minute per IP
- `POST /admin/reset-schema` — 1 attempt/minute per IP

**Implementation:**
- Import `Limiter` and `_rate_limit_exceeded_handler` from slowapi
- Create limiter instance in `main.py`, attach to app state
- Add `@limiter.limit()` decorators to route functions
- Return 429 with `Retry-After` header on limit exceeded

### Fix 2: Admin Secret to Env Var (BLOCKING)
**File:** `hodeia_auth/main.py`

Replace hardcoded `"alpha-reset-2026"` with env var:
```python
# config.py — add field
admin_secret: str = Field(default="", env="HODEIA_ADMIN_SECRET")

# main.py — use config
if secret != settings.admin_secret or not settings.admin_secret:
    return {"error": "unauthorized"}
```

### Fix 3: Sentinel Password Hash for OAuth Users (BLOCKING)
**Files:** `hodeia_auth/routes/oauth.py`, `hodeia_auth/routes/dev_login.py`, `hodeia_auth/models.py`

- Make `password_hash` nullable on User model: `password_hash: Mapped[Optional[str]]`
- Set `password_hash=None` for OAuth and dev-login created users
- Update `login.py` to reject login attempts on users with `password_hash=None` (return "Use OAuth to sign in")
- Add migration in `db.py` `_migrate_schema()` to allow NULL

### Feature 1: Password Reset Flow
**New files:** `hodeia_auth/routes/password_reset.py`, `hodeia_auth/services/reset_token.py`

**Endpoints:**
- `POST /password/forgot` — takes email, sends reset code via recovery email
- `POST /password/reset` — takes email, code, new_password; validates and updates

**Logic:**
- Generate 6-digit code, store hashed in DB with 15-min expiry
- Use existing `recovery_email` infrastructure for delivery
- Rate limit: 3 attempts/hour per email
- Audit log: `AUTH_PASSWORD_RESET_REQUEST`, `AUTH_PASSWORD_RESET_SUCCESS`

### Feature 2: Email Verification Flow
**New file:** `hodeia_auth/routes/email_verify.py`

**Endpoints:**
- `POST /email/send-verification` — (authenticated) sends verification code
- `POST /email/verify` — takes code, marks `email_verified=True`

**Logic:**
- Generate 6-digit code, send via Twilio Verify (email channel)
- 10-min expiry
- Audit log: `AUTH_EMAIL_VERIFIED`

### Feature 3: Session Management
**New file:** `hodeia_auth/routes/sessions.py`

**Endpoints:**
- `GET /sessions` — (authenticated) list active refresh tokens for current user (id, created_at, last_used, user_agent)
- `DELETE /sessions/:id` — (authenticated) revoke specific session
- `DELETE /sessions` — (authenticated) revoke all sessions except current

### Feature 4: Expose Revoke-All Route
**File:** `hodeia_auth/routes/token.py`

**Endpoint:**
- `POST /token/revoke-all` — (authenticated) revokes all refresh tokens for current user

Uses existing `revoke_all_user_tokens()` from `services/token.py`.

### Feature 5: Fix Test Suite
**Files:** `hodeia_auth/tests/conftest.py`, `hodeia_auth/tests/test_routes.py`, `hodeia_auth/tests/test_token_service.py`

Fix the 32 PermissionError failures:
- Use mock transport for SQLite thread safety (TestClient runs in different thread)
- Fix JWT invalid signature test — verify correct exception type
- All 75+ tests must pass

## Acceptance Criteria
- [ ] `slowapi` rate limiting active on login, register, MFA verify, token refresh, admin reset
- [ ] Admin secret loaded from `HODEIA_ADMIN_SECRET` env var, hardcoded value removed
- [ ] OAuth/dev-login users created with `password_hash=None`
- [ ] `POST /password/forgot` and `POST /password/reset` work end-to-end
- [ ] `POST /email/send-verification` and `POST /email/verify` work end-to-end
- [ ] `GET /sessions`, `DELETE /sessions/:id`, `DELETE /sessions` work
- [ ] `POST /token/revoke-all` works
- [ ] All existing tests pass + new tests for new endpoints
- [ ] No hardcoded secrets anywhere in codebase

## Smoke Test
```bash
pytest hodeia_auth/tests/ -v
# All tests pass, 0 failures, 0 errors
```

## Constraints
- Do NOT change JWT algorithm or key format
- Do NOT break existing login/register/OAuth flows
- Do NOT add new pip dependencies beyond `slowapi`
- Keep route file convention: one file per feature area
- All new routes must emit audit events
- Password reset codes must be hashed in DB (not plaintext)
