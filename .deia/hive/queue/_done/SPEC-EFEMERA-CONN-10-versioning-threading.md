# SPEC-EFEMERA-CONN-10: Port Message Versioning + Reply Threading

> **Project:** Efemera Connector (12 specs submitted as batch, 2026-03-28)
> Dependencies between specs ensure correct execution order.
> Design doc: `.deia/hive/responses/20260328-EFEMERA-CONNECTOR-DESIGN.md`

## Priority
P1

## Depends On
- SPEC-EFEMERA-CONN-07-backend-schema

## Model Assignment
sonnet

## Objective

Port message edit versioning and reply threading from platform to hivenode. Edits create new version rows chained via `parent_id`. Replies use `reply_to_id` for threaded conversations. Create routes in a NEW file `message_routes.py` (not in routes.py).

## Read First

- `.deia/BOOT.md` — hard rules
- Platform source: `C:\Users\davee\OneDrive\Documents\GitHub\platform\platform\efemera\src\efemera\messages\routes.py` (295 lines)
- Platform source: `C:\Users\davee\OneDrive\Documents\GitHub\platform\platform\efemera\src\efemera\messages\models.py` (79 lines)
- `hivenode/efemera/store.py` — store methods (after CONN-07 schema upgrade)
- `hivenode/efemera/routes.py` — existing message routes
- `.deia/hive/responses/20260328-EFEMERA-ASSESSMENT.md` — sections 1.2 (Messages)

## Store Methods (add to store.py)

### Edit Versioning

```python
def edit_message(self, message_id: str, new_content: str, editor_id: str) -> Dict[str, Any]:
    """Create a new version of a message. Returns the new version row."""
    original = self.get_message(message_id)
    if not original:
        raise ValueError(f"Message {message_id} not found")
    root_id = original.get("parent_id") or original["id"]
    # Get max version, create new row with version+1, parent_id=root_id

def get_message_history(self, message_id: str) -> List[Dict[str, Any]]:
    """Get all versions of a message (the edit chain)."""
    # Find root, return all rows with that root ordered by version

def get_replies(self, message_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Get replies to a message."""
    # SELECT WHERE reply_to_id = message_id ORDER BY created_at
```

### Reply Validation (update create_message)

```python
if reply_to_id:
    parent = self.get_message(reply_to_id)
    if not parent:
        raise ValueError(f"Reply target {reply_to_id} not found")
    if parent["channel_id"] != channel_id:
        raise ValueError("Cannot reply to message in different channel")
```

## Route File: `hivenode/efemera/message_routes.py` (~100 lines)

**Create a NEW file** — do NOT add these to `routes.py`. Register in `hivenode/routes/__init__.py`:
```python
from hivenode.efemera.message_routes import router as message_router
router.include_router(message_router, prefix='/efemera', tags=['efemera-messages'])
```

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

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

### Update list_messages to show latest version only

Listing should return the LATEST version of edited messages, not all versions.

## Acceptance Criteria
- [ ] edit_message creates new row with version 2
- [ ] edit_message twice creates version 3
- [ ] get_message_history returns all versions in order
- [ ] edit preserves original author_name and channel_id
- [ ] edit with invalid message_id raises ValueError
- [ ] list_messages shows latest version only (not all edit chain rows)
- [ ] create_message with reply_to_id links to parent
- [ ] get_replies returns all replies to a message
- [ ] reply to nonexistent message raises ValueError
- [ ] reply to message in different channel raises ValueError
- [ ] replies appear in list_messages (normal messages with reply_to_id set)
- [ ] message_routes.py registered in routes/__init__.py
- [ ] All tests pass

## Smoke Test
- [ ] `cd hivenode && python -m pytest tests/hivenode/test_efemera_versioning.py -v` — all pass
- [ ] `cd hivenode && python -m pytest tests/hivenode/test_efemera_threading.py -v` — all pass
- [ ] `cd hivenode && python -m pytest tests/ -v` — no regressions

## Constraints
- Port the versioning/threading logic from platform — don't redesign
- Edit creates new rows, never mutates existing rows
- Reply threading is flat (one level), not recursive
- Routes go in NEW message_routes.py, NOT in existing routes.py
- No file exceeds 500 lines
- TDD: write tests first

## Response File
20260328-EFEMERA-CONN-10-RESPONSE.md
