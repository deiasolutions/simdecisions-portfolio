# TASK-BUG-024-A: Verify cross-window message isolation

## Objective
Write tests demonstrating that MessageBus instances in different tabs/windows cannot leak messages to each other. Verify the bug report is accurate or identify the actual issue.

## Context
Bug report claims messages from Canvas EGG in tab A appear in Code EGG chat pane in tab B. Investigation shows:
- MessageBus is instantiated per Shell (line 31 in Shell.tsx)
- Each tab/window creates its own Shell and MessageBus instance
- No BroadcastChannel or localStorage event sync exists for messages
- Messages are routed via in-memory subscription map (`this._subs`)

This task verifies whether the bug exists and identifies the actual root cause.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\messageBus.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\__tests__\messageBus.test.ts`

## Deliverables
- [ ] Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\__tests__\messageBus.crossWindow.test.ts`
- [ ] Test case: Create two MessageBus instances (simulating two tabs)
- [ ] Test case: Send message on bus1, verify bus2 subscribers never receive it
- [ ] Test case: Broadcast message on bus1, verify bus2 subscribers never receive it
- [ ] Test case: Send targeted message with paneId collision across buses, verify isolation
- [ ] Documentation comment in messageBus.ts explaining per-window architecture
- [ ] Root cause analysis in response file (bug exists vs. misreported vs. same-window routing issue)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Two buses with identical paneIds (e.g., both have pane "p123")
  - Broadcast vs. targeted messages
  - Rapid message sending
- [ ] Minimum 8 tests

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (no CSS expected)
- No stubs
- Test must NOT use BroadcastChannel or localStorage — test in-memory isolation only

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-BUG-024-A-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — **CRITICAL: Document root cause analysis here. Does the bug exist? If not, what is the actual issue?**

DO NOT skip any section.

## Model Assignment
haiku

## Priority
P0
