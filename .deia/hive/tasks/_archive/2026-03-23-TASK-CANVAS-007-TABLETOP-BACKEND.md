# TASK-CANVAS-007: Wire Tabletop Mode to Backend API

## Objective
Transform TabletopMode from SHELL (client-only LocalGraphWalker) to WIRED (backend API). Currently uses client-side graph walk with no persistence. Must wire to backend for session persistence, multi-user support, and LLM-guided walkthrough state.

## Context
TabletopMode UI exists (`modes/TabletopMode.tsx`, 364 lines) with TabletopChat, LocalGraphWalker, decision prompts. But NO backend API. Audit report lines 40, 134 confirm it's a shell.

Old platform had `/api/tabletop/*` routes (needs verification). Check old platform backend.

Tabletop mode is LLM-guided walkthrough:
1. User starts at beginning of flow
2. LLM asks decision questions at each checkpoint
3. User answers, LLM advances to next node
4. Session state persists (current node, history, decisions made)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\modes\TabletopMode.tsx` (current UI, 364 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\tabletop\LocalGraphWalker.ts` (client-side logic)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\mode-views\TabletopView.tsx` (old implementation, 177 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py` (pattern for new routes)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\` (search for tabletop backend)

## CRITICAL ARCHITECTURE REQUIREMENT
Tabletop UI panels (TabletopChat, decision prompts) MUST be shell panes defined in the EGG, NOT custom absolute-positioned divs. Use the pane adapter pattern established by TASK-CANVAS-000. Panels communicate via MessageBus events, not React props. The tabletop chat pane should be a proper shell pane in the left or right slot, defined in canvas.egg.md under tabletop mode layout.

## Deliverables
- [ ] Tabletop chat pane adapter: `browser/src/apps/sim/adapters/tabletopChatPaneAdapter.tsx`
- [ ] Update `canvas.egg.md` to define tabletop mode pane layout (chat pane left or right, canvas center)
- [ ] Backend API routes in `hivenode/routes/tabletop_routes.py`:
  - `POST /api/tabletop/start` — create new tabletop session
  - `GET /api/tabletop/{session_id}` — get session state
  - `POST /api/tabletop/{session_id}/advance` — advance to next node (send user decision)
  - `POST /api/tabletop/{session_id}/restart` — restart session
  - `DELETE /api/tabletop/{session_id}` — delete session
- [ ] Backend storage: SQLite table `tabletop_sessions` (session_id, flow_id, current_node_id, history, decisions, created_at, updated_at)
- [ ] Graph walker logic on backend (port LocalGraphWalker.ts to Python)
- [ ] Update `tabletop/TabletopChat.tsx` to call backend APIs
- [ ] Register tabletop routes in `hivenode/routes/__init__.py`
- [ ] Frontend test: `browser/src/apps/sim/components/flow-designer/tabletop/__tests__/tabletop-backend.test.tsx`
- [ ] Backend test: `tests/hivenode/test_tabletop_routes.py`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Start session on empty flow — error "Flow has no start node"
  - Advance from end node — error "Already at end"
  - Delete session mid-walkthrough — session removed, GET returns 404
  - Restart session — resets to start node, clears history
  - Multiple concurrent sessions for same flow — each has independent state

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs — full backend API + graph walk logic
- Use SQLAlchemy for tabletop_sessions table
- Session state stored as JSON (history, decisions columns)
- Graph walk logic must handle:
  - Start → Task → Checkpoint → Decision → Task → End
  - Multiple outgoing edges from decision node (user picks one)
  - Dead ends (node with no outgoing edges except end node)

## Acceptance Criteria
- [ ] Backend routes file `tabletop_routes.py` created
- [ ] SQLite table `tabletop_sessions` created
- [ ] POST /api/tabletop/start works — creates session
- [ ] GET /api/tabletop/{session_id} works — returns session state
- [ ] POST /api/tabletop/{session_id}/advance works — moves to next node
- [ ] POST /api/tabletop/{session_id}/restart works — resets session
- [ ] DELETE /api/tabletop/{session_id} works — deletes session
- [ ] Graph walker ported to Python (in backend)
- [ ] TabletopChat.tsx calls backend APIs
- [ ] Frontend test file exists with 10+ tests
- [ ] Backend test file exists with 15+ tests (CRUD + graph walk logic)
- [ ] All existing tabletop UI tests still pass
- [ ] All existing backend tests still pass

## Response Requirements — MANDATORY
Write response file: `.deia/hive/responses/20260323-TASK-CANVAS-007-RESPONSE.md` with all 8 sections.
