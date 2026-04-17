# COORDINATION: SPEC-HIVENODE-E2E-001 Wave 4 — Tree-Browser Navigator + Node Announcement

**From:** Q33N
**To:** Q88N (Dave)
**Date:** 2026-03-12
**Parent Spec:** SPEC-HIVENODE-E2E-001
**Briefing:** `.deia/hive/coordination/2026-03-12-BRIEFING-HIVENODE-E2E-WAVE-4.md`

---

## Summary

Wave 4 is the final wave of SPEC-HIVENODE-E2E-001. Waves 1–3 built the full backend infrastructure (8os CLI, shell exec, cloud adapter, sync engine, chat persistence, repo indexing). Wave 4 completes the spec by wiring:

1. **Tree-browser conversation navigator** (browser) — Clickable conversation tree that loads chats into terminal
2. **Node announcement client** (backend) — Local nodes announce to cloud, send heartbeats, discover peers
3. **8os remaining CLI commands** (backend) — Queue, dispatch, index, inventory, volumes, node management

All three tasks are **independent** and can be dispatched in parallel.

---

## Tasks Created

### TASK-038: Tree-Browser Conversation Navigator

**File:** `.deia\hive\tasks\TASK-038-tree-browser-conversation-navigator.md`
**Layer:** Browser (TypeScript)
**Model:** Sonnet
**Tests:** ~12

**What it does:**

- Wires TreeBrowser component as conversation navigator pane
- On conversation click → publishes `conversation:selected` bus message
- Terminal subscribes → loads conversation via `getConversation(id)`
- Tree refreshes on `conversation:created` and `conversation:deleted` bus events
- Volume badges show sync status (green/yellow/red) from `/sync/status`
- Conversation actions: New conversation, Delete conversation (with confirmation)

**Files modified:**

- `browser/src/primitives/tree-browser/adapters/chatHistoryAdapter.ts` (add sync badges, actions)
- `browser/src/primitives/tree-browser/ChatNavigatorPane.tsx` (new component)
- `browser/src/infrastructure/relay_bus/types/messages.ts` (add ConversationSelectedData)
- `browser/src/primitives/tree-browser/__tests__/conversationNavigator.test.ts` (new tests)

---

### TASK-039: Node Announcement Client

**File:** `.deia\hive\tasks\TASK-039-node-announcement-client.md`
**Layer:** Backend (Python)
**Model:** Sonnet
**Tests:** ~12

**What it does:**

- `NodeAnnouncementClient` — announces local node to cloud, sends heartbeats, discovers peers
- `HeartbeatWorker` — background task sending heartbeat every 60 seconds
- Auto re-announces if cloud returns 404 (node expired)
- Startup hook in `main.py` lifespan — announces on startup, starts heartbeat worker
- Local-mode routes: `GET /node/status`, `GET /node/peers`
- Event Ledger logs: NODE_ANNOUNCED, NODE_HEARTBEAT, NODE_RECONNECTED
- Graceful degradation — network errors logged, don't crash hivenode

**Files created:**

- `hivenode/node/__init__.py`
- `hivenode/node/client.py` (NodeAnnouncementClient)
- `hivenode/node/heartbeat.py` (HeartbeatWorker)
- `hivenode/routes/node_local.py` (local-mode routes)
- `tests/hivenode/node/test_node_client.py` (test suite)

**Files modified:**

- `hivenode/main.py` (add startup announcement + heartbeat)
- `hivenode/dependencies.py` (add get_node_client())
- `hivenode/schemas.py` (add NodeLocalStatusResponse)

---

### TASK-040: 8os Remaining CLI Commands

**File:** `.deia\hive\tasks\TASK-040-8os-remaining-cli-commands.md`
**Layer:** Backend (Python)
**Model:** Sonnet
**Tests:** ~10

**What it does:**

Adds 7 new CLI commands to `8os`:

1. **`8os queue`** — run build queue (calls `run_queue.py`)
2. **`8os queue --status`** — show pending/archived task counts
3. **`8os dispatch TASK.md`** — dispatch single task (with `--model`, `--role`, `--inject-boot` flags)
4. **`8os index`** — rebuild repo semantic index (incremental)
5. **`8os index --full`** — full rebuild
6. **`8os inventory [args...]`** — passthrough to `_tools/inventory.py`
7. **`8os volumes`** — list mounted volumes with online/offline status
8. **`8os node list`** — show connected nodes from cloud
9. **`8os node announce`** — force re-announce to cloud

**Files modified:**

- `hivenode/cli.py` (add all new commands)
- `hivenode/routes/storage.py` (add GET /storage/volumes)
- `hivenode/routes/node_local.py` (add POST /node/announce)
- `hivenode/schemas.py` (add VolumeInfo, VolumesResponse)

**Files created:**

- `tests/hivenode/test_cli_commands.py` (test suite)

---

## Dependencies Between Tasks

```
TASK-038 (tree-browser navigator) — independent
TASK-039 (node announcement client) — independent
TASK-040 (8os CLI remaining) — partially depends on TASK-039 for node commands
```

**Recommendation:** Dispatch all three in parallel. TASK-040 can stub node commands if TASK-039 isn't done yet, or use existing routes.

---

## Dispatch Strategy

**Parallel dispatch recommended:**

```bash
python .deia/hive/scripts/dispatch.py .deia/hive/tasks/TASK-038-tree-browser-conversation-navigator.md --model sonnet --role bee
python .deia/hive/scripts/dispatch.py .deia/hive/tasks/TASK-039-node-announcement-client.md --model sonnet --role bee
python .deia/hive/scripts/dispatch.py .deia/hive/tasks/TASK-040-8os-remaining-cli-commands.md --model sonnet --role bee
```

Or via queue:

```bash
# Copy all three task files to queue directory (already there)
8os queue
```

---

## Test Strategy

Each task has its own test file:

- TASK-038: `browser/src/primitives/tree-browser/__tests__/conversationNavigator.test.ts` (~12 tests)
- TASK-039: `tests/hivenode/node/test_node_client.py` (~12 tests)
- TASK-040: `tests/hivenode/test_cli_commands.py` (~10 tests)

**Total:** ~34 new tests

**Run after completion:**

```bash
# Browser tests
npm test -- tree-browser

# Backend tests
pytest tests/hivenode/node/
pytest tests/hivenode/test_cli_commands.py
```

---

## Acceptance Criteria (Wave 4 Complete)

### TASK-038 (Tree-Browser Navigator)

- ✅ Clicking conversation publishes `conversation:selected` message
- ✅ Terminal loads conversation on message receipt
- ✅ Tree refreshes on conversation create/delete
- ✅ Volume badges show sync status
- ✅ New/delete conversation actions work

### TASK-039 (Node Announcement)

- ✅ Node announces to cloud on startup
- ✅ Heartbeat worker sends heartbeat every 60 seconds
- ✅ Auto re-announces on 404
- ✅ Local routes return node status and peers
- ✅ Event Ledger logs node events

### TASK-040 (8os CLI)

- ✅ All 7 new commands work
- ✅ Graceful error handling (hivenode not running)
- ✅ Passthrough commands work correctly

### Overall Wave 4

- ✅ All 34 tests pass
- ✅ No console errors or warnings
- ✅ SPEC-HIVENODE-E2E-001 complete (sections 8 + 9 + 2.1)

---

## Notes

- All three tasks follow TDD (tests first)
- No stubs allowed — full implementation required
- Network errors must not crash hivenode (graceful degradation)
- CLI commands handle "hivenode not running" gracefully
- Relay bus messages use existing MessageEnvelope format
- Node announcement is optional (graceful if cloud unreachable)

---

## Next Steps

1. **Review task files** — ensure clarity, completeness
2. **Dispatch in parallel** — all three tasks independent
3. **Monitor progress** — check responses in `.deia/hive/responses/`
4. **Run tests** — after each task completes
5. **Close spec** — when all three tasks complete + tests pass

---

**End of coordination file.**
