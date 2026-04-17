# Flow Designer Port — Enhancement Notes

**Created:** 2026-03-14
**Purpose:** Bees append observations here during the port. Do NOT fix anything — just log it.

---


## TASK-098: Tabletop + Checkpoints + Collaboration + Compare Port

**Date:** 2026-03-14  
**Files Ported:** 21 (7 tabletop + 3 checkpoints + 5 collaboration + 6 compare)  
**Total Lines:** 6,299

### Key Dependencies Observed

1. **Theme imports** — All files use `colors` and `fonts` from `../../../lib/theme`
2. **Auth imports** — Several files import from `../../../lib/auth`:
   - `useTabletop.ts`: `getAuthHeaders`
   - `useCheckpoints.ts`: `getAuthHeaders`
   - `useCollaboration.ts`: `getToken`, `getUser`
   - `useCompare.ts`: `getAuthHeaders`
3. **Config imports** — `useCollaboration.ts` imports `WS_URL` from `../../../lib/config`
4. **Adapter imports** — Several files use `useApiClient` from `../../../adapters`:
   - `useCheckpoints.ts`
   - `useCompare.ts`
5. **ReactFlow** — Multiple files import from `@xyflow/react`
6. **Phase types** — Compare files import from `../types` (PhaseNodeData, PhaseEdgeData)
7. **Phase nodes** — `SplitCanvas.tsx` imports `PhaseNode` from `../nodes/PhaseNode`

### Integration Work Needed

- Verify all theme color/font constants match ShiftCenter theme
- Ensure auth helper functions exist in `lib/auth`
- Verify `WS_URL` exists in `lib/config`
- Ensure `useApiClient` adapter hook is available
- Port or stub Phase types if not already present
- Ensure `PhaseNode` component exists in `../nodes/`

### Architecture Notes

- **Tabletop mode** uses both server API and local fallback (`LocalGraphWalker`)
- **Checkpoints** use localStorage with optimistic UI
- **Collaboration** is WebSocket-based with auto-reconnect
- **Compare** mode runs structural diff algorithm client-side
- All hooks follow React conventions with proper cleanup on unmount


## TASK-097: Simulation + Playback Port

**Date:** 2026-03-14
**Model:** Sonnet
**Files Ported:** 18 (11 simulation + 7 playback)
**Total Lines:** 4,462

### Simulation Files (11)
- LocalDESEngine.ts (281 lines) — Local discrete event simulation engine with priority queue scheduler
- ProgressPanel.tsx (301 lines) — Right-side progress panel with replication metrics
- ResultsPreview.tsx (172 lines) — Bottom-right aggregated results with mini histograms
- SimConfigPanel.tsx (318 lines) — Left-side config panel for simulation parameters
- SimulateOverlay.tsx (185 lines) — Transport controls + SimClock rendered as ReactFlow Panels
- SimulationConfig.tsx (343 lines) — Configuration dialog for DES parameters
- SimulationPanel.tsx (653 lines) — Side panel with stats, transport controls, event log
- SimulationResultsStore.ts (39 lines) — Singleton store for event log persistence
- simNodeStyle.ts (33 lines) — CSS style helper for DES node states
- useSimulation.ts (521 lines) — Hook for WebSocket + local DES engine lifecycle
- useSimulationLayer.ts (107 lines) — Hook for styled nodes/edges during simulation

### Playback Files (7)
- EventList.tsx (258 lines) — Scrolling event log synced with playback
- PlaybackControls.tsx (215 lines) — Play/pause/step/scrubber controls
- PlaybackTimeline.tsx (266 lines) — Scrubber timeline with event density visualization
- SpeedMetrics.tsx (255 lines) — Real-time metrics display with sim/wall time
- SpeedSelector.tsx (167 lines) — Fibonacci speed picker (0.5x to ∞)
- usePlayback.ts (281 lines) — Hook for playback state with animation frame loop
- usePlaybackLayer.ts (67 lines) — Hook for node highlight during playback

### Key Dependencies Observed

1. **Simulation Dependencies**:
   - `@xyflow/react` — Node, Edge, Panel types
   - `../../../lib/theme` — colors, fonts
   - `../../../lib/config` — WS_URL for WebSocket connection
   - `../../../lib/auth` — getToken for WebSocket auth
   - `../animation/SimClock` — Clock component for SimulateOverlay
   - `../types` — SimulationState, FlowMode types

2. **Playback Dependencies**:
   - `../simulation/SimulationResultsStore` — simResultsStore singleton
   - `../simulation/useSimulation` — SimEvent type
   - `../../../lib/theme` — colors, fonts
   - `../types` — FlowMode type

### Architecture Notes

1. **Dual-engine simulation**:
   - Primary: LocalDESEngine runs in-browser with priority queue scheduler
   - Secondary: Optional WebSocket to backend DES server (degrades gracefully)
   - Event stream unified via `handleEvent` callback

2. **Playback architecture**:
   - Reads events from SimulationResultsStore singleton
   - Uses `requestAnimationFrame` loop for smooth playback
   - Fibonacci speed scale: [0.5, 1, 2, 3, 5, 8, 13, 21, 34, 55, ∞]
   - Metrics calculated from playback state (sim time, wall time, events/sec)

3. **Event types**:
   - `token_move`, `node_activate`, `node_complete`
   - `checkpoint_reached`, `resource_claim`, `resource_release`
   - `sim_stats`, `sim_complete`, `sim_error`

4. **Visual feedback**:
   - Simulation: Node states (idle/active/completed/queued) + animated edges
   - Playback: Purple highlight box-shadow on current actor node

### Integration Work Needed

- Verify `../animation/SimClock` component exists (referenced by SimulateOverlay)
- Verify `../types` exports: SimulationState, FlowMode
- Ensure `WS_URL` and `getToken` exist in lib/ (optional for local-only mode)
- Port or stub theme lib if not already present

### Observations

- Clean 100% port — no changes to source code
- Line count variance (-18 total) due to line ending differences only
- LocalDESEngine is fully self-contained — can run without backend
- SimulationResultsStore provides bridge between Simulate and Playback modes
- All React hooks follow proper cleanup patterns (unmount, ref cleanup)

## TASK-096: Modes + Properties + Responsive Port

**Date:** 2026-03-14
**Model:** Sonnet

### Files Ported (20 total)
- 5 modes: CompareMode, DesignMode, PlaybackMode, SimulateMode, TabletopMode
- 8 properties: ActionsTab, GeneralTab, GuardsTab, NodePopover, OracleTab, PropertyPanel, ResourcesTab, TimingTab
- 7 responsive: FocusMode, MobileControls, ResponsiveLayout, SlideUpPanel, TouchGestures, index.ts, useBreakpoint.ts

### Observations
1. **Import patterns**: All files import from `../../../lib/theme` for colors/fonts — will need to verify this path exists in shiftcenter
2. **ReactFlow dependencies**: Multiple files import from `@xyflow/react` — verify package installed
3. **Peer component dependencies detected**:
   - CompareMode imports: SplitCanvas, MetricsPanel, DiffHighlighter, useCompare
   - PlaybackMode imports: PlaybackControls, SpeedSelector, PlaybackTimeline, EventList, SpeedMetrics, usePlayback
   - SimulateMode imports: PhaseNode, CheckpointNode, SimulationPanel, SimulationConfigDialog, useSimulation, CheckpointFlash, CheckpointManager, CheckpointTimeline, useCheckpoints, simResultsStore
   - TabletopMode imports: PhaseNode, CheckpointNode, TabletopChat, useTabletop
   - DesignMode imports: useFlowState (type only)
4. **CSS-in-JS patterns**: All styles use inline React.CSSProperties objects — consistent with platform repo patterns
5. **Responsive breakpoints**: useBreakpoint uses standard mobile/tablet/desktop breakpoints (768px, 1024px)
6. **Touch gesture support**: TouchGestures component supports pinch zoom, two-finger pan, tap, long-press, double-tap
7. **Oracle tier system**: OracleTab defines 5 tiers (none, level1, level2, level3, escalation) for governance
8. **Property accordion**: PropertyPanel uses collapsible sections with badge indicators showing active state
9. **Animation patterns**: Multiple components use CSS @keyframes animations for smooth transitions

### Recommendations for Next Wave
- Port peer components before attempting to use these modes (compare/, playback/, simulation/, tabletop/, checkpoints/, animation/)
- Verify theme utilities (colors, fonts) match expected structure
- Check if simResultsStore singleton needs separate porting
- Consider porting useFlowState hook for DesignMode context menu functionality

## TASK-095: Core + Nodes + Edges + Overlays + Telemetry (2026-03-14)

**Files ported:** 25 files, 5,098 lines total
- Core: 13 files (BranchExplorer, ContextMenu, FlowCanvas, FlowDesigner, FlowDesignerSkeleton, FlowToolbar, NodePalette, ZoomControls, demoFlow, index, types, useFlowState, useNodeEditing)
- Nodes: 4 files (CheckpointNode, GroupNode, PhaseNode, ResourceNode)
- Edges: 3 files (EdgeTimingEditor, PhaseEdge, TokenEdge)
- Overlays: 3 files (DistributionTooltip, TimingBadge, VariablePill)
- Telemetry: 2 files (eventTypes, useEventLedger)

**Observations:**
- All files copied with 100% preservation (0 changes)
- Line counts verified identical between source and destination
- Clean 1:1 port using `cp` command for efficiency
- All subdirectories created successfully (nodes/, edges/, overlays/, telemetry/)
- No missing dependencies detected — files use relative imports within flow-designer tree
- Port strategy: preserve source code 100% to enable downstream diff-analysis and selective enhancement

**Next wave:** TASK-096 will port modes/ and properties/ subdirectories
