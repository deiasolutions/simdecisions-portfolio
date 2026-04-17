# BRIEFING: SPEC-HIVENODE-E2E-001 Wave 3 — Volume Sync + Chat Persistence

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-12
**Spec:** `docs/specs/SPEC-HIVENODE-E2E-001.md` (Sections 6 + 7)
**Parent:** SPEC-HIVENODE-E2E-001

---

## Context

Wave 1 built the 8os CLI, E2E route tests, and `/shell/exec`. Wave 2 built the browser terminal shell parser, cloud storage adapter (httpx), and token tracking schema migration. The cloud adapter (`hivenode/storage/adapters/cloud.py`) is now fully wired with offline write queueing via `sync_queue.py`.

Wave 3 builds the volume sync engine and rewrites chat persistence to dual-write to `home://` + `cloud://`.

---

## What to Build — 3 Tasks

### TASK-035: Volume Sync Engine

**Spec sections:** 6.1–6.5

Build the bidirectional sync engine for `home://` ↔ `cloud://`. This is backend-only (Python).

**What already exists:**
- `hivenode/storage/adapters/cloud.py` — CloudAdapter with httpx (TASK-030)
- `hivenode/storage/adapters/sync_queue.py` — SyncQueue for offline writes (TASK-030)
- `hivenode/storage/transport.py` — FileTransport with provenance + ledger integration
- `hivenode/storage/provenance.py` — ProvenanceStore with content hash tracking
- `hivenode/ledger/writer.py` — LedgerWriter for event logging

**What to build:**
1. **`hivenode/sync/sync_log.py`** — sync_log.db schema + operations:
   ```sql
   CREATE TABLE sync_log (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       path TEXT NOT NULL,
       content_hash TEXT NOT NULL,
       source_volume TEXT NOT NULL,
       target_volume TEXT NOT NULL,
       status TEXT NOT NULL DEFAULT 'pending',
       queued_at TEXT NOT NULL,
       synced_at TEXT,
       error TEXT
   );
   ```
   - `queue_sync(path, hash, source, target)` — add pending sync entry
   - `mark_synced(id)` — update status + synced_at
   - `mark_conflict(id, error)` — update status to conflict
   - `mark_failed(id, error)` — update status to failed
   - `get_pending()` — all entries with status='pending'
   - `get_conflicts()` — all entries with status='conflict'

2. **`hivenode/sync/engine.py`** — SyncEngine class:
   - `sync(source_volume, target_volume)` — compare content hashes, push/pull
   - For each file: compare content_hash of local vs remote
     - Hashes match → skip (already synced)
     - Local newer → push local to remote
     - Remote newer → pull remote to local
     - Both changed since last sync → CONFLICT
   - Conflict resolution: last-write-wins by timestamp. Both versions preserved:
     - Winner overwrites file at original path
     - Loser saved as `{filename}.conflict.{timestamp}.{ext}`
   - Log all operations to Event Ledger: SYNC_STARTED, SYNC_COMPLETED, SYNC_CONFLICT, SYNC_QUEUED, SYNC_FLUSHED

3. **`hivenode/sync/ignore.py`** — sync ignore patterns:
   - Read `~/.shiftcenter/sync_ignore` (gitignore syntax)
   - Always skip: `.git/`, `node_modules/`, `__pycache__/`
   - `should_sync(path) -> bool`

4. **`hivenode/routes/sync_routes.py`** — HTTP routes:
   - `POST /sync/trigger` — trigger a sync cycle
   - `GET /sync/status` — last sync time, pending count, conflict count
   - `GET /sync/conflicts` — list all conflicts
   - `POST /sync/resolve` — resolve a conflict (pick winner)

**Model:** Sonnet
**Tests:** ~15 (sync_log CRUD, engine push/pull/conflict, ignore patterns, routes)
**Test file:** `tests/hivenode/sync/test_sync_engine.py`

---

### TASK-036: Chat Persistence Rewrite

**Spec sections:** 7.1–7.3

Rewrite chat persistence to use markdown format and dual-write to `home://` + `cloud://`. Changes both browser (TypeScript) and backend (Python).

**What already exists:**
- `browser/src/services/terminal/chatApi.ts` (221 lines) — stores conversations as JSON to `home://chat/` via hivenode, localStorage fallback
- `browser/src/services/terminal/types.ts` — Conversation, Message types
- `browser/src/primitives/tree-browser/adapters/chatHistoryAdapter.ts` — loads conversations, groups by date

**What to change:**

1. **`browser/src/services/terminal/chatApi.ts`** — rewrite storage format + dual-write:
   - Change storage format from JSON to markdown (see Section 7.2):
     ```markdown
     ---
     id: conversation-<uuid>
     title: "Chat about authentication"
     created: 2026-03-12T09:30:00Z
     updated: 2026-03-12T10:15:00Z
     model: claude-sonnet-4-6
     volume: home://
     ---

     ## You (09:30)
     How does the JWT validation work?

     ## Claude Sonnet 4.6 (09:30)
     The JWT validation flow works like this...
     ```
   - File paths: `{volume}://chats/{date}/conversation-{uuid}.md`
   - Index file: `{volume}://chats/index.json` (lightweight: id, title, date, path, resume_code)
   - Dual-write: write to BOTH `home://` and `cloud://` simultaneously (Promise.all)
   - If either write fails, the successful one is source of truth
   - Add volume choice per conversation: `home-only`, `cloud-only`, `both` (default: `both`)

2. **`browser/src/services/terminal/chatMarkdown.ts`** (new) — markdown serializer/parser:
   - `serializeConversation(conversation: ConversationWithMessages): string` — to markdown
   - `parseConversation(markdown: string): ConversationWithMessages` — from markdown
   - Handle frontmatter (YAML between `---` fences)
   - Handle message blocks (`## Role (timestamp)`)

3. **`browser/src/services/terminal/types.ts`** — update types:
   - Add `volume_preference: 'home-only' | 'cloud-only' | 'both'` to Conversation
   - Add `volume: string` to Conversation (where it's stored)

4. **`browser/src/primitives/tree-browser/adapters/chatHistoryAdapter.ts`** — update to handle markdown format + show volume info

**Model:** Sonnet
**Tests:** ~12 (markdown serialize/parse, dual-write success/partial-failure, volume choice, chatHistoryAdapter with markdown)
**Test file:** `browser/src/services/terminal/__tests__/chatMarkdown.test.ts`

---

### TASK-037: Sync CLI + Periodic Worker

**Spec sections:** 6.4, 2.1 (sync commands)

Wire the sync engine to CLI commands and periodic triggers. Backend-only (Python).

**What already exists:**
- `hivenode/cli.py` — 8os CLI with up/down/status commands (TASK-026)
- TASK-035's SyncEngine (this task depends on TASK-035)

**What to build:**

1. **Update `hivenode/cli.py`** — add sync commands:
   - `8os sync` — trigger immediate sync cycle (call SyncEngine.sync())
   - `8os sync --status` — show last sync time, pending count, conflicts

2. **`hivenode/sync/worker.py`** — periodic sync worker:
   - Background task that runs sync on interval (default 300s from config)
   - Starts automatically with `8os up` if `sync.enabled: true` in config
   - Also flushes SyncQueue on each cycle
   - Logs sync events to ledger

3. **`hivenode/sync/watcher.py`** — file watcher for on-write sync:
   - Uses `watchdog` library to monitor volume paths
   - On file write: queue sync entry in sync_log
   - Respects sync_ignore patterns
   - Only runs if `sync.on_write: true` in config

4. **Startup sync** — in `hivenode/main.py` lifespan:
   - On hivenode startup: pull changes from cloud since last sync timestamp
   - Flush any pending SyncQueue entries

**Model:** Sonnet
**Tests:** ~10 (CLI commands, periodic worker scheduling, file watcher events, startup sync)
**Test file:** `tests/hivenode/sync/test_sync_worker.py`

---

## Dependencies Between Tasks

```
TASK-035 (sync engine) ──┬──→ TASK-037 (sync CLI + worker)
                         │
TASK-036 (chat rewrite)  │  (independent — dual-write doesn't need sync engine)
```

- TASK-035 and TASK-036 are **independent** — dispatch in parallel
- TASK-037 **depends on TASK-035** — dispatch after TASK-035 completes

**Recommendation:** Dispatch TASK-035 + TASK-036 in parallel. After TASK-035 completes, dispatch TASK-037.

---

## Files to Read (for Q33N task file writing)

**Sync infrastructure:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\cloud.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\adapters\sync_queue.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\transport.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\provenance.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\resolver.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\registry.py`

**Chat persistence:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatApi.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts`

**CLI and config:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\cli.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py`

**Ledger (for event logging):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\writer.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\schema.py`

**Existing tests:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\storage\test_cloud_adapter.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\__tests__\chatApi.test.ts`

---

## Constraints

- No file over 500 lines
- TDD — tests first
- No stubs
- Backward compatibility: existing chatApi consumers must still work during transition
- Sync must be idempotent (running twice with no changes = no-op)
- Conflict resolution must preserve both versions (never lose data)

---

**End of Wave 3 briefing.**
