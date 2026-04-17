# TASK-126A: Initialize Inventory Engine in Hivenode Lifespan

## Objective
Initialize the inventory store engine during hivenode startup to connect kanban routes to Railway PostgreSQL.

## Context

**Current State:**
- `hivenode/inventory/store.py` provides `init_engine(url)` and `get_engine()` functions
- `kanban_routes.py` calls `get_engine()` but gets `RuntimeError` if not initialized
- `hivenode/config.py` has `inventory_database_url` setting (defaults to Railway PG URL)
- `_tools/inventory_db.py` auto-initializes on import for CLI usage
- Hivenode app does NOT initialize the engine, so kanban routes fall back to CSV

**What Changed (HIVE.md lines 280-305):**
- Inventory data (features, backlog, bugs) moved from local SQLite to Railway PostgreSQL
- CLI connects directly to PG via `inventory_db.py` (no hivenode dependency)
- Hivenode kanban API needs to connect to same PG database
- Connection string is in `config.settings.inventory_database_url`

**Files to Read First:**
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\inventory\store.py
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\kanban_routes.py
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory_db.py

## Deliverables

**Backend:**
- [ ] Update `hivenode/main.py` lifespan to call `init_engine(config.settings.inventory_database_url)`
- [ ] Engine initialization happens ONCE at startup (before routes are registered)
- [ ] Engine initialization is OPTIONAL (if it fails, kanban routes fall back to CSV)
- [ ] Log success/failure of inventory engine initialization
- [ ] Handle `INVENTORY_DATABASE_URL=local` env var (already handled by config.py)

**Tests:**
- [ ] All existing kanban tests pass (they use in-memory SQLite, auto-initialize)
- [ ] No new tests required (existing tests already cover kanban API + CSV fallback)
- [ ] Manual smoke test: start hivenode, verify kanban routes read from Railway PG

**Documentation:**
- [ ] Add comment to `main.py` lifespan explaining inventory engine initialization
- [ ] Update this task response with smoke test results

## Test Requirements

**TDD:** No new tests required. This is infrastructure wiring.

**Existing Tests Must Pass:**
- `pytest tests/hivenode/test_kanban_routes.py -v` → all 34 tests pass
- `pytest tests/hivenode/test_config.py -v` → all config tests pass

**Edge Cases Already Covered:**
- Engine not initialized → CSV fallback (tested in `test_kanban_csv_fallback_*`)
- Engine initialization failure → CSV fallback (same as not initialized)
- Tests initialize their own in-memory engine (via autouse fixture)

**Smoke Test (Manual):**
1. Start hivenode: `cd hivenode && python -m hivenode.main`
2. Check logs for: "Inventory store initialized: postgresql://..."
3. `curl http://localhost:8420/api/kanban/items` → returns items from Railway PG
4. Verify returned items match CLI output: `python _tools/inventory.py backlog list`

## Constraints

- No file over 500 lines
- CSS: `var(--sd-*)` only (not applicable, backend only)
- No stubs (all functions fully implemented)
- TDD (not applicable, infrastructure wiring)
- Absolute paths in docs
- Do NOT break existing tests
- Do NOT change `store.py` or `kanban_routes.py` (they already work correctly)
- Do NOT change test fixtures (they already initialize in-memory engine)

## Implementation Notes

**Where to initialize:**
```python
# hivenode/main.py
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ... existing ledger/node setup ...

    # Initialize inventory store (PostgreSQL or local SQLite)
    from hivenode.inventory.store import init_engine
    from hivenode.config import settings
    try:
        init_engine(settings.inventory_database_url)
        logger.info(f"Inventory store initialized: {settings.inventory_database_url[:50]}...")
    except Exception as e:
        logger.warning(f"Inventory store initialization failed (CSV fallback enabled): {e}")

    yield

    # ... existing cleanup ...
```

**Why this works:**
- `init_engine()` is idempotent (returns early if already initialized)
- Tests initialize their own in-memory engine BEFORE the app lifespan runs
- If PG is unreachable, `init_engine()` raises an exception → we catch it and log → kanban routes fall back to CSV
- `settings.inventory_database_url` defaults to Railway PG URL (from config.py)
- If `INVENTORY_DATABASE_URL=local` env var is set, config.py converts it to SQLite URL

**What NOT to do:**
- Do NOT use `force=True` when calling `init_engine()` (would break tests)
- Do NOT call `init_engine()` inside route handlers (too late, performance hit)
- Do NOT raise exceptions if init fails (CSV fallback should still work)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-126A-RESPONSE.md

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
