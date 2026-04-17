# TASK-BUG029: Stage App Add Warning

## Objective
When a user tries to add/drop an app onto a pane that already has an app, show a confirmation warning instead of silently replacing the existing app.

## Context
The stage manages app placement in panes. Currently, when an app is dropped onto a pane that already has content (i.e., `appType !== 'empty'`), the existing app is silently replaced without warning. This can cause accidental data loss if the user didn't realize they were overwriting an existing app.

**Current behavior:**
1. User drags app A onto pane containing app B
2. App B is silently replaced with app A
3. User may not notice until later

**Desired behavior:**
1. User drags app A onto pane containing app B
2. System detects occupied pane
3. Confirmation dialog appears: "This pane already contains [App B]. Replace it with [App A]?"
4. User clicks "Replace" → app B is replaced
5. User clicks "Cancel" → drop is cancelled, app B remains

**Exception:** Dropping onto an EMPTY pane should NOT show a warning (empty panes are meant to be filled).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\actions\layout.ts` (MOVE_APP action, line 143-201)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx` (drop handling)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx` (pane rendering)

## Strategy
1. Read `layout.ts` to understand the `MOVE_APP` action (line 143-201)
   - Line 160-165: center zone logic checks if `targetNode.appType === 'empty'`
   - If NOT empty, we need to show confirmation before replacing
2. Identify where to inject the confirmation check:
   - Option A: Add a new shell state field `pendingReplace: { sourceId, targetId, zone } | null`
   - Option B: Dispatch a new action `CONFIRM_REPLACE_APP` that shows a dialog
   - Option C: Use a simple `window.confirm()` (quickest, but not themeable)
3. **Recommended:** Add a shell state field + confirmation dialog component
4. Modify `MOVE_APP` action to:
   - Detect if targetNode is occupied (appType !== 'empty')
   - If occupied, set `pendingReplace` state instead of executing move
   - Render a confirmation dialog that dispatches `CONFIRM_REPLACE` or `CANCEL_REPLACE`
5. Write tests for all paths:
   - Drop on empty pane → no warning, move succeeds
   - Drop on occupied pane → warning shown, confirm → move succeeds
   - Drop on occupied pane → warning shown, cancel → move cancelled
   - Drop on tabbed pane → no warning (tabs append, don't replace)
   - Drop to create split (left/right/top/bottom zones) → no warning (split creates new pane)

## Files You May Modify
**Maximum files:** 3

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\actions\layout.ts` (MOVE_APP logic)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts` (add `pendingReplace` to ShellState)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ReplaceConfirmDialog.tsx` (new confirmation dialog component)
- Test file for the confirmation logic

## Files You Must NOT Modify
- Any primitive files (anything in `browser/src/primitives/`)
- Any adapter files
- Any backend files (`hivenode/`, `engine/`)
- Shell reducer files other than `layout.ts` and `types.ts`

## Deliverables
- [ ] Confirmation warning shown when dropping app onto occupied pane (center zone only)
- [ ] Confirmation dialog has "Replace" and "Cancel" buttons
- [ ] "Replace" → existing app is replaced, move succeeds
- [ ] "Cancel" → move is cancelled, existing app remains
- [ ] Empty panes do NOT show warning
- [ ] Tabbed panes do NOT show warning (tabs append)
- [ ] Split zones (left/right/top/bottom) do NOT show warning (split creates new pane)
- [ ] Tests verify all paths

## Test Requirements
**Minimum tests:** 5

- [ ] Tests written FIRST (TDD)
- [ ] Test: drop on empty pane → no warning, move succeeds
- [ ] Test: drop on occupied pane (center zone) → warning shown
- [ ] Test: confirm warning → move succeeds, target app replaced
- [ ] Test: cancel warning → move cancelled, target app preserved
- [ ] Test: drop to create split (left/right/top/bottom zone) → no warning, split created

**Test file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\ReplaceConfirmDialog.test.tsx`

## Build Verification
```bash
# Run shell tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run src/shell/

# Build
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npm run build
```

Include test summary and last 5 lines of build output in response file.

## Constraints
- No file over 500 lines
- CSS: `var(--sd-*)` only (no hardcoded colors)
- NO stubs — dialog component fully implemented
- Dialog must use existing shell theme variables
- Dialog should portal to `.hhp-root` (per MEMORY.md)

## Response Requirements — MANDATORY
When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260319-TASK-BUG029-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes (not intent)
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Acceptance Criteria
- [ ] Confirmation warning shown when dropping app onto occupied pane (center zone)
- [ ] Warning has "Replace" and "Cancel" buttons
- [ ] "Replace" → app replaced
- [ ] "Cancel" → drop cancelled
- [ ] Empty panes do NOT show warning
- [ ] Tabbed panes do NOT show warning
- [ ] Split zones do NOT show warning
- [ ] 5+ tests pass (empty pane, occupied pane, confirm, cancel, split zone)
- [ ] All existing tests still pass
- [ ] Build succeeds
- [ ] No hardcoded colors
- [ ] No files exceed 500 lines

## Model Assignment
haiku

## Risk
LOW — UI enhancement, no breaking changes to existing behavior
