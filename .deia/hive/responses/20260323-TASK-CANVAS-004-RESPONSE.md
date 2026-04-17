# TASK-CANVAS-004: Port Configure Mode -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-23

## Files Modified

### Created
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\modes\ConfigureMode.tsx` (335 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\modes\ConfigureMode.css` (282 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\modes\__tests__\ConfigureMode.test.tsx` (244 lines, 10 tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\modes\__tests__\ConfigureMode.integration.test.tsx` (101 lines, 3 tests)

### Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\types.ts` (added 'configure' to FlowMode type)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx` (added ConfigureMode import, isConfigure state, mode switch logic)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md` (added Configure sidebar panel with ⚙️ icon)

## What Was Done

- **ConfigureMode component created** (335 lines)
  - Read-only ReactFlow canvas with `nodesDraggable={false}`, `nodesConnectable={false}`, `elementsSelectable={true}`
  - Three-panel layout: validation (left), canvas (center), sim config (right)
  - Validation panel displays errors/warnings from `validateFlow()` function
  - Sim config panel with replications, time horizon, seed fields (reused from old platform)
  - Start button disabled when validation errors exist
  - Mode switching: Back to Design button, Start Simulation transitions to simulate mode

- **Validation logic ported from old platform**
  - Checks for missing START node (error)
  - Checks for missing END node (error)
  - Checks for multiple START nodes (warning)
  - Checks for disconnected nodes (warning)
  - Checks for checkpoint nodes with <2 outgoing edges (warning)
  - Click-to-focus: clicking validation issue centers canvas on that node

- **CSS file created** (282 lines)
  - All styles use CSS variables (`var(--sd-*)`)
  - No hardcoded colors (hex/rgb/named)
  - Three-panel responsive layout with flexbox
  - Button variants: primary (green), secondary (bordered), icon (purple-dim)
  - Validation issue cards with error (red-dim) and warning (orange-dim) backgrounds
  - Sim config panel styling matches old platform design

- **FlowMode type updated** in `types.ts`
  - Added `'configure'` to FlowMode union type
  - Updated comment from "five editing modes" to "six editing modes"

- **FlowDesigner.tsx integration**
  - Imported ConfigureMode component
  - Added `isConfigure` state variable
  - Added Configure to mode menu items in syndicatedMenuGroups
  - Added ConfigureMode render block (replaces canvas, similar to TabletopMode/CompareMode pattern)
  - Updated canvas visibility condition: `{!isConfigure && !isTabletop && !isCompare && (`

- **Canvas.egg.md updated**
  - Added Configure panel to sidebar panels array
  - Icon: "⚙️", label: "Configure"
  - Action: `sim:mode-change`, payload: `{ mode: "configure" }`
  - Position: between Design and Simulate panels

- **Tests created** (13 total tests)
  - ConfigureMode.test.tsx: 10 unit tests (TDD approach)
    - Renders without crashing
    - Displays "No issues" when flow is valid
    - Displays validation errors when flow is invalid (missing START/END)
    - Displays warnings for disconnected nodes
    - Displays warnings for checkpoint nodes with insufficient branches
    - Renders ReactFlow canvas in read-only mode
    - Calls onModeChange when exit button clicked
    - Displays sim config panel with default values
    - Prevents starting simulation when validation errors exist
    - Enables start button when flow is valid
  - ConfigureMode.integration.test.tsx: 3 integration tests
    - Switches from configure to simulate mode on Start button click
    - Switches from configure to design mode on Back button click
    - Renders both validation and sim config panels simultaneously

- **Build verification**
  - `npm run build` succeeded
  - Build artifact created: `browser/dist/index.html` (1.2K, timestamp: 2026-03-23 22:40)
  - No TypeScript compilation errors in ConfigureMode.tsx

## Architecture Compliance

- **CSS variables only**: All styles use `var(--sd-*)` variables, no hardcoded colors
- **File size limit**: ConfigureMode.tsx = 335 lines (under 500 line limit)
- **TDD approach**: Tests written first, then implementation
- **No stubs**: All functions fully implemented (validateFlow, handleStartSimulation, handleConfigChange, etc.)
- **Read-only canvas**: Uses ReactFlow props `nodesDraggable={false}`, `nodesConnectable={false}` to enforce read-only mode
- **Reused existing components**: SimConfigPanel logic ported from old platform, validation logic ported from ConfigureView.tsx

## Validation Logic Accuracy

Validation function ported from old platform (`simdecisions-2/src/components/mode-views/ConfigureView.tsx` lines 16-63):

1. **START node check**: Error if 0 start nodes, warning if >1 start nodes
2. **END node check**: Error if 0 end nodes
3. **Disconnected nodes**: Warning for nodes not in `connectedNodes` set (built from edge source/target), excluding START/END nodes
4. **Checkpoint branches**: Warning if checkpoint node has <2 outgoing edges

Click-to-focus: When user clicks a validation issue with `nodeId`, canvas centers on that node using `reactFlowInstance.setCenter(x, y, { zoom: 1.5, duration: 400 })`

## Mode Switching Behavior

- **Design → Configure**: User clicks Configure sidebar panel (⚙️ icon) in canvas.egg.md
- **Configure → Design**: User clicks "← Back to Design" button in ConfigureMode toolbar
- **Configure → Simulate**: User clicks "▶ Start Simulation" button (only enabled when `isValid === true`, i.e., no validation errors)

## Test Coverage

- **10 unit tests** in ConfigureMode.test.tsx
- **3 integration tests** in ConfigureMode.integration.test.tsx
- **Total: 13 tests** covering:
  - Rendering with valid/invalid flows
  - Validation error/warning display
  - Read-only canvas behavior
  - Mode switching (configure → design, configure → simulate)
  - Sim config panel display
  - Start button enable/disable based on validation

## Notes

- ConfigureMode is a **full-screen replacement** for the canvas (similar to TabletopMode/CompareMode), not an overlay
- Validation panel and sim config panel are **inline components** in ConfigureMode.tsx, not separate shell panes (this differs from TASK-CANVAS-000's pane adapter pattern, but matches the old platform's ConfigureView.tsx architecture)
- Sim config changes in configure mode update local state only — simulation does not start until user clicks "Start Simulation" and mode switches to simulate
- Read-only canvas allows panning and zooming but disables drag, connect, and edit operations
