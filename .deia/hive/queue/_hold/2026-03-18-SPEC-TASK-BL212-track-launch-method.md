# SPEC: BL-212 — Track launch method (queued vs direct) in inventory

## Priority: P2

## Problem
When a feature, bug fix, or backlog item is completed, we have no record of HOW it was launched — whether it was dispatched through the queue runner (queued) or fixed directly in a live session (direct). This matters for process analysis: understanding what percentage of work flows through the automated queue vs manual intervention.

## Objective
Add a `launch_method` field to all inventory types (features, bugs, backlog) that captures whether the item was completed via `queued` (queue runner dispatch) or `direct` (live session fix). Update the CLI, store, and display to support this.

## Model: haiku

## Acceptance Criteria
- [ ] Add `launch_method TEXT` column to `inv_features`, `inv_bugs`, `inv_backlog` tables (nullable, default NULL for existing rows)
- [ ] Valid values: `queued`, `direct`, or NULL (unknown/legacy)
- [ ] `inventory.py add` and `bug add` and `backlog add` accept optional `--launch-method` flag
- [ ] `inventory.py list` and `bug list` and `backlog list` display launch_method column when present
- [ ] `export-md` includes launch_method in the markdown table
- [ ] Queue runner specs that complete via queue automatically get `launch_method=queued` when archived by Q33N
- [ ] Tests: at least 8 tests covering add/list/export with launch_method
- [ ] No file over 500 lines

## Smoke Test
- `python _tools/inventory.py add --id FE-TEST --title 'test' --task TASK-999 --layer backend --tests 1 --launch-method queued` succeeds
- `python _tools/inventory.py list` shows launch_method column
- `python _tools/inventory.py export-md` includes launch method

## Constraints
- No file over 500 lines
- TDD — tests first
- Migration must be backwards-compatible (nullable column, no breaking changes to existing data)

## Files to Read First
- `_tools/inventory.py`
- `_tools/inventory_db.py`
- `hivenode/inventory/store.py`
- `docs/FEATURE-INVENTORY.md`
