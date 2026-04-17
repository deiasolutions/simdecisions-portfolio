# TASK-BUG-036: Build Monitor Tree Layout Fix

## Objective

Fix `buildStatusMapper.ts` so that Active Bees and Completed Tasks display all detail information (model, elapsed time, cost) on the same line as the task ID instead of as indented child nodes.

## Context

The Build Monitor tree view currently renders detail information as indented child nodes below task IDs. This should be part of the main label for a cleaner single-line display.

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

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\buildStatusMapper.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\buildStatusMapper.test.ts`

## Deliverables

- [ ] `mapActiveBees()`: detail appears in label, not as child
- [ ] `mapActiveBees()`: lastMsg still appears as child (if present)
- [ ] `mapCompletedTasks()`: detail appears in label, no children array
- [ ] All existing tests updated to reflect new structure
- [ ] All tests passing

## Test Requirements

- [ ] Update `buildStatusMapper.test.ts` to verify:
  - Active bee label contains model, elapsed time, cost
  - Active bee detail child is removed
  - Active bee lastMsg child remains (if present)
  - Completed task label contains time, duration, cost
  - Completed task has no children array
- [ ] Run: `cd browser && npx vitest run src/primitives/tree-browser/adapters/__tests__/buildStatusMapper.test.ts`
- [ ] All tests must pass
- [ ] TDD: Update tests first, then fix implementation

## Constraints

- No file over 500 lines (currently 279 lines — well under limit)
- CSS: var(--sd-*) only (no CSS changes needed)
- No stubs
- Model: **haiku** (simple refactor)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260318-TASK-BUG-036-RESPONSE.md`

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
