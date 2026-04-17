# Q33N Coordination Report: Properties Panel Canvas Wiring

**From:** Q33N
**To:** Q33NR
**Date:** 2026-03-16
**Spec ID:** 2026-03-16-1501-SPEC-w2-03-properties-canvas-wire
**Status:** TASK FILES READY FOR REVIEW

---

## Summary

Task files for wiring PropertyPanel to FlowDesigner canvas via bus events **already exist**. I discovered during codebase analysis that TASK-186 through TASK-190 were previously created for this exact work.

The existing task files cover all acceptance criteria from the briefing:
- Node selection → bus event emission
- PropertyPanel listening and opening
- Property edits → bus event emission
- FlowDesigner listening and updating canvas
- Canvas deselect → close panel
- E2E integration tests

---

## Existing Task Files (Already Written)

### TASK-186: Integrate MessageBus into FlowDesigner
**File:** `.deia/hive/tasks/2026-03-16-TASK-186-flow-designer-bus-integration.md`

**Deliverables:**
- Import `useShell` from relay_bus in FlowDesigner.tsx
- Wire `onNodeClick` to emit `node:selected` bus event with nodeId, nodeData, position
- Wire `onPaneClick` to emit `selection:cleared` bus event
- Add `node:selected` message type to types/messages.ts
- Tests for bus integration, event emission, graceful null handling

**Status:** NOT YET DISPATCHED

---

### TASK-187: PropertyPanel Listens for node:selected
**File:** `.deia/hive/tasks/2026-03-16-TASK-187-property-panel-bus-listener.md`

**Deliverables:**
- Add `paneId` and `bus` props to PropertyPanel
- Subscribe to `node:selected` bus event
- Convert bus payload to NodeProperties format
- Open panel when event received
- Subscribe to `selection:cleared` and close panel
- Unsubscribe on unmount
- Tests for subscription, opening, closing, payload conversion

**Status:** NOT YET DISPATCHED

---

### TASK-188: PropertyPanel Emits node:property-changed
**File:** `.deia/hive/tasks/2026-03-16-TASK-188-property-panel-emit-changes.md`

**Deliverables:**
- Add `NodePropertyChangedData` interface to types/messages.ts
- Modify PropertyPanel's `handleSave` to emit `node:property-changed` event
- Include nodeId, full properties, and which section changed
- Keep backward compatibility with `onSave` callback
- Tests for event emission, payload structure, backward compat

**Status:** NOT YET DISPATCHED

---

### TASK-189: FlowDesigner Listens for node:property-changed
**File:** `.deia/hive/tasks/2026-03-16-TASK-189-flow-designer-listen-property-changes.md`

**Deliverables:**
- Subscribe to `node:property-changed` event in FlowDesigner/useNodeEditing
- Convert NodeProperties to PhaseNodeData (reuse onPropertySave logic)
- Update nodes state with pushHistory()
- Emit ledger event
- Unsubscribe on unmount
- Tests for subscription, updates, history, ledger, non-existent nodes

**Status:** NOT YET DISPATCHED

---

### TASK-190: E2E Integration Test
**File:** `.deia/hive/tasks/2026-03-16-TASK-190-integration-test-properties-bus.md`

**Deliverables:**
- Create `browser/src/apps/sim/components/flow-designer/__tests__/properties-bus-integration.test.tsx`
- Test complete flow: click → open → edit → update → close
- 8+ integration tests covering:
  - Node click emits event
  - Panel opens with correct data
  - Property edit emits event
  - Canvas updates
  - Background click closes panel
  - Rapid node switches
  - Multiple saves

**Status:** NOT YET DISPATCHED

---

## Codebase Analysis

I read the following files to verify the task breakdown:
- `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx` — main canvas
- `browser/src/apps/sim/components/flow-designer/useNodeEditing.ts` — existing click handlers (lines 92-115)
- `browser/src/apps/sim/components/flow-designer/properties/PropertyPanel.tsx` — accordion panel
- `browser/src/apps/simAdapter.tsx` — shows bus access pattern
- `browser/src/infrastructure/relay_bus/messageBus.ts` — bus API
- `browser/src/infrastructure/relay_bus/types/messages.ts` — message type definitions
- `browser/src/apps/sim/components/flow-designer/properties/GeneralTab.tsx` — property tab structure
- `browser/src/apps/sim/components/flow-designer/properties/TimingTab.tsx` — property tab structure

---

## Task Dependencies

Tasks must be executed **sequentially** (not in parallel) due to dependencies:

1. **TASK-186** (FlowDesigner bus integration) — Must complete first
2. **TASK-187** (PropertyPanel listen) — Depends on TASK-186 message types
3. **TASK-188** (PropertyPanel emit) — Independent of 186/187, can run after 187
4. **TASK-189** (FlowDesigner listen) — Depends on TASK-188 message types
5. **TASK-190** (E2E integration test) — Depends on ALL previous tasks completing

**Dispatch order:** 186 → 187 → 188 → 189 → 190

---

## Acceptance Criteria Mapping

All criteria from briefing spec are covered:

| Criterion | Task |
|-----------|------|
| Clicking node emits `node:selected` | TASK-186 |
| PropertyPanel listens for `node:selected` and opens | TASK-187 |
| Editing property emits `node:property-changed` | TASK-188 |
| FlowDesigner listens for `node:property-changed` and updates | TASK-189 |
| Clicking background closes PropertyPanel | TASK-186, TASK-187 |
| PropertyPanel shows correct tab content | Already implemented, preserved |
| CSS uses `var(--sd-*)` only | All tasks enforce this |
| 5+ tests for selection → edit → update flow | TASK-190 (8+ tests) |
| No file over 500 lines | All tasks enforce this |

---

## Model Assignment

Briefing specified **haiku** for this work. Recommendations:

- **TASK-186:** haiku (bus integration, straightforward)
- **TASK-187:** haiku (subscription logic, straightforward)
- **TASK-188:** haiku (event emission, straightforward)
- **TASK-189:** haiku (reuses existing logic from onPropertySave)
- **TASK-190:** sonnet (complex E2E test scenarios, needs careful edge case handling)

---

## Build Verification Requirements

Each task must:
- POST heartbeats to `http://localhost:8420/build/heartbeat` every 3 minutes
- Claim files via `http://localhost:8420/build/claim` before modifying
- Release claims via `http://localhost:8420/build/release` when done

Final smoke test (after all tasks):
```bash
cd browser && npx vitest run src/apps/sim/components/flow-designer/
```

Expected: All existing tests pass + new tests from TASK-186 to TASK-190.

---

## Next Steps for Q33NR

1. **Review task files** (already written, paths listed above)
2. **Approve dispatch** if task breakdown is correct
3. **Q33N will dispatch** in sequential order: 186 → 187 → 188 → 189 → 190
4. **Q33N will monitor** bee responses and verify each step before next dispatch
5. **Q33N will report** completion to Q33NR with test counts and smoke test results

---

## Questions / Clarifications

None. Task files are complete and ready for review.

---

## Files Referenced

**Task Files:**
- `.deia/hive/tasks/2026-03-16-TASK-186-flow-designer-bus-integration.md`
- `.deia/hive/tasks/2026-03-16-TASK-187-property-panel-bus-listener.md`
- `.deia/hive/tasks/2026-03-16-TASK-188-property-panel-emit-changes.md`
- `.deia/hive/tasks/2026-03-16-TASK-189-flow-designer-listen-property-changes.md`
- `.deia/hive/tasks/2026-03-16-TASK-190-integration-test-properties-bus.md`

**Codebase Files Analyzed:**
- `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx`
- `browser/src/apps/sim/components/flow-designer/useNodeEditing.ts`
- `browser/src/apps/sim/components/flow-designer/properties/PropertyPanel.tsx`
- `browser/src/apps/simAdapter.tsx`
- `browser/src/infrastructure/relay_bus/messageBus.ts`
- `browser/src/infrastructure/relay_bus/types/messages.ts`

---

**Q33N awaits Q33NR approval to dispatch bees.**
