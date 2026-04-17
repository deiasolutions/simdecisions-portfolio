# SPEC-EFEMERA-CONN-07: Backend Schema Upgrade

> **Project:** Efemera Connector (12 specs submitted as batch, 2026-03-28)
> Dependencies between specs ensure correct execution order.
> Design doc: `.deia/hive/responses/20260328-EFEMERA-CONNECTOR-DESIGN.md`

## Priority
P1

## Depends On
- None

## Model Assignment
sonnet

## Objective

Extend the efemera SQLite schema to support the full platform feature set: message versioning, reply threading, channel types, moderation status, and metadata fields. All new columns have defaults — backward compatible with existing data. Add optional `channel_id` param to `create_channel()` for system channel seeding.

## Read First

- `.deia/BOOT.md` — hard rules
- `hivenode/efemera/store.py` — the file being modified (224 lines)
- `hivenode/efemera/routes.py` — routes that use the store (169 lines)
- `.deia/hive/responses/20260328-EFEMERA-ASSESSMENT.md` — section 3.1 (backend gaps)
- Platform source (for reference):
  - `C:\Users\davee\OneDrive\Documents\GitHub\platform\platform\efemera\src\efemera\channels\models.py`
  - `C:\Users\davee\OneDrive\Documents\GitHub\platform\platform\efemera\src\efemera\messages\models.py`

## Schema Changes

**channels table — extend:**
```sql
CREATE TABLE IF NOT EXISTS channels (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    type        TEXT NOT NULL CHECK(type IN (
        'channel', 'dm', 'commons', 'announcements', 'the_buzz',
        'the_window', 'dev', 'personal', 'moderation_log',
        'bugs_admin', 'approvals', 'humans_only', 'bok_submissions'
    )),
    description TEXT DEFAULT '',
    created_by  TEXT NOT NULL,
    pinned      BOOLEAN DEFAULT FALSE,
    read_only   BOOLEAN DEFAULT FALSE,
    created_at  TEXT NOT NULL
);
```

**messages table — extend:**
```sql
CREATE TABLE IF NOT EXISTS messages (
    id                TEXT PRIMARY KEY,
    channel_id        TEXT NOT NULL REFERENCES channels(id),
    author_id         TEXT NOT NULL,
    author_name       TEXT NOT NULL,
    content           TEXT NOT NULL,
    created_at        TEXT NOT NULL,
    version           INTEGER DEFAULT 1,
    parent_id         TEXT REFERENCES messages(id),
    reply_to_id       TEXT REFERENCES messages(id),
    edited_at         TEXT,
    author_type       TEXT DEFAULT 'human' CHECK(author_type IN ('human', 'bot', 'agent', 'system')),
    message_type      TEXT DEFAULT 'text' CHECK(message_type IN ('text', 'terminal_output', 'rag_answer', 'system')),
    moderation_status TEXT DEFAULT 'approved' CHECK(moderation_status IN ('approved', 'held', 'blocked')),
    moderation_reason TEXT,
    provider          TEXT,
    metadata_json     TEXT,
    topic_id          TEXT,
    topic_name        TEXT
);
```

## Migration Strategy

Add `_migrate_schema()` using `ALTER TABLE ADD COLUMN`. Idempotent — safe to run multiple times.

```python
def _migrate_schema(self) -> None:
    migrations = [
        ("channels", "description", "TEXT DEFAULT ''"),
        ("channels", "read_only", "BOOLEAN DEFAULT FALSE"),
        ("messages", "version", "INTEGER DEFAULT 1"),
        ("messages", "parent_id", "TEXT"),
        ("messages", "reply_to_id", "TEXT"),
        ("messages", "edited_at", "TEXT"),
        ("messages", "author_type", "TEXT DEFAULT 'human'"),
        ("messages", "message_type", "TEXT DEFAULT 'text'"),
        ("messages", "moderation_status", "TEXT DEFAULT 'approved'"),
        ("messages", "moderation_reason", "TEXT"),
        ("messages", "provider", "TEXT"),
        ("messages", "metadata_json", "TEXT"),
        ("messages", "topic_id", "TEXT"),
        ("messages", "topic_name", "TEXT"),
    ]
    for table, column, typedef in migrations:
        try:
            self._conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {typedef}")
        except sqlite3.OperationalError:
            pass
    self._conn.commit()
```

## Store Method Updates

**`create_channel()`** — accept optional `channel_id` param:
```python
def create_channel(
    self, name: str, channel_type: str = "channel", created_by: str = "system",
    pinned: bool = False, description: str = "", read_only: bool = False,
    channel_id: Optional[str] = None,
) -> Dict[str, Any]:
    cid = channel_id or str(uuid.uuid4())[:8]
```

**`create_message()`** — accept new optional params:
```python
def create_message(
    self, channel_id: str, author_id: str, author_name: str, content: str,
    author_type: str = "human", message_type: str = "text",
    reply_to_id: Optional[str] = None, moderation_status: str = "approved",
    moderation_reason: Optional[str] = None, metadata_json: Optional[str] = None,
) -> Dict[str, Any]:
```

**Add `get_message()`:**
```python
def get_message(self, message_id: str) -> Optional[Dict[str, Any]]:
```

**NOTE:** `edit_message()`, `get_message_history()`, and `get_replies()` are NOT added here — they belong to CONN-10.

## Route Updates

**Extend `CreateMessageRequest`:**
```python
class CreateMessageRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=4000)
    author_id: str = Field(default="local-user")
    author_name: str = Field(default="You")
    author_type: str = Field(default="human")
    message_type: str = Field(default="text")
    reply_to_id: Optional[str] = None
    metadata_json: Optional[str] = None
```

**Add join/leave endpoints only (edit/history/replies go in CONN-10's `message_routes.py`):**
```python
@router.post("/channels/{channel_id}/join")
async def join_channel(channel_id: str, req: JoinChannelRequest): ...

@router.post("/channels/{channel_id}/leave")
async def leave_channel(channel_id: str, req: LeaveChannelRequest): ...
```

## Acceptance Criteria
- [ ] create_channel with explicit channel_id uses that ID
- [ ] create_channel without channel_id generates UUID
- [ ] create_message with author_type and message_type stores correctly
- [ ] create_message with reply_to_id stores correctly
- [ ] create_message with moderation_status and moderation_reason stores correctly
- [ ] get_message returns single message by ID
- [ ] Schema migration adds all columns to existing DB
- [ ] Migration is idempotent (running twice doesn't error)
- [ ] join_channel endpoint works
- [ ] leave_channel endpoint works
- [ ] Channel type validation (new types accepted, invalid rejected)
- [ ] All existing tests still pass (new columns have defaults)
- [ ] No file exceeds 500 lines

## Smoke Test
- [ ] `cd hivenode && python -m pytest tests/hivenode/test_efemera.py -v` — all pass
- [ ] `cd hivenode && python -m pytest tests/ -v` — no regressions

## Constraints
- All new columns MUST have defaults or be nullable — backward compatible
- Migration must be idempotent (safe to run multiple times)
- No file exceeds 500 lines. If store.py grows past 400, split message methods into a separate `message_store.py`
- TDD: write tests first

## Response File
20260328-EFEMERA-CONN-07-RESPONSE.md
