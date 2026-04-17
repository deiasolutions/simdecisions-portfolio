# ShiftCenter Storage Architecture

> Volume-based filesystem with offline sync, provenance tracking, and Event Ledger integration.

## URI Protocol

All storage operations use volume URIs: `{volume}://{path}`

```
home://docs/README.md        → ~/.shiftcenter/home/docs/README.md
cloud://chat/conv-1.md       → remote hivenode (or local mirror)
local://scratch/tmp.txt      → session-scoped temp directory
```

### System Volumes (reserved, ≤7 chars)

| Volume | Adapter | Root | Purpose |
|--------|---------|------|---------|
| `home` | local_filesystem | `~/.shiftcenter/home` | User's persistent files |
| `cloud` | local_filesystem (mirrors remote) | `~/.shiftcenter/cloud` | Cloud sync target |
| `local` | local_filesystem | OS temp dir (session-scoped) | Ephemeral scratch space |

### User Volumes (≥8 chars)

Custom volumes can be declared at runtime via `VolumeRegistry.declare_volume()`.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│  Browser                                            │
│  ┌──────────────┐  ┌────────────────────────┐       │
│  │ volumeStorage│  │ filesystemAdapter       │       │
│  │ (localStorage│  │ (fetches /storage/list, │       │
│  │  sessionStore│  │  /storage/stat)         │       │
│  └──────────────┘  └────────────────────────┘       │
│         │                      │                    │
│  ┌──────────────┐              │                    │
│  │ volumeStatus │──────────────┤                    │
│  │ (polls node) │              │                    │
│  └──────────────┘              │                    │
└────────────────────────────────┼────────────────────┘
                                 │ HTTP
┌────────────────────────────────┼────────────────────┐
│  Hivenode (:8420)              │                    │
│  ┌─────────────────────────────▼──────────────────┐ │
│  │ storage_routes.py (7 endpoints)                │ │
│  └─────────────────────┬──────────────────────────┘ │
│                        │                            │
│  ┌─────────────────────▼──────────────────────────┐ │
│  │ FileTransport                                  │ │
│  │  - read / write / delete / move / copy / stat  │ │
│  │  - emits to Event Ledger                       │ │
│  │  - records provenance (hash, actor, intent)    │ │
│  └─────────────────────┬──────────────────────────┘ │
│                        │                            │
│  ┌─────────────────────▼──────────────────────────┐ │
│  │ VolumeRegistry                                 │ │
│  │  - resolves URI → adapter                      │ │
│  │  - caches adapter instances                    │ │
│  │  - loads config from YAML / env vars           │ │
│  └──────┬──────────────┬──────────────┬───────────┘ │
│         │              │              │             │
│  ┌──────▼─────┐ ┌──────▼─────┐ ┌─────▼──────────┐  │
│  │ LocalFS    │ │ CloudAdapter│ │ (future        │  │
│  │ Adapter    │ │ (HTTP→remote│ │  adapters)     │  │
│  │            │ │  hivenode)  │ │                │  │
│  │ - path     │ │ - offline   │ │                │  │
│  │   traversal│ │   → SyncQ   │ │                │  │
│  │   rejected │ │ - online    │ │                │  │
│  │            │ │   → direct  │ │                │  │
│  └────────────┘ └──────┬──────┘ └────────────────┘  │
│                        │                            │
│                 ┌──────▼──────┐                      │
│                 │ SyncQueue   │                      │
│                 │ (disk-backed│                      │
│                 │  write Q)   │                      │
│                 └─────────────┘                      │
└─────────────────────────────────────────────────────┘
```

## REST API (storage_routes.py)

All endpoints require auth (`verify_jwt_or_local`). Local dev mode uses device_id; cloud requires JWT.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/storage/write` | Write file (base64 content) |
| `GET` | `/storage/read?uri=` | Read file → raw bytes |
| `GET` | `/storage/list?uri=` | List directory entries |
| `GET` | `/storage/stat?uri=` | File metadata (size, modified, created) |
| `DELETE` | `/storage/delete?uri=` | Delete file |
| `POST` | `/storage/claim` | Migrate anonymous device data to authenticated user |
| `GET` | `/storage/volumes` | List mounted volumes with status |

## Offline Handling

The CloudAdapter handles connectivity loss gracefully:

- **Reads**: Fail immediately with `VolumeOfflineError` (caller must handle)
- **Writes**: Queue to `SyncQueue` on disk, succeed instantly (optimistic)
- **Queue flush**: Replays pending writes on next connectivity check

```python
# Offline write → queued
adapter.write("docs/note.md", content)  # returns {"queued": True}

# Online write → direct
adapter.write("docs/note.md", content)  # returns {"ok": True, "uri": "..."}
```

## Provenance & Audit

Every write/delete/move records:

| Field | Description |
|-------|-------------|
| `operation` | write, delete, move, copy |
| `content_hash` | SHA-256 of content |
| `parent_hash` | Previous content hash (version chain) |
| `actor` | `{type}:{id}` — e.g. `user:abc123`, `device:xyz` |
| `intent` | Human-readable reason for the operation |
| `timestamp` | ISO 8601 UTC |

Events also emit to the Event Ledger: `StorageWrite`, `StorageDelete`, `StorageMove`.

## Security

- **Path traversal**: Rejects `..`, absolute paths, backslashes
- **Actor validation**: Enforces `{type}:{id}` format
- **Volume isolation**: Each adapter operates within its root directory
- **Auth**: JWT required in cloud mode; device_id accepted in local mode

## Frontend Integration

### volumeStorage.ts (browser localStorage/sessionStorage)

```typescript
import { readVolume, writeVolume } from './shell/volumeStorage'

// All keys prefixed with sd:volume: to prevent collisions
writeVolume('local://prefs/theme', { mode: 'dark' })
const theme = readVolume<{ mode: string }>('local://prefs/theme')
```

### filesystemAdapter.ts (tree-browser)

```typescript
import { loadDirectoryTree } from './adapters/filesystemAdapter'

// Fetches from /storage/list + /storage/stat
const tree = await loadDirectoryTree('docs/', 'home')
// Returns TreeNodeData[] with icons, metadata
```

### volumeStatus.ts

```typescript
import { getVolumeStatus } from './services/volumes/volumeStatus'

const status = await getVolumeStatus('cloud://')
// 'online' | 'syncing' | 'conflict' | 'offline'
// Cached for 60s to avoid excessive polling
```

## 8OS CLI

Local environment manager. Entry point: `hivenode/cli.py`

```bash
8os up                    # Start hivenode on :8420
8os down                  # Stop hivenode
8os status                # Check if running
8os volumes               # List mounted volumes with status
8os queue [--status]      # Run build queue or show status
8os dispatch <task>       # Dispatch single task to bee
8os index [--full]        # Rebuild semantic search index
8os inventory [args...]   # Passthrough to inventory CLI
8os node list             # Show connected nodes
8os node announce         # Force re-announce to cloud
```

## Configuration

### YAML config (loaded by VolumeRegistry)

```yaml
volumes:
  home:
    adapter: local_filesystem
    root: ~/.shiftcenter/home
  cloud:
    adapter: local_filesystem
    root: ~/.shiftcenter/cloud
    always_available: true
    sync_target: hodeia
  local:
    adapter: local_filesystem
    root: /tmp/shiftcenter-session-{pid}
```

### Environment variables

| Variable | Purpose |
|----------|---------|
| `SHIFTCENTER_CLOUD_URL` | Remote hivenode URL for cloud adapter |
| `SHIFTCENTER_AUTH_TOKEN` | Bearer token for cloud requests |
| `SHIFTCENTER_SYNC_QUEUE_DIR` | Directory for offline write queue |

## File Map

```
hivenode/storage/
├── registry.py          # VolumeRegistry — adapter lifecycle
├── transport.py         # FileTransport — uniform API + ledger
├── resolver.py          # URI parsing: volume://path
├── config.py            # YAML + env var config loading
├── provenance.py        # Content hash + version chain tracking
└── adapters/
    ├── base.py          # Abstract adapter interface
    ├── local.py         # Local filesystem adapter
    ├── cloud.py         # HTTP client to remote hivenode
    └── sync_queue.py    # Offline write queue

hivenode/routes/
└── storage_routes.py    # 7 REST endpoints

hivenode/cli.py          # 8OS CLI entry point

browser/src/
├── shell/volumeStorage.ts                           # localStorage/sessionStorage
├── services/volumes/volumeStatus.ts                 # Online/offline polling
└── primitives/tree-browser/adapters/
    └── filesystemAdapter.ts                         # Tree-browser → /storage/list
```

## Test Coverage

| Suite | Tests | Status |
|-------|-------|--------|
| Cloud adapter (unit) | 15 | All passing |
| Cloud integration | 16 | All passing |
| Cloud E2E | 13 | Require live server |
| Config | 18 | All passing |
| Local adapter | 12+ | All passing |
| Storage routes | 10 | All passing |
| Auth (local/cloud) | 10 | All passing |
| Claim (device→user) | 4 | All passing |
| Volume integration | 10 | All passing |
| Cloud always-available | 5 | All passing |
| Sync queue | 8+ | All passing |
| volumeStorage (frontend) | 10 | All passing |
| filesystemAdapter (frontend) | 24 | All passing |
