# BRIEFING: BL-070 — Wire envelope handlers

**Date:** 2026-03-17
**From:** Q88NR (Regent)
**To:** Q33N (Coordinator)
**Subject:** Spec analysis and scope clarification needed

---

## Spec Summary

**BL-070** requests wiring envelope routing handlers so terminal commands with route targets (`to_explorer`, `to_ir`, `to_simulator`) deliver payloads to the correct pane primitives.

---

## Current State Analysis

I read the codebase and found:

### 1. Routing Infrastructure EXISTS ✅

**File:** `browser/src/services/terminal/terminalResponseRouter.ts`

All three envelope slots ARE wired in `routeEnvelope()`:

```typescript
// Line 172-182: to_explorer
if (envelope.to_explorer) {
  bus.send({
    type: 'terminal:explorer-command',
    sourcePane: fromPaneId,
    target: resolveTarget('to_explorer', paneRegistry) || '*',
    nonce: `${Date.now()}-${Math.random()}`,
    timestamp: new Date().toISOString(),
    data: envelope.to_explorer,
  });
}

// Line 184-194: to_ir
if (envelope.to_ir && Object.keys(envelope.to_ir).length > 0) {
  bus.send({
    type: 'terminal:ir-deposit',
    sourcePane: fromPaneId,
    target: resolveTarget('to_ir', paneRegistry) || '*',
    nonce: `${Date.now()}-${Math.random()}`,
    timestamp: new Date().toISOString(),
    data: envelope.to_ir,
  });
}

// Line 196-206: to_simulator
if (envelope.to_simulator) {
  bus.send({
    type: 'terminal:simulator-command',
    sourcePane: fromPaneId,
    target: resolveTarget('to_simulator', paneRegistry) || '*',
    nonce: `${Date.now()}-${Math.random()}`,
    timestamp: new Date().toISOString(),
    data: envelope.to_simulator,
  });
}
```

### 2. Receiver Status

| Envelope Slot | Bus Message Type | Receiver Status |
|---------------|-----------------|-----------------|
| `to_ir` | `terminal:ir-deposit` | ✅ **WIRED** — `CanvasApp.tsx` line 184 subscribes and handles IR deposits |
| `to_explorer` | `terminal:explorer-command` | ❌ **NO RECEIVER** — No pane subscribes to this message type |
| `to_simulator` | `terminal:simulator-command` | ❌ **NO RECEIVER** — No simulator pane exists yet |

**Evidence for to_ir:**
- `CanvasApp.tsx` lines 181-198: subscribes to bus messages, detects IR flow by shape (`d.nodes`), calls `loadIRFlow()`
- 11 passing tests in `CanvasApp.test.tsx` and `canvas.integration.test.tsx` verify `terminal:ir-deposit` delivery

**Evidence for to_explorer:**
- Grep search found **0 receivers** for `terminal:explorer-command` in `browser/src/primitives/`
- Tree-browser adapters (filesystemAdapter, chatHistoryAdapter, etc.) do not subscribe to this message type

**Evidence for to_simulator:**
- Grep search found **0 files** matching `*[Ss]imulation*` or `*[Ss]imulator*` in `browser/src/primitives/`
- No simulation pane exists yet

---

## Spec Diagnosis

**SPEC IS MISDIAGNOSED.** The statement "handlers for to_explorer, to_ir, and to_simulator are not wired" is incorrect.

**Actual state:**
- ✅ `to_ir` is FULLY WIRED (sender + receiver)
- ❌ `to_explorer` sender exists, receiver missing
- ❌ `to_simulator` sender exists, receiver missing (no pane exists)

---

## Scope Clarification Needed

Q88NR requires Dave's decision on scope before proceeding:

### Option A: Wire to_explorer only (small scope)
- Identify which tree-browser adapter should handle explorer commands
- Add bus subscription + handler to that adapter
- Write tests
- Skip `to_simulator` (defer to future spec)
- **Effort:** 2-4 hours (S)

### Option B: Build simulator pane (large scope)
- Create `browser/src/primitives/simulation/SimulationApp.tsx`
- Implement bus listener for `terminal:simulator-command`
- Define simulation data schema and rendering
- Write tests
- **Effort:** 8-16 hours (M-L)
- **Risk:** No design spec for simulator pane

### Option C: Mark BL-070 as ALREADY_COMPLETE
- Document that `to_ir` is already wired
- Split `to_explorer` and `to_simulator` into separate specs (BL-XXX and BL-YYY)
- Allows proper scoping and prioritization

---

## Recommended Action

**Q88NR recommends Option C:**

1. Mark BL-070 as ALREADY_COMPLETE (for `to_ir`)
2. Create **BL-071: Wire terminal:explorer-command receiver**
   - Scope: Add bus listener to filesystemAdapter or create ExplorerApp wrapper
   - Priority: P1
   - Size: S
3. Create **BL-072: Build simulation pane + wire terminal:simulator-command**
   - Scope: Full simulation pane primitive
   - Priority: P2
   - Size: M
   - Requires: Design spec for what simulator displays

This approach:
- ✅ Recognizes work already done (to_ir)
- ✅ Properly scopes remaining work
- ✅ Allows independent prioritization
- ✅ Avoids building simulator without design spec

---

## Decision Required

**Q88N (Dave):** Choose Option A, B, or C.

If Option A: specify which tree-browser adapter should handle `terminal:explorer-command`.

If Option B: provide design spec for simulator pane.

If Option C: approve split into BL-071 and BL-072.

---

**Status:** AWAITING_DAVE_DECISION
**Next Action:** Q88NR will proceed once Dave responds
