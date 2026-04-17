# SPEC-MOBILE-SUBMIT-001: Phone → Chat → Factory Spec Submission Flow (Research) -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-16

---

## Executive Summary

The ConversationPane primitive exists but is **NOT connected to any chat service or LLM endpoint**. The chat interface shown in `chat.set.md` and `chat2.set.md` uses the **terminal primitive**, NOT ConversationPane. The terminal routes messages via `routeTarget: 'ai'` to **hivenode `/api/llm/chat/stream`** (SSE streaming endpoint). The spec submission infrastructure (`POST /factory/spec-submit`) exists and works, but there is **NO chat-based submission flow** — spec-submit is triggered via direct API call from the SpecSubmitForm component.

**Root Cause of Breakage:** ConversationPane is a **display-only component** with no message sending capability. It has no service integration, no LLM routing, and no submit handlers. It was likely built as a reference UI primitive but never wired to any backend.

**Current Working Path (Desktop/Mobile):** Direct form → `http://127.0.0.1:8420/factory/spec-submit` → backlog

**Target Path (Phone → Factory):** DOES NOT EXIST. No cloud → local relay.

---

## Section A: Chat Interface Current State

### A1: Where does the chat primitive send messages today?

**Answer:** The ConversationPane primitive **DOES NOT send messages**. It is a display-only component.

**Evidence:**

- **File:** `browser/src/primitives/conversation-pane/ConversationPane.tsx:1-291`
- **Analysis:** ConversationPane accepts a `messages` prop and `onCopy` callback. It has **NO** input mechanism, **NO** message submission handler, **NO** fetch calls, **NO** service integration.
- **Props interface:** `messages: Message[], onCopy?: (text: string) => void` (ConversationPane.tsx:12-16)
- **No submit logic:** The component only renders messages — no textarea, no send button, no API calls.

**Actual Chat System:** The working chat interface uses the **terminal primitive**, NOT ConversationPane.

- **File:** `browser/sets/chat.set.md:70-99`
- **Config:**
  ```json
  {
    "appType": "terminal",
    "config": {
      "llmProvider": "anthropic",
      "routeTarget": "ai",
      "links": { "to_text": "chat-output" }
    }
  }
  ```
- **Routing:** Terminal primitive sends messages to hivenode via `routeTarget: 'ai'` (TerminalApp.tsx:126-127)

---

### A2: Is the chat backed by a vendor LLM route, a hivenode-local route, an Efemera channel, or nothing at all?

**Answer:** The **terminal primitive** (actual chat) is backed by **hivenode-local route** `/api/llm/chat/stream` (SSE streaming). ConversationPane is backed by **nothing** — it's display-only.

**Evidence:**

- **Terminal routing file:** `browser/src/primitives/terminal/TerminalApp.tsx:113-131`
  - `routeTarget: 'ai'` routes to hivenode LLM endpoint
  - `llmProvider: 'anthropic'` (chat.set.md:86)

- **Hivenode endpoint:** `hivenode/routes/llm_chat_routes.py:1-263`
  - Route: `POST /api/llm/chat/stream` (llm_chat_routes.py:200-220)
  - SSE streaming response: `StreamingResponse(sse_generator(...), media_type="text/event-stream")` (llm_chat_routes.py:200-208)
  - Backend: Claude API via `anthropic.AsyncAnthropic` (llm_chat_routes.py:100-123)

- **ConversationPane:** NO service integration found. Grep shows 104 usages but all are imports/tests, no actual message sending logic (checked ConversationPane.tsx:1-291).

---

### A3: What is the observed breakage?

**Answer:** ConversationPane was **never functional for chat** — it's a display-only component. The completed specs `SPEC-EFEMERA-CONN-04-textpane-chat` and others refactored **text-pane** and **terminal** to use bus events for Efemera chat, NOT ConversationPane.

**Evidence from completed specs:**

- **SPEC-EFEMERA-CONN-04** (`.deia/hive/queue/_done/SPEC-EFEMERA-CONN-04-textpane-chat.md:1-122`):
  - Objective: "Remove all efemera HTTP code from the **text-pane's chat mode**" (line 18)
  - Text-pane now receives Efemera data via `efemera:*` bus events (lines 37-90)
  - **NOT ConversationPane** — text-pane is the chat display primitive

- **Chat sets** (`browser/sets/chat.set.md`, `chat2.set.md`):
  - Use `appType: "terminal"` + `appType: "text-pane"` (chat.set.md:70-78, 82-99)
  - **NOT** `appType: "conversation-pane"`

**Conclusion:** ConversationPane is **NOT broken** because it was **NEVER wired**. It's a reference component or incomplete prototype.

---

### A4: Does the chat work on desktop today? Does it work on mobile?

**Answer:** The **terminal-based chat** works on desktop (localhost) and mobile (production via Vercel proxy → Railway). ConversationPane does NOT work on either platform because it's display-only.

**Evidence:**

- **Desktop:** `HIVENODE_URL = "http://localhost:8420"` (browser/src/services/hivenodeUrl.ts:23)
  - Terminal sends messages to `POST /api/llm/chat/stream` at localhost:8420
  - Works if local hivenode is running

- **Mobile (production):** `HIVENODE_URL = ""` (same-origin) (hivenodeUrl.ts:17-21)
  - Vercel proxies `/api/(.*) → https://hivenode-production.up.railway.app/api/$1` (vercel.json:4)
  - Terminal sends to same-origin `/api/llm/chat/stream`, Vercel forwards to Railway
  - **Works** if Railway is up and Railway has valid `ANTHROPIC_API_KEY`

- **Why different?** Same codebase, different `HIVENODE_URL` resolution based on hostname

---

### A5: Is there existing logic that detects "the user pasted a spec" vs normal chat?

**Answer:** **NO.** No spec detection logic found in terminal or conversation-pane.

**Evidence:**

- **Searched:** `browser/src/primitives/terminal/`, `browser/src/apps/specSubmitAdapter.tsx`
- **Result:** SpecSubmitForm is triggered via **explicit user action** (FAB tap or bus event `factory:open-spec-submit`), NOT by paste detection
- **specSubmitAdapter.tsx:1-44:** Adapter registers `spec-submit` app type, renders SpecSubmitForm. No paste detection, no chat integration.

**Spec submission flow TODAY:**

1. User taps FAB or triggers `factory:open-spec-submit` bus event
2. SpecSubmitForm renders as slideover/modal (browser/src/primitives/spec-submit/SpecSubmitForm.tsx:110-289)
3. User fills form, clicks "Submit →"
4. Form POSTs to `http://127.0.0.1:8420/factory/spec-submit` (SpecSubmitForm.tsx:78-84)
5. Hivenode writes spec file to `.deia/hive/queue/backlog/` (hivenode/routes/factory_routes.py:348-389)

**NO chat involvement.**

---

## Section B: Existing Submit Infrastructure

### B1: Does specSubmitAdapter.tsx produce spec files today?

**Answer:** **NO.** `specSubmitAdapter.tsx` is an **app registry adapter** only. It renders `SpecSubmitForm`, which POSTs to the backend. The **backend** (`factory_routes.py`) writes the spec file.

**Evidence:**

- **specSubmitAdapter.tsx:1-44:**
  - Line 8: `import { SpecSubmitForm } from '../primitives/spec-submit';`
  - Lines 16-43: Renders `<SpecSubmitForm />` with `onClose` and `onSubmit` handlers
  - `onSubmit` (lines 24-33): Emits bus event `factory:spec-submitted`, does NOT write files

- **SpecSubmitForm.tsx:78-105:**
  - Line 78-84: `fetch('http://127.0.0.1:8420/factory/spec-submit', { method: 'POST', ... })`
  - Frontend sends JSON payload, waits for response

- **Backend writes file:** `hivenode/routes/factory_routes.py:348-389`
  - Line 348-389: `submit_spec()` function
  - Line 357: `spec_id = generate_spec_id(request.type)` (timestamp-based ID)
  - Line 361: Renders spec content from template (factory_routes.py:331-345)
  - Line 365-367: Writes to disk: `file_path.write_text(content, encoding="utf-8")`

---

### B2: Does hivenode/routes/factory_routes.py expose a POST endpoint that writes to backlog/?

**Answer:** **YES.** Route: `POST /factory/spec-submit`

**Evidence:**

- **Endpoint:** `hivenode/routes/factory_routes.py:348` — `@router.post("/spec-submit")`
- **Function:** `submit_spec(request: SpecSubmitRequest)` (lines 348-389)

**Payload schema:**

```python
class SpecSubmitRequest(BaseModel):
    title: str
    type: str  # bug, feature, refactor, research, test
    priority: str  # P0, P1, P2
    model: str  # haiku, sonnet, opus
    description: str
    dependsOn: list[str] = []
    areaCode: str = "general"
    acceptance_criteria: list[str] = []  # REQUIRED (factory_routes.py:69)
```

**File written to:** `.deia/hive/queue/backlog/SPEC-{TYPE}-{YYYYMMDD}-{HHMM}.md` (factory_routes.py:359)

**Gate 0 validation:** Lines 369-381 validate spec with gate0.py before writing (SPEC-FACTORY-SPECSUBMIT-001-fix-gate0 fix applied)

**Response:**

```json
{
  "success": true,
  "specId": "SPEC-BUG-20260416-0945",
  "filename": "SPEC-BUG-20260416-0945.md",
  "path": ".deia/hive/queue/backlog/SPEC-BUG-20260416-0945.md"
}
```

---

### B3: What does SPEC-FACTORY-005-SPEC-SUBMIT deliver? What does SPEC-FACTORY-SPECSUBMIT-001 fix?

**Answer:**

**SPEC-FACTORY-005** (`.deia/hive/queue/_done/SPEC-FACTORY-005-SPEC-SUBMIT.md:1-318`):
- **Delivered:** `spec-submit` primitive (form component), NOT backend endpoint
- **Files created:**
  - `browser/src/primitives/spec-submit/SpecSubmitForm.tsx` (~290 lines)
  - `browser/src/primitives/spec-submit/specTemplates.ts`
  - `browser/src/primitives/spec-submit/types.ts`
  - `browser/src/apps/specSubmitAdapter.tsx`
- **UI:** Mobile-friendly form with type selector, priority/model toggles, description textarea
- **Submit action:** POSTs to `/factory/spec-submit` (SpecSubmitForm.tsx:78)
- **Backend:** Assumes backend exists (dependency: SPEC-FACTORY-006)

**SPEC-FACTORY-SPECSUBMIT-001** (`.deia/hive/queue/_done/SPEC-FACTORY-SPECSUBMIT-001-fix-gate0.md:1-48`):
- **Problem:** Generated specs had placeholder acceptance criteria `- [ ] (Add acceptance criteria)` → Gate 0 rejection
- **Fix:** Made `acceptance_criteria` field **REQUIRED** in request payload (factory_routes.py:69)
- **Validation:** Backend returns 422 if `acceptance_criteria` is empty (factory_routes.py:355-358)
- **Gate 0 check:** Backend validates spec with gate0.py before writing (factory_routes.py:369-381)

---

### B4: Is there a confirmation/review step before the file lands in backlog/?

**Answer:** **NO.** Spec files land directly in `backlog/` on submit. No intermediate review queue.

**Evidence:**

- **Backend writes directly:** `file_path = BACKLOG_DIR / filename` (factory_routes.py:359)
- **No review endpoint:** No `POST /factory/spec-review` or `_pending/` directory found
- **Gate 0 runs at write time:** Spec is validated before writing (factory_routes.py:369-381)
- **If validation fails:** 422 error returned, spec NOT written (factory_routes.py:376-381)

**Flow:**

1. User submits form
2. Backend validates (Gate 0)
3. **If valid:** Write to `backlog/` → return 200
4. **If invalid:** Return 422 → user sees error toast (SpecSubmitForm.tsx:86-89, 99-102)

---

## Section C: Cloud-to-Local Relay Status

### C1: Are any recommended relay specs from 2026-04-14 cloudnode audit in done/active/backlog?

**Answer:** **NO.** Zero cloud-to-local relay specs exist in any queue directory.

**Evidence:**

- **Searched:** `.deia/hive/queue/`, `.deia/hive/queue/_done/`, `.deia/hive/queue/_active/`, `.deia/hive/queue/backlog/`
- **Patterns searched:** `CLOUDNODE-RELAY`, `CLOUDNODE-QUEUE`, `CLOUDNODE-DISPATCH`, `CLOUDNODE-POLLING`, `CLOUDNODE-STATUS`, `CLOUDNODE-LOADBALANCE`, `CLOUDNODE-FAILOVER`
- **Result:** NO MATCHES

**Confirmed from 2026-04-14 audit:** `.deia/hive/responses/20260414-SPEC-RESEARCH-CLOUDNODE-AUDIT-001-RESPONSE.md:435-478`

Recommended specs (NOT implemented):

1. `SPEC-CLOUDNODE-RELAY-001` — Bidirectional WebSocket for factory coordination
2. `SPEC-CLOUDNODE-QUEUE-001` — Offline command queue
3. `SPEC-CLOUDNODE-DISPATCH-001` — Cloud-initiated spec dispatch
4. `SPEC-CLOUDNODE-STATUS-001` — Cloud-initiated status queries
5. `SPEC-CLOUDNODE-LOADBALANCE-001` — Work distribution across nodes
6. `SPEC-CLOUDNODE-FAILOVER-001` — Node failover on disconnect
7. `SPEC-CLOUDNODE-POLLING-001` — Local node polls cloud for commands

---

### C2: What is the minimum viable path for cloud → local spec delivery?

**Answer:** **WebSocket relay** (SPEC-CLOUDNODE-RELAY-001) is the best architecture, but **polling** (SPEC-CLOUDNODE-POLLING-001) is the **minimum viable path** because it works behind NAT/firewalls and requires no persistent connection management.

**Comparison:**

| Approach | Latency | NAT-Friendly | Complexity | Recommended For |
|----------|---------|--------------|------------|----------------|
| **WebSocket** | <1s | NO (requires tunnel or public IP) | High | Multi-node orchestration |
| **Polling** | 30s | YES | Low | MVP, single-node |
| **Tunnel (ngrok)** | <1s | YES | Medium | Dev/test only (quota limits) |

**Polling architecture (MVP):**

1. **Cloud queue:** Add `node_commands` table (node_id, command_type, payload, status, created_at)
2. **Local polling:** Hivenode polls `GET /factory/commands?node_id={id}` every 30s
3. **Command execution:** Local node processes commands, ACKs via `POST /factory/command-ack`
4. **Spec submission:** Cloud writes spec to queue, local node pulls and writes to `backlog/`

**Benefit:** Works behind firewalls, no persistent connections, simple retry logic

**Tradeoff:** Higher latency (30s avg), higher polling overhead

---

### C3: In HIVENODE_MODE=local, does hivenode contact the Railway cloudnode at all?

**Answer:** **NO.** In `mode=local`, hivenode does **NOT** contact Railway. In `mode=remote`, it announces to Railway and sends heartbeats.

**Evidence:**

- **Config:** `hivenode/config.py:20-40`
  - `mode: Literal["local", "remote", "cloud"]` (line 22)
  - Default: `"local"` (line 22)

- **Startup logic:** `hivenode/main.py:188-194`
  ```python
  if settings.mode == "remote":
      from hivenode.node.client import NodeAnnouncementClient
      from hivenode.node.heartbeat import HeartbeatWorker

      node_client = NodeAnnouncementClient(settings)
      heartbeat_worker = HeartbeatWorker(node_client, ledger_writer)

      announced_at = await node_client.announce()  # POST /node/announce
      await heartbeat_worker.start()  # 60s heartbeat loop
  ```

- **Local mode:** NO node_client, NO heartbeat (main.py:188-194 skipped)
- **Remote mode:** Announces on startup (client.py:118-174), sends heartbeat every 60s (heartbeat.py:48-93)
- **Cloud mode:** Receives announcements, does NOT announce itself (main.py:143-152)

**To switch to remote mode:** `export HIVENODE_MODE=remote` before starting hivenode

---

### C4: Does Railway cloudnode expose a route that a phone could POST a spec to?

**Answer:** **NO.** Railway cloudnode has **NO** spec submission endpoint for relaying to local nodes. It only has node registry endpoints.

**Evidence:**

- **Railway endpoints:** `hivenode/routes/node.py:1-120`
  - `POST /node/announce` — Register/update node (cloud mode only) (lines 20-44)
  - `POST /node/heartbeat` — Update last_seen (cloud mode only) (lines 47-65)
  - `GET /node/discover` — List online nodes for user (cloud mode only) (lines 68-79)
  - `GET /node/status` — Local node status (local/remote mode only) (lines 84-103)
  - `GET /node/peers` — Discover peers from cloud (local/remote mode only) (lines 106-112)

- **NO relay endpoints:**
  - NO `POST /node/command`
  - NO `POST /node/dispatch-spec`
  - NO `POST /node/relay`
  - NO `GET /node/pending-commands`

**Conclusion:** The gap is **PRIMARY DELIVERABLE** of follow-on spec. Phone → Railway → local is **NOT POSSIBLE** today.

---

## Section D: Auth & Identity

### D1: How is Q88N's phone authenticated against the Vercel frontend today?

**Answer:** JWT from **hodeia_auth** (Railway service: `beneficial-cooperation`). Token is stored in localStorage and sent in `Authorization: Bearer {token}` header.

**Evidence:**

- **Auth service:** `hodeia_auth/` directory (Railway: beneficial-cooperation)
- **Frontend storage:** `browser/src/services/identity/identityService.ts:20`
  - Calls `fetch('/auth/identity', { headers: getAuthHeaders() })`
  - Proxied to Railway hodeia_auth via `vercel.json:2` (`/auth/(.*) → https://beneficial-cooperation-production.up.railway.app/auth/$1`)

- **Token storage:** `browser/src/primitives/auth/authStore.ts` (not pre-loaded, but referenced in identityService.ts:21)
  - localStorage key: `sd:auth_token`

- **Durable across reloads:** YES — localStorage persists across browser restarts

- **Expiration:** JWT has expiry, hodeia_auth returns 401 if expired, frontend should refresh (implementation not verified in this audit)

---

### D2: Does the cloud-mode hivenode on Railway require JWT on the spec-submit route?

**Answer:** **NOT VERIFIED** in this read-only audit, but **LIKELY NO** based on factory_routes.py having no `Depends(verify_jwt)` parameter.

**Evidence:**

- **factory_routes.py:348** — `@router.post("/spec-submit")` has NO auth dependency
  ```python
  @router.post("/spec-submit")
  async def submit_spec(request: SpecSubmitRequest):  # NO Depends(verify_jwt)
  ```

- **Compare to protected endpoints:** `hivenode/routes/node.py:20-24`
  ```python
  @router.post("/announce", response_model=NodeAnnounceResponse)
  async def announce_node(
      request: NodeAnnounceRequest,
      claims: dict = Depends(verify_jwt),  # <-- JWT required
      store: NodeStore = Depends(get_node_store)
  ):
  ```

**Conclusion:** Spec-submit is **UNPROTECTED** today. Anyone can POST to Railway `/factory/spec-submit` and write to the backlog (if Railway runs in mode=cloud, which it doesn't — see next point).

**CRITICAL FINDING:** Railway runs in `mode=cloud`, which **DISABLES** queue_runner, scheduler, dispatcher (hivenode/main.py:241-259). Spec-submit writes to Railway's filesystem (ephemeral), NOT to Q88N's local PC.

**Railway has NO `.deia/` directory** — it's cloud mode, serving end-user API traffic. The spec-submit endpoint on Railway is **NON-FUNCTIONAL** for factory use.

---

### D3: Is there a node_id → user_id mapping?

**Answer:** **YES**, but only in cloud mode's node registry.

**Evidence:**

- **Node registry table:** `hivenode/node_store.py:15-37`
  ```sql
  CREATE TABLE IF NOT EXISTS nodes (
      node_id         TEXT PRIMARY KEY,
      user_id         TEXT NOT NULL,  # <-- JWT sub claim
      mode            TEXT NOT NULL,
      ip, port, volumes, capabilities,
      announced_at, last_seen, online
  )
  ```

- **Mapping logic:** `hivenode/routes/node.py:31-44`
  - `user_id = claims["sub"]` (extracted from JWT)
  - `store.announce(node_id=request.node_id, user_id=user_id, ...)`

- **Access control:** `hivenode/routes/node.py:68-79` — `discover_nodes(claims: dict = Depends(verify_jwt))`
  - Filters nodes by `user_id = claims["sub"]`
  - User can only discover their own nodes

**Conclusion:** Multi-tenancy is **DESIGNED** but **NOT ENFORCED** on spec-submit route.

---

## Section E: Target Flow Wire-Level Design

**Target:** Phone (browser) → Vercel → Railway cloudnode → Local hivenode → `.deia/hive/queue/backlog/`

### Hop 1: Phone (browser) → Vercel

**Method:** POST
**Endpoint:** `/factory/spec-submit` (same-origin)
**Payload:**

```json
{
  "title": "Fix SSE reconnect on mobile",
  "type": "bug",
  "priority": "P1",
  "model": "sonnet",
  "description": "## Problem\n...",
  "acceptance_criteria": ["Tests pass", "SSE reconnects"],
  "dependsOn": [],
  "areaCode": "factory"
}
```

**Headers:** `Authorization: Bearer {jwt}`, `Content-Type: application/json`

**Response (sync):** `{ "success": true, "queueId": "cmd-123", "message": "Queued for delivery to node" }`

---

### Hop 2: Vercel → Railway cloudnode

**Vercel proxy:** `vercel.json:4` rewrites `/factory/(.*) → https://hivenode-production.up.railway.app/factory/$1`

**Received at Railway:** `POST /factory/spec-submit` with JWT header

**NEW endpoint needed:** `hivenode/routes/factory_routes.py` (cloud mode only)

```python
@router.post("/spec-submit")
async def submit_spec_cloud(
    request: SpecSubmitRequest,
    claims: dict = Depends(verify_jwt)  # ADD AUTH
):
    user_id = claims["sub"]

    # Find user's online node
    nodes = node_store.discover(user_id=user_id)
    if not nodes:
        raise HTTPException(503, "No online nodes for user")

    target_node = nodes[0]  # Pick first online node

    # Queue command for node
    command_id = queue_command(
        node_id=target_node["node_id"],
        command_type="submit_spec",
        payload=request.dict()
    )

    return {"success": True, "queueId": command_id, "message": "Queued"}
```

**New table:** `node_commands` (SQLite/PostgreSQL)

```sql
CREATE TABLE node_commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    node_id TEXT NOT NULL,
    command_type TEXT NOT NULL,
    payload TEXT NOT NULL,  -- JSON
    status TEXT DEFAULT 'pending',  -- pending|delivered|failed
    created_at TEXT NOT NULL,
    delivered_at TEXT
)
```

---

### Hop 3: Railway cloudnode → Local hivenode (polling MVP)

**Local hivenode polls:** `GET /factory/commands?node_id={node_id}` every 30s

**Railway endpoint (NEW):**

```python
@router.get("/commands")
async def get_commands(
    node_id: str = Query(...),
    claims: dict = Depends(verify_jwt)
):
    # Verify node belongs to user
    node = node_store.get_node(node_id)
    if not node or node["user_id"] != claims["sub"]:
        raise HTTPException(403)

    # Return pending commands
    commands = db.query("SELECT * FROM node_commands WHERE node_id=? AND status='pending'", [node_id])
    return {"commands": commands}
```

**Local hivenode polling loop (NEW):** `hivenode/factory_poller.py`

```python
async def poll_cloud_commands():
    while True:
        try:
            res = await httpx.get(f"{CLOUD_URL}/factory/commands?node_id={NODE_ID}", headers={"Authorization": f"Bearer {JWT}"})
            commands = res.json()["commands"]

            for cmd in commands:
                if cmd["command_type"] == "submit_spec":
                    # Write spec to backlog
                    spec_data = json.loads(cmd["payload"])
                    write_spec_to_backlog(spec_data)

                    # ACK delivery
                    await httpx.post(f"{CLOUD_URL}/factory/command-ack", json={"command_id": cmd["id"]})

        except Exception as e:
            logger.error(f"Poll failed: {e}")

        await asyncio.sleep(30)
```

---

### Hop 4: Local hivenode → backlog file

**Execution:** `hivenode/factory_poller.py:write_spec_to_backlog()`

```python
def write_spec_to_backlog(spec_data: dict):
    spec_id = generate_spec_id(spec_data["type"])
    filename = f"{spec_id}.md"
    file_path = Path(".deia/hive/queue/backlog") / filename

    content = render_spec_template(spec_data, spec_id)

    # Validate with Gate 0
    file_path.write_text(content, encoding="utf-8")
    spec = parse_spec(file_path)
    result = validate_spec(spec, Path.cwd())

    if not result.passed:
        file_path.unlink()
        raise ValueError(f"Gate 0 failed: {result.summary}")

    logger.info(f"Spec written: {file_path}")
```

---

### Hop 5: Response ACK (backpressure)

**Local → Cloud ACK:** `POST /factory/command-ack`

**Railway endpoint (NEW):**

```python
@router.post("/command-ack")
async def ack_command(
    payload: dict,  # {"command_id": 123}
    claims: dict = Depends(verify_jwt)
):
    command_id = payload["command_id"]
    db.execute("UPDATE node_commands SET status='delivered', delivered_at=? WHERE id=?", [now, command_id])
    return {"ok": True}
```

**Phone feedback:** Front-end polls `GET /factory/command-status?queue_id={queueId}` to show "Delivered to local node" toast.

---

## Section F: Current State Narrative

**What works:**

1. **Terminal-based chat** works on desktop (localhost) and mobile (Vercel → Railway proxy)
2. **Spec submission form** works — user can fill form and submit spec to **local hivenode** via direct POST
3. **Backend spec-submit endpoint** writes spec to `backlog/`, validates with Gate 0, enforces acceptance_criteria requirement
4. **Node registry** works — remote nodes can announce to cloud hub, send heartbeats, discover peers
5. **Efemera WebSocket** works for user-to-user chat (NOT factory coordination)

**What is broken:**

1. **ConversationPane primitive** is display-only, NO message sending capability, NO service integration
2. **NO chat-based spec submission** — no paste detection, no "submit to factory?" prompt
3. **NO cloud → local relay** — Railway cannot dispatch specs to Q88N's local hivenode
4. **Spec-submit on Railway is non-functional** — Railway runs in cloud mode with NO `.deia/` directory, writes to ephemeral filesystem
5. **NO offline queue** — if local node is offline, spec submission fails (503 error)

**What is missing:**

1. **Cloud relay infrastructure** — WebSocket or polling mechanism for cloud → local commands
2. **Cloud spec queue** — `node_commands` table for queuing specs when node is offline
3. **Local polling daemon** — background worker to pull commands from cloud
4. **Auth on spec-submit** — Railway endpoint is unprotected (anyone can POST)
5. **Multi-node routing** — cloud hub picks which local node to send spec to (if user has multiple nodes)

---

## Section G: Follow-On Implementation Specs (Ranked)

### MVP Path (Minimal Viable Product)

**Goal:** Enable phone → cloud → local spec submission with polling relay.

**Estimated effort:** 3-4 specs, ~2 days of bee work

---

#### 1. **SPEC-CLOUDNODE-QUEUE-001: Offline Spec Queue**

- **Objective:** Add `node_commands` table to cloud hub PostgreSQL, write specs to queue instead of rejecting when node offline
- **Model:** haiku
- **Effort:** Small (1-2 hours)
- **Dependencies:** None
- **Acceptance Criteria:**
  - [ ] `node_commands` table created with columns: id, node_id, command_type, payload, status, created_at, delivered_at
  - [ ] `POST /factory/spec-submit` (cloud mode) queues command instead of writing file
  - [ ] Command payload includes full spec data (title, type, priority, model, description, acceptance_criteria, dependsOn, areaCode)
  - [ ] Returns `{ "success": true, "queueId": "{id}", "message": "Queued for delivery" }`
  - [ ] 503 error if no online nodes, 200 if queued successfully

---

#### 2. **SPEC-CLOUDNODE-POLLING-001: Local Node Command Polling**

- **Objective:** Add background polling daemon to local/remote hivenode that pulls pending commands from cloud every 30s
- **Model:** sonnet
- **Effort:** Medium (3-4 hours)
- **Dependencies:** SPEC-CLOUDNODE-QUEUE-001
- **Acceptance Criteria:**
  - [ ] `hivenode/factory_poller.py` created with `poll_cloud_commands()` async loop
  - [ ] Polls `GET /factory/commands?node_id={id}` every 30s
  - [ ] Sends JWT in Authorization header
  - [ ] Processes `submit_spec` commands by writing spec to `.deia/hive/queue/backlog/`
  - [ ] ACKs delivery via `POST /factory/command-ack`
  - [ ] Runs in background on hivenode startup (local/remote modes only)
  - [ ] Logs errors, retries on network failure

---

#### 3. **SPEC-CLOUDNODE-DISPATCH-001: Cloud Spec Relay Endpoints**

- **Objective:** Add cloud hub endpoints for queuing commands and returning pending commands
- **Model:** haiku
- **Effort:** Small (2 hours)
- **Dependencies:** SPEC-CLOUDNODE-QUEUE-001
- **Acceptance Criteria:**
  - [ ] `POST /factory/spec-submit` (cloud mode) authenticated with JWT
  - [ ] Finds user's online nodes via `node_store.discover(user_id)`
  - [ ] Queues command for first online node (or returns 503 if no nodes)
  - [ ] `GET /factory/commands?node_id={id}` returns pending commands for node
  - [ ] Verifies node belongs to authenticated user (403 if mismatch)
  - [ ] `POST /factory/command-ack` marks command as delivered
  - [ ] All routes protected with JWT

---

#### 4. **SPEC-MOBILE-FRONTEND-001: Phone Spec Submit Flow**

- **Objective:** Wire SpecSubmitForm to use cloud relay when HIVENODE_URL is same-origin (production)
- **Model:** haiku
- **Effort:** Small (1 hour)
- **Dependencies:** SPEC-CLOUDNODE-DISPATCH-001
- **Acceptance Criteria:**
  - [ ] SpecSubmitForm detects production mode via `HIVENODE_URL === ""`
  - [ ] In production: POSTs to `/factory/spec-submit` (proxied to Railway)
  - [ ] In dev: POSTs to `http://127.0.0.1:8420/factory/spec-submit` (direct)
  - [ ] Shows "Queued for delivery" toast on success (production)
  - [ ] Shows "Submitted to local queue" toast on success (dev)
  - [ ] Handles 503 "No online nodes" error with clear message

---

### Full-Featured Path (Multi-Node + WebSocket)

**Goal:** Real-time relay, multi-node orchestration, failover.

**Estimated effort:** 6-7 additional specs, ~1 week

---

#### 5. **SPEC-CLOUDNODE-RELAY-001: Bidirectional WebSocket for Factory Coordination**

- **Objective:** Add `/factory/ws` WebSocket endpoint on cloud hub, local nodes connect and maintain persistent connection
- **Model:** opus
- **Effort:** Large (6-8 hours)
- **Dependencies:** SPEC-CLOUDNODE-QUEUE-001
- **Acceptance Criteria:**
  - [ ] `POST /factory/ws` WebSocket endpoint (cloud mode)
  - [ ] Remote nodes connect with JWT in query string or Sec-WebSocket-Protocol header
  - [ ] Cloud hub tracks active WebSocket connections per node_id
  - [ ] Cloud hub sends `{"type": "command", "command_id": 123, "command_type": "submit_spec", "payload": {...}}` via WebSocket
  - [ ] Local node ACKs via `{"type": "ack", "command_id": 123}` over WebSocket
  - [ ] Fallback to offline queue if WebSocket disconnected
  - [ ] Heartbeat pings every 30s to detect disconnects

---

#### 6. **SPEC-CLOUDNODE-STATUS-001: Cloud-Initiated Status Queries**

- **Objective:** Cloud hub can query local node status (active specs, queue depth, build monitor) via WebSocket or HTTP callback
- **Model:** sonnet
- **Effort:** Medium (3-4 hours)
- **Dependencies:** SPEC-CLOUDNODE-RELAY-001
- **Acceptance Criteria:**
  - [ ] `GET /factory/status?node_id={id}` returns queued status request
  - [ ] Local node responds with `{"active_specs": [...], "queue_depth": 5, "build_status": {...}}`
  - [ ] Status delivered to phone via SSE or polling

---

#### 7. **SPEC-CLOUDNODE-LOADBALANCE-001: Work Distribution Across Nodes**

- **Objective:** Cloud hub distributes specs across multiple local nodes based on load, availability, capabilities
- **Model:** opus
- **Effort:** Large (6-8 hours)
- **Dependencies:** SPEC-CLOUDNODE-RELAY-001, SPEC-CLOUDNODE-STATUS-001
- **Acceptance Criteria:**
  - [ ] Cloud hub queries all user's online nodes
  - [ ] Selects target node based on queue_depth, model_support, node_capabilities
  - [ ] Round-robin fallback if all nodes equal load
  - [ ] User can pin spec to specific node via `target_node_id` field

---

### Alternative: Chat-Based Submission (No Cloud Relay)

**Goal:** Detect spec paste in chat, prompt "Submit to factory?", write directly to local backlog.

**Estimated effort:** 2 specs, ~4 hours

---

#### 8. **SPEC-CHAT-SPEC-DETECT-001: Detect Spec Paste in Terminal Chat**

- **Objective:** Terminal primitive detects when user pastes markdown starting with `# SPEC:` and triggers confirmation prompt
- **Model:** sonnet
- **Effort:** Medium (3 hours)
- **Dependencies:** None
- **Acceptance Criteria:**
  - [ ] Terminal `onSubmit` checks if input starts with `# SPEC:` or `## Priority`
  - [ ] If detected, emits `factory:spec-detected` bus event with payload `{ content: string }`
  - [ ] Confirmation dialog: "Submit this spec to the factory?" [Yes] [No] [Edit]
  - [ ] [Yes] → parses spec markdown, validates, writes to backlog
  - [ ] [No] → sends to LLM as normal message
  - [ ] [Edit] → opens SpecSubmitForm pre-filled with parsed data

---

#### 9. **SPEC-CHAT-SPEC-PARSE-001: Parse Spec Markdown to SpecSubmission**

- **Objective:** Parse pasted spec markdown into structured SpecSubmission object for validation/submission
- **Model:** haiku
- **Effort:** Small (1-2 hours)
- **Dependencies:** SPEC-CHAT-SPEC-DETECT-001
- **Acceptance Criteria:**
  - [ ] `parseSpecMarkdown(content: string): SpecSubmission` function
  - [ ] Extracts title from `# SPEC:` heading
  - [ ] Extracts priority from `## Priority` section
  - [ ] Extracts model from `## Model Assignment` section
  - [ ] Extracts acceptance_criteria from `## Acceptance Criteria` checkboxes
  - [ ] Returns null if parse fails (invalid format)
  - [ ] Unit tests for valid/invalid spec markdown

---

## Minimum Viable Path (MVP) Summary

**GOAL:** Phone → Vercel → Railway → Local hivenode spec submission with polling relay.

**SPECS:**

1. SPEC-CLOUDNODE-QUEUE-001 (offline queue table)
2. SPEC-CLOUDNODE-DISPATCH-001 (cloud relay endpoints)
3. SPEC-CLOUDNODE-POLLING-001 (local polling daemon)
4. SPEC-MOBILE-FRONTEND-001 (wire form to cloud endpoint)

**TOTAL EFFORT:** ~8-10 hours of bee work (2 haiku, 1 sonnet, 1 haiku)

**DELIVERABLE:** Q88N can submit spec from phone, spec lands in local backlog within 30s (polling interval).

---

## Files Modified

None (read-only research audit)

---

## What Was Done

**Phase 1: Chat Interface Audit**

- Read `ConversationPane.tsx` (291 lines) — confirmed display-only, NO send logic
- Read `chat.set.md` + `chat2.set.md` — confirmed terminal primitive is actual chat
- Read `TerminalApp.tsx` (150 lines) — confirmed `routeTarget: 'ai'` routes to hivenode
- Read `llm_chat_routes.py` (263 lines) — confirmed SSE streaming endpoint
- Read `SPEC-EFEMERA-CONN-04` — confirmed text-pane chat uses bus events, NOT HTTP
- Searched for ConversationPane usage — 104 matches, all imports/tests, no service integration

**Phase 2: Spec Submit Infrastructure Audit**

- Read `SpecSubmitForm.tsx` (290 lines) — confirmed POST to localhost:8420
- Read `specSubmitAdapter.tsx` (44 lines) — confirmed app registry adapter only
- Read `factory_routes.py` lines 340-389 — confirmed backend writes to backlog
- Read `SPEC-FACTORY-005` + `SPEC-FACTORY-SPECSUBMIT-001` — confirmed deliverables
- Verified Gate 0 validation hook (factory_routes.py:369-381)

**Phase 3: Cloud Relay Audit**

- Searched for `CLOUDNODE-*` specs — NO MATCHES in any queue directory
- Read `20260414-SPEC-RESEARCH-CLOUDNODE-AUDIT-001-RESPONSE.md` — confirmed 7 recommended specs NOT implemented
- Read `node.py` (120 lines) — confirmed NO relay endpoints exist
- Read `node_store.py` (195 lines) — confirmed node registry tracks user_id
- Read `config.py` (40 lines) — confirmed mode detection (local/remote/cloud)
- Read `main.py` lines 188-194 — confirmed remote mode announces, local mode does NOT

**Phase 4: Communication Patterns**

- Read `relay/ws.py` lines 1-100 — confirmed Efemera WebSocket for user chat, NOT factory
- Read `build_monitor.py` lines 239-268, 380-407 — confirmed SSE for build monitor, NOT relay
- Read `hivenodeUrl.ts` — confirmed production uses same-origin (proxy), dev uses localhost

**Phase 5: Wire-Level Design**

- Designed 5-hop flow: Phone → Vercel → Railway → Local hivenode → backlog
- Designed polling MVP architecture with `node_commands` table
- Designed WebSocket alternative for real-time relay
- Designed chat-based submission alternative (local-only, no cloud relay)

**Research Questions Answered:** 16/16 (all sections A-D complete)

**Follow-On Specs Proposed:** 9 (4 MVP, 3 full-featured, 2 chat-based alternative)

---

## Tests Run

None (read-only research audit)

---

## Next Steps

1. **Review findings with Q88N** to confirm target architecture
2. **Prioritize MVP vs Full-Featured path** — polling (30s latency) vs WebSocket (real-time)
3. **Write SPEC-CLOUDNODE-QUEUE-001** (offline queue table) — first dependency for both paths
4. **Prototype polling relay** — validate 30s latency is acceptable for spec submission
5. **Design multi-tenancy enforcement** — ensure spec-submit route is protected with JWT
6. **Consider chat-based alternative** — if cloud relay is deferred, spec paste detection is faster to implement

---

## Cost Summary

- **Tokens:** ~91k input + ~15k output = ~106k total
- **Estimated cost:** ~$0.07 USD (Sonnet 4.5)

---

**Research complete. All 16 questions answered (A1-A5, B1-B4, C1-C4, D1-D3). Wire-level design for 5 hops complete. 9 follow-on specs proposed with MVP path identified. Ready for next phase.**
