# BL-070: Envelope Handlers Analysis -- NEEDS_CLARIFICATION

**Status:** NEEDS_CLARIFICATION (spec is misdiagnosed)
**Model:** Sonnet (Q88NR regent analysis)
**Date:** 2026-03-17

---

## Findings

I analyzed BL-070 ("Wire envelope handlers") and discovered the spec is based on incomplete information.

### Claimed Issue (from spec)
> "The terminal sends envelopes with route targets but the handlers for to_explorer, to_ir, and to_simulator are not wired. Messages go nowhere or to the wrong pane."

### Actual State

**All three envelope slots ARE wired** in `browser/src/services/terminal/terminalResponseRouter.ts`:

| Envelope Slot | Bus Message | Sender Status | Receiver Status |
|---------------|-------------|---------------|-----------------|
| `to_ir` | `terminal:ir-deposit` | ✅ WIRED (line 184-194) | ✅ WIRED (`CanvasApp.tsx:184`) |
| `to_explorer` | `terminal:explorer-command` | ✅ WIRED (line 172-182) | ❌ NO RECEIVER |
| `to_simulator` | `terminal:simulator-command` | ✅ WIRED (line 196-206) | ❌ NO RECEIVER |

### Evidence

1. **to_ir is fully functional:**
   - Routing: `terminalResponseRouter.ts` lines 184-194 send `terminal:ir-deposit` to bus
   - Receiver: `CanvasApp.tsx` lines 181-198 subscribe and handle IR deposits
   - Tests: 11 passing tests verify delivery (`CanvasApp.test.tsx`, `canvas.integration.test.tsx`)

2. **to_explorer sends but nobody listens:**
   - Routing: `terminalResponseRouter.ts` lines 172-182 send `terminal:explorer-command`
   - Receiver: Grep search found **0 subscribers** in `browser/src/primitives/`
   - Tree-browser adapters do not listen for this message type

3. **to_simulator sends but no pane exists:**
   - Routing: `terminalResponseRouter.ts` lines 196-206 send `terminal:simulator-command`
   - Receiver: No simulation pane exists (grep found 0 matching files)

---

## Root Cause

The spec conflates **routing infrastructure** (which exists) with **receiver handlers** (which are partially missing). The statement "handlers are not wired" is imprecise — the **senders** are wired, but two of three **receivers** don't exist.

---

## Scope Ambiguity

The spec's acceptance criteria:

- [ ] to_explorer envelopes reach tree-browser pane
- [ ] to_ir envelopes reach canvas IR display
- [ ] to_simulator envelopes reach simulation pane

**Issue 1:** `to_ir` is ALREADY COMPLETE. Should this be marked done?

**Issue 2:** "tree-browser pane" is ambiguous. Tree-browser is a generic component used by 9 different adapters:
- filesystemAdapter
- chatHistoryAdapter
- channelsAdapter
- membersAdapter
- paletteAdapter
- propertiesAdapter
- buildStatusMapper
- simPaletteAdapter
- simPropertiesAdapter

Which adapter should handle `terminal:explorer-command`?

**Issue 3:** No simulator pane exists. Building it from scratch is a Medium-sized task (8-16 hrs) requiring design spec for what it displays.

---

## Options for Q88N

### Option A: Wire to_explorer only
- Scope: Add bus subscription to ONE tree-browser adapter (Dave must specify which)
- Mark `to_ir` as already complete
- Defer `to_simulator` to future spec
- **Size:** S (2-4 hours)

### Option B: Build simulator pane
- Scope: Create `SimulationApp.tsx` + wire `terminal:simulator-command`
- **Size:** M (8-16 hours)
- **Blocker:** No design spec for what simulator displays

### Option C: Split into 3 specs
1. BL-070-A: Mark `to_ir` ALREADY_COMPLETE (it's done)
2. BL-071: Wire `terminal:explorer-command` to [Dave specifies which adapter]
3. BL-072: Build simulation pane + wire `terminal:simulator-command`

**Q88NR recommends Option C** for proper scoping.

---

## Decision Required

**Q88N:** Choose Option A, B, or C.

If Option A: specify which tree-browser adapter handles explorer commands.

If Option B: provide design spec for simulator pane.

---

## Files Read

- `browser/src/primitives/terminal/useTerminal.ts`
- `browser/src/services/terminal/terminalResponseRouter.ts`
- `browser/src/services/terminal/index.ts`
- `browser/src/infrastructure/relay_bus/index.ts`
- `browser/src/infrastructure/relay_bus/types/messages.ts`
- `browser/src/primitives/canvas/CanvasApp.tsx`
- `browser/src/primitives/tree-browser/TreeBrowser.tsx`

## Files Modified

None (analysis only)

---

**Next Step:** Q88NR paused. Awaiting Dave's decision on scope.
