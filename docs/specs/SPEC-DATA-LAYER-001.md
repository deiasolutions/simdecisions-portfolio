# SPEC-DATA-LAYER-001: SQLite Databases + File Indexing Pipeline

**Date:** 2026-03-12
**Author:** Q88N (Dave) × Q33NR
**Status:** Reference — living document
**Audience:** Mr. AI, Q33N, bees

---

## 1. Purpose

This document describes every SQLite database in the ShiftCenter system, their schemas, and the complete file indexing pipeline. It exists so that any LLM or human working on the codebase understands how data is stored, searched, and tracked — without having to read 2,000 lines of Python.

**Architectural principle:** SQLite for local/edge, PostgreSQL for cloud. The local hivenode uses SQLite everywhere. The Railway-hosted cloud hivenode uses PostgreSQL for the node store and ledger, but the schemas are identical.

---

## 2. Database Inventory

| DB | Location | Tables | Created By |
|----|----------|--------|-----------|
| `ledger.db` | `~/.shiftcenter/` | `events` | `hivenode/ledger/schema.py` |
| `provenance.db` | `~/.shiftcenter/` | `provenance` | `hivenode/storage/provenance.py` |
| `chunks.db` | `.deia/index/` | `chunks` | `_tools/build_index.py` |
| `feature-inventory.db` | `docs/` (gitignored) | `features`, `backlog`, `bugs` | `_tools/inventory.py` |
| `nodes.db` | Cloud hivenode only | `nodes` | `hivenode/node_store.py` |
| `byok.db` | Hivenode internal | `byok_keys` | `hivenode/llm/byok.py` |
| `sync_log.db` | `~/.shiftcenter/` | `sync_log` | Upcoming (SPEC-HIVENODE-E2E-001 Wave 3) |

---

## 3. Event Ledger — `ledger.db`

The append-only audit trail. Every significant operation in the system logs here. WAL mode enabled for concurrent reads.

```sql
CREATE TABLE events (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp           TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f','now')),
    event_type          TEXT NOT NULL,       -- LLM_CALL, SHELL_EXEC, VOLUME_WRITE, etc.
    actor               TEXT NOT NULL,       -- user:dave, system:hivenode, bot:sonnet
    target              TEXT,                -- task ID, file path, etc.
    domain              TEXT,                -- llm, storage, shell, sync, node
    signal_type         TEXT CHECK(signal_type IN ('gravity','light','internal')),
    oracle_tier         INTEGER CHECK(oracle_tier BETWEEN 0 AND 4),
    random_seed         INTEGER,
    completion_promise  TEXT,
    verification_method TEXT,
    payload_json        TEXT,                -- JSON blob with event-specific data
    cost_tokens         INTEGER,             -- total tokens (input + output)
    cost_usd            REAL,                -- USD cost
    cost_carbon         REAL                 -- kg CO2e
);

CREATE INDEX idx_event_type ON events(event_type);
CREATE INDEX idx_actor ON events(actor);
CREATE INDEX idx_domain ON events(domain);
CREATE INDEX idx_timestamp ON events(timestamp);
CREATE INDEX idx_signal_type ON events(signal_type);
CREATE INDEX idx_oracle_tier ON events(oracle_tier);
```

**Pending migration (SPEC-HIVENODE-E2E-001 Section 10.1):**
```sql
ALTER TABLE events ADD COLUMN cost_tokens_up INTEGER;    -- input/prompt tokens
ALTER TABLE events ADD COLUMN cost_tokens_down INTEGER;  -- output/completion tokens
```

**Key event types:** `LLM_CALL`, `SHELL_EXEC`, `SHELL_DENIED`, `VOLUME_READ`, `VOLUME_WRITE`, `VOLUME_DELETE`, `SYNC_STARTED`, `SYNC_COMPLETED`, `SYNC_CONFLICT`, `NODE_ANNOUNCED`, `NODE_HEARTBEAT`, `NODE_OFFLINE`

**Writer:** `hivenode/ledger/writer.py` — `write_event()` inserts a row and returns the event ID.
**Reader:** `hivenode/ledger/reader.py` — queries with filters (event_type, actor, domain, time range, pagination).
**Aggregation:** `hivenode/ledger/aggregation.py` — `get_total_cost()`, `aggregate_cost_by_actor()`, `aggregate_cost_by_task()`, `aggregate_cost_by_domain()`.
**Routes:** `GET /ledger/events`, `GET /ledger/events/{id}`, `POST /ledger/query`, `GET /ledger/cost`

---

## 4. File Provenance — `provenance.db`

Tracks the full lineage of every file operation through the volume system. Every write records who did it, why, and the content hash before and after.

```sql
CREATE TABLE provenance (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp       TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f','now')),
    volume          TEXT NOT NULL,       -- home://, cloud://, work://
    path            TEXT NOT NULL,       -- relative path within volume
    operation       TEXT NOT NULL CHECK(operation IN ('write','move','copy','delete')),
    content_hash    TEXT,                -- SHA-256 of content after operation
    parent_hash     TEXT,                -- SHA-256 of content before operation
    actor           TEXT NOT NULL,       -- who initiated the operation
    intent          TEXT NOT NULL,       -- why (human-readable reason)
    source_volume   TEXT,                -- for move/copy: source volume
    source_path     TEXT,                -- for move/copy: source path
    payload_json    TEXT                 -- additional metadata
);
```

**Writer:** `hivenode/storage/provenance.py` — called by `FileTransport` on every storage operation.
**Query:** No dedicated reader yet. Queryable via direct SQL or future provenance route.

---

## 5. Semantic Search Index — `chunks.db`

### 5.1 Schema

```sql
CREATE TABLE chunks (
    id          INTEGER PRIMARY KEY,
    file_path   TEXT,            -- absolute path to source file
    chunk_type  TEXT,            -- function | class | section | node | stylesheet | metadata
    name        TEXT,            -- function/class/section name
    start_line  INTEGER,         -- first line in source file
    end_line    INTEGER,         -- last line in source file
    content     TEXT,            -- raw text content of the chunk
    embedding   BLOB,            -- pickled numpy array (384-dim float32)
    mtime       REAL             -- file modification time (for incremental updates)
);
```

**Companion file:** `.deia/index/vectors.faiss` (FAISS index for fast similarity search) or `.deia/index/vectors.npy` (numpy fallback if FAISS not installed).

### 5.2 The Indexing Pipeline

Three tools, one pipeline:

| Tool | Purpose | When to use |
|------|---------|-------------|
| `_tools/build_index.py` | Build or rebuild the full index | First time, or `--full` to force rebuild |
| `_tools/query_index.py` | Search the index by natural language | `python _tools/query_index.py "how does auth work"` |
| `_tools/index_watcher.py` | Real-time incremental updates | Run as a daemon while developing |

**CLI shortcut:** `8os index` runs `build_index.py` (incremental by default).

### 5.3 How Build Works

`_tools/build_index.py` does this:

**Step 1 — Walk the repo.** Starting from the repo root, walk every directory. Skip: `__pycache__`, `.git`, `venv`, `node_modules`, `.next`, `dist`, `build`, `.deia/hive/responses`, `.deia/hive/tasks/_archive`.

**Step 2 — Filter by extension.** Only process: `.py`, `.md`, `.ts`, `.tsx`, `.css`, `.ir.json`. Everything else is ignored.

**Step 3 — Chunk by structure.** Each file type gets its own chunking strategy:

| File type | Chunking strategy | Chunk types |
|-----------|------------------|-------------|
| `.py` | Python AST (`ast.parse`) | `function`, `class` — one chunk per function/class definition |
| `.ts`, `.tsx` | Regex matching | `function`, `class` — matches `export function`, `const x = (`, `class X` |
| `.md` | Heading-based splits | `section` — one chunk per `#` heading block |
| `.css` | Whole file | `stylesheet` — entire file as one chunk |
| `.ir.json` | JSON structure | `metadata` (file-level) + `node` (one per node in the `nodes` array) |

Each chunk records: file path, chunk type, name, start line, end line, raw content, and the file's mtime.

**Step 4 — Embed.** All chunks are embedded using `sentence-transformers` model `all-MiniLM-L6-v2`. This produces a 384-dimensional float32 vector per chunk. Batch size: 32. The model is ~80MB and loads once.

**Step 5 — Store.** Two storage targets:
- **SQLite** (`chunks.db`): Every chunk's metadata + content + pickled embedding blob.
- **FAISS index** (`vectors.faiss`): All embeddings in a flat inner-product index (`IndexFlatIP`). Embeddings are L2-normalized so inner product = cosine similarity. Falls back to `vectors.npy` (raw numpy array) if FAISS isn't installed.

**Incremental mode (default):** For each file on disk, compare its `mtime` to what's stored in the DB. If unchanged, skip. If modified, delete old chunks for that file and re-chunk/re-embed. If a file in the DB no longer exists on disk, its chunks are deleted. After processing changes, the FAISS index is rebuilt from all embeddings in the DB.

**Full rebuild (`--full`):** Deletes the entire DB, re-walks, re-chunks, re-embeds everything.

### 5.4 How Query Works

`_tools/query_index.py "your search query" --top 5`:

1. Load the same `all-MiniLM-L6-v2` model.
2. Encode the query string into a 384-dim vector.
3. L2-normalize the query vector.
4. Search the FAISS index (or numpy fallback) for top-k nearest neighbors by cosine similarity.
5. Map result indices back to chunk IDs in SQLite.
6. Return: file path, line range, chunk type, name, content preview, similarity score.

**Optional flags:**
- `--rebuild`: Run incremental build before querying.
- `--full-rebuild`: Run full build before querying.
- `--top N`: Number of results (default: 5).

### 5.5 How the Watcher Works

`_tools/index_watcher.py` provides real-time index updates:

1. **Startup:** Load the embedding model into memory (stays resident). Start a `watchdog` `Observer` monitoring the repo root recursively.
2. **On file event** (create/modify/delete/move): Add to pending changes queue. Same skip rules as build — ignores `__pycache__`, `.git`, `node_modules`, non-tracked extensions.
3. **Debounce:** Wait 2 seconds after the last change before processing. This batches rapid saves (e.g., IDE auto-save, git checkout).
4. **Process:**
   - **Creates/modifies:** Read file, chunk it, embed chunks, delete old chunks for that file in DB, insert new chunks, rebuild FAISS index.
   - **Deletes:** Remove chunks for that file from DB, rebuild FAISS index.
5. **Output:** Prints `[INDEX] Updated: filename (N chunks)` or `[INDEX] Removed: filename`.

The watcher is designed to run in a terminal alongside development. It keeps the embedding model hot in memory so updates are fast (no model load per change).

### 5.6 Dependencies

| Package | Purpose |
|---------|---------|
| `sentence-transformers` | Embedding model (`all-MiniLM-L6-v2`) |
| `faiss-cpu` | Fast vector similarity search (optional, numpy fallback) |
| `watchdog` | Filesystem monitoring for real-time updates |
| `numpy` | Vector math, embedding storage |

All in `[project.optional-dependencies] index` in pyproject.toml.

---

## 6. Feature Inventory — `feature-inventory.db`

Tracks everything built, every known bug, and every backlog item. Three tables. CLI-driven — never edit the export markdown directly.

```sql
CREATE TABLE features (
    id              TEXT PRIMARY KEY,     -- LEDGER-001, SHELL-EXEC-001, CLI-001
    title           TEXT NOT NULL,
    task_id         TEXT NOT NULL,        -- TASK-022, TASK-028, etc.
    status          TEXT NOT NULL DEFAULT 'BUILT',
    layer           TEXT NOT NULL,        -- ledger, storage, shell, privacy, llm, etc.
    test_count      INTEGER DEFAULT 0,
    test_files      TEXT,                 -- comma-separated test file paths
    source_files    TEXT,                 -- comma-separated source file paths
    dependencies    TEXT,
    notes           TEXT,
    created_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%S','now')),
    updated_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%S','now')),
    verified_at     TEXT
);
CREATE INDEX idx_status ON features(status);

CREATE TABLE backlog (
    id          TEXT PRIMARY KEY,     -- BL-001, BL-053, etc.
    title       TEXT NOT NULL,
    category    TEXT NOT NULL,        -- enhancement | debt | bug | spec-note | research
    priority    TEXT NOT NULL DEFAULT 'P2',
    source      TEXT,
    notes       TEXT,
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%S','now'))
);
CREATE INDEX idx_bl_category ON backlog(category);
CREATE INDEX idx_bl_priority ON backlog(priority);

CREATE TABLE bugs (
    id          TEXT PRIMARY KEY,     -- BUG-001, BUG-002
    title       TEXT NOT NULL,
    severity    TEXT NOT NULL DEFAULT 'P2',
    component   TEXT NOT NULL,
    description TEXT,
    steps       TEXT,
    source_task TEXT,
    status      TEXT NOT NULL DEFAULT 'OPEN',
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%S','now')),
    resolved_at TEXT,
    resolved_by TEXT
);
CREATE INDEX idx_bug_status ON bugs(status);
CREATE INDEX idx_bug_severity ON bugs(severity);
CREATE INDEX idx_bug_component ON bugs(component);
```

**CLI:** `python _tools/inventory.py` — subcommands: `add`, `stats`, `export-md`, `bug add`, `bug list`, `backlog add`, `backlog list`.
**Export:** `python _tools/inventory.py export-md` generates `docs/FEATURE-INVENTORY.md` from the DB. The .md is checked in; the .db is gitignored.

---

## 7. Node Store — `nodes.db`

Cloud hivenode only. Tracks registered hivenode instances for multi-device support.

```sql
CREATE TABLE nodes (
    node_id         TEXT PRIMARY KEY,    -- node-a1b2c3d4
    user_id         TEXT NOT NULL,       -- ra96it user ID
    mode            TEXT NOT NULL CHECK(mode IN ('local', 'remote')),
    ip              TEXT NOT NULL,
    port            INTEGER NOT NULL,
    volumes         TEXT NOT NULL,       -- JSON array of volume names
    capabilities    TEXT NOT NULL,       -- JSON array: ["storage", "shell", "ledger"]
    announced_at    TEXT NOT NULL,
    last_seen       TEXT NOT NULL,
    online          BOOLEAN DEFAULT TRUE
);
```

**Writer:** `hivenode/node_store.py`
**Routes:** `POST /node/announce`, `GET /node/discover`, `POST /node/heartbeat`
**Offline detection:** If a node misses 5 consecutive heartbeats (5 minutes), it's marked `online = FALSE`.

---

## 8. BYOK Key Store — `byok.db`

Stores Bring Your Own Key API keys, encrypted at rest. One key per user per provider.

```sql
CREATE TABLE byok_keys (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     TEXT NOT NULL,
    provider    TEXT NOT NULL CHECK(provider IN ('anthropic','openai','gemini')),
    encrypted_key TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f','now')),
    last_used   TEXT,
    UNIQUE(user_id, provider)
);
```

**Writer/Reader:** `hivenode/llm/byok.py` — `BYOKStore` class. Encrypts keys using `cryptography.fernet`.
**Used by:** LLM router — checks for user's own key before falling back to server key.

---

## 9. Sync Log — `sync_log.db` (Upcoming)

SPEC-HIVENODE-E2E-001 Wave 3. Tracks volume sync state between `home://` and `cloud://`.

```sql
CREATE TABLE sync_log (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    path            TEXT NOT NULL,
    content_hash    TEXT NOT NULL,
    source_volume   TEXT NOT NULL,      -- home:// or cloud://
    target_volume   TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'pending',  -- pending | synced | conflict | failed
    queued_at       TEXT NOT NULL,
    synced_at       TEXT,
    error           TEXT
);
```

**Conflict resolution:** Last-write-wins by timestamp. Both versions preserved (loser saved as `.conflict.<timestamp>.<ext>`).

---

**End of SPEC-DATA-LAYER-001.**

*daaaave-atx × Claude (Anthropic) · CC BY 4.0*
