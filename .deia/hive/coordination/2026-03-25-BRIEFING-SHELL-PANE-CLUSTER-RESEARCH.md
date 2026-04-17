# BRIEFING: Shell Pane Cluster — Research & Triage

**Date:** 2026-03-25
**From:** Q33NR
**To:** Q33N
**Model:** sonnet
**Role:** queen
**Type:** Research (no code changes)

## Objective

Research and verify whether the following 5 shell pane bugs are still reproducible. These bugs describe related symptoms around pane drag-and-drop, docking, and floating behavior. Determine which are still real issues, which may have been fixed by recent work, and whether any can be merged.

## Bugs to Investigate

### BUG-054 (P1) — Can't drag pane into open area
"Pane drag/dock: cannot drag pane into open area (BUG-054) and dragging onto canvas creates floating window instead of docking (BUG-059). Merged tracker."

### BUG-055 (P1) — Loading EGG into sub-pane shows unregistered app type
"Playground: loading EGG into sub-pane shows unregistered app type instead of replace dialog"

### BUG-056 (P1) — Kanban drag: whole pane highlights
"Kanban drag: whole pane highlights as invalid drop target before valid target accepts"

### BUG-059 (P1) — Dragging pane onto canvas creates float
"Dragging a pane onto canvas creates a floating window instead of docking" (currently marked FIXED/merged into BUG-054, but verify the underlying issue)

### BUG-066 (P1) — No way to return floated pane to docked
"Dragging pane to float has no way to return to docked position"

## Research Tasks

For each bug:

1. **Read the relevant source code** — shell drag/drop handlers, pane docking logic, float/dock state management
2. **Identify the code path** — trace what happens when a user drags a pane (drag start → drop target detection → dock/float decision)
3. **Assess current state** — has recent work (canvas drag isolation, pane architecture changes) fixed or changed the behavior?
4. **Recommend action** — close as fixed, keep open with updated description, or merge with another bug

## Key Files to Examine

- `browser/src/shell/` — shell reducer, drag handlers, layout tree
- `browser/src/shell/components/` — HiveHostPanes, PaneChrome, drop targets
- `browser/src/infrastructure/relay_bus/` — drag-related bus events
- Any recent commits touching pane drag/drop behavior

## Deliverables

Write a single response file with:
1. For each bug: current status assessment (still broken / fixed / partially fixed / needs merge)
2. Recommended inventory commands to update bug statuses
3. If any bugs are still real: a brief description of what code needs to change to fix them
4. If bugs should be merged: which ones and what the merged description should be

## Constraints

- **Read-only research.** Do NOT write code or modify files.
- **Do NOT dispatch bees.** This is a Q33N-level research task.
- Write your response to `.deia/hive/responses/`
