# BRIEFING: BL-211 — Inventory Uniform CRUD

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Queen Regent)
**Date:** 2026-03-18
**Model Assignment:** Sonnet (refactoring task, requires careful planning)

---

## Objective

Refactor `inventory.py` so all three inventory types (features, bugs, backlog) have identical CRUD command sets. Every type must support: add, update, list, search, remove, export-md. Type-specific status transitions (fix, done, move, stage, graduate, verify, break) remain unchanged.

---

## Context from Q88N

The current state is inconsistent:

| Command | Features | Bugs | Backlog |
|---------|----------|------|---------|
| add | YES | YES | YES |
| update | YES | NO | NO |
| list | YES | YES | YES |
| search | YES | NO | NO |
| remove | YES | NO | NO |
| export-md | YES | YES | YES |
| verify | YES | NO | NO |
| break | YES | NO | NO |
| fix | NO | YES | NO |
| done | NO | NO | YES |
| move | NO | NO | YES |
| stage | NO | NO | YES |
| graduate | NO | NO | YES |

Bugs and backlog are missing: update, search, remove.

---

## What Needs to Happen

### 1. Add missing commands to bugs
- `bug update --id BUG-XXX [--title] [--severity] [--component] [--status] [--description]`
- `bug search <query>` — search by title/component/description
- `bug remove --id BUG-XXX` — mark as removed

### 2. Add missing commands to backlog
- `backlog update --id BL-XXX [--title] [--priority] [--category] [--notes] [--source]`
- `backlog search <query>` — search by title/category/notes
- `backlog remove --id BL-XXX` — mark as removed

### 3. Refactor for consistency
- All three types should use the same patterns for shared operations
- Extract common helpers where it reduces duplication
- Keep it simple (follow existing patterns in features code)

---

## Files to Review

**Primary:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory_db.py`

**Related (for understanding existing patterns):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\inventory\store.py`

---

## Constraints

1. **No file over 500 lines.** Current `inventory.py` is already large. Modularize if needed.
2. **TDD.** Write tests first for new commands.
3. **No stubs.** Full implementation required.
4. **Only modify `inventory.py`.** Do not change the database schema or store.py.
5. **Keep existing commands working.** This is additive + refactoring, not replacement.
6. Hard Rule 10: NO GIT OPERATIONS without Q88N approval.

---

## Test Requirements

Create `_tools/tests/test_inventory_crud.py` (or add to existing test file):

**bug update:**
- Changes severity (P1 → P2)
- Changes title
- Partial update (only one field)
- Nonexistent ID errors with clear message

**bug search:**
- Finds by title substring
- Finds by component
- No results returns empty list
- Case-insensitive

**bug remove:**
- Marks as removed (does not delete from DB)
- Nonexistent ID errors

**backlog update:**
- Changes priority (P1 → P2)
- Changes title
- Partial update
- Nonexistent ID errors

**backlog search:**
- Finds by title substring
- Finds by category
- No results returns empty list
- Case-insensitive

**backlog remove:**
- Marks as removed
- Nonexistent ID errors

**Regression:**
- Existing `feature add`, `feature list`, `bug add`, `backlog add` still work unchanged

---

## Expected Deliverables

1. **Test file** with all scenarios above (~15-20 tests minimum)
2. **Refactored inventory.py** with:
   - `bug update` command
   - `bug search` command
   - `bug remove` command
   - `backlog update` command
   - `backlog search` command
   - `backlog remove` command
   - Common helpers extracted if it reduces duplication
3. **All tests pass** (new + existing)
4. **File stays under 1,000 lines** (modularize if approaching limit)

---

## Task Breakdown Guidance

This is a **single-bee task** (Sonnet). Do not split into multiple tasks unless the bee discovers `inventory.py` would exceed 1,000 lines after changes.

If modularization is needed:
- Extract common CRUD patterns to `inventory_crud.py`
- Keep CLI parsing in `inventory.py`
- Maintain backward compatibility

---

## Response to Q33NR

After you read this briefing and the codebase:

1. Write a task file to `.deia/hive/tasks/2026-03-18-TASK-BL211-inventory-uniform-crud.md`
2. Return the task file to me for review
3. DO NOT dispatch bees until I approve
4. Summarize:
   - What you will deliver
   - Test count estimate
   - Any concerns or clarifications needed

---

## Priority

P0 — inventory CLI is critical infrastructure for the hive workflow.
