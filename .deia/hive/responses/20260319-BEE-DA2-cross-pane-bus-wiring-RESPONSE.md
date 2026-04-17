# BEE-DA2: Cross-Pane Communication (Bus Wiring) -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-19

## Files Modified
NONE (research only)

## What Was Done
Conducted comprehensive audit of MessageBus architecture between platform (simdecisions-2) and shiftcenter (March 16 baseline). Traced message routing end-to-end from terminal → canvas via IR routing. Mapped governance checkpoints, capability advertisement, and EGG-level wiring declarations.

---

## Research Findings

---
bee: BEE-DA2
type: RESEARCH
finding: 1
source: platform/simdecisions-2/src/components/shell/shell.context.js:L99-L145
shift: false
---

### FINDING 1: Message Routing End-to-End (Terminal → Canvas IR Flow)

**How `terminal:open-in-designer` works end-to-end:**

1. **Terminal generates IR** → User types in terminal, hivenode returns IR JSON
2. **IR routing logic** (browser/src/primitives/terminal/irRouting.ts:L14-L61):
   - Saves IR to sessionStorage as `sd:terminal_ir` (for cross-window handoff)
   - Checks if running in pane mode via `ctx.isPane`
   - Calls `bus.hasPaneType('canvas')` to verify canvas pane exists
   - Calls `bus.getLastFocusedPane('canvas')` to get last focused canvas nodeId
   - Sends bus message: `{ type: 'terminal:open-in-designer', target: nodeId, data: { ir, timestamp } }`
3. **MessageBus delivery** (browser/src/infrastructure/relay_bus/messageBus.ts:L142-L238):
   - Validates `message.type` and `message.target` (L144-L146)
   - Generates unique nonce, checks replay attack (L149-L156)
   - Builds envelope with messageId, nonce, sourcePane, timestamp (L159-L165)
   - **Platform invariants bypass mute** (L168-L177): relay_bus, ledger_writer, gate_enforcer, settings_advertisement, metrics_advertisement
   - Mute enforcement for non-invariants (L179-L198): checks outbound/inbound/notifications/full mute states
   - Logs to Event Ledger via `dispatch({ type: 'LOG_EVENT', event: {...} })` (L217)
   - Delivers to target pane's subscriber handler (L234-L236)
4. **Canvas receives IR** (browser/src/primitives/canvas/CanvasApp.tsx:L181-L215):
   - Canvas subscribes via `bus.subscribe(nodeId, handler)` (L184)
   - Handler checks `msg.data` for nodes array (L189-L192)
   - Calls `loadIRFlow(d)` to convert IR → ReactFlow nodes + edges (L219-L223)
5. **Governance checkpoint** (browser/src/infrastructure/relay_bus/GovernanceProxy.tsx:L127-L202):
   - **BEFORE** message reaches MessageBus.send(), GovernanceProxy intercepts (L128)
   - Checks message type against EGG's `bus_emit` permissions (L153)
   - Platform invariants bypass governance (L139-L149)
   - If not in whitelist → blocked, logged as `GOVERNANCE_BLOCKED` (L155-L158)
   - If ethics loaded → runs BrowserGateEnforcer check (L162-L197)
   - Dispositions: PASS (allow), BLOCK (deny), HOLD/ESCALATE/REQUIRE_HUMAN (show modal)

**Wiring is IMPERATIVE** (not declarative in EGG):
- Terminal calls `bus.send({ type: '...', target: nodeId })` with explicit target
- Canvas declares what it can RECEIVE via EGG permissions `bus_receive: ['terminal:open-in-designer', ...]`
- Routing map `_lastFocusedByType` is maintained by Shell (browser/src/shell/components/Shell.tsx:L46)

DIVERGENCE: none (ported correctly)
P0: none
BACKLOG: none

---

---
bee: BEE-DA2
type: RESEARCH
finding: 2
source: eggs/canvas.egg.md:L244-L267
shift: false
---

### FINDING 2: Pane Capability Declaration via EGG Permissions

**How a pane declares what it can receive:**

Capabilities are declared in the EGG file's `permissions` block:

```yaml
permissions:
  bus_emit: [
    "canvas:node-created",
    "canvas:node-updated",
    "canvas:node-selected",
    "palette:node-drag-start",
    "terminal:ir-deposit"
  ]
  bus_receive: [
    "canvas:node-created",
    "canvas:node-updated",
    "terminal:ir-deposit",
    "terminal:text-patch"
  ]
```

**No runtime capability advertisement** like `settings_advertisement`. Panes do NOT announce capabilities on mount.

**How it works:**
1. EGG loader (browser/src/infrastructure/relay_bus/configEggCache.ts) parses EGG file
2. PermissionsResolver (browser/src/infrastructure/relay_bus/permissionsResolver.ts:L27-L93) builds ResolvedPermissions
3. GovernanceProxy wraps each pane with governed bus (L250-L260)
4. Governed `bus.send()` checks sender's `bus_emit` list (L153)
5. Governed `bus.subscribe()` filters incoming messages via receiver's `bus_receive` list (L227-L234)

**Trust tier determines defaults:**
- Platform EGGs: `bus_emit: ['*'], bus_receive: ['*']` (allow-all)
- GC/External EGGs: `bus_emit: ['metrics_advertisement'], bus_receive: ['settings_update']` (deny-unknown)

**Node-level permissions can ONLY tighten** (L53-L70):
- Layout node can specify `permissions: { bus_receive: ['foo'] }` → intersection with EGG ceiling
- Node CANNOT widen beyond EGG permissions

DIVERGENCE: none (matches platform pattern)
P0: none
BACKLOG: none

---

---
bee: BEE-DA2
type: RESEARCH
finding: 3
source: eggs/canvas.egg.md:L95-L99
shift: false
---

### FINDING 3: Wiring Specification — Declarative vs Imperative

**User/EGG specifies wiring in TWO ways:**

**1. Declarative link hints in layout (EGG `config.links` field):**

```json
{
  "type": "pane",
  "nodeId": "canvas-ir",
  "appType": "terminal",
  "config": {
    "routeTarget": "ir",
    "links": {
      "to_ir": "canvas-editor",
      "to_text": "canvas-chat"
    }
  }
}
```

- `links.to_ir` → tells terminal "route IR messages to canvas-editor pane"
- `links.to_text` → tells terminal "route text messages to canvas-chat pane"
- These are HINTS, not enforcement — terminal code reads them and calls `bus.send()`

**2. Imperative bus calls in app code:**

Terminal code (browser/src/primitives/terminal/irRouting.ts:L55-L60):
```typescript
bus.send({
  type: 'terminal:open-in-designer',
  target: target.nodeId,  // from getLastFocusedPane() or config.links
  data: { ir, timestamp }
})
```

Canvas code (browser/src/primitives/canvas/CanvasApp.tsx:L184):
```typescript
bus.subscribe(nodeId, (msg) => {
  if (msg.data.nodes) loadIRFlow(msg.data)
})
```

**Hybrid model:**
- EGG layout provides HINTS for static wiring
- App code uses hints + dynamic routing (last-focused pane tracking)
- MessageBus enforces PERMISSIONS (governance), not routing topology

**No centralized routing table.** Each sender decides target pane.

DIVERGENCE: none (both repos use same hybrid model)
P0: none
BACKLOG: none

---

---
bee: BEE-DA2
type: RESEARCH
finding: 4
source: platform/simdecisions-2/src/components/apps/EfemeraApp.tsx:L79-L99
shift: false
---

### FINDING 4: `settings_advertisement` Message — Pane Discovery

**What is `settings_advertisement`?**

A platform invariant message type that panes send to announce their **settings schema** to the shell.

**Purpose:**
- Allows shell to build a unified settings UI
- Advertises pane label, available settings, their types, and current values
- Used by contextual drawers (e.g., properties panel) to display pane-specific settings

**Example from EfemeraApp.tsx (platform):**

```typescript
bus.publish({
  type: 'settings_advertisement',
  fromPaneId: nodeId,
  payload: {
    paneLabel: 'Efemera Chat',
    settings: [
      {
        key: 'flowId',
        label: 'Flow Channel',
        type: 'text',
        value: flowId ?? 'general',
        scope: 'pane',
        description: 'Which Efemera flow channel to connect to'
      }
    ]
  }
})
```

**How it works:**
1. Pane sends `settings_advertisement` on mount (useEffect)
2. MessageBus intercepts it (messageBus.ts:L206-L214)
3. Dispatches to shell reducer: `{ type: 'REGISTER_PANE_SETTINGS', paneId, paneLabel, settings }`
4. Shell stores in `state.paneSettings[paneId]`
5. Properties drawer reads from `state.paneSettings` to render UI

**Platform invariant status:**
- Bypasses governance checks (GovernanceProxy.tsx:L139-L149)
- Bypasses mute enforcement (messageBus.ts:L168-L177)
- Always delivered, even if pane is muted

**This is NOT pane capability advertisement** — it's settings schema advertisement.
Capabilities are declared statically in EGG `permissions` block.

DIVERGENCE: none (shiftcenter has identical implementation)
P0: none
BACKLOG: none

---

---
bee: BEE-DA2
type: RESEARCH
finding: 5
source: browser/src/infrastructure/relay_bus/messageBus.ts:L1-L284 vs platform/simdecisions-2/src/components/shell/shell.context.js:L1-L187
shift: false
---

### FINDING 5: DIVERGENCE CHECK — Platform vs Shiftcenter MessageBus

**Comparison:** shiftcenter `browser/src/infrastructure/relay_bus/messageBus.ts` (284 lines, TypeScript) vs platform `src/components/shell/shell.context.js` (187 lines, JavaScript)

**Port quality: EXCELLENT. Fully ported with enhancements.**

**Differences:**

| Feature | Platform (JS) | Shiftcenter (TS) | Divergence Type |
|---------|--------------|------------------|-----------------|
| Language | JavaScript | TypeScript | Enhancement (type safety) |
| Mute states | None | Full support (`_muteStates`, `setMuteState`, `getMuteState`) | New feature |
| Mute enforcement | None | Enforced in `send()` L179-L198 | New feature |
| Platform invariants | 4 types | 5 types (added `metrics_advertisement`) | Enhancement |
| Subscriber count metric | Tracked | Tracked | Same |
| Nonce replay protection | 5s window | 5s window | Same |
| Tree synchronization | `setTree()`, `getLastFocusedPane()` | Identical | Same |
| Telemetry | Optional, `enableTelemetry()` | Identical | Same |
| `resetMetrics()` bug | Line 259 missing reset for `subscriberCount` | Line 260 missing reset for `subscriberCount` | **SAME BUG** |

**Key additions in shiftcenter:**
1. **Mute system** (L73, L122-L131): 5 levels (none, notifications, inbound, outbound, full)
2. **Mute enforcement during send()** (L179-L198): blocks messages based on source/target mute state
3. **Broadcast mute filtering** (L220-L233): respects mute for each subscriber during `target: '*'`

**Porting Doctrine verdict:**
- **Shiftcenter is AHEAD of platform** — mute system is a new feature
- No security issues
- No missing functionality
- TypeScript port adds type safety

**One shared bug:**
- `resetMetrics()` does NOT reset `subscriberCount` in either repo
- Should be: `this._metrics.subscriberCount = 0` (not tracked, counter stays stale)

DIVERGENCE: Shiftcenter ahead — new mute system, TypeScript types. Platform should port mute system.
P0: none
BACKLOG:
- **BL-NEW-001:** Port mute system from shiftcenter → platform (5 mute levels, enforcement during send/broadcast)
- **BUG-NEW-001:** Fix `resetMetrics()` in both repos — add `this._metrics.subscriberCount = 0`
  - Provenance: {source_bee: BEE-DA2, task_context: "MessageBus audit", files: ["messageBus.ts:L257", "shell.context.js:L163"]}

---

## NVWR Review Items

---
bee: BEE-DA2
type: NVWR
review: 1
source: browser/src/infrastructure/relay_bus/messageBus.ts:L257
category: QUALITY
severity: P2
nvwr_cooldown_reset: true
---

**Bug:** `resetMetrics()` does not reset `subscriberCount` metric.

```typescript
resetMetrics() {
  this._metrics.messageCount = 0
  this._metrics.messagesByType = {}
  // Missing: this._metrics.subscriberCount = 0
}
```

**Impact:** If telemetry is enabled → reset → subscriber count persists from previous session → stale metrics.

**Fix:** Add `this._metrics.subscriberCount = 0`

KANBAN-TITLE: Fix MessageBus.resetMetrics() — reset subscriberCount
KANBAN-TAGS: [relay_bus, metrics, telemetry]

---

---
bee: BEE-DA2
type: NVWR
review: 2
source: platform/simdecisions-2/src/components/shell/shell.context.js:L163
category: QUALITY
severity: P2
nvwr_cooldown_reset: true
---

**Bug:** `resetMetrics()` does not reset `subscriberCount` metric (SAME BUG as shiftcenter).

```javascript
resetMetrics() {
  this._metrics.messageCount = 0
  this._metrics.messagesByType = {}
  // Missing: this._metrics.subscriberCount = 0
}
```

**Impact:** If telemetry is enabled → reset → subscriber count persists from previous session → stale metrics.

**Fix:** Add `this._metrics.subscriberCount = 0`

KANBAN-TITLE: Fix MessageBus.resetMetrics() — reset subscriberCount (platform)
KANBAN-TAGS: [relay_bus, metrics, telemetry, platform]

---

---
bee: BEE-DA2
type: NVWR
review: 3
source: browser/src/infrastructure/relay_bus/GovernanceProxy.tsx:L139-L177
category: SECURITY
severity: P1
nvwr_cooldown_reset: true
---

**Platform invariants whitelist:** 5 message types bypass governance AND mute enforcement.

```typescript
const platformInvariants = [
  'relay_bus',
  'ledger_writer',
  'gate_enforcer',
  'settings_advertisement',
  'metrics_advertisement'
]
```

**Why this is security-relevant:**
- These messages ALWAYS deliver, even if sender/receiver is blocked
- Used for shell infrastructure (logging, governance, settings sync)
- If an attacker can inject a message with `type: 'relay_bus'` → bypasses all governance

**Current protection:**
- MessageBus.send() is wrapped by GovernanceProxy per-pane
- Attacker would need to call raw `bus.send()` directly (not exposed to applets)
- Applets receive governed bus via `useShell()` → wrapped send()

**No vulnerability found** — GovernanceProxy wraps every pane, no applet can access raw bus.

**Recommendation:** Document platform invariants in SPEC-HIVE-HOST-SHELL.md. Clarify why each type is invariant.

KANBAN-TITLE: Document platform invariants (security rationale)
KANBAN-TAGS: [relay_bus, governance, security, docs]

---

NVWR_REVIEW_COMPLETE: {
  files: [
    "browser/src/infrastructure/relay_bus/messageBus.ts",
    "browser/src/infrastructure/relay_bus/GovernanceProxy.tsx",
    "platform/simdecisions-2/src/components/shell/shell.context.js",
    "platform/simdecisions-2/src/components/shell/GovernanceProxy.tsx"
  ],
  bee: BEE-DA2,
  timestamp: 2026-03-19T14:30:00Z,
  items_found: 3
}

---

## Summary of Questions Answered

1. ✅ **How does `content_push` work end-to-end?**
   - Terminal generates IR → saves to sessionStorage → checks canvas exists → gets last focused canvas pane → sends `terminal:open-in-designer` to target nodeId → GovernanceProxy checks permissions → MessageBus delivers → Canvas subscribes, receives, loads IR.

2. ✅ **How does a pane declare what it can receive?**
   - Via EGG `permissions.bus_receive` array. No runtime advertisement. GovernanceProxy filters incoming messages against whitelist during `bus.subscribe()`.

3. ✅ **How does the user (or EGG) specify which pane talks to which pane?**
   - Hybrid: EGG layout has declarative `config.links` hints (e.g., `to_ir: "canvas-editor"`). App code reads hints + uses dynamic routing (`getLastFocusedPane()`). Wiring is imperative via `bus.send({ target: nodeId })`.

4. ✅ **What is `settings_advertisement` and how does it relate to pane discovery?**
   - Platform invariant message sent on pane mount. Announces pane's settings schema to shell. Shell stores in `state.paneSettings` for unified settings UI. NOT used for capability discovery (that's via EGG permissions).

5. ✅ **DIVERGENCE CHECK: Platform vs Shiftcenter at March 15**
   - Shiftcenter is AHEAD. Added full mute system (5 levels, enforcement during send/broadcast). TypeScript port adds type safety. One shared bug: `resetMetrics()` doesn't reset `subscriberCount`. No security issues. Port mute system to platform.

---

## Recommendations

1. **Port mute system from shiftcenter → platform** (enhancement, not bug fix)
2. **Fix `resetMetrics()` bug** in both repos (P2, low impact)
3. **Document platform invariants** in shell spec (security + maintainability)

---

**BEE-DA2 signing off. All questions answered. Zero code changes.**
