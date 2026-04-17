# TASK-099: Port Flow Designer File Ops + Dialect Importers

**Role:** BEE
**Model:** sonnet
**Priority:** P0
**Briefing:** 2026-03-14-BRIEFING-flow-designer-port.md

## Objective

Port 12 files from the flow designer's file-ops and dialect-importers subdirectories.

## Source Base

`C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\frontend\src\components\flow-designer\`

## Destination Base

`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\`

## Files to Port

### File Ops — 8 files
| Source File | Lines |
|-------------|-------|
| `file-ops/DownloadPanel.tsx` | 679 |
| `file-ops/ExportDialog.tsx` | 329 |
| `file-ops/FileOperations.tsx` | 220 |
| `file-ops/ImportDialog.tsx` | 536 |
| `file-ops/LoadDialog.tsx` | 313 |
| `file-ops/SaveDialog.tsx` | 202 |
| `file-ops/serialization.ts` | 453 |
| `file-ops/useAutoSave.ts` | 151 |

### Dialect Importers — 4 files
| Source File | Lines |
|-------------|-------|
| `file-ops/dialect-importers/bpmn-importer.ts` | 226 |
| `file-ops/dialect-importers/index.ts` | 138 |
| `file-ops/dialect-importers/lsys-importer.ts` | 284 |
| `file-ops/dialect-importers/sbml-importer.ts` | 285 |

## Instructions

1. Read each source file from the platform repo
2. Write it to the matching destination path — **NO CHANGES to the code**
3. After writing all files, count lines in each destination file
4. Report before/after line counts in a table

## Enhancement Log

Append observations to: `.deia/hive/responses/20260314-FLOW-DESIGNER-PORT-ENHANCEMENTS.md`

## Output

Write response to: `.deia/hive/responses/20260314-TASK-099-RESPONSE.md`
