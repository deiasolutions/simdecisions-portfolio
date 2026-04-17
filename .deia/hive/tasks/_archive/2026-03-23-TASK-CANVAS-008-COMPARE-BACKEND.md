# TASK-CANVAS-008: Wire Compare Mode to Backend API

## Objective
Transform CompareMode from SHELL (client-only diffAlgorithm) to WIRED (backend API). Currently uses client-side diff computation with no server caching. Must wire to backend for server-side diff caching and scenario comparison persistence.

## Context
CompareMode UI exists (`modes/CompareMode.tsx`, 298 lines) with SplitCanvas, DiffHighlighter, snapshotStorage. But NO backend API. Audit report lines 41, 139 confirm it's a shell.

Old platform CompareView (299 lines) likely had backend diff support.

Compare mode allows users to:
1. Load two flow snapshots (base vs compare)
2. View side-by-side canvases
3. Highlight differences (added nodes, deleted nodes, changed properties)
4. Navigate between diffs

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\modes\CompareMode.tsx` (current UI, 298 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\compare\diffAlgorithm.ts` (client-side diff logic)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\compare\snapshotStorage.ts` (localStorage snapshots)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\mode-views\CompareView.tsx` (old implementation, 299 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py` (pattern for new routes)

## CRITICAL ARCHITECTURE REQUIREMENT
Compare mode panels (snapshot list, diff summary, metrics) MUST be shell panes defined in the EGG, NOT custom absolute-positioned divs. Use the pane adapter pattern established by TASK-CANVAS-000. The dual canvas should be two shell panes side-by-side, defined in canvas.egg.md under compare mode layout. Diff highlighting and navigation controls go in a proper pane, not a floating overlay.

## Deliverables
- [ ] Compare panels as pane adapters: `browser/src/apps/sim/adapters/comparePaneAdapter.tsx`
- [ ] Update `canvas.egg.md` to define compare mode pane layout (base canvas left, compare canvas right, diff summary bottom or sidebar)
- [ ] Backend API routes in `hivenode/routes/compare_routes.py`:
  - `POST /api/compare/diff` — compute diff between two flows (server-side)
  - `POST /api/compare/snapshot` — store flow snapshot
  - `GET /api/compare/snapshots/{flow_id}` — list snapshots for a flow
  - `DELETE /api/compare/snapshot/{snapshot_id}` — delete snapshot
- [ ] Backend storage: SQLite table `flow_snapshots` (snapshot_id, flow_id, flow_data, created_at, label)
- [ ] Backend diff logic (port diffAlgorithm.ts to Python or reuse as-is via JSON API)
- [ ] Update `compare/snapshotStorage.ts` to use backend (not localStorage)
- [ ] Update CompareMode.tsx to call `/api/compare/diff` for diff computation
- [ ] Register compare routes in `hivenode/routes/__init__.py`
- [ ] Frontend test: `browser/src/apps/sim/components/flow-designer/compare/__tests__/compare-backend.test.tsx`
- [ ] Backend test: `tests/hivenode/test_compare_routes.py`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Diff identical flows — returns empty diff
  - Diff completely different flows — returns all adds + all deletes
  - Snapshot with large flow (1000+ nodes) — stores successfully
  - Delete snapshot that's in use by compare session — handle gracefully
  - List snapshots for flow with no snapshots — returns empty array

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs — full backend API + diff logic
- Use SQLAlchemy for flow_snapshots table
- Diff algorithm can stay client-side (send flows to backend, backend returns diff)
- OR port diffAlgorithm.ts to Python for server-side compute (your choice, justify in response)

## Acceptance Criteria
- [ ] Backend routes file `compare_routes.py` created
- [ ] SQLite table `flow_snapshots` created
- [ ] POST /api/compare/diff works — returns diff
- [ ] POST /api/compare/snapshot works — stores snapshot
- [ ] GET /api/compare/snapshots/{flow_id} works — lists snapshots
- [ ] DELETE /api/compare/snapshot/{snapshot_id} works — deletes snapshot
- [ ] snapshotStorage.ts uses backend (not localStorage)
- [ ] CompareMode.tsx calls backend diff API
- [ ] Frontend test file exists with 10+ tests
- [ ] Backend test file exists with 12+ tests
- [ ] All existing compare UI tests still pass
- [ ] All existing backend tests still pass

## Response Requirements — MANDATORY
Write response file: `.deia/hive/responses/20260323-TASK-CANVAS-008-RESPONSE.md` with all 8 sections.
