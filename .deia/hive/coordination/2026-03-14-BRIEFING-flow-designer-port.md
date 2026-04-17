# BRIEFING: Port Flow Designer to ShiftCenter

**Date:** 2026-03-14
**From:** Q88NR
**To:** Q33N
**Priority:** P0

## Objective

Port the entire Flow Designer (~120 files, ~23,000 lines) from platform to shiftcenter. Change as little as possible. The user WILL compare before/after line counts.

## CRITICAL RULES

1. **PORT, don't rewrite.** Copy files faithfully. Minimal changes.
2. **If a dependency is missing, PORT THE DEPENDENCY.** Do NOT rewrite dependent code.
3. **Line counts matter.** Before/after should be nearly identical.
4. **Log enhancement suggestions** — don't fix them now.

## Source

`C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\frontend\src\`

## Destination

`browser/src/apps/sim/` — mirror the platform directory structure so relative imports stay intact.

```
browser/src/apps/sim/
  lib/
    theme.ts          ← from platform lib/theme.ts (30 lines)
    auth.ts           ← from platform lib/auth.ts (48 lines)
    config.ts         ← from platform lib/config.ts (3 lines)
    ws.ts             ← from platform lib/ws.ts (126 lines)
    useMobile.ts      ← from platform lib/useMobile.ts (10 lines)
    icons.tsx         ← from platform lib/icons.tsx (10 lines)
  adapters/
    api-client.ts     ← from platform adapters/api-client.ts (620 lines)
    ApiClientContext.tsx ← from platform adapters/ApiClientContext.tsx (62 lines)
    index.ts          ← from platform adapters/index.ts (44 lines)
  components/flow-designer/   ← ALL 120 files from platform components/flow-designer/
```

This structure preserves ALL relative import paths. `../../lib/theme` from `components/flow-designer/FlowDesigner.tsx` resolves correctly.

## External Dependencies (4 modules, 87 import sites)

### 1. `lib/theme` (74 files import it)
- Provides: `colors` object (31 color tokens), `fonts` object (sans, mono)
- Port as-is. Note for later: "migrate to CSS vars" as enhancement.

### 2. `lib/auth` (7 files import it)
- Provides: `getToken()`, `getUser()`, `getAuthHeaders()`, `isAuthenticated()`
- Port as-is. Will need runtime wiring to shiftcenter auth later.

### 3. `lib/config` (2 files import it)
- Provides: `API_URL`, `WS_URL` from Vite env vars
- Port as-is.

### 4. `adapters/` (4 files import it)
- Provides: `ApiClientProvider`, `useApiClient()`, `PhaseAPIClient`
- Port as-is.

## File Inventory (from TASK-092)

| Group | Files | Lines | Source Subdir |
|-------|-------|-------|---------------|
| Dependencies | 9 | 953 | lib/ + adapters/ |
| Core | 13 | 2,885 | components/flow-designer/ (root) |
| Nodes | 4 | 544 | components/flow-designer/nodes/ |
| Edges | 3 | 666 | components/flow-designer/edges/ |
| Animation | 8 | 676 | components/flow-designer/animation/ |
| Modes | 5 | 1,756 | components/flow-designer/modes/ |
| File Ops | 8 | 2,883 | components/flow-designer/file-ops/ |
| Dialect Importers | 4 | 933 | components/flow-designer/file-ops/dialect-importers/ |
| Properties | 8 | 1,493 | components/flow-designer/properties/ |
| Simulation | 11 | 2,698 | components/flow-designer/simulation/ |
| Playback | 7 | 1,400 | components/flow-designer/playback/ |
| Tabletop | 7 | 1,956 | components/flow-designer/tabletop/ |
| Checkpoints | 3 | 959 | components/flow-designer/checkpoints/ |
| Collaboration | 5 | 1,352 | components/flow-designer/collaboration/ |
| Compare | 6 | 1,518 | components/flow-designer/compare/ |
| Responsive | 7 | 886 | components/flow-designer/responsive/ |
| Telemetry | 2 | 421 | components/flow-designer/telemetry/ |
| Overlays | 3 | 353 | components/flow-designer/overlays/ |
| Tests | 8 | 3,132 | components/flow-designer/__tests__/ + inline |
| **TOTAL** | **125** | **26,464** | |

## Dispatch Plan

Break into waves. Each wave is one bee task. Wave 0 goes first (deps). Rest can be parallel.

### Wave 0: Dependencies (TASK-094)
- lib/ (6 files) + adapters/ (3 files) = 9 files, 953 lines
- Model: haiku (simple copy)

### Wave 1: Core + Nodes + Edges + Overlays + Telemetry (TASK-095)
- 25 files, ~4,869 lines
- Model: sonnet

### Wave 2: Modes + Properties + Responsive (TASK-096)
- 20 files, ~4,135 lines
- Model: sonnet

### Wave 3: Simulation + Playback (TASK-097)
- 18 files, ~4,098 lines
- Model: sonnet

### Wave 4: Tabletop + Checkpoints + Collaboration + Compare (TASK-098)
- 21 files, ~5,785 lines
- Model: sonnet

### Wave 5: File Ops + Dialect Importers (TASK-099)
- 12 files, ~3,816 lines
- Model: sonnet

### Wave 6: Animation + Tests (TASK-100)
- 16 files, ~3,808 lines
- Model: sonnet

### Wave 7: Summary + line count verification (TASK-101)
- Read-only. Compare before/after. Compile enhancement notes.
- Model: haiku

## Enhancement Log

Each bee MUST append any observations to this file:
`.deia/hive/responses/20260314-FLOW-DESIGNER-PORT-ENHANCEMENTS.md`

Format:
```
## [TASK-XXX] Enhancement Notes
- FILE: path — OBSERVATION: what could be improved
```

Do NOT fix anything. Just log it.
