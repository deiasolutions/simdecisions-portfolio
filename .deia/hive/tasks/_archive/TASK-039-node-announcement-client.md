# TASK-039: Node Announcement Client

**Role:** BEE (coder)
**Model:** Sonnet
**Parent:** SPEC-HIVENODE-E2E-001 Wave 4
**Spec sections:** 9.1–9.3
**Date:** 2026-03-12
**Estimated tests:** ~12

---

## Objective

Build the client-side node announcement flow. The local hivenode announces itself to the cloud hivenode on startup, sends periodic heartbeats, and can discover other nodes.

**This is backend-only Python work. No browser changes.**

---

## What Already Exists (Cloud Side — Receiving End)

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\node_store.py` — NodeStore with `announce()`, `heartbeat()`, `discover()`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\node.py` — POST `/node/announce`, GET `/node/discover`, POST `/node/heartbeat`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\schemas.py` — NodeAnnounceRequest, NodeHeartbeatRequest, NodeAnnounceResponse, NodeHeartbeatResponse, NodeInfo, NodeDiscoverResponse

**Cloud routes already work. This task builds the client that calls them.**

---

## What to Build

### 1. Node Announcement Client

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\node\client.py`

**Class:** `NodeAnnouncementClient`

**Methods:**

#### `__init__(self, config: HivenodeConfig)`

Initialize client with config:

- Store `cloud_url` from config (e.g., `https://api.shiftcenter.com`)
- Load JWT from `~/.shiftcenter/token` (if exists)
- Create `httpx.AsyncClient` with:
  - `base_url = cloud_url`
  - `headers = {"Authorization": f"Bearer {jwt}"}` (if JWT exists)
  - `timeout = 30.0`

#### `async def announce(self) -> str`

POST to cloud hivenode `/node/announce`:

**Request body (NodeAnnounceRequest):**

```python
{
  "node_id": config.node_id,      # From ~/.shiftcenter/config.yml
  "mode": config.mode,             # "local" or "remote"
  "ip": self._get_ip(),            # Auto-detect IP
  "port": config.port,             # 8420
  "volumes": self._get_volumes(),  # From VolumeRegistry
  "capabilities": self._get_capabilities()
}
```

**Response (NodeAnnounceResponse):**

```python
{
  "ok": True,
  "announced_at": "2026-03-12T10:30:00Z"
}
```

**Returns:** `announced_at` timestamp

**Error handling:**

- Network error → log warning, return None (graceful degradation)
- 401 Unauthorized → log error "JWT expired or invalid", return None
- 400 Bad Request → log error with response detail, return None
- 500 Server Error → log error, return None

#### `async def heartbeat(self) -> bool`

POST to cloud hivenode `/node/heartbeat`:

**Request body (NodeHeartbeatRequest):**

```python
{
  "node_id": config.node_id
}
```

**Response (NodeHeartbeatResponse):**

```python
{
  "ok": True,
  "last_seen": "2026-03-12T10:35:00Z"
}
```

**Returns:** `True` if successful, `False` if 404 (node expired)

**Special handling:**

- 404 Not Found → return False (caller should re-announce)
- Network error → log warning, return True (assume temporary failure)
- Other errors → log warning, return True

#### `async def discover(self) -> List[NodeInfo]`

GET from cloud hivenode `/node/discover`:

**Response (NodeDiscoverResponse):**

```python
{
  "nodes": [
    {
      "node_id": "node-abc123",
      "user_id": "user-xyz",
      "mode": "local",
      "ip": "192.168.1.100",
      "port": 8420,
      "volumes": ["home"],
      "capabilities": ["storage", "sync"],
      "announced_at": "2026-03-12T10:00:00Z",
      "last_seen": "2026-03-12T10:35:00Z",
      "online": True
    }
  ]
}
```

**Returns:** List of `NodeInfo` objects

**Error handling:**

- Network error → log warning, return empty list
- 401 Unauthorized → log error, return empty list
- Other errors → log warning, return empty list

#### Helper Methods

**`def _get_ip(self) -> str`**

Auto-detect public IP:

1. Try `httpx.get("https://api.ipify.org")` (public IP service)
2. Fall back to `socket.gethostbyname(socket.gethostname())` (local IP)
3. Fall back to `"127.0.0.1"`

**`def _get_volumes(self) -> List[str]`**

Get volume names from VolumeRegistry:

```python
from hivenode.storage.registry import VolumeRegistry

registry = VolumeRegistry()  # Uses default config
return list(registry._adapters.keys())  # ["home", "cloud"]
```

**`def _get_capabilities(self) -> List[str]`**

Return static list of capabilities:

```python
return ["storage", "sync", "ledger", "shell"]
```

---

### 2. Heartbeat Worker

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\node\heartbeat.py`

**Class:** `HeartbeatWorker`

**Purpose:** Background async task that sends heartbeat every 60 seconds.

#### `__init__(self, client: NodeAnnouncementClient, ledger: LedgerWriter)`

Store client and ledger references.

#### `async def start(self)`

Start background heartbeat loop:

1. Create `asyncio.Task` that runs `self._heartbeat_loop()`
2. Store task in `self._task`

#### `async def stop(self)`

Stop background heartbeat:

1. If `self._task` exists, call `self._task.cancel()`
2. Wait for task to finish with `await self._task` (ignore CancelledError)

#### `async def _heartbeat_loop(self)`

Infinite loop:

```python
while True:
    try:
        success = await self.client.heartbeat()

        if success:
            # Log to Event Ledger
            self.ledger.log(
                event_type="NODE_HEARTBEAT",
                actor=self.client.config.node_id,
                domain="node",
            )
        else:
            # 404 response — node expired, re-announce
            announced_at = await self.client.announce()
            if announced_at:
                self.ledger.log(
                    event_type="NODE_RECONNECTED",
                    actor=self.client.config.node_id,
                    domain="node",
                    payload_json=json.dumps({"announced_at": announced_at})
                )
    except asyncio.CancelledError:
        break  # Graceful shutdown
    except Exception as e:
        # Log error but don't crash
        print(f"[HeartbeatWorker] Error: {e}")

    await asyncio.sleep(60)  # 60 seconds
```

---

### 3. Startup Announcement

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (modify existing lifespan)

**In `lifespan()` function:**

Add after existing initialization, before `yield`:

```python
# Initialize node announcement (local/remote mode only)
if settings.mode in ["local", "remote"]:
    from hivenode.node.client import NodeAnnouncementClient
    from hivenode.node.heartbeat import HeartbeatWorker

    node_client = NodeAnnouncementClient(settings)
    heartbeat_worker = HeartbeatWorker(node_client, ledger_writer)

    # Announce on startup
    announced_at = await node_client.announce()
    if announced_at:
        ledger_writer.log(
            event_type="NODE_ANNOUNCED",
            actor=settings.node_id,  # Assumes node_id added to config
            domain="node",
            payload_json=json.dumps({"announced_at": announced_at})
        )

    # Start heartbeat worker
    await heartbeat_worker.start()
else:
    heartbeat_worker = None
```

**After `yield` (shutdown):**

```python
# Stop heartbeat worker
if heartbeat_worker:
    await heartbeat_worker.stop()
```

**Note:** This assumes `settings.node_id` exists. If not, add it to `HivenodeConfig` by reading from `~/.shiftcenter/config.yml`.

---

### 4. Local-Mode Routes

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\node_local.py`

**Router:** `APIRouter()`

These routes work in local mode (unlike the cloud-only `/node/announce` etc.).

#### `GET /node/status`

**Response (new schema: NodeLocalStatusResponse):**

```python
{
  "node_id": str,
  "mode": str,
  "port": int,
  "volumes": List[str],
  "capabilities": List[str],
  "cloud_connected": bool,     # True if last announce succeeded
  "last_announced_at": str | None,
  "last_heartbeat_at": str | None
}
```

**Implementation:**

```python
@router.get("/status", response_model=NodeLocalStatusResponse)
async def get_node_status(
    client: NodeAnnouncementClient = Depends(get_node_client)
):
    return NodeLocalStatusResponse(
        node_id=client.config.node_id,
        mode=client.config.mode,
        port=client.config.port,
        volumes=client._get_volumes(),
        capabilities=client._get_capabilities(),
        cloud_connected=client._cloud_connected,  # Track in client
        last_announced_at=client._last_announced_at,
        last_heartbeat_at=client._last_heartbeat_at
    )
```

#### `GET /node/peers`

**Response:** `NodeDiscoverResponse` (reuse from cloud routes)

**Implementation:**

```python
@router.get("/peers", response_model=NodeDiscoverResponse)
async def get_peers(
    client: NodeAnnouncementClient = Depends(get_node_client)
):
    nodes = await client.discover()
    return NodeDiscoverResponse(nodes=nodes)
```

**Dependency injection:**

Add to `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py`:

```python
_node_client: Optional[NodeAnnouncementClient] = None

def init_node_client(client: NodeAnnouncementClient):
    global _node_client
    _node_client = client

def get_node_client() -> NodeAnnouncementClient:
    if not _node_client:
        raise HTTPException(status_code=503, detail="Node client not initialized")
    return _node_client
```

Call `init_node_client(node_client)` in `main.py` lifespan after creating client.

---

## File Structure

```
hivenode/node/
├── __init__.py           [CREATE] Empty init file
├── client.py             [CREATE] NodeAnnouncementClient class
└── heartbeat.py          [CREATE] HeartbeatWorker class

hivenode/routes/
└── node_local.py         [CREATE] Local-mode node routes

hivenode/
├── main.py               [MODIFY] Add startup announcement + heartbeat
├── dependencies.py       [MODIFY] Add get_node_client()
└── schemas.py            [MODIFY] Add NodeLocalStatusResponse

tests/hivenode/node/
└── test_node_client.py   [CREATE] Test suite
```

---

## Tests

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\node\test_node_client.py`

**Coverage (~12 tests):**

1. **Announcement:**
   - ✓ Successful announce returns timestamp
   - ✓ Network error returns None, logs warning
   - ✓ 401 error returns None, logs error

2. **Heartbeat:**
   - ✓ Successful heartbeat returns True
   - ✓ 404 response returns False (node expired)
   - ✓ Network error returns True, logs warning

3. **Discover:**
   - ✓ Successful discover returns list of nodes
   - ✓ Network error returns empty list
   - ✓ 401 error returns empty list

4. **Heartbeat worker:**
   - ✓ Worker sends heartbeat every 60 seconds (use `asyncio.sleep` mock)
   - ✓ Worker re-announces on 404 response
   - ✓ Worker stops gracefully on shutdown

5. **Startup integration:**
   - ✓ Lifespan calls announce on startup (mock in test)

6. **Local routes:**
   - ✓ GET /node/status returns node info
   - ✓ GET /node/peers returns peer list (mock client.discover())

**Test utilities:**

- Use `pytest-asyncio` for async tests
- Mock `httpx.AsyncClient` with `respx` or manual mocks
- Mock `VolumeRegistry` to return test volumes
- Use `freezegun` to control time for heartbeat tests
- Use FastAPI `TestClient` for route tests

---

## Acceptance Criteria

1. ✅ NodeAnnouncementClient announces to cloud on startup
2. ✅ Heartbeat worker sends heartbeat every 60 seconds
3. ✅ Worker re-announces automatically on 404 response
4. ✅ Discover returns list of online nodes from cloud
5. ✅ Network errors handled gracefully (log, don't crash)
6. ✅ Local routes return node status and peer list
7. ✅ Event Ledger logs NODE_ANNOUNCED, NODE_HEARTBEAT, NODE_RECONNECTED
8. ✅ All tests pass (12/12)
9. ✅ No crashes if cloud is unreachable

---

## Constraints

- No file over 500 lines
- TDD — tests first
- No stubs — every function fully implemented
- Network errors MUST NOT crash hivenode (graceful degradation)
- Heartbeat worker MUST stop gracefully on shutdown (no leaked tasks)
- JWT optional — if not present, skip auth header (local-to-local node discovery future feature)

---

## Dependencies

**Required before start:**
- NodeStore (already built)
- Cloud node routes (already built)
- VolumeRegistry (already built)
- LedgerWriter (already built)

**Blocks:**
- TASK-040 (8os CLI node commands) — partially depends on this task

---

## Notes

- JWT auth is optional for now — if `~/.shiftcenter/token` doesn't exist, skip auth header
- Cloud URL defaults to `https://api.shiftcenter.com` but can be overridden in config
- Node ID is generated on first run and stored in `~/.shiftcenter/config.yml`
- IP auto-detection may return local IP (192.168.x.x) if behind NAT — acceptable for MVP
- Heartbeat interval is 60 seconds, cloud marks nodes offline after 5 minutes (see NodeStore)
- Re-announce logic ensures nodes don't need manual re-registration after cloud restart
