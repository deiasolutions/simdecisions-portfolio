# TASK-166: Properties Adapter Event Emission

## Objective
Update simPropertiesAdapter to emit relay bus events when tree nodes are edited — enabling FlowDesigner to receive property updates.

## Context
TASK-165 adds inline editing to TreeNodeRow. This task connects that edit capability to the relay bus, so that when a user edits a node property in the tree panel, the event flows to FlowDesigner (which will handle the event in TASK-167).

**Current state:**
- simPropertiesAdapter.ts: 127 lines
- TreeNodeRow: now editable (TASK-165)
- relay_bus constants exist: `browser/src/infrastructure/relay_bus/constants.ts`

**Dependencies:**
- TASK-165 must be complete (editable TreeNodeRow)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\simPropertiesAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\constants.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\types.ts`

## Deliverables

### 1. Add new bus event type
- [ ] Add `canvas:property-updated` to `browser/src/infrastructure/relay_bus/constants.ts` (if not already present)
- [ ] Define event payload interface:
  ```typescript
  interface CanvasPropertyUpdatedPayload {
    nodeId: string;       // Canvas node ID (e.g., "node-1")
    field: string;        // Property field name (e.g., "label", "description")
    value: string;        // New value
  }
  ```

### 2. Update simPropertiesAdapter
- [ ] Add `editable: true` to tree nodes returned by `mapNodeToTreeNode()`
- [ ] Add `onEdit` callback that:
  - Validates the edit (non-empty string)
  - Extracts canvas node ID from tree node ID (e.g., "property-node-1-label" → "node-1")
  - Emits `canvas:property-updated` event with payload: `{ nodeId, field, value }`
- [ ] Ensure no file exceeds 500 lines

### 3. Tests (TDD — write FIRST)
- [ ] Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\simPropertiesAdapter.events.test.ts`
- [ ] Test: tree nodes have `editable: true`
- [ ] Test: tree nodes have `onEdit` callback
- [ ] Test: onEdit emits `canvas:property-updated` with correct payload (label edit)
- [ ] Test: onEdit emits `canvas:property-updated` with correct payload (description edit)
- [ ] Test: onEdit extracts correct canvas node ID from tree node ID
- [ ] Test: onEdit does NOT emit event if value is empty string
- [ ] All tests pass

## Scope Constraints
**Fields to support:**
- `label` (string)
- `description` (string)

**NOT in scope:**
- `duration.value` (deferred to follow-up task)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases covered:
  - Empty string validation
  - Node ID extraction (tree node ID → canvas node ID)
  - Bus event emission (spy on relay_bus.emit)

## Constraints
- No file over 500 lines (hard limit: 1,000)
- CSS: var(--sd-*) only (no hardcoded colors in event payloads)
- No stubs (fully implemented functions)
- Validation: do NOT emit event for empty string values

## Heartbeat

POST to `http://localhost:8420/build/heartbeat` every 3 minutes with JSON:
```json
{
  "task_id": "2026-03-15-TASK-166-properties-adapter-events",
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
     "task_id": "2026-03-15-TASK-166-properties-adapter-events",
     "files": [
       "C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\shiftcenter\\browser\\src\\primitives\\tree-browser\\adapters\\simPropertiesAdapter.ts",
       "C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\shiftcenter\\browser\\src\\infrastructure\\relay_bus\\constants.ts"
     ]
   }
   ```
2. If response has conflicts (ok=false), you are queued FIFO. Poll GET http://localhost:8420/build/claims every 30s until the file is yours.
3. When done with a file, release it early so other bees can proceed:
   ```json
   {
     "task_id": "2026-03-15-TASK-166-properties-adapter-events",
     "files": ["C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\shiftcenter\\browser\\src\\primitives\\tree-browser\\adapters\\simPropertiesAdapter.ts"]
   }
   ```
4. On heartbeat complete/failed, all your claims auto-release. Claims expire after 10 minutes.

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260315-TASK-166-RESPONSE.md`

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
