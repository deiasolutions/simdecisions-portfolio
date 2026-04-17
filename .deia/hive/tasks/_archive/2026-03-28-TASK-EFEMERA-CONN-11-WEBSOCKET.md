# TASK-EFEMERA-CONN-11: Port WebSocket Manager

## Objective
Port the WebSocket connection manager from platform. After this task, efemera supports real-time message delivery and typing indicators via WebSocket, with HTTP polling as a fallback.

## Context
Platform has a ConnectionManager (`ws.py`, 139 lines) that tracks per-connection presence, broadcasts messages via WebSocket, and supports typing indicators. ShiftCenter currently uses HTTP polling only (relayPoller, 3-second interval).

This task adds the WebSocket endpoint to hivenode. The frontend connector (CONN-02) will initially still use polling but can be upgraded to WebSocket in a future task.

**Depends on:** TASK-EFEMERA-CONN-07 (schema), TASK-EFEMERA-CONN-08 (presence management). Can run in parallel with CONN-09 and CONN-10.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\ws.py` (139 lines — reference implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\store.py` (presence methods)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\routes.py` (to see where WS endpoint registers)

## Deliverables

### 1. Create `hivenode/efemera/ws.py` (~140 lines)
Port from platform's `ws.py`:

**PresenceEntry class:**
- [ ] Fields: user_id, display_name, connected_at, last_active
- [ ] `touch()` method: updates last_active to now
- [ ] `status` property: returns 'online' if last_active < 5 min ago, else 'idle'
- [ ] `to_dict()` method: serializes to dict

**ConnectionManager class:**
- [ ] `active_connections: list[WebSocket]` — authenticated clients
- [ ] `public_connections: dict[str, list[WebSocket]]` — {channel_id: [ws, ...]}
- [ ] `_presence: dict[WebSocket, PresenceEntry]` — per-connection presence
- [ ] `async connect(ws, user_id, display_name)` — accept, add to list, create PresenceEntry
- [ ] `disconnect(ws)` — remove from all lists, delete presence
- [ ] `touch(ws)` — update last_active
- [ ] `get_presence() -> list[dict]` — deduplicated by user_id (latest per user)
- [ ] `async connect_public(ws, channel_id)` — add to public connections
- [ ] `disconnect_public(ws, channel_id)` — remove from public
- [ ] `async broadcast(message: dict, exclude=None)` — send JSON to all authenticated + relevant public

**WebSocket endpoint:**
- [ ] Route: `ws /efemera/ws?user_id=<str>&display_name=<str>`
- [ ] Accept connection, track presence
- [ ] Receive loop: plain text = heartbeat (touch presence). JSON with `type: "typing"/"stop_typing"` + `channel_id` = broadcast typing event
- [ ] On disconnect: clean up
- [ ] Typing broadcasts: `{"type": "typing"/"stop_typing", "user_id", "display_name", "channel_id"}`

**REST endpoint:**
- [ ] `GET /efemera/presence/ws` — returns WebSocket-tracked presence (deduplicated)

### 2. Integrate broadcast into message creation
- [ ] When a message is approved (moderation_status='approved'), broadcast via WebSocket:
  ```json
  {"type": "new_message", "data": {"id": "...", "channel_id": "...", "author_name": "...", "content": "...", "created_at": "..."}}
  ```
- [ ] This supplements (not replaces) the HTTP polling mechanism

### 3. Register WebSocket endpoint
- [ ] Register WS route in `hivenode/efemera/routes.py` or `hivenode/routes/__init__.py`
- [ ] Ensure FastAPI WebSocket route is properly configured

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing efemera tests still pass
- [ ] New test file: `tests/hivenode/test_efemera_ws.py`

### Test cases required (15+ tests):
**ConnectionManager:**
- connect adds to active_connections
- disconnect removes from active_connections
- touch updates last_active
- get_presence returns online for recent connections
- get_presence returns idle for stale connections (mock time)
- get_presence deduplicates by user_id
- connect_public adds to public_connections
- disconnect_public removes from public_connections
- broadcast sends to all connections
- broadcast excludes specified connection

**WebSocket endpoint:**
- Connect with user_id and display_name
- Send plain text heartbeat (touch presence)
- Send typing event (broadcast to others)
- Send stop_typing event (broadcast to others)
- Disconnect cleans up

**Integration:**
- Message creation broadcasts to connected clients

## Constraints
- No file over 500 lines
- No stubs
- Use FastAPI WebSocket (`from fastapi import WebSocket`)
- IDLE_TIMEOUT = 300 seconds (5 minutes) — match platform
- WebSocket is SUPPLEMENTAL to polling — polling still works as primary transport
- Module-level `manager = ConnectionManager()` singleton (same pattern as platform)
- Handle WebSocket errors gracefully (client may disconnect unexpectedly)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-EFEMERA-CONN-11-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
