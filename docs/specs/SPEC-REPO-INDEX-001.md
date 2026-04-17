# SPEC-REPO-INDEX-001: Repo File Index Service

**Status:** DRAFT
**Date:** 2026-03-12
**Author:** Q88N (Dave) + Q33NR
**Layer:** hivenode (backend), browser (frontend consumer)

---

## 1. Purpose

Give the web application read-only awareness of every file in the repository. A SQLite database indexes the repo tree — path, size, modified time, content hash, extension, gitignore status, and a user-controlled visibility flag. New `/repo/*` routes on the existing hivenode let the frontend browse the index, toggle visibility, and fetch file contents on demand.

The web app gets a file system it can query, filter, and feed to LLM context — without needing its own filesystem access.

## 2. Architecture

```
  ┌─────────────────────────────────────────────────┐
  │  Browser (Vite :5173)                           │
  │                                                 │
  │  repo index UI ──► GET /repo/index              │
  │  file viewer   ──► GET /repo/read?path=...      │
  │  tree view     ──► GET /repo/tree               │
  │  context feed  ──► GET /repo/read (bulk)        │
  │  visibility    ──► PATCH /repo/visibility       │
  │  refresh       ──► POST /repo/scan              │
  └────────────────────────┬────────────────────────┘
                           │ HTTP (localhost)
  ┌────────────────────────▼────────────────────────┐
  │  Hivenode (FastAPI :8420)                       │
  │                                                 │
  │  /repo/* routes ──► RepoIndexer                 │
  │                      │                          │
  │                      ├─ SQLite: repo-index.db   │
  │                      ├─ pathspec: .gitignore     │
  │                      └─ os.walk: repo root      │
  └─────────────────────────────────────────────────┘
```

## 3. SQLite Schema

**Database location:** `~/.shiftcenter/repo-index.db` (follows ledger.db pattern, gitignored by nature)

```sql
CREATE TABLE files (
    path        TEXT PRIMARY KEY,   -- relative to repo root, forward slashes
    is_dir      BOOLEAN NOT NULL,
    size        INTEGER NOT NULL DEFAULT 0,
    modified    REAL NOT NULL,      -- Unix timestamp
    content_hash TEXT,              -- SHA-256 hex, NULL for directories
    extension   TEXT,               -- lowercase, e.g. '.py', '.ts', NULL for dirs
    gitignored  BOOLEAN NOT NULL DEFAULT 0,
    visible     BOOLEAN NOT NULL DEFAULT 1
);

CREATE INDEX idx_files_visible ON files(visible);
CREATE INDEX idx_files_gitignored ON files(gitignored);
CREATE INDEX idx_files_extension ON files(extension);
CREATE INDEX idx_files_parent ON files(path);  -- prefix queries for tree
```

**Scan metadata table** (tracks when last scan happened):

```sql
CREATE TABLE scan_meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
-- Keys: 'last_scan_time', 'last_scan_file_count', 'repo_root'
```

## 4. Gitignore Awareness

### 4.1 Library

Add `pathspec` to `[project.dependencies]` in `pyproject.toml`. This is the standard Python library for parsing `.gitignore`-style patterns.

### 4.2 Behavior

On scan, the indexer:

1. Reads `.gitignore` at repo root (and any nested `.gitignore` files)
2. Compiles rules into a `pathspec.PathSpec` matcher
3. For each file, sets `gitignored = True` if the path matches
4. Always hard-skips `.git/` directory (never indexed, never served)

### 4.3 Hardcoded Exclusions (never indexed)

These are skipped during scan regardless of `.gitignore`:

- `.git/` — git internals
- `node_modules/` — too large, already gitignored
- `__pycache__/` — Python bytecode
- `.venv/`, `venv/` — Python virtual environments

## 5. Visibility Model

Every file has two independent boolean flags:

| Flag | Source | Default | Meaning |
|------|--------|---------|---------|
| `gitignored` | Computed from `.gitignore` rules on scan | varies | Would GitHub exclude this file? |
| `visible` | User-controlled via PATCH endpoint | `true` | User wants to see this in default view? |

### 5.1 View Modes

The frontend requests a view mode via query parameters:

| Mode | Query Params | What Shows |
|------|-------------|------------|
| **GitHub view** (default) | `(none)` | `visible=1 AND gitignored=0` |
| **All visible** | `?gitignored=include` | `visible=1` (regardless of gitignore) |
| **Everything** | `?show_all=true` | All files, hidden and gitignored included |
| **Hidden only** | `?hidden_only=true` | `visible=0` only |

### 5.2 Visibility Toggle

`PATCH /repo/visibility` accepts a path and a boolean. If the path is a directory, all descendants are updated (recursive toggle).

```json
{
    "path": ".deia/hive/responses/",
    "visible": false
}
```

This hides the entire responses directory from default view. You can still see it with `?show_all=true`.

## 6. API Routes

All routes mounted at `/repo` prefix. Auth: `verify_jwt_or_local` (local mode bypasses JWT).

### 6.1 POST /repo/scan

Full repo re-scan. Walks the file tree, computes hashes, parses gitignore rules, upserts every entry. Preserves user-set `visible` flags from previous scan.

**Request:** empty body
**Response:**
```json
{
    "ok": true,
    "file_count": 1842,
    "dir_count": 203,
    "duration_ms": 1250,
    "gitignored_count": 487
}
```

**Behavior:**
- Deletes rows for files that no longer exist on disk
- Upserts rows for new/changed files (by modified time or hash)
- Preserves `visible` flag for existing paths
- New files default to `visible=true`

### 6.2 GET /repo/index

Query the file index with filters. Returns metadata only (no file contents).

**Query params:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `path` | string | `""` | Filter to files under this prefix |
| `ext` | string | — | Filter by extension (e.g. `.py`, `.ts`) |
| `gitignored` | string | `exclude` | `exclude` (default), `include`, `only` |
| `show_all` | bool | `false` | Override visibility, show everything |
| `hidden_only` | bool | `false` | Only show hidden files |
| `search` | string | — | Substring match on path |
| `limit` | int | `500` | Max results |
| `offset` | int | `0` | Pagination offset |

**Response:**
```json
{
    "files": [
        {
            "path": "hivenode/routes/storage_routes.py",
            "is_dir": false,
            "size": 4102,
            "modified": 1741792800.0,
            "content_hash": "a1b2c3...",
            "extension": ".py",
            "gitignored": false,
            "visible": true
        }
    ],
    "total": 1355,
    "limit": 500,
    "offset": 0
}
```

### 6.3 GET /repo/tree

Directory tree structure. Returns nested JSON representing the folder hierarchy.

**Query params:** same filter params as `/repo/index`

**Response:**
```json
{
    "name": "",
    "path": "",
    "children": [
        {
            "name": "hivenode",
            "path": "hivenode/",
            "is_dir": true,
            "children": [
                {
                    "name": "routes",
                    "path": "hivenode/routes/",
                    "is_dir": true,
                    "children": [
                        {
                            "name": "storage_routes.py",
                            "path": "hivenode/routes/storage_routes.py",
                            "is_dir": false,
                            "size": 4102,
                            "extension": ".py"
                        }
                    ]
                }
            ]
        }
    ]
}
```

### 6.4 GET /repo/read

Read a single file's contents from disk (not from DB — always fresh from disk).

**Query params:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `path` | string | yes | Relative file path |
| `encoding` | string | `auto` | `auto`, `utf-8`, `base64` |

**Response (text files):**
```json
{
    "path": "hivenode/main.py",
    "content": "from fastapi import FastAPI\n...",
    "encoding": "utf-8",
    "size": 2048
}
```

**Response (binary files or `encoding=base64`):**
```json
{
    "path": "browser/public/favicon.ico",
    "content": "AAABAAEAEBAAAAEAIABo...",
    "encoding": "base64",
    "size": 15086
}
```

**Auto-detection:** Files with extensions in a known text set (`.py`, `.ts`, `.tsx`, `.js`, `.jsx`, `.md`, `.json`, `.yml`, `.yaml`, `.toml`, `.css`, `.html`, `.sql`, `.sh`, `.bat`, `.txt`, `.cfg`, `.ini`, `.env`, `.egg.md`) are served as UTF-8. Everything else as base64.

**Security:**
- Path traversal blocked (`..` rejected, must be relative)
- `.git/` contents never served
- No write capability through this endpoint

### 6.5 PATCH /repo/visibility

Toggle visibility for a file or directory (recursive for directories).

**Request:**
```json
{
    "path": ".deia/hive/responses/",
    "visible": false
}
```

**Response:**
```json
{
    "ok": true,
    "affected": 47
}
```

### 6.6 GET /repo/stats

Summary statistics about the indexed repo.

**Response:**
```json
{
    "total_files": 1842,
    "total_dirs": 203,
    "visible_files": 1355,
    "gitignored_files": 487,
    "hidden_files": 12,
    "last_scan_time": "2026-03-12T16:45:00Z",
    "extensions": {
        ".py": 245,
        ".ts": 312,
        ".tsx": 189,
        ".md": 67,
        ".json": 43
    },
    "total_size_bytes": 12485632
}
```

## 7. RepoIndexer Module

**File:** `hivenode/repo/indexer.py`

Core class that owns the SQLite DB and scan logic.

```python
class RepoIndexer:
    def __init__(self, repo_root: Path, db_path: Path):
        """
        repo_root: absolute path to the git repo root
        db_path: where to store repo-index.db
        """

    async def scan(self) -> ScanResult:
        """Full re-scan of repo tree."""

    async def query(self, filters: IndexQuery) -> IndexResult:
        """Query the file index with filters."""

    async def tree(self, filters: IndexQuery) -> TreeNode:
        """Build directory tree from index."""

    async def read_file(self, path: str) -> FileContent:
        """Read a file from disk (not from DB)."""

    async def set_visibility(self, path: str, visible: bool) -> int:
        """Set visibility flag. Returns affected row count."""

    async def stats(self) -> RepoStats:
        """Summary statistics."""
```

### 7.1 File Layout

```
hivenode/repo/
├── __init__.py
├── indexer.py        -- RepoIndexer class, scan logic, DB operations
├── gitignore.py      -- .gitignore parser using pathspec
├── schemas.py        -- Pydantic models (ScanResult, IndexQuery, etc.)
└── routes.py         -- FastAPI router (/repo/* endpoints)
```

### 7.2 Initialization

The `RepoIndexer` is created during hivenode startup (in `main.py` lifespan), stored in `app.state.repo_indexer`. Routes access it via dependency injection.

Repo root is auto-detected: walk up from `hivenode/` directory until a `.git/` folder is found.

## 8. `.deia/to_localhost/`

This directory exists in the repo and is indexed like any other directory. Its purpose is a curated staging area — files placed here are explicitly intended to be accessible from the web app.

No special backend treatment beyond being part of the indexed tree. The frontend may choose to surface it prominently (e.g., as a pinned folder or quick-access panel).

**The directory should be committed to git** (with a `.gitkeep` or `README.md` inside) so it exists in every clone.

## 9. Security

| Concern | Mitigation |
|---------|-----------|
| Path traversal | Reject any path containing `..` or starting with `/` or `\` |
| `.git/` exposure | Hard-skip during scan, reject in read endpoint |
| Secrets (`.env`) | Gitignored by default, hidden from default view |
| Binary bombs | Size limit on read responses (configurable, default 10 MB) |
| Auth | `verify_jwt_or_local` — local dev bypasses, cloud requires JWT |
| Write access | None. All `/repo/*` routes are read-only (except visibility toggle) |
| Repo root escape | Resolve real path, assert it starts with repo root |

## 10. Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `pathspec` | `>=0.12` | Parse `.gitignore` patterns |

Add to `[project.dependencies]` in `pyproject.toml`. No other new dependencies — uses stdlib `sqlite3`, `hashlib`, `os.walk`.

## 11. Testing

### 11.1 Unit Tests

**File:** `tests/hivenode/repo/test_indexer.py`

- Scan a temp directory tree, verify DB contents
- Gitignore parsing: files matching patterns get `gitignored=True`
- Hardcoded exclusions: `.git/`, `node_modules/` never appear
- Visibility toggle: single file, directory (recursive)
- Query filters: by path prefix, extension, gitignored, visible
- Path traversal rejection
- Read file: text (UTF-8), binary (base64), missing (404)
- Stats calculation
- Re-scan preserves visibility flags
- Re-scan removes deleted files
- Tree structure correctness

### 11.2 Route Tests

**File:** `tests/hivenode/repo/test_repo_routes.py`

- POST `/repo/scan` → 200, returns counts
- GET `/repo/index` → default filters, custom filters, pagination
- GET `/repo/index?show_all=true` → includes hidden
- GET `/repo/tree` → nested structure
- GET `/repo/read?path=existing.py` → UTF-8 content
- GET `/repo/read?path=missing.py` → 404
- GET `/repo/read?path=../../../etc/passwd` → 400 (traversal blocked)
- GET `/repo/read?path=.git/config` → 403 (forbidden)
- PATCH `/repo/visibility` → toggles, recursive for dirs
- GET `/repo/stats` → summary counts

### 11.3 Gitignore Tests

**File:** `tests/hivenode/repo/test_gitignore.py`

- Parse standard `.gitignore` patterns
- Nested `.gitignore` files
- Negation patterns (`!important.log`)
- Wildcard patterns (`*.pyc`, `dist/`)

## 12. Implementation Priority

| Phase | Tasks | Estimate |
|-------|-------|----------|
| **Phase 1** | SQLite schema + RepoIndexer.scan() + gitignore parsing | S |
| **Phase 2** | Routes: /repo/scan, /repo/index, /repo/read | S |
| **Phase 3** | Routes: /repo/tree, /repo/visibility, /repo/stats | S |
| **Phase 4** | Tests (unit + route) | M |

All phases are bee-sized. Phases 1-2 are sequential. Phase 3 can parallel with Phase 2 if schema is stable. Phase 4 should be TDD (written alongside or before each phase per Rule 5).

## 13. Future Considerations (Not in Scope)

- **Watchdog auto-refresh:** Real-time scan on file changes (currently on-demand only)
- **Content search:** Full-text search within file contents via the index
- **Diff tracking:** Track changes between scans
- **Frontend tree browser component:** UI for browsing the repo index
- **Bulk read endpoint:** Fetch multiple files in one request for LLM context building
- **Webhook notifications:** Notify browser when scan completes

---

*daaaave-atx x Claude x CC BY 4.0*
