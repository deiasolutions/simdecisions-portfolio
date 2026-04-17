# TASK-EFEMERA-CONN-10: Port Message Versioning + Reply Threading

**Priority:** P1
**Depends on:** CONN-07
**Blocks:** None
**Model:** Sonnet
**Role:** Bee

## Objective

Port message edit versioning and reply threading from platform to hivenode. Edits create new version rows chained via `parent_id`. Replies use `reply_to_id` for threaded conversations.

## Read First

- `.deia/BOOT.md` — hard rules
- Platform source: `C:\Users\davee\OneDrive\Documents\GitHub\platform\platform\efemera\src\efemera\messages\routes.py` (295 lines)
- Platform source: `C:\Users\davee\OneDrive\Documents\GitHub\platform\platform\efemera\src\efemera\messages\models.py` (79 lines)
- `hivenode/efemera/store.py` — store methods (after CONN-07 schema upgrade)
- `hivenode/efemera/routes.py` — existing message routes
- `.deia/hive/responses/20260328-EFEMERA-ASSESSMENT.md` — sections 1.2 (Messages)

## What to Port

### Edit Versioning

Platform pattern: when a message is edited, a **new row** is created with:
- Same content (updated)
- `parent_id` = original message ID
- `version` = previous version + 1
- `edited_at` = current timestamp

The original row is NOT modified. The latest version is the one with the highest `version` for a given `parent_id` chain.

**Store methods (add to store.py):**

```python
def edit_message(self, message_id: str, new_content: str, editor_id: str) -> Dict[str, Any]:
    """Create a new version of a message. Returns the new version row."""
    original = self.get_message(message_id)
    if not original:
        raise ValueError(f"Message {message_id} not found")

    # Find the root of the edit chain
    root_id = original.get("parent_id") or original["id"]

    # Get current max version
    cursor = self._conn.cursor()
    row = cursor.execute(
        "SELECT MAX(version) as max_v FROM messages WHERE id = ? OR parent_id = ?",
        (root_id, root_id),
    ).fetchone()
    next_version = (row["max_v"] or 1) + 1

    new_id = str(uuid.uuid4())
    now = datetime.now(UTC).isoformat()
    self._conn.execute(
        """INSERT INTO messages (id, channel_id, author_id, author_name, content, created_at,
           version, parent_id, edited_at, author_type, message_type)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (new_id, original["channel_id"], editor_id, original["author_name"],
         new_content, original["created_at"], next_version, root_id, now,
         original.get("author_type", "human"), original.get("message_type", "text")),
    )
    self._conn.commit()
    return self.get_message(new_id)

def get_message(self, message_id: str) -> Optional[Dict[str, Any]]:
    """Get a single message by ID."""
    cursor = self._conn.cursor()
    row = cursor.execute("SELECT * FROM messages WHERE id = ?", (message_id,)).fetchone()
    return dict(row) if row else None

def get_message_history(self, message_id: str) -> List[Dict[str, Any]]:
    """Get all versions of a message (the edit chain)."""
    # Find root
    msg = self.get_message(message_id)
    if not msg:
        return []
    root_id = msg.get("parent_id") or msg["id"]
    cursor = self._conn.cursor()
    rows = cursor.execute(
        "SELECT * FROM messages WHERE id = ? OR parent_id = ? ORDER BY version ASC",
        (root_id, root_id),
    ).fetchall()
    return [dict(r) for r in rows]
```

### Reply Threading

Platform pattern: `reply_to_id` points to the message being replied to. It's a flat reference — not nested (no reply-to-reply chains, just one level of threading).

**Store methods (add to store.py):**

```python
def get_replies(self, message_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Get replies to a message."""
    cursor = self._conn.cursor()
    rows = cursor.execute(
        "SELECT * FROM messages WHERE reply_to_id = ? ORDER BY created_at ASC LIMIT ?",
        (message_id, limit),
    ).fetchall()
    return [dict(r) for r in rows]
```

**Update `create_message()`** — already takes `reply_to_id` from CONN-07. Add validation:
```python
if reply_to_id:
    parent = self.get_message(reply_to_id)
    if not parent:
        raise ValueError(f"Reply target {reply_to_id} not found")
    if parent["channel_id"] != channel_id:
        raise ValueError("Cannot reply to message in different channel")
```

### Route File: `hivenode/efemera/message_routes.py` (~100 lines)

**Create a NEW file** — do NOT add these to `routes.py` (it already has 5 tasks modifying it). Register in `hivenode/routes/__init__.py`:
```python
from hivenode.efemera.message_routes import router as message_router
router.include_router(message_router, prefix='/efemera', tags=['efemera-messages'])
```

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter()

class EditMessageRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=4000)
    editor_id: str = Field(default="local-user")

@router.put("/messages/{message_id}")
async def edit_message(message_id: str, req: EditMessageRequest):
    store = _get_store()
    try:
        return store.edit_message(message_id, req.content, req.editor_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/messages/{message_id}/history")
async def get_message_history(message_id: str):
    store = _get_store()
    return store.get_message_history(message_id)

@router.get("/messages/{message_id}/replies")
async def get_message_replies(message_id: str, limit: int = 50):
    store = _get_store()
    return store.get_replies(message_id, limit=limit)
```

### Display Name in Listings

**Update `list_messages()`** — include version info in response:
- If a message has `parent_id`, it's an edit version. The listing should return the LATEST version only.
- Add a query filter: exclude rows where `parent_id IS NOT NULL AND id != (SELECT id FROM messages WHERE parent_id = m.parent_id ORDER BY version DESC LIMIT 1)`

Or simpler approach: listing shows all non-edit messages (parent_id IS NULL) plus the latest version of edited messages. Use a window function or subquery.

## Tests to Create

### `tests/hivenode/test_efemera_versioning.py`
- edit_message creates new row with version 2
- edit_message twice creates version 3
- get_message_history returns all versions in order
- edit preserves original author_name and channel_id
- edit with invalid message_id raises ValueError
- list_messages shows latest version only (not all edit chain rows)

### `tests/hivenode/test_efemera_threading.py`
- create_message with reply_to_id links to parent
- get_replies returns all replies to a message
- reply to nonexistent message raises ValueError
- reply to message in different channel raises ValueError
- replies appear in list_messages (they're normal messages with reply_to_id set)

## Constraints

- Port the versioning/threading logic from platform — don't redesign
- Edit creates new rows, never mutates existing rows
- Reply threading is flat (one level), not recursive
- No file exceeds 500 lines
- TDD: write tests first
