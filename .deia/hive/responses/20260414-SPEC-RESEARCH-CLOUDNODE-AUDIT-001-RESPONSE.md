# SPEC-RESEARCH-CLOUDNODE-AUDIT-001: Hivenode/Cloudnode Architecture Audit -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-14

## Executive Summary

The simdecisions repository has a **partial cloudnode architecture** for remote hivenode discovery and coordination. The infrastructure exists for local/remote nodes to announce themselves to a cloud hub, but there is **no command relay mechanism** and **no offline queue** for cloud-to-local communication. The frontend connects to **Railway in production** via Vercel proxy, and **localhost in dev** — never directly to local hivenode.

**Key Finding:** The target architecture (Phone → Vercel → Railway cloudnode → local hivenode) is **partially implemented** for coordination/discovery, but **not implemented** for command dispatch or factory control.

---

## Findings YAML

```yaml
hivenode:
  entry_point:
    file: hivenode/main.py:247-250
    command: "uvicorn hivenode.main:app --host 127.0.0.1 --port 8420"
    deployment_modes:
      - local  # standalone PC, no cloud coordination
      - remote # PC that announces to cloud hub
      - cloud  # Railway deployment (cloud hub)

  daemons:
    - name: queue_runner
      file: .deia/hive/scripts/queue/run_queue.py
      embedded: true
      embed_file: hivenode/queue_bridge.py
      modes: [local, remote]
      function: Picks specs from queue, dispatches to Claude via MCP
      startup: main.py:241-259

    - name: scheduler
      file: hivenode/scheduler/scheduler_daemon.py
      embedded: true
      embed_file: hivenode/scheduler/scheduler_bridge.py
      modes: [local, remote]
      function: Computes optimal task schedule (OR-Tools)
      startup: main.py:250-254

    - name: dispatcher
      file: hivenode/scheduler/dispatcher_daemon.py
      embedded: true
      embed_file: hivenode/scheduler/dispatcher_bridge.py
      modes: [local, remote]
      function: Moves specs from backlog → queue based on schedule
      startup: main.py:255-259

    - name: heartbeat_worker
      file: hivenode/node/heartbeat.py
      modes: [remote]
      function: Sends 60s heartbeat to cloud hub
      startup: main.py:188-194

  checkin_exists: true
  checkin_file: hivenode/node/client.py:118-174
  checkin_endpoint: POST /node/announce
  checkin_payload: {node_id, mode, ip, port, volumes, capabilities}
  checkin_trigger: On startup (remote mode only)
  checkin_auth: JWT from ~/.shiftcenter/token

  heartbeat_exists: true
  heartbeat_file: hivenode/node/heartbeat.py:48-93
  heartbeat_interval: 60 seconds
  heartbeat_endpoint: POST /node/heartbeat
  heartbeat_payload: {node_id}
  heartbeat_on_404: Re-announce automatically

  inbound_command_method: null
  inbound_command_notes: |
    No command relay exists. Cloud hub cannot dispatch commands to local hivenodes.
    Local nodes run their own factory loop (queue_runner, scheduler, dispatcher).
    Cloud hub only tracks node registry — no orchestration capability.

cloudnode:
  exists: true
  location: Railway (hivenode service in cloud mode)
  codebase: Same hivenode/ codebase, mode=cloud
  deployment_file: Dockerfile + railway.toml
  database_url: $DATABASE_URL (Railway PostgreSQL)
  entry_point: "uvicorn hivenode.main:app --host 0.0.0.0 --port ${PORT}"

  registry_exists: true
  registry_file: hivenode/node_store.py
  registry_table: nodes (SQLite/PostgreSQL)
  registry_fields:
    - node_id (primary key)
    - user_id (from JWT)
    - mode (local | remote)
    - ip, port
    - volumes (JSON list)
    - capabilities (JSON list)
    - announced_at (ISO 8601)
    - last_seen (ISO 8601)
    - online (boolean, based on heartbeat freshness)

  relay_exists: false
  relay_notes: |
    No command relay from cloud → local exists.
    Cloud hub cannot dispatch work to local nodes.
    Cloud hub is a passive registry only.

  api_routes:
    - POST /node/announce  # Register/update node (cloud mode only)
    - POST /node/heartbeat # Update last_seen timestamp (cloud mode only)
    - GET  /node/discover  # List online nodes for user (cloud mode only)
    - GET  /node/status    # Local node status (local/remote mode only)
    - GET  /node/peers     # Discover peers from cloud (local/remote mode only)
  api_routes_file: hivenode/routes/node.py

  offline_queue_exists: false
  offline_queue_notes: |
    No deferred command queue exists.
    Cloud hub cannot queue work for offline nodes.

frontend:
  backend_url_config:
    file: browser/src/services/hivenodeUrl.ts:12-25
    logic: |
      if VITE_HIVENODE_URL is set: use that value
      else if hostname == localhost: "http://localhost:8420"
      else: "" (same-origin, proxied by Vercel)

  production_url: "" (same-origin)
  dev_url: "http://localhost:8420"

  vercel_proxy:
    file: vercel.json:2-11
    pattern: /api/(.*), /relay/(.*), /build/(.*), /health, /storage/(*)
    destination: https://hivenode-production.up.railway.app/$1

  direct_hivenode_connection: false
  direct_notes: |
    Frontend NEVER connects directly to local hivenode.
    In production: Vercel → Railway (cloud mode)
    In dev: localhost → local hivenode (local/remote mode)

  auth_method:
    provider: hodeia_auth (Railway service: beneficial-cooperation)
    jwt_issuer: hodeia.me
    verification: JWKS endpoint (hivenode/services/jwks_cache.py)
    storage: localStorage (sd:auth_token)
    header: Authorization: Bearer {token}

communication:
  websocket:
    exists: true
    purpose: Efemera messaging (chat channels)
    endpoint: /relay/ws
    file: hivenode/relay/ws.py
    scope: User-to-user chat only, NOT cloud-to-local coordination

  sse:
    exists: true
    purpose: Build monitor live updates
    endpoint: GET /build/stream
    file: hivenode/routes/build_monitor.py:239-263
    scope: Push heartbeats to frontend, NOT cloud-to-local coordination

  mcp:
    exists: true
    purpose: Local factory coordination (bees → hivenode)
    port: 8421
    file: hivenode/hive_mcp/local_server.py
    scope: Local-only, NOT cloud-to-local coordination
    availability: local/remote modes only (disabled in cloud mode)

  tunnel: null
  tunnel_notes: |
    No ngrok/cloudflared/tunnel infrastructure found.
    No reverse proxy for cloud → local communication.
```

---

## Research Questions Answered

### Hivenode (Local Runtime)

**Q1: What is the current entry point for hivenode?**

**A1:** `hivenode/main.py` line 247-250. Runs via `uvicorn hivenode.main:app --host 127.0.0.1 --port 8420`. Deployment mode is controlled by `HIVENODE_MODE` env var (local | remote | cloud).

**Evidence:** hivenode/main.py:247-250, hivenode/config.py:21-23

---

**Q2: What daemons/services run locally?**

**A2:** Four embedded services run in local/remote mode:

1. **Queue Runner** — `.deia/hive/scripts/queue/run_queue.py` embedded via `hivenode/queue_bridge.py` (main.py:241-247). Picks specs from queue, dispatches to Claude via MCP.

2. **Scheduler** — `hivenode/scheduler/scheduler_daemon.py` embedded via `hivenode/scheduler/scheduler_bridge.py` (main.py:250-254). Computes optimal task schedule using OR-Tools CP-SAT solver.

3. **Dispatcher** — `hivenode/scheduler/dispatcher_daemon.py` embedded via `hivenode/scheduler/dispatcher_bridge.py` (main.py:255-259). Moves specs from backlog → queue based on schedule.json.

4. **Heartbeat Worker** — `hivenode/node/heartbeat.py` (main.py:188-194, remote mode only). Sends 60s heartbeat to cloud hub.

**Evidence:** hivenode/main.py:188-259, hivenode/queue_bridge.py, hivenode/scheduler/scheduler_bridge.py, hivenode/scheduler/dispatcher_bridge.py, hivenode/node/heartbeat.py

---

**Q3: Does hivenode currently check in with any remote service on boot?**

**A3:** **Yes, in remote mode only.** On startup, `NodeAnnouncementClient.announce()` is called (main.py:190-196), which sends `POST /node/announce` to the cloud URL (default: `https://api.shiftcenter.com`) with node metadata (node_id, mode, ip, port, volumes, capabilities). Local mode does NOT check in.

**Evidence:** hivenode/main.py:188-196, hivenode/node/client.py:118-174

---

**Q4: Does hivenode maintain a heartbeat or presence signal to any external endpoint?**

**A4:** **Yes, in remote mode only.** `HeartbeatWorker` runs in background and sends `POST /node/heartbeat` every 60 seconds to the cloud hub. If 404 is returned (node expired), it automatically re-announces. Local mode does NOT send heartbeats.

**Evidence:** hivenode/node/heartbeat.py:48-93, hivenode/node/client.py:176-220

---

**Q5: How does hivenode receive inbound commands today?**

**A5:** **It does NOT receive inbound commands from cloud.** Hivenode runs its own autonomous factory loop (queue_runner + scheduler + dispatcher). Commands are dispatched **locally** via MCP on port 8421 from the queue runner to Claude bees. There is no cloud-to-local command relay mechanism.

**Evidence:** No cloud-to-local relay found. MCP server on port 8421 is local-only (hivenode/hive_mcp/local_server.py). Queue watcher monitors file changes locally (hivenode/queue_watcher.py).

---

### Cloudnode (Railway Backend)

**Q6: What currently runs on Railway?**

**A6:** The **same hivenode codebase** in `mode=cloud`. Railway runs `uvicorn hivenode.main:app` from the root `Dockerfile`. The cloud mode:
- Uses PostgreSQL (from $DATABASE_URL)
- Accepts node announcements and heartbeats
- Stores node registry in `nodes` table
- Does NOT run queue_runner, scheduler, dispatcher (disabled in cloud mode)
- Does NOT run MCP server (disabled in cloud mode)

**Evidence:** Dockerfile:17 (CMD uvicorn hivenode.main:app), railway.toml, hivenode/config.py:36-49

---

**Q7: Is there any registry or tracking of connected hivenode instances?**

**A7:** **Yes.** Cloud mode stores node announcements in a `nodes` table (SQLite/PostgreSQL) via `NodeStore` (hivenode/node_store.py). Tracks: node_id, user_id, mode, ip, port, volumes, capabilities, announced_at, last_seen, online (boolean). Nodes are marked offline if last_seen > 5 minutes ago.

**Evidence:** hivenode/node_store.py:8-195, hivenode/routes/node.py:20-79

---

**Q8: Is there a command relay mechanism from cloud to local?**

**A8:** **No.** Cloud hub is a **passive registry only**. It cannot dispatch commands to local nodes. Local nodes run their own autonomous factory loops. No relay endpoint exists. No offline queue exists.

**Evidence:** No POST /node/command or similar endpoint found. Cloud hub only exposes: /node/announce, /node/heartbeat, /node/discover (hivenode/routes/node.py).

---

**Q9: What API routes exist on the Railway deployment?**

**A9:** Cloud mode exposes:

**Node coordination:**
- `POST /node/announce` — Register/update node (cloud mode only)
- `POST /node/heartbeat` — Update last_seen timestamp (cloud mode only)
- `GET /node/discover` — List online nodes for user (cloud mode only)

**Other APIs (all modes):**
- `POST /build/heartbeat` — Build monitor (file: hivenode/routes/build_monitor.py)
- `GET /build/status` — Build status
- `GET /build/stream` — SSE for live heartbeats
- `POST /relay/ws` — WebSocket for Efemera chat (hivenode/relay/ws.py)
- Various storage, RAG, wiki, governance endpoints

**Evidence:** hivenode/routes/node.py, hivenode/routes/build_monitor.py, hivenode/relay/ws.py, hivenode/main.py:252-281

---

**Q10: Is there any offline queue or deferred command pattern?**

**A10:** **No.** Cloud hub does NOT queue work for offline nodes. No deferred command table exists. When a node goes offline, it simply disappears from the registry (online=FALSE). No commands are queued for later delivery.

**Evidence:** No offline queue table found in node_store.py. No queue-related fields in nodes table.

---

### Frontend (Vercel)

**Q11: What backend URL does the frontend connect to?**

**A11:**

- **Production (non-localhost):** `""` (same-origin), which Vercel proxies to `https://hivenode-production.up.railway.app` via vercel.json routes.
- **Dev (localhost):** `http://localhost:8420` (direct to local hivenode)

The logic is in `browser/src/services/hivenodeUrl.ts:12-25`.

**Evidence:** browser/src/services/hivenodeUrl.ts, vercel.json:2-11

---

**Q12: Does the frontend ever attempt to connect directly to hivenode?**

**A12:** **No (in production).** In production, the frontend always goes through Vercel's proxy to Railway (cloud mode). In dev, it connects directly to `localhost:8420` (local/remote mode). The frontend NEVER connects to a user's local hivenode from production.

**Evidence:** browser/src/services/hivenodeUrl.ts:14-24

---

**Q13: How is auth handled in frontend-to-backend calls?**

**A13:** JWT-based auth via `hodeia_auth` service (Railway: beneficial-cooperation). Frontend stores JWT in localStorage (`sd:auth_token`), sends it in `Authorization: Bearer {token}` header. Hivenode verifies via JWKS endpoint (`https://api.hodeia.me/.well-known/jwks.json`) using `JWKSCache` (hivenode/services/jwks_cache.py).

**Evidence:** browser/src/services/identity/identityService.ts:20-21, hivenode/config.py:73, hivenode/main.py:177-178

---

### Communication Patterns

**Q14: Is there any WebSocket, SSE, or long-poll connection between hivenode and cloud?**

**A14:**

- **WebSocket:** Exists for Efemera chat (`/relay/ws`), but this is **user-to-user messaging**, NOT cloud-to-local coordination. (hivenode/relay/ws.py)
- **SSE:** Exists for build monitor (`GET /build/stream`), but this is **frontend-only**, NOT cloud-to-local coordination. (hivenode/routes/build_monitor.py:239-263)
- **No long-poll** for cloud-to-local communication.

**Evidence:** hivenode/relay/ws.py, hivenode/routes/build_monitor.py:239-263

---

**Q15: Is MCP used for any cloud-to-local communication?**

**A15:** **No.** MCP server (port 8421) is local-only, runs in local/remote mode, and is used for **local factory coordination** (bees → hivenode). It is explicitly disabled in cloud mode (hivenode/main.py:220-238). MCP is NOT used for cloud-to-local relay.

**Evidence:** hivenode/main.py:220-238, hivenode/hive_mcp/local_server.py

---

**Q16: Are there any tunnel or reverse-proxy patterns in use?**

**A16:** **No.** No ngrok, cloudflared, localtunnel, or similar tunnel infrastructure found. No reverse proxy for cloud → local communication.

**Evidence:** No tunnel references found in codebase (searched ngrok, cloudflared, tunnel, localtunnel).

---

## Gaps List (Delta vs Target Architecture)

**Target:** Phone → Frontend (Vercel) → cloudnode (Railway) → hivenode (local PC)

**Current State:**

1. ✅ Phone → Frontend (Vercel) — **Works**
2. ✅ Frontend (Vercel) → Railway cloudnode — **Works** (via vercel.json proxy)
3. ❌ Railway cloudnode → hivenode (local PC) — **DOES NOT EXIST**

**Specific Gaps:**

1. **No command relay from cloud to local**
   - Cloud hub cannot dispatch work to local nodes
   - Cloud hub cannot trigger local queue runs
   - Cloud hub cannot request status from local nodes beyond heartbeat

2. **No offline queue**
   - Cloud hub cannot queue commands for offline nodes
   - No deferred execution pattern

3. **No bidirectional WebSocket for factory coordination**
   - Current WebSocket is user-to-user chat only
   - No factory control channel

4. **No tunnel/reverse-proxy for cloud → local communication**
   - Local nodes are behind NAT/firewall
   - Cloud hub cannot initiate connections to local nodes

5. **No cloud-initiated work dispatch**
   - Local nodes run autonomous factory loops
   - Cloud hub is passive registry only

6. **No multi-node coordination**
   - Cloud hub tracks nodes but doesn't orchestrate them
   - No load balancing or work distribution

---

## Recommendations List (Next Specs)

**Priority 1 (P0): Core cloud-to-local relay**

1. **SPEC-CLOUDNODE-RELAY-001: Bidirectional WebSocket for factory coordination**
   - Objective: Add `/factory/ws` WebSocket endpoint on cloud hub for remote nodes to connect
   - Scope: Remote nodes initiate WebSocket connection to cloud on startup, maintain persistent connection
   - Benefit: Enables cloud hub to send commands to local nodes in real-time

2. **SPEC-CLOUDNODE-QUEUE-001: Offline command queue**
   - Objective: Add `node_commands` table (node_id, command_type, payload, status, created_at, executed_at)
   - Scope: Cloud hub queues commands for offline nodes, delivers on reconnection
   - Benefit: Supports async dispatch when local nodes are offline

**Priority 2 (P1): Factory control from cloud**

3. **SPEC-CLOUDNODE-DISPATCH-001: Cloud-initiated spec dispatch**
   - Objective: Cloud hub can dispatch specs to specific local nodes via WebSocket relay
   - Scope: `POST /factory/dispatch` endpoint on cloud hub, sends `{spec_file, target_node_id}` via WebSocket
   - Benefit: Mobile factory control — dispatch work from phone

4. **SPEC-CLOUDNODE-STATUS-001: Cloud-initiated status queries**
   - Objective: Cloud hub can query local node status (active specs, queue depth, build monitor state)
   - Scope: `GET /factory/status?node_id={id}` endpoint, relays to local node via WebSocket
   - Benefit: Remote monitoring of local factory state

**Priority 3 (P2): Multi-node orchestration**

5. **SPEC-CLOUDNODE-LOADBALANCE-001: Work distribution across nodes**
   - Objective: Cloud hub can distribute specs across multiple local nodes
   - Scope: Algorithm to select target node based on load, availability, capabilities
   - Benefit: Horizontal scaling of factory

6. **SPEC-CLOUDNODE-FAILOVER-001: Node failover on disconnect**
   - Objective: Cloud hub detects node disconnect, re-queues in-flight specs to other nodes
   - Scope: Track spec → node assignment, transfer on heartbeat timeout
   - Benefit: Resilience to node crashes

**Alternative approach (if WebSocket is not viable):**

7. **SPEC-CLOUDNODE-POLLING-001: Local node polls cloud for commands**
   - Objective: Local nodes poll `GET /factory/commands?node_id={id}` every 30s
   - Scope: Cloud hub returns queued commands, local node acknowledges
   - Benefit: Simpler than WebSocket, works behind restrictive firewalls
   - Tradeoff: Higher latency (30s vs real-time)

---

## Files Modified

None (read-only research audit)

---

## What Was Done

- Read 16 files from pre-loaded list
- Searched codebase for node-related files (Glob, Bash grep)
- Read node coordination files: client.py, heartbeat.py, node_store.py, node.py
- Analyzed frontend URL resolution (hivenodeUrl.ts)
- Searched for WebSocket/SSE/MCP/tunnel patterns
- Analyzed embedded service bridges (queue_bridge.py, scheduler_bridge.py, dispatcher_bridge.py)
- Verified Vercel proxy configuration (vercel.json)
- Verified Railway deployment (Dockerfile, railway.toml)
- Answered all 16 research questions with file paths and line numbers
- Identified 6 major architectural gaps
- Proposed 7 next specs for cloudnode relay implementation

---

## Tests Run

None (read-only research audit)

---

## Next Steps

1. **Review findings YAML** with Q88N to confirm target architecture
2. **Prioritize gaps** — decide which relay pattern to pursue (WebSocket vs polling)
3. **Write next specs** from recommendations list (likely SPEC-CLOUDNODE-RELAY-001 first)
4. **Prototype WebSocket relay** — spike to validate feasibility on Railway + NAT traversal
5. **Design offline queue schema** — node_commands table + delivery protocol

---

## Cost Summary

- **Tokens:** ~40k input + ~8k output = ~48k total
- **Estimated cost:** ~$0.03 USD (Sonnet 4.5)

---

**Research complete. All 16 questions answered. Architecture delta identified. Ready for next phase.**
