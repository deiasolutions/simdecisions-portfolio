# SPEC-HIVENODE-E2E-001: Hivenode End-to-End + Volume Architecture

**Date:** 2026-03-12
**Author:** Q88N (Dave) × Mr. AI (Claude)
**Status:** DRAFT — pending Q88N review
**Priority:** Alpha Part 2, Step 2

---

## 1. Purpose

Make the hivenode fully operational end-to-end: real data flowing through all routes, cloud storage wired to Railway, volume sync working between home:// and cloud://, shell commands executable from the browser terminal, and the 8os CLI tool installed and working from PowerShell.

After this spec is complete: Dave can start his local hivenode, save a chat conversation, see it sync to cloud, open it on his Mac, run shell commands from the browser terminal, and manage everything from the `8os` CLI.

---

## 2. 8os CLI Tool

A single CLI entry point for managing the ShiftCenter local environment. Installed via `pip install -e .` from the repo root. Provided by pyproject.toml scripts entry.

### 2.1 Commands

```
8os up                      # start local hivenode (port 8420)
8os down                    # stop local hivenode
8os status                  # running? volumes? connected nodes?
8os queue                   # run the build queue (SPEC-BUILD-QUEUE-001)
8os queue --status          # what's in the queue?
8os dispatch TASK.md        # dispatch a single task via dispatch.py
8os index                   # rebuild repo semantic search index
8os inventory stats         # feature/bug/backlog counts
8os inventory add ...       # passthrough to _tools/inventory.py
8os sync                    # force sync home:// ↔ cloud://
8os sync --status           # last sync time, pending items
8os volumes                 # list mounted volumes + online/offline
8os node list               # show connected nodes
8os node announce           # force re-announce to cloud
```

### 2.2 Implementation

Single Python entry point: `hivenode/cli.py` with `click` or `argparse` subcommands.

pyproject.toml:
```toml
[project.scripts]
8os = "hivenode.cli:main"
```

`8os up` runs `uvicorn hivenode.main:app --host 0.0.0.0 --port 8420` as a background process. PID stored at `~/.shiftcenter/hivenode.pid`. `8os down` reads the PID and kills it. `8os status` checks if the PID is alive.

### 2.3 Config Location

`~/.shiftcenter/config.yml` — created on first `8os up` if it doesn't exist.

```yaml
node_id: "node-a1b2c3d4"  # auto-generated, persisted
mode: "local"               # local | remote | cloud
port: 8420
cloud_url: "https://api.shiftcenter.com"
volumes:
  home: "C:\\Users\\davee\\ShiftCenter"     # Windows
  # home: "/Users/davee/ShiftCenter"        # Mac
sync:
  enabled: true
  interval_seconds: 300     # sync every 5 minutes
  on_write: true            # also sync immediately on file write
```

---

## 3. End-to-End Route Verification

All 16 existing routes verified with real HTTP calls and real data on disk. Not unit tests with mocks — actual `httpx` calls to a running hivenode instance.

### 3.1 Verification Test Suite

`tests/hivenode/test_e2e.py` — starts a real hivenode instance on a random port, runs all routes against it, tears down.

| Route | Test |
|-------|------|
| `GET /health` | Returns 200 + `{"status": "ok"}` |
| `GET /status` | Returns node_id, mode, uptime, volumes |
| `POST /auth/verify` | Rejects invalid JWT with 401. Accepts valid JWT (or bypasses in local mode). |
| `GET /auth/whoami` | Returns user info from token (or local user in local mode) |
| `GET /ledger/events` | Returns list after writing 3 test events |
| `GET /ledger/events/{id}` | Returns specific event |
| `POST /ledger/query` | Filters by event_type, actor, time range |
| `GET /ledger/cost` | Returns cost aggregation after writing events with cost data |
| `POST /storage/read` | Reads a file written to home:// |
| `POST /storage/write` | Writes a file, verifies on disk |
| `POST /storage/list` | Lists directory contents |
| `POST /storage/stat` | Returns file metadata (size, modified, content_hash) |
| `POST /storage/delete` | Deletes file, verifies gone |
| `POST /node/announce` | Registers node, returns ack |
| `GET /node/discover` | Returns list of known nodes |
| `POST /node/heartbeat` | Updates last_seen timestamp |

### 3.2 New Route: Shell Execution

`POST /shell/exec` — receives an IR shell command, translates to local OS, executes, returns output.

```json
// Request
{
  "command": "mkdir",
  "args": ["foo/bar"],
  "working_dir": "home://projects/myapp",
  "os_hint": "auto"
}

// Response
{
  "status": "success",
  "exit_code": 0,
  "stdout": "",
  "stderr": "",
  "os_used": "windows",
  "command_executed": "mkdir foo\\bar",
  "duration_ms": 12
}
```

#### 3.2.1 OS Translation

The hivenode detects its own OS on startup (`platform.system()`). Shell commands in IR are OS-agnostic. The executor translates:

| IR command | Windows | Unix/Mac |
|-----------|---------|----------|
| `mkdir foo/bar` | `mkdir foo\bar` | `mkdir -p foo/bar` |
| `ls -la` | `dir /a` | `ls -la` |
| `cp file1 file2` | `copy file1 file2` | `cp file1 file2` |
| `rm file` | `del file` | `rm file` |
| `cat file` | `type file` | `cat file` |
| `grep pattern file` | `findstr pattern file` | `grep pattern file` |
| `pwd` | `cd` | `pwd` |
| `mv file1 file2` | `move file1 file2` | `mv file1 file2` |
| `touch file` | `type nul > file` | `touch file` |

Path separators normalized: `/` → `\` on Windows, `\` → `/` on Unix.

#### 3.2.2 Allowlist / Denylist

Default allowlist (configurable in `~/.shiftcenter/config.yml`):

```yaml
shell:
  allowlist:
    - mkdir
    - ls
    - dir
    - cp
    - copy
    - mv
    - move
    - rm
    - del
    - cat
    - type
    - grep
    - findstr
    - pwd
    - cd
    - echo
    - touch
    - find
    - git
    - npm
    - python
    - pytest
    - node
    - pip
  denylist:
    - "rm -rf /"
    - "del /s /q C:\\"
    - "format"
    - "mkfs"
    - ":(){:|:&};:"
```

Commands not in allowlist → rejected with error. Commands matching denylist patterns → rejected with error + Event Ledger log (`SHELL_DENIED`).

#### 3.2.3 Security

- Shell exec is LOCAL MODE ONLY by default. Cloud hivenode does NOT expose `/shell/exec` unless explicitly enabled in config.
- Every execution logged to Event Ledger: `SHELL_EXEC` event with command, args, exit_code, duration, actor.
- Timeout: 30 seconds default, configurable per command.
- Working directory resolved through volume system — `home://projects/myapp` resolves to the actual path on disk.

---

## 4. Shell Input in Browser Terminal

### 4.1 Smart Parsing (No LLM)

The browser terminal detects what the user typed without calling an LLM:

1. Starts with `!` → force shell. Strip `!`, parse as shell command, send IR to `/shell/exec`.
2. Starts with `/` → slash command (SPEC-IPC-001). Handle locally.
3. Starts with `//` → IPC (SPEC-IPC-001). Route to target pane.
4. Starts with `>` → command palette mode.
5. Matches a known shell command pattern → shell. Parse as IR, send to `/shell/exec`.
6. Natural language → route to LLM.
7. Ambiguous → prompt: "Could not parse. Resolve with LLM? (Y/n)"

### 4.2 Known Shell Command Detection

A static list of command names checked against the first token:

```typescript
const SHELL_COMMANDS = new Set([
  // Unix
  'ls', 'cd', 'pwd', 'mkdir', 'rmdir', 'cp', 'mv', 'rm', 'cat',
  'grep', 'find', 'chmod', 'chown', 'touch', 'head', 'tail', 'wc',
  'sort', 'uniq', 'tar', 'curl', 'wget',
  // DOS
  'dir', 'copy', 'move', 'del', 'ren', 'type', 'findstr', 'cls',
  // Cross-platform tools
  'git', 'npm', 'npx', 'node', 'python', 'pip', 'pytest', 'docker',
  'ssh', 'scp',
]);
```

If the first word (lowercased) is in this set → shell command. No LLM needed.

### 4.3 Mode Override

User can set a mode to change the default behavior:

| Command | Effect |
|---------|--------|
| `/mode shell` | Everything treated as shell. `!` prefix added automatically. No LLM calls. |
| `/mode chat` | Everything treated as natural language. Shell commands sent to LLM. |
| `/mode hybrid` | Default. Smart parsing decides. |

Mode persists for the session. Resets on page reload or EGG switch.

When in shell mode, the prompt changes to show `!` prefix: `! hive>` or similar visual indicator.

### 4.4 User OS Preference

User setting (stored in settings panel alongside API keys):

| Setting | Values | Default |
|---------|--------|---------|
| Shell syntax | `unix` / `dos` / `both` | `both` |

When `both`: accept either style. The IR normalizes everything. The hivenode translates to whatever OS it's running on.

When `unix` or `dos`: reject commands in the wrong syntax with a helpful error: "You typed a DOS command but your shell syntax is set to Unix. Did you mean `ls` instead of `dir`?"

### 4.5 Efemera Shell Access

In Efemera (headless chat mode), shell is hidden by default. User must go to Settings → Developer → Enable Shell. When enabled, `!` prefix and `/mode shell` become available. The EGG config controls this:

```yaml
terminal:
  allow_shell: false    # Efemera default
```

---

## 5. Cloud Storage Adapter (Railway Object Storage)

Wire the cloud:// volume adapter to Railway's object storage so `cloud://` actually reads and writes.

### 5.1 Storage Backend

Railway provides persistent volumes. The cloud adapter uses Railway's volume mount or an S3-compatible API if Railway offers one. If Railway doesn't expose an S3 API, the cloud hivenode (running on Railway) stores files on its own persistent volume at `/data/cloud/`.

The cloud adapter on the LOCAL hivenode calls the CLOUD hivenode's `/storage/read` and `/storage/write` routes over HTTPS. The local hivenode is a client of the cloud hivenode for cloud:// operations.

```
Browser → local hivenode (home://) → writes to local disk
Browser → cloud hivenode (cloud://) → writes to Railway volume
Local hivenode → cloud hivenode → sync
```

### 5.2 Cloud Adapter Interface

```python
class CloudStorageAdapter(BaseStorageAdapter):
    def __init__(self, cloud_url, auth_token):
        self.cloud_url = cloud_url    # https://api.shiftcenter.com
        self.auth_token = auth_token  # ra96it JWT
    
    def read(self, path):
        # GET cloud_url/storage/read with path
    
    def write(self, path, content, actor, intent):
        # POST cloud_url/storage/write with path, content, provenance
    
    def list(self, path):
        # POST cloud_url/storage/list
    
    def stat(self, path):
        # POST cloud_url/storage/stat
    
    def delete(self, path):
        # POST cloud_url/storage/delete
```

Every operation includes the ra96it JWT for authentication. The cloud hivenode validates the token and scopes access to the user's storage.

### 5.3 Offline Behavior

If cloud:// is unreachable (network down, Railway down):

- Reads from cloud:// return `VOLUME_OFFLINE` error
- Writes intended for cloud:// get queued in `~/.shiftcenter/sync_queue/`
- Queue flushes when cloud:// comes back online
- The user sees the cloud:// volume as offline in the tree-browser (grey icon, "offline" badge)

---

## 6. Volume Sync: home:// ↔ cloud://

### 6.1 Sync Direction

Bidirectional. Both home:// and cloud:// are first-class. Neither is "primary."

| Event | What happens |
|-------|-------------|
| User saves file on browser (cloud:// online, home:// online) | Write to BOTH simultaneously |
| User saves file on browser (cloud:// online, home:// offline) | Write to cloud://. Queue sync to home:// for when it reconnects. |
| User saves file on browser (cloud:// offline, home:// online) | Write to home://. Queue sync to cloud:// for when it reconnects. |
| User saves file on local machine (not browser) | home:// hivenode detects change (file watcher). Queues sync to cloud://. |
| Cloud receives a write from another device | Cloud queues push to all registered home:// nodes on next heartbeat. |

### 6.2 Sync Mechanism

Each hivenode maintains a sync log: `~/.shiftcenter/sync_log.db` (SQLite)

```sql
CREATE TABLE sync_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    source_volume TEXT NOT NULL,
    target_volume TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',  -- pending | synced | conflict | failed
    queued_at TEXT NOT NULL,
    synced_at TEXT,
    error TEXT
);
```

On sync:
1. Compare content_hash of local file vs remote file
2. If hashes match → already synced, skip
3. If local is newer (by timestamp) → push local to remote
4. If remote is newer → pull remote to local
5. If both changed since last sync → CONFLICT

### 6.3 Conflict Resolution

Last-write-wins by timestamp. BOTH versions preserved:

- Winner overwrites the file at the original path
- Loser saved as `<filename>.conflict.<timestamp>.<ext>`
- Event Ledger logs `SYNC_CONFLICT` with both versions, both timestamps, which one won
- Tree-browser shows a conflict badge on the file
- User can open either version and choose which to keep

### 6.4 Sync Triggers

| Trigger | When |
|---------|------|
| On file write | Immediate queue (if `sync.on_write: true` in config) |
| Periodic | Every `sync.interval_seconds` (default 300 = 5 minutes) |
| Manual | `8os sync` from CLI |
| On node reconnect | When a previously offline node announces, full sync runs |
| On hivenode startup | Pull changes from cloud since last sync timestamp |

### 6.5 What Syncs

Everything under the volume's storage path EXCEPT:

- `.git/` directories
- `node_modules/`
- `__pycache__/`
- Files matching patterns in `~/.shiftcenter/sync_ignore` (gitignore syntax)

---

## 7. Chat Persistence End-to-End

### 7.1 Write Flow

When the user sends a message and receives a response:

1. Browser writes conversation to cloud:// always (via cloud hivenode API)
2. Browser ALSO writes to home:// if home hivenode is online (via local hivenode API)
3. Both writes happen simultaneously (Promise.all)
4. If either fails, the successful one is the source of truth
5. Sync reconciles later

### 7.2 Storage Format

Conversations stored as markdown files:

```
cloud://chats/2026-03-12/conversation-<uuid>.md
home://chats/2026-03-12/conversation-<uuid>.md
```

Format:
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

## You (09:32)
What about refresh tokens?

## Claude Sonnet 4.6 (09:32)
Refresh tokens use a rotation strategy...
```

Human-readable. Grep-searchable. No binary format. No database required for basic access.

### 7.3 Volume Choice

Users can choose where conversations are saved:

- Default: cloud:// + home:// (both, synced)
- Work conversations: work:// + cloud:// (synced, but NOT to home://)
- Private conversations: home:// only (never syncs to cloud)
- Setting per-conversation or as a default in settings panel

---

## 8. Tree-Browser Conversation Navigator

### 8.1 What It Shows

The tree-browser sidebar displays a list of conversations grouped by volume and date:

```
📁 home://chats/
   📁 2026-03-12/
      💬 Chat about authentication (10:15 AM)
      💬 Build queue planning (09:00 AM)
   📁 2026-03-11/
      💬 ShiftCenter repo build (all day)
📁 cloud://chats/
   💬 (synced copies — grey if identical to home)
📁 work://chats/
   💬 Client project discussion (2:30 PM)
```

### 8.2 What It Does NOT Do

The tree-browser does NOT read conversation content. It reads metadata only (title, date, volume, path). When the user selects a conversation:

1. Tree-browser sends `tree-browser:conversation-selected { path: "home://chats/2026-03-12/conversation-abc.md" }` on the bus
2. The 8os handler (a bus subscriber) receives the message
3. The handler calls the hivenode `/storage/read` route for that path
4. The handler pushes the content to the text-pane via `terminal:text-patch` bus message
5. The text-pane renders the conversation

### 8.3 Volume Badges

| Badge | Meaning |
|-------|---------|
| 🟢 | Volume online, synced |
| 🔄 | Sync in progress |
| ⚠️ | Conflict — two versions exist |
| ⬆️ | Pending upload to cloud |
| ⬇️ | Available on cloud, not cached locally |
| 🔴 | Volume offline |

---

## 9. Node Announcement + Discovery

### 9.1 On Startup

When a local hivenode starts (`8os up`):

1. Read `node_id` from `~/.shiftcenter/config.yml` (generate if first run)
2. Call cloud hivenode `POST /node/announce`:
   ```json
   {
     "node_id": "node-a1b2c3d4",
     "volume_name": "home",
     "ip": "auto-detected",
     "port": 8420,
     "os": "windows",
     "capabilities": ["storage", "shell", "ledger"]
   }
   ```
3. Cloud stores the node in its nodes table with `last_seen: now()`

### 9.2 Heartbeat

Every 60 seconds, local hivenode calls `POST /node/heartbeat` with `node_id`. Cloud updates `last_seen`. If a node misses 5 consecutive heartbeats (5 minutes), cloud marks it offline.

### 9.3 Discovery

`GET /node/discover` returns all nodes registered to the authenticated user:

```json
{
  "nodes": [
    { "node_id": "node-a1b2c3d4", "volume_name": "home", "os": "windows", "online": true, "last_seen": "..." },
    { "node_id": "node-e5f6g7h8", "volume_name": "mac", "os": "darwin", "online": false, "last_seen": "..." }
  ]
}
```

The browser uses this to show volume online/offline status in the tree-browser.

---

## 10. Event Ledger Integration

Every operation logs to the Event Ledger:

| Event Type | When |
|-----------|------|
| `SHELL_EXEC` | Shell command executed. Logs: command, args, exit_code, duration, actor. |
| `SHELL_DENIED` | Shell command rejected (not in allowlist or in denylist). |
| `VOLUME_READ` | File read from any volume. |
| `VOLUME_WRITE` | File written to any volume. Includes content_hash, actor, intent. |
| `VOLUME_DELETE` | File deleted. |
| `SYNC_STARTED` | Sync cycle begins. |
| `SYNC_COMPLETED` | Sync cycle ends. Logs: files_synced, files_skipped, conflicts. |
| `SYNC_CONFLICT` | Two versions of same file. Logs: both hashes, both timestamps, winner. |
| `SYNC_QUEUED` | Write queued for offline volume. |
| `SYNC_FLUSHED` | Queued write delivered after reconnect. |
| `NODE_ANNOUNCED` | Hivenode registered with cloud. |
| `NODE_HEARTBEAT` | Keepalive received. |
| `NODE_OFFLINE` | Node missed 5 heartbeats. |
| `NODE_RECONNECTED` | Previously offline node announced again. |

### 10.1 Token Tracking: Tokens Up vs Tokens Down

LLM vendors charge different rates for input (prompt) and output (completion) tokens — often 3-5x more for output. The Event Ledger must track these separately as first-class columns, not buried in payload JSON.

**Schema migration:** Add two columns to the `events` table:

```sql
ALTER TABLE events ADD COLUMN cost_tokens_up INTEGER;    -- input/prompt tokens
ALTER TABLE events ADD COLUMN cost_tokens_down INTEGER;  -- output/completion tokens
```

The existing `cost_tokens` column remains as the total (up + down) for backward compatibility.

**LLM_CALL events** must populate all three:
- `cost_tokens_up`: prompt tokens sent to the model
- `cost_tokens_down`: completion tokens received from the model
- `cost_tokens`: total (up + down)

**Cost aggregation** (`GET /ledger/cost`) must report:
```json
{
  "total_usd": 12.50,
  "total_tokens": 450000,
  "tokens_up": 400000,
  "tokens_down": 50000,
  "cost_up_usd": 1.20,
  "cost_down_usd": 11.30,
  "by_model": {
    "claude-sonnet-4-5": {
      "tokens_up": 300000,
      "tokens_down": 40000,
      "cost_usd": 10.50
    }
  }
}
```

**Why this matters:** A session that sends 400k prompt tokens and receives 50k completion tokens looks like 450k total — but the 50k output tokens may cost more than the 400k input tokens. Without directional tracking, cost analysis is blind.

The existing `hivenode/llm/cost.py` already calculates per-direction costs internally. This change promotes that data from payload JSON to schema columns so it's queryable, indexable, and visible in aggregation endpoints.

---

## 11. Platform Compatibility

### 11.1 Windows (Dave's PC)

- `8os up` starts hivenode on port 8420
- Volume path: `C:\Users\davee\ShiftCenter\` (configurable)
- Shell exec translates to DOS or PowerShell commands
- File watcher uses `watchdog` library for sync triggers
- PID file at `~/.shiftcenter/hivenode.pid`

### 11.2 Mac (Dave's Mac)

- Same `8os up` command
- Volume path: `/Users/davee/ShiftCenter/` (configurable)
- Shell exec translates to unix commands
- Same file watcher, same sync, same everything
- Same config file format at `~/.shiftcenter/config.yml`

### 11.3 Railway (Cloud)

- Starts via `uvicorn hivenode.main:app --host 0.0.0.0 --port $PORT`
- `HIVENODE_MODE=cloud` in environment
- Storage on Railway persistent volume at `/data/cloud/`
- No shell exec by default (disabled in cloud mode)
- JWT required on all routes (no local bypass)
- Node table in PostgreSQL (not SQLite)

---

## 12. Dependencies

| Package | Purpose | Install |
|---------|---------|---------|
| `click` | CLI framework for 8os | `pip install click` |
| `watchdog` | File system watcher for sync | `pip install watchdog` |
| `httpx` | Async HTTP client for cloud API calls | Already installed |
| `uvicorn` | ASGI server | Already installed |
| `fastapi` | HTTP framework | Already installed |

All added to pyproject.toml `[project.dependencies]`.

---

## 13. Implementation Priority

| Step | What | Effort | Depends on |
|------|------|--------|-----------|
| 1 | `8os` CLI tool (up/down/status) | M | pyproject.toml |
| 2 | E2E route verification test suite | M | Running hivenode |
| 3 | `/shell/exec` route + OS translation | M | Route verification |
| 4 | Browser terminal shell parsing (`!` prefix, smart detect, `/mode`) | M | Shell exec route |
| 5 | Cloud storage adapter (Railway volume) | M | Cloud hivenode deployed |
| 6 | Volume sync engine (sync_log, conflict resolution, queue) | L | Cloud adapter |
| 7 | Chat persistence rewrite (dual-write cloud + home) | M | Cloud adapter, sync |
| 8 | Tree-browser conversation navigator (bus-based, volume-aware) | M | Chat persistence |
| 9 | Node announcement + discovery + heartbeat | S | Cloud hivenode deployed |
| 10 | Event Ledger wiring for all new operations | S | Throughout |
| 11 | `8os` remaining commands (queue, dispatch, index, inventory, sync, volumes, node) | M | Various |
| 12 | Efemera shell toggle (settings, EGG config) | S | Shell parsing |

---

## 14. Testing Requirements

- E2E test suite: 16 route tests + 10 shell exec tests + 10 sync tests + 5 conflict tests + 5 node tests = ~46 minimum
- Every test uses real HTTP calls against a running hivenode instance (not mocked routes)
- Sync tests use two hivenode instances (simulating home + cloud)
- Shell tests verify OS translation on the current platform
- Cloud adapter tests mock the Railway endpoint (can't hit real Railway in CI)

---

**End of SPEC-HIVENODE-E2E-001.**

*daaaave-atx × Claude (Anthropic) · CC BY 4.0*
