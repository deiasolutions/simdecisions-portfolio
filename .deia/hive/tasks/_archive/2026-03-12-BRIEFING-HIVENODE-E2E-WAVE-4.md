# BRIEFING: SPEC-HIVENODE-E2E-001 Wave 4 — Tree-Browser Navigator + Node Announcement

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-12
**Spec:** `docs/specs/SPEC-HIVENODE-E2E-001.md` (Sections 8 + 9 + 2.1 remaining)
**Parent:** SPEC-HIVENODE-E2E-001

---

## Context

Waves 1–3 built the full backend: 8os CLI, shell exec, cloud adapter, sync engine, chat persistence rewrite, sync CLI + worker. Wave 4 is the final wave — wiring the tree-browser conversation navigator and node announcement protocol.

**Key infrastructure already built:**
- Tree-browser primitive: `TreeBrowser.tsx`, `TreeNodeRow.tsx`, `useTreeState.ts` — fully functional with keyboard nav, search, drag/drop
- Chat history adapter: `chatHistoryAdapter.ts` — loads conversations, groups by date
- Filesystem adapter: `filesystemAdapter.ts` — loads repo tree from hivenode
- Chat API: `chatApi.ts` — dual-write `home://` + `cloud://`, markdown format, volume preference
- Relay bus: `messageBus.ts` — publish/subscribe with governance, mute enforcement
- Node store: `node_store.py` — SQLite, announce/heartbeat/discover, offline detection
- Node routes: `routes/node.py` — POST /announce, GET /discover, POST /heartbeat (cloud mode, JWT required)
- Node schemas: `schemas.py` — NodeAnnounceRequest, NodeInfo, NodeDiscoverResponse

---

## What to Build — 3 Tasks

### TASK-038: Tree-Browser Conversation Navigator

**Spec section:** 8.1–8.3

Wire the tree-browser primitive as a conversation navigator pane. When the user clicks a conversation in the tree, load it into the chat terminal. This is browser-only (TypeScript).

**What already exists:**
- `browser/src/primitives/tree-browser/TreeBrowser.tsx` — complete component with `onSelect`, `onExpand`, `onCollapse`, keyboard nav
- `browser/src/primitives/tree-browser/adapters/chatHistoryAdapter.ts` — `loadChatHistory()` returns `TreeNodeData[]` grouped by date
- `browser/src/services/terminal/chatApi.ts` — `listConversations()`, `getConversation(id)`, `createConversation()`, `deleteConversation(id)`
- `browser/src/infrastructure/relay_bus/messageBus.ts` — `send()`, `subscribe()`
- `browser/src/primitives/tree-browser/types.ts` — `TreeBrowserPaneConfig` with adapter type `'chat-history'`

**What to build:**

1. **Conversation selection handler** — When user selects a conversation in the tree:
   - Publish `conversation:selected` message on relay bus with `{ conversationId, path, volume }`
   - The terminal/chat pane subscribes and calls `getConversation(id)` to load messages
   - Display loaded conversation in the terminal output

2. **Tree-browser pane integration** — Wire TreeBrowser component into the pane system:
   - Use the existing `TreeBrowserPaneConfig` with `adapter: 'chat-history'`
   - Call `loadChatHistory()` on mount and on conversation create/delete
   - Refresh tree when conversations change (subscribe to `conversation:created` and `conversation:deleted` bus events)

3. **Volume badges** (Section 8.3) — Show sync status on conversations:
   - Online/synced (green), sync in progress, conflict, pending upload, offline (red)
   - Read volume status from hivenode `/sync/status` route (built in Wave 3)
   - Badge displayed on tree nodes via `TreeNodeData.badge`

4. **Conversation actions** — Right-click or action menu on conversations:
   - New conversation: calls `createConversation()`, refreshes tree, selects new conversation
   - Delete conversation: confirmation, calls `deleteConversation(id)`, refreshes tree
   - Wire through `TreeNodeData.actions[]` + `TreeNodeAction` interface

**Model:** Sonnet
**Tests:** ~12 (selection handler publishes bus event, tree refresh on create/delete, volume badges, conversation actions)
**Test file:** `browser/src/primitives/tree-browser/__tests__/conversationNavigator.test.ts`

---

### TASK-039: Node Announcement Client

**Spec sections:** 9.1–9.3

Build the client-side node announcement flow. The local hivenode announces itself to the cloud hivenode on startup, sends periodic heartbeats, and can discover other nodes. This is backend-only (Python).

**What already exists (cloud side — receiving end):**
- `hivenode/node_store.py` — NodeStore with announce(), heartbeat(), discover()
- `hivenode/routes/node.py` — POST /node/announce, GET /node/discover, POST /node/heartbeat
- `hivenode/schemas.py` — NodeAnnounceRequest, NodeHeartbeatRequest, etc.

**What to build (local hivenode — sending end):**

1. **`hivenode/node/client.py`** — NodeAnnouncementClient:
   - `announce()` — POST to cloud hivenode `/node/announce` with:
     - `node_id` from `~/.shiftcenter/config.yml` (generate if first run)
     - `mode`, `ip` (auto-detect), `port`, `volumes` (from VolumeRegistry), `capabilities`
   - `heartbeat()` — POST to cloud hivenode `/node/heartbeat` with node_id
   - `discover()` — GET from cloud hivenode `/node/discover`, return list of online nodes
   - Uses httpx.AsyncClient with JWT auth header
   - Handles network errors gracefully (log, don't crash)

2. **`hivenode/node/heartbeat.py`** — HeartbeatWorker:
   - Background async task that sends heartbeat every 60 seconds
   - If 404 response (node expired), re-announce automatically
   - Logs to Event Ledger: NODE_ANNOUNCED, NODE_HEARTBEAT, NODE_RECONNECTED
   - Graceful shutdown on hivenode stop

3. **Startup announcement** — in `hivenode/main.py` lifespan:
   - On startup (if mode is local or remote, NOT cloud): create NodeAnnouncementClient, call announce(), start HeartbeatWorker
   - On shutdown: stop HeartbeatWorker

4. **`hivenode/routes/node_local.py`** — Local-mode routes:
   - `GET /node/status` — return this node's info (id, mode, volumes, capabilities, cloud connection status)
   - `GET /node/peers` — call discover() on cloud, return list of peer nodes
   - These routes work in local mode (unlike the cloud-only /node/announce etc.)

**Model:** Sonnet
**Tests:** ~12 (announce with mock cloud, heartbeat cycling, re-announce on 404, discover, startup integration, local routes)
**Test file:** `tests/hivenode/node/test_node_client.py`

---

### TASK-040: 8os Remaining CLI Commands

**Spec section:** 2.1 (remaining commands)

Wire the remaining 8os CLI commands that aren't yet implemented. Backend-only (Python).

**What already exists:**
- `hivenode/cli.py` — `8os up`, `8os down`, `8os status`, `8os sync`, `8os sync --status` (from Waves 1+3)

**What to add:**

1. **`8os queue`** — run the build queue (`run_queue.py`)
   - Calls `run_queue()` from `.deia/hive/scripts/queue/run_queue.py`
   - `8os queue --status` — show queue dir contents and pending count

2. **`8os dispatch TASK.md`** — dispatch a single task
   - Calls `dispatch.py` with the given task file
   - Passthrough args: `--model`, `--role`, `--inject-boot`

3. **`8os index`** — rebuild repo semantic search index
   - Calls `_tools/build_index.py` (incremental by default)
   - `8os index --full` — full rebuild

4. **`8os inventory`** — passthrough to `_tools/inventory.py`
   - `8os inventory stats` — feature/bug/backlog counts
   - `8os inventory add ...` — add feature
   - `8os inventory bug add ...` — add bug

5. **`8os volumes`** — list mounted volumes + online/offline status
   - Read config, check each volume's adapter
   - Show: volume name, type (local/cloud), path, online/offline

6. **`8os node list`** — show connected nodes
   - Call `/node/peers` (local mode) or `/node/discover` (cloud mode)
   - Display table: node_id, mode, os, online, last_seen

7. **`8os node announce`** — force re-announce to cloud
   - Call `/node/announce` or NodeAnnouncementClient.announce()

**Model:** Sonnet
**Tests:** ~10 (each CLI command with mock responses, error handling)
**Test file:** `tests/hivenode/test_cli_commands.py`

---

## Dependencies Between Tasks

```
TASK-038 (tree-browser navigator) — independent
TASK-039 (node announcement client) — independent
TASK-040 (8os CLI remaining) — partially depends on TASK-039 for node commands
```

- TASK-038 and TASK-039 are **independent** — dispatch in parallel
- TASK-040 can also run in parallel (node CLI commands can stub the client if TASK-039 isn't done yet, or use the existing routes)

**Recommendation:** Dispatch all three in parallel.

---

## Files to Read (for Q33N task file writing)

**Tree-browser:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeBrowser.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\filesystemAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\index.ts`

**Relay bus:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\messageBus.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts`

**Chat API:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatApi.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\types.ts`

**Node infrastructure:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\node_store.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\node.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\schemas.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py`

**CLI:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\cli.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py`

**Existing tests:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_cli.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\chatHistoryAdapter.test.ts`

---

## Constraints

- No file over 500 lines
- TDD — tests first
- No stubs
- Relay bus messages must use existing MessageEnvelope format
- Node announcement must not crash if cloud is unreachable (graceful degradation)
- CLI commands must handle "hivenode not running" gracefully

---

**End of Wave 4 briefing.**
