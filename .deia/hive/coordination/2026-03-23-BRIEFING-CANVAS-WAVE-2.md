# BRIEFING: Canvas Full Port — Wave 2 Dispatch

**Date:** 2026-03-23
**From:** Q33NR
**To:** Q33N
**Priority:** HIGH — dispatch as soon as Wave 1 completes

## Context

Wave 1 dispatched 6 bees in parallel:
- CANVAS-000: Convert floating panels to shell panes (FOUNDATION)
- CANVAS-001: LLM → IR → Canvas pipeline
- CANVAS-002: Port Split/Join/Queue nodes
- CANVAS-003A: Port basic annotation nodes (text, rect, ellipse, sticky)
- CANVAS-003B: Port rich annotation nodes (line, image, callout)
- CANVAS-010: ELK auto-layout engine

Wave 2 depends on Wave 1 completion — specifically CANVAS-000 (pane architecture) which establishes the adapter pattern that modes 004 and 005 build on.

## Wave 2 Task Files (Already Written — Review Before Dispatch)

All 5 task files are in `.deia/hive/tasks/`. Read each one, verify it's still correct after Wave 1 output, then dispatch.

### 1. CANVAS-004: Port Configure Mode
- **File:** `.deia/hive/tasks/2026-03-23-TASK-CANVAS-004-CONFIGURE-MODE.md`
- **What:** Pre-simulation setup mode — validation panel + sim config + read-only canvas
- **Depends on:** CANVAS-000 (pane adapter pattern)
- **Model:** sonnet

### 2. CANVAS-005: Port Optimize Mode
- **File:** `.deia/hive/tasks/2026-03-23-TASK-CANVAS-005-OPTIMIZE-MODE.md`
- **What:** Parameter sweep, Pareto frontier, optimization engine
- **Depends on:** CANVAS-000 (pane adapter pattern)
- **Model:** sonnet
- **Risk flag:** This was flagged as potentially too large. Review the bee's approach — if it tries to do backend + full Pareto viz in one shot, consider splitting

### 3. CANVAS-009A: Lasso Selection + BroadcastChannel Sync
- **File:** `.deia/hive/tasks/2026-03-23-TASK-CANVAS-009A-LASSO-AND-BROADCAST.md`
- **What:** Freeform lasso multi-select, multi-window sync via BroadcastChannel
- **Depends on:** Nothing in Wave 1 (independent)
- **Model:** sonnet

### 4. CANVAS-009B: Smart Edge Handles
- **File:** `.deia/hive/tasks/2026-03-23-TASK-CANVAS-009B-SMART-HANDLES.md`
- **What:** Auto-positioned edge connection points based on relative node positions
- **Depends on:** Nothing in Wave 1 (independent)
- **Model:** sonnet

### 5. CANVAS-009C: Missing Property Tabs (6 tabs)
- **File:** `.deia/hive/tasks/2026-03-23-TASK-CANVAS-009C-PROPERTY-TABS.md`
- **What:** Port Queue, Operator, Outputs, Badges, Edge, Design property sections
- **Depends on:** CANVAS-002 (new node types need property support)
- **Model:** sonnet

## Pre-Dispatch Checklist (Q33N Must Do)

Before dispatching each bee:

1. **Read Wave 1 response files** — check for failures, partial completions, or conflicts
2. **Verify CANVAS-000 completed successfully** — if it failed, CANVAS-004 and CANVAS-005 cannot dispatch (they depend on the pane adapter pattern)
3. **Check for file conflicts** — Wave 1 bees may have modified FlowCanvas.tsx, types.ts, NodePalette.tsx, canvas.egg.md. If multiple bees edited the same file, resolve conflicts before Wave 2
4. **Verify new node types registered** — CANVAS-002, 003A, 003B should have added node types to FlowCanvas.tsx. Confirm before dispatching 009C (property tabs need to know what node types exist)
5. **Run tests** — `cd browser && npx vitest run src/apps/sim/` to verify Wave 1 didn't break anything

## Dispatch Strategy

- **CANVAS-009A and CANVAS-009B** have no Wave 1 dependencies — dispatch immediately
- **CANVAS-004 and CANVAS-005** depend on CANVAS-000 — dispatch only after verifying 000 completed
- **CANVAS-009C** depends on CANVAS-002 — dispatch only after verifying 002 completed
- Maximum 5 bees in parallel (all 5 can go if dependencies are met)

## Wave 3 Preview

After Wave 2 completes, Wave 3 has 3 backend wiring tasks:
- CANVAS-006: Playback backend + pane adapter
- CANVAS-007: Tabletop backend + pane adapter
- CANVAS-008: Compare backend + pane adapter

These depend on the pane architecture (000) and the modes being in place (004, 005). Q33NR will write the Wave 3 briefing after reviewing Wave 2 results.

## Rules

- Dispatch through dispatch.py ONLY
- All bees: sonnet model, --inject-boot
- Read each bee's response file when it completes — all 8 sections must be present
- If a bee fails or ships stubs, dispatch a fix task before moving to Wave 3
- Report results to Q33NR when all 5 complete
