# SPEC: BL-211 — Make all inventory types have identical modification methods

## Priority: P0

## Problem
The three inventory types have inconsistent command sets:

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

Every type should have the SAME set of modification methods. If one type has it, all types have it. Type-specific commands (fix, done, move, stage, graduate, verify, break) are fine to keep as-is — those are domain-specific status transitions. But the core CRUD operations (add, update, list, search, remove, export-md) must exist on ALL types.

## Scope
Refactor `inventory.py` ONLY.

## Deliverables

### Make bugs have: update, search, remove
- `bug update --id BUG-XXX [--title] [--severity] [--component] [--status] [--description]`
- `bug search <query>` — search bugs by title/component/description
- `bug remove --id BUG-XXX` — mark bug as removed

### Make backlog have: update, search, remove
- `backlog update --id BL-XXX [--title] [--priority] [--category] [--notes] [--source]`
- `backlog search <query>` — search backlog by title/category/notes
- `backlog remove --id BL-XXX` — mark backlog item as removed

### Refactor inventory.py
- All three types should use the same patterns for add/update/list/search/remove/export-md
- Extract shared logic into common helpers where it reduces duplication
- Keep it simple

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory_db.py`

## Files to Modify
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory.py`

## Test Requirements
- bug update: changes severity, changes title, partial update, nonexistent ID errors
- bug search: finds by title substring, finds by component, no results returns empty
- bug remove: marks as removed, nonexistent ID errors
- backlog update: changes priority, changes title, partial update, nonexistent ID errors
- backlog search: finds by title substring, finds by category, no results returns empty
- backlog remove: marks as removed, nonexistent ID errors
- Existing commands still work unchanged

## Constraints
- No file over 500 lines (modularize if needed)
- No stubs
- TDD

## Model: sonnet
