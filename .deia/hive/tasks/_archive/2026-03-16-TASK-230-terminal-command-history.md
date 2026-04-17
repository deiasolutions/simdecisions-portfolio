# TASK-230: Terminal Command History Persistence

## Objective
Verify terminal command history navigation (up/down arrows) works as expected, then add localStorage persistence so command history survives page reloads.

## Context
Wave 4 Product Polish (BL-069), task 4.2 from `docs/specs/WAVE-4-PRODUCT-POLISH.md`.

The command history logic was implemented in BL-069 with:
- 100-item ring buffer
- Deduplication of consecutive commands
- Up-arrow/down-arrow navigation wired in TerminalPrompt.tsx
- Tests for ring buffer, deduplication, and navigation

**Current state:**
- localStorage persistence is PARTIALLY implemented in `useTerminal.ts`:
  - Lines 145-158: Load from localStorage on mount
  - Lines 246-251: Save to localStorage on history change
  - Key: `sd:terminal_command_history`

**What needs verification/fixing:**
1. Confirm up/down arrow navigation works
2. Confirm localStorage persistence actually works across page reloads
3. Add tests for localStorage persistence (save, restore, corruption handling)
4. Fix any bugs found during verification

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalPrompt.tsx` (lines 94-111: arrow key handlers)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (lines 99-100, 145-158, 246-251: history state + persistence)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\commandHistory.test.ts` (existing tests)

## Deliverables

### Verification (Already Built)
- [ ] Up-arrow recalls previous commands in single-line mode
- [ ] Down-arrow navigates forward through history
- [ ] Consecutive duplicate commands are deduplicated
- [ ] History caps at 100 items
- [ ] History loads from localStorage on mount
- [ ] History saves to localStorage after each command

### New Work (Add Tests)
- [ ] Add new test file: `browser/src/primitives/terminal/__tests__/commandHistoryPersistence.test.ts`
- [ ] Test: history saves to localStorage after command submission
- [ ] Test: history loads from localStorage on mount
- [ ] Test: corrupted localStorage data (invalid JSON) is handled gracefully
- [ ] Test: localStorage data exceeding 100 items is truncated to 100 on load
- [ ] Test: empty localStorage returns empty history
- [ ] Minimum 5 new persistence tests

### Bug Fixes (If Any)
- [ ] Fix any bugs found during verification
- [ ] Document fixes in response file

## Test Requirements
Run all terminal tests after changes:
```bash
cd browser && npx vitest run src/primitives/terminal/
```

Expected test counts:
- **Existing tests:** commandHistory.test.ts has ~17 tests (based on describe blocks)
- **New tests:** Minimum 5 persistence tests in commandHistoryPersistence.test.ts
- **Total expected:** At least 22 terminal tests passing

## Constraints
- **No hardcoded colors.** CSS variables (`var(--sd-*)`) only.
- **No file over 500 lines.** Modularize at 500. Hard limit: 1,000.
- **TDD.** Write tests first, then fix bugs if any.
- **NO STUBS.** Every function fully implemented.
- **localStorage key:** Use existing `sd:terminal_command_history` (already in code)

## Acceptance Criteria
- [ ] All existing terminal tests pass (commandHistory.test.ts)
- [ ] 5+ new persistence tests pass (commandHistoryPersistence.test.ts)
- [ ] Manual smoke test: Type 3 commands, reload page, press up-arrow → sees last command
- [ ] Manual smoke test: localStorage corrupted (manually set to `"{bad json"`) → terminal loads without crashing, shows empty history
- [ ] No console errors related to localStorage or command history
- [ ] Response file includes test output showing all tests passing

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-230-RESPONSE.md`

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

## Model Assignment
haiku

## Estimated Time
30 minutes
