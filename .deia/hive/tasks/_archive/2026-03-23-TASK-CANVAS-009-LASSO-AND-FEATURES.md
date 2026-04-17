# TASK-CANVAS-009: Port Missing Features (Lasso, BroadcastChannel, Smart Handles, Properties)

## Objective
Port 4 missing features from old platform: (1) Lasso selection, (2) BroadcastChannel multi-window sync, (3) Smart edge handles, (4) Missing property panel sections.

## Context
Audit report (lines 157-171) identifies these regressions:
- **Lasso selection**: Old had freeform lasso multi-select (LassoOverlay.tsx), new has only rectangle select
- **BroadcastChannel sync**: Old had multi-window coordination (highlight sync, execution mutations), new has none
- **Smart edge handles**: Old had applySmartHandles() for auto-positioned edge connection points, new unclear
- **Property sections**: Old had 16 sections, new has 6 tabs. Missing: Queue, Operator, Outputs, Badges, Edge, Design

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\LassoOverlay.tsx` (lasso selection)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\Canvas.tsx` (lines 238-343: BroadcastChannel sync, line 362: smart handles)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\panels\properties\` (16 property sections)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowCanvas.tsx` (where to add lasso)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\properties\PropertyPanel.tsx` (current 6 tabs)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\edges\PhaseEdge.tsx` (edge component, for smart handles)

## Deliverables

### Part 1: Lasso Selection
- [ ] `browser/src/apps/sim/components/flow-designer/LassoOverlay.tsx` (~200 lines max)
- [ ] Wire into FlowCanvas.tsx (render LassoOverlay when selection tool is 'lasso')
- [ ] Add lasso tool to FlowToolbar.tsx (icon, toggle between rectangle/lasso)
- [ ] Test: `browser/src/apps/sim/components/flow-designer/__tests__/lasso-selection.test.tsx`

### Part 2: BroadcastChannel Multi-Window Sync
- [ ] `browser/src/apps/sim/components/flow-designer/collaboration/BroadcastSync.tsx` (~150 lines max)
- [ ] Sync highlight events across windows (when node highlighted in window A, window B also highlights)
- [ ] Sync execution mutations (when simulation runs in window A, window B sees same state)
- [ ] Use BroadcastChannel API (already in browsers)
- [ ] Test: `browser/src/apps/sim/components/flow-designer/collaboration/__tests__/broadcast-sync.test.tsx`

### Part 3: Smart Edge Handles
- [ ] Port applySmartHandles() logic to `browser/src/apps/sim/components/flow-designer/edges/smartHandles.ts`
- [ ] Auto-position edge handles based on node connections (top, bottom, left, right)
- [ ] Wire into PhaseEdge.tsx (apply smart handles on mount)
- [ ] Test: `browser/src/apps/sim/components/flow-designer/edges/__tests__/smart-handles.test.tsx`

### Part 4: Missing Property Sections
- [ ] `browser/src/apps/sim/components/flow-designer/properties/QueueTab.tsx` (queue properties)
- [ ] `browser/src/apps/sim/components/flow-designer/properties/OperatorTab.tsx` (operator properties)
- [ ] `browser/src/apps/sim/components/flow-designer/properties/OutputsTab.tsx` (outputs properties)
- [ ] `browser/src/apps/sim/components/flow-designer/properties/BadgesTab.tsx` (badges/annotations)
- [ ] `browser/src/apps/sim/components/flow-designer/properties/EdgeTab.tsx` (edge properties)
- [ ] `browser/src/apps/sim/components/flow-designer/properties/DesignTab.tsx` (design metadata)
- [ ] Register all 6 tabs in PropertyPanel.tsx
- [ ] Test: `browser/src/apps/sim/components/flow-designer/properties/__tests__/new-tabs.test.tsx`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Lasso selection with no nodes — clears selection
  - BroadcastChannel when only one window open — no errors
  - Smart handles on node with 10+ edges — handles don't overlap
  - Property tabs with no selected node — show "No selection" message
  - Each new tab: validates input, shows defaults, saves to node data

## Constraints
- No file over 500 lines (split if needed)
- CSS: var(--sd-*) only
- No stubs — all 4 features fully implemented
- Lasso: SVG path for lasso shape, select nodes inside path
- BroadcastChannel: channel name must be flow-specific (e.g., `canvas-${flowId}`)
- Smart handles: deterministic (same flow always produces same handle layout)
- Property tabs: match old platform field names where possible

## Acceptance Criteria
- [ ] LassoOverlay.tsx created, renders on canvas
- [ ] Lasso tool in FlowToolbar, toggles selection mode
- [ ] Lasso selection works (drag lasso, nodes inside are selected)
- [ ] BroadcastSync.tsx created, syncs highlight/mutations
- [ ] Multi-window highlight sync works (tested manually or via Playwright)
- [ ] smartHandles.ts created, auto-positions edge handles
- [ ] Smart handles applied to all edges (no overlapping handles)
- [ ] All 6 property tabs created (Queue, Operator, Outputs, Badges, Edge, Design)
- [ ] All 6 tabs registered in PropertyPanel.tsx
- [ ] Test files exist for all 4 features (4 test files minimum)
- [ ] All existing tests pass

## Response Requirements — MANDATORY
Write response file: `.deia/hive/responses/20260323-TASK-CANVAS-009-RESPONSE.md` with all 8 sections.
