# BRIEFING: BUG-036 — Build Monitor Tree Layout Fix

**Date:** 2026-03-18
**From:** Q33NR
**To:** Q33N
**Priority:** P0

---

## Objective

Fix `buildStatusMapper.ts` so that Active Bees and Completed Tasks show all detail (model, elapsed time, cost) on the same line as the task ID instead of as indented child nodes.

---

## Problem

In the Build Monitor tree view, Active Bees and Completed Tasks are rendering detail information as indented child nodes below the task ID, when they should be part of the main label for a cleaner single-line display.

### Current Behavior

**Active Bees (lines 148-159):**
- Label: `${role} ${shortId}`
- Creates child node with detail (model, elapsed, cost)
- Result: detail appears indented below task ID

**Completed Tasks (lines 260-274):**
- Label: `${abbreviateId(task.task_id)}`
- Creates child node with detail (time, duration, cost)
- Result: detail appears indented below task ID

### Required Behavior

**Active Bees:**
- Label should be: `${role} ${shortId} ${detail}` (all on one line)
- Remove the detail child node
- Keep `lastMsg` as an optional child (if present) — that's fine as a sub-line

**Completed Tasks:**
- Label should be: `${abbreviateId(task.task_id)} ${detail}` (all on one line)
- Remove the children array entirely

---

## Context

- File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\buildStatusMapper.ts`
- Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\buildStatusMapper.test.ts`
- The `detail` variable is already computed correctly in both functions
- We just need to move it from a child node into the main label

---

## Files to Modify

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\buildStatusMapper.ts`
   - Modify `mapActiveBees()` (lines 148-159)
   - Modify `mapCompletedTasks()` (lines 260-274)

2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\buildStatusMapper.test.ts`
   - Update tests to expect detail in label, not as children
   - Active bee nodes should not have detail child
   - Completed task nodes should have no children array (unless there's a lastMsg)

---

## Acceptance Criteria

- [ ] `mapActiveBees()`: detail appears in label, not as child
- [ ] `mapActiveBees()`: lastMsg still appears as child (if present)
- [ ] `mapCompletedTasks()`: detail appears in label, no children array
- [ ] All existing tests updated and passing
- [ ] Build monitor displays correctly (single-line task entries)

---

## Test Requirements

- Update existing `buildStatusMapper.test.ts` to verify:
  - Active bee label contains model, elapsed time, cost
  - Active bee detail child is removed
  - Active bee lastMsg child remains (optional)
  - Completed task label contains time, duration, cost
  - Completed task has no children array
- All tests must pass
- TDD: verify tests first, then fix implementation

---

## Constraints

- No file over 500 lines (currently 279 lines — well under limit)
- CSS: var(--sd-*) only (no CSS changes needed)
- No stubs
- Model: **haiku** (simple refactor)

---

## Dispatch Instructions

After Q33NR approval:
1. Create task file in `.deia/hive/tasks/`
2. Dispatch single bee with haiku model
3. Wait for completion
4. Review response file
5. Report back to Q33NR

---

**END BRIEFING**
