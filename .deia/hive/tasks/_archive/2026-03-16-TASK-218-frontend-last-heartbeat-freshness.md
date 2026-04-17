# TASK-218: Frontend Last Heartbeat Freshness Check

## Objective
Update Active Bees frontend mapping to use `last_heartbeat` timestamp to distinguish truly active bees from stale entries.

## Context
After TASK-216, task entries have two timestamps:
- `last_heartbeat`: updated on every heartbeat (liveness)
- `last_seen`: updated only on state transitions (status changes, new messages)

The Active Bees pane should show only tasks where:
1. `status` is "running" or "dispatched", AND
2. `last_heartbeat` is fresh (within last 30 minutes)

This prevents showing stale entries from crashed bees or bees that transitioned to complete/failed but haven't been cleaned up yet.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\buildStatusMapper.ts` (lines 106-141: `mapActiveBees` function)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\build_monitor.py` (to understand `last_heartbeat` field structure)

## Deliverables
- [ ] Add `last_heartbeat?: string` field to `TaskState` TypeScript interface
- [ ] Modify `mapActiveBees()` to filter out tasks where `last_heartbeat` is stale (> 30 minutes old)
- [ ] Handle case where `last_heartbeat` is undefined (backward compatibility) — fall back to `last_seen`
- [ ] Add helper function `isHeartbeatFresh(timestamp: string | undefined, maxAgeMinutes: number): boolean`
- [ ] Update SSE snapshot handler in `buildDataService.tsx` to include `last_heartbeat` in TaskState type

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Task with fresh `last_heartbeat` (< 30 min) → included in active list
  - Task with stale `last_heartbeat` (> 30 min) → excluded from active list
  - Task with no `last_heartbeat` field → fall back to `last_seen`
  - Task with invalid timestamp → excluded from active list
  - Task with status "complete" but fresh `last_heartbeat` → excluded (status takes precedence)
- [ ] Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\__tests__\buildStatusMapper.test.ts`
- [ ] Minimum 6 tests covering all edge cases above

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (N/A for this task)
- No stubs
- Preserve existing badge display, icon logic, and role formatting
- Do NOT modify the SSE stream backend or build log mapping

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-218-RESPONSE.md`

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
