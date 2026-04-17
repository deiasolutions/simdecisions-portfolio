# Efemera Connector — Architecture Design v2

**Date:** 2026-03-28
**Author:** Q33NR (revised from Q33N v1)
**Status:** APPROVED — ready for task specs

---

## 1. Overview

The Efemera Connector is a **primitive** — a registered appType like terminal, text-pane, or tree-browser. It renders the left sidebar of the efemera EGG with two tabs (Channels and Members) and owns all backend communication via WebSocket (primary) and HTTP polling (fallback).

**Key decisions (Q33NR):**
- The connector is a primitive, not a service. It mounts/unmounts with the EGG like any other pane.
- WebSocket is built in the same batch — primary transport, polling as fallback.
- Clean event rename to `efemera:*` namespace — no parallel migration period.
- No generic EGG services schema. The connector is a registered appType, period.

**What changes from v1:**
- ~~Tree-browser with channelsAdapter~~ → Connector primitive renders channels directly
- ~~Tree-browser with membersAdapter~~ → Connector renders members as second tab
- ~~Service layer started via lifecycle hook~~ → Primitive mounted by EGG layout
- ~~Polling-first, WS later~~ → WebSocket primary, polling fallback

---

## 2. Architecture

### 2.1 The Primitive

`efemera-connector` is registered in `apps/index.ts` like every other appType. The EGG layout references it as `"appType": "efemera-connector"`.

It renders:
- **Two tabs** in the sidebar: Channels (channel list with unread badges, presence dots, typing indicators) and Members (member list with online/idle/offline status, role badges)
- **No other visible chrome** — the content area is the full sidebar surface

It owns:
- WebSocket connection to hivenode (primary transport)
- HTTP polling fallback (when WS unavailable)
- All efemera state: active channel, message cache, member list, presence, typing
- Bus coordination with terminal (compose) and text-pane (messages)

### 2.2 Leveraging Existing Code

| Existing Code | What We Keep | What Changes |
|---------------|-------------|-------------|
| `channelsAdapter.ts` — `channelToNode()`, grouping logic, `ChannelData` interface | Keep `ChannelData` interface and grouping logic (pinned/channels/DMs). Reuse `channelToNode()` for rendering. | Remove `fetchChannels()` HTTP call and mock fallback. Connector owns data fetching. |
| `membersAdapter.ts` — `memberToNode()`, grouping logic, `MemberData` interface | Keep `MemberData` interface and grouping logic (online/idle/offline). Reuse `memberToNode()` for rendering. | Remove `fetchMembers()` HTTP call and mock fallback. Connector owns data fetching. |
| `relayPoller.ts` — polling loop, lastTimestamp tracking, interval management | Keep polling logic as fallback transport inside connector. | Move into connector's messageService module. Delete standalone file. |
| `store.py` — SQLite schema (channels, messages, members, presence tables) | Keep entire store. All 4 tables remain. | Extend messages table with versioning/threading fields. Add channel type enum. |
| `routes.py` — 8 FastAPI endpoints | Keep all existing endpoints. | Add WebSocket endpoint. Extend with join/leave, edit, replies, version history. |
| `treeBrowserAdapter.tsx` — `handleSelect` for channels adapter (lines 276-289) | Pattern for bus event emission on channel click. | This code path removed (connector handles clicks directly). |
| `useTerminal.ts` — relay mode (lines 182-194, 468-535) | Error classification pattern (`classifyError`, `getErrorMessage`). | Remove all relay HTTP code. Terminal emits `efemera:message-send` on Enter, listens for `efemera:message-sent` to clear input. |
| `SDEditor.tsx` — efemera bus handlers (lines 369-410) | Chat rendering pattern (markdown format: `**author:** content`). | Remove HTTP fetch and channel:selected handler. Listen for `efemera:messages-loaded` and `efemera:message-received`. |
| `sidebarAdapter.tsx` — activity bar + switchable panel pattern | Two-tab UI pattern with activity bar icons. | Connector builds its own tabbed UI using the same pattern, but renders channel/member lists directly instead of delegating to TreeBrowserAdapter. |
| `TreeBrowser.tsx` — pure presentational tree component | Reuse for rendering channel and member lists inside the connector tabs. TreeBrowser already accepts `nodes[]`, handles selection, expand/collapse. | Pass nodes from connector state instead of from an adapter's async load. |

### 2.3 Module Structure

```
browser/src/primitives/efemera-connector/
  EfemeraConnector.tsx       — React component (registered primitive), two-tab UI  (~200 lines)
  useEfemeraConnector.ts     — Hook: WebSocket, polling, bus wiring, state          (~250 lines)
  channelService.ts          — Channel CRUD, list caching, grouping (from adapter)  (~120 lines)
  messageService.ts          — Message send/receive, polling fallback, history      (~180 lines)
  presenceService.ts         — Presence heartbeat, idle detection, WebSocket ping   (~120 lines)
  memberService.ts           — Member list fetch, role display                      (~80 lines)
  wsTransport.ts             — WebSocket connection, reconnect, message routing     (~150 lines)
  types.ts                   — Shared types (Channel, Message, Member, Presence)    (~80 lines)
  index.ts                   — Public exports                                       (~10 lines)
  __tests__/
    EfemeraConnector.test.tsx
    useEfemeraConnector.test.ts
    channelService.test.ts
    messageService.test.ts
    presenceService.test.ts
    wsTransport.test.ts
```

**Estimated total:** ~1,190 lines across 8 modules (all under 500-line limit) + ~600 lines tests.

### 2.4 EGG Layout Change

**Before:**
```json
{
  "type": "pane",
  "nodeId": "efemera-channels",
  "appType": "tree-browser",
  "config": { "adapter": "channels", "header": "Channels" }
}
```
Plus separate members pane:
```json
{
  "type": "pane",
  "nodeId": "efemera-members",
  "appType": "tree-browser",
  "config": { "adapter": "members", "header": "Members" }
}
```

**After:**
```json
{
  "type": "pane",
  "nodeId": "efemera-connector",
  "appType": "efemera-connector",
  "label": "Efemera",
  "chrome": false,
  "config": {
    "tabs": [
      { "id": "channels", "icon": "#", "label": "Channels" },
      { "id": "members", "icon": "@", "label": "Members" }
    ],
    "defaultTab": "channels",
    "pollingIntervalMs": 3000,
    "presenceAutoIdleMs": 300000
  }
}
```

The separate members pane is removed from the layout. The connector owns both surfaces.

---

## 3. Bus Event Contract

### 3.1 Events the Connector LISTENS FOR

| Event Type | Source | Data Shape | Connector Action |
|-----------|--------|------------|------------------|
| `efemera:message-send` | terminal (compose) | `{ content: string, replyToId?: string }` | Send message via WS (or POST fallback). Emit `efemera:message-sent` on success. |
| `efemera:channel-create` | command palette | `{ name: string, type: 'channel' \| 'dm' }` | POST channel. Reload channel list. |
| `efemera:typing-start` | terminal (on keydown) | `{ channelId: string }` | Forward via WS. |
| `efemera:typing-stop` | terminal (on idle) | `{ channelId: string }` | Forward via WS. |

### 3.2 Events the Connector EMITS

**All events use `target: '*'` (broadcast).** Consumers filter by type via `bus.subscribeType()`. No targeted delivery to specific paneIds — this keeps the bus contract simple and testable.

| Event Type | Target | Data Shape | Consumed By |
|-----------|--------|------------|-------------|
| `efemera:channel-changed` | `*` | `{ channelId, channelName, type }` | terminal (update prompt label), text-pane (clear + loading) |
| `efemera:messages-loaded` | `*` | `{ channelId, messages: Message[] }` | text-pane (render full history) |
| `efemera:message-received` | `*` | `{ channelId, message: Message }` | text-pane (append single message) |
| `efemera:message-sent` | `*` | `{ channelId, message: Message }` | terminal (setLoading(false), clear input) |
| `efemera:presence-changed` | `*` | `{ userId, status, displayName }` | connector (update member status icons) |
| `efemera:typing` | `*` | `{ userId, displayName, channelId }` | text-pane (show typing indicator) |
| `efemera:typing-stop` | `*` | `{ userId, channelId }` | text-pane (hide typing indicator) |
| `efemera:error` | `*` | `{ code, message, context? }` | terminal (setLoading(false), show inline error) |
| `efemera:ready` | `*` | `{}` | signals init complete |

### 3.3 What Dies

These old events are removed entirely (clean swap, no migration period):
- `channel:selected` — replaced by connector's internal tab click + `efemera:channel-changed`
- `channel:message-sent` — replaced by `efemera:message-sent`
- `channel:message-received` — replaced by `efemera:message-received`
- `channel:messages-loaded` — replaced by `efemera:messages-loaded`
- `terminal:text-patch` for relay mode — connector emits `efemera:messages-loaded` / `efemera:message-received` directly

---

## 4. Data Flow

### 4.1 User Sends a Message

```
User types in terminal → [Enter]
  → terminal emits bus: efemera:message-send { content }
  → connector receives via subscribeType
  → connector sends via WebSocket (or POST fallback)
  → on success: connector emits efemera:message-sent → terminal clears input
  → on success: connector emits efemera:message-received → text-pane appends
  → on error: connector emits efemera:error → terminal shows error
```

### 4.2 User Clicks a Channel

```
User clicks channel row in connector's Channels tab
  → connector sets activeChannelId internally (no bus needed — it owns the state)
  → connector emits efemera:channel-changed → terminal updates prompt, text-pane clears
  → connector fetches message history (HTTP GET)
  → connector emits efemera:messages-loaded → text-pane renders history
  → connector fetches member list (HTTP GET)
  → connector updates Members tab internally
  → connector switches WS subscription to new channel
```

### 4.3 WebSocket Message Arrives

```
WS receives new message for active channel
  → wsTransport routes to messageService
  → connector emits efemera:message-received → text-pane appends
```

### 4.4 WebSocket Unavailable (Fallback)

```
WS connection fails or not supported
  → wsTransport sets fallbackMode = true
  → messageService starts polling (interval from EGG settings, default 3s)
  → poll detects new messages → connector emits efemera:message-received
```

---

## 5. Primitive Refactoring

### 5.1 Terminal (useTerminal.ts) — Relay Mode

**REMOVE:**
- Lines 182-194: `channel:selected` bus subscription (connector owns channel state)
- Lines 468-535: Relay mode HTTP POST + `terminal:text-patch` + `channel:message-sent` emission

**REPLACE WITH:**
- On Enter (relay mode): `setLoading(true)`, emit `efemera:message-send { content }`
- On `efemera:message-sent`: `setLoading(false)`, clear input
- On `efemera:channel-changed`: update prompt label to `#channelName`
- On `efemera:error`: `setLoading(false)`, show inline error

**Net:** ~67 lines removed, ~25 lines added.

### 5.2 Text-Pane (SDEditor.tsx) — Chat Mode

**REMOVE:**
- Lines 369-398: `channel:selected` handler that fetches from `/efemera/channels/{id}/messages`
- Lines 401-410: `channel:message-received` handler that appends content

**REPLACE WITH:**
- On `efemera:messages-loaded`: replace content with rendered message history
- On `efemera:message-received`: append single message
- On `efemera:channel-changed`: clear content, show loading state
- On `efemera:typing` / `efemera:typing-stop`: show/hide typing indicator (required, with 5s auto-clear timeout)

**Net:** ~42 lines removed, ~45 lines added.

### 5.3 Adapters + Tree Browser

**channelsAdapter.ts:** Keep file. Remove `fetchChannels()` and mock data. Export `channelToNode()`, `groupChannels()`, and `ChannelData` interface for the connector to import. (CONN-05 runs before CONN-02.)

**membersAdapter.ts:** Keep file. Remove `fetchMembers()` and mock data. Export `memberToNode()`, `groupMembers()`, and `MemberData` interface for the connector to import. (CONN-05 runs before CONN-02.)

**treeBrowserAdapter.tsx:** Remove the `channels` and `members` adapter paths (lines 74-77 in the load function, lines 276-289 in handleSelect). These paths are dead once the connector renders channels/members directly.

**relayPoller.ts:** Delete after connector is complete. Polling logic moves into connector's messageService.

---

## 6. Backend Changes

### 6.1 WebSocket Endpoint

New endpoint: `WS /efemera/ws`

Ported from platform's `ws.py` (139 lines). Connection manager with:
- Per-connection presence tracking (PresenceEntry)
- Auto idle detection (5-minute timeout)
- Channel subscription (client sends `{ type: "subscribe", channelId }`)
- Message broadcast to subscribed clients
- Typing indicator relay
- Heartbeat (ping/pong)
- Reconnect support (client sends last seen timestamp)

### 6.2 Schema Extensions (store.py)

**messages table — add columns:**
- `version INTEGER DEFAULT 1`
- `parent_id TEXT` (edit chain)
- `reply_to_id TEXT` (thread replies)
- `edited_at TEXT`
- `author_type TEXT DEFAULT 'human'`
- `message_type TEXT DEFAULT 'text'`
- `metadata_json TEXT`

**channels table — extend type CHECK:**
- From: `CHECK(type IN ('channel', 'dm'))`
- To: `CHECK(type IN ('channel', 'dm', 'commons', 'announcements', 'the_buzz', 'the_window', 'dev', 'personal', 'moderation_log', 'bugs_admin', 'approvals', 'humans_only', 'bok_submissions'))`
- Add `description TEXT`, `read_only BOOLEAN DEFAULT FALSE`

### 6.3 New Backend Modules

| Module | Port From | Lines (est.) | Created By |
|--------|-----------|-------------|-----------|
| `hivenode/efemera/ws.py` | `platform/ws.py` | ~150 | CONN-08 |
| `hivenode/efemera/system_channels.py` | `platform/channels/system_channels.py` | ~150 | CONN-09 |
| `hivenode/efemera/roles.py` | `platform/auth/roles.py` | ~50 | CONN-09 |
| `hivenode/efemera/message_routes.py` | `platform/messages/routes.py` | ~100 | CONN-10 |
| `hivenode/efemera/moderation/pipeline.py` | `platform/tasaas/pipeline.py` | ~130 | CONN-11 |
| `hivenode/efemera/moderation/routes.py` | `platform/moderation/routes.py` | ~160 | CONN-11 |
| `hivenode/efemera/moderation/logger.py` | `platform/moderation/logger.py` | ~70 | CONN-11 |
| `hivenode/efemera/commands/router.py` | `platform/commands/router.py` | ~40 | CONN-12 |
| `hivenode/efemera/commands/parser.py` | `platform/commands/parser.py` | ~57 | CONN-12 |
| `hivenode/efemera/commands/status_commands.py` | `platform/commands/status_commands.py` | ~150 | CONN-12 |

### 6.4 Route Extensions

**Existing routes.py — extend with (CONN-07 only):**
- `POST /channels/{id}/join`
- `POST /channels/{id}/leave`

**New message_routes.py (CONN-10):**
- `PUT /messages/{id}` (edit with versioning)
- `GET /messages/{id}/history` (version chain)
- `GET /messages/{id}/replies`

**WebSocket endpoint (CONN-08):**
- `WS /efemera/ws` — registered via `app.add_api_websocket_route()`, not the efemera REST router

**Moderation routes (CONN-11):**
- `GET /moderation/queue`, `POST /moderation/messages/{id}/review`, etc.

**create_message modifications (sequential: CONN-07 → CONN-11 → CONN-12):**
- CONN-07: add optional params (author_type, message_type, moderation_status, etc.)
- CONN-11: add moderation pipeline intercept
- CONN-12: add slash command intercept (before moderation)

---

## 7. Task Breakdown

### Phase A: Foundation (sequential)
1. **CONN-01**: Types + service modules (channelService, messageService, presenceService, memberService, wsTransport) — data layer, no UI, no bus
2. **CONN-05**: Clean up adapters — export `channelToNode()`, `memberToNode()`, `groupChannels()`, `groupMembers()` as public functions. Strip HTTP. Delete relayPoller.ts. (Must run BEFORE CONN-02 so imports work.)
3. **CONN-02**: EfemeraConnector primitive — React component with two-tab UI, bus wiring, registered appType. Imports from CONN-01 services and CONN-05 exported functions.

### Phase B: Primitive Refactoring (parallel after CONN-02)
4. **CONN-03**: Refactor terminal relay mode — remove HTTP, use `efemera:*` bus events, add loading state management
5. **CONN-04**: Refactor text-pane chat mode — remove HTTP, use `efemera:*` bus events, add typing indicator (required)

### Phase C: EGG + Integration (after Phase B)
6. **CONN-06**: Update efemera.egg.md — new layout with efemera-connector pane, new bus permissions, remove old tree-browser panes

### Phase D: Backend Upgrades (independent of frontend)
7. **CONN-07**: Backend schema upgrade — extend messages table, channel types, optional channel_id for create_channel, new columns
8. **CONN-08**: Port WebSocket manager from platform — ws.py has ConnectionManager + endpoint (parallel with CONN-09, CONN-10)
9. **CONN-09**: Port RBAC + system channels — roles.py, system_channels.py with known IDs, seeding (parallel with CONN-08, CONN-10)
10. **CONN-10**: Port message versioning + reply threading — `message_routes.py` (separate from routes.py), edit chain, reply_to_id (parallel with CONN-08, CONN-09)
11. **CONN-11**: Port moderation pipeline — depends on CONN-07 + CONN-09 (needs system channels for logger)
12. **CONN-12**: Port command system — depends on CONN-11 (commands intercept BEFORE moderation in create_message)

### Dependencies
```
CONN-01 → CONN-05 (export pure functions) → CONN-02 → CONN-03, CONN-04 (parallel) → CONN-06
CONN-07 → CONN-08, CONN-09, CONN-10 (parallel after schema)
CONN-07 + CONN-09 → CONN-11 → CONN-12 (sequential: commands intercept before moderation)
Phase D is independent of Phase A-C (backend vs frontend)
```

---

## 8. Test Strategy

| Module | Tests (est.) | What It Tests |
|--------|-------------|---------------|
| `EfemeraConnector.test.tsx` | 15 | Tab switching, channel click → state update, bus event emission, lifecycle |
| `useEfemeraConnector.test.ts` | 12 | Bus subscription routing, channel switch flow, error handling |
| `channelService.test.ts` | 8 | loadChannels, createChannel, cache, grouping (reuse channelsAdapter logic) |
| `messageService.test.ts` | 12 | loadMessages, sendMessage, polling start/stop/fallback |
| `presenceService.test.ts` | 10 | heartbeat, idle detection, status transitions |
| `wsTransport.test.ts` | 10 | connect, reconnect, message routing, fallback trigger |
| Backend tests | 30+ | WebSocket, RBAC, versioning, threading, moderation pipeline |

All frontend tests: mock MessageBus + mock fetch/WebSocket. No real backend.
