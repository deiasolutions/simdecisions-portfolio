# BRIEFING: Efemera Connector — Port, Refactor, and Decouple

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-28
**Priority:** P0

## Context

Efemera is a real-time messaging EGG that runs on Stage. It has a chat window (text-pane), a compose bar (terminal), a channels sidebar, and a members sidebar. These primitives need to communicate with efemera backend services (channels, messages, members, presence).

**Current state:** Efemera backend logic is smeared across three primitives:
- `useTerminal.ts` has ~150 lines of relay-mode code (POST messages, subscribe to channel:selected, send terminal:text-patch)
- `SDEditor.tsx` has efemera-specific code (fetch message history on channel:selected, receive channel:message-received)
- `channelsAdapter.ts` and `membersAdapter.ts` directly call hivenode HTTP endpoints

**Problem:** Primitives should be primitive. The terminal shouldn't know about efemera HTTP endpoints. The text-pane shouldn't fetch efemera messages. An efemera connector service should own all backend communication and coordinate via bus events.

**Platform had more:** The platform/efemera/ implementation had WebSocket real-time sync, RBAC (3 roles, 7 permissions), 11 system channel types, message versioning, reply threading, TASaaS moderation, typing indicators, presence management, and a Discord bridge. Most of this was NOT ported.

## Your Mission

### Phase 1: Assess What Platform Had

Read all efemera code in both repos and produce an assessment document.

**Platform repo** (`C:\Users\davee\OneDrive\Documents\GitHub\platform`):
- `platform/efemera/src/efemera/channels/` — models, routes, public_routes, system_channels
- `platform/efemera/src/efemera/messages/` — models, routes (versioning, threading, moderation)
- `platform/efemera/src/efemera/ws.py` — WebSocket connection manager
- `platform/efemera/src/efemera/auth/roles.py` — RBAC system

**ShiftCenter repo** (current):
- `hivenode/efemera/store.py` — SQLite store (224 lines)
- `hivenode/efemera/routes.py` — REST API (169 lines)
- `browser/src/services/efemera/relayPoller.ts` — polling service (97 lines)
- `browser/src/primitives/tree-browser/adapters/channelsAdapter.ts` — channels adapter (132 lines)
- `browser/src/primitives/tree-browser/adapters/membersAdapter.ts` — members adapter (113 lines)
- `browser/src/primitives/terminal/useTerminal.ts` — relay mode section (~lines 182-535)
- `browser/src/primitives/text-pane/SDEditor.tsx` — efemera bus subscriptions (~lines 293-410)

Write the assessment to: `.deia/hive/responses/20260328-EFEMERA-ASSESSMENT.md`

### Phase 2: Design the Efemera Connector

Design a modular connector architecture. The connector is a **browser-side service** that:

1. **Owns all HTTP communication** with hivenode efemera endpoints
2. **Owns the message polling loop** (absorbs relayPoller.ts)
3. **Owns presence management** (heartbeats, idle detection)
4. **Coordinates all panes via bus events only** — primitives never call HTTP endpoints directly

#### Proposed Module Structure

```
browser/src/services/efemera/
├── EfemeraConnector.ts      — Main orchestrator, lifecycle management
├── channelService.ts        — Channel CRUD, channel list caching
├── messageService.ts        — Message send/receive, polling, history loading
├── presenceService.ts       — Presence heartbeat, idle detection, status updates
├── memberService.ts         — Member list, role management
├── types.ts                 — Shared types (Channel, Message, Member, Presence)
└── __tests__/
    ├── EfemeraConnector.test.ts
    ├── channelService.test.ts
    ├── messageService.test.ts
    ├── presenceService.test.ts
    └── memberService.test.ts
```

#### Bus Event Contract

The connector is the single source of truth for efemera state. Primitives interact ONLY through bus events:

**Connector listens for (from primitives):**
- `efemera:channel-select` — user clicked a channel in sidebar
- `efemera:message-send` — user typed a message in compose bar
- `efemera:channel-create` — user wants to create a channel
- `efemera:presence-update` — user status changed (idle, active, offline)

**Connector emits (to primitives):**
- `efemera:channels-loaded` — channel list ready (for sidebar)
- `efemera:channel-changed` — active channel changed (for all panes)
- `efemera:messages-loaded` — message history for a channel (for chat window)
- `efemera:message-received` — new message arrived (for chat window)
- `efemera:message-sent` — message successfully sent (for compose bar to clear input)
- `efemera:members-loaded` — member list for active channel (for members sidebar)
- `efemera:presence-changed` — someone's presence changed (for members sidebar)
- `efemera:error` — backend error (for any pane to display)

#### Primitive Behavior After Refactor

**Terminal (compose bar):**
- On Enter: emit `efemera:message-send` with `{content, channelId}`
- On `efemera:message-sent`: clear input
- On `efemera:channel-changed`: update prompt label
- On `efemera:error`: show inline error
- **Deletes:** All relay HTTP code, channel:selected subscription, terminal:text-patch emission

**Text-pane (chat window):**
- On `efemera:messages-loaded`: render full message history
- On `efemera:message-received`: append new message
- On `efemera:channel-changed`: clear and show loading state
- **Deletes:** Direct HTTP fetch of messages, channel:selected fetch logic

**Tree-browser (channels sidebar):**
- On `efemera:channels-loaded`: render channel tree
- On click: emit `efemera:channel-select` with `{channelId, channelName}`
- **channelsAdapter refactored:** No longer calls HTTP directly. Receives data from connector via bus or callback.

**Tree-browser (members sidebar):**
- On `efemera:members-loaded`: render member tree
- On `efemera:presence-changed`: update status icons
- **membersAdapter refactored:** No longer calls HTTP directly. Receives data from connector via bus or callback.

### Phase 3: Plan the Port from Platform

Identify what to port from platform/efemera/ and how it maps to the new modular structure:

| Platform Source | Port To | Notes |
|----------------|---------|-------|
| `channels/models.py` | `hivenode/efemera/models.py` | SQLAlchemy models, channel types enum |
| `channels/routes.py` | Keep `hivenode/efemera/routes.py` | Extend with missing endpoints |
| `channels/system_channels.py` | `hivenode/efemera/system_channels.py` | Auto-seed on startup |
| `messages/models.py` | `hivenode/efemera/models.py` | Message model with versioning fields |
| `messages/routes.py` | `hivenode/efemera/message_routes.py` | Split from main routes, add threading |
| `ws.py` | `hivenode/efemera/ws.py` | WebSocket manager (LATER — polling first) |
| `auth/roles.py` | `hivenode/efemera/roles.py` | RBAC for channel permissions |

**Everything gets ported.** No deferred tiers. The Q33N should plan the full build:
- Channel CRUD, system channel types, auto-seeding
- Message send/receive/history, versioning, reply threading
- Member management, RBAC (3 roles, 7 permissions)
- Presence management, typing indicators
- WebSocket manager (replace polling from day one if feasible, or design polling as a fallback mode)
- TASaaS moderation pipeline hooks (block/flag/approve)
- Discord bridge hooks (can be stubbed but architecture must support it)

The task specs should sequence these into a buildable order with dependencies, but nothing is "later."

### Phase 4: Write Task Specs

After assessment and design, write task specs for bees to implement:

1. **TASK: Create efemera connector service** — EfemeraConnector.ts + sub-services, bus event contract, tests
2. **TASK: Refactor terminal relay mode** — Remove all efemera HTTP code from useTerminal.ts, replace with bus events
3. **TASK: Refactor text-pane chat mode** — Remove efemera HTTP code from SDEditor.tsx, replace with bus events
4. **TASK: Refactor tree-browser adapters** — channelsAdapter and membersAdapter receive data from connector, not HTTP
5. **TASK: Port backend models** — Bring over platform message model, channel types, system channels
6. **TASK: Wire connector into EGG lifecycle** — Connector starts when efemera EGG loads, stops on unload

## Deliverables

1. Assessment document: `.deia/hive/responses/20260328-EFEMERA-ASSESSMENT.md`
2. Connector design document: `.deia/hive/responses/20260328-EFEMERA-CONNECTOR-DESIGN.md`
3. Task specs (one per bee task): `.deia/hive/tasks/TASK-EFEMERA-CONNECTOR-*.md`

## Constraints

- **Read BOTH repos** before writing anything
- **Do NOT write implementation code** — design documents and task specs only
- **500-line file limit** applies to all proposed modules
- **TDD** — every task spec must include test requirements
- **Bus events are the API** — no primitive should import from `services/efemera/` directly except the connector bootstrap
- The connector pattern must work for ANY EGG that needs backend services, not just efemera — keep it generalizable

## Read First

1. `.deia/BOOT.md` — hard rules
2. `.deia/HIVE.md` — your workflow
3. All files listed in Phase 1 above
4. `eggs/efemera.egg.md` — current EGG config and permissions block
5. `browser/src/infrastructure/relay_bus/` — understand the bus API (subscribe, send, subscribeType)

## Model Assignment

Opus — this is architecture work requiring cross-repo analysis and design.
