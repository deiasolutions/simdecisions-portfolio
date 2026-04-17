# SPEC-FACTORY-006: Backend Factory Routes (MCP-with-Fallback)

**MODE: EXECUTE**

**Spec ID:** SPEC-FACTORY-006
**Created:** 2026-04-09
**Author:** Q88N
**Type:** BACKEND
**Status:** READY
**Wave:** 1 (no dependencies)

---

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Purpose

Create `/factory` API routes in hivenode for mobile factory operations. Routes **prefer MCP tools when available**, **fallback to file operations when MCP is down**. This ensures the factory keeps running even if MCP crashes.

**Architecture:**
- Browser → hivenode REST → MCP (preferred) → file ops (fallback)
- MCP is sideband, not primary
- File-based task/response flow remains canonical

**Deliverable:** `hivenode/routes/factory_routes.py` (~250 lines) + MCP client wrapper + tests

---

## Endpoints

### GET /factory/responses

List response files with parsed metadata.

**Response:**
```json
{
  "responses": [
    {
      "id": "20260409-FACTORY-001-RESPONSE",
      "filename": "20260409-FACTORY-001-RESPONSE.md",
      "path": ".deia/hive/responses/20260409-FACTORY-001-RESPONSE.md",
      "taskId": "FACTORY-001",
      "beeId": "BEE-SONNET",
      "model": "sonnet",
      "timestamp": "2026-04-09T12:37:00Z",
      "status": "pending",
      "success": true,
      "duration": 282.4,
      "cost": 2.95,
      "turns": 38,
      "excerpt": "Survey complete. Found 17 endpoints...",
      "sections": 27
    }
  ],
  "total": 15,
  "filter": "pending"
}
```

**Query params:**
- `status`: `all` | `pending` | `reviewed` | `archived` (default: `all`)
- `limit`: number (default: 50)
- `offset`: number (default: 0)

**Implementation:**
1. List files in `.deia/hive/responses/`
2. Parse YAML frontmatter / header comments for metadata
3. Extract excerpt (first 200 chars after headers)
4. Count `##` sections
5. Return sorted by timestamp desc

---

### GET /factory/responses/{id}/content

Get full content of a response file.

**Response:**
```json
{
  "id": "20260409-FACTORY-001-RESPONSE",
  "content": "# BEE RESPONSE: FACTORY-001\n\n...",
  "metadata": { ... }
}
```

---

### POST /factory/archive

Archive a completed task (move to `_archive/`).

**Request:**
```json
{
  "taskId": "FACTORY-001",
  "responseId": "20260409-FACTORY-001-RESPONSE"
}
```

**Response:**
```json
{
  "success": true,
  "archivedTask": ".deia/hive/tasks/_archive/SPEC-FACTORY-001.md",
  "archivedResponse": ".deia/hive/responses/_archive/20260409-FACTORY-001-RESPONSE.md",
  "ledgerEventId": "evt_abc123"
}
```

**Implementation:**
1. Move task file to `_archive/`
2. Move response file to `_archive/` (create dir if needed)
3. Emit `TASK_ARCHIVED` to Event Ledger
4. Return paths

---

### POST /factory/spec-submit

Submit a new spec to the backlog.

**Request:**
```json
{
  "title": "Fix SSE reconnect on mobile",
  "type": "bug",
  "priority": "P1",
  "model": "sonnet",
  "description": "## Problem\nSSE stream disconnects...",
  "dependsOn": ["TASK-125"],
  "areaCode": "factory"
}
```

**Response:**
```json
{
  "success": true,
  "specId": "SPEC-BUG-20260409-1234",
  "filename": "SPEC-BUG-20260409-1234.md",
  "path": ".deia/hive/queue/backlog/SPEC-BUG-20260409-1234.md",
  "ledgerEventId": "evt_def456"
}
```

**Implementation:**
1. Validate required fields
2. Generate spec ID: `SPEC-{TYPE}-{YYYYMMDD}-{HHMM}`
3. Render markdown from template
4. Write to `.deia/hive/queue/backlog/`
5. Emit `SPEC_SUBMITTED` to Event Ledger
6. Return spec info

---

### GET /factory/git-summary

Get recent git activity summary.

**Response:**
```json
{
  "branch": "main",
  "dirty": false,
  "uncommittedFiles": 0,
  "recentCommits": [
    {
      "hash": "abc1234",
      "shortHash": "abc1234",
      "message": "[BEE-003] TASK-127: implement approval cards",
      "author": "BEE-003",
      "timestamp": "2026-04-09T12:30:00Z",
      "filesChanged": 5
    }
  ],
  "lastCommitAge": "15 minutes ago"
}
```

**Query params:**
- `limit`: number of commits (default: 20)

**Implementation:**
1. `git rev-parse --abbrev-ref HEAD` — current branch
2. `git status --porcelain` — dirty state
3. `git log --oneline -n {limit}` — recent commits
4. Parse commit info

---

## MCP-with-Fallback Pattern

### Core Principle

Every route follows this pattern:
1. Try MCP tool first (fast, real-time)
2. If MCP unavailable or times out (500ms), fallback to file ops
3. Log which path was taken for debugging

### hivenode/mcp/client.py (New File)

```python
"""
MCP Client Wrapper — Async client with fallback support.

Connects to local MCP server (port 8421).
Returns None on connection failure, letting caller fallback.
"""

import asyncio
import httpx
from typing import Optional, Any
from ..config import settings

MCP_BASE_URL = "http://localhost:8421"
MCP_TIMEOUT = 0.5  # 500ms timeout

class MCPClient:
    def __init__(self):
        self._client: Optional[httpx.AsyncClient] = None
        self._available: Optional[bool] = None
    
    async def _get_client(self) -> Optional[httpx.AsyncClient]:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=MCP_BASE_URL,
                timeout=MCP_TIMEOUT
            )
        return self._client
    
    async def is_available(self) -> bool:
        """Check if MCP server is responding."""
        try:
            client = await self._get_client()
            resp = await client.get("/health")
            self._available = resp.status_code == 200
        except Exception:
            self._available = False
        return self._available
    
    async def call_tool(self, tool_name: str, params: dict = None) -> Optional[dict]:
        """
        Call MCP tool. Returns None if MCP unavailable.
        Caller should fallback to file ops on None.
        """
        try:
            client = await self._get_client()
            resp = await client.post(
                f"/tools/{tool_name}",
                json=params or {}
            )
            if resp.status_code == 200:
                return resp.json()
            return None
        except Exception:
            self._available = False
            return None
    
    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None

# Singleton instance
mcp_client = MCPClient()
```

### Fallback Pattern in Routes

```python
async def list_responses_impl(status: str, limit: int, offset: int):
    """
    List responses — MCP first, file fallback.
    """
    # Try MCP
    mcp_result = await mcp_client.call_tool("response_list", {
        "status": status,
        "limit": limit,
        "offset": offset
    })
    
    if mcp_result is not None:
        logger.debug("list_responses: used MCP")
        return mcp_result
    
    # Fallback to file operations
    logger.debug("list_responses: MCP unavailable, using file fallback")
    return await list_responses_from_files(status, limit, offset)


async def list_responses_from_files(status: str, limit: int, offset: int):
    """
    File-based fallback for listing responses.
    """
    responses = []
    response_dir = RESPONSES_DIR
    
    for f in sorted(response_dir.glob("*.md"), reverse=True):
        if f.name.startswith("_"):
            continue
        
        content = f.read_text()
        metadata = parse_response_metadata(content)
        
        if status != "all" and metadata.get("status") != status:
            continue
        
        responses.append({
            "id": f.stem,
            "filename": f.name,
            "path": str(f),
            **metadata
        })
    
    return {
        "responses": responses[offset:offset + limit],
        "total": len(responses),
        "filter": status,
        "source": "file"  # Indicates fallback was used
    }
```

---

## File Structure

### hivenode/routes/factory_routes.py

```python
"""
Factory Routes — Mobile factory operations API.

MCP-with-fallback pattern:
- Prefer MCP tools when available (fast, real-time)
- Fallback to file operations when MCP is down
- File-based flow remains canonical

Endpoints:
- GET  /factory/responses         — List response files
- GET  /factory/responses/{id}/content — Get response content
- POST /factory/archive           — Archive task + response
- POST /factory/spec-submit       — Submit new spec
- GET  /factory/git-summary       — Git activity summary
- GET  /factory/health            — Service health check
"""

from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
import subprocess
import json
import logging
from datetime import datetime

from ..mcp.client import mcp_client
from ..config import settings
from ..ledger import emit_event

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/factory", tags=["factory"])

RESPONSES_DIR = Path(".deia/hive/responses")
TASKS_DIR = Path(".deia/hive/tasks")
BACKLOG_DIR = Path(".deia/hive/queue/backlog")
ARCHIVE_DIR = Path("_archive")


@router.get("/health")
async def health_check():
    """
    Service health check — reports MCP and file system status.
    """
    mcp_up = await mcp_client.is_available()
    fs_ok = RESPONSES_DIR.exists() and TASKS_DIR.exists()
    
    return {
        "status": "healthy" if fs_ok else "degraded",
        "mcp": "up" if mcp_up else "down",
        "filesystem": "ok" if fs_ok else "error",
        "mode": "mcp" if mcp_up else "file-fallback"
    }


@router.get("/responses")
async def list_responses(
    status: str = Query("all", regex="^(all|pending|reviewed|archived)$"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List response files with metadata. MCP first, file fallback."""
    return await list_responses_impl(status, limit, offset)


@router.get("/responses/{response_id}/content")
async def get_response_content(response_id: str):
    """Get full content of a response file."""
    # MCP attempt
    mcp_result = await mcp_client.call_tool("response_read", {
        "responseId": response_id
    })
    if mcp_result:
        return mcp_result
    
    # File fallback
    file_path = RESPONSES_DIR / f"{response_id}.md"
    if not file_path.exists():
        raise HTTPException(404, f"Response {response_id} not found")
    
    return {
        "id": response_id,
        "content": file_path.read_text(),
        "source": "file"
    }


@router.post("/archive")
async def archive_task(request: ArchiveRequest):
    """Archive a completed task and its response."""
    # MCP attempt
    mcp_result = await mcp_client.call_tool("task_archive", {
        "taskId": request.taskId,
        "responseId": request.responseId
    })
    if mcp_result:
        return mcp_result
    
    # File fallback — move files to _archive/
    return await archive_task_files(request.taskId, request.responseId)


@router.post("/spec-submit")
async def submit_spec(request: SpecSubmitRequest):
    """Submit a new spec to the backlog."""
    # Spec submission always writes to file (canonical)
    # MCP is notified after for real-time pickup
    
    spec_id = generate_spec_id(request.type)
    filename = f"{spec_id}.md"
    file_path = BACKLOG_DIR / filename
    
    content = render_spec_template(request, spec_id)
    file_path.write_text(content)
    
    # Emit to ledger
    event_id = await emit_event("SPEC_SUBMITTED", {
        "specId": spec_id,
        "type": request.type,
        "priority": request.priority,
        "model": request.model
    })
    
    # Notify MCP (non-blocking, best-effort)
    await mcp_client.call_tool("queue_wake", {})
    
    return {
        "success": True,
        "specId": spec_id,
        "filename": filename,
        "path": str(file_path),
        "ledgerEventId": event_id
    }


@router.get("/git-summary")
async def git_summary(limit: int = Query(20, ge=1, le=100)):
    """Get recent git activity summary."""
    # Git ops are always local subprocess
    pass
```

---

## File Targets

| File | Action | Lines |
|------|--------|-------|
| `hivenode/mcp/client.py` | CREATE | ~60 |
| `hivenode/routes/factory_routes.py` | CREATE | ~250 |
| `hivenode/main.py` | MODIFY | +2 (mount router) |
| `tests/hivenode/test_factory_routes.py` | CREATE | ~150 |

---

## Reference Files

Read before implementation:
- `hivenode/routes/build_monitor.py` — existing route pattern
- `hivenode/hive_mcp/local_server.py` — MCP tool definitions
- `hivenode/main.py` — router mounting pattern
- `hivenode/ledger.py` or equivalent — event emission
- `.deia/hive/responses/` — response file format
- `.deia/hive/tasks/` — task file format

---

## Acceptance Criteria

- [ ] MCP client wrapper exists at `hivenode/mcp/client.py`
- [ ] `/factory/health` reports MCP status + filesystem status
- [ ] `/factory/responses` tries MCP first, falls back to file ops
- [ ] `/factory/responses/{id}/content` returns full markdown
- [ ] `/factory/archive` moves files and emits ledger event
- [ ] `/factory/spec-submit` writes to file (canonical), notifies MCP
- [ ] `/factory/git-summary` returns branch, commits, dirty state
- [ ] All endpoints work when MCP is down (file fallback)
- [ ] Response includes `source: "mcp"` or `source: "file"` for debugging
- [ ] Tests pass: `pytest tests/hivenode/test_factory_routes.py -v`

## Smoke Test

```bash
# Start hivenode
cd hivenode && python -m uvicorn main:app --reload &

# Test health endpoint
curl http://127.0.0.1:8420/factory/health | jq
# Should show mcp: "up" or "down"

# Test responses with MCP up
curl http://127.0.0.1:8420/factory/responses | jq
# Check source field

# Kill MCP, test fallback
pkill -f "hive_mcp"
curl http://127.0.0.1:8420/factory/responses | jq
# Should still work, source: "file"

# Test spec submit
curl -X POST http://127.0.0.1:8420/factory/spec-submit \
  -H "Content-Type: application/json" \
  -d '{"title":"Test spec","type":"bug","priority":"P1","model":"sonnet","description":"Test"}' | jq

# Verify file created
ls -la .deia/hive/queue/backlog/
```

## Constraints

- MCP timeout: 500ms max
- File ops are canonical, MCP is optimization
- No file over 250 lines
- All endpoints must work when MCP is down
- Emit events to Event Ledger for all mutations

## Response File

`.deia/hive/responses/20260409-FACTORY-006-RESPONSE.md`

---

*SPEC-FACTORY-006 — Q88N — 2026-04-09*
