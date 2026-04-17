# TASK-CANVAS-006: Wire Playback Mode to Backend API

## Objective
Transform PlaybackMode from SHELL (localStorage-only) to WIRED (backend API). Currently reads simulation events from client-side SimulationResultsStore. Must wire to backend for server-side event storage, multi-user replay, and session persistence.

## Context
PlaybackMode UI exists (`modes/PlaybackMode.tsx`, 378 lines) with full UI: PlaybackControls, PlaybackTimeline, EventList. But NO backend API. Audit report lines 39, 129 confirm it's a shell.

Old platform PlaybackView (313 lines) likely had backend integration. Check for `/api/playback/*` routes or similar.

Playback mode allows users to:
1. Replay simulation results step-by-step
2. Control playback speed (0.5x, 1x, 2x, 4x)
3. Scrub timeline to specific events
4. View event details (node activated, token moved, resource acquired)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\modes\PlaybackMode.tsx` (current UI, 378 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\playback\` (all playback components)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\mode-views\PlaybackView.tsx` (old implementation, 313 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py` (may need new routes)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\des\` (check for playback API in old backend)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\simulation\SimulationResultsStore.ts` (current localStorage store)

## CRITICAL ARCHITECTURE REQUIREMENT
Playback controls MUST be a shell pane defined in the EGG, NOT a custom absolute-positioned div. Use the pane adapter pattern established by TASK-CANVAS-000 (`playbackControlsPaneAdapter.tsx`). Panels communicate via MessageBus events (`sim:playback-control`), not React props. If CANVAS-000 has not run yet, create the adapter yourself following the pattern in `browser/src/apps/textPaneAdapter.tsx`.

## Deliverables
- [ ] Backend API routes in `hivenode/routes/playback_routes.py`:
  - `POST /api/playback/store` — store simulation events server-side
  - `GET /api/playback/{flow_id}/{run_id}` — retrieve events for playback
  - `GET /api/playback/{flow_id}/runs` — list all runs for a flow
  - `DELETE /api/playback/{flow_id}/{run_id}` — delete playback session
- [ ] Backend storage: SQLite table `playback_events` (flow_id, run_id, event_index, event_type, event_data, timestamp)
- [ ] Update `usePlaybackLayer.ts` to fetch events from backend instead of localStorage
- [ ] Migrate existing SimulationResultsStore to server on first load (optional migration)
- [ ] Register playback routes in `hivenode/routes/__init__.py`
- [ ] Frontend test: `browser/src/apps/sim/components/flow-designer/playback/__tests__/playback-backend.test.tsx`
- [ ] Backend test: `tests/hivenode/test_playback_routes.py` (CRUD operations on playback events)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Store events for non-existent flow_id — creates new entry
  - Retrieve events for non-existent run_id — returns 404
  - Delete playback session — events removed, subsequent GET returns 404
  - Large event set (10,000+ events) — pagination or streaming (if needed)
  - Concurrent playback of same run by multiple users — read-only, no conflicts

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs — full backend API implementation
- Use SQLAlchemy for playback_events table (match existing hivenode patterns)
- Events stored as JSON blobs (event_data column)
- Backend API must support CORS (same as existing DES routes)

## Acceptance Criteria
- [ ] Backend routes file `playback_routes.py` created
- [ ] SQLite table `playback_events` created (schema in store module)
- [ ] POST /api/playback/store works — stores events
- [ ] GET /api/playback/{flow_id}/{run_id} works — retrieves events
- [ ] GET /api/playback/{flow_id}/runs works — lists runs
- [ ] DELETE /api/playback/{flow_id}/{run_id} works — deletes session
- [ ] usePlaybackLayer.ts fetches from backend (not localStorage)
- [ ] Frontend test file exists with 8+ tests
- [ ] Backend test file exists with 12+ tests (CRUD + edge cases)
- [ ] All existing playback UI tests still pass
- [ ] All existing backend tests still pass

## Response Requirements — MANDATORY
Write response file: `.deia/hive/responses/20260323-TASK-CANVAS-006-RESPONSE.md` with all 8 sections.
