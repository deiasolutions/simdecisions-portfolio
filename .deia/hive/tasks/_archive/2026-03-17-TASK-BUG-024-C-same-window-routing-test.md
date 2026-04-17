# TASK-BUG-024-C: Same-window multi-EGG routing integration test

## Objective
Write integration tests simulating the Canvas → Code chat scenario within a SINGLE window to verify messages are correctly routed to the intended pane when multiple EGGs (or multiple instances of panes) coexist.

## Context
The bug report says "Canvas IR response appears in Code chat in different tab." However, the architecture shows MessageBus is per-window. This task tests the alternate hypothesis:
- User opened Canvas and Code as *panes* in the same window
- Terminal in Canvas (pane A) sends `terminal:text-patch` to `links.to_text` pane
- If `links.to_text` resolves to the wrong pane (e.g., Code chat instead of Canvas terminal's linked text-pane), messages appear in the wrong place

This is a **same-window routing issue**, not cross-window.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (lines 456-481: relay mode send)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\chatRenderer.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\messageBus.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx`

## Deliverables
- [ ] Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\terminal-multi-egg-routing.test.tsx`
- [ ] Test case: Create single MessageBus with two panes (terminal1, text1)
- [ ] Test case: Create two more panes (terminal2, text2)
- [ ] Test case: terminal1 sends `terminal:text-patch` to text1 → verify only text1 receives it
- [ ] Test case: terminal2 sends `terminal:text-patch` to text2 → verify only text2 receives it
- [ ] Test case: Simulate Canvas EGG config with `links.to_text` → verify IR routing
- [ ] Test case: Simulate Code EGG config with separate `links.to_text` → verify no leak
- [ ] Edge case: Two panes with same appType but different nodeIds
- [ ] Minimum 8 tests

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Multiple panes of same appType (e.g., two terminals)
  - Targeted messages with correct vs. incorrect paneId
  - Broadcast messages filtered by subscriber
- [ ] Minimum 8 tests

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (no CSS expected)
- No stubs
- Use MessageBus directly (not full Shell integration) for speed

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-BUG-024-C-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — **CRITICAL: Document whether same-window routing works correctly or if this is the actual bug**

DO NOT skip any section.

## Model Assignment
haiku

## Priority
P0 (parallel with TASK-BUG-024-A)
