# TASK-002: ra96it Auth MVP — Register, Login, MFA, JWT

## Objective

Build the ra96it authentication service MVP inside the shiftcenter monorepo. This is a standalone FastAPI service at `ra96it/` that handles user registration, login with MFA, and JWT token lifecycle. Every other service in the platform depends on ra96it for identity.

## Dependencies

- **TASK-001 (Event Ledger)** must complete first. This task imports `hivenode.ledger.writer` to emit audit events from every auth endpoint.

## Context

ra96it is the identity provider for all ShiftCenter products. It issues JWTs that other services (hivenode, browser, engine) validate. The architecture decisions are locked:

- **Framework:** FastAPI (already in pyproject.toml)
- **Database:** PostgreSQL on Railway (production), SQLite for local dev/tests
- **JWT:** RS256 asymmetric signing. ra96it holds the private key, consumers verify with the public key. Access tokens expire in 15 minutes.
- **Refresh tokens:** Opaque tokens stored in DB. Single-use with rotation — issuing a new access token consumes the old refresh token and issues a new one. 30-day expiry.
- **Passwords:** bcrypt via passlib
- **MFA:** Required for all users. SMS + email codes via Twilio Verify API. 6-digit codes, 5-minute expiry.
- **User tiers:** admin, alpha, beta, regular, paid (stored on user model, no enforcement logic in this task)

## MVP Scope — What to Build

Five endpoints:

| Method | Path | Description |
|--------|------|-------------|
| POST | `/register` | Create account (email, password, display_name). Returns user_id. Does NOT issue tokens — user must verify MFA first. |
| POST | `/login` | Email + password → triggers MFA code send (SMS or email based on user preference). Returns `mfa_pending` status + `login_session_id` (short-lived, 10 min). |
| POST | `/mfa/verify` | `login_session_id` + `code` → verifies MFA code, issues access_token + refresh_token. This is the only endpoint that issues tokens. |
| POST | `/token/refresh` | `refresh_token` → rotates: consumes old refresh token, issues new access_token + new refresh_token. Rejects reused tokens (replay detection). |
| POST | `/token/revoke` | `refresh_token` → revokes token (logout). Returns 200 even if token already revoked (idempotent). |

## What NOT to Build

- No GitHub OAuth (future task, gated behind MFA)
- No cross-app SSO redirect flow (future task)
- No bot tokens / chat tokens / utility tokens (future task)
- No Four-Vector identity system
- No social graph
- No alias system
- No tier enforcement middleware (just store the tier on the user model)
- No email verification flow (future — MVP trusts email at registration)
- No rate limiting (future)
- No frontend code

## Database Schema

Three tables. Use SQLAlchemy 2.0 mapped_column style.

### users
```
id              UUID PRIMARY KEY (uuid4)
email           TEXT NOT NULL UNIQUE
password_hash   TEXT NOT NULL
display_name    TEXT NOT NULL
tier            TEXT NOT NULL DEFAULT 'regular' CHECK(tier IN ('admin','alpha','beta','regular','paid'))
mfa_method      TEXT NOT NULL DEFAULT 'email' CHECK(mfa_method IN ('sms','email'))
phone           TEXT          -- required if mfa_method='sms', nullable otherwise
mfa_verified    BOOLEAN NOT NULL DEFAULT FALSE  -- has user completed MFA setup
created_at      TIMESTAMP NOT NULL DEFAULT now()
updated_at      TIMESTAMP NOT NULL DEFAULT now()
```

### refresh_tokens
```
id              UUID PRIMARY KEY (uuid4)
user_id         UUID NOT NULL REFERENCES users(id)
token_hash      TEXT NOT NULL UNIQUE  -- SHA-256 hash of the opaque token (never store raw)
expires_at      TIMESTAMP NOT NULL
consumed_at     TIMESTAMP            -- set when token is rotated (single-use detection)
revoked_at      TIMESTAMP            -- set when explicitly revoked
created_at      TIMESTAMP NOT NULL DEFAULT now()
```

A refresh token is valid if: `consumed_at IS NULL AND revoked_at IS NULL AND expires_at > now()`.

If a consumed token is presented again (replay), revoke ALL refresh tokens for that user (token family breach).

### login_sessions
```
id              UUID PRIMARY KEY (uuid4)
user_id         UUID NOT NULL REFERENCES users(id)
mfa_code_hash   TEXT NOT NULL  -- SHA-256 hash of the 6-digit code
mfa_method      TEXT NOT NULL  -- 'sms' or 'email'
expires_at      TIMESTAMP NOT NULL  -- 10 minutes from creation
verified_at     TIMESTAMP           -- set when MFA code verified
created_at      TIMESTAMP NOT NULL DEFAULT now()
```

## JWT Claims

Access token payload (RS256, 15-min expiry):
```json
{
  "sub": "<user_id uuid>",
  "email": "<email>",
  "tier": "<tier>",
  "iat": 1234567890,
  "exp": 1234568790,
  "iss": "ra96it",
  "aud": "shiftcenter"
}
```

## File Structure

```
ra96it/
├── __init__.py            -- (exists, empty)
├── main.py                -- FastAPI app, mount routes, lifespan (create tables)
├── config.py              -- Settings via pydantic-settings (DB URL, JWT keys, Twilio creds)
├── db.py                  -- async engine, session factory, Base
├── models.py              -- SQLAlchemy models: User, RefreshToken, LoginSession
├── schemas.py             -- Pydantic request/response models for all 5 endpoints
├── services/
│   ├── __init__.py
│   ├── password.py        -- hash_password(), verify_password() via passlib+bcrypt
│   ├── jwt.py             -- create_access_token(), decode_access_token(), load RS256 keys
│   ├── mfa.py             -- send_mfa_code(), verify_mfa_code() via Twilio Verify
│   ├── token.py           -- issue_refresh_token(), rotate_refresh_token(), revoke_refresh_token(), revoke_all_user_tokens()
│   └── audit.py           -- emit_auth_event() wrapper around hivenode.ledger.writer
├── routes/
│   ├── __init__.py
│   ├── register.py        -- POST /register
│   ├── login.py           -- POST /login
│   ├── mfa.py             -- POST /mfa/verify
│   └── token.py           -- POST /token/refresh, POST /token/revoke
```

```
tests/ra96it/
├── __init__.py
├── conftest.py            -- test DB fixture (SQLite in-memory), test client, RSA key pair fixture
├── test_models.py         -- model creation, constraints, defaults
├── test_password.py       -- hash + verify, reject wrong password
├── test_jwt.py            -- create + decode, expiry, wrong key rejection, claim validation
├── test_register.py       -- happy path, duplicate email, missing fields, invalid tier
├── test_login.py          -- happy path (triggers MFA), wrong password, unknown email
├── test_mfa.py            -- happy path (tokens issued), wrong code, expired session, replay
├── test_token_refresh.py  -- happy path (rotation), expired token, consumed token (replay → revoke all), revoked token
├── test_token_revoke.py   -- happy path, idempotent revoke, unknown token
├── test_audit.py          -- verify ledger events emitted for each auth action
```

## Dependencies

Add to pyproject.toml `dependencies` (or note them for bee to add):
- `pyjwt[crypto]>=2.8` — JWT with RS256 support
- `passlib[bcrypt]>=1.7` — password hashing
- `cryptography>=42.0` — RSA key operations (pyjwt dependency for RS256)
- `pydantic-settings>=2.0` — config from environment
- `twilio>=9.0` — Twilio Verify API for MFA

For tests only (already in dev deps):
- `pytest`, `pytest-asyncio`, `httpx` (already present)

## Key Implementation Details

### RS256 Key Handling
- For tests: generate an ephemeral RSA 2048-bit key pair in conftest.py
- For production: read PEM files from paths in config (`RA96IT_JWT_PRIVATE_KEY_PATH`, `RA96IT_JWT_PUBLIC_KEY_PATH`)
- The config should also support `RA96IT_JWT_PRIVATE_KEY` as a raw PEM string (for Railway env vars)

### Twilio MFA
- Use Twilio Verify service (not raw SMS). Service SID in config.
- For tests: mock the Twilio client entirely. No real SMS in tests.
- `send_mfa_code(phone_or_email, method)` → calls Twilio Verify
- `verify_mfa_code(phone_or_email, code, method)` → calls Twilio Verify check

### Refresh Token Rotation
- Generate 32-byte random token (secrets.token_urlsafe)
- Store SHA-256 hash in DB, return raw token to client
- On refresh: look up hash, verify not consumed/revoked/expired, mark consumed, issue new pair
- On replay (consumed token presented): revoke ALL tokens for that user (breach detection)

### Password Hashing
- Use passlib CryptContext with bcrypt scheme
- Hash on register, verify on login

### Event Ledger Integration
Every auth action MUST emit to the Event Ledger via `hivenode.ledger.writer`. This is the audit trail — every authentication event is recorded. Create `ra96it/services/audit.py` to wrap the ledger writer with auth-specific helpers.

Events to emit (use these as `event_type` values):

| event_type | actor | When |
|------------|-------|------|
| `auth.register` | `human:<user_id>` | User registers successfully |
| `auth.login.success` | `human:<user_id>` | Password verified, MFA sent |
| `auth.login.failure` | `system:ra96it` | Wrong password (target = attempted email) |
| `auth.mfa.verify` | `human:<user_id>` | MFA code verified, tokens issued |
| `auth.mfa.failure` | `system:ra96it` | Wrong MFA code (target = `login_session:<id>`) |
| `auth.token.issue` | `system:ra96it` | Access + refresh tokens issued (target = `human:<user_id>`) |
| `auth.token.refresh` | `human:<user_id>` | Refresh token rotated |
| `auth.token.revoke` | `human:<user_id>` | Refresh token revoked (logout) |
| `auth.token.replay` | `system:ra96it` | Consumed refresh token reused — breach detected, all tokens revoked (target = `human:<user_id>`) |

All events use:
- `domain`: `"auth"`
- `signal_type`: `"internal"`
- `payload_json`: JSON with relevant context (endpoint, IP if available, session_id, etc.)

For tests: the conftest.py fixture must set up an in-memory Event Ledger DB alongside the auth DB. Tests should verify that the correct events are emitted (query the ledger after each endpoint call).

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Minimum 40 tests across all test files
- [ ] Edge cases: duplicate email registration, wrong password, expired MFA, replay MFA code, refresh token replay (revoke-all trigger), expired refresh token, expired access token, invalid JWT signature, malformed requests

## Constraints

- Python 3.13
- SQLite for tests (in-memory), PostgreSQL-compatible schema (SQLAlchemy handles both)
- No file over 500 lines
- No stubs — every function fully implemented
- No external API calls in tests (mock Twilio)
- All timestamps in UTC
- All IDs are UUID4

## Files to Read First

- `pyproject.toml` — current dependencies
- `ra96it/__init__.py` — existing package (empty)
- `hivenode/ledger/schema.py` — Event Ledger schema (from TASK-001)
- `hivenode/ledger/writer.py` — Event Ledger write interface (from TASK-001) — you MUST use this to emit auth events

## Deliverables

- [ ] `ra96it/main.py`
- [ ] `ra96it/config.py`
- [ ] `ra96it/db.py`
- [ ] `ra96it/models.py`
- [ ] `ra96it/schemas.py`
- [ ] `ra96it/services/__init__.py`
- [ ] `ra96it/services/password.py`
- [ ] `ra96it/services/jwt.py`
- [ ] `ra96it/services/mfa.py`
- [ ] `ra96it/services/token.py`
- [ ] `ra96it/services/audit.py`
- [ ] `ra96it/routes/__init__.py`
- [ ] `ra96it/routes/register.py`
- [ ] `ra96it/routes/login.py`
- [ ] `ra96it/routes/mfa.py`
- [ ] `ra96it/routes/token.py`
- [ ] `tests/ra96it/__init__.py`
- [ ] `tests/ra96it/conftest.py`
- [ ] `tests/ra96it/test_models.py`
- [ ] `tests/ra96it/test_password.py`
- [ ] `tests/ra96it/test_jwt.py`
- [ ] `tests/ra96it/test_register.py`
- [ ] `tests/ra96it/test_login.py`
- [ ] `tests/ra96it/test_mfa.py`
- [ ] `tests/ra96it/test_token_refresh.py`
- [ ] `tests/ra96it/test_token_revoke.py`
- [ ] `tests/ra96it/test_audit.py`
- [ ] Updated `pyproject.toml` with new dependencies

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-002-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** -- task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** -- every file created/modified/deleted, full paths
3. **What Was Done** -- bullet list of concrete changes
4. **Test Results** -- test files run, pass/fail counts
5. **Build Verification** -- pytest output summary
6. **Acceptance Criteria** -- copy deliverables above, mark [x] or [ ]
7. **Clock / Cost / Carbon** -- all three, never omit any
8. **Issues / Follow-ups** -- edge cases, dependencies, recommended next tasks

DO NOT skip any section. A response without all 8 sections is incomplete.
