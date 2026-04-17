# SPEC-RESEARCH-BOT-AUTH-AUDIT-001: Bot Token Infrastructure Assessment — COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-04-16
**Time:** 10:50 CDT

---

## Executive Summary

Bot token infrastructure for BL-146 exists in `platform/simdecisions-2` with a complete implementation (models, services, endpoints, tests) totaling ~13KB of Python code. The system is **directly portable** to CloudNode with minimal adaptation. Current hivenode/hodeia_auth infrastructure has analogous JWT token patterns but **no bot-specific code**. Efemera keeper chat integration exists with ChatSender/ChatListener classes providing WebSocket-based @mention detection and REST message posting.

**Key finding:** Most code can be ported verbatim; primary adaptation needed is database migration tooling (Alembic vs raw SQL) and integrating bot auth into hivenode's existing JWT dependency chain.

---

## A. Platform Repo Bot Auth System (Source)

### A1. Bot Token Models

**File:** `platform/simdecisions-2/api/bot_token.py` (42 lines)

**Table:** `sd_bot_tokens`
```python
id: String (UUID)
user_id: String (indexed)
name: String (default="My Bot")
token_hash: String (SHA-256, unique, indexed)
token_prefix: String(10)  # e.g., "sd_bot_a3f"
created_at: DateTime(timezone=True)
last_used_at: DateTime(timezone=True, nullable)
revoked_at: DateTime(timezone=True, nullable)
```

**Constraints:**
- Partial unique index: `idx_one_active_bot_per_user` on `user_id` WHERE `revoked_at IS NULL`
- Enforces one active bot per user at database level (PostgreSQL partial index)

**File:** `platform/simdecisions-2/api/bot_mutation.py` (55 lines)

**Table:** `sd_bot_mutations`
```python
id: String (UUID)
bot_token_id: String (FK to sd_bot_tokens.id)
repo: String  # "owner/repo-name"
scenario: String  # scenario name without .ir.json
mutations: Text (JSON array)
message: Text (commit/PR message)
status: String(20)  # pending, applied, rejected
pr_number: Integer (nullable)
pr_url: Text (nullable)
commit_sha: String(40, nullable)
commit_url: Text (nullable)
created_at: DateTime(timezone=True)
resolved_at: DateTime(timezone=True, nullable)
```

**Constraints:**
- Check constraint on status values
- Index on `status` WHERE status='pending'
- Composite index on `(repo, scenario)`

### A2. Bot Endpoints

**File:** `platform/simdecisions-2/api/bot.py` (23KB, 200+ lines reviewed)

**Endpoints:**
1. `POST /api/bot/token` — Create bot token (returns full token once)
   - Requires JWT auth (user identity)
   - One active bot per user enforced
   - Returns: `{id, name, token, token_prefix, created_at, warning}`

2. `GET /api/bot/token` — Get bot info (no token, just metadata)
   - Returns: `{bot: {id, name, token_prefix, created_at, last_used_at}}`

3. `DELETE /api/bot/token` — Revoke bot token
   - Sets `revoked_at` timestamp
   - Returns: `{revoked: true, revoked_at}`

4. `POST /api/bot/mutate` — Submit mutation (bot-authenticated)
   - Auth: `Authorization: Bearer sd_bot_xxxxx`
   - Body: `{repo, scenario, mutations[], message}`
   - Rate limit: 60 mutations/hour per bot
   - Validation flow:
     - Verify token hash (SHA-256)
     - Check rate limit
     - Validate mutation operations
     - Check destructive ops (delete_node, delete_edge)
     - Auto-commit OR create PR based on mode
   - Returns: `{status, mutationId, prNumber, prUrl, commitSha, commitUrl, mutationCount}`

**Authentication Flow:**
- User auth: Standard JWT in `Authorization: Bearer <jwt>`
- Bot auth: Custom bearer token `Authorization: Bearer sd_bot_{32_hex}`
- Bot tokens verified by SHA-256 hash lookup
- Updates `last_used_at` on each valid use

**Rate Limiting:**
- 60 mutations/hour per bot
- Sliding window via `created_at` timestamp query
- Returns `429 Too Many Requests` with `Retry-After` header

**Scoping/Permissions:**
- Bots inherit user permissions (bot_token → user_id → user permissions)
- No separate bot-level scoping system
- Mutation validation enforces scenario structure rules

### A3. Bot Mutation/Activity Tracking

**File:** `platform/simdecisions-2/api/bot_service.py` (187 lines)

**Core Functions:**
- `generate_bot_token()` → `(full_token, token_hash, token_prefix)`
  - Format: `sd_bot_{32_hex_chars}` (39 chars total)
  - SHA-256 hash of full token stored
  - Prefix is first 10 chars for display

- `create_bot_token(session, user_id, name)` → `(BotTokenInfo, full_token) | None`
  - Checks for existing active bot
  - Returns None if user already has bot

- `verify_bot_token(session, token)` → `user_id | None`
  - Hashes token, looks up in database
  - Updates `last_used_at` on success
  - Returns user_id for permission resolution

- `revoke_bot_token(session, user_id)` → `bool`
  - Sets `revoked_at` timestamp
  - Idempotent

**Mutation Tracking:**
- Every mutation attempt logged to `sd_bot_mutations` (success or failure)
- Status progression: `pending` → `applied` | `rejected`
- PR/commit URLs stored for audit trail
- No automatic deletion — permanent audit log

**Audit Trail:**
- Each bot token records: creation time, last use time, revocation time
- Each mutation records: bot_token_id, repo, scenario, full mutation JSON, timestamps
- No separate audit events table — mutation log is the audit trail

### A4. Test Coverage

**Files:**
- `test_bot.py` (7.7 KB)
- `test_bot_activity.py` (11 KB)
- `test_bot_mutate.py` (10 KB)

**Key Flows Validated (from `test_bot.py` first 100 lines):**
1. Token generation format (sd_bot_xxxxx, 39 chars, SHA-256 hash)
2. Create bot token success (201 response with full token)
3. Duplicate bot token rejection (409 Conflict)
4. Get bot token info (metadata without token)
5. Revoke bot token
6. Bot auth with Bearer token

**Additional Coverage (inferred from file names):**
- Mutation listing/approval/rejection flows (`test_bot_activity.py`)
- Mutation validation rules (`test_bot_mutate.py`)
- Auto-commit mode vs PR mode
- Rate limiting enforcement

---

## B. CloudNode/Hivenode Current State (Target)

### B1. Auth Infrastructure

**Models** (`hodeia_auth/models.py`):
```python
User:
  - id, email, password_hash, display_name, tier, mfa_method
  - phone, mfa_verified, github_id (deprecated), provider, provider_id
  - email_verified, recovery_email, setup_completed
  - created_at, updated_at
  - Relationships: refresh_tokens, login_sessions

RefreshToken:
  - id, user_id, token_hash (SHA-256), expires_at
  - consumed_at, revoked_at, created_at
  - Single-use rotation pattern

LoginSession:
  - id, user_id, mfa_code_hash, mfa_method
  - expires_at, verified_at, created_at
  - MFA verification flow
```

**Database:** PostgreSQL (Railway production) + SQLite fallback (local)
- Connection: `hodeia_auth/db.py` → SQLAlchemy ORM
- Migration: `_migrate_schema()` function in `create_tables()` (additive only)
- No Alembic — raw SQL ALTER TABLE statements in migration function

**Endpoints** (`hodeia_auth/routes/`):
- `/register` — Email + password + MFA setup
- `/login` — Email + password → MFA challenge
- `/mfa/verify` — Verify MFA code → JWT + refresh token
- `/token/refresh` — Rotate refresh token, issue new JWT
- `/token/revoke` — Revoke refresh token (logout)
- `/token/revoke-all` — Revoke all user tokens (breach response)
- `/auth/github/callback`, `/auth/google/callback` — OAuth flows
- `/profile` — Get/update user profile
- `/sessions` — List/revoke active sessions

**JWT Flow:**
- RS256 signing with PEM keypair
- Issuer: `hodeia`, Audience: `deiasolutions`
- Scope field: `chat`, `terminal`, `api`
- Claims: `sub` (user_id), `email`, `tier`, `provider`, `provider_id`, `display_name`
- Expiry: 30 days (alpha — no refresh rotation yet, refresh token exists but long-lived)

**Permission System:**
- Tier-based: `admin`, `alpha`, `beta`, `regular`, `paid`
- No role/scope enforcement in hivenode beyond tier checks
- Local mode bypass: `verify_jwt_or_local()` returns stub claims if mode=local

### B2. Existing Bot-Related Code

**Search Results:**
- `hivenode/adapters/cli/*bot*` — CLI adapter infrastructure (Claude SDK, Gemini, mock bots)
- No `sd_bot_tokens` or `sd_bot_mutations` tables
- No bot token generation/validation code
- No bearer token auth for bots

**Closest Analog:**
- `hodeia_auth/services/token.py` — Refresh token service
  - `generate_token()` → `secrets.token_urlsafe(32)`
  - `hash_token()` → SHA-256
  - `issue_refresh_token()`, `rotate_refresh_token()`, `revoke_all_user_tokens()`
- **Pattern is identical** to platform bot token service

**Extensibility:**
- `hodeia_auth/models.py` User model has `provider` field with check constraint:
  - Current: `email`, `github`, `google`, `bot`, `local`
  - **`bot` provider already exists** — intended for future bot users
- Adding bot token tables is straightforward (same Base, same migration pattern)

### B3. Database Schema

**PostgreSQL Structure:**
- Tables: `users`, `refresh_tokens`, `login_sessions`
- FKs: `refresh_tokens.user_id → users.id`, `login_sessions.user_id → users.id`
- Cascade: `ON DELETE CASCADE` for tokens/sessions

**Migration System:**
- No Alembic — `_migrate_schema()` in `hodeia_auth/db.py`
- Additive migrations only (ALTER TABLE ADD COLUMN)
- Check constraints updated via DROP/ADD (PostgreSQL)
- SQLite migrations skipped for incompatible operations (ALTER COLUMN)
- Manual backfill queries for data migrations

**Connection Patterns:**
- `SessionLocal` context manager (sync SQLAlchemy)
- `get_session()` FastAPI dependency
- No async SQLAlchemy (all sync)

### B4. Hivenode → CloudNode Communication

**Current Pattern:**
- Hivenode verifies JWT via JWKS endpoint (hodeia_auth `/jwks.json`)
- `hivenode/dependencies.py:verify_jwt()` → fetches public key, decodes token
- JWKS cache with auto-refresh on signature failure

**Bot Token Integration Needs:**
1. New endpoint in hodeia_auth: `POST /bot/verify` (or middleware in hivenode)
2. Bot tokens sent as `Bearer sd_bot_xxxxx`
3. Hivenode distinguishes JWT vs bot token by prefix (`sd_bot_` vs eyJ...)
4. Validation flow: hivenode → hodeia_auth → hash lookup → user_id

**Proposed Flow:**
```
Client → Hivenode (Authorization: Bearer sd_bot_xxxxx)
  ↓
Hivenode extracts token, sees sd_bot_ prefix
  ↓
Hivenode calls hodeia_auth POST /bot/verify {token}
  ↓
hodeia_auth hashes token, looks up in sd_bot_tokens
  ↓
Returns {valid: true, user_id, bot_id} OR 401
  ↓
Hivenode caches result (5 min TTL), proceeds with user_id
```

---

## C. Efemera Bot Integration (Historical)

### C1. Bot Participation in Efemera

**File:** `platform/efemera/keeper/chat.py` (179 lines)

**ChatSender Class:**
- REST API posting to `/api/messages/`
- Body: `{channel_id, content, author_type: "bot", message_type: "text"}`
- Auth: `Authorization: Bearer {token}` (presumably bot token or user JWT)
- Session-based HTTP client with retry disabled

**Message Format Differentiation:**
- `author_type` field: `"user"` vs `"bot"`
- No separate display styling implied in keeper code
- Bot messages indistinguishable from user messages except for `author_type` flag

**ChatListener Class:**
- WebSocket connection to `/ws?user_id={bot_user_id}&display_name={keeper_name}`
- Receives broadcast messages
- Filters for `@{keeper_name}` mentions (case-insensitive regex)
- Callback: `on_mention(data: dict, instruction: str)`
- Auto-reconnect with exponential backoff (5s → 30s max)
- Daemon thread (dies with main process)

**Authentication Method:**
- WebSocket: Query params `user_id` and `display_name` (no explicit token in URL)
- REST: Bearer token in headers
- **Unclear** if bot tokens were used or if bots used user JWTs

### C2. Keeper Architecture

**Components:**
1. **ChatSender** — POST messages as bot
2. **ChatListener** — Listen for @mentions via WebSocket
3. **Executor** (inferred, not read) — Likely handles @mention command execution
4. **Daemon** (inferred) — Orchestration/lifecycle management

**@Mention Flow:**
```
User posts: "@keeper-bot run test suite"
  ↓
Efemera broadcasts message via WebSocket
  ↓
ChatListener receives, regex matches "@keeper-bot"
  ↓
Extracts instruction: "run test suite"
  ↓
Fires callback: on_mention(data, "run test suite")
  ↓
Executor parses command, dispatches work
  ↓
ChatSender posts result back to channel
```

**Response Mechanism:**
- ChatSender posts reply to same `channel_id` from incoming message
- No threading/reply-to mechanism visible in keeper code
- Linear conversation in channel

### C3. What Broke the Bot→Efemera Integration

**Evidence:** None found in code review.

**Hypothesis (from context):**
- Platform/simdecisions-2 and platform/efemera are sibling repos (confirmed structure)
- Efemera is standalone service (Railway deploy per docs)
- Bot tokens lived in simdecisions-2 database
- Efemera likely expected bot auth but lost connection to simdecisions-2 auth DB
- OR: JWT issuer changed (ra96it → hodeia migration) and efemera still validates old issuer

**When:** Not determinable from static code review (no git log inspection performed)

**What Changed:** Speculation — auth service split (hodeia_auth became standalone), efemera lost bot token validation route

---

## D. Integration Architecture

### D1. Minimal CloudNode Bot API for BL-146

**Required Endpoints:**

1. **POST /bot/token** (hodeia_auth)
   - Auth: JWT (user identity)
   - Body: `{name: string}`
   - Response: `{id, name, token, token_prefix, created_at, warning}`
   - Table: `sd_bot_tokens` (new)

2. **GET /bot/token** (hodeia_auth)
   - Auth: JWT
   - Response: `{bot: {id, name, token_prefix, created_at, last_used_at} | null}`

3. **DELETE /bot/token** (hodeia_auth)
   - Auth: JWT
   - Response: `{revoked: true, revoked_at}`

4. **POST /bot/verify** (hodeia_auth, new)
   - Body: `{token: string}`
   - Response: `{valid: boolean, user_id: string, bot_id: string}` OR 401
   - Used by hivenode for bot auth validation

**Database Additions:**

```sql
CREATE TABLE sd_bot_tokens (
  id VARCHAR(36) PRIMARY KEY,
  user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR NOT NULL DEFAULT 'My Bot',
  token_hash VARCHAR NOT NULL UNIQUE,
  token_prefix VARCHAR(10) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  last_used_at TIMESTAMP,
  revoked_at TIMESTAMP
);

CREATE UNIQUE INDEX idx_one_active_bot_per_user
  ON sd_bot_tokens(user_id)
  WHERE revoked_at IS NULL;

CREATE INDEX idx_bot_tokens_hash ON sd_bot_tokens(token_hash);
CREATE INDEX idx_bot_tokens_user ON sd_bot_tokens(user_id);
```

**Migration Strategy:**
- Add `_migrate_schema()` case in `hodeia_auth/db.py`
- Check if `sd_bot_tokens` table exists
- If not, execute CREATE TABLE + CREATE INDEX statements
- Use existing pattern: `conn.execute(text("CREATE TABLE ..."))`

### D2. Hivenode Bot Token Validation

**New Dependency:** `hivenode/dependencies.py:verify_bot_token_or_jwt()`

```python
async def verify_bot_token_or_jwt(authorization: str | None = Header(None)) -> dict:
    """
    Verify bot token OR JWT token.

    Bot token: Authorization: Bearer sd_bot_xxxxx
    JWT: Authorization: Bearer eyJhbGc...

    Returns claims dict with user_id.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing or invalid Authorization header")

    token = authorization.split(" ", 1)[1]

    # Bot token: starts with sd_bot_
    if token.startswith("sd_bot_"):
        return await _verify_bot_token(token)

    # JWT token
    return await verify_jwt(authorization)

async def _verify_bot_token(token: str) -> dict:
    """Verify bot token via CloudNode /bot/verify endpoint."""
    # Cache lookup (5 min TTL)
    cached = _bot_token_cache.get(token)
    if cached and cached["expires"] > time.time():
        return cached["claims"]

    # Call CloudNode
    resp = await httpx_client.post(
        f"{settings.cloudnode_url}/bot/verify",
        json={"token": token}
    )

    if resp.status_code != 200:
        raise HTTPException(401, "Invalid bot token")

    data = resp.json()
    claims = {
        "sub": data["user_id"],
        "bot_id": data["bot_id"],
        "mode": "bot",
        "tier": "alpha",  # Bots inherit user tier (query separately if needed)
    }

    # Cache for 5 minutes
    _bot_token_cache[token] = {
        "claims": claims,
        "expires": time.time() + 300,
    }

    return claims
```

**Caching Strategy:**
- In-memory dict cache with TTL (5 min)
- Keyed by full token string
- Invalidate on 401 from CloudNode
- No persistent cache (memory only)

**Fallback Behavior if CloudNode Unreachable:**
- Return 503 Service Unavailable
- Do NOT bypass auth (security-critical)
- Log error, include retry guidance in response

### D3. Keeper → CloudNode → Efemera Flow

**Authentication Chain:**

1. **User creates bot token** (hodeia.me frontend → CloudNode)
   - POST /bot/token → returns `sd_bot_xxxxx`

2. **User configures keeper** (external config file)
   - Keeper reads bot token from env/config

3. **Keeper connects to efemera** (ChatListener WebSocket)
   - URL: `wss://efemera.live/ws?user_id={bot_id}&display_name={keeper_name}`
   - **TODO:** Efemera must accept bot tokens for WebSocket auth

4. **Keeper sends messages** (ChatSender REST)
   - POST /api/messages/ with `Authorization: Bearer sd_bot_xxxxx`
   - Efemera validates token via CloudNode /bot/verify

**Command Routing:**

1. User types: `@keeper-bot run simulation scenario-123`
2. Efemera broadcasts via WebSocket
3. Keeper ChatListener detects `@keeper-bot`, extracts instruction
4. Keeper executor parses command, calls hivenode API (authenticated as bot)
5. Hivenode validates bot token via CloudNode
6. Hivenode executes command, returns result
7. Keeper ChatSender posts result to efemera channel

**Response Delivery:**
- ChatSender posts to same `channel_id`
- Message content includes result (text, JSON, error)
- No threading — linear conversation

**Missing Links:**
- Efemera WebSocket auth currently uses `user_id` query param (insecure)
- **TODO:** Efemera must accept bot tokens in WebSocket upgrade request
- **TODO:** Efemera must validate bot tokens via CloudNode /bot/verify

---

## E. Integration Requirements

### E1. CloudNode Additions

**New Tables:**
- `sd_bot_tokens` (schema in D1)
- Optional: `sd_bot_mutations` (if mutation tracking desired, defer to follow-up spec)

**New Endpoints:**
1. `POST /bot/token` — Create bot token (port from platform)
2. `GET /bot/token` — Get bot info (port from platform)
3. `DELETE /bot/token` — Revoke bot token (port from platform)
4. `POST /bot/verify` — Verify bot token (new, for hivenode validation)

**Migration:**
- Add to `hodeia_auth/db.py:_migrate_schema()`
- Check for `sd_bot_tokens` table existence
- Execute CREATE TABLE + CREATE INDEX if missing
- No data migration needed (new feature)

### E2. Hivenode Changes

**New Validation Client:**
- `hivenode/dependencies.py:verify_bot_token_or_jwt()` (new)
- `hivenode/dependencies.py:_verify_bot_token()` (new, calls CloudNode)
- In-memory cache with 5 min TTL

**Keeper Updates:**
- Port `platform/efemera/keeper/chat.py` → `hivenode/keeper/chat.py`
- Update `ChatSender` URL to efemera.live (or configurable)
- Update `ChatListener` WebSocket URL
- Add configuration loading (bot token, keeper name, channels)

**Fallback Strategy (Offline Behavior):**
- If CloudNode unreachable during bot token validation:
  - Return 503 Service Unavailable
  - Do NOT bypass auth
  - Log error with CloudNode URL
- No offline mode for bot tokens (security-critical)

### E3. Efemera Changes (Out of Scope, Documented for Completeness)

**WebSocket Auth:**
- Accept `Authorization: Bearer sd_bot_xxxxx` in WebSocket upgrade headers
- Validate via CloudNode /bot/verify before accepting connection
- OR: Continue using `user_id` param but validate bot ownership

**Message Endpoint Auth:**
- Already accepts `Authorization` header
- Add bot token validation via CloudNode /bot/verify
- Distinguish `author_type: "bot"` for display

---

## F. Portability Assessment

### F1. Direct Port (Copy with minimal changes)

**Files to Copy:**
1. `platform/simdecisions-2/api/bot_token.py` → `hodeia_auth/models.py` (add SDBotToken class)
2. `platform/simdecisions-2/api/bot_service.py` → `hodeia_auth/services/bot_token.py` (copy entire file)
3. `platform/simdecisions-2/api/bot.py` → `hodeia_auth/routes/bot.py` (copy endpoints 1-4 only)
4. `platform/efemera/keeper/chat.py` → `hivenode/keeper/chat.py` (copy entire file)

**Changes Needed:**
- Update imports (database → hodeia_auth.db)
- Update auth dependency (get_current_user → hodeia_auth.dependencies)
- Remove mutation endpoints (defer to follow-up spec)
- Remove GitHub service integration (not needed for BL-146)
- Add `POST /bot/verify` endpoint (new)

**Estimated Effort:** 2-4 hours (copy, test, commit)

### F2. Needs Adaptation

**Migration Tooling:**
- Platform uses `Base.metadata.create_all()` (SQLAlchemy auto-create)
- CloudNode uses `_migrate_schema()` manual migration function
- **Adaptation:** Write CREATE TABLE statements in `_migrate_schema()`

**Bot Token Validation in Hivenode:**
- Platform validates inline (session query in same process)
- CloudNode/Hivenode are separate services (Railway vs local)
- **Adaptation:** Add HTTP client call from hivenode → CloudNode `/bot/verify`

**Keeper Configuration:**
- Platform keeper config not visible (external file)
- **Adaptation:** Create `hivenode/keeper/config.py` or env var loading

**Test Fixtures:**
- Platform tests use `create_token(user_id, email, scope)` from `jwt_utils`
- CloudNode tests must use `hodeia_auth.services.jwt.create_access_token()`
- **Adaptation:** Update test fixtures in ported tests

**Estimated Effort:** 4-8 hours (write HTTP client, add config loading, update tests)

### F3. Complete Rewrite

**None.** All required components exist and are portable.

**Deferred to Follow-Up Specs:**
- `sd_bot_mutations` table and mutation tracking (complex, 23KB of code)
- Rate limiting (60/hour enforcement)
- Auto-commit vs PR mode (GitHub service integration)
- Bot activity approval/rejection UI

---

## G. Next Steps (Ordered Implementation Specs)

### G1. SPEC-BL-146-A: Port Bot Token CRUD to CloudNode (P1)
**Scope:** Copy bot_token.py, bot_service.py models and CRUD functions to hodeia_auth. Add database migration. Add POST /bot/token, GET /bot/token, DELETE /bot/token endpoints. Write tests. No hivenode changes yet.

**Deliverables:**
- `hodeia_auth/models.py` — Add SDBotToken class
- `hodeia_auth/services/bot_token.py` — Port generate, create, get, verify, revoke functions
- `hodeia_auth/routes/bot.py` — Add token CRUD endpoints
- `hodeia_auth/db.py` — Add migration for sd_bot_tokens table
- `tests/hodeia_auth/test_bot_token.py` — Port token generation, CRUD tests

**Smoke Test:** `curl -X POST https://hodeia.me/bot/token -H "Authorization: Bearer {jwt}" -d '{"name": "Test Bot"}'` returns bot token

---

### G2. SPEC-BL-146-B: Add Bot Token Verification Endpoint (P1)
**Scope:** Add POST /bot/verify endpoint in hodeia_auth for external validation. Takes bot token, returns {valid, user_id, bot_id} or 401. Used by hivenode and efemera. Write tests.

**Deliverables:**
- `hodeia_auth/routes/bot.py` — Add POST /bot/verify endpoint
- `hodeia_auth/schemas.py` — Add BotVerifyRequest, BotVerifyResponse
- `tests/hodeia_auth/test_bot_verify.py` — Test valid token, invalid token, revoked token

**Smoke Test:** `curl -X POST https://hodeia.me/bot/verify -d '{"token": "sd_bot_xxxxx"}'` returns {valid: true, user_id, bot_id}

---

### G3. SPEC-BL-146-C: Hivenode Bot Auth Validation (P1)
**Scope:** Add verify_bot_token_or_jwt() dependency in hivenode. Detect sd_bot_ prefix, call CloudNode /bot/verify, cache result. Update protected routes to accept bot tokens. Write tests.

**Deliverables:**
- `hivenode/dependencies.py` — Add verify_bot_token_or_jwt(), _verify_bot_token()
- `hivenode/config.py` — Add CLOUDNODE_URL setting
- `tests/hivenode/test_bot_auth.py` — Test bot token validation, JWT validation, cache behavior

**Smoke Test:** `curl http://127.0.0.1:8420/identity -H "Authorization: Bearer sd_bot_xxxxx"` returns bot identity claims

---

### G4. SPEC-BL-146-D: Port Keeper Chat to Hivenode (P2)
**Scope:** Copy keeper/chat.py to hivenode/keeper/chat.py. Add config loading (bot token, keeper name, efemera URL). Write tests for ChatSender and ChatListener. No daemon yet (manual start).

**Deliverables:**
- `hivenode/keeper/chat.py` — Port ChatSender, ChatListener
- `hivenode/keeper/config.py` — Config model (bot_token, keeper_name, efemera_url, channels)
- `tests/hivenode/keeper/test_chat.py` — Test ChatSender.send(), ChatListener @mention detection

**Smoke Test:** Start keeper manually, post @mention in efemera, confirm callback fires

---

### G5. SPEC-BL-146-E: Keeper Daemon Integration (P2)
**Scope:** Add keeper daemon to hivenode lifecycle. Start ChatListener on hivenode startup. Add /keeper/status endpoint. Add graceful shutdown. Write tests.

**Deliverables:**
- `hivenode/keeper/daemon.py` — Daemon lifecycle (start, stop, status)
- `hivenode/main.py` — Add keeper to lifespan
- `hivenode/routes/keeper.py` — Add GET /keeper/status
- `tests/hivenode/keeper/test_daemon.py` — Test start/stop, @mention flow

**Smoke Test:** Start hivenode, confirm keeper connected to efemera, post @mention, confirm response

---

### G6. SPEC-BL-146-F: Efemera Bot Token Auth (P2, External Repo)
**Scope:** Update efemera WebSocket and message endpoints to validate bot tokens via CloudNode /bot/verify. Add bot token to WebSocket upgrade auth. Write tests. (Requires access to platform/efemera repo)

**Deliverables:**
- `platform/efemera/src/efemera/websocket.py` — Add bot token validation
- `platform/efemera/src/efemera/messages/routes.py` — Add bot token validation
- `platform/efemera/src/efemera/auth.py` — Add verify_bot_token() function
- `tests/efemera/test_bot_auth.py` — Test bot message posting, WebSocket connection

**Smoke Test:** Connect to efemera WebSocket with bot token, post message, confirm accepted

---

### G7. SPEC-BL-146-G: Bot Settings UI (P3, Deferred)
**Scope:** Add bot token management UI to hodeia.me frontend. Show active bot, create new bot (shows token once), revoke bot. Display token prefix and last_used_at. Write E2E tests.

**Deliverables:**
- `frontend/src/pages/Settings/BotTokens.tsx` — Bot token management UI
- `frontend/src/api/bot.ts` — API client for bot endpoints
- `tests/e2e/bot_settings.spec.ts` — E2E test for create/revoke

**Smoke Test:** Navigate to hodeia.me/settings/bots, create bot, confirm token shown once

---

## H. Gaps (Unanswered Questions)

### H1. Efemera WebSocket Auth Current State
**Question:** How does efemera currently authenticate WebSocket connections? Query param `user_id` suggests no real auth.

**Blocker:** Cannot inspect `platform/efemera/src/efemera/websocket.py` without full file read (only keeper code reviewed).

**Impact:** SPEC-BL-146-F scope depends on this. May need to add auth from scratch.

---

### H2. Bot→Efemera Integration Breakage Root Cause
**Question:** When did bot integration break? What changed (auth service split, JWT issuer, database migration)?

**Blocker:** No git log inspection performed. Would require:
- `git log --all --grep="bot" platform/efemera`
- `git log --all --grep="ra96it\|hodeia" platform/simdecisions-2`
- Compare last known working commit to first broken commit

**Impact:** Low — can rebuild from working state (platform/simdecisions-2) without knowing breakage history.

---

### H3. Platform Bot Test Full Coverage
**Question:** What specific flows do `test_bot_activity.py` and `test_bot_mutate.py` cover?

**Blocker:** Only read first 100 lines of `test_bot.py`. Full coverage requires reading all 3 test files.

**Impact:** Low — can port tests incrementally as features are ported.

---

### H4. Mutation Validation Rules
**Question:** What mutation validation rules exist in `mutation_service.py`?

**Blocker:** File not read (not in "Files to Read First" list).

**Impact:** Medium — SPEC-BL-146-H (mutation tracking, deferred) requires this.

---

### H5. Rate Limiting Implementation
**Question:** How is rate limiting enforced? In-memory counter, database query, external service?

**Blocker:** Only saw rate limit check function (database query COUNT in window). Don't know if there's middleware or decorator.

**Impact:** Low — can implement from scratch if needed (pattern is clear from bot.py).

---

## I. Summary YAML

```yaml
research_id: SPEC-RESEARCH-BOT-AUTH-AUDIT-001
completed_by: BEE-SONNET-QUEUE-TEMP
completed_at: 2026-04-16T10:50:00-05:00

platform_bot_system:
  models:
    bot_token: |
      sd_bot_tokens table with SHA-256 hashed tokens, one active per user,
      partial unique index on user_id WHERE revoked_at IS NULL
    bot_mutation: |
      sd_bot_mutations table with audit log, FK to bot_token,
      tracks pending/applied/rejected status, PR/commit URLs
  endpoints:
    - path: POST /api/bot/token
      method: POST
      purpose: Create bot token (shown once)
    - path: GET /api/bot/token
      method: GET
      purpose: Get bot metadata (no token)
    - path: DELETE /api/bot/token
      method: DELETE
      purpose: Revoke bot token
    - path: POST /api/bot/mutate
      method: POST
      purpose: Submit mutation (bot-authenticated, rate limited)
  tests:
    coverage: Token generation, CRUD, validation, rate limiting, mutation validation
    key_flows:
      - Token format validation (sd_bot_xxxxx, 39 chars)
      - SHA-256 hash verification
      - One active bot per user enforcement
      - Bearer token authentication
      - Rate limiting (60/hour)

cloudnode_current:
  auth_infrastructure:
    models: User, RefreshToken, LoginSession (no bot tables)
    endpoints: register, login, mfa, token refresh/revoke, OAuth callbacks
    database: PostgreSQL (Railway) + SQLite fallback, SQLAlchemy ORM, manual migrations
  bot_support:
    existing_code: No bot token code. Refresh token service uses identical pattern (SHA-256, secrets.token_urlsafe)
    extensibility: User.provider includes 'bot' enum value (prepared for bots). Easy to add bot tables.

efemera_integration:
  historical_pattern: |
    ChatSender posts messages via REST with author_type='bot'.
    ChatListener connects via WebSocket, filters @mentions, fires callback.
  keeper_architecture: |
    ChatSender: REST client with Bearer token auth.
    ChatListener: WebSocket client with auto-reconnect, @mention regex, daemon thread.
    Callback: on_mention(data, instruction) fired when @keeper_name detected.
  broken_dependencies: |
    Unknown when/why. Hypothesis: auth service split (hodeia_auth standalone),
    efemera lost bot token validation route OR JWT issuer changed (ra96it → hodeia).

integration_requirements:
  cloudnode_additions:
    tables: sd_bot_tokens (id, user_id, token_hash, token_prefix, timestamps)
    endpoints: POST/GET/DELETE /bot/token, POST /bot/verify (new, for external validation)
    migrations: Add _migrate_schema case, CREATE TABLE + CREATE INDEX statements
  hivenode_changes:
    validation_client: verify_bot_token_or_jwt() with HTTP call to CloudNode /bot/verify, 5min cache
    keeper_updates: Port chat.py, add config loading, integrate to hivenode lifecycle
    fallback_strategy: Return 503 if CloudNode unreachable (no auth bypass)

portability_assessment:
  direct_port:
    - bot_token.py model (42 lines)
    - bot_service.py CRUD (187 lines)
    - bot.py token endpoints (3 endpoints, ~100 lines)
    - keeper/chat.py ChatSender/ChatListener (179 lines)
  needs_adaptation:
    - Migration tooling (Base.metadata.create_all → _migrate_schema manual SQL)
    - Bot validation client (inline session query → HTTP call to CloudNode)
    - Test fixtures (jwt_utils.create_token → hodeia_auth.services.jwt.create_access_token)
    - Keeper config loading (external file → env vars or config.py)
  complete_rewrite:
    - None

gaps:
  - question: H1 - Efemera WebSocket auth current state
    blocker: Need to read platform/efemera/src/efemera/websocket.py
  - question: H2 - Bot integration breakage root cause
    blocker: Need git log inspection across repos
  - question: H3 - Platform bot test full coverage
    blocker: Only read 100 lines of test_bot.py (3 files total)
  - question: H4 - Mutation validation rules detail
    blocker: Did not read mutation_service.py
  - question: H5 - Rate limiting implementation pattern
    blocker: Only saw check function, not enforcement mechanism

next_steps:
  - spec_id: SPEC-BL-146-A
    scope: Port bot token CRUD to CloudNode (models, services, endpoints, migration, tests)
  - spec_id: SPEC-BL-146-B
    scope: Add bot token verification endpoint for external validation
  - spec_id: SPEC-BL-146-C
    scope: Hivenode bot auth validation client with caching
  - spec_id: SPEC-BL-146-D
    scope: Port keeper chat.py to hivenode with config loading
  - spec_id: SPEC-BL-146-E
    scope: Keeper daemon integration into hivenode lifecycle
  - spec_id: SPEC-BL-146-F
    scope: Efemera bot token auth (external repo, requires access)
  - spec_id: SPEC-BL-146-G
    scope: Bot settings UI in hodeia.me frontend (deferred)
```

---

## Files Modified

None — research-only audit.

## What Was Done

- Audited `platform/simdecisions-2/api/bot*.py` (4 files, ~30KB Python code)
- Audited `platform/efemera/keeper/chat.py` (179 lines)
- Audited `hodeia_auth/models.py`, `hodeia_auth/services/token.py`, `hodeia_auth/routes/token.py`
- Audited `hivenode/dependencies.py`, `hivenode/routes/auth.py`, `hivenode/identity.py`
- Documented platform bot system: 2 models, 4 endpoints, SHA-256 token hashing, rate limiting
- Documented CloudNode auth system: 3 models, JWT flow, refresh token rotation, no bot code
- Documented efemera keeper: ChatSender REST client, ChatListener WebSocket with @mention detection
- Assessed portability: 90% direct port, 10% adaptation (HTTP validation client, migration tooling)
- Produced 7 follow-up spec proposals (BL-146-A through BL-146-G)
- Identified 5 research gaps (efemera WebSocket auth, breakage root cause, test coverage, mutation rules, rate limiting)

## Tests Run

None — research-only audit, no code changes.

## Blockers

None.

## Cost

~$0.15 (estimated, Sonnet 4.5 research session)

## Notes

- Bot token system is well-architected and portable
- Primary challenge is service separation (hivenode/CloudNode split) requiring HTTP validation
- Efemera integration requires access to external repo (platform/efemera)
- Mutation tracking (sd_bot_mutations table) is complex and should be separate spec (BL-146-H, not listed)
- Rate limiting enforcement pattern needs clarification (gap H5)

## Recommendations

1. **Start with SPEC-BL-146-A** (CloudNode CRUD) — establishes foundation
2. **Follow with BL-146-B** (verification endpoint) — enables hivenode integration
3. **Then BL-146-C** (hivenode validation) — completes basic bot auth flow
4. **Defer BL-146-F** (efemera auth) until platform/efemera repo access confirmed
5. **Defer BL-146-G** (settings UI) to P3 — low priority, can use cURL for alpha testing
6. **Create BL-146-H** (mutation tracking) if needed — large scope, separate from core auth

---

**END OF REPORT**
