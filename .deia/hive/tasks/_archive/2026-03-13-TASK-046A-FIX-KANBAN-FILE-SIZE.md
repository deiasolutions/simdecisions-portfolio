# TASK-046A: Fix KanbanPane File Size + 2 Test Failures

## Objective
Split `KanbanPane.tsx` (1,032 lines — over 1,000-line hard limit) into smaller components and fix the 2 failing tests.

## Context
TASK-046 created the kanban pane primitive but produced a single 1,032-line file. This violates Rule 4 (500-line limit, 1,000 hard limit). The component needs to be split into sub-components. Additionally, 2 of 16 tests are failing and need fixes.

**DO NOT rewrite from scratch.** Extract existing code into separate files.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\KanbanPane.tsx` (1,032 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\__tests__\KanbanPane.test.tsx` (418 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\types.ts`

## Deliverables

### 1. Split KanbanPane.tsx into components
- [ ] Extract column rendering into `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\KanbanColumn.tsx`
- [ ] Extract card rendering into `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\KanbanCard.tsx`
- [ ] Extract filter/toolbar into `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\KanbanToolbar.tsx`
- [ ] Extract settings sheet into `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\KanbanSettings.tsx` (if settings logic exists)
- [ ] Extract mobile move sheet into `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\kanban-pane\KanbanMobileSheet.tsx` (if mobile sheet exists)
- [ ] KanbanPane.tsx should be the orchestrator only — import sub-components, manage state via useKanban hook
- [ ] **Target: every file ≤ 400 lines**

### 2. Fix 2 failing tests
- [ ] Run the test suite, identify the 2 failures, fix them
- [ ] All 16 tests must pass after fixes

### 3. CSS variables
- [ ] Verify all new CSS variables (`--sd-col-*`, `--sd-pri-*`, `--sd-type-*`) were added to `browser/src/shell/shell-themes.css`
- [ ] If not added by TASK-046, add them now (see TASK-046 task file for the variable definitions)

## Test Requirements
- [ ] All 16 kanban pane tests pass
- [ ] Full browser suite: no regressions
- [ ] No file over 500 lines

## Constraints
- No file over 500 lines
- CSS: `var(--sd-*)` only
- No stubs
- Pure refactor + test fix — no new features

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260313-TASK-046A-RESPONSE.md`

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
