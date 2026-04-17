# TASK-073: Canonical Status Validation + Migration Function

## Objective

Implement canonical status set validation and database migration function to unify all inventory statuses to: `backlog`, `queued`, `in_progress`, `review`, `done`, `blocked`, `deferred`, `cancelled`.

## Context

The feature inventory currently uses inconsistent status vocabularies:
- Features: `BUILT`, `SPECCED`, `BROKEN`, `REMOVED`
- Bugs: `OPEN`, `ASSIGNED`, `FIXED`, `WONTFIX`
- Backlog: No status column (uses `kanban_column` and `stage_status`)

This task creates a migration function to normalize existing DB values and updates the VALID_STATUSES constant.

Current DB state (verified 2026-03-14):
- Features: 64 entries
- Backlog: 108 entries
- Both counts > 50 (safe to migrate)

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory_db.py` — Database operations
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory.py` — CLI tool

## Deliverables

- [ ] Update `VALID_STATUSES` constant in `inventory_db.py` to: `{"backlog", "queued", "in_progress", "review", "done", "blocked", "deferred", "cancelled"}`
- [ ] Create `db_migrate_statuses()` function in `inventory_db.py` that:
  - Verifies feature count >= 50 (safety check per spec)
  - Creates backup: `docs/feature-inventory.db.bak`
  - Applies status mapping to `features.status` column:
    - `BUILT` → `done`
    - `SPECCED` → `queued`
    - `BROKEN` → `blocked`
    - `REMOVED` → `cancelled`
  - Applies status mapping to `bugs.status` column:
    - `OPEN` → `backlog`
    - `ASSIGNED` → `in_progress`
    - `FIXED` → `done`
    - `WONTFIX` → `cancelled`
  - Also handles legacy values (if found):
    - `complete` / `shipped` → `done`
    - `open` → `backlog`
    - `pending` → `queued`
    - `wip` → `in_progress`
  - Is idempotent (safe to run multiple times)
  - Returns `(success: bool, message: str)`
- [ ] Add `migrate-statuses` command to CLI in `inventory.py`
- [ ] Update `VALID_BUG_STATUSES` constant to use canonical set
- [ ] Ensure file sizes stay under 500 lines each (currently inventory.py=505, inventory_db.py=518)

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] Test: Migration creates backup file
- [ ] Test: Migration refuses to run if feature count < 50
- [ ] Test: Each status mapping (BUILT→done, SPECCED→queued, etc.)
- [ ] Test: Idempotency (running migration twice produces same result)
- [ ] Test: Migration succeeds with valid DB, returns (True, message)
- [ ] Test: Invalid status in DB after migration would fail validation
- [ ] Test: CLI command `migrate-statuses` calls `db_migrate_statuses()`
- [ ] Minimum 8 tests total

**Test file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\tests\test_migrate_statuses.py`

Edge cases to test:
- DB with < 50 features (should abort)
- DB with already-migrated statuses (idempotent)
- Backup file already exists (should overwrite or error clearly)
- Mixed old and new statuses in same DB

## Constraints

- No file over 500 lines
- CSS: not applicable (backend only)
- No stubs — migration function must be fully implemented
- TDD: tests first, then implementation
- Migration must create backup BEFORE modifying DB
- Migration must be idempotent

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-073-RESPONSE.md`

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

---

**Model Assignment:** haiku
**Estimated Size:** M (migration function ~50 lines, tests ~100 lines)
