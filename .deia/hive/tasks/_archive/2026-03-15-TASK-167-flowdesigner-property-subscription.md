# TASK-167: FlowDesigner Property Update Subscription

## Objective
Subscribe FlowDesigner to `canvas:property-updated` events and update node data in React Flow when properties are edited in the tree panel.

## Context
TASK-165 added inline editing to TreeNodeRow. TASK-166 wired the adapter to emit bus events. This task completes the circuit: FlowDesigner listens for `canvas:property-updated` events and updates the canvas node accordingly.

**Current state:**
- FlowDesigner.tsx: 921 lines (WARNING: close to 1,000 line hard limit)
- Bus events already exist for other features (e.g., channel:selected)
- React Flow nodes already have label and description fields

**Dependencies:**
- TASK-165 must be complete (editable TreeNodeRow)
- TASK-166 must be complete (adapter emits events)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\constants.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\Canvas.broadcast.test.tsx` (existing bus event tests)

## Deliverables

### 1. Add bus subscription in FlowDesigner
- [ ] Subscribe to `canvas:property-updated` event in useEffect
- [ ] On event: extract `nodeId`, `field`, `value` from payload
- [ ] Find node in React Flow state by `nodeId`
- [ ] Update node.data[field] with new value
- [ ] Call `setNodes()` to trigger React Flow re-render
- [ ] Unsubscribe on unmount

### 2. Handle edge cases
- [ ] If node not found by ID, log warning but do not throw error
- [ ] If field is invalid (not "label" or "description"), log warning and ignore
- [ ] Ensure immutability: clone nodes array before updating

### 3. Tests (TDD — write FIRST)
- [ ] Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\__tests__\Canvas.property-updates.test.tsx`
- [ ] Test: FlowDesigner subscribes to `canvas:property-updated` on mount
- [ ] Test: emitting `canvas:property-updated` with label updates node label in React Flow state
- [ ] Test: emitting `canvas:property-updated` with description updates node description
- [ ] Test: event with unknown node ID logs warning, does not crash
- [ ] Test: event with invalid field logs warning, does not update
- [ ] Test: unsubscribes on unmount (no memory leak)
- [ ] All tests pass

## File Size Constraint — CRITICAL
**FlowDesigner.tsx is at 921 lines.** Hard limit is 1,000 lines. This task adds ~20-30 lines.

If you project FlowDesigner will exceed 1,000 lines after this task:
- STOP. Do NOT proceed.
- Write response file with status: BLOCKED
- Recommend: extract bus subscription logic to separate hook (e.g., `useCanvasPropertySubscription.ts`)

If under 1,000 lines after edits: proceed.

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases covered:
  - Unknown node ID (log warning, no crash)
  - Invalid field name (log warning, no update)
  - Unmount cleanup (no memory leak)

## Constraints
- FlowDesigner.tsx MUST NOT exceed 1,000 lines after this task
- CSS: var(--sd-*) only (no hardcoded colors)
- No stubs (fully implemented functions)
- Immutability: clone nodes array before updating (React Flow best practice)

## Heartbeat

POST to `http://localhost:8420/build/heartbeat` every 3 minutes with JSON:
```json
{
  "task_id": "2026-03-15-TASK-167-flowdesigner-property-subscription",
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
     "task_id": "2026-03-15-TASK-167-flowdesigner-property-subscription",
     "files": [
       "C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\shiftcenter\\browser\\src\\apps\\sim\\components\\flow-designer\\FlowDesigner.tsx"
     ]
   }
   ```
2. If response has conflicts (ok=false), you are queued FIFO. Poll GET http://localhost:8420/build/claims every 30s until the file is yours.
3. When done with a file, release it early so other bees can proceed:
   ```json
   {
     "task_id": "2026-03-15-TASK-167-flowdesigner-property-subscription",
     "files": ["C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\shiftcenter\\browser\\src\\apps\\sim\\components\\flow-designer\\FlowDesigner.tsx"]
   }
   ```
4. On heartbeat complete/failed, all your claims auto-release. Claims expire after 10 minutes.

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260315-TASK-167-RESPONSE.md`

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
