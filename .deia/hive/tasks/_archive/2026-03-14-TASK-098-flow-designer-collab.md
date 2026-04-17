# TASK-098: Port Flow Designer Tabletop + Checkpoints + Collaboration + Compare

**Role:** BEE
**Model:** sonnet
**Priority:** P0
**Briefing:** 2026-03-14-BRIEFING-flow-designer-port.md

## Objective

Port 21 files from the flow designer's tabletop, checkpoints, collaboration, and compare subdirectories.

## Source Base

`C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\frontend\src\components\flow-designer\`

## Destination Base

`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\`

## Files to Port

### Tabletop — 7 files
| Source File | Lines |
|-------------|-------|
| `tabletop/DecisionPanel.tsx` | 425 |
| `tabletop/DecisionPrompt.tsx` | 219 |
| `tabletop/FrankSuggestion.tsx` | 158 |
| `tabletop/LocalGraphWalker.ts` | 170 |
| `tabletop/StepProgress.tsx` | 134 |
| `tabletop/TabletopChat.tsx` | 445 |
| `tabletop/useTabletop.ts` | 405 |

### Checkpoints — 3 files
| Source File | Lines |
|-------------|-------|
| `checkpoints/CheckpointManager.tsx` | 322 |
| `checkpoints/CheckpointTimeline.tsx` | 361 |
| `checkpoints/useCheckpoints.ts` | 276 |

### Collaboration — 5 files
| Source File | Lines |
|-------------|-------|
| `collaboration/DesignFlight.tsx` | 321 |
| `collaboration/LiveCursors.tsx` | 120 |
| `collaboration/NodeComments.tsx` | 358 |
| `collaboration/useCollaboration.ts` | 433 |
| `collaboration/useCollaborationLayer.ts` | 120 |

### Compare — 6 files
| Source File | Lines |
|-------------|-------|
| `compare/DiffHighlighter.tsx` | 344 |
| `compare/MetricsPanel.tsx` | 250 |
| `compare/SplitCanvas.tsx` | 327 |
| `compare/diffAlgorithm.ts` | 347 |
| `compare/snapshotStorage.ts` | 34 |
| `compare/useCompare.ts` | 216 |

## Instructions

1. Read each source file from the platform repo
2. Write it to the matching destination path — **NO CHANGES to the code**
3. After writing all files, count lines in each destination file
4. Report before/after line counts in a table

## Enhancement Log

Append observations to: `.deia/hive/responses/20260314-FLOW-DESIGNER-PORT-ENHANCEMENTS.md`

## Output

Write response to: `.deia/hive/responses/20260314-TASK-098-RESPONSE.md`
