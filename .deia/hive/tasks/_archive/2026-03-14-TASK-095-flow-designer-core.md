# TASK-095: Port Flow Designer Core + Nodes + Edges + Overlays + Telemetry

**Role:** BEE
**Model:** sonnet
**Priority:** P0
**Briefing:** 2026-03-14-BRIEFING-flow-designer-port.md

## Objective

Port 25 files from the flow designer's core, nodes, edges, overlays, and telemetry subdirectories.

## Source Base

`C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\frontend\src\components\flow-designer\`

## Destination Base

`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\`

## Files to Port

### Core (root level) — 13 files
| Source File | Lines |
|-------------|-------|
| `BranchExplorer.tsx` | 260 |
| `ContextMenu.tsx` | 151 |
| `FlowCanvas.tsx` | 143 |
| `FlowDesigner.tsx` | 768 |
| `FlowDesignerSkeleton.tsx` | 109 |
| `FlowToolbar.tsx` | 300 |
| `NodePalette.tsx` | 165 |
| `ZoomControls.tsx` | 124 |
| `demoFlow.ts` | 95 |
| `index.ts` | 49 |
| `types.ts` | 200 |
| `useFlowState.ts` | 300 |
| `useNodeEditing.ts` | 221 |

### Nodes — 4 files
| Source File | Lines |
|-------------|-------|
| `nodes/CheckpointNode.tsx` | 158 |
| `nodes/GroupNode.tsx` | 86 |
| `nodes/PhaseNode.tsx` | 170 |
| `nodes/ResourceNode.tsx` | 130 |

### Edges — 3 files
| Source File | Lines |
|-------------|-------|
| `edges/EdgeTimingEditor.tsx` | 212 |
| `edges/PhaseEdge.tsx` | 307 |
| `edges/TokenEdge.tsx` | 147 |

### Overlays — 3 files
| Source File | Lines |
|-------------|-------|
| `overlays/DistributionTooltip.tsx` | 183 |
| `overlays/TimingBadge.tsx` | 83 |
| `overlays/VariablePill.tsx` | 87 |

### Telemetry — 2 files
| Source File | Lines |
|-------------|-------|
| `telemetry/eventTypes.ts` | 255 |
| `telemetry/useEventLedger.ts` | 166 |

## Instructions

1. Read each source file from the platform repo
2. Write it to the matching destination path — **NO CHANGES to the code**
3. After writing all files, count lines in each destination file
4. Report before/after line counts in a table

## Enhancement Log

Append observations to: `.deia/hive/responses/20260314-FLOW-DESIGNER-PORT-ENHANCEMENTS.md`

## Output

Write response to: `.deia/hive/responses/20260314-TASK-095-RESPONSE.md`
