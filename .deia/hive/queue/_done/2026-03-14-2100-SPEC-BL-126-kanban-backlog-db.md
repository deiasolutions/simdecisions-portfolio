# SPEC: BL-126 — Connect kanban to new backlog process DB

## Priority
P0.010

## Objective
The kanban pane currently reads from `feature-inventory.db` via `hivenode/inventory/store.py` (backlog_table + bugs_table). Connect it to the new backlog/process database so the kanban board reflects the authoritative data source. Update `kanban_routes.py` and `useKanban.ts` if any API contract changes are needed.

## Context
- Kanban primitive: `browser/src/primitives/kanban-pane/`
- Kanban routes: `hivenode/routes/kanban_routes.py`
- Current data source: `hivenode/inventory/store.py` → `docs/feature-inventory.db`
- Backlog CSV: `docs/feature-inventory-backlog.csv`
- Kanban adapter: `browser/src/apps/kanbanAdapter.tsx`
- EGG: `eggs/kanban.egg.md`
- Source: Q88N-direct

## Acceptance Criteria
- [ ] Kanban routes read from the correct/authoritative backlog data source
- [ ] Items display with correct column, priority, type, and metadata
- [ ] Move operation persists to the correct DB
- [ ] Local fallback: if PostgreSQL is unreachable, kanban reads from local CSV (`docs/feature-inventory-backlog.csv`)
- [ ] No regression in existing kanban tests (`browser/src/primitives/kanban-pane/__tests__/KanbanPane.test.tsx`)
- [ ] No regression in kanban route tests (`tests/hivenode/test_kanban_routes.py`)
- [ ] API contract (request/response shapes) unchanged or backward-compatible

## Smoke Test
- [ ] `GET /api/kanban/items` returns items from new DB
- [ ] `POST /api/kanban/move` persists to new DB
- [ ] `GET /api/kanban/columns` still works
- [ ] Load `localhost:5173/?egg=kanban` and see populated board

## Model Assignment
sonnet

## Constraints
- Do not break existing tests
- Keep all files under 500 lines
- CSS: `var(--sd-*)` only
- Port, not rewrite — preserve existing kanban_routes.py structure
