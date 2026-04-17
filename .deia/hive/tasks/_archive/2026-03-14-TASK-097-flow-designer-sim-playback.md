# TASK-097: Port Flow Designer Simulation + Playback

**Role:** BEE
**Model:** sonnet
**Priority:** P0
**Briefing:** 2026-03-14-BRIEFING-flow-designer-port.md

## Objective

Port 18 files from the flow designer's simulation and playback subdirectories.

## Source Base

`C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\frontend\src\components\flow-designer\`

## Destination Base

`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\`

## Files to Port

### Simulation — 11 files
| Source File | Lines |
|-------------|-------|
| `simulation/LocalDESEngine.ts` | 230 |
| `simulation/ProgressPanel.tsx` | 276 |
| `simulation/ResultsPreview.tsx` | 156 |
| `simulation/SimConfigPanel.tsx` | 293 |
| `simulation/SimulateOverlay.tsx` | 181 |
| `simulation/SimulationConfig.tsx` | 320 |
| `simulation/SimulationPanel.tsx` | 619 |
| `simulation/SimulationResultsStore.ts` | 32 |
| `simulation/simNodeStyle.ts` | 32 |
| `simulation/useSimulation.ts` | 461 |
| `simulation/useSimulationLayer.ts` | 98 |

### Playback — 7 files
| Source File | Lines |
|-------------|-------|
| `playback/EventList.tsx` | 241 |
| `playback/PlaybackControls.tsx` | 203 |
| `playback/PlaybackTimeline.tsx` | 248 |
| `playback/SpeedMetrics.tsx` | 241 |
| `playback/SpeedSelector.tsx` | 157 |
| `playback/usePlayback.ts` | 249 |
| `playback/usePlaybackLayer.ts` | 61 |

## Instructions

1. Read each source file from the platform repo
2. Write it to the matching destination path — **NO CHANGES to the code**
3. After writing all files, count lines in each destination file
4. Report before/after line counts in a table

## Enhancement Log

Append observations to: `.deia/hive/responses/20260314-FLOW-DESIGNER-PORT-ENHANCEMENTS.md`

## Output

Write response to: `.deia/hive/responses/20260314-TASK-097-RESPONSE.md`
