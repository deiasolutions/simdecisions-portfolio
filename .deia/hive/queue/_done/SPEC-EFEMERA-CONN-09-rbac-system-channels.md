# SPEC-EFEMERA-CONN-09: Port RBAC + System Channels

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

Port the RBAC permission system and system channel auto-seeding from platform to hivenode. This gives efemera proper permission checks on channel operations and automatic creation of the 10+ system channels on first boot. Uses the optional `channel_id` param added by CONN-07 to create channels with known IDs.

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
        ChannelPermission.READ_CHANNEL, ChannelPermission.WRITE_CHANNEL,
        ChannelPermission.LEAVE_CHANNEL, ChannelPermission.SEND_MESSAGE,
        ChannelPermission.READ_MESSAGES,
    },
    UserRole.ADMIN: {
        ChannelPermission.READ_CHANNEL, ChannelPermission.WRITE_CHANNEL,
        ChannelPermission.LEAVE_CHANNEL, ChannelPermission.MANAGE_CHANNEL,
        ChannelPermission.JOIN_CHANNEL, ChannelPermission.SEND_MESSAGE,
        ChannelPermission.READ_MESSAGES,
    },
    UserRole.OWNER: {
        ChannelPermission.READ_CHANNEL, ChannelPermission.WRITE_CHANNEL,
        ChannelPermission.MANAGE_CHANNEL, ChannelPermission.JOIN_CHANNEL,
        ChannelPermission.SEND_MESSAGE, ChannelPermission.READ_MESSAGES,
    },
}

def has_permission(role: str, permission: ChannelPermission) -> bool:
    try:
        user_role = UserRole(role)
    except ValueError:
        return False
    return permission in PERMISSION_MATRIX.get(user_role, set())
```

Note: OWNER cannot LEAVE (intentional — owner must transfer ownership first).

### 2. `hivenode/efemera/system_channels.py` (~150 lines)

Port from platform. Uses `channel_id` param from CONN-07 to create channels with known IDs.

```python
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

def seed_system_channels(store) -> None:
    """Create system channels if they don't exist. Idempotent."""
    for ch_def in SYSTEM_CHANNELS:
        existing = store.get_channel(ch_def["id"])
        if not existing:
            store.create_channel(
                name=ch_def["name"],
                channel_type=ch_def["type"],
                created_by="system",
                pinned=ch_def.get("pinned", False),
                channel_id=ch_def["id"],  # Use known ID
            )
            store.create_message(
                channel_id=ch_def["id"],
                author_id="system",
                author_name="System",
                content=f"Welcome to #{ch_def['name']}. {ch_def.get('description', '')}",
                author_type="system",
                message_type="system",
            )
```

### Update `hivenode/efemera/store.py`

Replace `_seed_defaults()` to call `seed_system_channels()`.

### Update `hivenode/efemera/routes.py`

Add RBAC checks to existing endpoints. For local mode (no JWT), skip RBAC checks using `verify_jwt_or_local()` pattern.

## Acceptance Criteria
- [ ] MEMBER has read, write, leave, send, read_messages permissions
- [ ] ADMIN has all of MEMBER + manage, join
- [ ] OWNER has all except leave
- [ ] Unknown role returns False
- [ ] seed_system_channels creates all 10 channels with correct IDs
- [ ] seed_system_channels is idempotent (running twice doesn't duplicate)
- [ ] Each system channel has a welcome message
- [ ] create_personal_channel creates channel + adds user as owner
- [ ] create_personal_channel returns existing if already created
- [ ] Local mode bypasses RBAC entirely
- [ ] All tests pass

## Smoke Test
- [ ] `cd hivenode && python -m pytest tests/hivenode/test_efemera_rbac.py -v` — all pass
- [ ] `cd hivenode && python -m pytest tests/hivenode/test_efemera_system_channels.py -v` — all pass
- [ ] `cd hivenode && python -m pytest tests/ -v` — no regressions

## Constraints
- Port from platform code — don't redesign the RBAC model
- Local mode (no JWT) bypasses RBAC entirely
- System channel seeding is idempotent
- No file exceeds 500 lines
- TDD: write tests first

## Response File
20260328-EFEMERA-CONN-09-RESPONSE.md
