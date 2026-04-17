# TASK-EFEMERA-CONN-08: Port RBAC + System Channels

## Objective
Port the RBAC permission system and system channel auto-seeding from platform to shiftcenter. After this task, efemera has role-based channel permissions and automatically creates system channels on startup.

## Context
Platform has:
- `auth/roles.py`: UserRole enum (MEMBER, ADMIN, OWNER), ChannelPermission enum (7 permissions), permission matrix, `has_permission()` function
- `channels/system_channels.py`: `ensure_system_channels()` auto-seeds 10 system channels, `ensure_personal_channel()` creates per-user channels with welcome messages

ShiftCenter currently has no permission checks and only 3 hardcoded default channels.

**Depends on:** TASK-EFEMERA-CONN-07 (schema must support channel types and member roles).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\auth\roles.py` (51 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\channels\system_channels.py` (216 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\store.py` (after CONN-07 modifications)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\efemera\routes.py` (169 lines — will need permission checks)

## Deliverables

### 1. Create `hivenode/efemera/roles.py` (~60 lines)
- [ ] `UserRole` enum: MEMBER, ADMIN, OWNER
- [ ] `ChannelPermission` enum: READ_CHANNEL, WRITE_CHANNEL, LEAVE_CHANNEL, MANAGE_CHANNEL, JOIN_CHANNEL, SEND_MESSAGE, READ_MESSAGES
- [ ] `ROLE_PERMISSIONS` dict mapping each role to its allowed permissions
- [ ] `has_permission(role: UserRole, permission: ChannelPermission) -> bool` function
- [ ] Permission matrix matches platform: MEMBER gets read/write/leave/send/read_messages; ADMIN adds manage/join; OWNER same as ADMIN

### 2. Create `hivenode/efemera/system_channels.py` (~150 lines)
- [ ] `SYSTEM_USER_ID = "system"` constant
- [ ] `SYSTEM_CHANNELS` list: 10 channels (commons, humans-only, the-buzz, announcements, dev, approvals, moderation_log, bugs_admin, bok_submissions, the_window) with their types, descriptions, and pinned status
- [ ] `ensure_system_channels(store: EfemeraStore) -> dict[str, str]` — creates system channels if they don't exist, returns {name: channel_id} mapping
- [ ] `ensure_personal_channel(store: EfemeraStore, user_id: str, display_name: str) -> str` — creates personal-{user_id[:8]} channel with welcome message, returns channel_id
- [ ] System channels are owned by SYSTEM_USER_ID
- [ ] System channels use read_only=True for announcements and moderation_log

### 3. Modify `hivenode/efemera/store.py`
- [ ] Update `_seed_defaults()` to call `ensure_system_channels()` instead of hardcoding 3 channels
- [ ] Import and use the new system_channels module

### 4. Modify `hivenode/efemera/routes.py`
- [ ] Add permission checks to message creation: verify sender has SEND_MESSAGE permission on channel
- [ ] Add permission checks to channel access: verify reader has READ_CHANNEL permission
- [ ] Public channels (commons, the_buzz, announcements, dev, the_window) auto-allow non-members to read
- [ ] Personal channels only visible to owner
- [ ] Add `POST /channels/{channel_id}/join` endpoint
- [ ] Add `POST /channels/{channel_id}/leave` endpoint (owner cannot leave)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing efemera tests still pass
- [ ] New test file: `tests/hivenode/test_efemera_rbac.py`

### Test cases required (20+ tests):
**RBAC:**
- MEMBER has READ_CHANNEL permission
- MEMBER has SEND_MESSAGE permission
- MEMBER does NOT have MANAGE_CHANNEL permission
- ADMIN has MANAGE_CHANNEL permission
- ADMIN has JOIN_CHANNEL permission
- OWNER has all permissions
- has_permission with invalid role returns False

**System channels:**
- ensure_system_channels creates 10 channels
- ensure_system_channels is idempotent (second call creates nothing)
- System channels have correct types
- announcements and moderation_log are read_only
- ensure_personal_channel creates channel
- ensure_personal_channel is idempotent
- Personal channel has welcome message

**Route permission checks:**
- Non-member can read public channel
- Non-member cannot read private channel → 403
- Member can send message to channel
- Non-member cannot send message to private channel → 403
- Join endpoint adds member
- Join endpoint 400 if already member
- Leave endpoint removes member
- Leave endpoint 400 if owner tries to leave

## Constraints
- No file over 500 lines
- No stubs
- Port from platform — do NOT redesign the permission model
- SQLite-based (not SQLAlchemy ORM — match existing store pattern)
- System channels must be created at store initialization (not on first HTTP request)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-EFEMERA-CONN-08-RESPONSE.md`

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
