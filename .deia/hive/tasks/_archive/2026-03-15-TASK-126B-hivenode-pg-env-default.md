# TASK-126B: Hivenode Config - Default to Railway PostgreSQL for Inventory

## Objective
Update hivenode config to default `inventory_database_url` to Railway PostgreSQL (unless explicitly overridden), ensuring kanban reads from authoritative backlog data.

## Context

**Current State:**
- `hivenode/config.py` has `inventory_database_url: Optional[str] = None`
- `main.py` uses `settings.inventory_database_url or settings.database_url` to init inventory store
- If both are None, inventory store is not initialized (or uses SQLite in local mode)
- CLI tool (`_tools/inventory_db.py`) hardcodes Railway PG URL
- Per HIVE.md: inventory data lives on Railway PG, local SQLite is fallback only

**Problem:**
- Hivenode server doesn't default to Railway PG for inventory
- Developers must manually set `HIVENODE_INVENTORY_DATABASE_URL` or inventory uses local SQLite

**Solution:**
- Add Railway PG URL as default in `config.py` for `inventory_database_url`
- Allow override via `HIVENODE_INVENTORY_DATABASE_URL=local` for offline work
- Special value `"local"` → use local SQLite (`docs/feature-inventory.db`)

**Railway PG URL (from inventory_db.py):**
```
postgresql://[REDACTED]@[REDACTED]/railway
```

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory_db.py`

## Deliverables
- [ ] Add class-level constant `_RAILWAY_PG_URL` in `HivenodeConfig`
- [ ] Update `_set_defaults()` to set `inventory_database_url` to Railway PG URL if not set
- [ ] Handle special value `"local"` → convert to SQLite path `docs/feature-inventory.db`
- [ ] Update docstring for `inventory_database_url` to document default and "local" special value
- [ ] No changes to `main.py` (it already uses `settings.inventory_database_url or settings.database_url`)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] New test file: `tests/hivenode/test_config_inventory_url.py`
- [ ] Test: `test_inventory_url_defaults_to_railway_pg()` - no env var set → Railway PG URL
- [ ] Test: `test_inventory_url_respects_env_override()` - `HIVENODE_INVENTORY_DATABASE_URL=postgresql://custom` → custom URL
- [ ] Test: `test_inventory_url_local_keyword()` - `HIVENODE_INVENTORY_DATABASE_URL=local` → SQLite path
- [ ] Test: `test_inventory_url_empty_string_uses_default()` - `HIVENODE_INVENTORY_DATABASE_URL=""` → Railway PG URL
- [ ] All existing hivenode config tests still pass
- [ ] Edge cases:
  - `inventory_database_url` set to None explicitly → use Railway PG default
  - `inventory_database_url` set to empty string → use Railway PG default
  - `inventory_database_url` set to "local" → use SQLite
  - `inventory_database_url` set to custom URL → use custom URL

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (N/A - backend only)
- No stubs
- Do NOT hardcode Railway PG URL in multiple places (use constant)
- Do NOT break existing tests for `database_url` (separate from `inventory_database_url`)
- SQLite path for "local" should be absolute path to `docs/feature-inventory.db` relative to project root

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260315-TASK-126B-RESPONSE.md`

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
