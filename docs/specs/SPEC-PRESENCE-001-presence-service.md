# SPEC-PRESENCE-001: Presence Service

**Date:** 2026-03-13
**Author:** Q88N (Dave) × Claude (Anthropic)
**Status:** SPEC — LOCKED
**Area:** INFRA
**T-Shirt Size:** L
**Depends On:** relay_bus (BUILT), Y.js integration (SPEC-YIJS-001), gate_enforcer (BUILT)

---

## 1. Purpose

The Presence Service is a platform infrastructure service that tracks who is in a shared
session, what their state is, and what permissions they hold. It is the substrate for:

- Collaborative cursor visibility
- Remote admin / support agent takeover
- Meeting host control and survivor election
- Q33NR in-memory simulation observation
- Viewport sync (host snap-to)

Every one of these is a permission-tiered expression of the same underlying event stream.

---

## 2. Presence States

Each participant in a session carries one presence state at a time:

| State | Meaning |
|-------|---------|
| `DESKTOP_ACTIVE` | Participant is on a desktop/laptop, actively engaged |
| `DESKTOP_IDLE` | Participant's session is open but no input for > 60s |
| `MOBILE_BRIDGE` | Participant has handed off to Efemera mobile — voice/chat only |
| `TABLET_ACTIVE` | Participant is on a tablet viewport |
| `OBSERVER` | Read-only participant — can see but not interact |
| `DISCONNECTED` | Connection lost — grace period before removal (30s default) |
| `RECONNECTING` | Briefly disconnected, Y.js syncing state on return |

State transitions emit `PRESENCE_STATE_CHANGED` events on the relay_bus.

---

## 3. Permission Tiers

Every participant holds one permission tier at a time. Tiers are granted by the session owner
or current host. gate_enforcer mediates all tier transitions.

| Tier | Label | Can Do |
|------|-------|--------|
| 0 | `OBSERVER` | See canvas, see cursors, read chat |
| 1 | `PARTICIPANT` | All of tier 0 + type in chat, move own cursor |
| 2 | `ANNOTATE` | All of tier 1 + draw on canvas (canvas-pinned overlays only) |
| 3 | `INTERACT` | All of tier 2 + click UI elements, open panes |
| 4 | `CONTROL` | All of tier 3 + type in any text field, trigger actions |
| 5 | `HOST` | All of tier 4 + viewport sync, agenda control, grant/revoke tiers |
| 6 | `OWNER` | All of tier 5 + end session, set survivor order, hard reclaim |

The session `OWNER` always retains hard reclaim of tier 6 regardless of who holds `HOST`.
Reclaim is instantaneous and requires no approval.

---

## 4. Host Model

### 4.1 Roles

- **Owner:** Created the session. Tier 6 always. Can reclaim HOST at any time.
- **Host:** Currently holds Tier 5. Controls viewport sync, agenda, participant tiers.
- **Designated Survivor:** Named by Owner in session config. Auto-receives HOST if current
  host drops.
- **Implicit Survivor:** Fallback if no designee is online — longest-connected PARTICIPANT.

### 4.2 Host Drop Protocol

```
1. Host presence state → DISCONNECTED
2. Grace period: 30 seconds (configurable per session)
3. If host reconnects within grace: HOST restored automatically
4. If grace expires:
   a. Check designee list (ordered) — first online designee receives HOST
   b. If no designee online — implicit survivor (longest-connected) receives HOST
   c. If no participants online — session enters LEADERLESS state
```

### 4.3 Leaderless State

When no eligible host exists:
- Canvas goes read-only (no model mutations accepted)
- Chat remains active
- Viewport sync suspended
- First eligible participant to connect receives HOST automatically
- All participants notified via sim-chat system message

### 4.4 "Continue Without Me" — Mobile Bridge

When a host transitions to `MOBILE_BRIDGE`:
1. Host explicitly delegates HOST to a designee or implicit survivor
2. Host's presence indicator shows phone icon in HUD
3. Host's canvas cursor disappears (not visible on mobile)
4. Host's chat messages tagged with mic icon (voice-sourced via STT)
5. TTS reads incoming chat to host
6. Host retains OWNER tier — can reclaim HOST at any time

---

## 5. Cursor Protocol

### 5.1 Cursor Events

Each participant's cursor position emits on the relay_bus at max 30fps (throttled):

```json
{
  "type": "CURSOR_MOVED",
  "participantId": "ra96it-uuid",
  "displayName": "Dave",
  "color": "#8B5CF6",
  "canvasX": 4500,
  "canvasY": 2200,
  "viewportX": 320,
  "viewportY": 180,
  "paneId": "whiteboard-canvas",
  "timestamp": 1710000000000
}
```

`canvasX/Y` = position in infinite canvas coordinate space.
`viewportX/Y` = position in participant's current viewport (for observers to render correctly).

### 5.2 Cursor Rendering

Cursors render on a transparent overlay layer above all panes. They are viewport-pinned
relative to each observer's own scroll position — meaning: if participant A is at canvas
(4500, 2200) and observer B is scrolled to show that region, they see A's cursor there.
If observer B is scrolled away, A's cursor is off-screen (minimap shows a dot).

Cursor overlay is an AppletShell capability, not a pane primitive. Any pane can opt in via
`showPresenceCursors: true` in EGG config.

---

## 6. Viewport Sync

Host emits `VIEWPORT_SYNC` to align all participants to a canvas region:

```json
{
  "type": "VIEWPORT_SYNC",
  "sourceParticipantId": "host-uuid",
  "targetCanvasX": 2000,
  "targetCanvasY": 1500,
  "zoom": 1.0,
  "animationMs": 600,
  "breakable": true
}
```

`breakable: true` means participants can scroll away after sync (default).
`breakable: false` means participants are locked to host viewport until released. Use
sparingly — only for structured demos or presentations.

Viewport sync does NOT steal focus from active text inputs. Canvas scrolls; glass stays stable.

---

## 7. Bus Events Summary

### Emitted

| Event | When |
|-------|------|
| `PRESENCE_JOINED` | Participant connects |
| `PRESENCE_LEFT` | Participant disconnects (after grace) |
| `PRESENCE_STATE_CHANGED` | Any state transition |
| `PRESENCE_TIER_CHANGED` | Permission tier granted or revoked |
| `CURSOR_MOVED` | Cursor position update (30fps max) |
| `HOST_CHANGED` | HOST role transferred |
| `SESSION_LEADERLESS` | No host online |
| `VIEWPORT_SYNC` | Host snap-to broadcast |
| `MOBILE_BRIDGE_ENTERED` | Host → mobile handoff |

### Consumed

| Event | Source | Effect |
|-------|--------|--------|
| `SESSION_END` | Owner | Triggers graceful teardown, meeting summary |
| `TIER_GRANT_REQUEST` | Any participant | Routed to HOST for approval |
| `SURVIVOR_ORDER_SET` | Owner | Updates designee list in Y.js shared doc |

---

## 8. Transport

Presence events require real-time bidirectional transport. The relay_bus handles in-process
pub/sub; presence adds a network layer via Y.js Awareness Protocol (built into Y.js).

Y.js Awareness carries ephemeral state (cursor position, presence state, display name, color)
separately from the persistent document state. Awareness data is not persisted to the Event
Ledger — it is session-only. Model mutations (canvas changes) ARE persisted.

See SPEC-YIJS-001 for transport configuration.

---

## 9. Integration with IR

Presence state changes are IR-triggerable conditions. The following presence events can be
used as IR `trigger` conditions:

```yaml
trigger:
  type: presence
  event: HOST_CHANGED
  condition: "new_host.id == designee_list[0]"
```

```yaml
trigger:
  type: presence
  event: PRESENCE_STATE_CHANGED
  condition: "participant.state == 'DISCONNECTED' AND participant.tier == 'HOST'"
```

This enables meeting agenda IR to react to participant events without hardcoded platform logic.
The meeting bot executes the process; presence events are just another input stream.

---

## 10. Open Items — PARTIALLY RESOLVED

| # | Question | Decision (Q88N, 2026-03-13) |
|---|----------|-----------------------------|
| 1 | Grace period default: 30s for host drop. Right? Configurable? | **Yes, 30s.** Standard for "user closed laptop lid" detection. |
| 2 | `breakable: false` viewport lock — require participant consent or host authority? | Still open — no decision recorded. |
| 3 | Cursor color assignment: auto-assigned from palette, or ra96it profile color? | **Auto-assigned from a palette on join, with ra96it profile color as override if the user set one.** Auto-assign first, profile override later. |
| 4 | Guest participants (no ra96it identity) — allowed at what tier maximum? | Still open — no decision recorded. |

---

*Signed,*
**Q88N (Dave) × Claude (Anthropic)**
SPEC-PRESENCE-001 — LOCKED 2026-03-13
License: CC BY 4.0 | Copyright: © 2026 DEIA Solutions

---

## IMPLEMENTATION ADDENDUM — Bus Event Routing (Q33NR, 2026-03-13)

> *This section is an implementation note appended after spec lock. It does not modify the spec.*

Presence events are **consumed across multiple layers**. Routing map:

| Emitted Event | Consumers | Handler Location |
|---------------|-----------|-----------------|
| `PRESENCE_JOINED` | sim-chat (system message), IR engine (presence triggers), scaffold (participant count HUD) | sim-chat pane adapter, `services/ir/triggerEvaluator.ts`, scaffold HUD |
| `PRESENCE_LEFT` | sim-chat (system message), IR engine | sim-chat pane adapter, `services/ir/triggerEvaluator.ts` |
| `PRESENCE_STATE_CHANGED` | IR engine, scaffold (mobile reflow) | `services/ir/triggerEvaluator.ts`, `services/scaffold/scaffoldService.ts` |
| `HOST_CHANGED` | IR engine, sim-chat (bot announcement), scaffold (host HUD) | `services/ir/triggerEvaluator.ts`, sim-chat pane adapter, scaffold HUD |
| `SESSION_LEADERLESS` | IR engine, canvas (read-only mode), sim-chat | `services/ir/triggerEvaluator.ts`, canvas_surface, sim-chat pane adapter |
| `CURSOR_MOVED` | AppletShell cursor overlay (30fps throttled) | `AppletShell` cursor overlay capability |
| `VIEWPORT_SYNC` | canvas_surface (animate viewport) | `services/canvas/canvasSurface.ts` |
| `MOBILE_BRIDGE_ENTERED` | IR engine, sim-chat (TTS mode) | `services/ir/triggerEvaluator.ts`, sim-chat pane adapter |

**Consumed events (from other systems):**

| Consumed Event | Source | Handler |
|----------------|--------|---------|
| `SESSION_END` | Owner action | Presence service teardown |
| `TIER_GRANT_REQUEST` | Any participant | Routed to HOST via presence service |
| `SURVIVOR_ORDER_SET` | Owner | Updates Y.js Awareness via yjsBridge |
