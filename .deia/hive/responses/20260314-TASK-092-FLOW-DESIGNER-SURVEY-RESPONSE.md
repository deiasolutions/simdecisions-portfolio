# TASK-092: Flow Designer Directory Survey + Dependency Analysis -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-14

## Files Modified

### Created
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\scripts\analyze_flow_designer.py` (analysis script)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-092-FLOW-DESIGNER-SURVEY.md` (full survey report)

## What Was Done

1. **Located Flow Designer source directory** at `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\frontend\src`
2. **Created comprehensive analysis script** that:
   - Recursively walked entire src directory tree
   - Classified files by type (component, hook, store, test, typescript, css, config)
   - Counted non-blank lines in each file
   - Extracted and categorized ALL import statements
   - Identified imports escaping the flow-designer tree boundary
3. **Analyzed 153 total files** (120 specifically in flow-designer subdirectory):
   - 101 components (21,148 lines)
   - 16 hooks (3,256 lines)
   - 24 TypeScript utilities (3,801 lines)
   - 10 test files (3,836 lines)
   - 1 store (32 lines)
   - 1 CSS file (100 lines)
4. **Identified 87 external imports from 6 unique modules**:
   - `lib/theme` — 74 files (colors + fonts design tokens)
   - `lib/auth` — 7 files (JWT utilities)
   - `lib/config` — 2 files (env vars)
   - `adapters` — 4 files (Phase API client)
5. **Analyzed dependency module contents** by reading source files:
   - `lib/theme.ts` — 31 color tokens + 2 font families (hardcoded)
   - `lib/auth.ts` — JWT token storage, user state, auth headers
   - `lib/config.ts` — 3 env vars (API_URL, WS_URL, RAQCOON_URL)
   - `adapters/index.ts` — Phase API client with CloudAPIClient/LocalAPIClient
6. **Compiled npm package usage**:
   - react (105 imports) — already in ShiftCenter
   - @xyflow/react (22 imports) — NEW, must add
   - vitest (9 imports) — already in ShiftCenter
   - react-dom (7 imports) — already in ShiftCenter
7. **Generated executive summary** with:
   - Module structure breakdown (16 feature modules)
   - External dependency analysis and port strategies
   - Port complexity assessment
   - Recommended 6-wave port sequence

## Key Findings

**Flow Designer Statistics:**
- **Total files in flow-designer tree:** 120 files
- **Total lines of code:** ~23,000 lines
- **Module count:** 16 distinct feature modules

**16 Feature Modules:**
1. Core (13 files) — Main designer, canvas, toolbar, palette
2. Nodes (4 files) — Phase, Checkpoint, Group, Resource
3. Edges (3 files) — Phase edges, Token edges, timing
4. Animation (8 files) — Token animation, pulse, clock, bars
5. Modes (5 files) — Design, Simulate, Tabletop, Playback, Compare
6. File Operations (12 files) — Save, Load, Export, Import + dialect importers
7. Properties (8 files) — Property panel with 7 tabs
8. Simulation (11 files) — Local DES engine, config, progress
9. Playback (7 files) — Controls, timeline, events, speed
10. Tabletop (7 files) — Graph walker, decisions, Frank AI
11. Checkpoints (3 files) — Manager, timeline, persistence
12. Collaboration (5 files) — Live cursors, comments, Design Flight
13. Compare (6 files) — Split canvas, diff algorithm, metrics
14. Responsive (7 files) — Mobile controls, touch, breakpoints
15. Telemetry (2 files) — Event ledger, event types
16. Overlays (3 files) — Timing badges, tooltips, pills

**Critical External Dependencies:**
1. **lib/theme** (74 files depend on it)
   - Provides: 31 color tokens, 2 font families
   - Port Strategy: Replace with ShiftCenter CSS variables (`var(--sd-*)`)
   - Impact: 74 files need find-replace for theme imports
2. **lib/auth** (7 files depend on it)
   - Provides: getToken(), getUser(), getAuthHeaders(), isAuthenticated()
   - Port Strategy: Map to ShiftCenter auth service (hivenode/auth/jwt.py + browser/src/services/auth.ts)
   - Impact: 7 files need import path updates
3. **lib/config** (2 files depend on it)
   - Provides: API_URL, WS_URL, RAQCOON_URL
   - Port Strategy: Map to ShiftCenter .env + browser/src/config.ts
   - Impact: 2 files need import path updates
4. **adapters** (4 files depend on it)
   - Provides: ApiClientProvider, useApiClient(), PhaseAPIClient interface
   - Port Strategy: Map to ShiftCenter API service + Phase-IR backend routes
   - Impact: 4 files need integration adapter

**npm Dependencies:**
- **@xyflow/react** — NEW dependency, must add to ShiftCenter package.json
- All other packages already present

**Port Complexity Assessment:**
- **Direct port:** ~90 files (mostly self-contained components/hooks)
- **Refactor needed:** ~30 files (theme replacements)
- **Integration needed:** 4 adapters + 7 auth calls + 2 config usages
- **New dependency:** 1 npm package (@xyflow/react)
- **Estimated effort:** Medium complexity, 6 waves recommended

## Output Location

Full survey report with all file listings, dependency tables, and analysis:
`.deia\hive\responses\20260314-TASK-092-FLOW-DESIGNER-SURVEY.md`

Total report size: 620 lines including:
- Complete file inventory (16 directory groups)
- External dependency analysis (87 imports detailed)
- Grouped imports by module
- npm package statistics
- Executive summary with port strategies
