# TASK-134: ra96it SSO Phase 2 — Federation Service (Backend)

## Objective

Build the ra96it FastAPI federation service that acts as the token issuer for the deiasolutions website family. Trusts Efemera's GitHub OAuth tokens and issues family-wide JWTs. This is a **separate service** in the ra96it repo, not part of shiftcenter/hivenode.

## Context

This is Phase 2 of the ra96it SSO federation system:
1. **Phase 1 (TASK-133):** Login page + auth store (browser-only) — COMPLETE
2. **Phase 2 (this task):** ra96it service (backend, separate repo)
3. **Phase 3 (TASK-135):** Wire ShiftCenter to ra96it (backend + frontend integration)

The ra96it service sits between Efemera's GitHub OAuth and the deiasolutions app family. It validates Efemera tokens, stores user identity, and issues JWT tokens scoped to the family (`shiftcenter.com`, `efemera.live`, `deiasolutions.org`).

## Dependencies

- **Efemera GitHub OAuth** (already exists) — provides user identity via GitHub
- **TASK-002** (ra96it Auth MVP) — reference implementation for JWT handling, but this task is simpler (no MFA, no refresh tokens initially)

## Repository Location

**CRITICAL:** This code goes in the **ra96it repo**, NOT the shiftcenter repo.

- **Repo path:** `C:\Users\davee\OneDrive\Documents\GitHub\ra96it`
- **Service directory:** `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\`
- **Tests directory:** `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\tests\`

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-14-2200-SPEC-ra96it-sso-federation.md` — full spec
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\_archive\2026-03-10-TASK-002-RA96IT-AUTH-MVP.md` — reference JWT implementation
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py` — verify_jwt() pattern (what consumers expect)

## Deliverables

### Service Files

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\main.py` — FastAPI app entry point
  - CORS middleware for cross-origin requests (allow shiftcenter.com, efemera.live, localhost:5174)
  - Mount all routes
  - Lifespan context manager (create DB tables on startup)

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\config.py` — Configuration via pydantic-settings
  - `DATABASE_URL` — PostgreSQL for prod, SQLite for dev/tests
  - `JWT_PRIVATE_KEY_PATH` — path to RS256 private key PEM
  - `JWT_PUBLIC_KEY_PATH` — path to RS256 public key PEM
  - `JWT_PRIVATE_KEY` — raw PEM string (alternative to file path, for Railway env vars)
  - `JWT_PUBLIC_KEY` — raw PEM string (alternative to file path)
  - `EFEMERA_API_URL` — Efemera API endpoint (for token exchange)
  - `EFEMERA_CLIENT_ID` — GitHub OAuth app client ID (for validation)
  - `EFEMERA_CLIENT_SECRET` — GitHub OAuth app secret (for validation)
  - `PORT` — service port (default 8421, Railway reads from $PORT)
  - `MODE` — "local" | "cloud" (local bypasses some checks)

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\db.py` — SQLAlchemy setup
  - Async engine (asyncpg for PostgreSQL, aiosqlite for SQLite)
  - Session factory
  - Base class for models

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\models.py` — SQLAlchemy models
  - `User` table:
    - `id` — UUID primary key
    - `provider` — TEXT ("github" for now)
    - `provider_id` — TEXT (GitHub user ID)
    - `email` — TEXT UNIQUE
    - `display_name` — TEXT
    - `created_at` — TIMESTAMP
    - `updated_at` — TIMESTAMP
  - Index on `(provider, provider_id)` — UNIQUE

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\schemas.py` — Pydantic request/response models
  - `TokenExchangeRequest` — { efemera_token: str }
  - `TokenExchangeResponse` — { access_token: str, token_type: "Bearer", expires_in: int }
  - `TokenValidateRequest` — { token: str }
  - `TokenValidateResponse` — { valid: bool, claims: dict }
  - `TokenRefreshRequest` — { token: str } (future — not in MVP)
  - `TokenRefreshResponse` — { access_token: str } (future — not in MVP)
  - `UserInfoResponse` — { sub: str, email: str, display_name: str, provider: str }
  - `JWKSResponse` — { keys: list[dict] } (JWKS format)

### Services

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\services\jwt.py` — JWT operations
  - `load_private_key()` — load RS256 private key from config
  - `load_public_key()` — load RS256 public key from config
  - `create_access_token(user: User) -> str` — sign JWT with RS256, 24-hour expiry
  - `decode_access_token(token: str) -> dict` — verify + decode JWT
  - `get_jwks() -> dict` — return JWKS JSON (public key in JWK format)
  - Use PyJWT library (RS256 algorithm)

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\services\efemera.py` — Efemera token exchange
  - `validate_efemera_token(token: str) -> dict` — call Efemera API to validate token, return user profile
  - `exchange_efemera_token(token: str, db_session) -> User` — validate Efemera token, create/update user in DB, return User
  - HTTP calls via httpx (async)

### Routes

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\routes\authorize.py` — `GET /authorize`
  - Query params: `app` (required), `redirect` (required)
  - Check if user authenticated (cookie or session — future)
  - If authenticated: issue JWT, redirect to `{redirect}?token={jwt}`
  - If not authenticated: redirect to Efemera OAuth flow
  - **MVP simplification:** For now, return 501 Not Implemented with message "Use /token/exchange for direct token exchange"

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\routes\token.py` — Token operations
  - `POST /token/exchange` — exchange Efemera access_token for ra96it JWT
    - Request: `{ efemera_token: "..." }`
    - Validate Efemera token via Efemera API
    - Get user profile (GitHub ID, email, display_name)
    - Create/update user in DB
    - Issue JWT with claims: `{ sub: "github:{id}", email, display_name, iss: "ra96it.com", aud: "deiasolutions", scope: [...], provider: "github", provider_id: "{id}" }`
    - Return `{ access_token, token_type: "Bearer", expires_in: 86400 }`

  - `POST /token/validate` — validate a ra96it JWT
    - Request: `{ token: "..." }`
    - Decode + verify JWT signature
    - Return `{ valid: true, claims: {...} }` or `{ valid: false, error: "..." }`

  - `POST /token/refresh` — refresh a ra96it JWT (future — not in MVP)
    - Return 501 Not Implemented for now

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\routes\userinfo.py` — `GET /userinfo`
  - Requires valid JWT in Authorization header
  - Return user profile from JWT claims: `{ sub, email, display_name, provider }`

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\service\routes\jwks.py` — `GET /.well-known/jwks.json`
  - Return JWKS JSON with ra96it public key
  - Standard JWKS format (list of JWK objects)
  - Consumers use this to verify JWT signatures

### Dependencies File

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\pyproject.toml` — Python dependencies
  - `fastapi>=0.104`
  - `uvicorn[standard]>=0.24`
  - `sqlalchemy[asyncio]>=2.0`
  - `asyncpg>=0.29` (PostgreSQL async driver)
  - `aiosqlite>=0.19` (SQLite async driver)
  - `pydantic-settings>=2.0`
  - `pyjwt[crypto]>=2.8` (RS256 JWT)
  - `httpx>=0.25` (async HTTP client for Efemera API)
  - `python-multipart>=0.0.6` (form data handling)
  - Dev dependencies: `pytest>=7.4`, `pytest-asyncio>=0.21`, `httpx` (for TestClient)

### Configuration Files

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\.env.example` — Example environment variables
  - DATABASE_URL=sqlite+aiosqlite:///[REDACTED].db
  - JWT_PRIVATE_KEY_PATH=./keys/ra96it-private.pem
  - JWT_PUBLIC_KEY_PATH=./keys/ra96it-public.pem
  - EFEMERA_API_URL=https://efemera.live/api
  - EFEMERA_CLIENT_ID=your-github-oauth-app-id
  - EFEMERA_CLIENT_SECRET=your-github-oauth-app-secret
  - PORT=8421
  - MODE=local

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\README.md` — Service documentation
  - What is ra96it
  - Architecture diagram (text-based)
  - How to run locally
  - How to run tests
  - API endpoints documentation
  - JWT claims specification
  - Deployment notes

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Minimum 25 tests across all test files

### Test Files

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\tests\conftest.py`
  - Async test DB fixture (SQLite in-memory)
  - Test client fixture (FastAPI TestClient)
  - RSA key pair fixture (ephemeral keys for tests)
  - Mock Efemera API fixture (httpx-mock or similar)

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\tests\test_models.py`
  - User creation
  - Unique constraint on (provider, provider_id)
  - Email uniqueness
  - Timestamps auto-populate

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\tests\test_jwt.py`
  - Create access token
  - Decode access token
  - Verify signature with public key
  - Reject invalid signature
  - Reject expired token
  - JWKS generation

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\tests\test_token_exchange.py`
  - Happy path: valid Efemera token → ra96it JWT
  - User created in DB on first exchange
  - User updated in DB on subsequent exchange
  - Invalid Efemera token rejected
  - Missing token rejected
  - JWT claims match user profile

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\tests\test_token_validate.py`
  - Valid token → { valid: true, claims }
  - Invalid signature → { valid: false }
  - Expired token → { valid: false }
  - Malformed token → { valid: false }

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\tests\test_userinfo.py`
  - Valid JWT → user profile
  - Missing Authorization header → 401
  - Invalid JWT → 401

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\ra96it\tests\test_jwks.py`
  - GET /.well-known/jwks.json returns JWKS
  - JWKS contains public key in JWK format
  - JWKS keys array is not empty

## Acceptance Criteria

- [ ] `POST /token/exchange` accepts Efemera token, returns ra96it JWT
- [ ] JWT contains correct claims: `{ sub: "github:{id}", email, display_name, iss: "ra96it.com", aud: "deiasolutions", scope: [...], provider: "github", provider_id: "{id}" }`
- [ ] JWT signed with RS256 (asymmetric — ra96it signs, consumers verify)
- [ ] JWT expires in 24 hours (86400 seconds)
- [ ] `POST /token/validate` verifies JWT signature and returns claims
- [ ] `GET /userinfo` returns user profile from JWT claims
- [ ] `GET /.well-known/jwks.json` returns public key in JWKS format
- [ ] User identity stored in PostgreSQL (production) or SQLite (dev/tests)
- [ ] Efemera token validation works (calls Efemera API)
- [ ] CORS configured for shiftcenter.com, efemera.live, localhost:5174
- [ ] All 25+ tests pass
- [ ] No file over 500 lines
- [ ] No stubs — all endpoints fully implemented
- [ ] No hardcoded secrets in source code (use env vars)

## Constraints

- **No file over 500 lines.** Modularize at 500. Hard limit: 1,000.
- **TDD.** Tests first, then implementation. No exceptions.
- **NO STUBS.** Every function fully implemented. No `// TODO`, no empty bodies.
- **No hardcoded secrets.** All secrets in environment variables.
- **Python 3.13** (or compatible with 3.11+)
- **SQLite for tests** (in-memory), **PostgreSQL-compatible schema** (SQLAlchemy handles both)
- **RS256 JWT signing** (asymmetric — private key signs, public key verifies)
- **24-hour JWT expiry** (no refresh tokens in MVP — Phase 3 will add them)

## Implementation Notes

### JWT Claims Specification

```json
{
  "sub": "github:12345",
  "email": "user@example.com",
  "display_name": "Dave",
  "iss": "ra96it.com",
  "aud": "deiasolutions",
  "iat": 1710000000,
  "exp": 1710086400,
  "scope": ["shiftcenter", "efemera", "deiasolutions"],
  "provider": "github",
  "provider_id": "12345"
}
```

### Efemera Token Exchange Flow

1. Client (ShiftCenter browser) has Efemera access_token from GitHub OAuth
2. Client calls `POST /token/exchange` with `{ efemera_token: "..." }`
3. ra96it calls Efemera API: `GET /api/auth/user` with `Authorization: Bearer {efemera_token}`
4. Efemera returns user profile: `{ id: "12345", email: "...", display_name: "..." }`
5. ra96it looks up user in DB by `(provider="github", provider_id="12345")`
6. If not found: create user. If found: update `display_name`, `email`, `updated_at`
7. ra96it issues JWT with user claims
8. ra96it returns `{ access_token: "...", token_type: "Bearer", expires_in: 86400 }`

### JWKS Format

Example JWKS response:

```json
{
  "keys": [
    {
      "kty": "RSA",
      "use": "sig",
      "kid": "ra96it-2024",
      "n": "...",
      "e": "AQAB"
    }
  ]
}
```

Use PyJWT's `jwk.PyJWK.from_dict()` or similar to generate JWK from RSA public key.

### RSA Key Generation (For Dev/Test)

Generate keys for local development:

```bash
# Private key
openssl genrsa -out keys/ra96it-private.pem 2048

# Public key
openssl rsa -in keys/ra96it-private.pem -pubout -out keys/ra96it-public.pem
```

For tests, generate ephemeral keys in conftest.py using `cryptography` library.

### Dev Mode Bypass

In `MODE=local`, skip Efemera token validation and accept any token. Return stub user profile for testing.

### CORS Configuration

Allow these origins:
- `https://code.shiftcenter.com`
- `https://pm.shiftcenter.com`
- `https://chat.efemera.live`
- `http://localhost:5174`
- `http://localhost:3000`

Allow methods: GET, POST, OPTIONS
Allow headers: Authorization, Content-Type

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-134-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — pytest output summary
6. **Acceptance Criteria** — copy from above, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, recommended next tasks

DO NOT skip any section. A response without all 8 sections is incomplete.
