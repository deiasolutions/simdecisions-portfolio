# TASK-003: Named Volume System — Registry, Transport, Provenance

## Objective

Build the named volume filesystem at `hivenode/storage/`. This is the storage abstraction for ShiftCenter — every file operation goes through volumes with provenance tracking and ledger emission. Users never touch raw paths; they use `cloud://docs/report.md` or `home://projects/foo/main.py`.

## Dependencies

- **TASK-001 (Event Ledger)** must be complete. Every FileTransport operation emits to the Event Ledger via `hivenode.ledger.writer`.

## Context

ShiftCenter has a named volume system where storage locations are declared, resolved, and accessed through a uniform interface. Volumes are adapter-backed — the registry doesn't care if the backend is a local directory, Railway object storage, or a VPS in Hetzner. It just needs an adapter that implements read/write/move/list/exists/delete.

**Three built-in volumes:**

| Volume | Scheme | Backend | Description |
|--------|--------|---------|-------------|
| cloud | `cloud://` | Railway object storage | Every user gets this. Always available when online. Persistent. |
| home | `home://` | Local filesystem | User's personal hivenode on their local machine. Syncs from cloud (sync is future task). |
| local | `local://` | Local filesystem | Current session scratch space. Ephemeral. |

Users can also register **custom volumes** — a work machine, a VPS, a second laptop — anything with an adapter. The registry is open-ended but enforces **namespace separation**:

- **System volumes** (cloud, home, local, work) are reserved names. All system volume names are **≤7 characters**.
- **User-defined volumes** must have names **≥8 characters** (e.g., `work-mac`, `hetzner-vps-1`, `basement-nas`).
- This prevents collisions structurally — no user can accidentally shadow a system volume.
- The registry must reject attempts to declare a user volume with ≤7 characters, and reject attempts to redeclare a reserved system volume.

## MVP Scope — What to Build

Four subsystems:

### 1. Volume Registry
- Load volume declarations from YAML config
- Declare new volumes at runtime (register custom volumes)
- Resolve a volume scheme to its adapter + config
- Report volume status (available/unavailable/degraded)
- Built-in defaults for `cloud://`, `home://`, `local://`

### 2. Path Resolver
- Parse `volume://path/to/file` URIs into (volume_name, relative_path)
- Resolve to actual backend location via the volume's adapter
- Validate paths (no traversal attacks, no absolute paths inside volume)
- Support `volume://` root (list volume root)

### 3. FileTransport
- Uniform file operations across any volume: `read`, `write`, `move`, `copy`, `list`, `exists`, `delete`, `stat`
- Every mutating operation (write, move, copy, delete) emits to the Event Ledger
- Every mutating operation records provenance (see below)
- Cross-volume operations supported (e.g., `move cloud://a.txt home://a.txt`)
- Operations take `actor` (universal entity ID) and `intent` (string) as required params

### 4. Provenance Chain
- Every file version gets a provenance record: `content_hash + parent_hash + actor + intent`
- `content_hash`: SHA-256 of file content after the operation
- `parent_hash`: content_hash of the previous version (None for new files)
- `actor`: universal entity ID (`human:dave`, `agent:BEE-001`)
- `intent`: what the actor was doing (`"initial upload"`, `"edit section 3"`, `"auto-format"`)
- Provenance stored in a SQLite table alongside the ledger (same DB or separate — bee's choice, but same pattern)
- Query provenance history for any file path

## What NOT to Build

- No sync engine (cloud ↔ home sync is a future task)
- No offline queue (future)
- No archive resurrection / tombstone recovery (future)
- No encryption at rest (future)
- No quota enforcement (future)
- No file locking / conflict resolution (future)
- No frontend code
- No FastAPI routes (future — API layer comes later)

## Volume Config Format (YAML)

```yaml
# Example: ~/.shiftcenter/volumes.yaml
volumes:
  cloud:
    adapter: "railway_object_storage"
    config:
      endpoint_url: "${RAILWAY_STORAGE_URL}"
      bucket: "user-${USER_ID}"
    always_available: true

  home:
    adapter: "local_filesystem"
    config:
      root: "~/.shiftcenter/home"

  local:
    adapter: "local_filesystem"
    config:
      root: "${TMPDIR}/shiftcenter/session-${SESSION_ID}"
      ephemeral: true

  # Example custom volume
  work-mac:
    adapter: "local_filesystem"
    config:
      root: "/Volumes/Projects"
```

The config supports `${ENV_VAR}` expansion and `~` home directory expansion.

## Database Schema — Provenance

```sql
CREATE TABLE provenance (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp       TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f','now')),
    volume          TEXT NOT NULL,
    path            TEXT NOT NULL,
    operation       TEXT NOT NULL CHECK(operation IN ('write','move','copy','delete')),
    content_hash    TEXT,             -- SHA-256 of content after op (NULL for delete)
    parent_hash     TEXT,             -- content_hash of previous version (NULL for new files)
    actor           TEXT NOT NULL,    -- universal entity ID
    intent          TEXT NOT NULL,    -- human-readable purpose
    source_volume   TEXT,             -- for move/copy: source volume
    source_path     TEXT,             -- for move/copy: source path
    payload_json    TEXT              -- additional metadata
);
```

Indexes on: `(volume, path)`, `content_hash`, `actor`, `timestamp`.

## Event Ledger Integration

Every mutating FileTransport operation emits to the Event Ledger:

| event_type | actor | target | When |
|------------|-------|--------|------|
| `storage.write` | caller actor | `volume://path` | File written |
| `storage.move` | caller actor | `volume://dest` | File moved (payload has source) |
| `storage.copy` | caller actor | `volume://dest` | File copied (payload has source) |
| `storage.delete` | caller actor | `volume://path` | File deleted |

All events use `domain: "storage"`, `signal_type: "internal"`.

## Adapter Interface

```python
class BaseVolumeAdapter(ABC):
    """Abstract base for volume storage backends."""

    @abstractmethod
    def read(self, path: str) -> bytes:
        """Read file content. Raises FileNotFoundError."""

    @abstractmethod
    def write(self, path: str, content: bytes) -> None:
        """Write file content. Creates parent dirs as needed."""

    @abstractmethod
    def delete(self, path: str) -> None:
        """Delete file. Raises FileNotFoundError."""

    @abstractmethod
    def exists(self, path: str) -> bool:
        """Check if file exists."""

    @abstractmethod
    def list(self, path: str = "") -> list[str]:
        """List files/dirs at path. Returns relative names."""

    @abstractmethod
    def stat(self, path: str) -> dict:
        """Return file metadata: size, modified, created."""

    @abstractmethod
    def move(self, src: str, dst: str) -> None:
        """Move file within this volume."""
```

### LocalFilesystemAdapter
- Fully implemented working adapter
- Maps paths to a root directory on the local filesystem
- Validates no path traversal outside root (resolve + check prefix)
- Creates parent directories on write

### CloudAdapter (Railway Object Storage)
- Interface defined, constructor wired, methods raise `NotImplementedError("Cloud backend not yet connected")`
- This is NOT a stub — the class is real, the constructor takes config (endpoint_url, bucket), the methods have correct signatures and docstrings
- The actual Railway/S3-compatible wiring is a future task
- Tests use the local adapter; cloud adapter tests verify the interface contract only

## File Structure

```
hivenode/storage/
├── __init__.py
├── registry.py            -- VolumeRegistry: load YAML, declare, resolve, status
├── resolver.py            -- parse volume://path URIs, resolve to adapter + relative path
├── transport.py           -- FileTransport: read/write/move/copy/list/exists/delete/stat + ledger + provenance
├── provenance.py          -- ProvenanceStore: record/query provenance chain, content hashing
├── config.py              -- default volume YAML, env var expansion, path expansion
├── adapters/
│   ├── __init__.py
│   ├── base.py            -- BaseVolumeAdapter ABC
│   ├── local.py           -- LocalFilesystemAdapter (fully working)
│   └── cloud.py           -- CloudAdapter (interface wired, backend not yet connected)
```

```
tests/hivenode/storage/
├── __init__.py
├── conftest.py            -- temp dirs, volume YAML fixtures, ledger fixture, test registry
├── test_registry.py       -- YAML load, declare, resolve, status, custom volumes, missing volume
├── test_resolver.py       -- URI parsing, path traversal rejection, root listing, invalid URIs
├── test_transport.py      -- read/write/move/copy/delete via transport, ledger event verification, provenance verification
├── test_provenance.py     -- hash chain, parent tracking, history query, delete provenance
├── test_local_adapter.py  -- all adapter ops on real temp dirs, path traversal guard, nested dirs
├── test_cloud_adapter.py  -- interface contract, NotImplementedError on ops, config acceptance
├── test_config.py         -- env var expansion, ~ expansion, default volumes, malformed YAML
```

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Minimum 45 tests across all test files
- [ ] Edge cases: path traversal (`../../etc/passwd`), missing volume, write to read-only, cross-volume move, empty file, binary content, deep nested paths, env var expansion with missing vars, Unicode filenames, user volume name ≤7 chars rejected, system volume redeclare rejected, user volume name ≥8 chars accepted

## Constraints

- Python 3.13
- No file over 500 lines
- No stubs — every function fully implemented (except CloudAdapter backend methods which raise NotImplementedError with clear message)
- No external dependencies beyond stdlib + pytest + pyyaml
- All timestamps in ISO 8601 UTC
- All entity IDs follow `{type}:{id}` format
- Content hashes are SHA-256 hex digest

## Files to Read First

- `hivenode/ledger/writer.py` — Event Ledger writer interface (TASK-001)
- `hivenode/ledger/schema.py` — Event Ledger schema patterns (TASK-001)
- `pyproject.toml` — current dependencies

## Deliverables

- [ ] `hivenode/storage/__init__.py`
- [ ] `hivenode/storage/registry.py`
- [ ] `hivenode/storage/resolver.py`
- [ ] `hivenode/storage/transport.py`
- [ ] `hivenode/storage/provenance.py`
- [ ] `hivenode/storage/config.py`
- [ ] `hivenode/storage/adapters/__init__.py`
- [ ] `hivenode/storage/adapters/base.py`
- [ ] `hivenode/storage/adapters/local.py`
- [ ] `hivenode/storage/adapters/cloud.py`
- [ ] `tests/hivenode/storage/__init__.py`
- [ ] `tests/hivenode/storage/conftest.py`
- [ ] `tests/hivenode/storage/test_registry.py`
- [ ] `tests/hivenode/storage/test_resolver.py`
- [ ] `tests/hivenode/storage/test_transport.py`
- [ ] `tests/hivenode/storage/test_provenance.py`
- [ ] `tests/hivenode/storage/test_local_adapter.py`
- [ ] `tests/hivenode/storage/test_cloud_adapter.py`
- [ ] `tests/hivenode/storage/test_config.py`
- [ ] Updated `pyproject.toml` with `pyyaml` dependency

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-003-RESPONSE.md`

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
