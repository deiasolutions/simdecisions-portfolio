# TASK-R18: Fix Kanban routes schema mismatch

## Objective
Fix the 1 error in `tests/hivenode/test_kanban_routes.py` where SQLAlchemy insert fails on `inv_backlog` table.

## Context
R13 verification found 1 error — `test_kanban_items_get_all` fails with a SQLAlchemy insert error. TASK-159 (entity archetypes) may have modified a shared database model causing schema mismatch.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_kanban_routes.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\kanban.py` (or similar)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\database.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-R13-RESPONSE.md`

## Deliverables
- [ ] Identify the schema mismatch (missing column, wrong type, etc.)
- [ ] Fix the model or migration to match expected schema
- [ ] Run: `python -m pytest tests/hivenode/test_kanban_routes.py -v`
- [ ] All kanban tests must pass

## Constraints
- Minimal fix — only fix the schema mismatch, don't refactor
- If the model was intentionally changed, update the test fixture instead

## Acceptance Criteria
- [ ] Kanban route tests pass (0 errors)
- [ ] No regressions in other tests

## Response Requirements — MANDATORY
Write response to: `.deia/hive/responses/20260316-TASK-R18-RESPONSE.md`
All 8 sections required.
