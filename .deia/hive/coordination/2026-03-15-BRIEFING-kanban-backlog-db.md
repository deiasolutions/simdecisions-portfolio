# BRIEFING: Connect Kanban to New Backlog Process DB

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-15
**Spec:** BL-126
**Priority:** P1
**Model Assignment:** sonnet

---

## Objective

The kanban pane currently reads from `docs/feature-inventory.db` (local SQLite) via `hivenode/inventory/store.py`. It must now read from the **Railway PostgreSQL** database (the authoritative backlog data source) to ensure the kanban board reflects real-time, multi-session data.

---

## Context from Q88N

Per HIVE.md lines 280-305:

- **Inventory data (features, backlog, bugs, stage log) lives on Railway PostgreSQL**, not local SQLite
- The CLI connects directly to PG via `_tools/inventory_db.py` which imports `hivenode/inventory/store.py`
- Connection string is hardcoded in `inventory_db.py`
- Local SQLite fallback: `INVENTORY_DATABASE_URL=local` env var
- Concurrent Claude sessions used to corrupt the local SQLite DB; PG handles concurrency correctly
- Data is now safe on Railway, not lost on OneDrive sync

---

## Current State

**Kanban routes:** `hivenode/routes/kanban_routes.py`
**Kanban frontend:** `browser/src/primitives/kanban-pane/`
**Kanban adapter:** `browser/src/apps/kanbanAdapter.tsx`
**Data source (old):** `hivenode/inventory/store.py` → `docs/feature-inventory.db`
**Data source (new):** `hivenode/inventory/store.py` → Railway PostgreSQL
**Backlog CSV (fallback):** `docs/feature-inventory-backlog.csv`
**EGG:** `eggs/kanban.egg.md`

**Kanban endpoints (current):**
- `GET /api/kanban/items` — returns items from backlog_table + bugs_table
- `POST /api/kanban/move` — persists column/priority changes to DB
- `GET /api/kanban/columns` — returns column metadata

**Acceptance Criteria from Spec:**
- [ ] Kanban routes read from Railway PostgreSQL (via store.py)
- [ ] Items display with correct column, priority, type, metadata
- [ ] Move operation persists to correct DB (PostgreSQL)
- [ ] Local fallback: if PostgreSQL unreachable, read from CSV (`docs/feature-inventory-backlog.csv`)
- [ ] No regression in `browser/src/primitives/kanban-pane/__tests__/KanbanPane.test.tsx`
- [ ] No regression in `tests/hivenode/test_kanban_routes.py`
- [ ] API contract unchanged or backward-compatible

**Smoke Test:**
- [ ] `GET /api/kanban/items` returns items from Railway PG
- [ ] `POST /api/kanban/move` persists to Railway PG
- [ ] `GET /api/kanban/columns` still works
- [ ] Load `localhost:5173/?egg=kanban` and see populated board

---

## Key Files to Read

**Backend:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\kanban_routes.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\inventory\store.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory_db.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_kanban_routes.py`

**Frontend:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\KanbanPane.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\__tests__\KanbanPane.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\kanbanAdapter.tsx`

**EGG:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\kanban.egg.md`

**Fallback CSV:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\feature-inventory-backlog.csv`

---

## Constraints

1. **Do NOT break existing tests.** All kanban tests must pass before and after.
2. **Port, not rewrite.** Preserve existing `kanban_routes.py` structure.
3. **Keep files under 500 lines.** Modularize if necessary.
4. **CSS: `var(--sd-*)` only.** No hardcoded colors.
5. **No stubs.** Fully implement all functions.
6. **TDD.** Tests first, then implementation.

---

## What Q33N Must Deliver

**Task files** to `.deia/hive/tasks/` covering:

1. **Update kanban routes** to read from Railway PG (via store.py) with CSV fallback
2. **Verify kanban frontend** still works (no API contract changes, or backward-compatible changes)
3. **Update tests** to reflect new data source (if needed)
4. **Smoke test** the kanban board with real data

**Each task file must include:**
- Objective (one sentence)
- Context (file paths, schema details)
- Files to Read First (absolute paths)
- Deliverables (concrete outputs)
- Test Requirements (TDD, edge cases)
- Constraints (500 lines, var(--sd-*), no stubs)
- Response Requirements (8-section template)

**Return task files to Q33NR for review. DO NOT dispatch bees until Q33NR approves.**

---

## Expected Outcome

After bees complete:
- Kanban reads from Railway PG
- Kanban falls back to CSV if PG unreachable
- All tests pass
- Kanban board loads with real data at `localhost:5173/?egg=kanban`
- No API contract breakage

---

## Q33N: Read this briefing, read the key files, write task files, return to Q33NR for review.
