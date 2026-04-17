# TASK-170: Implement Pin and Collapse Reducer Logic

## Objective
Add shell reducer actions to handle `TOGGLE_PIN` and `TOGGLE_COLLAPSE` pane states, implementing the full behavior for pinned and collapsed panes.

## Context
TASK-169 renders the UI buttons. This task implements the logic:

**Pin behavior:**
- When pinned: set `node.meta.isPinned = true`, find sibling pane in parent split, set sibling `node.meta.isCollapsed = true` (temporary forced collapse)
- When unpinned: restore both panes to normal state
- Only works if pane is in a binary split (2 children)

**Collapse behavior:**
- When collapsed: set `node.meta.isCollapsed = true` (pane should render as thin ~34px strip via CSS)
- When expanded: set `node.meta.isCollapsed = false`
- Collapsed pane shows icon strip with expand button (UI in TASK-171)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\reducer.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\utils.ts`

## Deliverables
- [ ] Add `TOGGLE_PIN` action to `ShellAction` type in `browser/src/shell/types.ts`:
  ```typescript
  | { type: 'TOGGLE_PIN'; nodeId: string }
  ```
- [ ] Add `TOGGLE_COLLAPSE` action to `ShellAction` type
- [ ] Implement `TOGGLE_PIN` reducer case in `browser/src/shell/reducer.ts`:
  - Find target node by nodeId
  - Find parent split node (must be binary split)
  - If not in binary split → no-op (log warning)
  - Toggle `node.meta.isPinned` boolean
  - If pinning: find sibling, set `sibling.meta.isCollapsed = true`
  - If unpinning: restore sibling `sibling.meta.isCollapsed = false`
  - Return new tree (immutable update)
- [ ] Implement `TOGGLE_COLLAPSE` reducer case:
  - Find target node by nodeId
  - Toggle `node.meta.isCollapsed` boolean
  - If pane is pinned sibling (sibling.meta.isPinned), don't allow manual collapse toggle (pinned sibling controls it)
  - Return new tree
- [ ] Helper function `findParentSplit(tree, nodeId)` to locate parent split of a node
- [ ] Helper function `getSibling(splitNode, childNodeId)` to find the other child in a binary split

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test `TOGGLE_PIN` sets `isPinned = true` and collapses sibling
- [ ] Test `TOGGLE_PIN` again restores both panes to normal state
- [ ] Test `TOGGLE_PIN` on pane not in binary split → no-op
- [ ] Test `TOGGLE_COLLAPSE` sets `isCollapsed = true`
- [ ] Test `TOGGLE_COLLAPSE` again restores to expanded state
- [ ] Test `TOGGLE_COLLAPSE` on pinned sibling → no-op (pinned pane controls it)
- [ ] All tests pass
- [ ] Edge cases:
  - Pin toggle on root pane (no parent) → no-op
  - Pin toggle on tabbed pane → no-op (only binary splits supported)
  - Collapse toggle while pinned sibling exists → no-op

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (not applicable — reducer logic)
- No stubs
- All file paths must be absolute
- Immutable updates: always return new tree, never mutate existing nodes

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-170-RESPONSE.md`

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
{"task_id": "TASK-170", "status": "running", "model": "sonnet", "message": "working"}
```

## File Claim
POST to http://localhost:8420/build/claim before modifying files with JSON:
```json
{"task_id": "TASK-170", "files": ["browser/src/shell/reducer.ts", "browser/src/shell/types.ts", "browser/src/shell/__tests__/reducer.test.ts"]}
```
