# TASK-172: E2E Tests for Pane Chrome Options

## Objective
Write end-to-end integration tests verifying the full pin/collapse/close flow with EGG inflation and user interaction.

## Context
TASK-168, 169, 170, 171 implement the feature. This task verifies the complete user flow:
- EGG with `chromeClose: false` → close X button hidden
- EGG with `chromePin: true` → pin button visible, clicking pins pane and collapses sibling
- EGG with `chromeCollapsible: true` → collapse button visible, clicking collapses pane to icon strip
- Icon strip expand button restores pane

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\PaneChrome.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\__tests__\reducer.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggInflater.ts`

## Deliverables
- [ ] Create E2E test file: `browser/src/shell/components/__tests__/PaneChrome.e2e.test.tsx`
- [ ] Test 1: EGG with `chromeClose: false` → close X button not rendered
- [ ] Test 2: EGG with `chromePin: true` → pin button renders and toggles `isPinned` state
- [ ] Test 3: Pin button click → sibling pane collapses (icon strip shown)
- [ ] Test 4: Unpin button click → sibling pane expands (full chrome restored)
- [ ] Test 5: EGG with `chromeCollapsible: true` → collapse button renders and toggles `isCollapsed` state
- [ ] Test 6: Collapse button click → pane becomes icon strip with expand button
- [ ] Test 7: Expand button on icon strip → pane restores to full chrome
- [ ] Test 8: Pinned sibling cannot manually collapse (collapse button disabled)
- [ ] Test 9: All chrome options combined work together
- [ ] All tests pass

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Use real EGG inflation via `eggLayoutToShellTree()`
- [ ] Use real shell reducer for state changes
- [ ] Simulate user clicks with `@testing-library/react` `fireEvent` or `userEvent`
- [ ] Verify DOM updates after state changes
- [ ] All tests pass
- [ ] Edge cases:
  - Pin pane not in binary split → no-op
  - Collapse then pin → both states coexist
  - Pin then collapse sibling manually → blocked

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (not applicable — tests)
- No stubs
- All file paths must be absolute

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-172-RESPONSE.md`

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

## Build Heartbeat
POST to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
```json
{"task_id": "TASK-172", "status": "running", "model": "haiku", "message": "working"}
```

## File Claim
POST to http://localhost:8420/build/claim before modifying files with JSON:
```json
{"task_id": "TASK-172", "files": ["browser/src/shell/components/__tests__/PaneChrome.e2e.test.tsx"]}
```
