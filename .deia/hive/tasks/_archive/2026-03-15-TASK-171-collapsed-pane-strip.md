# TASK-171: Implement Collapsed Pane Icon Strip

## Objective
Create CollapsedPaneStrip component: renders a thin (~34px wide) vertical strip with pane icon and expand button when `node.meta.isCollapsed === true`.

## Context
When a pane is collapsed (via collapse toggle or pinned sibling), it should shrink to a minimal icon strip instead of hiding completely. The strip shows:
- Pane icon (from APP_REGISTRY)
- Pane label (vertical text or tooltip)
- Expand button (▶ arrow icon)

Clicking expand button or the strip itself dispatches `TOGGLE_COLLAPSE` to restore the pane.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\constants.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\shell.css`

## Deliverables
- [ ] Create new component: `browser/src/shell/components/CollapsedPaneStrip.tsx`
- [ ] Component interface:
  ```typescript
  interface CollapsedPaneStripProps {
    node: AppNode;
  }
  ```
- [ ] Render vertical strip (~34px wide, full height):
  - Background: `var(--sd-surface-alt)`
  - Border: `1px solid var(--sd-border-subtle)`
  - Pane icon at top (from APP_REGISTRY, fontSize 14px)
  - Vertical text label (CSS `writing-mode: vertical-rl`, `transform: rotate(180deg)`) OR tooltip on hover
  - Expand button at bottom (▶ icon, fontSize 12px)
- [ ] On click anywhere: dispatch `{ type: 'TOGGLE_COLLAPSE', nodeId: node.id }`
- [ ] Update `ShellNodeRenderer.tsx` to check `node.meta.isCollapsed`:
  - If true: render `<CollapsedPaneStrip node={node} />` instead of full PaneChrome
  - If false: render PaneChrome as normal
- [ ] CSS styles in `shell.css` using `var(--sd-*)` variables only:
  ```css
  .collapsed-pane-strip {
    width: 34px;
    min-width: 34px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 8px 0;
    background: var(--sd-surface-alt);
    border-right: 1px solid var(--sd-border-subtle);
    cursor: pointer;
    transition: background 0.15s;
  }
  .collapsed-pane-strip:hover {
    background: var(--sd-surface-hover);
  }
  ```
- [ ] Create test file: `browser/src/shell/components/__tests__/CollapsedPaneStrip.test.tsx`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test CollapsedPaneStrip renders icon from APP_REGISTRY
- [ ] Test CollapsedPaneStrip renders label (vertical or tooltip)
- [ ] Test CollapsedPaneStrip renders expand button
- [ ] Test clicking strip dispatches TOGGLE_COLLAPSE action
- [ ] Test ShellNodeRenderer shows CollapsedPaneStrip when `node.meta.isCollapsed === true`
- [ ] Test ShellNodeRenderer shows PaneChrome when `node.meta.isCollapsed === false`
- [ ] All tests pass
- [ ] Edge cases:
  - Pane with no icon → fallback icon (□)
  - Long label → truncated or tooltip
  - Collapsed + maximized → shouldn't happen (collapse disabled when maximized)

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- All file paths must be absolute

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-171-RESPONSE.md`

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
{"task_id": "TASK-171", "status": "running", "model": "sonnet", "message": "working"}
```

## File Claim
POST to http://localhost:8420/build/claim before modifying files with JSON:
```json
{"task_id": "TASK-171", "files": ["browser/src/shell/components/CollapsedPaneStrip.tsx", "browser/src/shell/components/ShellNodeRenderer.tsx", "browser/src/shell/components/__tests__/CollapsedPaneStrip.test.tsx", "browser/src/shell/components/shell.css"]}
```
