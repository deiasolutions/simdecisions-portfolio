# Briefing: Fix Kanban Route Test — Wrong Table Assumption

## Objective
Fix the kanban route test that looks for a separate `inv_kanban_items` table. Kanban is a column (`kanban_column`) on the existing inventory tables, not a separate table.

## What's Broken
- Test: `tests/hivenode/routes/test_kanban_routes.py::test_kanban_items_get_all`
- Error: `sqlalchemy.exc.OperationalError: table inv_kanban_items not found`
- The test assumes a separate kanban table exists, but kanban is implemented as a `kanban_column` field on inventory tables
- Reference: `.deia/hive/responses/20260318-FULL-TEST-SWEEP-REPORT.md` section "Kanban (1)"
- Evidence: `hivenode/inventory/store.py` uses `kanban_column` on existing tables (lines 49, 445, 514, 669, 680)

## What To Do
1. Read `hivenode/routes/kanban_routes.py` to understand the route
2. Read `tests/hivenode/routes/test_kanban_routes.py` to see the failing test
3. Read `hivenode/inventory/store.py` to see how kanban_column is used
4. Fix the test (and route if needed) to use the inventory table's kanban_column instead of a separate table
5. Run the test to confirm fix

## Model: haiku

## Response
Write response to: `.deia/hive/responses/20260318-FIX-KANBAN-TEST.md`
