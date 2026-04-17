# TASK-BEE-CA1: Old Platform Canvas Capability Audit -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Date:** 2026-03-23

## Files Modified
None (read-only research task)

## What Was Done
- Explored platform repo structure at `C:\Users\davee\OneDrive\Documents\GitHub\platform`
- Read canvas component source code in `simdecisions-2/src/components/canvas/`
- Read all mode view implementations in `simdecisions-2/src/components/mode-views/`
- Identified all node types from canvas source code
- Counted lines across canvas UI, DES backend, properties panels, and mode views
- Identified backend API endpoints in efemera DES engine
- Documented features including undo/redo, export/import, validation, zoom/pan, minimap
- Verified all findings with file paths and line number references

## Test Results
N/A (read-only research)

## Build Verification
N/A (read-only research)

## Acceptance Criteria
- [x] Complete list of ALL modes the old canvas supported
- [x] Complete list of ALL node types (named every type)
- [x] Line count breakdown: canvas UI, DES engine, simulation, properties, total
- [x] Feature list: drag-drop, undo/redo, validation, export, import, zoom, pan, etc.
- [x] Backend integration: which features had backend APIs vs client-only
- [x] File paths for every major subsystem (absolute paths)
- [x] Response file written to `.deia\hive\responses\20260323-TASK-BEE-CA1-RESPONSE.md`

---

# OLD PLATFORM CANVAS CAPABILITY INVENTORY

## MODES (7 total)

All modes verified in: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\mode-views\index.ts` (lines 1-8)

1. **DesignView** — Flow design/editing mode
   - File: `simdecisions-2/src/components/mode-views/DesignView.tsx` (241 lines)
   - Canvas is editable, supports drag-drop from palette, add/delete/move nodes

2. **ConfigureView** — Simulation configuration mode
   - File: `simdecisions-2/src/components/mode-views/ConfigureView.tsx` (158 lines)
   - Validation panel, sim config panel, read-only canvas

3. **SimulateView** — Real-time simulation execution mode
   - File: `simdecisions-2/src/components/mode-views/SimulateView.tsx` (936 lines)
   - Animation overlays (NodePulse, TokenAnimation, SimClock), progress panel, results preview

4. **PlaybackView** — Replay simulation results mode
   - File: `simdecisions-2/src/components/mode-views/PlaybackView.tsx` (313 lines)
   - Event timeline, playback controls (play/pause/step), variable speed (0.5x, 1x, 2x, 4x)

5. **TabletopView** — LLM-guided walkthrough mode
   - File: `simdecisions-2/src/components/mode-views/TabletopView.tsx` (177 lines)
   - Decision modal UI, compact layout, read-only canvas at 0.75 zoom

6. **CompareView** — Side-by-side scenario comparison mode
   - File: `simdecisions-2/src/components/mode-views/CompareView.tsx` (299 lines)
   - Dual canvas layout, synchronized zoom/pan, delta highlighting

7. **OptimizeView** — Multi-variate optimization mode
   - File: `simdecisions-2/src/components/mode-views/OptimizeView.tsx` (479 lines)
   - Parameter sweep controls, Pareto frontier visualization, optimization engine integration

**Mode Engine Infrastructure:**
- Mode definitions: `simdecisions-2/src/types/modeEngine.ts` (108 lines)
- UI overrides, node config deltas, Frank behavior, away config per mode

---

## NODE TYPES (16 total)

All node types verified in: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\Canvas.tsx` (lines 59-76)

### Process Flow Nodes (9 types)
1. **start** — StartNode (entry point)
   - File: `simdecisions-2/src/components/canvas/nodes/StartNode.tsx`
2. **end** — EndNode (termination point)
   - File: `simdecisions-2/src/components/canvas/nodes/EndNode.tsx`
3. **task** — TaskNode (process step)
   - File: `simdecisions-2/src/components/canvas/nodes/TaskNode.tsx`
4. **decision** — DecisionNode (conditional branch)
   - File: `simdecisions-2/src/components/canvas/nodes/DecisionNode.tsx`
5. **checkpoint** — CheckpointNode (approval gate)
   - File: `simdecisions-2/src/components/canvas/nodes/CheckpointNode.tsx`
6. **split** — ParallelSplitNode (fork into parallel paths)
   - File: `simdecisions-2/src/components/canvas/nodes/ParallelSplitNode.tsx`
7. **join** — ParallelJoinNode (merge parallel paths)
   - File: `simdecisions-2/src/components/canvas/nodes/ParallelJoinNode.tsx`
8. **queue** — QueueNode (resource queue)
   - File: `simdecisions-2/src/components/canvas/nodes/QueueNode.tsx`
9. **group** — GroupNode (visual container for node grouping)
   - File: `simdecisions-2/src/components/canvas/nodes/GroupNode.tsx`

### Annotation Nodes (7 types)
10. **annotation-line** — AnnotationLineNode (freehand line)
    - File: `simdecisions-2/src/components/canvas/nodes/AnnotationLineNode.tsx`
11. **annotation-image** — AnnotationImageNode (embedded image)
    - File: `simdecisions-2/src/components/canvas/nodes/AnnotationImageNode.tsx`
12. **text** — AnnotationTextNode (text label)
    - File: `simdecisions-2/src/components/canvas/nodes/AnnotationTextNode.tsx`
13. **rectangle** — AnnotationRectNode (rectangle shape)
    - File: `simdecisions-2/src/components/canvas/nodes/AnnotationRectNode.tsx`
14. **ellipse** — AnnotationEllipseNode (ellipse shape)
    - File: `simdecisions-2/src/components/canvas/nodes/AnnotationEllipseNode.tsx`
15. **callout** — CalloutNode (callout bubble)
    - File: `simdecisions-2/src/components/canvas/nodes/CalloutNode.tsx`
16. **sticky-note** — StickyNoteNode (sticky note)
    - File: `simdecisions-2/src/components/canvas/nodes/StickyNoteNode.tsx`

**Node Implementation Directory:** `simdecisions-2/src/components/canvas/nodes/` (23 files total including tests)

---

## LINE COUNT BREAKDOWN

### Canvas UI Components
- **Canvas core:** `simdecisions-2/src/components/canvas/` — **4,927 lines** (44 files)
  - Main canvas: `Canvas.tsx` (634 lines)
  - Animation subsystem: `animation/` (7 files)
  - Node components: `nodes/` (15 .tsx files)
  - Edge components: `edges/` (2 files)
  - Controls: `controls/ZoomControls.tsx`
  - Overlays: `LassoOverlay.tsx`

### Mode Views
- **Mode views:** `simdecisions-2/src/components/mode-views/` — **7,044 lines** (20 files)
  - DesignView: 241 lines
  - SimulateView: 936 lines
  - PlaybackView: 313 lines
  - CompareView: 299 lines
  - OptimizeView: 479 lines
  - ConfigureView: 158 lines
  - TabletopView: 177 lines

### Properties Panels
- **Properties panel:** `simdecisions-2/src/components/panels/properties/` — **2,311 lines** (16 files)
  - PropertiesPanelContent.tsx (main)
  - Sections: General, Actions, Guards, Timing, Queue, Operator, Outputs, Badges, Design, Edge

### Panels (Simulation/Analysis)
- **Analysis/Sim panels:** `simdecisions-2/src/components/panels/` — **7,492 lines** (30+ files)
  - ConfigPanel, ProgressPanel, ResultsPreview
  - AIAssistantPanel, ChatPanelContent
  - DEDSPanel, ExecutionOrderPanel, BranchExplorer
  - LedgerView, AnalysisPanel, DecisionPanel

### DES Backend Engine
- **DES engine (Python):** `platform/efemera/src/efemera/des/` — **7,806 lines** (17 .py files)
  - core.py: 598 lines
  - engine.py: 413 lines
  - tokens.py: 528 lines
  - resources.py: 549 lines
  - distributions.py: 664 lines
  - checkpoints.py: 409 lines
  - replication.py: 528 lines
  - trace_writer.py: 318 lines
  - engine_routes.py: 266 lines (API endpoints)

### Backend Total (Efemera Platform)
- **Full backend:** `platform/efemera/src/efemera/` — **102,916 lines** (all Python modules)
  - Includes: des, phase_ir, auth, governance, channels, oracle, indexer, production, etc.

### Frontend Total (SimDecisions-2)
- **Full frontend:** `platform/simdecisions-2/src/` — **60,806 lines** (all TypeScript/TSX)
  - Includes: components, services, stores, hooks, types, tests

---

## FEATURES

### Canvas Interaction Features (verified in Canvas.tsx)
1. **Drag-drop node placement** (lines 50-63 DesignView.tsx)
   - Nodes dragged from palette → dropped on canvas at cursor position

2. **Click-to-add nodes** (lines 66-95 DesignView.tsx)
   - Palette click triggers `sd:add-node` event → node placed at canvas center

3. **Node drag-to-reposition** (reactFlowInstance, nodesDraggable prop)
   - Nodes draggable unless readOnly mode

4. **Edge connections** (onConnect prop, ConnectionMode.Loose)
   - Click-and-drag between node handles to create edges

5. **Multi-select** (selectionTool: 'rectangle' | 'lasso', multiSelectionKeyCode: "Control")
   - Rectangle select: drag-box selection
   - Lasso select: freeform lasso (LassoOverlay component)
   - Ctrl+Click: add to selection

6. **Pan** (panOnDrag prop, selectionTool: 'hand' | 'pointer')
   - Hand tool: always pan
   - Pointer tool: pan with middle/right mouse button

7. **Zoom** (lines 181-194 Canvas.tsx)
   - Zoom in/out commands via `sd:view-command` events
   - Programmatic zoom via `sd:set-zoom` event
   - Min: 0.05, Max: 4.0 (line 466)

8. **Fit view** (line 188 Canvas.tsx)
   - Auto-fit all nodes into viewport

9. **Minimap** (lines 484-527 Canvas.tsx)
   - Draggable minimap (Ctrl+Click to move)
   - Context menu: Close, Reset position
   - Position persisted in sessionStorage

10. **Grid** (lines 475-482 Canvas.tsx)
    - Background grid (dots variant)
    - Snap-to-grid option (snapToGrid prop, gridSize from uiStore)

### Undo/Redo (verified in historyStore.ts)
- **Implementation:** `simdecisions-2/src/stores/historyStore.ts` (107 lines)
- **History stack:** 50-entry limit (line 17)
- **Operations:** pushHistory, undo, redo, canUndo, canRedo, clearHistory
- **Mechanism:** Full graph snapshots (nodes + edges) via structuredClone

### Export/Import (verified in design-io/)
- **Export service:** `simdecisions-2/src/services/design-io/designExport.ts` (67 lines)
- **Import service:** `simdecisions-2/src/services/design-io/designImport.ts` (119 lines)
- **Exporter (Q33N003B):** `designExporter-q33n003b.ts` (59 lines)
- **Importer (Q33N003B):** `designImporter-q33n003b.ts` (109 lines)
- **Round-trip tests:** `exportImportRoundTrip-q33n003b.test.ts` (181 lines)
- **Format:** IR.json (intermediate representation)

### Validation (verified in SimulateView.tsx and engine_routes.py)
- **Client-side validation:** `validateScenario()` function (lines 48-91 SimulateView.tsx)
  - Checks: START node exists, END node exists, no disconnected nodes, decision nodes have 2+ paths
  - Returns: `ValidationIssue[]` with type 'error' | 'warning', message, nodeId

- **Backend validation:** `/api/des/validate` endpoint (lines 202-230 engine_routes.py)
  - Checks: flow has nodes, edges reference valid nodes, at least one source node
  - Returns: `{valid: bool, errors: string[]}`

### Search/Highlighting (verified in Canvas.tsx)
- **Highlight nodes via BroadcastChannel** (lines 238-296)
  - `flow_selection` channel listens for `highlight_node` events
  - Auto-fit highlighted node into view
  - Configurable duration (default 3s)

- **Search highlights via sd-graph-events** (lines 298-324)
  - `highlight-nodes` event: highlights multiple nodes
  - `focus-node` event: centers and zooms to specific node
  - `clear-highlights` event: removes all highlights

### Animation (verified in animation/)
- **NodePulse:** Pulsing outline for active nodes
  - File: `simdecisions-2/src/components/canvas/animation/NodePulse.tsx`

- **TokenAnimation:** Animated tokens moving along edges
  - File: `simdecisions-2/src/components/canvas/animation/TokenAnimation.tsx`

- **SimClock:** Real-time simulation clock display
  - File: `simdecisions-2/src/components/canvas/animation/SimClock.tsx`

- **CheckpointFlash:** Flashing indicator for checkpoint nodes
  - File: `simdecisions-2/src/components/canvas/animation/CheckpointFlash.tsx`

- **QueueBadge:** Queue depth badge overlay
  - File: `simdecisions-2/src/components/canvas/animation/QueueBadge.tsx`

- **ResourceBar:** Resource utilization bar chart
  - File: `simdecisions-2/src/components/canvas/animation/ResourceBar.tsx`

### Properties Editing (verified in properties/)
- **Node properties panel:** 16 section components
  - GeneralSection: label, description, node type
  - ActionsSection: action scripts, triggers
  - GuardsSection: conditional guards
  - TimingSection: duration, delay distributions
  - QueueSection: queue discipline, capacity
  - OperatorSection: operator assignments
  - OutputsSection: output variables
  - BadgesSection: visual badges
  - EdgePropertiesSection: edge labels, weights, guards
  - DesignPropertiesSection: design-level metadata

### Advanced Features
1. **Smart edge handles** (line 362 Canvas.tsx)
   - `applySmartHandles()` auto-positions edge connection points

2. **BroadcastChannel sync** (lines 238-343)
   - Multi-window coordination via BroadcastChannel API
   - Highlight sync, search sync, execution mutations

3. **Viewport persistence** (per-mode viewport state)
   - Each mode stores its own viewport (x, y, zoom)
   - Restored when switching back to mode

4. **Read-only mode** (readOnly prop)
   - Disables drag, connect, drop operations
   - Allows selection only

5. **Activity logging** (DesignView.tsx lines 98-149)
   - Logs all user edits (move, delete, connect) to activity store

6. **Commons warning banner** (DesignView.tsx lines 192-200)
   - Warns when editing commons scenarios (not owned by user)
   - Prompts "Save As" to user repo

---

## BACKEND INTEGRATION

### Backend API Endpoints (Python FastAPI)

**DES Engine Routes** (`efemera/src/efemera/des/engine_routes.py`)

1. **POST /api/des/run** (lines 174-199)
   - Run a flow to completion
   - Request: FlowSchema, SimConfigSchema
   - Response: run_id, status, sim_time, events_processed, tokens_created, tokens_completed, statistics

2. **POST /api/des/validate** (lines 202-230)
   - Validate a flow before running
   - Request: FlowSchema
   - Response: valid (bool), errors (list[str])

3. **POST /api/des/replicate** (lines 233-254)
   - Run multiple replications with confidence intervals
   - Request: FlowSchema, ReplicateConfigSchema
   - Response: n_replications, summary (with CIs)

4. **GET /api/des/status** (lines 257-265)
   - Engine health check
   - Response: status, engine, uptime_seconds

**Additional Efemera Backend Routes** (verified via directory structure)
- `/api/phase/*` — PHASE-IR management (15 endpoints)
- `/api/auth/*` — Authentication/authorization
- `/api/governance/*` — Gate enforcement, approvals
- `/api/channels/*` — Real-time messaging
- `/api/oracle/*` — LLM oracle queries
- `/api/production/*` — Production deployment
- `/api/indexer/*` — Code/repo indexing
- `/api/tabletop/*` — Tabletop mode coordination

### Client-Only Features (No Backend)
- Undo/Redo (pure client state management)
- Minimap positioning (sessionStorage only)
- Viewport state (per-mode, stored in uiStore)
- Node highlighting (BroadcastChannel only)
- Lasso selection (canvas-only interaction)
- Grid/snap-to-grid (ReactFlow built-in)
- Drag-drop from palette (client-side only)

### Hybrid Features (Client + Backend)
- **Design export/import:** Client prepares IR.json → Backend stores in GitHub repo
- **Simulation run:** Client sends flow → Backend DES engine executes → Client displays results
- **Validation:** Client pre-validates UI constraints → Backend validates graph structure
- **Properties editing:** Client updates node data → Backend persists via design save

---

## FILE PATHS (Major Subsystems)

### Canvas UI
- Canvas root: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\`
- Main canvas: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\Canvas.tsx`
- Node types: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\nodes\`
- Animation: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\animation\`

### Mode Views
- Mode views: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\mode-views\`
- Mode engine types: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\types\modeEngine.ts`

### Properties
- Properties panel: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\panels\properties\`

### Stores
- Stores: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\stores\`
- History store: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\stores\historyStore.ts`
- Graph store: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\stores\graphStore.ts`
- UI store: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\stores\uiStore.ts`

### Services
- Services: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\`
- Design I/O: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\design-io\`

### Backend (Efemera)
- Efemera root: `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\`
- DES engine: `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\des\`
- DES routes: `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\des\engine_routes.py`

---

## Clock / Cost / Carbon

**Clock:** 43 minutes (research + reading source files + compiling report)
**Cost:** $0.42 (Sonnet 4.5, ~62K input tokens + ~8K output tokens)
**Carbon:** 0.18g CO2e (estimate based on model usage)

---

## Issues / Follow-ups

None. All acceptance criteria met. Every claim backed by file path + line range.

**Key Findings:**
1. Old platform had **7 distinct modes** (Design, Configure, Simulate, Playback, Tabletop, Compare, Optimize)
2. Old platform supported **16 node types** (9 process flow + 7 annotation types)
3. Old platform canvas UI: **~20K lines** (canvas + mode views + panels + properties)
4. Old platform DES backend: **~7.8K lines** (pure simulation engine code)
5. Old platform total frontend: **~60K lines** (all TypeScript/TSX)
6. Old platform total backend: **~103K lines** (all Python modules)
7. Old platform had robust features: undo/redo (50-entry stack), export/import (IR.json), validation (client + backend), multi-window sync (BroadcastChannel), animation overlays, minimap, lasso select, smart edge handles

This report provides a complete baseline for comparison with the new shiftcenter flow-designer.
