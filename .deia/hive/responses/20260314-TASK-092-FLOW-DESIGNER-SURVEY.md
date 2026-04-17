# TASK-092: Flow Designer Directory Survey + Dependency Analysis

**Date:** 2026-03-14
**Source Directory:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\frontend\src`

## 1. Complete File Inventory

### Directory: `root`

| File | Lines | Type |
|------|-------|------|
| App.tsx | 96 | component |
| index.css | 100 | css |
| main.tsx | 9 | component |
| vite-env.d.ts | 1 | typescript |

**Subtotal:** 4 files, 206 lines

### Directory: `adapters`

| File | Lines | Type |
|------|-------|------|
| adapters\ApiClientContext.tsx | 62 | component |
| adapters\api-client.ts | 620 | typescript |
| adapters\index.ts | 44 | typescript |

**Subtotal:** 3 files, 726 lines

### Directory: `adapters\__tests__`

| File | Lines | Type |
|------|-------|------|
| adapters\__tests__\cloud-api-client.test.ts | 647 | test |

**Subtotal:** 1 files, 647 lines

### Directory: `components`

| File | Lines | Type |
|------|-------|------|
| components\ApiKeyGenerator.tsx | 144 | component |
| components\AppLayout.tsx | 25 | component |
| components\ChannelSidebar.tsx | 64 | component |
| components\ChatMessage.tsx | 231 | component |
| components\CommandPopup.tsx | 80 | component |
| components\MembersPanel.tsx | 44 | component |
| components\MessageInput.tsx | 149 | component |
| components\Nav.tsx | 69 | component |
| components\QueueApproval.tsx | 203 | component |
| components\QueueStatusBadge.tsx | 52 | component |
| components\RAGAnswer.tsx | 100 | component |
| components\RAGRequest.tsx | 45 | component |
| components\Sidebar.tsx | 264 | component |
| components\TerminalOutput.tsx | 82 | component |
| components\TerminalRequest.tsx | 44 | component |

**Subtotal:** 15 files, 1596 lines

### Directory: `components\flow-designer`

| File | Lines | Type |
|------|-------|------|
| components\flow-designer\BranchExplorer.tsx | 260 | component |
| components\flow-designer\ContextMenu.tsx | 151 | component |
| components\flow-designer\FlowCanvas.tsx | 143 | component |
| components\flow-designer\FlowDesigner.tsx | 768 | component |
| components\flow-designer\FlowDesignerSkeleton.tsx | 109 | component |
| components\flow-designer\FlowToolbar.tsx | 300 | component |
| components\flow-designer\NodePalette.tsx | 165 | component |
| components\flow-designer\ZoomControls.tsx | 124 | component |
| components\flow-designer\demoFlow.ts | 95 | typescript |
| components\flow-designer\index.ts | 49 | typescript |
| components\flow-designer\types.ts | 200 | typescript |
| components\flow-designer\useFlowState.ts | 300 | hook |
| components\flow-designer\useNodeEditing.ts | 221 | hook |

**Subtotal:** 13 files, 2885 lines

### Directory: `components\flow-designer\__tests__`

| File | Lines | Type |
|------|-------|------|
| components\flow-designer\__tests__\FileOperations.test.tsx | 553 | test |
| components\flow-designer\__tests__\FlowToolbar.test.tsx | 364 | test |
| components\flow-designer\__tests__\Modes.test.tsx | 1165 | test |
| components\flow-designer\__tests__\NodePalette.test.tsx | 215 | test |
| components\flow-designer\__tests__\PropertyPanel.test.tsx | 243 | test |
| components\flow-designer\__tests__\serialization.test.ts | 512 | test |

**Subtotal:** 6 files, 3052 lines

### Directory: `components\flow-designer\animation`

| File | Lines | Type |
|------|-------|------|
| components\flow-designer\animation\CheckpointFlash.tsx | 130 | component |
| components\flow-designer\animation\NodePulse.tsx | 73 | component |
| components\flow-designer\animation\QueueBadge.tsx | 71 | component |
| components\flow-designer\animation\ResourceBar.tsx | 84 | component |
| components\flow-designer\animation\SimClock.tsx | 173 | component |
| components\flow-designer\animation\TokenAnimation.tsx | 96 | component |
| components\flow-designer\animation\index.ts | 13 | typescript |
| components\flow-designer\animation\useAnimationFrame.ts | 36 | hook |

**Subtotal:** 8 files, 676 lines

### Directory: `components\flow-designer\checkpoints`

| File | Lines | Type |
|------|-------|------|
| components\flow-designer\checkpoints\CheckpointManager.tsx | 322 | component |
| components\flow-designer\checkpoints\CheckpointTimeline.tsx | 361 | component |
| components\flow-designer\checkpoints\useCheckpoints.ts | 276 | hook |

**Subtotal:** 3 files, 959 lines

### Directory: `components\flow-designer\collaboration`

| File | Lines | Type |
|------|-------|------|
| components\flow-designer\collaboration\DesignFlight.tsx | 321 | component |
| components\flow-designer\collaboration\LiveCursors.tsx | 120 | component |
| components\flow-designer\collaboration\NodeComments.tsx | 358 | component |
| components\flow-designer\collaboration\useCollaboration.ts | 433 | hook |
| components\flow-designer\collaboration\useCollaborationLayer.ts | 120 | hook |

**Subtotal:** 5 files, 1352 lines

### Directory: `components\flow-designer\compare`

| File | Lines | Type |
|------|-------|------|
| components\flow-designer\compare\DiffHighlighter.tsx | 344 | component |
| components\flow-designer\compare\MetricsPanel.tsx | 250 | component |
| components\flow-designer\compare\SplitCanvas.tsx | 327 | component |
| components\flow-designer\compare\diffAlgorithm.ts | 347 | typescript |
| components\flow-designer\compare\snapshotStorage.ts | 34 | typescript |
| components\flow-designer\compare\useCompare.ts | 216 | hook |

**Subtotal:** 6 files, 1518 lines

### Directory: `components\flow-designer\edges`

| File | Lines | Type |
|------|-------|------|
| components\flow-designer\edges\EdgeTimingEditor.tsx | 212 | component |
| components\flow-designer\edges\PhaseEdge.tsx | 307 | component |
| components\flow-designer\edges\TokenEdge.tsx | 147 | component |

**Subtotal:** 3 files, 666 lines

### Directory: `components\flow-designer\file-ops`

| File | Lines | Type |
|------|-------|------|
| components\flow-designer\file-ops\DownloadPanel.tsx | 679 | component |
| components\flow-designer\file-ops\ExportDialog.tsx | 329 | component |
| components\flow-designer\file-ops\FileOperations.tsx | 220 | component |
| components\flow-designer\file-ops\ImportDialog.tsx | 536 | component |
| components\flow-designer\file-ops\LoadDialog.tsx | 313 | component |
| components\flow-designer\file-ops\SaveDialog.tsx | 202 | component |
| components\flow-designer\file-ops\serialization.ts | 453 | typescript |
| components\flow-designer\file-ops\useAutoSave.ts | 151 | hook |

**Subtotal:** 8 files, 2883 lines

### Directory: `components\flow-designer\file-ops\dialect-importers`

| File | Lines | Type |
|------|-------|------|
| components\flow-designer\file-ops\dialect-importers\bpmn-importer.ts | 226 | typescript |
| components\flow-designer\file-ops\dialect-importers\index.ts | 138 | typescript |
| components\flow-designer\file-ops\dialect-importers\lsys-importer.ts | 284 | typescript |
| components\flow-designer\file-ops\dialect-importers\sbml-importer.ts | 285 | typescript |

**Subtotal:** 4 files, 933 lines

### Directory: `components\flow-designer\modes`

| File | Lines | Type |
|------|-------|------|
| components\flow-designer\modes\CompareMode.tsx | 268 | component |
| components\flow-designer\modes\DesignMode.tsx | 196 | component |
| components\flow-designer\modes\PlaybackMode.tsx | 352 | component |
| components\flow-designer\modes\SimulateMode.tsx | 601 | component |
| components\flow-designer\modes\TabletopMode.tsx | 339 | component |

**Subtotal:** 5 files, 1756 lines

### Directory: `components\flow-designer\nodes`

| File | Lines | Type |
|------|-------|------|
| components\flow-designer\nodes\CheckpointNode.tsx | 158 | component |
| components\flow-designer\nodes\GroupNode.tsx | 86 | component |
| components\flow-designer\nodes\PhaseNode.tsx | 170 | component |
| components\flow-designer\nodes\ResourceNode.tsx | 130 | component |

**Subtotal:** 4 files, 544 lines

### Directory: `components\flow-designer\overlays`

| File | Lines | Type |
|------|-------|------|
| components\flow-designer\overlays\DistributionTooltip.tsx | 183 | component |
| components\flow-designer\overlays\TimingBadge.tsx | 83 | component |
| components\flow-designer\overlays\VariablePill.tsx | 87 | component |

**Subtotal:** 3 files, 353 lines

### Directory: `components\flow-designer\playback`

| File | Lines | Type |
|------|-------|------|
| components\flow-designer\playback\EventList.tsx | 241 | component |
| components\flow-designer\playback\PlaybackControls.tsx | 203 | component |
| components\flow-designer\playback\PlaybackTimeline.tsx | 248 | component |
| components\flow-designer\playback\SpeedMetrics.tsx | 241 | component |
| components\flow-designer\playback\SpeedSelector.tsx | 157 | component |
| components\flow-designer\playback\usePlayback.ts | 249 | hook |
| components\flow-designer\playback\usePlaybackLayer.ts | 61 | hook |

**Subtotal:** 7 files, 1400 lines

### Directory: `components\flow-designer\properties`

| File | Lines | Type |
|------|-------|------|
| components\flow-designer\properties\ActionsTab.tsx | 234 | component |
| components\flow-designer\properties\GeneralTab.tsx | 103 | component |
| components\flow-designer\properties\GuardsTab.tsx | 170 | component |
| components\flow-designer\properties\NodePopover.tsx | 187 | component |
| components\flow-designer\properties\OracleTab.tsx | 215 | component |
| components\flow-designer\properties\PropertyPanel.tsx | 195 | component |
| components\flow-designer\properties\ResourcesTab.tsx | 238 | component |
| components\flow-designer\properties\TimingTab.tsx | 151 | component |

**Subtotal:** 8 files, 1493 lines

### Directory: `components\flow-designer\responsive`

| File | Lines | Type |
|------|-------|------|
| components\flow-designer\responsive\FocusMode.tsx | 212 | component |
| components\flow-designer\responsive\MobileControls.tsx | 119 | component |
| components\flow-designer\responsive\ResponsiveLayout.tsx | 141 | component |
| components\flow-designer\responsive\SlideUpPanel.tsx | 193 | component |
| components\flow-designer\responsive\TouchGestures.tsx | 157 | component |
| components\flow-designer\responsive\index.ts | 11 | typescript |
| components\flow-designer\responsive\useBreakpoint.ts | 53 | hook |

**Subtotal:** 7 files, 886 lines

### Directory: `components\flow-designer\simulation`

| File | Lines | Type |
|------|-------|------|
| components\flow-designer\simulation\LocalDESEngine.ts | 230 | typescript |
| components\flow-designer\simulation\ProgressPanel.tsx | 276 | component |
| components\flow-designer\simulation\ResultsPreview.tsx | 156 | component |
| components\flow-designer\simulation\SimConfigPanel.tsx | 293 | component |
| components\flow-designer\simulation\SimulateOverlay.tsx | 181 | component |
| components\flow-designer\simulation\SimulationConfig.tsx | 320 | component |
| components\flow-designer\simulation\SimulationPanel.tsx | 619 | component |
| components\flow-designer\simulation\SimulationResultsStore.ts | 32 | store |
| components\flow-designer\simulation\simNodeStyle.ts | 32 | typescript |
| components\flow-designer\simulation\useSimulation.ts | 461 | hook |
| components\flow-designer\simulation\useSimulationLayer.ts | 98 | hook |

**Subtotal:** 11 files, 2698 lines

### Directory: `components\flow-designer\simulation\__tests__`

| File | Lines | Type |
|------|-------|------|
| components\flow-designer\simulation\__tests__\LocalDESEngine.test.ts | 39 | test |

**Subtotal:** 1 files, 39 lines

### Directory: `components\flow-designer\tabletop`

| File | Lines | Type |
|------|-------|------|
| components\flow-designer\tabletop\DecisionPanel.tsx | 425 | component |
| components\flow-designer\tabletop\DecisionPrompt.tsx | 219 | component |
| components\flow-designer\tabletop\FrankSuggestion.tsx | 158 | component |
| components\flow-designer\tabletop\LocalGraphWalker.ts | 170 | typescript |
| components\flow-designer\tabletop\StepProgress.tsx | 134 | component |
| components\flow-designer\tabletop\TabletopChat.tsx | 445 | component |
| components\flow-designer\tabletop\useTabletop.ts | 405 | hook |

**Subtotal:** 7 files, 1956 lines

### Directory: `components\flow-designer\tabletop\__tests__`

| File | Lines | Type |
|------|-------|------|
| components\flow-designer\tabletop\__tests__\LocalGraphWalker.test.ts | 41 | test |

**Subtotal:** 1 files, 41 lines

### Directory: `components\flow-designer\telemetry`

| File | Lines | Type |
|------|-------|------|
| components\flow-designer\telemetry\eventTypes.ts | 255 | typescript |
| components\flow-designer\telemetry\useEventLedger.ts | 166 | hook |

**Subtotal:** 2 files, 421 lines

### Directory: `lib`

| File | Lines | Type |
|------|-------|------|
| lib\auth.ts | 48 | typescript |
| lib\commands.test.ts | 57 | test |
| lib\commands.ts | 107 | typescript |
| lib\config.ts | 3 | typescript |
| lib\icons.tsx | 10 | component |
| lib\theme.ts | 30 | typescript |
| lib\useMobile.ts | 10 | hook |
| lib\ws.ts | 126 | typescript |

**Subtotal:** 8 files, 391 lines

### Directory: `pages`

| File | Lines | Type |
|------|-------|------|
| pages\AuthPage.tsx | 124 | component |
| pages\ChatPage.tsx | 573 | component |
| pages\DashboardPage.tsx | 317 | component |
| pages\DocsPage.tsx | 105 | component |
| pages\FlowDesignerPage.tsx | 42 | component |
| pages\LandingPage.tsx | 137 | component |
| pages\OnboardingPage.tsx | 242 | component |
| pages\SettingsPage.tsx | 156 | component |
| pages\SimDecisionsPage.tsx | 255 | component |
| pages\dashboard-widgets.tsx | 145 | component |

**Subtotal:** 10 files, 2096 lines

### Grand Totals

- **Total Files:** 153
- **Total Lines:** 32173

**Breakdown by Type:**

| Type | Files | Lines |
|------|-------|-------|
| component | 101 | 21148 |
| css | 1 | 100 |
| hook | 16 | 3256 |
| store | 1 | 32 |
| test | 10 | 3836 |
| typescript | 24 | 3801 |

## 2. External Dependency Analysis

### Internal-Outside Imports (Critical Dependencies)

These are imports from OUTSIDE the `components/flow-designer/` tree:

| Importing File | Imported Module | What's Imported |
|----------------|-----------------|-----------------|
| components\flow-designer\BranchExplorer.tsx | `../../lib/theme` | { colors, fonts } |
| components\flow-designer\ContextMenu.tsx | `../../lib/theme` | { colors, fonts } |
| components\flow-designer\FlowCanvas.tsx | `../../lib/theme` | { colors } |
| components\flow-designer\FlowDesigner.tsx | `../../lib/theme` | { colors } |
| components\flow-designer\FlowDesigner.tsx | `../../adapters` | { ApiClientProvider } |
| components\flow-designer\FlowDesignerSkeleton.tsx | `../../lib/theme` | { colors } |
| components\flow-designer\FlowToolbar.tsx | `../../lib/theme` | { colors, fonts } |
| components\flow-designer\NodePalette.tsx | `../../lib/theme` | { colors, fonts } |
| components\flow-designer\ZoomControls.tsx | `../../lib/theme` | { colors, fonts } |
| components\flow-designer\animation\CheckpointFlash.tsx | `../../../lib/theme` | { colors } |
| components\flow-designer\animation\NodePulse.tsx | `../../../lib/theme` | { colors } |
| components\flow-designer\animation\QueueBadge.tsx | `../../../lib/theme` | { colors } |
| components\flow-designer\animation\ResourceBar.tsx | `../../../lib/theme` | { colors } |
| components\flow-designer\animation\SimClock.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\animation\TokenAnimation.tsx | `../../../lib/theme` | { colors } |
| components\flow-designer\checkpoints\CheckpointManager.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\checkpoints\CheckpointTimeline.tsx | `../../../lib/theme` | { colors } |
| components\flow-designer\checkpoints\useCheckpoints.ts | `../../../lib/auth` | { getAuthHeaders } |
| components\flow-designer\checkpoints\useCheckpoints.ts | `../../../adapters` | { useApiClient } |
| components\flow-designer\collaboration\DesignFlight.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\collaboration\LiveCursors.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\collaboration\NodeComments.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\collaboration\useCollaboration.ts | `../../../lib/auth` | { getToken, getUser } |
| components\flow-designer\collaboration\useCollaboration.ts | `../../../lib/config` | { WS_URL } |
| components\flow-designer\compare\DiffHighlighter.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\compare\MetricsPanel.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\compare\SplitCanvas.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\compare\useCompare.ts | `../../../lib/auth` | { getAuthHeaders } |
| components\flow-designer\compare\useCompare.ts | `../../../adapters` | { useApiClient } |
| components\flow-designer\edges\EdgeTimingEditor.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\edges\PhaseEdge.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\edges\TokenEdge.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\file-ops\DownloadPanel.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\file-ops\DownloadPanel.tsx | `../../../lib/auth` | { getAuthHeaders } |
| components\flow-designer\file-ops\ExportDialog.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\file-ops\FileOperations.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\file-ops\ImportDialog.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\file-ops\LoadDialog.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\file-ops\SaveDialog.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\modes\CompareMode.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\modes\DesignMode.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\modes\PlaybackMode.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\modes\SimulateMode.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\modes\TabletopMode.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\nodes\CheckpointNode.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\nodes\GroupNode.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\nodes\PhaseNode.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\nodes\ResourceNode.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\overlays\DistributionTooltip.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\overlays\TimingBadge.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\overlays\VariablePill.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\playback\EventList.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\playback\PlaybackControls.tsx | `../../../lib/theme` | { colors } |
| components\flow-designer\playback\PlaybackTimeline.tsx | `../../../lib/theme` | { colors } |
| components\flow-designer\playback\SpeedMetrics.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\playback\SpeedSelector.tsx | `../../../lib/theme` | { colors } |
| components\flow-designer\playback\usePlaybackLayer.ts | `../../../lib/theme` | { colors } |
| components\flow-designer\properties\ActionsTab.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\properties\GeneralTab.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\properties\GuardsTab.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\properties\NodePopover.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\properties\OracleTab.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\properties\PropertyPanel.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\properties\ResourcesTab.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\properties\TimingTab.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\responsive\FocusMode.tsx | `../../../lib/theme` | { colors } |
| components\flow-designer\responsive\MobileControls.tsx | `../../../lib/theme` | { colors } |
| components\flow-designer\responsive\ResponsiveLayout.tsx | `../../../lib/theme` | { colors } |
| components\flow-designer\responsive\SlideUpPanel.tsx | `../../../lib/theme` | { colors } |
| components\flow-designer\simulation\ProgressPanel.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\simulation\ResultsPreview.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\simulation\SimConfigPanel.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\simulation\SimulateOverlay.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\simulation\SimulationConfig.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\simulation\SimulationPanel.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\simulation\simNodeStyle.ts | `../../../lib/theme` | { colors } |
| components\flow-designer\simulation\useSimulation.ts | `../../../lib/config` | { WS_URL } |
| components\flow-designer\simulation\useSimulation.ts | `../../../lib/auth` | { getToken } |
| components\flow-designer\simulation\useSimulationLayer.ts | `../../../lib/theme` | { colors } |
| components\flow-designer\tabletop\DecisionPanel.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\tabletop\DecisionPrompt.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\tabletop\FrankSuggestion.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\tabletop\StepProgress.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\tabletop\TabletopChat.tsx | `../../../lib/theme` | { colors, fonts } |
| components\flow-designer\tabletop\useTabletop.ts | `../../../lib/auth` | { getAuthHeaders } |
| components\flow-designer\telemetry\useEventLedger.ts | `../../../lib/auth` | { getUser } |
| components\flow-designer\telemetry\useEventLedger.ts | `../../../adapters` | { useApiClient } |

**Total:** 87 external imports from 6 unique modules

### Grouped by Imported Module

**`../../../adapters`** (imported by 3 files)
  - components\flow-designer\checkpoints\useCheckpoints.ts
  - components\flow-designer\compare\useCompare.ts
  - components\flow-designer\telemetry\useEventLedger.ts

**`../../../lib/auth`** (imported by 7 files)
  - components\flow-designer\checkpoints\useCheckpoints.ts
  - components\flow-designer\collaboration\useCollaboration.ts
  - components\flow-designer\compare\useCompare.ts
  - components\flow-designer\file-ops\DownloadPanel.tsx
  - components\flow-designer\simulation\useSimulation.ts
  - components\flow-designer\tabletop\useTabletop.ts
  - components\flow-designer\telemetry\useEventLedger.ts

**`../../../lib/config`** (imported by 2 files)
  - components\flow-designer\collaboration\useCollaboration.ts
  - components\flow-designer\simulation\useSimulation.ts

**`../../../lib/theme`** (imported by 66 files)
  - components\flow-designer\animation\CheckpointFlash.tsx
  - components\flow-designer\animation\NodePulse.tsx
  - components\flow-designer\animation\QueueBadge.tsx
  - components\flow-designer\animation\ResourceBar.tsx
  - components\flow-designer\animation\SimClock.tsx
  - components\flow-designer\animation\TokenAnimation.tsx
  - components\flow-designer\checkpoints\CheckpointManager.tsx
  - components\flow-designer\checkpoints\CheckpointTimeline.tsx
  - components\flow-designer\collaboration\DesignFlight.tsx
  - components\flow-designer\collaboration\LiveCursors.tsx
  - components\flow-designer\collaboration\NodeComments.tsx
  - components\flow-designer\compare\DiffHighlighter.tsx
  - components\flow-designer\compare\MetricsPanel.tsx
  - components\flow-designer\compare\SplitCanvas.tsx
  - components\flow-designer\edges\EdgeTimingEditor.tsx
  - components\flow-designer\edges\PhaseEdge.tsx
  - components\flow-designer\edges\TokenEdge.tsx
  - components\flow-designer\file-ops\DownloadPanel.tsx
  - components\flow-designer\file-ops\ExportDialog.tsx
  - components\flow-designer\file-ops\FileOperations.tsx
  - components\flow-designer\file-ops\ImportDialog.tsx
  - components\flow-designer\file-ops\LoadDialog.tsx
  - components\flow-designer\file-ops\SaveDialog.tsx
  - components\flow-designer\modes\CompareMode.tsx
  - components\flow-designer\modes\DesignMode.tsx
  - components\flow-designer\modes\PlaybackMode.tsx
  - components\flow-designer\modes\SimulateMode.tsx
  - components\flow-designer\modes\TabletopMode.tsx
  - components\flow-designer\nodes\CheckpointNode.tsx
  - components\flow-designer\nodes\GroupNode.tsx
  - components\flow-designer\nodes\PhaseNode.tsx
  - components\flow-designer\nodes\ResourceNode.tsx
  - components\flow-designer\overlays\DistributionTooltip.tsx
  - components\flow-designer\overlays\TimingBadge.tsx
  - components\flow-designer\overlays\VariablePill.tsx
  - components\flow-designer\playback\EventList.tsx
  - components\flow-designer\playback\PlaybackControls.tsx
  - components\flow-designer\playback\PlaybackTimeline.tsx
  - components\flow-designer\playback\SpeedMetrics.tsx
  - components\flow-designer\playback\SpeedSelector.tsx
  - components\flow-designer\playback\usePlaybackLayer.ts
  - components\flow-designer\properties\ActionsTab.tsx
  - components\flow-designer\properties\GeneralTab.tsx
  - components\flow-designer\properties\GuardsTab.tsx
  - components\flow-designer\properties\NodePopover.tsx
  - components\flow-designer\properties\OracleTab.tsx
  - components\flow-designer\properties\PropertyPanel.tsx
  - components\flow-designer\properties\ResourcesTab.tsx
  - components\flow-designer\properties\TimingTab.tsx
  - components\flow-designer\responsive\FocusMode.tsx
  - components\flow-designer\responsive\MobileControls.tsx
  - components\flow-designer\responsive\ResponsiveLayout.tsx
  - components\flow-designer\responsive\SlideUpPanel.tsx
  - components\flow-designer\simulation\ProgressPanel.tsx
  - components\flow-designer\simulation\ResultsPreview.tsx
  - components\flow-designer\simulation\SimConfigPanel.tsx
  - components\flow-designer\simulation\SimulateOverlay.tsx
  - components\flow-designer\simulation\SimulationConfig.tsx
  - components\flow-designer\simulation\SimulationPanel.tsx
  - components\flow-designer\simulation\simNodeStyle.ts
  - components\flow-designer\simulation\useSimulationLayer.ts
  - components\flow-designer\tabletop\DecisionPanel.tsx
  - components\flow-designer\tabletop\DecisionPrompt.tsx
  - components\flow-designer\tabletop\FrankSuggestion.tsx
  - components\flow-designer\tabletop\StepProgress.tsx
  - components\flow-designer\tabletop\TabletopChat.tsx

**`../../adapters`** (imported by 1 files)
  - components\flow-designer\FlowDesigner.tsx

**`../../lib/theme`** (imported by 8 files)
  - components\flow-designer\BranchExplorer.tsx
  - components\flow-designer\ContextMenu.tsx
  - components\flow-designer\FlowCanvas.tsx
  - components\flow-designer\FlowDesigner.tsx
  - components\flow-designer\FlowDesignerSkeleton.tsx
  - components\flow-designer\FlowToolbar.tsx
  - components\flow-designer\NodePalette.tsx
  - components\flow-designer\ZoomControls.tsx

## 3. npm Package Dependencies

| Package | Import Count |
|---------|--------------|
| `react` | 105 |
| `@xyflow/react` | 22 |
| `vitest` | 9 |
| `react-dom` | 7 |

**Total Unique Packages:** 4

---

## Executive Summary

### Scope
The Flow Designer is located at `platform/efemera/frontend/src/components/flow-designer/` and comprises **120 files** (excluding the broader src directory context).

### Size & Complexity
- **Total Lines of Code:** ~23,000 lines within flow-designer tree
  - Components: 76 files, ~17,000 lines
  - Hooks: 12 files, ~2,500 lines
  - TypeScript utilities: 15 files, ~2,000 lines
  - Tests: 8 files, ~3,100 lines
  - Store: 1 file, 32 lines

### Module Structure
The Flow Designer is organized into 16 distinct feature modules:

1. **Core** (13 files) — Main designer, canvas, toolbar, palette, state management
2. **Nodes** (4 files) — Phase, Checkpoint, Group, Resource nodes
3. **Edges** (3 files) — Phase edges, Token edges, timing editor
4. **Animation** (8 files) — Token animation, node pulse, sim clock, resource bars
5. **Modes** (5 files) — Design, Simulate, Tabletop, Playback, Compare
6. **File Operations** (8 files + 4 importers) — Save, Load, Export, Import, serialization, BPMN/SBML/L-systems importers
7. **Properties** (8 files) — Property panel with 7 specialized tabs (General, Timing, Actions, Guards, Resources, Oracle)
8. **Simulation** (11 files) — Local DES engine, config, progress, results, overlays
9. **Playback** (7 files) — Controls, timeline, event list, speed metrics
10. **Tabletop** (7 files) — Graph walker, decision prompts, Frank AI suggestions
11. **Checkpoints** (3 files) — Checkpoint manager, timeline, persistence
12. **Collaboration** (5 files) — Live cursors, node comments, Design Flight mode
13. **Compare** (6 files) — Split canvas, diff algorithm, metrics, snapshot storage
14. **Responsive** (7 files) — Mobile controls, touch gestures, breakpoints, slide-up panel
15. **Telemetry** (2 files) — Event ledger, event type definitions
16. **Overlays** (3 files) — Timing badges, distribution tooltips, variable pills

### External Dependencies — CRITICAL FOR PORT

The Flow Designer has **4 external module dependencies** from the platform repo:

#### 1. `lib/theme` (74 files depend on it)
**Provides:** `colors` (31 color tokens), `fonts` (sans, mono)
**Type:** Design tokens
**Port Strategy:** Replace with ShiftCenter's CSS variable system (`var(--sd-*)`)

#### 2. `lib/auth` (7 files depend on it)
**Provides:** `getToken()`, `getUser()`, `getAuthHeaders()`, `isAuthenticated()`
**Type:** Authentication utilities
**Port Strategy:** Map to ShiftCenter's `hivenode/auth/jwt.py` + `browser/src/services/auth.ts`

#### 3. `lib/config` (2 files depend on it)
**Provides:** `API_URL`, `WS_URL`, `RAQCOON_URL` (Vite env vars)
**Type:** Environment configuration
**Port Strategy:** Map to ShiftCenter's `.env` + `browser/src/config.ts`

#### 4. `adapters` (4 files depend on it)
**Provides:** `ApiClientProvider`, `useApiClient()`, `PhaseAPIClient` interface
**Type:** Phase API client (HTTP + types)
**Port Strategy:** Map to ShiftCenter's `browser/src/services/api.ts` + Phase-IR backend routes

### npm Dependencies
- **react** (105 imports) — Already in ShiftCenter
- **@xyflow/react** (22 imports) — Need to add to ShiftCenter
- **vitest** (9 imports in tests) — Already in ShiftCenter
- **react-dom** (7 imports) — Already in ShiftCenter

### Port Complexity Assessment
- **Direct port files:** ~90 files (components, hooks, utilities) — mostly self-contained
- **Refactor needed:** ~30 files (those importing lib/theme) — replace hardcoded colors with CSS vars
- **Integration points:** 4 adapters, 7 auth calls, 2 config usages — map to ShiftCenter equivalents
- **New npm package:** `@xyflow/react` — add to package.json

### Recommended Port Sequence
1. **Wave 1:** Core ReactFlow wrapper + basic nodes (Phase, Group)
2. **Wave 2:** File operations + serialization (needed for save/load)
3. **Wave 3:** Simulation mode + local DES engine
4. **Wave 4:** Playback + Tabletop modes
5. **Wave 5:** Collaboration + Compare modes
6. **Wave 6:** Advanced features (checkpoints, responsive, telemetry)

