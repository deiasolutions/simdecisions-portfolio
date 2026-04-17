# TASK-BUG-024-B: Add windowId scoping to MessageBus (defensive measure)

## Objective
Add window/tab identification to MessageBus and MessageEnvelope to future-proof against cross-window leaks if someone adds BroadcastChannel or other cross-tab sync in the future.

## Context
Current architecture:
- MessageBus is per-window (created in Shell.tsx)
- No cross-window communication exists
- TASK-BUG-024-A verified whether cross-window leaks occur

This task adds defensive scoping:
- Generate a unique `windowId` when MessageBus is created
- Add `windowId` to MessageEnvelope type
- Add `windowId` validation in `send()` and `subscribe()` (no-op for now, but enables future filtering)
- Document that windowId should be checked if cross-window sync is ever added

This is a **defensive measure** to prevent future regressions if someone ports BroadcastChannel sync from platform repo.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\messageBus.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx`

## Deliverables
- [ ] Add `windowId` field to MessageBus constructor (generated via crypto.randomUUID or Date.now)
- [ ] Add `windowId` field to MessageEnvelope type (optional for backward compat)
- [ ] Populate `windowId` in `bus.send()` method
- [ ] Add JSDoc comment warning future developers to filter by windowId if adding BroadcastChannel
- [ ] Tests updated to verify windowId is populated
- [ ] Tests verify two bus instances have different windowIds
- [ ] All existing relay bus tests still pass

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Two MessageBus instances have unique windowIds
  - windowId is populated in every sent message
  - windowId does not break existing message routing
- [ ] Add 4 new tests to existing test suite

## Constraints
- No file over 500 lines (messageBus.ts is 301 lines — OK)
- CSS: var(--sd-*) only (no CSS expected)
- No stubs
- Do NOT add BroadcastChannel sync (just add the windowId field)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-BUG-024-B-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — any issues discovered, edge cases, next tasks

DO NOT skip any section.

## Model Assignment
haiku

## Priority
P1 (defensive measure, depends on TASK-BUG-024-A findings)
