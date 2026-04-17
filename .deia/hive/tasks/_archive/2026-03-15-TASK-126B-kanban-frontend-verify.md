# TASK-126B: Verify Kanban Frontend with PostgreSQL Backend

## Objective
Verify kanban frontend still works correctly with Railway PostgreSQL backend (no API contract breakage).

## Context

**Current State:**
- Kanban routes now connect to Railway PostgreSQL (via TASK-126A)
- Kanban frontend (`browser/src/primitives/kanban-pane/`) fetches from `/api/kanban/items`
- API contract must remain unchanged or backward-compatible
- Frontend tests use mock API (do not hit real backend)
- Frontend loads at `localhost:5173/?egg=kanban`

**What Changed:**
- Backend now reads from PostgreSQL instead of local SQLite
- CSV fallback still exists for when PG is unreachable
- API response structure unchanged (same `KanbanItem` schema)

**Files to Read First:**
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\KanbanPane.tsx
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\useKanban.ts
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\__tests__\KanbanPane.test.tsx
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\kanbanAdapter.tsx
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\kanban.egg.md

## Deliverables

**Frontend Tests:**
- [ ] All existing kanban frontend tests pass
- [ ] No new tests required (API contract unchanged)

**Smoke Test (Manual):**
- [ ] Load `http://localhost:5173/?egg=kanban` in browser
- [ ] Verify items load from backend API
- [ ] Verify filters work (type, priority, graduated)
- [ ] Verify drag-drop move persists to backend
- [ ] Verify columns accordion expand/collapse
- [ ] Verify mobile responsive layout (resize to <700px)

**Documentation:**
- [ ] Update task response with smoke test results
- [ ] Screenshot kanban board showing loaded items from Railway PG

## Test Requirements

**TDD:** Not applicable. This is verification of existing functionality.

**Existing Tests Must Pass:**
- `cd browser && npx vitest run src/primitives/kanban-pane` → all tests pass
- No new tests required

**Smoke Test (Manual):**
1. Start backend: `cd hivenode && python -m hivenode.main`
2. Start frontend: `cd browser && npm run dev`
3. Load: `http://localhost:5173/?egg=kanban`
4. Verify:
   - Items load from API (check network tab: `/api/kanban/items`)
   - Item count matches CLI: `python _tools/inventory.py backlog list | wc -l`
   - Filters work (type=work/bug, priority=P0/P1/P2/P3)
   - Drag item to new column → POST to `/api/kanban/move` → item moves
   - Refresh page → item still in new column (persisted to PG)
5. Test CSV fallback:
   - Stop Railway PG (or set `INVENTORY_DATABASE_URL=local`)
   - Restart backend
   - Load kanban → should show items from CSV (`docs/feature-inventory-backlog.csv`)

## Constraints

- No file over 500 lines
- CSS: `var(--sd-*)` only
- No stubs
- Do NOT modify frontend code unless you find a bug
- Do NOT modify API contract
- Do NOT break existing tests

## Implementation Notes

**This is a VERIFICATION task, not an IMPLEMENTATION task.**

You should:
1. Read the kanban frontend files
2. Run the frontend tests
3. Perform manual smoke test
4. Report results

You should NOT:
1. Write new code (unless you find a bug)
2. Change API endpoints
3. Modify test files (unless they are broken)

**If you find bugs:**
- Document them in the response file "Issues / Follow-ups" section
- Do NOT fix them in this task (report to Q33N for triage)

**If all tests pass and smoke test works:**
- Mark task COMPLETE
- Document smoke test results with screenshots if possible

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-126B-RESPONSE.md

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths (should be NONE unless bugs found)
3. **What Was Done** — bullet list of verification steps performed
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — frontend build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — bugs found, next tasks, recommendations

DO NOT skip any section.
