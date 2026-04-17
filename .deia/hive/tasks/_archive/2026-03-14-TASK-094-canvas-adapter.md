# TASK-094: Build Canvas App Adapter

## Objective
Create the ShiftCenter app adapter for the canvas primitive, registering it in the app registry so it can be loaded by EGG configs.

## Context
ShiftCenter uses an app adapter pattern — each primitive has an adapter that registers it with the shell. See `terminalAdapter.tsx` and `browser/src/apps/index.ts` for the pattern.

## Dependencies
- **TASK-093 must be complete** (provides `browser/src/primitives/canvas/CanvasApp.tsx`)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\index.ts` (app registry)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\terminalAdapter.tsx` (pattern reference)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx` (from TASK-093)

## Deliverables
- [ ] Create `browser/src/apps/canvasAdapter.tsx` (~80 lines)
  - Export `CanvasAdapter` component that wraps `CanvasApp`
  - Accept pane config props (paneId, appConfig)
  - Pass relevant config to CanvasApp (initial graph data, read-only mode, etc.)
- [ ] Register in `browser/src/apps/index.ts` — add `registerApp('canvas', CanvasAdapter)`
- [ ] Create `browser/src/apps/__tests__/canvasAdapter.test.tsx` — 5+ tests:
  - Adapter renders CanvasApp
  - Adapter passes paneId
  - Adapter handles missing config gracefully
  - App registry resolves 'canvas' to CanvasAdapter
  - Unmount cleans up bus listeners

## Constraints
- No file over 500 lines
- CSS: `var(--sd-*)` only
- Follow the exact same pattern as `terminalAdapter.tsx`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260314-TASK-094-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Model Assignment
haiku
