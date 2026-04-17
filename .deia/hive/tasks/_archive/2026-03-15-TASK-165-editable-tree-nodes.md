# TASK-165: Editable Tree Nodes Infrastructure

## Objective
Add inline editing capability to TreeNodeRow for string fields (label, description) — foundation for property editing in sim properties panel.

## Context
Currently TreeNodeRow is read-only. We need inline editing to support sim property editing (label, description fields). This task builds the infrastructure. Subsequent tasks will wire it to FlowDesigner via the relay bus.

**File line counts (current):**
- TreeNodeRow.tsx: 110 lines
- TreeBrowser.tsx: 160 lines

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeBrowser.tsx`

## Deliverables

### 1. Update TreeNode interface in types.ts
- [ ] Add optional `editable?: boolean` flag to TreeNode interface
- [ ] Add optional `onEdit?: (nodeId: string, field: string, newValue: string) => void` callback

### 2. Update TreeNodeRow component
- [ ] Accept `editable` and `onEdit` props from parent TreeBrowser
- [ ] Render label as editable inline text input when `editable=true` and field is clicked
- [ ] On blur or Enter key, call `onEdit(node.id, 'label', newValue)`
- [ ] Restore previous value if newValue is empty string (inline validation)
- [ ] Style: use existing CSS variables (var(--sd-*) only)
- [ ] Ensure no file exceeds 500 lines

### 3. Update TreeBrowser component
- [ ] Accept optional `editable` and `onEdit` props
- [ ] Pass `editable` and `onEdit` to TreeNodeRow children

### 4. Tests (TDD — write FIRST)
- [ ] Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\TreeNodeRow.editable.test.tsx`
- [ ] Test: clicking label when editable=true renders input element
- [ ] Test: blur with valid value calls onEdit
- [ ] Test: Enter key with valid value calls onEdit
- [ ] Test: blur with empty string does NOT call onEdit (restores previous value)
- [ ] Test: Escape key restores previous value and exits edit mode
- [ ] Test: editable=false (default) renders label as read-only span
- [ ] All tests pass

## Scope Constraints
**Fields to support in this task:**
- `label` (string, required)
- `description` (optional string — only if node.meta.description exists)

**NOT in scope for this task:**
- `duration.value` (number validation complexity — deferred to follow-up task)
- Multi-line editing
- Rich text editing

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases covered:
  - Empty string input (validation)
  - Escape key (cancel edit)
  - Enter key (commit edit)
  - Blur (commit edit)
  - Rapid edit mode toggle

## Constraints
- No file over 500 lines (hard limit: 1,000)
- CSS: var(--sd-*) only (no hex, rgb, or named colors)
- No stubs (fully implemented functions)
- Inline validation: restore previous value on invalid input (empty string)

## Heartbeat

POST to `http://localhost:8420/build/heartbeat` every 3 minutes with JSON:
```json
{
  "task_id": "2026-03-15-TASK-165-editable-tree-nodes",
  "status": "running",
  "model": "haiku",
  "message": "working"
}
```

On completion, POST final heartbeat with `"status": "complete"` or `"status": "failed"`.

## File Claims (IMPORTANT — parallel bees)

Before modifying any file, claim it to prevent conflicts with other bees:
1. POST http://localhost:8420/build/claim with JSON:
   ```json
   {
     "task_id": "2026-03-15-TASK-165-editable-tree-nodes",
     "files": [
       "C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\shiftcenter\\browser\\src\\primitives\\tree-browser\\TreeNodeRow.tsx",
       "C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\shiftcenter\\browser\\src\\primitives\\tree-browser\\types.ts",
       "C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\shiftcenter\\browser\\src\\primitives\\tree-browser\\TreeBrowser.tsx"
     ]
   }
   ```
2. If response has conflicts (ok=false), you are queued FIFO. Poll GET http://localhost:8420/build/claims every 30s until the file is yours.
3. When done with a file, release it early so other bees can proceed:
   ```json
   {
     "task_id": "2026-03-15-TASK-165-editable-tree-nodes",
     "files": ["C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\shiftcenter\\browser\\src\\primitives\\tree-browser\\TreeNodeRow.tsx"]
   }
   ```
4. On heartbeat complete/failed, all your claims auto-release. Claims expire after 10 minutes.

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260315-TASK-165-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full absolute paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
