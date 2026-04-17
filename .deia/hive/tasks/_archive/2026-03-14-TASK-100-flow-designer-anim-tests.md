# TASK-100: Port Flow Designer Animation + Tests

**Role:** BEE
**Model:** sonnet
**Priority:** P0
**Briefing:** 2026-03-14-BRIEFING-flow-designer-port.md

## Objective

Port 16 files: the animation subdirectory and all test files.

## Source Base

`C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\frontend\src\components\flow-designer\`

## Destination Base

`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\`

## Files to Port

### Animation — 8 files
| Source File | Lines |
|-------------|-------|
| `animation/CheckpointFlash.tsx` | 130 |
| `animation/NodePulse.tsx` | 73 |
| `animation/QueueBadge.tsx` | 71 |
| `animation/ResourceBar.tsx` | 84 |
| `animation/SimClock.tsx` | 173 |
| `animation/TokenAnimation.tsx` | 96 |
| `animation/index.ts` | 13 |
| `animation/useAnimationFrame.ts` | 36 |

### Tests — 8 files
| Source File | Lines |
|-------------|-------|
| `__tests__/FileOperations.test.tsx` | 553 |
| `__tests__/FlowToolbar.test.tsx` | 364 |
| `__tests__/Modes.test.tsx` | 1165 |
| `__tests__/NodePalette.test.tsx` | 215 |
| `__tests__/PropertyPanel.test.tsx` | 243 |
| `__tests__/serialization.test.ts` | 512 |
| `simulation/__tests__/LocalDESEngine.test.ts` | 39 |
| `tabletop/__tests__/LocalGraphWalker.test.ts` | 41 |

## Instructions

1. Read each source file from the platform repo
2. Write it to the matching destination path — **NO CHANGES to the code**
3. After writing all files, count lines in each destination file
4. Report before/after line counts in a table

## Enhancement Log

Append observations to: `.deia/hive/responses/20260314-FLOW-DESIGNER-PORT-ENHANCEMENTS.md`

## Output

Write response to: `.deia/hive/responses/20260314-TASK-100-RESPONSE.md`
