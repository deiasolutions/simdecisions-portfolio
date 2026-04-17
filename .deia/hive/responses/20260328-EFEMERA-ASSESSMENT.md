# Efemera Assessment: Platform vs. ShiftCenter

**Date:** 2026-03-28
**Author:** Q33N (QUEEN-2026-03-28-BRIEFING-EFEMERA-CO)
**Purpose:** Cross-repo audit of efemera implementation — what platform built, what shiftcenter ported, what's missing.

---

## 1. Platform Efemera — Full Feature Set

The platform repo contains a mature messaging system across ~1,900 lines of backend code plus ~900 lines of tests.

### 1.1 Channels (channels/)

| File | Lines | What It Does |
|------|-------|--------------|
| `models.py` | 82 | SQLAlchemy ORM: Channel, ChannelMember. ChannelType enum (11 types). Pydantic schemas. |
| `routes.py` | 158 | CRUD + join/leave. RBAC permission checks. Personal channel filtering. Public channel auto-allow. |
| `public_routes.py` | 49 | Public read-only endpoints + WebSocket for "the-window" channel. |
| `system_channels.py` | 216 | Auto-seed 10 system channels. Personal channel creation with welcome message. Keeper bot join. |

**ChannelType enum (11 types):** commons, humans_only, the_buzz, announcements, approvals, moderation_log, bugs_admin, bok_submissions, the_window, dev, personal.

**Key features:**
- Owner/admin/member roles on ChannelMember
- Public channels auto-allow non-members to read
- Personal channels only visible to owner
- Owner cannot leave their own channel
- System user ("system") owns system channels

### 1.2 Messages (messages/)

| File | Lines | What It Does |
|------|-------|--------------|
| `models.py` | 79 | Message ORM with versioning, threading, moderation, author_type, message_type, metadata_json. |
| `routes.py` | 295 | Send (with TASaaS), list, edit (re-versioned), history, reply threads. WebSocket broadcast. Discord forward. |

**Message model fields:**
- `id`, `channel_id`, `sender_id`, `content`, `created_at`
- `version` (int), `parent_id` (edit chain), `edited_at`
- `reply_to_id` (thread replies, distinct from edit chain)
- `moderation_status` (approved/held/blocked), `moderation_reason`
- `provider` (for Discord bridge loop prevention)
- `topic_id`, `topic_name` (topic-based threading)
- `author_type` (human/bot/agent/system)
- `message_type` (text/terminal_output/rag_answer/system)
- `metadata_json` (structured data: queue ids, risk scores, etc.)

**Key features:**
- Edit versioning: edits create new rows with parent_id=original, version++
- Reply threading: reply_to_id points to parent message (separate from edit versioning)
- TASaaS moderation pipeline on all sends and edits
- Display name resolution from User table
- WebSocket broadcast for approved messages
- Discord bridge forwarding (with loop prevention via provider field)
- Slash command interception: messages starting with `/` routed to command system

### 1.3 WebSocket Manager (ws.py)

| File | Lines | What It Does |
|------|-------|--------------|
| `ws.py` | 139 | ConnectionManager with presence tracking, typing indicators, public channel WebSocket. |

**Key features:**
- Per-connection PresenceEntry: user_id, display_name, connected_at, last_active
- Auto idle detection: 5-minute timeout, status property returns "online" or "idle"
- Deduplicated presence by user_id (latest connection per user)
- Separate public_connections dict for read-only public channels
- Typing indicator broadcast: `{"type": "typing"/"stop_typing", "user_id", "display_name", "channel_id"}`
- Heartbeat: plain text messages keep presence alive
- REST endpoint: `GET /api/presence` returns all online/idle users

### 1.4 RBAC (auth/roles.py)

| File | Lines | What It Does |
|------|-------|--------------|
| `roles.py` | 51 | UserRole enum (3 roles), ChannelPermission enum (7 permissions), permission matrix, has_permission(). |

**Roles:** MEMBER, ADMIN, OWNER

**Permissions:** READ_CHANNEL, WRITE_CHANNEL, LEAVE_CHANNEL, MANAGE_CHANNEL, JOIN_CHANNEL, SEND_MESSAGE, READ_MESSAGES

**Matrix:**
- MEMBER: read, write, leave, send, read_messages
- ADMIN: all of member + manage, join
- OWNER: all of admin (same as admin in current matrix)

### 1.5 Moderation (moderation/)

| File | Lines | What It Does |
|------|-------|--------------|
| `logger.py` | 73 | Logs moderation events to moderation_log channel. Logs errors to bugs_admin channel. |
| `routes.py` | 161 | Moderation queue (held/blocked), review (approve/reject), resubmit, withdraw. |

**Endpoints:** queue listing, message review, resubmit through pipeline, sender withdrawal.

### 1.6 TASaaS Content Safety (tasaas/)

| File | Lines | What It Does |
|------|-------|--------------|
| `pipeline.py` | 130 | Sequential scanner pipeline: PII detection, content classification, crisis detection. Three decisions: pass/flag/block. |

**Pipeline:** PII scanner (emails, phones, SSNs, credit cards) -> Content classifier (toxic, hate) -> Crisis detector (suicide, violence, harm). Priority: crisis/hate=BLOCK, toxic+PII=FLAG, PII=FLAG, clean=PASS.

### 1.7 Commands (commands/)

| File | Lines | What It Does |
|------|-------|--------------|
| `router.py` | 39 | Command dispatcher with registry pattern. |
| `parser.py` | 57 | `/command arg1 --flag value` parser. |
| `status_commands.py` | 207 | /status, /burn, /tasks, /bees, /log commands. |

### 1.8 Discord Bridge (discord/)

| File | Lines | What It Does |
|------|-------|--------------|
| `routes.py` | 142 | Discord bridge start/stop/send/status. Loop prevention via provider field. |

### 1.9 Tests

| File | Lines | Coverage |
|------|-------|----------|
| `test_api.py` | 198 | Channel CRUD, message send/edit/history, version tracking |
| `test_moderation.py` | 659 | PII, toxicity, crisis, moderation queue, review, resubmit, withdraw, audit |
| `test_ws.py` | 34 | WebSocket connect, broadcast, multi-client |

**Total test coverage:** 891 lines, ~30+ test cases.

---

## 2. ShiftCenter Efemera — Current State

### 2.1 Backend

| File | Lines | What It Has |
|------|-------|-------------|
| `hivenode/efemera/store.py` | 224 | SQLite store. 4 tables: channels, messages, members, presence. Basic CRUD. No versioning, no threading, no moderation, no author_type/message_type fields. |
| `hivenode/efemera/routes.py` | 169 | FastAPI REST API. 8 endpoints. No RBAC, no moderation, no system channels. |

**What's missing from backend:**
- No channel types enum (only 'channel'|'dm')
- No system channel auto-seeding (only 3 hardcoded defaults)
- No personal channels
- No message versioning (no parent_id, no version field)
- No reply threading (no reply_to_id)
- No moderation pipeline
- No author_type/message_type/metadata_json fields
- No RBAC permission checks
- No WebSocket support
- No typing indicators
- No slash command integration
- No Discord bridge
- No display name resolution

### 2.2 Frontend

| File | Lines | What It Has |
|------|-------|-------------|
| `browser/src/services/efemera/relayPoller.ts` | 97 | Polling service. Polls `/efemera/channels/{id}/messages?since=`. Emits `channel:message-received` on bus. |
| `browser/src/primitives/tree-browser/adapters/channelsAdapter.ts` | 132 | Fetches channels from `/efemera/channels`. Mock fallback. Groups by pinned/regular/DM. |
| `browser/src/primitives/tree-browser/adapters/membersAdapter.ts` | 113 | Fetches members from `/efemera/channels/{id}/members`. Mock fallback. Groups by status. |
| `browser/src/primitives/terminal/useTerminal.ts` (relay section) | ~67 lines (468-535) | POST messages to `/efemera/channels/{id}/messages`. Bus send to text-pane. Error handling. |
| `browser/src/primitives/text-pane/SDEditor.tsx` (efemera section) | ~42 lines (369-410) | channel:selected -> fetch messages. channel:message-received -> append. |

**What's missing from frontend:**
- No connector service (HTTP calls scattered across 4 files)
- No presence management (no heartbeats, no idle detection)
- No typing indicators
- No message editing
- No reply threading UI
- No unread tracking (field exists but always 0)
- No channel creation from UI
- No member role display logic beyond badge

### 2.3 Bus Events (Already Defined)

| Event | Typed Interface | Used By |
|-------|-----------------|---------|
| `channel:selected` | `ChannelSelectedData` | channelsAdapter -> terminal + text-pane |
| `channel:message-sent` | `ChannelMessageData` | terminal -> bus (after POST) |
| `channel:message-received` | `ChannelMessageData` | relayPoller -> text-pane |
| `channel:messages-loaded` | `ChannelMessagesLoadedData` | defined but unused |
| `presence:update` | `PresenceUpdateData` | defined but unused |

### 2.4 EGG Config

The efemera.egg.md defines:
- 5 panes: chrome-menu, channels sidebar, messages (text-pane), compose (terminal), members sidebar
- Terminal routeTarget: 'relay'
- Terminal links: to_text=efemera-messages, to_channels=efemera-channels
- Commands: new-channel, new-dm, toggle-members, search-messages (handlers not implemented)
- Settings: pollingInterval=3000, presenceAutoIdle=300000
- Permissions: bus_emit/bus_receive whitelists for channel and presence events

### 2.5 Existing Tests

| File | Coverage |
|------|----------|
| `tests/hivenode/test_efemera.py` | Backend store + API tests (29 tests) |
| `tests/hivenode/test_efemera_smoke.py` | Smoke tests |
| `browser/src/apps/__tests__/efemera.channels.integration.test.tsx` | Frontend channelsAdapter (7 tests) |

---

## 3. Gap Analysis — What Needs Porting

### 3.1 Backend Gaps (Priority Order)

| # | Feature | Platform Has | ShiftCenter Has | Gap Size |
|---|---------|-------------|-----------------|----------|
| 1 | Channel type enum | 11 types | 2 types (channel/dm) | Medium |
| 2 | System channel seeding | 10 auto-seeded channels + personal | 3 hardcoded defaults | Medium |
| 3 | RBAC | 3 roles, 7 permissions, matrix | No permission checks | Large |
| 4 | Message versioning | version field, parent_id chain, history endpoint | None | Large |
| 5 | Reply threading | reply_to_id, replies endpoint | None | Medium |
| 6 | Message model fields | author_type, message_type, metadata_json, provider | None | Medium |
| 7 | Moderation pipeline | TASaaS (PII, toxicity, crisis), 3 decisions | None | Large |
| 8 | Moderation queue | Queue listing, review, resubmit, withdraw | None | Large |
| 9 | WebSocket manager | Per-connection presence, typing, public channels | None (polling only) | Large |
| 10 | Typing indicators | WS broadcast typing/stop_typing | None | Medium |
| 11 | Presence management | PresenceEntry with auto-idle, REST endpoint | Basic status table | Medium |
| 12 | Command system | Registry, parser, 5 built-in commands | None in efemera context | Medium |
| 13 | Discord bridge | Full bridge with loop prevention | None | Medium |
| 14 | Moderation logging | Log to system channels | None | Small |
| 15 | Personal channels | Per-user with welcome message | None | Medium |
| 16 | Channel join/leave | Endpoints with RBAC | None | Small |
| 17 | Display name resolution | User table lookup | Hardcoded "You" | Small |

### 3.2 Frontend Gaps

| # | Feature | Platform Has | ShiftCenter Has | Gap Size |
|---|---------|-------------|-----------------|----------|
| 1 | Connector service | N/A (monolith) | HTTP scattered across 4 files | Large (new design) |
| 2 | Presence heartbeats | WebSocket keep-alive | None | Medium |
| 3 | Typing indicators | WS-based | None | Medium |
| 4 | Message editing UI | PUT endpoint used | None | Medium |
| 5 | Reply threading UI | reply_to_id support | None | Medium |
| 6 | Unread tracking | Functional | Field exists, always 0 | Medium |
| 7 | Channel creation UI | POST endpoint used | No UI (command defined in EGG but handler missing) | Small |
| 8 | Member role management | RBAC + admin UI | Display-only badges | Small |
| 9 | Idle detection | WebSocket-based | EGG config has presenceAutoIdle but no implementation | Medium |

### 3.3 Architecture Debt

| Issue | Impact |
|-------|--------|
| Terminal (useTerminal.ts) directly POSTs to efemera HTTP endpoints | Primitive coupled to backend service |
| Text-pane (SDEditor.tsx) directly fetches efemera messages on channel:selected | Primitive coupled to backend service |
| channelsAdapter.ts directly calls /efemera/channels | Adapter coupled to HTTP layer |
| membersAdapter.ts directly calls /efemera/channels/{id}/members | Adapter coupled to HTTP layer |
| relayPoller.ts is standalone — not coordinated with channel selection or presence | No unified lifecycle |
| No single service owns efemera state | State scattered across 5 files |
| No error coordination — each file handles errors independently | Inconsistent error UX |

---

## 4. Connector Architecture Rationale

The briefing's proposed connector pattern is correct. The current architecture violates primitive isolation: terminal, text-pane, and tree-browser all know about efemera HTTP endpoints. This must change.

**The connector should:**
1. Be the ONLY code that calls efemera HTTP/WS endpoints
2. Own all state: active channel, message cache, presence, members
3. Coordinate all panes through bus events exclusively
4. Start when efemera EGG loads, stop when EGG unloads
5. Be testable in isolation (mock bus, mock HTTP)

**The refactored primitives should:**
1. Never import from `services/efemera/` (except connector bootstrap)
2. Never call `fetch()` for efemera endpoints
3. Only emit and listen to bus events for efemera data
4. Remain usable in non-efemera EGGs (no efemera coupling in base code)

---

## 5. Recommendations

### Phase 1: Connector + Refactor (Decouple)
Build the connector service, refactor primitives to use bus events only. This is the foundation — nothing else works without it.

### Phase 2: Backend Model Upgrade
Port channel types, RBAC, message versioning, reply threading, system channels from platform. Extend the SQLite schema.

### Phase 3: Moderation Pipeline
Port TASaaS pipeline, moderation queue, moderation routes. This is safety-critical.

### Phase 4: Real-Time (WebSocket)
Port WebSocket manager from platform. Add typing indicators, presence heartbeats. Replace polling as primary transport (keep polling as fallback).

### Phase 5: Integration Features
Port command system, Discord bridge hooks, personal channels, display name resolution.

---

## 6. Line Counts Summary

| Area | Platform Lines | ShiftCenter Lines | Gap |
|------|---------------|-------------------|-----|
| Backend models + routes | ~820 | 393 | -427 |
| Moderation | ~364 | 0 | -364 |
| WebSocket | 139 | 0 | -139 |
| RBAC | 51 | 0 | -51 |
| Commands | 303 | 0 | -303 |
| Discord bridge | 142 | 0 | -142 |
| Frontend services | 0 (monolith) | 342 | N/A |
| Frontend primitive coupling | 0 | ~109 | -109 (to remove) |
| Tests | 891 | ~36+ | -855 |
| **Total** | **~2,710** | **~880** | **~-1,830** |
