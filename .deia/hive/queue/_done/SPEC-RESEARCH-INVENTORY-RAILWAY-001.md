# SPEC-RESEARCH-INVENTORY-RAILWAY-001: Troubleshoot & Resurrect Inventory → Railway PostgreSQL

**MODE: EXECUTE**

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

The inventory system (`_tools/inventory.py` + `hivenode/inventory/store.py`) is supposed to use Railway PostgreSQL for persistent storage. Something is broken or misconfigured — it may be falling back to local SQLite, failing silently, or not connecting at all. Survey the full inventory pipeline, diagnose what's wrong, fix it, and confirm data flows to Railway PG.

## Read First

- `_tools/inventory.py` — CLI entry point. How does it get its DB URL?
- `hivenode/inventory/store.py` — store module, engine init, table definitions, migrations
- `hivenode/config.py` — `HIVENODE_INVENTORY_DATABASE_URL`, `DATABASE_URL`, fallback logic
- `hivenode/main.py` — how inventory store is initialized at startup (around line 252-279)
- `hivenode/routes/inventory_routes.py` — API routes that read/write inventory
- `.env` or any env files — check for `INVENTORY_DATABASE_URL`, `HIVENODE_INVENTORY_DATABASE_URL`, `DATABASE_URL`
- `railway.toml` — what env vars are configured for the hivenode service
- `Dockerfile` (hivenode) — does it pass env vars correctly?
- `hivenode/inventory/tests/test_inventory_schema_columns.py` — existing schema tests
- `hivenode/inventory/tests/test_inventory_schema_init.py` — existing init tests

## Questions to Answer

### Section 1: Configuration Diagnosis

**Q1.1** What environment variable(s) does the inventory store look for to get its database URL? Trace the full chain from `config.py` → `main.py` → `store.py`. What is the fallback if no env var is set?

**Q1.2** Is `HIVENODE_INVENTORY_DATABASE_URL` or `INVENTORY_DATABASE_URL` set in any `.env` file in the repo? Is it set in Railway env vars? Check `railway.toml` and any Railway config files.

**Q1.3** When running locally (`python _tools/inventory.py stats`), what database does it actually connect to? Is it hitting Railway PG or falling back to local SQLite? Add a diagnostic that prints the resolved URL (masked) on startup.

**Q1.4** When hivenode runs on Railway, what database URL does the inventory store receive? Is it the same PostgreSQL instance as the main app, or separate?

### Section 2: Connection Testing

**Q2.1** Can you connect to the Railway PostgreSQL from the local machine right now? Try a basic connection test using the DATABASE_URL from Railway. Report success or failure with error message.

**Q2.2** Do the 6 inventory tables exist in Railway PG? (`inv_features`, `inv_backlog`, `inv_bugs`, `inv_tests`, `inv_stage_log`, `inv_early_access`). Query `information_schema.tables` or use SQLAlchemy inspect.

**Q2.3** If tables exist, how many rows are in each? Is there any data, or are they empty?

**Q2.4** Does `_migrate_schema()` run successfully against Railway PG? Any column mismatches?

### Section 3: CLI Pipeline

**Q3.1** Walk through `python _tools/inventory.py stats` end to end. What happens? Does it: (a) find the DB URL, (b) connect, (c) query, (d) return results? At which step does it fail or fall back?

**Q3.2** Walk through `python _tools/inventory.py bug add "test bug" --priority P3`. Same question — trace the full write path.

**Q3.3** Is there a way to run `inventory.py` with an explicit `--db-url` flag? If not, how does a user point it at Railway PG vs local SQLite?

### Section 4: Fix and Verify

**Q4.1** Based on your diagnosis: what is broken? State the root cause clearly.

**Q4.2** Fix the issue. If it's a config problem, fix the config. If it's a code problem, fix the code. If env vars are missing, document exactly what needs to be set and where.

**Q4.3** After fixing: run `inventory.py stats` and confirm it connects to Railway PG and returns real data. Show the output.

**Q4.4** Run `inventory.py bug add "test-connectivity-probe" --priority P4` and confirm the row appears in Railway PG. Then delete it.

## Acceptance Criteria

- [ ] Full configuration chain traced and documented (env var → config → store → connection)
- [ ] Root cause of inventory/Railway disconnect identified
- [ ] All 6 inventory tables verified present (or created) in Railway PG
- [ ] `inventory.py stats` successfully queries Railway PG and returns results
- [ ] Write path verified: can add and remove a test record via CLI
- [ ] Any code or config fixes applied and documented
- [ ] If env vars need to be set on Railway, exact variable names and values documented
- [ ] Response written to `.deia/hive/responses/20260409-INVENTORY-RAILWAY-RESPONSE.md`

## Smoke Test

```bash
cd /c/Users/davee/OneDrive/Documents/GitHub/shiftcenter
python _tools/inventory.py stats
# Should connect to Railway PG and show feature/bug/backlog counts
```

## Constraints

- Do NOT delete or modify existing inventory data in Railway PG
- Do NOT change table schemas — they were verified correct in TASK-HIVE2A
- The test record added in Q4.4 must be cleaned up (deleted) after verification
- If Railway credentials are needed that aren't available, STOP and report what's needed
- Mask/redact any database URLs or credentials in the response file
- Max response length: 400 lines

## Response File

`.deia/hive/responses/20260409-INVENTORY-RAILWAY-RESPONSE.md`
