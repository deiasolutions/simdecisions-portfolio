# BRIEFING: Canvas Full Port — Wire Everything, Close Every Gap

**Date:** 2026-03-23
**From:** Q33NR
**To:** Q33N
**Priority:** CRITICAL — Q88N wants this ASAP

## Context

We ran a 3-bee audit (CA1, CA2, CA3) comparing old platform canvas to new shiftcenter flow-designer. The results are damning: bees built outward (importers, mobile, collaboration stubs) instead of inward (core functionality). The old system had 7 working modes and 16 node types. The new has 5 modes (3 are shells), 6 node types, and the fundamental LLM-to-canvas pipeline doesn't work.

**Full audit report:** `.deia/hive/coordination/2026-03-23-CANVAS-COMPARISON-REPORT.md`
**Old platform CA1 response:** `.deia/hive/responses/20260323-TASK-BEE-CA1-RESPONSE.md`
**New shiftcenter CA2 response:** `.deia/hive/responses/20260323-TASK-BEE-CA2-RESPONSE.md`

## Objective

Port ALL missing canvas functionality from the old platform to shiftcenter. Wire ALL shell modes to backends. Close EVERY regression gap identified in the audit. When done, the new system must have feature parity with the old system PLUS the genuinely new features that already exist.

## What Must Be Built (Priority Order)

### TIER 1 — Core Pipeline (blocks everything)

**T1-A: LLM → IR → Canvas Pipeline**
The fundamental use case: user talks to LLM in terminal, LLM generates PHASE-IR, IR appears as nodes on the canvas. The bus event `terminal:ir-deposit` exists, the canvas EGG subscribes to it, but nothing sends it. Wire it end-to-end.
- Old platform source: Check how old tabletop/AI features created nodes
- New terminal: `browser/src/primitives/terminal/useTerminal.ts`
- New canvas: `browser/src/apps/sim/components/flow-designer/FlowCanvas.tsx`
- Bus types: `terminal:ir-deposit` in `browser/src/infrastructure/relay_bus/`
- DES routes: `hivenode/routes/des_routes.py`

### TIER 2 — Missing Node Types (10 types)

**T2-A: Process Flow Nodes (3 types)**
Port from old platform to new flow-designer:
- `split` (ParallelSplitNode) — fork into parallel paths
- `join` (ParallelJoinNode) — merge parallel paths
- `queue` (QueueNode) — resource queue

Old source: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\canvas\nodes\`
New target: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\nodes\`
Register in: `FlowCanvas.tsx` nodeTypes map (lines 36-44)

**T2-B: Annotation Nodes (7 types)**
Port all 7 annotation node types:
- `annotation-line` (AnnotationLineNode) — freehand line
- `annotation-image` (AnnotationImageNode) — embedded image
- `text` (AnnotationTextNode) — text label
- `rectangle` (AnnotationRectNode) — rectangle shape
- `ellipse` (AnnotationEllipseNode) — ellipse shape
- `callout` (CalloutNode) — callout bubble
- `sticky-note` (StickyNoteNode) — sticky note

Old source: same nodes/ directory
New target: same nodes/ directory
Register in: `FlowCanvas.tsx` nodeTypes map
Add to: `NodePalette.tsx` so users can drag them onto canvas

### TIER 3 — Missing Modes (2 modes)

**T3-A: Configure Mode**
Port ConfigureView from old platform:
- Validation panel + sim config panel + read-only canvas
- Old source: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\mode-views\ConfigureView.tsx` (158 lines)
- New target: `browser/src/apps/sim/components/flow-designer/modes/ConfigureMode.tsx`
- Register in mode engine types: `types.ts` line 155-160

**T3-B: Optimize Mode**
Port OptimizeView from old platform:
- Parameter sweep controls, Pareto frontier visualization, optimization engine integration
- Old source: `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\mode-views\OptimizeView.tsx` (479 lines)
- New target: `browser/src/apps/sim/components/flow-designer/modes/OptimizeMode.tsx`
- Register in mode engine types

### TIER 4 — Wire Shell Modes to Backends (3 modes)

**T4-A: Playback Mode Backend**
Currently SHELL (reads from localStorage). Wire to backend:
- Current UI: `modes/PlaybackMode.tsx` (378 lines), `playback/PlaybackControls.tsx`, `PlaybackTimeline.tsx`, `EventList.tsx`
- Needs: Backend API for simulation event replay, server-side event storage
- Old approach: Check old PlaybackView.tsx (313 lines) for backend integration pattern

**T4-B: Tabletop Mode Backend**
Currently SHELL (client-only LocalGraphWalker). Wire to backend:
- Current UI: `modes/TabletopMode.tsx` (364 lines), `tabletop/TabletopChat.tsx`, `LocalGraphWalker.ts`
- Needs: Backend tabletop API for session persistence, multi-user support
- Old platform had `/api/tabletop/*` routes — check and port

**T4-C: Compare Mode Backend**
Currently SHELL (client-only diffAlgorithm). Wire to backend:
- Current UI: `modes/CompareMode.tsx` (298 lines), `compare/SplitCanvas.tsx`, `DiffHighlighter.tsx`
- Needs: Backend API for server-side diff caching, scenario comparison
- Old approach: Check old CompareView.tsx (299 lines) for backend pattern

### TIER 5 — Missing Features

**T5-A: Lasso Selection**
Port LassoOverlay component for freeform multi-select:
- Old source: `simdecisions-2/src/components/canvas/LassoOverlay.tsx`
- Add to canvas interaction tools

**T5-B: BroadcastChannel Multi-Window Sync**
Port multi-window coordination:
- Old source: Canvas.tsx lines 238-343 (highlight sync, search sync, execution mutations)
- Wire into new FlowCanvas.tsx

**T5-C: Missing Property Sections**
Old had 16 sections, new has 6 tabs. Port the missing ones:
- Queue section
- Operator section
- Outputs section
- Badges section
- Edge properties section
- Design properties section
- Old source: `simdecisions-2/src/components/panels/properties/`

**T5-D: Smart Edge Handles**
Port applySmartHandles() for auto-positioned edge connection points:
- Old source: Canvas.tsx line 362

## Dispatch Strategy

Break into bee-sized tasks. Suggested grouping:
- T1-A: 1 bee (sonnet — requires understanding full pipeline)
- T2-A + T2-B: 2 bees (1 for process nodes, 1 for annotation nodes)
- T3-A + T3-B: 1-2 bees
- T4-A + T4-B + T4-C: 2-3 bees (may need backend + frontend bees)
- T5-A through T5-D: 2-3 bees

Total: ~8-12 bees, sonnet model for all (these require reading old code and porting carefully).

## Rules

- READ the old platform source before writing new code. PORT, don't reinvent.
- TDD. Tests first.
- No hardcoded colors. CSS variables only.
- No file over 500 lines. The existing FlowDesigner.tsx at 1,123 lines is ALREADY a violation — do not make it worse.
- Every new node type, mode, and feature must be registered in the appropriate maps/types.
- Wire end-to-end. No shells, no stubs.
- Response files with all 8 sections.

## Model Assignment

All bees: **sonnet** (port work requires reading + understanding old code patterns)

## Dependencies

- T1-A (IR pipeline) has no blockers — start immediately
- T2-A, T2-B (node types) have no blockers — can parallel with T1-A
- T3-A, T3-B (modes) can run after T2 completes (modes may reference new node types)
- T4-A, T4-B, T4-C (backend wiring) should run after modes exist
- T5-A through T5-D (features) can run in parallel with T3/T4
