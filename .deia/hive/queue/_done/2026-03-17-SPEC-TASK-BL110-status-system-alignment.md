# BL-110: Status system alignment (kanban + dev cycle + inventory unification)

## Objective
Align the status systems across kanban, dev cycle, and inventory so they use a single unified status model.

## Context
Currently there are separate status enums/models in kanban (todo/doing/done), dev cycle (queue/claimed/buzz/archive), and inventory (OPEN/FIXED). These need alignment so the same item can be tracked consistently across all views.

## Files to Read First
- `hivenode/inventory/store.py`
- `browser/src/primitives/kanban/`
- `_tools/inventory.py`
- `.deia/processes/`

## Deliverables
- [ ] Define unified status model that maps across all three systems
- [ ] Update kanban to use unified status
- [ ] Update inventory to recognize kanban statuses
- [ ] Status transitions are consistent
- [ ] Tests for status mapping

## Acceptance Criteria
- [ ] Single status model works across kanban, dev cycle, inventory
- [ ] Status transitions are consistent
- [ ] No data loss on status mapping
- [ ] Tests pass

## Smoke Test
- [ ] `cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter" && python -m pytest tests/hivenode/ -v -k status`
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/kanban/`

## Constraints
- No file over 500 lines
- No stubs

## Model Assignment
haiku

## Priority
P0
