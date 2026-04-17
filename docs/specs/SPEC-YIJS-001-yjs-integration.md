# SPEC-YIJS-001: Y.js Integration — Collaborative State Sync

**Date:** 2026-03-13
**Author:** Q88N (Dave) × Claude (Anthropic)
**Status:** SPEC — LOCKED
**Area:** INFRA
**T-Shirt Size:** L
**Depends On:** relay_bus (BUILT), hivenode_api (SPECCED), ledger_writer (BUILT)

---

## 1. Purpose

Y.js is the CRDT (Conflict-free Replicated Data Type) library that provides real-time
collaborative state synchronization across multiple ShiftCenter clients. It is the transport
layer underneath presence_service and canvas_surface for any session with more than one
participant.

Y.js does two things SC needs and cannot easily build:
1. **Shared document state** — canvas model, scaffold config, session metadata — synced
   across all clients with automatic conflict resolution.
2. **Awareness protocol** — ephemeral, non-persisted state (cursors, presence, viewport)
   broadcast in real-time.

Y.js is MIT licensed. The WebSocket provider (`y-websocket`) runs on the hivenode.

---

## 2. Hosting Model

Three tiers, user's choice. EGG config declares which tier the session uses.
The architecture is identical across all three — only the `wsUrl` changes.

| Tier | Who Runs the Sync Server | Cost | #NOKINGS |
|------|--------------------------|------|----------|
| **Self-hosted** | User's own hivenode (`hive up`) | Free | Full sovereignty |
| **DEIA-hosted** | DEIA Solutions managed relay | Paid feature / enterprise | Portable — migrate any time |
| **Peer-to-peer** | WebRTC direct (no server) | Free | Full sovereignty, max 4 participants |

Migration between tiers requires only changing `wsUrl` in the EGG config. No data loss.
No lock-in. This satisfies #NOKINGS while allowing DEIA to monetize convenience.

### Self-Hosted Setup

The hivenode ships with `y-websocket` server pre-configured:

```bash
hive up                          # starts hivenode including Y.js sync server
# Y.js WebSocket available at ws://localhost:1234
```

### DEIA-Hosted

```yaml
# In EGG config
sync:
  provider: yjs
  wsUrl: wss://sync.shiftcenter.com/rooms/{roomId}
  tier: deia-hosted              # requires paid subscription
```

---

## 3. Two Channels: Document vs Awareness

Y.js separates two types of shared state. SC uses both.

### 3.1 Shared Document (Persistent)

The Y.js `Y.Doc` holds all canvas model state that must survive disconnections and be
consistent across clients:

- Canvas node positions and connections (canvas_surface model)
- Scaffold region config and current applet assignments
- Session metadata (survivor order, permission tiers, agenda IR)
- Whiteboard draw.io model (when draw.io is the backdrop)
- Sim-chat message log

This state IS persisted. On reconnect, a client receives the full document state.
Y.js handles conflict resolution automatically via CRDT — no server-side merge logic needed.

**Y.js → Event Ledger bridge:** Every Y.js document mutation also writes to the Event Ledger
via `ledger_writer`. This gives SC the append-only audit trail that Y.js does not provide.
Y.js owns real-time collaborative state. The Ledger owns the immutable history.
They are complementary, not redundant.

```
Y.js Doc mutation
    ↓ (sync to all clients via WebSocket)
    ↓ (also write to Event Ledger via bridge)
Event Ledger (append-only, tamper-evident audit trail)
```

### 3.2 Awareness (Ephemeral)

Y.js Awareness carries state that is session-only and does not need persistence:

- Cursor position (canvasX, canvasY, viewportX, viewportY)
- Presence state (DESKTOP_ACTIVE, MOBILE_BRIDGE, etc.)
- Display name and cursor color
- Current pane focus

Awareness data is NOT written to the Event Ledger. It evaporates when the session ends.
This keeps the Ledger clean — it records decisions and mutations, not mouse movements.

---

## 4. Room Model

Each collaborative session is a Y.js room identified by a `roomId`.

```
roomId = {eggId}:{sessionId}
Example: meeting-room-egg:session-2026-03-13-0900
```

Rooms are created when the first participant connects. They persist in Y.js server memory
until all participants disconnect + a configurable TTL (default: 24h for paid tier, 2h
for self-hosted free tier).

The Y.js document for a room is also snapshotted to the hivenode filesystem (or DEIA storage
on paid tier) at configurable intervals (default: every 5 minutes and on clean session end).
This enables session recovery if the sync server restarts.

---

## 5. Conflict Resolution Strategy

Y.js handles structural conflicts automatically. SC adds one rule on top:

**Owned regions reduce conflicts.** The scaffold service assigns each participant a primary
region of the canvas. Mutations within your own region are always yours — no conflict.
Cross-region mutations (moving someone else's node) are flagged with a visual indicator
(dim highlight for 2s) so participants can see what changed and who changed it.

For the draw.io backdrop specifically: concurrent edits to the same shape are resolved
last-write-wins within a 100ms debounce window. This is acceptable for whiteboarding; it
is not acceptable for IR node editing (where semantic correctness matters). IR editing on
the canvas_surface primitive uses a separate Y.js shared type with stricter merge rules.

---

## 6. relay_bus Integration

Y.js awareness events are bridged to the relay_bus so all SC components can subscribe
without knowing Y.js exists:

```
Y.js Awareness change
    ↓ (Y.js bridge adapter)
relay_bus event (CURSOR_MOVED, PRESENCE_STATE_CHANGED, etc.)
    ↓
AppletShell cursor overlay, HUD, scaffold_service
```

The bridge is a thin adapter. It does not transform events — it re-emits them.
Components always subscribe to relay_bus; they never subscribe to Y.js directly.

---

## 7. EGG Configuration

```yaml
# In EGG frontmatter or config block
sync:
  provider: yjs                  # required for multi-user
  wsUrl: ws://localhost:1234     # self-hosted hivenode default
  roomId: auto                   # auto = {eggId}:{sessionId}
  persistence: true              # snapshot to filesystem
  snapshotIntervalMs: 300000     # 5 minutes
  roomTTLMs: 86400000            # 24h after last disconnect
  awareness: true                # enable cursor/presence sync
  maxParticipants: 50            # hard cap (WebSocket server enforced)
```

Single-user EGGs do not declare `sync`. No Y.js overhead for solo sessions.

---

## 8. Security

- Room access requires a valid ra96it session token (or guest token for OBSERVER tier)
- WebSocket connection authenticated on handshake — unauthenticated connections rejected
- Room IDs are UUIDs — not guessable
- DEIA-hosted rooms: encrypted in transit (WSS), encrypted at rest
- Self-hosted rooms: user's own security posture (their hivenode, their responsibility)

---

## 9. Performance Targets

| Metric | Target |
|--------|--------|
| Cursor update latency (LAN) | < 20ms |
| Cursor update latency (internet) | < 100ms |
| Canvas model sync latency | < 200ms |
| Max participants before degradation | 50 (WebSocket), 4 (WebRTC) |
| Reconnect state recovery time | < 2s |

---

## 10. Implementation Notes for Mr. Code

Primary packages:
- `yjs` — core CRDT library
- `y-websocket` — WebSocket provider (runs on hivenode)
- `y-webrtc` — WebRTC provider (peer-to-peer fallback)
- `lib0` — Y.js utility library (included with yjs)

The Y.js bridge adapter lives at `services/sync/yjsBridge.ts`. It:
1. Initializes `Y.Doc` on session start
2. Connects WebSocket provider to configured `wsUrl`
3. Sets up Awareness with local participant state
4. Subscribes to Y.js document changes → emits to relay_bus
5. Subscribes to relay_bus mutation events → applies to Y.js doc
6. Bridges Awareness changes → relay_bus presence events
7. Writes Y.js doc mutations → Event Ledger via `ledger_writer`

The bridge is the only component that touches Y.js directly. Everything else uses relay_bus.

---

*Signed,*
**Q88N (Dave) × Claude (Anthropic)**
SPEC-YIJS-001 — LOCKED 2026-03-13
License: CC BY 4.0 | Copyright: © 2026 DEIA Solutions

---

## IMPLEMENTATION ADDENDUM — Bus Event Routing (Q33NR, 2026-03-13)

> *This section is an implementation note appended after spec lock. It does not modify the spec.*

Y.js is the **event source layer** — it produces relay_bus events but does not consume SC-level events directly. The yjsBridge adapter is the sole translator.

**Events produced by yjsBridge → consumed by:**

| Event | Consumer | Handler Location |
|-------|----------|-----------------|
| `CURSOR_MOVED` | Presence cursor overlay | `AppletShell` (cursor overlay capability) |
| `PRESENCE_STATE_CHANGED` | Presence service, scaffold, HUD | `services/presence/presenceService.ts` |
| `PRESENCE_JOINED` / `PRESENCE_LEFT` | Presence service, sim-chat (system messages) | `services/presence/presenceService.ts`, sim-chat pane adapter |
| Y.js doc mutations | Event Ledger | `yjsBridge.ts` → `ledger_writer` (direct, not via bus) |

**yjsBridge does NOT handle:** scaffold events, canvas events, sim-chat messages, drawio events. It is upstream of all of them.
