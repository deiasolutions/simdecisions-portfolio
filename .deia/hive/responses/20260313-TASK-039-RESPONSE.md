# TASK-039: Node Announcement Client -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-13

## Files Modified

### Created
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\node\__init__.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\node\client.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\node\heartbeat.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\node\__init__.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\node\test_node_client.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\node\test_node_integration.py`

### Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` — Added node_id field + auto-generation logic
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\schemas.py` — Added NodeLocalStatusResponse
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\node.py` — Added local routes (GET /node/status, GET /node/peers)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py` — Added set_node_client() and get_node_client()
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` — Integrated node announcement + heartbeat into lifespan

## What Was Done

### 1. Node Announcement Client (`client.py`)
- Implemented `NodeAnnouncementClient` class with HTTP client to cloud hivenode
- Auto-loads JWT from `~/.shiftcenter/token` (optional)
- `announce()` — POST /node/announce with node info (returns timestamp or None)
- `heartbeat()` — POST /node/heartbeat (returns True/False for 404 handling)
- `discover()` — GET /node/discover (returns list of NodeInfo objects)
- Auto-detects IP via ipify.org API, falls back to local IP
- Gets volumes from VolumeRegistry
- Returns static capabilities list: ["storage", "sync", "ledger", "shell"]
- Graceful error handling: network errors logged, don't crash
- Tracks connection status: `_cloud_connected`, `_last_announced_at`, `_last_heartbeat_at`

### 2. Heartbeat Worker (`heartbeat.py`)
- Implemented `HeartbeatWorker` class with asyncio background task
- Sends heartbeat every 60 seconds
- Re-announces automatically on 404 response (node expired)
- Logs events to Event Ledger:
  - `NODE_HEARTBEAT` — successful heartbeat
  - `NODE_RECONNECTED` — re-announce after expiry
- Graceful shutdown via `stop()` method (cancels task, no leaked tasks)

### 3. Config Integration (`config.py`)
- Added `node_id` field to `HivenodeConfig`
- Loads node_id from `~/.shiftcenter/config.yml` or generates new UUID-based ID
- Auto-saves generated node_id to config.yml for persistence
- Uses format `node-{uuid[:12]}` (e.g., "node-abc123def456")

### 4. Startup Integration (`main.py`)
- Integrated node announcement into FastAPI lifespan
- On startup (local/remote mode only):
  - Creates `NodeAnnouncementClient` with settings
  - Creates `HeartbeatWorker` with client + ledger
  - Calls `announce()` immediately
  - Logs `NODE_ANNOUNCED` event to ledger
  - Starts heartbeat worker
- On shutdown:
  - Stops heartbeat worker gracefully
  - Closes HTTP client

### 5. Local Node Routes (`node.py`)
- Added GET /node/status — returns node info (id, mode, port, volumes, capabilities, cloud connection status)
- Added GET /node/peers — returns list of peer nodes from cloud discovery
- Only available in local/remote mode (400 error in cloud mode)
- Uses `get_node_client()` dependency

### 6. Dependencies (`dependencies.py`)
- Added global `_node_client` variable
- Added `set_node_client()` setter (called in lifespan)
- Added `get_node_client()` getter for dependency injection

### 7. Schemas (`schemas.py`)
- Added `NodeLocalStatusResponse` schema with all node status fields

### 8. Tests (16 tests, all passing)

**`test_node_client.py` (13 tests):**
- Announcement: success, network error, 401, 400
- Heartbeat: success, 404 (re-announce), network error
- Discover: success, network error, 401
- Heartbeat worker: sends heartbeat, re-announces on 404, stops gracefully

**`test_node_integration.py` (3 tests):**
- Startup announcement integration (announces + logs to ledger)
- GET /node/status route returns node info
- GET /node/peers route returns peer list

## Test Results

```
============================= 16 passed in 3.26s ==============================
```

All tests pass. No existing tests broken.

## Acceptance Criteria

✅ NodeAnnouncementClient announces to cloud on startup
✅ Heartbeat worker sends heartbeat every 60 seconds
✅ Worker re-announces automatically on 404 response
✅ Discover returns list of online nodes from cloud
✅ Network errors handled gracefully (log, don't crash)
✅ Local routes return node status and peer list
✅ Event Ledger logs NODE_ANNOUNCED, NODE_HEARTBEAT, NODE_RECONNECTED
✅ All tests pass (16/16)
✅ No crashes if cloud is unreachable

## Notes

- Node ID stored in `~/.shiftcenter/config.yml` for persistence
- JWT auth is optional — if token file doesn't exist, requests skip auth header
- IP auto-detection uses ipify.org, falls back to local IP (may be 192.168.x.x behind NAT)
- Heartbeat interval: 60 seconds
- Cloud marks nodes offline after 5 minutes (see NodeStore)
- Actor format for ledger events: `node:{node_id}` (e.g., "node:node-abc123")
- HTTP client base URL defaults to `https://api.shiftcenter.com`
- All event payloads use dict (not JSON string) for `payload_json` parameter
- Graceful degradation: network errors return None/empty list, don't crash hivenode
- Background task properly cancelled on shutdown (no leaked tasks)

## Files Created

- hivenode/node/__init__.py (4 lines)
- hivenode/node/client.py (229 lines)
- hivenode/node/heartbeat.py (87 lines)
- tests/hivenode/node/__init__.py (1 line)
- tests/hivenode/node/test_node_client.py (257 lines)
- tests/hivenode/node/test_node_integration.py (142 lines)

**Total:** 6 files, ~720 lines of code + tests

## Dependencies

- httpx (async HTTP client)
- pyyaml (config file)
- uuid (node ID generation)

All dependencies already in project.
