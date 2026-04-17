# TASK-094: Port Flow Designer Dependencies

**Role:** BEE
**Model:** haiku
**Priority:** P0
**Briefing:** 2026-03-14-BRIEFING-flow-designer-port.md

## Objective

Port the 9 dependency files that the Flow Designer imports from outside its directory.

## Source → Destination

All source files are in: `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\frontend\src\`
All destination files go to: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\`

| Source | Destination | Lines |
|--------|------------|-------|
| `lib/theme.ts` | `browser/src/apps/sim/lib/theme.ts` | 30 |
| `lib/auth.ts` | `browser/src/apps/sim/lib/auth.ts` | 48 |
| `lib/config.ts` | `browser/src/apps/sim/lib/config.ts` | 3 |
| `lib/ws.ts` | `browser/src/apps/sim/lib/ws.ts` | 126 |
| `lib/useMobile.ts` | `browser/src/apps/sim/lib/useMobile.ts` | 10 |
| `lib/icons.tsx` | `browser/src/apps/sim/lib/icons.tsx` | 10 |
| `adapters/api-client.ts` | `browser/src/apps/sim/adapters/api-client.ts` | 620 |
| `adapters/ApiClientContext.tsx` | `browser/src/apps/sim/adapters/ApiClientContext.tsx` | 62 |
| `adapters/index.ts` | `browser/src/apps/sim/adapters/index.ts` | 44 |

## Instructions

1. Read each source file
2. Write it to the destination path — **NO CHANGES to the code**
3. After writing all files, count lines in each destination file
4. Report before/after line counts

## Enhancement Log

If you notice anything worth noting (e.g. hardcoded URLs, deprecated patterns, platform-specific assumptions), append to:
`.deia/hive/responses/20260314-FLOW-DESIGNER-PORT-ENHANCEMENTS.md`

## Output

Write response to: `.deia/hive/responses/20260314-TASK-094-RESPONSE.md`
