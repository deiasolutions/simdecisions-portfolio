# TASK-EFEMERA-CONN-09: Port RBAC + System Channels

**Priority:** P1
**Depends on:** CONN-07
**Blocks:** None
**Model:** Sonnet
**Role:** Bee

## Objective

Port the RBAC permission system and system channel auto-seeding from platform to hivenode. This gives efemera proper permission checks on channel operations and automatic creation of the 10+ system channels on first boot.

## Read First

- `.deia/BOOT.md` — hard rules
- Platform source:
  - `C:\Users\davee\OneDrive\Documents\GitHub\platform\platform\efemera\src\efemera\auth\roles.py` (51 lines)
  - `C:\Users\davee\OneDrive\Documents\GitHub\platform\platform\efemera\src\efemera\channels\system_channels.py` (216 lines)
  - `C:\Users\davee\OneDrive\Documents\GitHub\platform\platform\efemera\src\efemera\channels\routes.py` (158 lines) — RBAC usage
- `hivenode/efemera/store.py` — current store (extend with RBAC checks)
- `hivenode/efemera/routes.py` — current routes (add permission checks)
- `.deia/hive/responses/20260328-EFEMERA-ASSESSMENT.md` — sections 1.1, 1.4

## Files to Create

### 1. `hivenode/efemera/roles.py` (~50 lines)

Direct port from platform's `roles.py`.

```python
from enum import Enum

class UserRole(str, Enum):
    MEMBER = "member"
    ADMIN = "admin"
    OWNER = "owner"

class ChannelPermission(str, Enum):
    READ_CHANNEL = "read_channel"
    WRITE_CHANNEL = "write_channel"
    LEAVE_CHANNEL = "leave_channel"
    MANAGE_CHANNEL = "manage_channel"
    JOIN_CHANNEL = "join_channel"
    SEND_MESSAGE = "send_message"
    READ_MESSAGES = "read_messages"

PERMISSION_MATRIX: dict[UserRole, set[ChannelPermission]] = {
    UserRole.MEMBER: {
        ChannelPermission.READ_CHANNEL,
        ChannelPermission.WRITE_CHANNEL,
        ChannelPermission.LEAVE_CHANNEL,
        ChannelPermission.SEND_MESSAGE,
        ChannelPermission.READ_MESSAGES,
    },
    UserRole.ADMIN: {
        ChannelPermission.READ_CHANNEL,
        ChannelPermission.WRITE_CHANNEL,
        ChannelPermission.LEAVE_CHANNEL,
        ChannelPermission.MANAGE_CHANNEL,
        ChannelPermission.JOIN_CHANNEL,
        ChannelPermission.SEND_MESSAGE,
        ChannelPermission.READ_MESSAGES,
    },
    UserRole.OWNER: {
        ChannelPermission.READ_CHANNEL,
        ChannelPermission.WRITE_CHANNEL,
        ChannelPermission.MANAGE_CHANNEL,
        ChannelPermission.JOIN_CHANNEL,
        ChannelPermission.SEND_MESSAGE,
        ChannelPermission.READ_MESSAGES,
    },
}

def has_permission(role: str, permission: ChannelPermission) -> bool:
    """Check if a role has a specific permission."""
    try:
        user_role = UserRole(role)
    except ValueError:
        return False
    return permission in PERMISSION_MATRIX.get(user_role, set())
```

Note: OWNER cannot LEAVE (intentional — owner must transfer ownership first).

### 2. `hivenode/efemera/system_channels.py` (~150 lines)

Port from platform's `system_channels.py`. Adapt from SQLAlchemy to our SQLite store.

```python
from hivenode.efemera.store import EfemeraStore

SYSTEM_CHANNELS = [
    {"id": "commons", "name": "commons", "type": "commons", "pinned": True, "description": "General discussion for everyone."},
    {"id": "the-buzz", "name": "the-buzz", "type": "the_buzz", "pinned": True, "description": "What's happening right now."},
    {"id": "announcements", "name": "announcements", "type": "announcements", "pinned": True, "description": "Official announcements.", "read_only": True},
    {"id": "the-window", "name": "the-window", "type": "the_window", "pinned": False, "description": "Public-facing channel."},
    {"id": "dev", "name": "dev", "type": "dev", "pinned": False, "description": "Development discussion."},
    {"id": "approvals", "name": "approvals", "type": "approvals", "pinned": False, "description": "Pending approvals queue."},
    {"id": "moderation-log", "name": "moderation-log", "type": "moderation_log", "pinned": False, "description": "Moderation actions log."},
    {"id": "bugs-admin", "name": "bugs-admin", "type": "bugs_admin", "pinned": False, "description": "Bug reports and admin alerts."},
    {"id": "bok-submissions", "name": "bok-submissions", "type": "bok_submissions", "pinned": False, "description": "Body of Knowledge submissions."},
    {"id": "humans-only", "name": "humans-only", "type": "humans_only", "pinned": False, "description": "No bots allowed."},
]

def seed_system_channels(store: EfemeraStore) -> None:
    """Create system channels if they don't exist. Idempotent."""
    for ch_def in SYSTEM_CHANNELS:
        existing = store.get_channel(ch_def["id"])
        if not existing:
            store.create_channel(
                name=ch_def["name"],
                channel_type=ch_def["type"],
                created_by="system",
                pinned=ch_def.get("pinned", False),
            )
            # Add system welcome message
            store.create_message(
                channel_id=ch_def["id"],
                author_id="system",
                author_name="System",
                content=f"Welcome to #{ch_def['name']}. {ch_def.get('description', '')}",
                author_type="system",
                message_type="system",
            )

def create_personal_channel(store: EfemeraStore, user_id: str, display_name: str) -> dict:
    """Create a personal channel for a user. Returns existing if already created."""
    personal_id = f"personal-{user_id}"
    existing = store.get_channel(personal_id)
    if existing:
        return existing
    channel = store.create_channel(
        name=f"{display_name}'s Notes",
        channel_type="personal",
        created_by=user_id,
        pinned=False,
    )
    store.create_message(
        channel_id=channel["id"],
        author_id="system",
        author_name="System",
        content=f"This is your personal channel, {display_name}. Only you can see it.",
        author_type="system",
        message_type="system",
    )
    store.add_member(channel["id"], user_id, display_name, role="owner")
    return channel
```

### Update `hivenode/efemera/store.py`

**Replace `_seed_defaults()`:**
```python
def _seed_defaults(self) -> None:
    """Seed system channels if none exist."""
    from hivenode.efemera.system_channels import seed_system_channels
    cursor = self._conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM channels")
    if cursor.fetchone()[0] == 0:
        seed_system_channels(self)
```

**Update `create_channel()`** to accept `description` and `read_only` params.

### Update `hivenode/efemera/routes.py`

**Add RBAC checks** to existing endpoints:
- `create_message`: check `has_permission(role, SEND_MESSAGE)` for the user's role in the channel
- `list_messages`: check `has_permission(role, READ_MESSAGES)`
- `create_channel`: no RBAC needed (anyone can create)
- `join_channel`: check `has_permission(role, JOIN_CHANNEL)` — new members default to MEMBER role
- `leave_channel`: check owner cannot leave (`has_permission` returns False for OWNER + LEAVE)

**For local mode** (no JWT): skip RBAC checks. Use `verify_jwt_or_local()` pattern — local always has full access.

## Tests to Create

### `tests/hivenode/test_efemera_rbac.py`
- MEMBER has read, write, leave, send, read_messages
- ADMIN has all of MEMBER + manage, join
- OWNER has all except leave
- Unknown role returns False
- has_permission with invalid permission returns False

### `tests/hivenode/test_efemera_system_channels.py`
- seed_system_channels creates all 10 channels
- seed_system_channels is idempotent (running twice doesn't duplicate)
- Each system channel has a welcome message
- create_personal_channel creates channel + adds user as owner
- create_personal_channel returns existing if already created

## Constraints

- Port from platform code — don't redesign the RBAC model
- Local mode (no JWT) bypasses RBAC entirely
- System channel seeding is idempotent
- No file exceeds 500 lines
- TDD: write tests first
