# Survey Report: Canvas App Porting from SimDecisions-2

**Date:** 2026-03-14
**Q33N:** QUEEN-QUEUE-TEMP-2026-03-14-0200-SPE
**Spec:** SPEC-CANVAS-APP-001

---

## 1. Old Repo (platform/simdecisions-2)

### Found Components

| Component | Status | Location | Line Count | Notes |
|-----------|--------|----------|------------|-------|
| **ReactFlow Canvas** | ✅ FULL | `src/components/canvas/Canvas.tsx` | 633 | Full ReactFlow instance with zoom, pan, selection, minimap, grid, snap-to-grid |
| **Custom Nodes** | ✅ FULL | `src/components/canvas/nodes/` | ~15 files | StartNode, EndNode, TaskNode, DecisionNode, CheckpointNode, ParallelSplit, ParallelJoin, GroupNode, QueueNode, AnnotationLine, AnnotationImage, AnnotationText, AnnotationRect, AnnotationEllipse, CalloutNode, StickyNoteNode |
| **Custom Edges** | ✅ FULL | `src/components/canvas/edges/CustomEdge.tsx` | ~100 | Smart edge routing |
| **LLM Tool Calling** | ✅ FULL | `src/services/llm/tools/canvas-tools.ts` | ~200 | `apply_diff` tool with add/remove/update nodes/edges |
| **Canvas Chat Guide** | ✅ DOC | `src/hooks/CANVAS_CHAT_BROWSER_GUIDE.md` | 150 | Integration docs for useCanvasChatBrowser hook |
| **Properties Panel** | ✅ FULL | `src/components/panels/properties/PropertiesPanelContent.tsx` | ~600 | 6 accordion sections: General, Timing, Actions, Outputs, Badges, Operator, Queue |
| **Node Palette** | ❌ NOT FOUND | — | — | No dedicated palette component. Nodes created via right-click context menu or LLM chat. |
| **Toolbar** | ⚠️ MINIMAL | `src/components/layout/toolbar.css` + test | ~50 | Basic toolbar, no drag-to-canvas palette |
| **IR Types** | ✅ FULL | `src/types/ir.ts` | ~500 | PHASE-IR v1.0 types: NodeType, IRNode, IREdge, IRGraph, OperatorConfig, TimingConfig, GuardConfig, Action, etc. |
| **Dialect Pack** | ⚠️ PARTIAL | `src/services/frank/dialectLoader.ts` | ~100 | Exists but no canvas-specific dialect .md file found |

### ReactFlow Version
- **Package:** `@xyflow/react` version `^12.10.1`
- **Layout lib:** `dagre` version `^0.8.5`
- Old repo uses **ReactFlow v12** (latest major version in Feb 2026)

### Key Patterns
1. **Node Types:** 16 custom node types, registered in Canvas.tsx nodeTypes map
2. **Edge Rendering:** CustomEdge with smart handle positioning
3. **Lasso Selection:** LassoOverlay.tsx component (custom selection UI)
4. **Minimap + Grid:** Built-in ReactFlow components
5. **Chat Integration:** LLM uses `apply_diff` tool to generate IR mutations
6. **Properties:** Accordion-style panel, synchronized with selection store
7. **No drag palette:** Users add nodes via chat or context menu, NOT drag-from-palette

---

## 2. New Repo (shiftcenter)

### Found Components

| Component | Status | Location | Notes |
|-----------|--------|----------|-------|
| **Canvas primitive** | ❌ NOT STARTED | `browser/src/primitives/canvas/` | Directory does not exist |
| **Canvas adapter** | ❌ NOT STARTED | `browser/src/apps/canvasAdapter.tsx` | File does not exist |
| **ReactFlow dependency** | ❌ NOT INSTALLED | `browser/package.json` | `reactflow` and `@xyflow/react` NOT in dependencies |
| **IR types** | ⚠️ PARTIAL | `browser/src/primitives/terminal/irRouting.ts` | Basic IR routing exists, but no full PHASE-IR type definitions |
| **App registry** | ✅ EXISTS | `browser/src/apps/index.ts` | Has `registerApp()` pattern, ready for canvas registration |
| **`to_ir` handler** | ✅ WIRED | `browser/src/services/terminal/terminalResponseRouter.ts:184-194` | `to_ir` slot ALREADY implemented! Sends `terminal:ir-deposit` bus message |
| **Tree-browser** | ✅ EXISTS | `browser/src/primitives/tree-browser/` | Has TreeBrowser primitive + 4 adapters (channels, chatHistory, filesystem, members) |
| **Tree-browser adapters** | ✅ PATTERN | `browser/src/primitives/tree-browser/adapters/channelsAdapter.ts` | Existing adapter pattern shows TreeNodeData structure, async loading, mock fallback |
| **Canvas EGG** | ❌ NOT STARTED | `eggs/canvas.egg.md` | File does not exist |

### Key Insights
- **`to_ir` handler ALREADY exists** — no need to implement (spec section 7.3 says "wire it" but it's done)
- **Tree-browser adapter pattern established** — palette + properties adapters follow same pattern as channelsAdapter
- **App registry ready** — just add `registerApp('canvas', CanvasAdapter)`
- **No IR types ported yet** — need to port PHASE-IR types from old repo

---

## 3. What to PORT vs BUILD

### PORT from Old Repo
1. **Canvas.tsx** → `browser/src/primitives/canvas/CanvasApp.tsx`
   - 633 lines → modularize to stay under 500 line rule
   - Split into: CanvasApp.tsx (main), CanvasNodeTypes.ts (node registry), CanvasEdgeTypes.ts (edge registry)
2. **Custom node components** (16 files) → `browser/src/primitives/canvas/nodes/`
   - Port: StartNode, EndNode, TaskNode, DecisionNode only (core 4)
   - Build stubs for others (CheckpointNode, SplitNode, JoinNode, QueueNode, GroupNode, annotations)
3. **CustomEdge.tsx** → `browser/src/primitives/canvas/edges/CustomEdge.tsx`
4. **IR types** → `browser/src/types/ir.ts`
   - Port full PHASE-IR v1.0 type definitions from old repo
5. **canvas-tools.ts** (LLM tool def) → NOT NEEDED for ShiftCenter (terminal uses envelope format, not tool calling)

### BUILD Fresh
1. **canvasAdapter.tsx** — ShiftCenter app registry adapter (follows terminalAdapter pattern)
2. **paletteAdapter.ts** — Tree-browser adapter for node types (follows channelsAdapter pattern)
3. **propertiesAdapter.ts** — Tree-browser adapter for selected node properties (follows channelsAdapter pattern)
4. **Bus integration** — Canvas listens for `terminal:ir-deposit`, publishes `canvas:node-selected`
5. **canvas.egg.md** — 5-pane layout (palette | canvas + terminal | properties)
6. **Dialect .md file** — Canvas-specific terminal prompt teaching LLM to generate IR mutations (port from old repo's tool schema)

### DO NOT BUILD (per spec section 8)
- Simulation execution engine
- Optimization mode
- Persistence (save/load graphs)
- Multi-user collaboration
- Undo/redo
- Tabletop walkthrough
- Scenario branching / Alterverse
- DES engine

---

## 4. Modularization Strategy (Rule 4: No file over 500 lines)

Old `Canvas.tsx` is 633 lines. Split into:

| File | Responsibility | Est. Lines |
|------|---------------|------------|
| `CanvasApp.tsx` | Main ReactFlow wrapper, bus integration, hooks | ~250 |
| `CanvasNodeTypes.ts` | Node type registry + nodeTypes map | ~100 |
| `CanvasEdgeTypes.ts` | Edge type registry + edgeTypes map | ~50 |
| `CanvasControls.tsx` | Zoom, minimap, grid controls (port from old ZoomControls.tsx) | ~100 |
| `nodes/StartNode.tsx` | Start node component | ~80 |
| `nodes/EndNode.tsx` | End node component | ~80 |
| `nodes/TaskNode.tsx` | Task node component | ~100 |
| `nodes/DecisionNode.tsx` | Decision node component | ~100 |
| `edges/CustomEdge.tsx` | Custom edge renderer | ~100 |

Total: ~960 lines across 9 files. All files under 250 lines each.

---

## 5. Testing Strategy

### Unit Tests (20+ required)
- **CanvasApp:**
  - Renders with zero nodes (empty state)
  - Renders with sample IR data (5 nodes, 4 edges)
  - Publishes `canvas:node-selected` on node click
  - Receives `terminal:ir-deposit` and adds node
  - Receives `terminal:ir-deposit` and adds edge
- **Palette Adapter:**
  - Loads node types as TreeNodeData
  - Groups by category (Process, Flow Control, Resources, Events)
  - Items are draggable
  - Publishes `palette:drag-start` on drag
- **Properties Adapter:**
  - Listens for `canvas:node-selected`
  - Renders node properties as accordion sections
  - Publishes `properties:value-changed` on edit
- **Node Components:**
  - Each core node type (Start, End, Task, Decision) renders correctly
  - Node data changes trigger re-render
- **Bus Integration:**
  - `to_ir` envelope slot routes to canvas
  - Terminal → LLM → envelope → canvas renders node (E2E, mocked LLM)

### Integration Tests
- Full EGG load: canvas.egg.md → 5 panes appear
- Terminal NL input → mocked LLM response → canvas updates
- Palette drag → canvas drop → node created
- Canvas node click → properties panel updates

---

## 6. Dependency Additions

Add to `browser/package.json`:
```json
"@xyflow/react": "^12.10.1",
"dagre": "^0.8.5"
```

Do NOT add `elkjs` (not used in old repo, spec lists it but old repo only uses dagre).

---

## 7. Files to Create (Task File Summary)

### Task 1: Port PHASE-IR Types (Haiku, 1h)
- Port `src/types/ir.ts` from old repo to `browser/src/types/ir.ts`
- 15 tests: type validation, codec support, node/edge parsing

### Task 2: Build Canvas Primitive (Sonnet, 3h)
- `browser/src/primitives/canvas/CanvasApp.tsx` (main)
- `browser/src/primitives/canvas/CanvasNodeTypes.ts` (registry)
- `browser/src/primitives/canvas/CanvasEdgeTypes.ts` (registry)
- `browser/src/primitives/canvas/CanvasControls.tsx` (zoom/minimap/grid)
- `browser/src/primitives/canvas/nodes/StartNode.tsx`
- `browser/src/primitives/canvas/nodes/EndNode.tsx`
- `browser/src/primitives/canvas/nodes/TaskNode.tsx`
- `browser/src/primitives/canvas/nodes/DecisionNode.tsx`
- `browser/src/primitives/canvas/edges/CustomEdge.tsx`
- 20 tests: render, bus integration, node selection, IR deposit handling

### Task 3: Build Canvas Adapter (Haiku, 1h)
- `browser/src/apps/canvasAdapter.tsx`
- Register in `browser/src/apps/index.ts`
- 3 tests: adapter lifecycle, pane config, bus wiring

### Task 4: Build Palette Adapter (Haiku, 1.5h)
- `browser/src/primitives/tree-browser/adapters/paletteAdapter.ts`
- Mock node type data (4 categories, 12 node types)
- 5 tests: load, group by category, draggable, bus publish

### Task 5: Build Properties Adapter (Sonnet, 2h)
- `browser/src/primitives/tree-browser/adapters/propertiesAdapter.ts`
- Accordion sections: General, Four-Vector, Three Currencies, Connections
- 5 tests: listen for selection, render properties, edit flow, bus publish

### Task 6: Build Canvas EGG (Haiku, 0.5h)
- `eggs/canvas.egg.md` (5-pane layout, links, prompt block)
- No tests (pure YAML config)

### Task 7: Integration Tests (Haiku, 1h)
- `browser/src/primitives/canvas/__tests__/canvas.integration.test.ts`
- E2E: terminal → envelope → canvas → properties
- 5 tests: full flow with mocked LLM

---

## 8. Estimated Effort

| Task | Model | Hours | Parallel? |
|------|-------|-------|-----------|
| 1. Port IR types | Haiku | 1.0 | Yes |
| 2. Canvas primitive | Sonnet | 3.0 | Yes (after task 1) |
| 3. Canvas adapter | Haiku | 1.0 | Yes (after task 2) |
| 4. Palette adapter | Haiku | 1.5 | Yes (after task 1) |
| 5. Properties adapter | Sonnet | 2.0 | Yes (after task 1) |
| 6. Canvas EGG | Haiku | 0.5 | Yes (after tasks 2-5) |
| 7. Integration tests | Haiku | 1.0 | After all |

**Total:** ~10 hours sequential, ~5 hours if tasks 2-5 dispatched in parallel after task 1 completes.

**Parallel dispatch strategy:**
1. Task 1 (IR types) → blocks all others
2. Tasks 2, 3, 4, 5 → parallel (independent directories)
3. Task 6 (EGG) → after 2-5 complete
4. Task 7 (integration tests) → after task 6

---

## 9. Recommendation to Q88NR

**APPROVED TO PROCEED.**

This spec is well-scoped. All dependencies exist in the old repo. The new repo has the infrastructure (app registry, tree-browser adapters, bus, `to_ir` handler) ready.

**Risk areas:**
1. **File size:** Old Canvas.tsx is 633 lines — MUST modularize to 9 files to stay under 500 line rule. Task file enforces this.
2. **ReactFlow v12 compatibility:** New repo uses Vite 5, React 18. Old repo uses Vite 7, React 19. ReactFlow v12 works on both, but test carefully for any React 19 → 18 compat issues (unlikely, but check).
3. **No drag palette in old repo:** Spec assumes drag-from-palette exists, but old repo used context menu + chat. Task 4 (palette adapter) must BUILD drag behavior from scratch, not port.

**Approval conditions:**
- All files under 500 lines (enforced in task deliverables)
- CSS uses `var(--sd-*)` only (enforced in task constraints)
- 20+ tests total (enforced in task test requirements)
- No stubs (enforced in task constraints)

**Dispatch sequence:**
1. Q33N writes 7 task files
2. Q88NR reviews task files (mechanical checklist)
3. Q88NR approves (or sends back for corrections, max 2 cycles)
4. Q33N dispatches bees:
   - Task 1 (Haiku) → wait for completion
   - Tasks 2 (Sonnet), 3 (Haiku), 4 (Haiku), 5 (Sonnet) → parallel dispatch
   - Task 6 (Haiku) → after tasks 2-5 complete
   - Task 7 (Haiku) → after task 6 completes

---

**End of Survey Report.**

*Q33N · DEIA Hive · 2026-03-14*
