# TASK-CANVAS-010: Implement ELK Auto-Layout (Replacing Dagre) -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-03-23

## Files Modified

### Created
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\services\layout\elk.ts` (107 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\services\layout\distribute.ts` (67 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\services\layout\index.ts` (5 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\hooks\useLayout.ts` (68 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\services\layout\__tests__\elk.test.ts` (149 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\services\layout\__tests__\distribute.test.ts` (185 lines)

### Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\ZoomControls.tsx` (added onAutoLayout prop + button)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx` (integrated useLayout hook)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\package.json` (added elkjs dependency)

## What Was Done

- **Installed elkjs package** — `npm install elkjs` (v0.9.3)
- **Implemented ELK layout engine** (`elk.ts`) — async `layoutWithElk()` function
  - Supports all 4 directions: LR (RIGHT), RL (LEFT), TB (DOWN), BT (UP)
  - Direction mapping: LR→RIGHT, RL→LEFT, TB→DOWN, BT→UP
  - Configurable spacing: nodeSep (80px), rankSep (120px), nodeWidth (180px), nodeHeight (60px)
  - Handle position auto-set based on direction (LR/RL → horizontal, TB/BT → vertical)
  - Edge label support (width: 80px, height: 24px)
  - No coordinate transform needed — ELK returns top-left positions (same as ReactFlow)
- **Implemented manual distribute functions** (`distribute.ts`)
  - `distributeHorizontal(nodes, minGap=80)` — sort by X, equalize spacing, center around group
  - `distributeVertical(nodes, minGap=100)` — sort by Y, equalize spacing, center around group
  - Uses `node.measured.width/height` with fallbacks to 180x60
- **Created useLayout hook** (`useLayout.ts`) — React integration with ReactFlow
  - `applyLayout(direction)` — async auto-layout for all nodes
  - `distributeH(minGap)` — distribute selected nodes (or all if none selected) horizontally
  - `distributeV(minGap)` — distribute selected nodes (or all if none selected) vertically
- **Added auto-layout button to ZoomControls**
  - Click → TB layout
  - Shift+Click → LR layout
  - SVG icon matching old platform dagre button
  - Hover states with CSS variables
- **Integrated into FlowDesigner**
  - Imported `useLayout` hook
  - Wired `applyLayout` to ZoomControls `onAutoLayout` prop
  - Available in design, simulate, playback, compare modes (not tabletop)
- **TDD approach** — wrote 24 tests first, then implementation
  - 14 ELK tests: direction ordering, handle positions, edge labels, node preservation
  - 10 distribute tests: horizontal/vertical, overlapping nodes, single node, normalization

## Test Results

```
Test Files  2 passed (2)
     Tests  24 passed (24)
  Duration  42.46s
```

### ELK Tests (14 passing)
- ✓ lays out nodes without positions
- ✓ produces left-to-right flow with LR direction
- ✓ produces top-to-bottom flow with TB direction
- ✓ ensures no node overlaps (unique positions)
- ✓ returns empty array for empty nodes
- ✓ handles edges with labels
- ✓ LR layout sets horizontal handle positions
- ✓ TB layout sets vertical handle positions
- ✓ RL layout sets horizontal handle positions
- ✓ BT layout sets vertical handle positions
- ✓ TB layout produces vertical node arrangement
- ✓ LR layout produces horizontal node arrangement
- ✓ preserves node id and type
- ✓ returns same number of nodes

### Distribute Tests (10 passing)
- ✓ distributes 3 overlapping nodes in a row with min 80px gap
- ✓ distributes 5 nodes at random positions left-to-right
- ✓ handles single node (no-op)
- ✓ handles 2 nodes correctly
- ✓ normalizes nodes already wider than minimum gap
- ✓ distributes 3 overlapping nodes in a column with min 100px gap
- ✓ distributes 5 nodes at random positions top-to-bottom
- ✓ handles single node (no-op)
- ✓ handles 2 nodes correctly
- ✓ normalizes nodes already taller than minimum gap

## Build Verification

- TypeScript type check: ✓ No errors in layout files
- All layout tests passing: ✓ 24/24
- No hardcoded colors: ✓ All CSS uses `var(--sd-*)` or theme tokens
- No file over 500 lines: ✓ Largest file is 185 lines (distribute.test.ts)
- No stubs: ✓ All functions fully implemented

## Acceptance Criteria

- [x] Install `elkjs` package: `cd browser && npm install elkjs`
- [x] `browser/src/apps/sim/services/layout/elk.ts` — ELK layout engine wrapper
  - [x] `layoutWithElk(nodes, edges, options): Promise<LayoutedNode[]>`
  - [x] Support directions: LR, RL, TB, BT (mapped to ELK's `elk.direction`)
  - [x] Options: nodeSep, rankSep, nodeWidth, nodeHeight
  - [x] Handle position auto-set based on direction
  - [x] Center→top-left coordinate transform for ReactFlow (NOT NEEDED — ELK returns top-left)
- [x] `browser/src/apps/sim/services/layout/distribute.ts` — manual distribute functions
  - [x] `distributeHorizontal(nodes, minGap=80)` — sort by X, equalize spacing
  - [x] `distributeVertical(nodes, minGap=100)` — sort by Y, equalize spacing
- [x] `browser/src/apps/sim/services/layout/index.ts` — barrel exports
- [x] `browser/src/apps/sim/hooks/useLayout.ts` — React hook: `const { applyLayout, distributeH, distributeV } = useLayout()`
- [x] Toolbar integration: add auto-layout button to ZoomControls (click=TB, shift+click=LR)
- [x] Test file: `browser/src/apps/sim/services/layout/__tests__/elk.test.ts` — 14 tests (exceeded 13+ requirement)
- [x] Test file: `browser/src/apps/sim/services/layout/__tests__/distribute.test.ts` — 10 tests (matched requirement)
- [x] Tests written FIRST (TDD)
- [x] All tests pass
- [x] 13+ ELK tests: LR ordering, TB ordering, no overlaps, handle positions for all 4 directions, edge labels, node preservation
- [x] 10+ distribute tests: horizontal/vertical, overlapping nodes, single node, normalization

## Clock / Cost / Carbon

- **Clock:** 90 minutes (research old platform, TDD test writing, implementation, debugging ELK direction mapping, integration, verification)
- **Cost:** ~$0.40 (Sonnet 4.5 — 70K tokens in, 20K tokens out, debugging iterations)
- **Carbon:** ~2g CO2e (LLM inference + npm install)

## Issues / Follow-ups

### Resolved During Implementation
- **ELK direction mapping:** Initially used `TB/LR/etc` directly, but ELK expects `DOWN/RIGHT/LEFT/UP`. Fixed with direction map.
- **Coordinate transform:** Initially thought ELK returns center-based positions (like dagre), but ELK actually returns top-left. Removed unnecessary transform.

### Recommended Next Tasks
- **TASK-CANVAS-011:** LLM tool call integration for `layout_actions` (port from old platform `canvas-tools.ts`)
  - Tool definition: `layout_actions` with enum actions: `auto_layout_lr`, `auto_layout_tb`, `auto_layout_rl`, `auto_layout_bt`, `distribute_horizontal`, `distribute_vertical`
  - Handler needs to call `useLayout` hook functions
  - Optional `node_ids` parameter for selected nodes
- **BL-XXX (new):** Keyboard shortcuts for auto-layout (e.g., `Ctrl+Shift+L` for TB layout)
- **BL-XXX (new):** Context menu integration — right-click selected nodes → "Distribute Horizontally" / "Distribute Vertically"
- **TASK-CANVAS-003:** Annotation nodes (depends on layout for auto-arranging comments)

### Notes
- ELK is async (returns Promise) — this is handled correctly in the hook and button handler
- Old platform used dagre (sync), new uses ELK (async) — no backward compatibility needed
- ELK supports hierarchical layouts for future group drill-down (advantage over dagre)
- Distribute functions center the group around its midpoint (same behavior as old platform)
- Auto-layout button visible in all non-tabletop/non-compare modes
- Tests cover all 4 directions + edge cases (empty, single node, overlapping, labels)
