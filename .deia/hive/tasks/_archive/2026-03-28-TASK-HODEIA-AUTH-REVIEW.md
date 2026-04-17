# BRIEFING: Hodeia Auth — Playwright Tests + Code Review

**From:** Q33NR
**To:** Q33N (bee dispatch)
**Date:** 2026-03-28
**Priority:** P1

## Objective

Full code review and test coverage assessment of `hodeia_auth/` — the standalone FastAPI auth service for hodeia.me (cross-app SSO).

## Scope

### 1. Code Review
- Review all files in `hodeia_auth/` for security, correctness, and completeness
- Check: JWT handling, password hashing, OAuth flow, MFA implementation
- Check: SQL injection prevention, input validation, error handling
- Check: CORS config, token expiration, refresh token flow
- Check: Are all routes wired up in `main.py`?
- Check: Are there any hardcoded secrets, debug flags, or dev-only bypasses left in?
- Report: What's implemented, what's stubbed, what's missing

### 2. Write Playwright E2E Tests
- Target the LIVE auth service at `https://hodeia.me`
- Test the full auth flow as a user would experience it:
  - Landing page loads
  - Login form renders
  - Invalid credentials show error
  - Dev-login flow (if available)
  - OAuth redirect initiation (GitHub)
  - Token in URL gets extracted correctly
  - JWKS endpoint returns valid keys
- Use `browser/e2e/` directory for test files
- Name: `hodeia-auth.spec.ts`

### 3. Write Unit Tests
- Create `hodeia_auth/tests/` with proper pytest tests
- Test token service (JWT creation, validation, expiry)
- Test password hashing (hash + verify)
- Test schema validation
- Test route handlers with TestClient

## Files to Review
```
hodeia_auth/
├── main.py              # FastAPI app entry
├── config.py            # Settings/env vars
├── db.py                # Database setup
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── dependencies.py      # Auth dependencies
├── routes/
│   ├── login.py         # Login flow
│   ├── register.py      # Registration
│   ├── oauth.py         # OAuth (GitHub)
│   ├── token.py         # Token refresh
│   ├── jwks.py          # JWKS endpoint
│   ├── mfa.py           # MFA verification
│   ├── mfa_setup.py     # MFA enrollment
│   ├── profile.py       # User profile
│   ├── dev_login.py     # Dev/local login bypass
│   └── recovery_email.py # Password recovery
├── services/
│   ├── jwt.py           # JWT creation/validation
│   ├── password.py      # Password hashing
│   ├── github.py        # GitHub OAuth client
│   ├── mfa.py           # MFA (TOTP) logic
│   ├── token.py         # Token management
│   └── audit.py         # Audit logging
└── tests/               # Currently empty
```

## Deliverables

1. **Code review report** — markdown summary of findings, issues, and recommendations
2. **Playwright E2E tests** — `browser/e2e/hodeia-auth.spec.ts`
3. **Python unit tests** — `hodeia_auth/tests/test_*.py` files
4. **Bug list** — any security issues or bugs found, formatted for `inventory.py bug add`

## Response Format

Write response to `.deia/hive/responses/20260328-HODEIA-AUTH-REVIEW.md`
