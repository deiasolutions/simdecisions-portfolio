# BRIEFING: Status System Alignment

**Date:** 2026-03-14
**From:** Q88NR
**To:** Q33N (Coordinator)
**Re:** SPEC BL-110 — Status System Alignment

---

## Objective

Unify all inventory status values across the platform to a single canonical set:

```
backlog, queued, in_progress, review, done, blocked, deferred, cancelled
```

This spec standardizes the feature inventory CLI (`_tools/inventory.py`) and database (`docs/feature-inventory.db`) so all features, bugs, and backlog items use the same status vocabulary.

---

## Context

### Current State (Inconsistent)

**Features table (`features.status`):**
- Current values: `BUILT`, `SPECCED`, `BROKEN`, `REMOVED`
- Usage: 64 features in DB (safe to migrate)

**Bugs table (`bugs.status`):**
- Current values: `OPEN`, `ASSIGNED`, `FIXED`, `WONTFIX`

**Backlog table:**
- No `status` column currently
- Uses `kanban_column`: `icebox`, `backlog`, `in_progress`, `review`, `done`
- Uses `stage_status`: `done`, `active`, `pending`, `failed`, `blocked`

### Problem

The system uses different status vocabularies for the same concept (work state). This causes:
- Confusion when querying across features/bugs/backlog
- Inconsistent CLI validation
- Unclear mapping between old and new statuses

---

## Files to Read First

**Absolute paths (Windows):**

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory.py` — CLI tool
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory_db.py` — Database operations
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\feature-inventory.db` — SQLite DB (read schema only)

---

## Acceptance Criteria

**From SPEC BL-110:**

- [ ] `inventory.py` validates status values against the canonical set: `backlog`, `queued`, `in_progress`, `review`, `done`, `blocked`, `deferred`, `cancelled`
- [ ] Invalid status values are rejected with a clear error message listing valid options
- [ ] `inventory.py add` accepts `--status` flag with validation
- [ ] `inventory.py update` (if it exists) validates status on update
- [ ] `inventory.py stats` groups by canonical statuses
- [ ] `inventory.py export-md` uses canonical statuses in the markdown output
- [ ] A migration function normalizes existing DB entries:
  - `"complete"` → `"done"`
  - `"shipped"` → `"done"`
  - `"open"` → `"backlog"`
  - `"pending"` → `"queued"`
  - `"wip"` → `"in_progress"`
  - Additional mappings for current statuses:
    - `"BUILT"` → `"done"` (features)
    - `"SPECCED"` → `"queued"` (features)
    - `"BROKEN"` → `"blocked"` (features)
    - `"REMOVED"` → `"cancelled"` (features)
    - `"OPEN"` → `"backlog"` (bugs)
    - `"ASSIGNED"` → `"in_progress"` (bugs)
    - `"FIXED"` → `"done"` (bugs)
    - `"WONTFIX"` → `"cancelled"` (bugs)
- [ ] Migration creates a backup before modifying (`docs/feature-inventory.db.bak`)
- [ ] 8+ tests covering validation, migration, and stats grouping
- [ ] **WARNING:** The backlog DB was recently wiped. Before ANY DB modification, verify item count. If count < 50, STOP and report — do NOT proceed with migration.

---

## Model Assignment

**haiku** — This is a data migration + validation task. Haiku is sufficient.

---

## Constraints

1. **Hard Rules (BOOT.md):**
   - No file over 500 lines (inventory.py is currently 505 lines, inventory_db.py is 518 lines — both need modularization if adding significant code)
   - TDD: tests first, then implementation
   - No stubs
   - All file paths must be absolute in task docs

2. **Migration Safety:**
   - Do NOT delete or modify existing DB data without creating a backup first
   - If the DB has fewer than 50 backlog items, STOP and report without modifying
   - Migration is idempotent — running it twice produces the same result
   - Verify backlog count BEFORE running migration

3. **Scope:**
   - Only modify `_tools/inventory.py` and `_tools/inventory_db.py`
   - Do NOT modify the database schema (tables/columns)
   - Migration only updates values in existing `status` columns

---

## Implementation Notes

### Recommended Approach

1. **Add migration command to CLI:**
   - `python _tools/inventory.py migrate-statuses`
   - Creates backup: `docs/feature-inventory.db.bak`
   - Verifies feature count >= 50 (safety check from spec)
   - Updates all `features.status`, `bugs.status` values using mapping table
   - Idempotent: safe to run multiple times

2. **Update VALID_STATUSES constant:**
   - Change from `{"BUILT", "SPECCED", "BROKEN", "REMOVED"}` to `{"backlog", "queued", "in_progress", "review", "done", "blocked", "deferred", "cancelled"}`
   - Update all validation in `cmd_add()`, `cmd_update()`

3. **Update stats/export functions:**
   - `db_stats()` — group by new statuses
   - `db_export_features()` — show new statuses in markdown

4. **File size management:**
   - If adding migration pushes `inventory_db.py` over 550 lines, extract migration logic to `_tools/inventory_migrate.py`

---

## Task Files to Write

Q33N should break this into **2-3 task files** maximum:

**TASK-073:** Canonical status validation + migration function
**TASK-074:** Update CLI commands to use new statuses
**TASK-075:** Tests (8+ covering validation, migration, stats, export)

---

## Success Criteria

When Q33N returns task files to Q88NR for review, they must include:

1. Absolute file paths for all deliverables
2. Test requirements specifying exact scenarios to test
3. Migration logic that is idempotent and creates backups
4. Clear validation error messages listing valid statuses
5. No file over 500 lines after changes
6. All 8 sections in response file template

---

## Q33N: Your Next Steps

1. Read the three files listed above
2. Understand current DB schema and status values
3. Write task files for the bee (haiku model)
4. Return task files to Q88NR for review
5. Do NOT dispatch bees until Q88NR approves task files

---

**END OF BRIEFING**
