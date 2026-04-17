# SPEC-EFEMERA-CONN-08: Port WebSocket Manager -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-28

## Files Modified

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\ws.py` (created, 218 lines)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_efemera_ws.py` (created, 368 lines)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (modified, added WebSocket route registration)
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` (modified, added import for websocket_endpoint)

## What Was Done

- Created `hivenode/efemera/ws.py` porting WebSocket manager from platform
- Implemented `PresenceEntry` class with 5-minute idle timeout
- Implemented `ConnectionManager` class managing active connections, channel subscriptions, and presence tracking
- Implemented `websocket_endpoint` function handling subscribe/unsubscribe, message sending, typing indicators, and heartbeat
- Created module-level singleton pattern for `ConnectionManager` via `get_connection_manager()`
- Registered WebSocket endpoint at `/efemera/ws` in `main.py` via `app.add_api_websocket_route()`
- Created comprehensive test suite with 21 tests covering all acceptance criteria
- All tests pass (21 new tests + 94 existing efemera tests = 115 total)

## Test Results

**New tests (test_efemera_ws.py):** 21 tests, all passing
- PresenceEntry: 5 tests (init, touch, status online/idle, to_dict)
- ConnectionManager: 10 tests (init, connect/disconnect, subscribe/unsubscribe, broadcast, send_to_user, get_online_users, touch_presence)
- WebSocketEndpoint: 5 tests (subscribe, unsubscribe, message broadcast, typing indicator, heartbeat)
- Singleton: 1 test (get_connection_manager returns same instance)

**All efemera tests:** 115 tests passed, 0 failures

```
tests/hivenode/test_efemera_ws.py::TestPresenceEntry::test_init PASSED
tests/hivenode/test_efemera_ws.py::TestPresenceEntry::test_touch_updates_last_active PASSED
tests/hivenode/test_efemera_ws.py::TestPresenceEntry::test_status_online PASSED
tests/hivenode/test_efemera_ws.py::TestPresenceEntry::test_status_idle_after_timeout PASSED
tests/hivenode/test_efemera_ws.py::TestPresenceEntry::test_to_dict PASSED
tests/hivenode/test_efemera_ws.py::TestConnectionManager::test_init PASSED
tests/hivenode/test_efemera_ws.py::TestConnectionManager::test_connect PASSED
tests/hivenode/test_efemera_ws.py::TestConnectionManager::test_disconnect PASSED
tests/hivenode/test_efemera_ws.py::TestConnectionManager::test_subscribe_channel PASSED
tests/hivenode/test_efemera_ws.py::TestConnectionManager::test_unsubscribe_channel PASSED
tests/hivenode/test_efemera_ws.py::TestConnectionManager::test_broadcast_to_channel PASSED
tests/hivenode/test_efemera_ws.py::TestConnectionManager::test_broadcast_to_channel_excludes_sender PASSED
tests/hivenode/test_efemera_ws.py::TestConnectionManager::test_send_to_user PASSED
tests/hivenode/test_efemera_ws.py::TestConnectionManager::test_get_online_users PASSED
tests/hivenode/test_efemera_ws.py::TestConnectionManager::test_touch_presence PASSED
tests/hivenode/test_efemera_ws.py::TestWebSocketEndpoint::test_websocket_endpoint_subscribe PASSED
tests/hivenode/test_efemera_ws.py::TestWebSocketEndpoint::test_websocket_endpoint_unsubscribe PASSED
tests/hivenode/test_efemera_ws.py::TestWebSocketEndpoint::test_websocket_endpoint_message_broadcast PASSED
tests/hivenode/test_efemera_ws.py::TestWebSocketEndpoint::test_websocket_endpoint_typing_indicator PASSED
tests/hivenode/test_efemera_ws.py::TestWebSocketEndpoint::test_websocket_endpoint_heartbeat PASSED
tests/hivenode/test_efemera_ws.py::test_get_connection_manager_singleton PASSED

======================== 21 passed, 1 warning in 0.85s ========================
```

**Regression tests:** All 94 existing efemera tests pass (no regressions)

## Build Verification

All tests pass:
- New WebSocket tests: 21/21 passed
- All efemera tests: 115/115 passed
- No regressions in existing test suite

Test command:
```bash
cd C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter
python -m pytest tests/ -v -k efemera
```

## Acceptance Criteria

- [x] connect: WebSocket accepted, user added to active_connections
- [x] disconnect: user removed, channel subscriptions cleaned up
- [x] subscribe_channel: user added to channel set
- [x] broadcast_to_channel: message sent to all subscribed users except sender
- [x] message type: saved to store and broadcast
- [x] typing type: broadcast to channel (not saved to store)
- [x] heartbeat: updates last_active
- [x] presence status: online if active < 5 min, idle otherwise
- [x] get_online_users: returns all connected users with status
- [x] Endpoint registered via app.add_api_websocket_route("/efemera/ws")
- [x] All tests pass

## Clock / Cost / Carbon

- **Clock:** 22 minutes (research + TDD + implementation + testing)
- **Cost:** ~$0.30 USD (Sonnet 4.5 usage)
- **Carbon:** ~0.5g CO2e (estimated based on token usage)

## Issues / Follow-ups

None. Implementation is complete and fully tested. All acceptance criteria met.

**Notes:**
- The WebSocket endpoint is registered in `main.py` rather than in the routes module because FastAPI WebSocket routes require special handling
- The implementation closely follows the platform pattern with minor adaptations for ShiftCenter's SQLite store
- Presence tracking uses in-memory state (not persisted to SQLite presence table) — this matches platform behavior
- Module-level singleton pattern ensures single ConnectionManager instance across the application
- Tests use AsyncMock for WebSocket testing to avoid TestClient WebSocket context limitations
