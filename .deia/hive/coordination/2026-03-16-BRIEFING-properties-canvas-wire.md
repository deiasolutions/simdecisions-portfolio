# BRIEFING: Wire Properties Panel to Canvas Node Selection

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-16
**Model Assignment:** haiku
**Spec ID:** 2026-03-16-1501-SPEC-w2-03-properties-canvas-wire

---

## Objective

Wire the existing PropertyPanel component to FlowDesigner canvas via bus events:
- Node selection on canvas → opens PropertyPanel
- Property edits in PropertyPanel → updates canvas node in real-time
- Canvas deselect → closes PropertyPanel

Both components are already ported. This is pure event wiring.

---

## Context from Q88N

This is part of Wave 2 wiring tasks. The PropertyPanel and FlowDesigner canvas both exist. They need bus event integration so clicking a node opens the properties panel and editing properties updates the node visually.

---

## Files Q33N Must Read Before Writing Tasks

### Core Components
- `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx` (lines 302-358: onDrop handler)
- `browser/src/apps/sim/components/flow-designer/properties/PropertyPanel.tsx`
- `browser/src/apps/sim/components/flow-designer/useNodeEditing.ts` (line 159: emits node_properties_saved)
- `browser/src/apps/sim/components/flow-designer/properties/GeneralTab.tsx`
- `browser/src/apps/sim/components/flow-designer/properties/TimingTab.tsx`

### Bus System
- `browser/src/infrastructure/relay_bus/` (bus event system)

---

## Acceptance Criteria (from spec)

- [ ] Clicking a node on canvas emits `node:selected` bus event with node data
- [ ] PropertyPanel listens for `node:selected` and opens with the selected node's properties
- [ ] Editing a property in PropertyPanel emits `node:property-changed` bus event
- [ ] FlowDesigner listens for `node:property-changed` and updates the canvas node in real-time
- [ ] Clicking canvas background (deselect) closes PropertyPanel
- [ ] PropertyPanel shows correct tab content for different node types (source, activity, gateway, etc.)
- [ ] CSS uses `var(--sd-*)` only
- [ ] 5+ tests for selection → edit → update flow
- [ ] No file over 500 lines

---

## Constraints

- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: `var(--sd-*)` only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  ```json
  {"task_id": "2026-03-16-1501-SPEC-w2-03-properties-canvas-wire", "status": "running", "model": "haiku", "message": "working"}
  ```
- File claims via http://localhost:8420/build/claim before modifying files
- Release claims early via http://localhost:8420/build/release

---

## Task Requirements

Q33N must create task files that:

1. **Break work into bee-sized units** (ideally 1-2 files per task)
2. **Specify absolute file paths** for all deliverables
3. **Include test requirements** with specific scenarios
4. **Verify bus event schema** (what properties are in `node:selected`? what's in `node:property-changed`?)
5. **Ensure no stubs** — all event handlers fully implemented
6. **Check line counts** — no file over 500 lines
7. **Use 8-section response template** from BOOT.md

---

## Expected Task Breakdown (suggestion, not mandate)

Q33N should read the codebase first, but likely needs:

- **TASK-186:** Wire FlowDesigner node click to emit `node:selected` bus event + tests
- **TASK-187:** Wire PropertyPanel to listen for `node:selected` and open with node data + tests
- **TASK-188:** Wire PropertyPanel edits to emit `node:property-changed` bus event + tests
- **TASK-189:** Wire FlowDesigner to listen for `node:property-changed` and update canvas + tests
- **TASK-190:** Wire canvas background click to close PropertyPanel + tests
- **TASK-191:** E2E integration test (click node → edit property → verify canvas updates)

---

## Smoke Test

After all tasks complete:
- Click node → PropertyPanel opens with node data
- Edit property → canvas node updates immediately
- Click background → PropertyPanel closes
- `cd browser && npx vitest run src/apps/sim/components/flow-designer/`
- No new test failures

---

## Next Steps for Q33N

1. Read all files listed in "Files Q33N Must Read Before Writing Tasks"
2. Understand current bus event structure
3. Write task files to `.deia/hive/tasks/`
4. Return task file summary to Q33NR for review
5. **DO NOT dispatch bees yet** — wait for Q33NR approval

---

**Q33NR will review your task files before you dispatch bees.**
