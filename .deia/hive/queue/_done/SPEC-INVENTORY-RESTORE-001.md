# SPEC-INVENTORY-RESTORE-001: Full Inventory Process Restoration & Data Migration

**MODE: EXECUTE**

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Objective

The inventory process broke during the repo move to shiftcenter. The DB connection to Railway PG has been restored (`.env` now has the correct `DATABASE_URL`), but the process is NOT fully fixed yet. This spec covers everything else:

1. **Data migration** — local SQLite accumulated data while Railway was disconnected. Migrate it to Railway PG.
2. **Process verification** — verify every inventory CLI command works end-to-end against Railway PG.
3. **Identify any other breakage** — the repo move may have broken more than just the DB URL. Find and fix anything else.

## Context

- The `.env` file now has: `DATABASE_URL=postgresql://[REDACTED]@[REDACTED]/railway`
- Railway hivenode has: `DATABASE_URL=${{Postgres.DATABASE_URL}}` and `HIVENODE_INVENTORY_DATABASE_URL=${{Postgres.DATABASE_URL}}`
- Local SQLite is at: `docs/feature-inventory.db` (accessed via `INVENTORY_DATABASE_URL=local`)
- Previous research response: `.deia/hive/responses/20260409-INVENTORY-RAILWAY-RESPONSE.md`

## Read First

- `_tools/inventory.py` — full CLI, all commands
- `_tools/inventory_db.py` — DB connection layer
- `hivenode/inventory/store.py` — store module, all CRUD functions
- `hivenode/routes/inventory_routes.py` — API routes
- `.deia/hive/responses/20260409-INVENTORY-RAILWAY-RESPONSE.md` — previous diagnosis

## Task 1: Audit Local SQLite Data

Export everything from local SQLite. For each table, report row counts and contents:

```bash
cd /c/Users/davee/OneDrive/Documents/GitHub/shiftcenter
export INVENTORY_DATABASE_URL=local

python _tools/inventory.py list
python _tools/inventory.py backlog list
python _tools/inventory.py bug list
python _tools/inventory.py test list
python _tools/inventory.py export-md
python _tools/inventory.py backlog export-md
python _tools/inventory.py bug export-md
python _tools/inventory.py test export-md
```

Report exactly what data exists locally that needs to be migrated.

## Task 2: Audit Railway PG Data

Check what's already in Railway PG:

```bash
export DATABASE_URL="postgresql://[REDACTED]@[REDACTED]/railway"

python _tools/inventory.py list
python _tools/inventory.py backlog list
python _tools/inventory.py bug list
python _tools/inventory.py test list
```

Report what exists (may be empty if this is a fresh DB, or may have old data from before the repo move).

## Task 3: Migrate Local Data to Railway PG

For any data that exists locally but not on Railway:

1. Export from local SQLite using `export-md` commands
2. Import to Railway PG using `import-md` commands
3. If `import-md` doesn't exist or doesn't cover all tables, use direct store calls or SQL inserts
4. Verify row counts match after migration
5. Do NOT delete local SQLite data — keep it as backup

## Task 4: Verify Full Inventory Process

Test every major CLI command against Railway PG (using the default `DATABASE_URL` from `.env`):

```bash
# Source the .env so DATABASE_URL is set
cd /c/Users/davee/OneDrive/Documents/GitHub/shiftcenter

# Feature lifecycle
python _tools/inventory.py add --id TEST-RESTORE --name "Restore test" --layer shell --status wip
python _tools/inventory.py list
python _tools/inventory.py verify --id TEST-RESTORE
python _tools/inventory.py remove --id TEST-RESTORE

# Backlog lifecycle
python _tools/inventory.py backlog add --title "Restore test backlog" --category enhancement --priority P3
python _tools/inventory.py backlog list
# Note the ID assigned, then remove it

# Bug lifecycle
python _tools/inventory.py bug add --id BUG-RESTORE --title "Restore test bug" --severity P3 --component inventory
python _tools/inventory.py bug list
python _tools/inventory.py bug remove --id BUG-RESTORE --notes "test cleanup"

# Stats
python _tools/inventory.py stats

# Search
python _tools/inventory.py search "test"
```

Report PASS/FAIL for each command with output.

## Task 5: Check for Other Breakage

Beyond the DB connection, check:

1. Are all imports in `inventory.py` and `inventory_db.py` resolving correctly?
2. Does `hivenode/routes/inventory_routes.py` work? (API layer, not just CLI)
3. Are there any hardcoded paths from the old repo that need updating?
4. Does `python _tools/inventory.py stats` produce the same output format as before?
5. Is `FEATURE-INVENTORY.md` being generated correctly by `export-md`?

## Acceptance Criteria

- [ ] Local SQLite data fully audited and documented
- [ ] Railway PG data fully audited and documented
- [ ] All local data migrated to Railway PG (or confirmed already present)
- [ ] Row counts verified matching after migration
- [ ] Every CLI command tested against Railway PG: add, list, update, verify, remove, search, stats, export-md for features, backlog, bugs, and tests
- [ ] All test records created during verification cleaned up
- [ ] Any additional breakage found and fixed
- [ ] Response written to `.deia/hive/responses/20260409-INVENTORY-RESTORE-RESPONSE.md`

## Smoke Test

```bash
cd /c/Users/davee/OneDrive/Documents/GitHub/shiftcenter
python _tools/inventory.py stats
python _tools/inventory.py backlog list
# Should show data from Railway PG including migrated items
```

## Constraints

- Do NOT delete local SQLite data — keep as backup
- Clean up ALL test records created during verification
- Do NOT modify table schemas
- If `import-md` is missing or broken for a table, write the migration using direct store function calls
- The `.env` file has the Railway public URL in `DATABASE_URL` — use that for all Railway operations (do NOT set `INVENTORY_DATABASE_URL` unless testing local SQLite specifically)
- Max response length: 400 lines

## Response File

`.deia/hive/responses/20260409-INVENTORY-RESTORE-RESPONSE.md`
