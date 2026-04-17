# BRIEFING: Canvas Full Port — Wave 3 Dispatch (Backend Wiring)

**Date:** 2026-03-23
**From:** Q33NR
**To:** Q33N
**Priority:** HIGH — dispatch as soon as Wave 2 completes

## Context

This is the final wave of the Canvas Full Port build. 14 bees across 3 waves.

**Wave 1 (6 bees):** Foundation — pane architecture, IR pipeline, node types, annotations, ELK layout
**Wave 2 (5 bees):** Modes + features — Configure, Optimize, lasso, smart handles, property tabs
**Wave 3 (3 bees):** Backend wiring — transform 3 shell modes into fully wired systems

All 3 Wave 3 tasks take existing UI-only shell modes and wire them to backend APIs with server-side storage, proper pane adapters, and EGG definitions.

## Wave 3 Task Files (Already Written)

### 1. CANVAS-006: Wire Playback Mode to Backend
- **File:** `.deia/hive/tasks/2026-03-23-TASK-CANVAS-006-PLAYBACK-BACKEND.md`
- **What:** Backend API for simulation event storage + replay. Currently reads from localStorage. After this: server-side event storage, multi-user replay, session persistence.
- **Backend routes:** `POST /api/playback/store`, `GET /api/playback/{flow_id}/{run_id}`, `GET /api/playback/{flow_id}/runs`, `DELETE /api/playback/{flow_id}/{run_id}`
- **Pane requirement:** Playback controls must be a shell pane via adapter, defined in canvas.egg.md
- **Depends on:** CANVAS-000 (pane adapter pattern)
- **Model:** sonnet

### 2. CANVAS-007: Wire Tabletop Mode to Backend
- **File:** `.deia/hive/tasks/2026-03-23-TASK-CANVAS-007-TABLETOP-BACKEND.md`
- **What:** Backend API for LLM-guided walkthrough sessions. Currently runs client-side LocalGraphWalker with no persistence. After this: server-side session state, graph walker logic on backend, multi-user tabletop.
- **Backend routes:** `POST /api/tabletop/start`, `GET /api/tabletop/{session_id}`, `POST /api/tabletop/{session_id}/advance`, `POST /api/tabletop/{session_id}/restart`, `DELETE /api/tabletop/{session_id}`
- **Pane requirement:** TabletopChat must be a shell pane via adapter, defined in canvas.egg.md
- **Depends on:** CANVAS-000 (pane adapter pattern)
- **Model:** sonnet

### 3. CANVAS-008: Wire Compare Mode to Backend
- **File:** `.deia/hive/tasks/2026-03-23-TASK-CANVAS-008-COMPARE-BACKEND.md`
- **What:** Backend API for flow snapshot storage + server-side diff computation. Currently uses client-side diffAlgorithm.ts and localStorage. After this: server-cached diffs, persistent snapshots, proper dual-canvas layout.
- **Backend routes:** `POST /api/compare/diff`, `POST /api/compare/snapshot`, `GET /api/compare/snapshots/{flow_id}`, `DELETE /api/compare/snapshot/{snapshot_id}`
- **Pane requirement:** Compare panels and dual canvases must be shell panes, defined in canvas.egg.md
- **Depends on:** CANVAS-000 (pane adapter pattern)
- **Model:** sonnet

## Pre-Dispatch Checklist (Q33N Must Do)

1. **Read ALL Wave 1 + Wave 2 response files** — confirm no failures or partial completions
2. **Verify CANVAS-000 pane architecture is solid** — all 3 Wave 3 tasks build pane adapters on this pattern. If 000 had issues, fix them first.
3. **Verify modes exist** — CANVAS-004 (Configure) and CANVAS-005 (Optimize) should be in place. Wave 3 tasks modify mode registration and EGG layout alongside them.
4. **Run full test suite:**
   - `cd browser && npx vitest run src/apps/sim/` (frontend)
   - `cd hivenode && python -m pytest tests/ -v` (backend — new routes will be added)
5. **Check canvas.egg.md** — multiple Wave 1+2 bees may have edited it. Resolve any conflicts before Wave 3 bees add more pane definitions.
6. **Check hivenode/routes/__init__.py** — Wave 3 adds 3 new route modules (playback, tabletop, compare). Verify the registration pattern is clean.

## Dispatch Strategy

All 3 bees can run in parallel — they touch different backend route files and different frontend adapters:
- CANVAS-006: `playback_routes.py` + `playbackControlsPaneAdapter.tsx`
- CANVAS-007: `tabletop_routes.py` + `tabletopChatPaneAdapter.tsx`
- CANVAS-008: `compare_routes.py` + `comparePaneAdapter.tsx`

**Shared files (conflict risk):**
- `hivenode/routes/__init__.py` — all 3 add route registrations. Dispatch all 3 but check for merge conflicts after.
- `eggs/canvas.egg.md` — all 3 add mode pane layouts. Same risk.

If conflict risk is too high, dispatch sequentially: 006 → 007 → 008.

## After Wave 3

When all 3 bees complete:

1. **Run full test suite** — frontend + backend
2. **Verify all modes work end-to-end:**
   - Design: drag nodes, edit properties, undo/redo
   - Configure: validation panel (pane), sim config (pane), read-only canvas
   - Simulate: backend DES + progress pane + results pane
   - Playback: backend replay + playback controls pane
   - Tabletop: backend session + chat pane
   - Compare: backend diff + dual canvas panes
   - Optimize: parameter sweep + results pane
3. **Verify IR pipeline** — terminal command → LLM → IR → canvas nodes
4. **Verify ELK layout** — toolbar button auto-arranges nodes in all 4 directions
5. **Report to Q33NR** with:
   - Total bees dispatched (14)
   - Pass/fail count
   - Any stubs or failures
   - Remaining gaps (if any)
   - Total cost across all 3 waves

## Rules

- Dispatch through dispatch.py ONLY
- All bees: sonnet model, --inject-boot
- Read each bee's response file when it completes — all 8 sections must be present
- If a bee fails or ships stubs, dispatch a fix task
- After all 3 complete, write a final completion report to `.deia/hive/responses/` summarizing the entire 3-wave build
- Report results to Q33NR
