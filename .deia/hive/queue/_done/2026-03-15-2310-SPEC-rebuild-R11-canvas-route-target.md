# SPEC: Wire canvas route target in terminal

## Priority
P0.55

## Model Assignment
sonnet

## Objective
Restore terminal's `routeTarget='canvas'` functionality — modify types.ts and useTerminal.ts so the canvas mode handler POSTs NL text to `/api/phase/nl-to-ir` and sends IR flows to canvas pane.

## Task File
`.deia/hive/tasks/2026-03-15-TASK-R11-wire-canvas-route-target.md`

## Acceptance Criteria
- [ ] types.ts updated: 'canvas' added to routeTarget unions
- [ ] useTerminal.ts updated: 73-line canvas handler inserted
- [ ] All 10 canvas tests pass
- [ ] No regressions in existing terminal tests
