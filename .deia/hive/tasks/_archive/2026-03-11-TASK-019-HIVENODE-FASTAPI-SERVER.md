# TASK-019: Hivenode FastAPI Server — Three Modes + Core Routes + Node Discovery

## Objective

Build the hivenode FastAPI server at `hivenode/`. One codebase, three deployment modes: **cloud** (Railway, PostgreSQL, object storage), **local** (Windows/Mac/Linux, SQLite, filesystem), **remote** (edge node, SQLite, filesystem, announces to cloud). Core routes for health, auth verification, ledger queries, storage operations, and node discovery. This is the HTTP surface for every backend service already built (ledger, storage, governance, LLM routing, privacy).

## Context

All the backend modules exist but have no HTTP surface:
- **Ledger** (`hivenode/ledger/`) — Event Ledger with writer, reader, aggregation, export. Complete, 42+ tests.
- **Storage** (`hivenode/storage/`) — Named volumes (home://, local://, cloud://, work://), file transport, provenance. Complete, 40+ tests.
- **Governance** (`hivenode/governance/gate_enforcer/`) — Five-disposition policy engine. Complete.
- **LLM** (`hivenode/llm/`) — Multi-vendor routing, sensitivity gate, BYOK key storage. Complete.
- **Privacy** (`hivenode/privacy/`) — PII redaction, consent, audit trail, training store. Complete.
- **Auth** (`ra96it/`) — Separate FastAPI service with JWT (RS256), MFA, refresh tokens. Complete.

The auth service (`ra96it/`) is a standalone FastAPI app. Hivenode does NOT duplicate auth — it verifies ra96it JWTs using the public key. The ra96it service issues tokens; hivenode validates them.

No sync between nodes in this task. Sync (cloud↔local replication, conflict resolution) is TASK-020+. This task builds the server, the routes, and the node announcement protocol.

### Three Modes

| Mode | Env Var | Database | Storage Backend | Node Role |
|------|---------|----------|-----------------|-----------|
| `cloud` | `HIVENODE_MODE=cloud` | PostgreSQL (Railway) | Railway object storage (cloud://) | Hub. Receives announcements. |
| `local` | `HIVENODE_MODE=local` | SQLite (WAL) | Local filesystem (home://, local://) | Edge. Announces to cloud on startup. |
| `remote` | `HIVENODE_MODE=remote` | SQLite (WAL) | Local filesystem | Edge. Announces to cloud on startup. Same as local but on a different machine (Mac, Linux server, etc.) |

**local** and **remote** are functionally identical — the distinction is semantic (local = same machine as browser, remote = different machine). Both announce to cloud://.

### Startup Flow

1. Read `HIVENODE_MODE` env var (default: `local`)
2. Load config from `hivenode/config/` based on mode
3. Initialize database (SQLite for local/remote, PostgreSQL for cloud)
4. Initialize storage registry with mode-appropriate volumes
5. Initialize ledger writer
6. Start FastAPI server (uvicorn)
7. If local or remote: POST `/node/announce` to cloud URL with node metadata
8. Ready to serve

### Local Startup Commands

```bash
# Option 1: Module mode
python -m hivenode

# Option 2: CLI alias (via pyproject.toml script entry)
hive up

# Option 3: Direct
uvicorn hivenode.main:app --host 0.0.0.0 --port 8420
```

Default port: **8420** (local/remote). Cloud uses Railway's `$PORT`.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\main.py` — FastAPI app pattern (lifespan, routers, health check)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\config.py` — pydantic-settings pattern
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\reader.py` — LedgerReader API
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\writer.py` — LedgerWriter API
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\transport.py` — FileTransport API
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\registry.py` — VolumeRegistry API
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\resolver.py` — PathResolver API
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\services\jwt.py` — JWT verification (import public key pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\pyproject.toml` — existing dependencies

## Route Definitions

### Health & Status

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health` | No | Returns `{"status": "ok", "mode": "local", "version": "0.1.0", "uptime_s": 123}` |
| GET | `/status` | No | Extended status: mode, volumes, ledger event count, node ID |

### Auth Verification

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/auth/verify` | Bearer JWT | Validates ra96it JWT. Returns `{"valid": true, "user_id": "...", "exp": ...}` |
| GET | `/auth/whoami` | Bearer JWT | Returns user claims from JWT |

JWT verification uses ra96it's **public key** (RS256). The public key is loaded from:
- Env var `RA96IT_PUBLIC_KEY` (PEM string)
- Or file path `RA96IT_PUBLIC_KEY_PATH`
- Issuer: `ra96it`, Audience: `shiftcenter`

Do NOT import from `ra96it/` directly — copy the verification logic or use PyJWT with the public key. The two services are independent deployments.

### Ledger Routes

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/ledger/events` | Bearer JWT | Query events. Query params: `event_type`, `actor`, `domain`, `start`, `end`, `limit` (default 100), `offset` |
| GET | `/ledger/events/{id}` | Bearer JWT | Get single event by ID |
| GET | `/ledger/query` | Bearer JWT | Aggregation query. Query params: `group_by` (actor\|task\|domain), `start`, `end` |
| GET | `/ledger/cost` | Bearer JWT | Total cost for current user. Returns `{tokens, usd, carbon}` |

All ledger routes are read-only via HTTP. Writes happen internally (ledger writer is a service dependency, not an HTTP endpoint). The FileTransport and other services write to the ledger as a side effect of operations.

### Storage Routes

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/storage/read` | Bearer JWT | Read file. Query param: `uri` (e.g., `home://docs/readme.md`). Returns file bytes with Content-Type. |
| POST | `/storage/write` | Bearer JWT | Write file. JSON body: `{"uri": "home://docs/readme.md", "content_base64": "..."}`. Returns `{"ok": true, "uri": "..."}`. |
| GET | `/storage/list` | Bearer JWT | List directory. Query param: `uri` (e.g., `home://docs/`). Returns `{"entries": ["file1.txt", "subdir/"]}`. |
| GET | `/storage/stat` | Bearer JWT | File metadata. Query param: `uri`. Returns `{"size": 1234, "modified": "...", "created": "..."}`. |
| DELETE | `/storage/delete` | Bearer JWT | Delete file. Query param: `uri`. Returns `{"ok": true}`. |

Storage routes use the existing `FileTransport` which integrates with the ledger (every write/delete/move emits a ledger event) and provenance store.

**Security:** All storage routes validate the JWT user_id and scope access. A user can only access their own volumes. Volume path validation (no `..`, no absolute paths) is already in `resolver.py`.

### Node Discovery Routes

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/node/announce` | Bearer JWT | Register a node. Body: `{"node_id": "...", "mode": "local", "ip": "...", "port": 8420, "volumes": ["home", "local"], "capabilities": ["ledger", "storage"]}`. Cloud stores this. |
| GET | `/node/discover` | Bearer JWT | List known nodes. Returns `{"nodes": [...]}` with last-seen timestamps. |
| POST | `/node/heartbeat` | Bearer JWT | Update last-seen. Body: `{"node_id": "..."}`. Called every 60s by local/remote nodes. |

**Node ID:** Generated on first startup, stored in `~/.shiftcenter/node_id`. Format: `node-{8-char-hex}` (e.g., `node-a3f7c2e1`).

**Cloud stores announcements** in SQLite (cloud mode) or PostgreSQL. Table:

```sql
CREATE TABLE nodes (
    node_id         TEXT PRIMARY KEY,
    user_id         TEXT NOT NULL,
    mode            TEXT NOT NULL CHECK(mode IN ('local', 'remote')),
    ip              TEXT NOT NULL,
    port            INTEGER NOT NULL,
    volumes         TEXT NOT NULL,      -- JSON array of volume names
    capabilities    TEXT NOT NULL,      -- JSON array of capability strings
    announced_at    TEXT NOT NULL,
    last_seen       TEXT NOT NULL,
    online          BOOLEAN DEFAULT TRUE
);
```

Nodes are marked offline if no heartbeat for 5 minutes. The `/node/discover` endpoint only returns online nodes.

## Component Architecture

```
hivenode/
├── __init__.py                 — Package init (exports version)
├── __main__.py                 — python -m hivenode entry point
├── main.py                     — FastAPI app, lifespan, CORS
├── config.py                   — HivenodeConfig (pydantic-settings), mode detection
├── dependencies.py             — FastAPI dependency injection (db, transport, auth)
├── routes/
│   ├── __init__.py             — Router aggregation
│   ├── health.py               — /health, /status
│   ├── auth.py                 — /auth/verify, /auth/whoami
│   ├── ledger_routes.py        — /ledger/events, /ledger/query, /ledger/cost
│   ├── storage_routes.py       — /storage/read, /storage/write, /storage/list, /storage/stat, /storage/delete
│   └── node.py                 — /node/announce, /node/discover, /node/heartbeat
├── schemas.py                  — Pydantic request/response models for all routes
├── node_identity.py            — Node ID generation + persistence (~/.shiftcenter/node_id)
├── node_announcer.py           — Background task: announce to cloud on startup, heartbeat every 60s
└── node_store.py               — SQLite/PostgreSQL store for node announcements (cloud mode only)
```

## Deliverables

### Source Files (13)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\__init__.py` — Update with version export
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\__main__.py` — Entry point: `python -m hivenode`
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` — FastAPI app with lifespan
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` — HivenodeConfig with mode detection
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py` — FastAPI dependency injection
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\schemas.py` — Pydantic request/response models
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` — Router aggregation
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\health.py` — Health + status routes
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\auth.py` — JWT verification routes
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\ledger_routes.py` — Ledger query routes
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\storage_routes.py` — Storage operation routes
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\node.py` — Node discovery routes
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\node_identity.py` — Node ID generation + persistence
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\node_announcer.py` — Background announcement + heartbeat
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\node_store.py` — Node announcement storage

### Modified Files (1)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\pyproject.toml` — Add `[project.scripts]` entry: `hive = "hivenode.__main__:main"`

### Test Files (7)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_config.py` — 8 tests (mode detection, defaults, env override)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_health.py` — 6 tests (health, status, uptime, mode in response)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_auth_routes.py` — 8 tests (valid JWT, expired JWT, invalid sig, missing header, whoami)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_ledger_routes.py` — 10 tests (query by type/actor/domain/time, pagination, aggregation, cost)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_storage_routes.py` — 10 tests (read, write, list, stat, delete, invalid URI, path traversal rejection)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_node_routes.py` — 8 tests (announce, discover, heartbeat, offline detection, duplicate announce)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_node_identity.py` — 5 tests (generate, persist, reload, format validation)

**Total: 23 deliverables (16 source + 7 test), 55+ tests**

## Test Requirements (~55 tests minimum)

### test_config.py (~8 tests)
- [ ] Default mode is 'local'
- [ ] HIVENODE_MODE=cloud sets cloud mode
- [ ] HIVENODE_MODE=remote sets remote mode
- [ ] Invalid mode raises ValueError
- [ ] Cloud mode requires DATABASE_URL
- [ ] Local mode uses SQLite default path
- [ ] Port defaults to 8420 for local/remote
- [ ] Port reads from $PORT for cloud mode

### test_health.py (~6 tests)
- [ ] /health returns 200 with status ok
- [ ] /health includes mode field
- [ ] /health includes version field
- [ ] /health includes uptime_s field
- [ ] /status returns extended info (volumes, event count)
- [ ] /status includes node_id

### test_auth_routes.py (~8 tests)
- [ ] /auth/verify returns valid=true for good JWT
- [ ] /auth/verify returns 401 for expired JWT
- [ ] /auth/verify returns 401 for invalid signature
- [ ] /auth/verify returns 401 for missing Authorization header
- [ ] /auth/verify returns 401 for malformed Bearer token
- [ ] /auth/whoami returns user claims
- [ ] /auth/whoami returns user_id from JWT
- [ ] JWT issuer must be 'ra96it'

### test_ledger_routes.py (~10 tests)
- [ ] /ledger/events returns empty list when no events
- [ ] /ledger/events returns events filtered by event_type
- [ ] /ledger/events returns events filtered by actor
- [ ] /ledger/events returns events filtered by time range
- [ ] /ledger/events respects limit and offset
- [ ] /ledger/events/{id} returns single event
- [ ] /ledger/events/{id} returns 404 for missing event
- [ ] /ledger/query returns aggregation by actor
- [ ] /ledger/query returns aggregation by domain
- [ ] /ledger/cost returns total cost for user

### test_storage_routes.py (~10 tests)
- [ ] /storage/write creates file and returns ok
- [ ] /storage/read returns file content
- [ ] /storage/read returns 404 for missing file
- [ ] /storage/list returns directory entries
- [ ] /storage/stat returns file metadata
- [ ] /storage/delete removes file
- [ ] /storage/delete returns 404 for missing file
- [ ] /storage/write rejects path traversal (.. in URI)
- [ ] /storage/read rejects invalid volume name
- [ ] All storage routes require auth

### test_node_routes.py (~8 tests)
- [ ] /node/announce stores node metadata
- [ ] /node/announce updates existing node (re-announce)
- [ ] /node/discover returns announced nodes
- [ ] /node/discover excludes offline nodes
- [ ] /node/heartbeat updates last_seen
- [ ] /node/heartbeat returns 404 for unknown node
- [ ] Node marked offline after 5 min without heartbeat
- [ ] /node/discover requires auth

### test_node_identity.py (~5 tests)
- [ ] Generates node ID on first call
- [ ] Node ID format matches node-{8hex}
- [ ] Persists node ID to file
- [ ] Reloads same ID on subsequent calls
- [ ] Creates ~/.shiftcenter/ directory if missing

## Constraints

- Python 3.12+
- FastAPI + uvicorn (already in pyproject.toml)
- SQLite for local/remote mode, PostgreSQL for cloud (use SQLAlchemy async engine)
- No file over 500 lines
- TDD: Tests first
- No stubs — every route fully implemented
- All timestamps ISO 8601 UTC
- JWT verification via PyJWT with RS256 public key (do NOT import ra96it modules)
- Use existing ledger/storage/governance modules — do NOT rewrite them
- CORS: Allow localhost:5173 (Vite dev) and *.shiftcenter.app (production)
- Do NOT build sync (no replication, no conflict resolution — that's TASK-020+)
- Do NOT build LLM proxy routes (that's a separate task)
- Use httpx AsyncClient for tests (same pattern as ra96it tests)

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-019-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** -- task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** -- every file created/modified/deleted, full paths
3. **What Was Done** -- bullet list of concrete changes
4. **Test Results** -- test files run, pass/fail counts
5. **Build Verification** -- pytest output summary
6. **Acceptance Criteria** -- copy deliverables above, mark [x] or [ ]
7. **Clock / Cost / Carbon** -- all three, never omit any
8. **Issues / Follow-ups** -- edge cases, dependencies, recommended next tasks

DO NOT skip any section. A response without all 8 sections is incomplete.
