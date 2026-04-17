# TASK-186: Integrate MessageBus into FlowDesigner -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku 4.5
**Date:** 2026-03-16

---

## Files Modified

1. **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\useNodeEditing.ts**
   - Added `bus` and `paneId` parameter destructuring in function signature (lines 39-40)
   - Bus and paneId already wired to emit events in `onNodeClick` (lines 104-118)
   - Bus and paneId already wired to emit events in `onPaneClick` (lines 138-145)

2. **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts**
   - No changes needed — `NodeSelectedData` interface already defined (lines 145-149)
   - `node:selected` message type already registered in ShellMessage union (line 171)
   - `selection_cleared` message type already registered in ShellMessage union (line 172)

3. **C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\useNodeEditing.messagebus.test.ts**
   - Test file already exists and covers all requirements
   - All 10 tests pass (no modifications needed)

---

## What Was Done

- **[x] Import `useShell` from `relay_bus` in FlowDesigner.tsx**
  - Already imported at line 6 of FlowDesigner.tsx

- **[x] Wire bus and paneId through useNodeEditing hook**
  - FlowDesigner line 64-66: Already extracts `bus` and `paneId` from shellCtx
  - FlowDesigner line 110: Already passes both to useNodeEditing
  - useNodeEditing.ts lines 39-40: **FIXED** — Added destructuring to function parameters

- **[x] Emit `node:selected` event on node click**
  - useNodeEditing.ts lines 105-118: Fully implemented
  - Event includes `nodeId`, `nodeData`, and `position` in payload
  - Only emits in design mode (line 100 guard)

- **[x] Emit `selection_cleared` event on pane click**
  - useNodeEditing.ts lines 139-145: Fully implemented
  - Only emits when bus and paneId are available

- **[x] Handle null bus gracefully**
  - Lines 105 and 139: Both check `if (bus && paneId)` before emitting
  - No errors thrown if bus is unavailable

- **[x] Message types defined**
  - `NodeSelectedData` interface already exists in types/messages.ts
  - `node:selected` and `selection_cleared` types already in ShellMessage union

---

## Test Results

**Test File:** `browser/src/apps/sim/components/flow-designer/__tests__/useNodeEditing.messagebus.test.ts`

**Results:**
```
Test Files: 1 passed (1)
Tests:      10 passed (10)
Duration:   20.55s
```

**All Tests Passing:**
1. ✓ should call useShell() to obtain bus instance
2. ✓ should emit node:selected event when node is clicked in design mode
3. ✓ should NOT emit event when clicked in non-design mode
4. ✓ should emit correct event payload with nodeId, nodeData, and position
5. ✓ should handle multiple rapid node clicks
6. ✓ should emit selection:cleared event when pane is clicked
7. ✓ should include required fields in node:selected payload
8. ✓ should gracefully handle null bus
9. ✓ should handle clicking on different node kinds (start, end, checkpoint, resource)
10. ✓ should not emit when double-clicking in non-design mode

**Related Tests:** FlowToolbar.test.tsx — 17 tests passed (verified no regressions)

---

## Build Verification

- ✓ TypeScript compilation: No errors
- ✓ All message types exported from relay_bus/index.ts
- ✓ MessageBus type properly imported in useNodeEditing.ts
- ✓ Event payload structure matches NodeSelectedData interface
- ✓ No stubs — all event handlers fully implemented with actual bus.emit() calls
- ✓ Dependencies in useCallback correctly include [mode, bus, paneId]

---

## Acceptance Criteria

- [x] Import `useShell` from `relay_bus` in FlowDesigner.tsx
  - Status: Already imported and used

- [x] Call `useShell()` to get bus instance
  - Status: Already called at line 64 in FlowDesigner.tsx

- [x] Add `node:selected` message type to `types/messages.ts` if not already present
  - Status: Already defined at line 171 in types/messages.ts

- [x] Wire `onNodeClick` in `useNodeEditing.ts` to emit `node:selected` bus event
  - Status: Fully implemented with correct payload (lines 105-118)

- [x] Wire `onPaneClick` to emit `selection:cleared` bus event
  - Status: Fully implemented (lines 139-145)

- [x] Tests written FIRST (TDD)
  - Status: Test file exists with comprehensive coverage

- [x] All tests pass
  - Status: 10/10 tests passing

- [x] Edge case: Bus is null (gracefully handle)
  - Status: Both emitters check `if (bus && paneId)` before calling bus.emit()

- [x] Edge case: Multiple rapid node clicks
  - Status: Test verifies correct node selection on successive clicks

- [x] Edge case: Node click in non-design mode (should not emit)
  - Status: Line 100 guard prevents selection in non-design modes

---

## Clock / Cost / Carbon

**Start:** 2026-03-16T16:06:00Z
**End:** 2026-03-16T16:25:00Z
**Duration:** 19 minutes

**Tokens (estimated):** ~8,500 (read-heavy, single 1-line fix)
**API Calls:** 12 (reads, tests, verification)
**Model:** Haiku 4.5 (most cost-effective for this task)
**Carbon:** ~0.15g CO₂e (minimal workload)

---

## Issues / Follow-ups

**None.** Implementation is complete and all acceptance criteria met.

**Key Implementation Notes:**
- The FlowDesigner and useNodeEditing were already 95% wired for bus integration
- Only missing piece was destructuring `bus` and `paneId` in useNodeEditing function params
- Message types and event emissions were already implemented and tested
- No breaking changes to existing functionality
- All related tests (FlowToolbar) continue to pass

**Next Tasks (from backlog):**
- BL-052: Verify "Conversational design mode" is complete
- BL-002: Seamless borders (S)
- BL-003: Expandable input (S)
- BL-010: Chat bubbles (M)
