# TASK-169: Implement Pane Chrome UI Components (Pin, Collapse)

## Objective
Add UI controls to PaneChrome component: pin toggle button, collapse toggle button, conditional close X button based on `chromeOptions`.

## Context
TASK-168 provides the types. This task implements the UI:
- Close X button shows only if `chromeOptions.close !== false`
- Pin toggle button shows if `chromeOptions.pin === true`
- Collapse toggle button shows if `chromeOptions.collapsible === true`

Pin behavior: when active, pane should get full width (sibling collapses). This requires shell reducer support (TASK-170).
Collapse behavior: pane shrinks to ~34px icon strip with expand button. This requires shell reducer support (TASK-170).

For this task: render the buttons, wire them to shell actions (to be handled by reducer in TASK-170). No full behavior implementation yet.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ChromeBtn.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\shell.css`

## Deliverables
- [ ] Update `PaneChrome.tsx` to read `node.chromeOptions` (from TASK-168)
- [ ] Conditionally render close X button only if `chromeOptions.close !== false`
- [ ] Render pin toggle button if `chromeOptions.pin === true`:
  - Icon: 📌 (unpinned) / 📍 (pinned)
  - Title: "Pin pane" / "Unpin pane"
  - Dispatch: `{ type: 'TOGGLE_PIN', nodeId: node.id }`
  - Active state: read from `node.meta.isPinned` (boolean)
- [ ] Render collapse toggle button if `chromeOptions.collapsible === true`:
  - Icon: ◀ (expanded) / ▶ (collapsed)
  - Title: "Collapse pane" / "Expand pane"
  - Dispatch: `{ type: 'TOGGLE_COLLAPSE', nodeId: node.id }`
  - Active state: read from `node.meta.isCollapsed` (boolean)
- [ ] CSS styles for new buttons using `var(--sd-*)` variables only
- [ ] Buttons use existing `ChromeBtn` component for consistency

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test PaneChrome renders close X only when `chromeOptions.close !== false`
- [ ] Test PaneChrome renders pin button only when `chromeOptions.pin === true`
- [ ] Test PaneChrome renders collapse button only when `chromeOptions.collapsible === true`
- [ ] Test pin button dispatches TOGGLE_PIN action
- [ ] Test collapse button dispatches TOGGLE_COLLAPSE action
- [ ] Test pin button shows active state when `node.meta.isPinned === true`
- [ ] Test collapse button shows active state when `node.meta.isCollapsed === true`
- [ ] All tests pass
- [ ] Edge cases:
  - All chrome options false → no extra buttons
  - Multiple chrome options true → all buttons render
  - Maximized pane → restore button still works (existing behavior)

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- All file paths must be absolute

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-169-RESPONSE.md`

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
{"task_id": "TASK-169", "status": "running", "model": "sonnet", "message": "working"}
```

## File Claim
POST to http://localhost:8420/build/claim before modifying files with JSON:
```json
{"task_id": "TASK-169", "files": ["browser/src/shell/components/PaneChrome.tsx", "browser/src/shell/components/__tests__/PaneChrome.test.tsx"]}
```
