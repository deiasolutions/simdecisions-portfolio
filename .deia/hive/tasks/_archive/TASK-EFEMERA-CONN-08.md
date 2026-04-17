# TASK-EFEMERA-CONN-08: Port WebSocket Manager

**Priority:** P1
**Depends on:** CONN-07
**Blocks:** None
**Model:** Sonnet
**Role:** Bee

## Objective

Port the WebSocket connection manager from platform to hivenode. This provides real-time message delivery, typing indicators, and presence tracking — replacing polling as the primary transport.

## Read First

- `.deia/BOOT.md` — hard rules
- Platform source: `C:\Users\davee\OneDrive\Documents\GitHub\platform\platform\efemera\src\efemera\ws.py` (139 lines)
- `hivenode/efemera/store.py` — presence store methods
- `hivenode/efemera/routes.py` — existing route registration
- `.deia/hive/responses/20260328-EFEMERA-ASSESSMENT.md` — section 1.3 (WebSocket Manager)

## File to Create

### `hivenode/efemera/ws.py` (~150 lines)

Port from platform's `ws.py`. This file contains BOTH the `ConnectionManager` class AND the WebSocket endpoint function. The endpoint is registered in `hivenode/routes/__init__.py` separately from the existing efemera REST router.

**Registration in `routes/__init__.py`:**
```python
from hivenode.efemera.ws import websocket_endpoint
app.add_api_websocket_route("/efemera/ws", websocket_endpoint)
```

**ConnectionManager class:**
```python
from fastapi import WebSocket
from datetime import datetime, UTC
from typing import Dict, Optional
from dataclasses import dataclass, field

@dataclass
class PresenceEntry:
    user_id: str
    display_name: str
    connected_at: str
    last_active: str

    @property
    def status(self) -> str:
        """Returns 'online' if active in last 5 min, else 'idle'."""
        ...

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}  # user_id -> ws
        self.channel_subscriptions: Dict[str, set] = {}     # channel_id -> {user_id, ...}
        self.presence: Dict[str, PresenceEntry] = {}        # user_id -> PresenceEntry

    async def connect(self, websocket: WebSocket, user_id: str, display_name: str) -> None
    def disconnect(self, user_id: str) -> None
    async def subscribe_channel(self, user_id: str, channel_id: str) -> None
    def unsubscribe_channel(self, user_id: str, channel_id: str) -> None
    async def broadcast_to_channel(self, channel_id: str, message: dict, exclude_user: Optional[str] = None) -> None
    async def send_to_user(self, user_id: str, message: dict) -> None
    def get_online_users(self) -> list
    def touch_presence(self, user_id: str) -> None  # update last_active
```

### WebSocket Endpoint (in ws.py, same file as ConnectionManager)

```python
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_id: str = "anonymous", display_name: str = "User"):
    manager = get_connection_manager()
    await manager.connect(websocket, user_id, display_name)
    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")

            if msg_type == "subscribe":
                await manager.subscribe_channel(user_id, data["channelId"])

            elif msg_type == "unsubscribe":
                manager.unsubscribe_channel(user_id, data["channelId"])

            elif msg_type == "message":
                # Save to store, then broadcast
                store = _get_store()
                msg = store.create_message(
                    channel_id=data["channelId"],
                    author_id=user_id,
                    author_name=display_name,
                    content=data["content"],
                )
                await manager.broadcast_to_channel(data["channelId"], {
                    "type": "message",
                    "data": msg,
                }, exclude_user=user_id)

            elif msg_type == "typing":
                await manager.broadcast_to_channel(data["channelId"], {
                    "type": "typing",
                    "data": {"userId": user_id, "displayName": display_name, "channelId": data["channelId"]},
                }, exclude_user=user_id)

            elif msg_type == "stop_typing":
                await manager.broadcast_to_channel(data["channelId"], {
                    "type": "stop_typing",
                    "data": {"userId": user_id, "channelId": data["channelId"]},
                }, exclude_user=user_id)

            elif msg_type == "heartbeat":
                manager.touch_presence(user_id)

    except WebSocketDisconnect:
        manager.disconnect(user_id)
```

### Module-level singleton

```python
_manager: Optional[ConnectionManager] = None

def get_connection_manager() -> ConnectionManager:
    global _manager
    if _manager is None:
        _manager = ConnectionManager()
    return _manager
```

## Tests to Create

### `tests/hivenode/test_efemera_ws.py`

- connect: WebSocket accepted, user added to active_connections
- disconnect: user removed, channel subscriptions cleaned up
- subscribe_channel: user added to channel set
- broadcast_to_channel: message sent to all subscribed users except sender
- message: saved to store and broadcast
- typing: broadcast to channel (not saved to store)
- heartbeat: updates last_active
- presence status: online if active < 5 min, idle otherwise
- get_online_users: returns all connected users with status

Use `TestClient` from Starlette with `with client.websocket_connect("/efemera/ws") as ws:` pattern.

## Constraints

- Port from platform code — don't rewrite from scratch
- Adapt SQLAlchemy patterns to our SQLite store
- Use FastAPI WebSocket (not raw asyncio WebSocket)
- Single global ConnectionManager instance (module-level singleton, same pattern as _store)
- No file exceeds 500 lines
- TDD: write tests first
