# COMMS FLOW TRACE - 7 Pipes

**Date:** 2026-03-20
**Requested by:** Q88N
**Executed by:** Q33NR (Claude Code CLI)
**Scope:** READ ONLY diagnostic - no files modified

---

## VERDICT SUMMARY

| Pipe | Name | Status | Transport |
|------|------|--------|-----------|
| 1 | Pane -> Pane (same browser) | **CONNECTED** | In-memory MessageBus |
| 2 | Pane -> Shell (iframe postMessage) | **MISSING** | N/A - no iframes in architecture |
| 3 | Terminal -> Backend | **CONNECTED** | HTTP POST (4 route targets) |
| 4 | Browser -> Hivenode (WebSocket) | **MISSING** | No WS endpoint exposed to browser |
| 5 | Browser -> Hivenode (SSE) | **CONNECTED** | EventSource (build monitor only) |
| 6 | Hivenode -> Cloud (upstream push) | **CONNECTED** | httpx async POST |
| 7 | Cloud -> Browser (push path) | **STUBBED** | Polling only (3s interval) |

**Score: 4 CONNECTED, 1 STUBBED, 2 MISSING**

---

## PIPE 1: Pane -> Pane (same browser)              CONNECTED

### Files in the path
- `browser/src/infrastructure/relay_bus/messageBus.ts` (lines 142-239): Core bus - subscribe, send, mute, nonce replay protection, telemetry
- `browser/src/infrastructure/relay_bus/GovernanceProxy.tsx` (lines 127-203): Whitelist enforcement, gate enforcer, ethics check, approval modal
- `browser/src/infrastructure/relay_bus/constants.ts` (lines 7-24): Mute cycle definition (none/notifications/inbound/outbound/full)

### What works
- Message delivery to specific pane via `target: 'pane-id'` - finds subscriber, delivers envelope
- Broadcast delivery via `target: '*'` - delivers to all subscribers with per-pane mute checks
- Whitelist enforcement - GovernanceProxy blocks messages not in bus_emit list
- All 5 mute levels correctly block/allow delivery
- Platform invariants (relay_bus, ledger_writer, gate_enforcer, settings_advertisement, metrics_advertisement) bypass mute
- Nonce replay protection - duplicates rejected within 5s window (line 156)
- LOG_EVENT dispatched with kind: PLATFORM_PANE_MESSAGE on every send (line 216-217)

### What breaks
- Governance modal (HOLD/ESCALATE/REQUIRE_HUMAN) queues message but loses it if modal dismissed without action
- No retry mechanism - if subscriber handler throws, message lost silently
- No message acknowledgment - sender gets nonce but no delivery confirmation

### Tests
- `browser/src/infrastructure/relay_bus/__tests__/messageBus.test.ts` - subscribe, send, broadcast, nonce, LOG_EVENT (PASSING)
- `browser/src/infrastructure/relay_bus/__tests__/messageBus.mute.test.ts` - all 5 mute levels verified (PASSING)
- `browser/src/infrastructure/relay_bus/__tests__/messageBus.crossWindow.test.ts` - same-window isolation (PASSING)
- `browser/src/infrastructure/relay_bus/__tests__/GovernanceProxy.test.tsx` - whitelist, invariant bypass, modal (PASSING)

---

## PIPE 2: Pane -> Shell (iframe postMessage)        MISSING

### Files in the path
- None. No `window.addEventListener('message', ...)` handler exists for hive-shell protocol.

### What works
- Nothing. This pipe does not exist.

### What breaks
- No event listener for incoming postMessage events
- No "hive-shell" protocol handler anywhere in codebase
- No iframe wrapper component for apps

### Why it's MISSING (not broken)
All panes are in-process React components, not iframes:
- `browser/src/shell/components/AppFrame.tsx` (lines 15-30): Apps loaded via `getAppRenderer(appType)` as React components
- `browser/src/shell/components/PaneContent.tsx` (lines 21-30): Same pattern - inline DOM rendering
- All panes share one MessageBus instance via ShellCtx - no IPC bridge needed

This pipe would only be needed for third-party iframe-embedded apps (future capability).

### Tests
- None exist. No implementation to test.

---

## PIPE 3: Terminal -> Backend                        CONNECTED

### Files in the path
- `browser/src/primitives/terminal/useTerminal.ts` (line 46): routeTarget options defined ('ai' | 'shell' | 'relay' | 'ir' | 'canvas')
- `browser/src/services/terminal/shellExecutor.ts` (lines 28-111): Shell command execution
- `browser/src/services/terminal/terminalResponseRouter.ts` (lines 139-223): Envelope bus routing

### Route target breakdown

**routeTarget='shell'** - CONNECTED
- Handler: `executeShellCommand()` in shellExecutor.ts (lines 28-111)
- Endpoint: `POST /shell/exec`
- Backend: `hivenode/routes/shell.py` (lines 15-93)
- Security: Allowlist validation, Event Ledger logging, 30s timeout
- Response returns to terminal at useTerminal.ts lines 394-401

**routeTarget='relay'** - CONNECTED
- Handler: useTerminal.ts lines 428-495
- Endpoint: `POST /efemera/channels/{channelId}/messages`
- Backend: `hivenode/efemera/routes.py` (lines 102-120)
- Bus event: `channel:message-sent` dispatched to all listeners

**routeTarget='canvas'** - CONNECTED
- Handler: useTerminal.ts lines 498-572
- Endpoint: `POST /api/phase/nl-to-ir`
- Backend: `hivenode/routes/phase_nl_routes.py` (lines 297-450)
- LLM call: Routes to Anthropic or OpenAI API
- Bus event: `terminal:ir-deposit` sent to canvas pane

**routeTarget='ir'** - CONNECTED
- Handler: useTerminal.ts lines 589-773
- Endpoint: `POST /llm/chat`
- Backend: `hivenode/routes/llm_routes.py` (lines 74-180)
- Splits response: chat text -> `terminal:text-patch` to text-pane, IR blocks -> `terminal:ir-deposit` to canvas

**routeTarget='ai'** - CONNECTED
- Handler: useTerminal.ts lines 746-762
- Endpoint: `POST /llm/chat`
- Simpler than 'ir' - no IR extraction, text only -> `terminal:text-patch`

### What works
- All 5 route targets make HTTP calls and receive responses
- Shell commands validated against allowlist
- Efemera messages route through bus to text-pane
- NL-to-IR conversion with LLM integration
- LLM chat proxy with cost tracking

### What breaks
- No retry on failed API calls (all route targets fail-fast)
- Canvas mode requires manual API key in request body
- Relay mode has no real-time updates (polling only)
- Only shell commands are logged to Event Ledger; other routes are not audited

### Tests
- `browser/src/services/terminal/__tests__/terminalResponseRouter.test.ts` (PASSING)
- `browser/src/primitives/terminal/__tests__/useTerminal.test.ts` (PASSING)
- `tests/hivenode/routes/test_shell.py` (PASSING)

---

## PIPE 4: Browser -> Hivenode (WebSocket)            MISSING

### Files in the path
- `hivenode/adapters/cli/bot_http_server.py` (lines 95-150): WebSocket server exists but for CLI bots only, NOT browser
- `browser/src/apps/sim/lib/ws.ts` (lines 1-149): EphemeraWS class for Sim app only, NOT terminal/shell

### What works
- Nothing for browser-to-hivenode WebSocket communication.

### What breaks
- **Browser side:** No WebSocket client in browser/src/services/terminal/. No /api/ws connection attempted. Terminal uses HTTP exclusively.
- **Hivenode side:** No `@router.websocket()` in any route file. No /api/ws endpoint in FastAPI app. Bot WS server in bot_http_server.py is NOT mounted in hivenode/main.py.
- No ConnectionManager class exists.
- No broadcast mechanism from hivenode to browser via WS.

### Tests
- None exist. No implementation to test.

---

## PIPE 5: Browser -> Hivenode (SSE)                  CONNECTED

### Files in the path
- `hivenode/routes/build_monitor.py` (lines 528-560): SSE endpoint via StreamingResponse
- `browser/src/apps/buildMonitorAdapter.tsx` (lines 149-197): EventSource consumer
- `browser/src/apps/buildDataService.tsx` (lines 86-147): SSE subscriber + bus broadcaster

### What works
- Live heartbeat delivery from dispatch tasks to browser within seconds
- State persistence via `.deia/hive/queue/monitor-state.json` (survives restarts)
- Fallback polling: buildDataService polls `/build/status` every 5s if SSE drops
- Snapshot pattern: initial SSE event sends full status, then incremental updates
- Keepalive: `: keepalive {timestamp}\n\n` every 15 seconds
- Multi-subscriber: async queue (maxsize=50) for concurrent browser connections
- Bus broadcast: 4 events (build:bees-updated, build:runner-updated, build:log-updated, build:completed-updated)

### What breaks
- **Monitor-only** - SSE is NOT general-purpose. Only build monitor uses it. Cannot carry bus messages.
- Queue full scenario: if subscriber queue exceeds 50 pending, new heartbeats silently dropped
- Subscriber leak: if browser crashes mid-SSE, queue stays in _subscribers list (no timeout cleanup)
- No message delivery guarantee (at-most-once semantics)

### Tests
- `tests/hivenode/routes/test_build_monitor_sse.py` (359 lines, 10+ tests, ALL PASSING)

---

## PIPE 6: Hivenode -> Cloud (upstream push)          CONNECTED

### Files in the path
- `hivenode/node/client.py` (261 lines): Node announcement client
  - announce() lines 118-151: POST /node/announce
  - heartbeat() lines 176-220: POST /node/heartbeat
  - discover() lines 222-256: GET /node/discover
- `hivenode/storage/adapters/cloud.py` (292 lines): Cloud storage adapter
  - write() lines 85-129: POST /storage/write (with offline queue fallback)
  - read() lines 47-83: GET /storage/read
  - delete() lines 204-240: DELETE /storage/delete
- `hivenode/storage/adapters/sync_queue.py` (130 lines): Offline write queue
  - enqueue() lines 36-64: Queue to disk
  - flush() lines 78-129: Retry queued writes

### What works
- JWT-authenticated outbound to cloud (Bearer token from ~/.shiftcenter/token)
- Node announcement: POST /node/announce with node_id, mode, ip, port, volumes, capabilities
- Cloud storage I/O: read, write, delete to cloud:// URIs
- Offline write queueing: when cloud unreachable, writes queue to ~/.shiftcenter/sync_queue/
- Peer discovery: GET /node/discover returns list of connected nodes
- Cloud URL configurable (defaults to https://api.shiftcenter.com)
- Public IP detection via ipify.org fallback (lines 79-93)

### What breaks
- **No auto-heartbeat thread** - heartbeat() must be explicitly called; no daemon
- **No auto-announce on startup** - announce() requires explicit call
- **Sync queue flush is manual** - SyncQueue.flush() not called by any background task
- **No push-back from cloud** - cloud can only respond to requests, cannot initiate
- **Token expiry not handled** - 401 on heartbeat just logs error, no refresh logic
- **One-directional** - hivenode pushes to cloud, cloud cannot push to hivenode

### Tests
- Manual e2e via CLOUD-STORAGE-SMOKE-TEST.md
- No unit tests for NodeAnnouncementClient

---

## PIPE 7: Cloud -> Browser (push path)               STUBBED

### Files in the path
- `browser/src/services/efemera/relayPoller.ts` (96 lines): Long-polling client
- `browser/src/primitives/tree-browser/adapters/channelsAdapter.ts`: Channel data adapter
- `browser/src/primitives/tree-browser/adapters/membersAdapter.ts`: Members data adapter
- `hivenode/efemera/routes.py`: GET /efemera/channels/{id}/messages?since={timestamp}

### What works
- Polling mechanism: fetch() with 5s timeout, 3s interval (line 28 default)
- Incremental sync: `since` param fetches only new messages after lastTimestamp
- Bus integration: dispatches `channel:message-received` to MessageBus
- Network resilient: silently ignores poll failures

### What breaks
- **NO EventSource/SSE from cloud** - only polling, no server-sent events
- **NO WebSocket client** - no bidirectional socket for real-time sync
- **NO push notifications** - no service worker, no browser notification API
- **NO message queue on server** - server doesn't persist "sent but not yet delivered"
- **NO presence sync** - members list is polled, not pushed
- **Up to 3-second latency** for channel messages
- **~60 HTTP requests/hour** per active channel (scalability concern)
- **No delivery guarantee** - if browser closes between polls, messages missed

### What's NOT built (from ADR-023 Efemera Relay design)
- Server-side relay queue
- Conflict resolution / CRDT
- Presence protocol
- Push notification infrastructure

### Tests
- `browser/src/apps/__tests__/efemera.channels.integration.test.tsx` (PASSING)
- No backend relay tests

---

## GAPS FOR HODEIA MOBILE-FIRST

| Gap | Impact | Severity |
|-----|--------|----------|
| **No WebSocket (Pipe 4)** | No real-time bidirectional comms | HIGH - mobile needs push |
| **No cloud->browser push (Pipe 7)** | 3s polling latency, no offline delivery | HIGH - mobile UX blocker |
| **No iframe bridge (Pipe 2)** | Cannot embed third-party apps | LOW - not needed for mobile |
| **SSE is monitor-only (Pipe 5)** | Cannot reuse for app messaging | MEDIUM - parallel infrastructure needed |
| **No auto-heartbeat (Pipe 6)** | Node goes stale without explicit calls | MEDIUM - edge nodes disappear |
| **No sync daemon (Pipe 6)** | Offline writes queue but never flush | HIGH - data loss on mobile |

**Bottom line:** Pipes 1, 3, 5, 6 work. Pipe 7 is the critical gap for Hodeia - mobile needs real push, not 3-second polling. Pipe 4 (WebSocket) would solve both Pipe 4 and Pipe 7 if implemented as a bidirectional channel.

---

*Q33NR diagnostic - 2026-03-20*
*Source task: TASK-COMMS-FLOW-TRACE.md (Q88N)*
