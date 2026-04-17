# SPEC-BL-146-A: CloudNode Bot Token CRUD System

## Priority
P1

## Depends On
- SPEC-RESEARCH-BOT-AUTH-AUDIT-001 (audit that informed this spec)

## Model Assignment
sonnet

## Objective

Port the bot token authentication system from `platform/simdecisions-2` to CloudNode (hodeia_auth), providing the foundation for bot authentication across the platform. This enables bots to authenticate against hodeia.me auth service and perform actions on behalf of users. Uses the existing `_migrate_schema()` pattern — no Alembic.

## Files to Read First

- hodeia_auth/main.py
- hodeia_auth/models.py
- hodeia_auth/db.py
- hodeia_auth/dependencies.py
- hodeia_auth/routes/token.py
- hodeia_auth/routes/__init__.py
- hodeia_auth/services/token.py
- hodeia_auth/services/__init__.py
- .deia/hive/responses/2026-04-16-1050-BEE-SONNET-RESEARCH-BOT-AUTH-AUDIT-001.md

## Acceptance Criteria

- [ ] `cd hodeia_auth && python -m pytest tests/test_bot_token.py -v` — all tests pass
- [ ] At least 15 tests covering generation, CRUD, API endpoints, and edge cases
- [ ] `_migrate_schema()` in hodeia_auth/db.py creates `bot_tokens` table with: id (UUID PK), user_id (UUID, indexed), name, token_hash (SHA-256, unique), token_prefix, created_at, last_used_at, revoked_at
- [ ] Partial unique index `idx_one_active_bot_per_user` on user_id WHERE revoked_at IS NULL
- [ ] POST /bot/token creates a token, returns sd_bot_xxx full token exactly ONCE with a warning field
- [ ] GET /bot/token returns bot metadata (id, name, token_prefix, created_at, last_used_at) — never the plaintext token
- [ ] DELETE /bot/token sets revoked_at and returns 200 with revoked=true
- [ ] Creating a second active token for same user returns HTTP 409 with "already has an active bot token"
- [ ] Bot token format is `sd_bot_` + 32 hex chars (39 chars total)
- [ ] Token stored as SHA-256 hash only — plaintext never persisted
- [ ] `verify_bot_token()` updates `last_used_at` on successful validation
- [ ] `get_current_user_from_bot_token` dependency added to hodeia_auth/dependencies.py and returns 401 for invalid/expired/non-bot tokens
- [ ] Routes registered in hodeia_auth/main.py
- [ ] No Alembic imports, no alembic.ini, no migration files — uses existing `_migrate_schema()` pattern
- [ ] No file exceeds 500 lines

## Smoke Test

- [ ] `cd hodeia_auth && python -m pytest tests/test_bot_token.py -v` exits 0
- [ ] `python -c "from hodeia_auth.services.bot_token import BotTokenService; t,h,p = BotTokenService.generate_bot_token(); assert t.startswith('sd_bot_') and len(t)==39 and len(h)==64"` exits 0
- [ ] `grep -r "alembic" hodeia_auth/ --include="*.py"` returns no matches
- [ ] `python -c "import hodeia_auth.main"` imports cleanly (routes register without error)

## Constraints

- TDD — write tests first, then implementation
- Use async/await patterns throughout (match existing hodeia_auth style)
- Follow existing hodeia_auth code patterns (see services/token.py and routes/token.py for JWT token reference pattern)
- **No Alembic.** Use the existing `_migrate_schema()` approach in hodeia_auth/db.py. Railway has had bad luck with Alembic — this is a hard rule.
- No file over 500 lines (hard limit 1000)
- No stubs — every function complete
- No git operations
- Plaintext tokens are NEVER stored or logged — only SHA-256 hashes

## Files to Create

- hodeia_auth/services/bot_token.py — BotTokenService with async CRUD + generate/verify/revoke
- hodeia_auth/routes/bot_token.py — POST/GET/DELETE /bot/token endpoints
- hodeia_auth/tests/test_bot_token.py — 15+ tests covering generation, CRUD, API, edge cases

## Files to Modify

- hodeia_auth/models.py — Add BotToken SQLAlchemy model with partial unique index
- hodeia_auth/db.py — Add bot_tokens CREATE TABLE + indexes into `_migrate_schema()`
- hodeia_auth/main.py — Register bot_token router
- hodeia_auth/dependencies.py — Add `get_current_user_from_bot_token` dependency

## Implementation

### Database Model (hodeia_auth/models.py)

Based on platform `bot_token.py` with CloudNode patterns:

```python
from sqlalchemy import Column, String, DateTime, Index, text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid

# (assumes existing Base and User model are defined in this file)

class BotToken(Base):
    __tablename__ = "bot_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    name = Column(String(100), nullable=False, default="My Bot")
    token_hash = Column(String(64), nullable=False, unique=True, index=True)  # SHA-256
    token_prefix = Column(String(10), nullable=False)  # Display prefix: "sd_bot_abc"
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    revoked_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index(
            "idx_one_active_bot_per_user",
            "user_id",
            unique=True,
            postgresql_where=text("revoked_at IS NULL"),
        ),
    )

    def is_active(self) -> bool:
        return self.revoked_at is None

    def revoke(self):
        self.revoked_at = datetime.now(timezone.utc)

    def update_last_used(self):
        self.last_used_at = datetime.now(timezone.utc)
```

### Service Layer (hodeia_auth/services/bot_token.py)

```python
import hashlib
import secrets
from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from ..models import BotToken, User


class BotTokenService:
    """Bot token management service."""

    @staticmethod
    def generate_bot_token() -> Tuple[str, str, str]:
        """Returns (full_token, token_hash, token_prefix)."""
        token_bytes = secrets.token_bytes(16)
        full_token = f"sd_bot_{token_bytes.hex()}"
        token_hash = hashlib.sha256(full_token.encode()).hexdigest()
        token_prefix = full_token[:10]
        return full_token, token_hash, token_prefix

    @staticmethod
    async def create_bot_token(
        session: AsyncSession,
        user_id: str,
        name: str = "My Bot",
    ) -> Optional[Tuple[BotToken, str]]:
        """Returns (BotToken, full_token) or None if user already has an active bot."""
        existing = await BotTokenService.get_active_bot_token(session, user_id)
        if existing:
            return None

        full_token, token_hash, token_prefix = BotTokenService.generate_bot_token()
        bot_token = BotToken(
            user_id=user_id,
            name=name,
            token_hash=token_hash,
            token_prefix=token_prefix,
        )
        session.add(bot_token)
        await session.commit()
        await session.refresh(bot_token)
        return bot_token, full_token

    @staticmethod
    async def get_active_bot_token(session: AsyncSession, user_id: str) -> Optional[BotToken]:
        result = await session.execute(
            select(BotToken).where(
                and_(BotToken.user_id == user_id, BotToken.revoked_at.is_(None))
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def verify_bot_token(session: AsyncSession, token: str) -> Optional[str]:
        """Verify bot token. Returns user_id if valid. Updates last_used_at."""
        if not token.startswith("sd_bot_"):
            return None

        token_hash = hashlib.sha256(token.encode()).hexdigest()
        result = await session.execute(
            select(BotToken).where(
                and_(BotToken.token_hash == token_hash, BotToken.revoked_at.is_(None))
            )
        )
        bot_token = result.scalar_one_or_none()
        if not bot_token:
            return None

        bot_token.update_last_used()
        await session.commit()
        return str(bot_token.user_id)

    @staticmethod
    async def revoke_bot_token(session: AsyncSession, user_id: str) -> bool:
        bot_token = await BotTokenService.get_active_bot_token(session, user_id)
        if not bot_token:
            return False
        bot_token.revoke()
        await session.commit()
        return True

    @staticmethod
    async def get_bot_token_info(session: AsyncSession, user_id: str) -> Optional[BotToken]:
        return await BotTokenService.get_active_bot_token(session, user_id)
```

### API Routes (hodeia_auth/routes/bot_token.py)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from ..dependencies import get_current_user, get_db
from ..services.bot_token import BotTokenService
from ..models import User

router = APIRouter(prefix="/bot", tags=["bot-tokens"])


class CreateBotTokenRequest(BaseModel):
    name: str = "My Bot"


class BotTokenResponse(BaseModel):
    id: str
    name: str
    token_prefix: str
    created_at: datetime
    last_used_at: Optional[datetime] = None


class CreateBotTokenResponse(BaseModel):
    id: str
    name: str
    token: str  # shown only once
    token_prefix: str
    created_at: datetime
    warning: str = "Store this token securely. It will not be shown again."


class BotTokenInfoResponse(BaseModel):
    bot: Optional[BotTokenResponse] = None


class RevokeBotTokenResponse(BaseModel):
    revoked: bool
    revoked_at: datetime


@router.post("/token", response_model=CreateBotTokenResponse, status_code=201)
async def create_bot_token(
    request: CreateBotTokenRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    result = await BotTokenService.create_bot_token(session, str(current_user.id), request.name)
    if result is None:
        raise HTTPException(409, detail="User already has an active bot token. Revoke existing token first.")
    bot_token, full_token = result
    return CreateBotTokenResponse(
        id=str(bot_token.id),
        name=bot_token.name,
        token=full_token,
        token_prefix=bot_token.token_prefix,
        created_at=bot_token.created_at,
    )


@router.get("/token", response_model=BotTokenInfoResponse)
async def get_bot_token_info(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    bot_token = await BotTokenService.get_bot_token_info(session, str(current_user.id))
    if bot_token is None:
        return BotTokenInfoResponse(bot=None)
    return BotTokenInfoResponse(
        bot=BotTokenResponse(
            id=str(bot_token.id),
            name=bot_token.name,
            token_prefix=bot_token.token_prefix,
            created_at=bot_token.created_at,
            last_used_at=bot_token.last_used_at,
        )
    )


@router.delete("/token", response_model=RevokeBotTokenResponse)
async def revoke_bot_token(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    success = await BotTokenService.revoke_bot_token(session, str(current_user.id))
    if not success:
        raise HTTPException(404, detail="No active bot token found")
    return RevokeBotTokenResponse(revoked=True, revoked_at=datetime.now())
```

### Migration (hodeia_auth/db.py — extend existing `_migrate_schema`)

**DO NOT add Alembic.** Append to the existing migration helper:

```python
# Inside _migrate_schema(engine):
try:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS bot_tokens (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID NOT NULL,
            name VARCHAR(100) NOT NULL DEFAULT 'My Bot',
            token_hash VARCHAR(64) NOT NULL UNIQUE,
            token_prefix VARCHAR(10) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            last_used_at TIMESTAMPTZ,
            revoked_at TIMESTAMPTZ
        )
    """))
    conn.execute(text("CREATE INDEX IF NOT EXISTS idx_bot_tokens_user_id ON bot_tokens(user_id)"))
    conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS idx_bot_tokens_token_hash ON bot_tokens(token_hash)"))
    conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS idx_one_active_bot_per_user ON bot_tokens(user_id) WHERE revoked_at IS NULL"))
    conn.commit()
except Exception as e:
    print(f"Bot token migration error (may be safe to ignore): {e}")
    conn.rollback()
```

### Bot Auth Dependency (hodeia_auth/dependencies.py)

```python
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .services.bot_token import BotTokenService
from .models import User

security = HTTPBearer()


async def get_current_user_from_bot_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_db),
) -> User:
    if not credentials.credentials.startswith("sd_bot_"):
        raise HTTPException(401, detail="Invalid bot token format")

    user_id = await BotTokenService.verify_bot_token(session, credentials.credentials)
    if user_id is None:
        raise HTTPException(401, detail="Invalid or expired bot token")

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(401, detail="User not found")
    return user
```

### Tests (hodeia_auth/tests/test_bot_token.py)

At least 15 tests covering: generate format, SHA-256 hashing, token_prefix, create success, duplicate 409, verify valid/invalid/revoked, revoke success/no-token, last_used_at updates, API endpoints (POST/GET/DELETE), GET omits plaintext token, DELETE idempotency, malformed token rejected.

## Notes on Current hodeia_auth Structure

- `hodeia_auth/models.py` is currently a single file. Either extend it in-place with `class BotToken(Base):` or refactor to a package. Prefer extending in-place to minimize diff.
- `hodeia_auth/services/token.py` already exists (JWT token service) — reference for async patterns.
- `hodeia_auth/routes/token.py` already exists (JWT token routes) — reference for endpoint style.
