# TASK-BL211: Inventory Uniform CRUD

**Bot ID:** BEE-SONNET-BL211
**Model:** Sonnet (refactoring + TDD)
**Priority:** P0
**Estimated Scope:** Medium (3-4 hours)

---

## Objective

Add missing CRUD commands (`update`, `search`, `remove`) to bugs and backlog in `inventory.py`, making all three inventory types (features, bugs, backlog) have identical CRUD command sets.

---

## Context

The current inventory CLI has inconsistent command coverage:

**Features** have: add, update, list, search, remove, verify, break, export-md
**Bugs** have: add, list, fix, export-md — **MISSING:** update, search, remove
**Backlog** have: add, list, done, move, stage, graduate, export-md — **MISSING:** update, search, remove

This task fills the gaps so all three types have uniform CRUD operations. Type-specific status transitions (fix, done, move, stage, graduate, verify, break) remain unchanged.

---

## Files to Read First

**Primary:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory.py` (510 lines — CLI implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory_db.py` (60 lines — imports from store)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\inventory\store.py` (653 lines — backend CRUD functions)

**For test patterns:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\tests\test_cli_status_validation.py` (174 lines — CLI test patterns)

---

## Deliverables

### 1. Backend Functions in `store.py`

Add these missing functions to `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\inventory\store.py`:

- [ ] `db_update_bug(bug_id, updates_dict)` — update title, severity, component, status, or description
- [ ] `db_search_bugs(query)` — search by title, component, or description (case-insensitive)
- [ ] `db_remove_bug(bug_id, notes)` — mark as REMOVED (add notes column if needed, or use description)
- [ ] `db_update_backlog(bid, updates_dict)` — update title, priority, category, notes, or source
- [ ] `db_search_backlog(query)` — search by title, category, or notes (case-insensitive)
- [ ] `db_remove_backlog(bid, notes)` — mark as removed (soft delete, not hard delete like `done`)

**Pattern to follow:** Copy the structure of `db_update_feature()` and `db_search_features()`.

**Notes handling:** If bugs table doesn't have a `notes` column, either:
1. Add it via migration (preferred), OR
2. Use `description` field for removal notes

### 2. CLI Commands in `inventory.py`

Add these command handlers to `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory.py`:

**Bug commands:**
- [ ] `cmd_bug_update(args)` — wrapper for `db_update_bug()`
- [ ] `cmd_bug_search(args)` — wrapper for `db_search_bugs()`
- [ ] `cmd_bug_remove(args)` — wrapper for `db_remove_bug()`

**Backlog commands:**
- [ ] `cmd_bl_update(args)` — wrapper for `db_update_backlog()`
- [ ] `cmd_bl_search(args)` — wrapper for `db_search_backlog()`
- [ ] `cmd_bl_remove(args)` — wrapper for `db_remove_backlog()`

**Argparse updates:**
- [ ] Add `bug update` subparser with args: `id, --title, --severity, --component, --status, --description`
- [ ] Add `bug search` subparser with arg: `query`
- [ ] Add `bug remove` subparser with args: `id, --notes`
- [ ] Add `backlog update` subparser with args: `id, --title, --priority, --category, --notes, --source`
- [ ] Add `backlog search` subparser with arg: `query`
- [ ] Add `backlog remove` subparser with args: `id, --notes`

**Update `cmd_map` dicts:**
- Add entries in `cmd_bug()` for: `"update": cmd_bug_update`, `"search": cmd_bug_search`, `"remove": cmd_bug_remove`
- Add entries in `cmd_backlog()` for: `"update": cmd_bl_update`, `"search": cmd_bl_search`, `"remove": cmd_bl_remove`

### 3. Update `inventory_db.py` Exports

Add new function imports to `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory_db.py`:

```python
from hivenode.inventory.store import (
    # ... existing imports ...
    db_update_bug, db_search_bugs, db_remove_bug,
    db_update_backlog, db_search_backlog, db_remove_backlog,
)
```

### 4. Test File

Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\tests\test_inventory_crud.py` with:

**Bug update tests (5 tests):**
- [ ] `test_bug_update_changes_severity` — change P1 → P2
- [ ] `test_bug_update_changes_title` — change title
- [ ] `test_bug_update_partial` — update only one field
- [ ] `test_bug_update_nonexistent_id` — error with clear message
- [ ] `test_bug_update_invalid_severity` — rejects invalid severity

**Bug search tests (4 tests):**
- [ ] `test_bug_search_finds_by_title` — finds by title substring
- [ ] `test_bug_search_finds_by_component` — finds by component
- [ ] `test_bug_search_no_results` — returns empty list
- [ ] `test_bug_search_case_insensitive` — "BUG" matches "bug"

**Bug remove tests (2 tests):**
- [ ] `test_bug_remove_marks_as_removed` — status becomes REMOVED
- [ ] `test_bug_remove_nonexistent_id` — error with clear message

**Backlog update tests (5 tests):**
- [ ] `test_backlog_update_changes_priority` — change P1 → P2
- [ ] `test_backlog_update_changes_title` — change title
- [ ] `test_backlog_update_partial` — update only one field
- [ ] `test_backlog_update_nonexistent_id` — error with clear message
- [ ] `test_backlog_update_invalid_priority` — rejects invalid priority

**Backlog search tests (4 tests):**
- [ ] `test_backlog_search_finds_by_title` — finds by title substring
- [ ] `test_backlog_search_finds_by_category` — finds by category
- [ ] `test_backlog_search_no_results` — returns empty list
- [ ] `test_backlog_search_case_insensitive` — "ENHANCEMENT" matches "enhancement"

**Backlog remove tests (2 tests):**
- [ ] `test_backlog_remove_marks_as_removed` — soft delete, not hard delete
- [ ] `test_backlog_remove_nonexistent_id` — error with clear message

**Regression tests (4 tests):**
- [ ] `test_feature_add_still_works` — unchanged
- [ ] `test_feature_list_still_works` — unchanged
- [ ] `test_bug_add_still_works` — unchanged
- [ ] `test_backlog_add_still_works` — unchanged

**Total: 26 tests minimum**

---

## Test Requirements

- [ ] Write tests FIRST (TDD)
- [ ] All 26+ tests pass
- [ ] Use subprocess.run() to test CLI (follow pattern in `test_cli_status_validation.py`)
- [ ] Test both success and error cases
- [ ] Verify error messages are clear (include ID, reason)
- [ ] Test case-insensitive search
- [ ] Test partial updates (only one field changed)

---

## Implementation Guidance

### Backend Functions (store.py)

**Update pattern (from `db_update_feature`):**
```python
def db_update_bug(bug_id, updates_dict):
    if not updates_dict:
        return False, "nothing to update"
    eng = get_engine()
    with eng.begin() as conn:
        row = conn.execute(
            select(bugs_table.c.id).where(bugs_table.c.id == bug_id)
        ).fetchone()
        if not row:
            return False, f"bug '{bug_id}' not found"
        conn.execute(
            bugs_table.update().where(bugs_table.c.id == bug_id)
            .values(**updates_dict)
        )
    return True, None
```

**Search pattern (from `db_search_features`):**
```python
def db_search_bugs(query):
    eng = get_engine()
    q = f"%{query.lower()}%"
    with eng.connect() as conn:
        rows = conn.execute(
            select(bugs_table).where(
                or_(
                    func.lower(bugs_table.c.title).like(q),
                    func.lower(bugs_table.c.component).like(q),
                    func.lower(bugs_table.c.description).like(q),
                )
            ).order_by(bugs_table.c.severity, bugs_table.c.id)
        ).fetchall()
    return _rows_to_dicts(rows)
```

**Remove pattern (soft delete):**
```python
def db_remove_bug(bug_id, notes):
    eng = get_engine()
    with eng.begin() as conn:
        row = conn.execute(
            select(bugs_table.c.id).where(bugs_table.c.id == bug_id)
        ).fetchone()
        if not row:
            return False, f"bug '{bug_id}' not found"
        now = _now()
        conn.execute(
            bugs_table.update().where(bugs_table.c.id == bug_id)
            .values(status="REMOVED", resolved_at=now, resolved_by=notes)
        )
    return True, None
```

**Notes:** If bugs table doesn't have a REMOVED status in `VALID_BUG_STATUSES`, add it. If there's no `notes` column, use `resolved_by` to store removal notes.

### CLI Functions (inventory.py)

**Update command pattern:**
```python
def cmd_bug_update(args):
    updates = {}
    if args.title:
        updates["title"] = args.title
    if args.severity:
        if args.severity not in VALID_BUG_SEVERITIES:
            print(f"Error: severity must be one of {VALID_BUG_SEVERITIES}", file=sys.stderr)
            sys.exit(1)
        updates["severity"] = args.severity
    if args.component:
        updates["component"] = args.component
    if args.status:
        if args.status not in VALID_BUG_STATUSES:
            print(f"Error: status must be one of {VALID_BUG_STATUSES}", file=sys.stderr)
            sys.exit(1)
        updates["status"] = args.status
    if args.description:
        updates["description"] = args.description

    ok, err = db_update_bug(args.id, updates)
    if not ok:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)
    print(f"Updated {args.id}")
```

**Search command pattern:**
```python
def cmd_bug_search(args):
    rows = db_search_bugs(args.query)
    _print_table(rows, ["id", "severity", "component", "title", "status", "resolved_by"])
```

**Remove command pattern:**
```python
def cmd_bug_remove(args):
    if not args.notes:
        print("Error: --notes required when removing a bug.", file=sys.stderr)
        sys.exit(1)
    ok, err = db_remove_bug(args.id, args.notes)
    if not ok:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)
    print(f"Marked {args.id} as REMOVED")
```

---

## Constraints

1. **No file over 500 lines.** Current `inventory.py` is 510 lines. After adding 6 commands + argparse, it may exceed 600 lines. If it exceeds 700 lines, extract shared helpers to `inventory_crud.py`.
2. **Hard limit: 1,000 lines.** If approaching this, MUST modularize.
3. **TDD.** Tests first, implementation second.
4. **NO STUBS.** Every function fully implemented.
5. **Consistent patterns.** Follow existing `cmd_*` and `db_*` patterns exactly.
6. **Error messages.** Include the ID and reason in all error messages.
7. **Case-insensitive search.** Use `func.lower()` and `.like()` patterns.
8. **Hard Rule 10:** NO GIT OPERATIONS. Do not commit.

---

## Acceptance Criteria

- [ ] 6 new backend functions in `store.py` (3 for bugs, 3 for backlog)
- [ ] 6 new CLI commands in `inventory.py` (3 for bugs, 3 for backlog)
- [ ] 6 new argparse subparsers
- [ ] `inventory_db.py` exports all new functions
- [ ] Test file with 26+ tests, all passing
- [ ] `bug update --id BUG-XXX --severity P2` works
- [ ] `bug search <query>` works (case-insensitive)
- [ ] `bug remove --id BUG-XXX --notes "reason"` works
- [ ] `backlog update --id BL-XXX --priority P1` works
- [ ] `backlog search <query>` works (case-insensitive)
- [ ] `backlog remove --id BL-XXX --notes "reason"` works
- [ ] Existing commands unchanged (regression tests pass)
- [ ] File stays under 1,000 lines (modularize if needed)
- [ ] No hardcoded colors (N/A — CLI only)
- [ ] All tests pass: `cd _tools && python -m pytest tests/test_inventory_crud.py -v`

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260318-TASK-BL211-RESPONSE.md`

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

## Notes for Bee

1. **If bugs table needs a `notes` column:** Add it via a migration helper in `store.py` (follow pattern in `_migrate_backlog_project()`). Do NOT manually edit SQL files.

2. **If REMOVED status doesn't exist:** Add `"REMOVED"` to `VALID_BUG_STATUSES` in `store.py` and `inventory_db.py`.

3. **Backlog remove vs done:** `done` hard-deletes the row. `remove` should soft-delete (mark as removed, keep row). Use a `removed` column or `kanban_column='removed'` to indicate removed state.

4. **File size management:** If `inventory.py` exceeds 700 lines, create `inventory_crud.py` with shared helpers (e.g., `_print_table`, `_validate_updates`). Keep CLI parsing in `inventory.py`.

5. **Test database:** Tests use Railway PostgreSQL by default (from `inventory_db.py`). To use local SQLite for tests, set `INVENTORY_DATABASE_URL=local` in test setup.

6. **Imports:** All new functions must be imported in `inventory_db.py` AND used in `inventory.py`.

---

## Model Assignment Rationale

**Sonnet assigned** because:
- Refactoring task requires careful pattern matching
- 6 new functions + 6 CLI commands + 26+ tests = ~500 lines of new code
- Needs to maintain consistency with existing code
- Medium complexity (not trivial, but not architecture-level)
