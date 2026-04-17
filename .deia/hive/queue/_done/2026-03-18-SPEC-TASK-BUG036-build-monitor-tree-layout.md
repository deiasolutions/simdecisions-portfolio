# SPEC: BUG-036 — Build monitor tree items show detail indented below instead of same line

## Priority: P0

## Problem
In `buildStatusMapper.ts`, the Active Bees and Completed Tasks mappers put model/role/elapsed/cost info as **children nodes** instead of on the same label line. This causes the tree-browser to render them as bulleted items indented below the task ID, instead of a single-line summary per item.

## Root Cause
`mapActiveBees()` (lines 148-159) creates a parent node with `label: "${role} ${shortId}"` and then puts `detail` (model, elapsed, cost) and `lastMsg` as child nodes.

`mapCompletedTasks()` (lines 260-274) creates a parent node with `label: "${abbreviateId(task.task_id)}"` and then puts `detail` (time, duration, cost) as a child node.

## Fix Required

### mapActiveBees — fold detail into the label
**Before:** label is `${role} ${shortId}`, detail is a child node
**After:** label should be `${role} ${shortId} ${detail}` (model, elapsed, cost all on one line). Remove the detail child. Keep lastMsg as an optional child if present (that one is fine as a sub-line).

### mapCompletedTasks — fold detail into the label
**Before:** label is `${abbreviateId(task.task_id)}`, detail is a child node
**After:** label should be `${abbreviateId(task.task_id)} ${detail}` (time, duration, cost all on one line). Remove the children array entirely.

## Files to Modify
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\buildStatusMapper.ts`

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\buildStatusMapper.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\buildStatusMapper.test.ts`

## Test Requirements
- Update existing buildStatusMapper tests to expect detail on the label line, not as children
- Active bee node label should contain model, elapsed time, and cost
- Completed task node label should contain time, duration, and cost
- No children array on completed tasks
- Active bees may still have lastMsg as a child (optional)

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- TDD

## Model: haiku
