# TASK-126C: Kanban Frontend - Verify No Regression After PG Migration

## Objective
Verify that kanban frontend (KanbanPane, useKanban hook, adapters) still works correctly after backend migrates to Railway PostgreSQL, with no API contract breakage.

## Context

**Current State:**
- Kanban frontend uses `useKanban()` hook to fetch data from `/api/kanban/items`, `/api/kanban/columns`, `/api/kanban/move`
- API contract defined by schemas in `hivenode/schemas.py`
- Frontend components: `KanbanPane.tsx`, `useKanban.ts`, `KanbanColumn.tsx`, etc.
- Existing tests: `browser/src/primitives/kanban-pane/__tests__/KanbanPane.test.tsx`

**Changes from TASK-126A and TASK-126B:**
- Kanban routes now read from Railway PG (or CSV fallback)
- Hivenode config defaults to Railway PG for inventory
- API contract should be UNCHANGED (same schemas, same endpoints)

**This Task:**
- Verify frontend tests still pass
- Verify API contract is unchanged (or backward-compatible)
- Verify kanban board loads with real data from Railway PG
- No code changes expected unless API contract broke

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\KanbanPane.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\useKanban.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\__tests__\KanbanPane.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\kanbanAdapter.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\schemas.py` (search for Kanban schemas)

## Deliverables
- [ ] Run `cd browser && npx vitest run` to verify all kanban tests pass
- [ ] If tests fail: identify root cause (API contract change? Frontend bug? Test needs update?)
- [ ] If API contract changed: update frontend to match OR update backend to restore compatibility
- [ ] If tests pass: document verification in response file
- [ ] Smoke test: start hivenode + browser, load `localhost:5173/?egg=kanban`, verify:
  - [ ] Items load from Railway PG
  - [ ] Columns display correctly
  - [ ] Filters work (type, priority, search)
  - [ ] Drag-drop move works
  - [ ] Mobile view works
- [ ] Document any visual regressions or UI bugs
- [ ] If CSV fallback is active (PG unreachable), verify UI shows read-only indicator or error

## Test Requirements
- [ ] All tests in `browser/src/primitives/kanban-pane/__tests__/KanbanPane.test.tsx` pass
- [ ] No new tests required (unless API contract changed)
- [ ] Smoke test documented in response file with screenshots or console output
- [ ] Edge cases:
  - Empty kanban board (no items) → should show empty state
  - Large dataset (100+ items) → should render without performance issues
  - PG connection error → frontend shows error or falls back gracefully
  - CSV fallback active → move button disabled or shows "read-only" message

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- Do NOT modify frontend code unless API contract broke
- Do NOT modify test mocks unless API contract changed
- If API contract changed: prefer fixing backend to restore compatibility over updating frontend

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260315-TASK-126C-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary (npm run build)
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
