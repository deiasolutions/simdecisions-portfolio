# TASK-096: Port Flow Designer Modes + Properties + Responsive

**Role:** BEE
**Model:** sonnet
**Priority:** P0
**Briefing:** 2026-03-14-BRIEFING-flow-designer-port.md

## Objective

Port 20 files from the flow designer's modes, properties, and responsive subdirectories.

## Source Base

`C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\frontend\src\components\flow-designer\`

## Destination Base

`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\`

## Files to Port

### Modes — 5 files
| Source File | Lines |
|-------------|-------|
| `modes/CompareMode.tsx` | 268 |
| `modes/DesignMode.tsx` | 196 |
| `modes/PlaybackMode.tsx` | 352 |
| `modes/SimulateMode.tsx` | 601 |
| `modes/TabletopMode.tsx` | 339 |

### Properties — 8 files
| Source File | Lines |
|-------------|-------|
| `properties/ActionsTab.tsx` | 234 |
| `properties/GeneralTab.tsx` | 103 |
| `properties/GuardsTab.tsx` | 170 |
| `properties/NodePopover.tsx` | 187 |
| `properties/OracleTab.tsx` | 215 |
| `properties/PropertyPanel.tsx` | 195 |
| `properties/ResourcesTab.tsx` | 238 |
| `properties/TimingTab.tsx` | 151 |

### Responsive — 7 files
| Source File | Lines |
|-------------|-------|
| `responsive/FocusMode.tsx` | 212 |
| `responsive/MobileControls.tsx` | 119 |
| `responsive/ResponsiveLayout.tsx` | 141 |
| `responsive/SlideUpPanel.tsx` | 193 |
| `responsive/TouchGestures.tsx` | 157 |
| `responsive/index.ts` | 11 |
| `responsive/useBreakpoint.ts` | 53 |

## Instructions

1. Read each source file from the platform repo
2. Write it to the matching destination path — **NO CHANGES to the code**
3. After writing all files, count lines in each destination file
4. Report before/after line counts in a table

## Enhancement Log

Append observations to: `.deia/hive/responses/20260314-FLOW-DESIGNER-PORT-ENHANCEMENTS.md`

## Output

Write response to: `.deia/hive/responses/20260314-TASK-096-RESPONSE.md`
