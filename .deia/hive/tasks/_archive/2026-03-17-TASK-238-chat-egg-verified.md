# TASK-238: Chat EGG Verified (Wave 4.10)

## Objective

Verify that `eggs/chat.egg.md` renders correctly as a 3-pane layout with proper proportions, seamless borders, and functional chat rendering. This is Wave 4 Task 4.10 (Product Polish).

## Context

The chat.egg.md defines a 3-pane layout:
- **Left sidebar (22%):** tree-browser with chat-history adapter
- **Center top (70%):** text-pane with markdown chat output (renderMode: "chat")
- **Center bottom (30%):** terminal with `routeTarget: "ai"` and 3-currency status bar

TASK-229 already verified that chat bubbles render correctly (user right, AI left, copy button, markdown). This task focuses on verifying the overall EGG layout renders properly in the browser.

The chat.egg.md uses `seamless: true` on the center split, which should remove visible borders between chat output and terminal input.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\chat.egg.md` (131 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggLoader.ts` (EGG parsing logic)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\layoutEngine.tsx` (layout rendering)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\chatRenderer.tsx` (chat bubble rendering)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\Terminal.tsx` (terminal component)

## Deliverables

- [ ] Manual verification: Load `http://localhost:5173/?egg=chat` in browser and verify all three panes render
- [ ] Manual verification: Verify left sidebar shows tree-browser (even if empty)
- [ ] Manual verification: Verify center top shows text-pane with chat rendering
- [ ] Manual verification: Verify center bottom shows terminal with prompt
- [ ] Manual verification: Verify border between chat and terminal is seamless (no visible divider)
- [ ] Manual verification: Verify 3-currency status bar appears (clock, coin, carbon)
- [ ] Automated test: Write integration test to verify EGG layout structure matches spec
- [ ] Automated test: Write test to verify `seamless: true` flag is respected
- [ ] Automated test: Write test to verify terminal config includes `routeTarget: "ai"`
- [ ] Fix any rendering issues found during verification
- [ ] Update test file if any existing tests conflict with the fixes

## Test Requirements

- [ ] Tests written FIRST (TDD) for any rendering issues found
- [ ] All existing tests still pass after fixes
- [ ] New tests: minimum 3 (layout structure, seamless flag, routeTarget config)
- [ ] Edge cases:
  - [ ] Empty chat history (tree-browser shows empty state)
  - [ ] No active conversation (text-pane shows placeholder)
  - [ ] Terminal renders status bar even with no provider configured

## Acceptance Criteria

- [ ] Load `?egg=chat` in browser and verify:
  - [ ] Left sidebar (22%): chat-history tree-browser visible
  - [ ] Center top (70%): chat output text-pane visible
  - [ ] Center bottom (30%): terminal with `routeTarget: "ai"` visible
  - [ ] Seamless border between chat output and terminal (no visible divider)
- [ ] Verify chat bubbles render (user right, AI left) per TASK-229 results
- [ ] Verify terminal shows prompt (e.g., "hive>")
- [ ] Verify 3-currency status bar shows (clock, coin, carbon)
- [ ] Fix any layout or rendering issues discovered
- [ ] Run: `cd browser && npx vitest run` — all tests pass
- [ ] Run: `cd browser && npm run build` — build succeeds with no errors

## Constraints

- No file over 500 lines (if modularization needed, split files)
- CSS: `var(--sd-*)` only (no hardcoded colors)
- No stubs in any code written
- TDD: write tests before implementation for any fixes

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-238-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary (last 5 lines)
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Notes

- TASK-229 verified chat bubble rendering (42 tests passing for chatRenderer)
- The `seamless: true` flag is critical for product polish
- This is a verification task — write tests and fix issues, but don't add features beyond the spec
- Manual verification steps are required because EGG rendering involves browser layout engine
