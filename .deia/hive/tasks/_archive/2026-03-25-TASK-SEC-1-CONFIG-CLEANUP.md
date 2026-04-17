# TASK-SEC-1: Clean Hardcoded Credentials from config.py

## Objective
Remove all hardcoded Railway PostgreSQL URLs from `hivenode/config.py` and replace with environment-variable-only configuration.

## Context
Phase 0 (credential rotation) is complete. This task removes the old hardcoded credentials from the codebase. The inventory database URL currently has fallback logic that includes a hardcoded Railway URL — this must be replaced with a cleaner fallback that only uses environment variables or local SQLite.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_config.py`

## Deliverables
- [ ] Remove any hardcoded `RAILWAY_DATABASE_URL` constant if it exists
- [ ] Remove any hardcoded `RAILWAY_DATABASE_PUBLIC_URL` constant if it exists
- [ ] Replace `inventory_database_url` fallback logic in `_set_defaults()` method with clean env-var logic:
  ```python
  _inv_url = os.environ.get("HIVENODE_INVENTORY_DATABASE_URL", "")
  if _inv_url == "local" or not _inv_url:
      inventory_path = Path.home() / ".shiftcenter" / "inventory.db"
      inventory_path.parent.mkdir(parents=True, exist_ok=True)
      self.inventory_database_url = f"sqlite:///{inventory_path}"
  else:
      self.inventory_database_url = _inv_url
  ```
- [ ] Verify NO `postgresql://` strings remain anywhere in the file (grep verification)
- [ ] Verify `database_url` reads from `os.environ.get("DATABASE_URL")` with NO hardcoded production fallback
- [ ] Update test assertions in `test_config.py` if they expect old hardcoded URLs

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing config tests pass
- [ ] New test: config with `HIVENODE_INVENTORY_DATABASE_URL="local"` creates SQLite in ~/.shiftcenter/
- [ ] New test: config with `HIVENODE_INVENTORY_DATABASE_URL=<postgres-url>` uses that URL
- [ ] New test: config with no inventory URL and no DATABASE_URL raises ValueError
- [ ] Edge cases:
  - Empty string for inventory URL falls back to local
  - Valid postgres URL is preserved as-is
  - No postgresql:// strings remain in config.py

## Constraints
- No file over 500 lines
- No stubs
- TDD — tests first
- Do NOT modify `.env` or `.gitignore` (separate task)

## Model
Sonnet (infrastructure code requiring careful reading)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260325-TASK-SEC-1-RESPONSE.md`

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
