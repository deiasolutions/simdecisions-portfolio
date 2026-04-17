# TASK-044: Status Alignment — Schema Migration + CLI

## Objective
Add kanban workflow columns and dev cycle stage tracking to `feature-inventory.db`, plus CLI commands to manage them. Enables unified status tracking for kanban + progress panes.

## Context
Currently, the `backlog` table has no workflow state tracking — items can't be assigned to kanban columns, can't track which dev cycle stage they're in, and can't graduate to the feature inventory. This task unifies four separate tracking systems (kanban columns, dev cycle stages, feature inventory, DEIA task lifecycle) into one coherent model.

**Key Design Decisions:**
- Backlog items flow through kanban columns: `icebox → backlog → in_progress → review → done`
- Items in `in_progress` track dev cycle stage: `SPEC → IR → VAL → BUILD → TEST`
- Each stage has start/end timestamps (append-only log) for Gantt timeline display
- When item completes all stages, it can graduate to feature inventory with a `feature_id`
- Bugs skip IR pipeline (SPEC → BUILD → TEST)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory.py` (current schema + CLI structure)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\kanban-pane-v03.jsx` (kanban workflow model)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\progress-pane-v01.jsx` (dev cycle stage model)

## Deliverables

### PREREQUISITE: Split inventory.py (currently 705 lines — over 500-line limit)

Before adding any new functionality, split `inventory.py` into two files:

- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory_db.py` — extract ALL database functions:
  - `_connect()`, `_ensure_tables()`, `_migrate_schema()` (new)
  - All `cmd_*` functions that do DB reads/writes (the function bodies, not the argparse wiring)
  - All SQL queries and table creation statements
  - Export functions that `inventory.py` will import
- [ ] Keep `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory.py` as the CLI entry point:
  - argparse setup, subcommand definitions, `main()`
  - Import DB functions from `inventory_db.py`
  - `_print_table()` and other display helpers stay here
- [ ] After split: `inventory.py` should be ~250-350 lines, `inventory_db.py` should be ~350-450 lines
- [ ] All existing tests must pass after the split (no behavioral change)
- [ ] All existing CLI commands work identically

### Schema Changes
- [ ] Add columns to `backlog` table:
  ```sql
  ALTER TABLE backlog ADD COLUMN kanban_column TEXT NOT NULL DEFAULT 'backlog';
  ALTER TABLE backlog ADD COLUMN stage TEXT DEFAULT NULL;
  ALTER TABLE backlog ADD COLUMN stage_status TEXT DEFAULT NULL;
  ALTER TABLE backlog ADD COLUMN assigned_to TEXT DEFAULT NULL;
  ALTER TABLE backlog ADD COLUMN feature_id TEXT DEFAULT NULL;
  ```
- [ ] Create `stage_log` table (append-only, for progress/Gantt pane):
  ```sql
  CREATE TABLE stage_log (
      id          INTEGER PRIMARY KEY AUTOINCREMENT,
      item_id     TEXT NOT NULL,          -- BL-xxx or BUG-xxx
      item_type   TEXT NOT NULL,          -- 'backlog' or 'bug'
      stage       TEXT NOT NULL,          -- SPEC, IR, VAL, BUILD, TEST
      status      TEXT NOT NULL,          -- done, active, pending, failed, blocked
      started_at  TEXT,                   -- ISO timestamp
      ended_at    TEXT,                   -- ISO timestamp (null if active)
      notes       TEXT,
      created_at  TEXT NOT NULL DEFAULT (datetime('now'))
  );
  CREATE INDEX idx_stage_item ON stage_log(item_id);
  ```
- [ ] Migration function `_migrate_schema()` that runs on `_connect()` if columns don't exist
- [ ] Migrate existing 97 backlog items: all default to `kanban_column='backlog'`

### CLI Commands
- [ ] `python _tools/inventory.py backlog move <ID> --column <icebox|backlog|in_progress|review|done>`
  - Updates `kanban_column` for a backlog item
  - Validates column is one of the 5 allowed values
- [ ] `python _tools/inventory.py backlog stage <ID> --stage <SPEC|IR|VAL|BUILD|TEST> --status <done|active|pending|failed|blocked> [--notes]`
  - Inserts new row in `stage_log` with timestamp
  - If status=active, ends any previous active stage for same item
  - Updates `backlog.stage` and `backlog.stage_status` for current state
- [ ] `python _tools/inventory.py backlog graduate <ID> --feature-id <FE-XXX>`
  - Sets `feature_id` column on backlog item
  - Moves item to `kanban_column='done'`
  - Validates feature exists in `features` table (optional warning if not)
  - Does NOT delete the backlog item (preserved for audit trail)
- [ ] Update `cmd_bl_export_md()` to include new columns in markdown table:
  - Add columns: `Column | Stage | Assigned`
  - Show graduated items with ✓ and feature_id link

### Data Validation
- [ ] Kanban column must be one of: `icebox`, `backlog`, `in_progress`, `review`, `done`
- [ ] Stage must be one of: `SPEC`, `IR`, `VAL`, `BUILD`, `TEST`
- [ ] Stage status must be one of: `done`, `active`, `pending`, `failed`, `blocked`
- [ ] Auto-transition rules:
  - Item can only have ONE active stage at a time
  - Setting a stage to `active` ends the previous active stage (sets `ended_at`)
  - Setting a stage to `done` sets `ended_at` timestamp

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Migration runs idempotently (no error if columns already exist)
  - Moving to invalid column fails with clear error
  - Setting stage=active ends previous active stage
  - Graduating item without all stages done issues warning but proceeds
  - Exporting markdown renders new columns correctly
  - Large backlog (100+ items) performs well on queries
- [ ] Test coverage:
  - `test_schema_migration()` — columns added, indexes created
  - `test_backlog_move()` — valid + invalid columns
  - `test_backlog_stage()` — stage transitions, auto-end active
  - `test_backlog_graduate()` — sets feature_id, moves to done
  - `test_stage_log_append_only()` — verify no updates, only inserts
  - `test_backlog_export_md_new_columns()` — markdown output
  - ~15 tests total

## Constraints
- No file over 500 lines — `inventory.py` is currently 705 lines, so the split is MANDATORY before adding code
- After split + new code: `inventory.py` ≤ 350 lines, `inventory_db.py` ≤ 500 lines
- All SQL queries parameterized (no f-strings in WHERE clauses)
- No stubs — every function fully implemented
- Follow existing CLI patterns in `inventory.py` (argparse subcommands, `_connect()`, `_print_table()`)
- Timestamps in UTC, ISO 8601 format

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260313-TASK-044-RESPONSE.md`

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
