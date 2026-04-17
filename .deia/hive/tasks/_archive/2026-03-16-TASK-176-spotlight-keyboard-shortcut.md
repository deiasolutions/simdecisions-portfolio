# TASK-176: Add Ctrl+Shift+P keyboard shortcut to open SpotlightOverlay

## Objective
Add global Ctrl+Shift+P keyboard shortcut that opens the spotlight overlay by moving the focused pane (or creating an empty pane) to the spotlight branch.

## Context

SpotlightOverlay component is fully implemented with:
- Backdrop dismiss (click backdrop to close)
- 13 existing tests covering display and dismiss behavior
- Renders at z-index 1000 above all other content
- Dispatches REPARENT_TO_BRANCH action when dismissed

**Missing:** Global keyboard shortcut to open spotlight.

### Current Behavior
- Spotlight can be opened programmatically via `REPARENT_TO_BRANCH` action
- Click backdrop dismisses spotlight (moves node back to layout branch)
- Escape key already works (MenuBar.tsx handles Escape globally)

### Required Behavior
- **Ctrl+Shift+P** opens spotlight overlay
- If a pane is focused: move that pane to spotlight branch
- If no pane is focused: create an empty pane in spotlight branch
- If spotlight already open: do nothing (or close it — your choice, document in tests)

### Integration Points

**Shell.tsx** is the best place for the global keyboard listener:
- It's the root shell component
- Has access to dispatch and state via ShellCtx
- Already manages theme state and bus wiring

**Reducer action:**
```typescript
dispatch({
  type: 'REPARENT_TO_BRANCH',
  nodeId: focusedPaneId || newEmptyNode.id,
  fromBranch: 'layout',
  toBranch: 'spotlight',
});
```

**Alternatively use ADD_SPOTLIGHT action** (check reducer.ts):
```typescript
dispatch({ type: 'ADD_SPOTLIGHT', node?: AppNode });
```

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\SpotlightOverlay.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\SpotlightOverlay.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\reducer.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\actions\branch.ts`

## Deliverables

### 1. Tests FIRST (TDD)

**New test file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\Shell.keyboard.test.tsx`

Tests:
- [ ] Ctrl+Shift+P opens spotlight when pane is focused
- [ ] Ctrl+Shift+P creates empty pane in spotlight when no pane focused
- [ ] Ctrl+Shift+P does nothing if spotlight already open (or closes it — document behavior)
- [ ] Other key combos do not trigger spotlight
- [ ] Escape closes spotlight (already works via MenuBar, verify integration)

**Minimum 5 tests.**

### 2. Implementation

**Modify:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx`

Add useEffect hook for keyboard listener:
```typescript
useEffect(() => {
  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.ctrlKey && e.shiftKey && e.key === 'P') {
      e.preventDefault();
      // Logic here: check if spotlight already open, get focused pane, dispatch action
    }
  };

  document.addEventListener('keydown', handleKeyDown);
  return () => document.removeEventListener('keydown', handleKeyDown);
}, [state.focusedPaneId, state.root.spotlight, dispatch]);
```

**Logic:**
1. Check if `state.root.spotlight` is already populated
   - If yes: do nothing (or close it by dispatching REMOVE_SPOTLIGHT)
2. If no spotlight:
   - If `state.focusedPaneId` exists: dispatch REPARENT_TO_BRANCH or ADD_SPOTLIGHT with that node
   - If no focused pane: create empty node and dispatch ADD_SPOTLIGHT

**Check reducer actions in `browser/src/shell/actions/branch.ts`** for ADD_SPOTLIGHT and REPARENT_TO_BRANCH implementations.

### 3. Verify existing tests still pass

- [ ] Run: `cd browser && npx vitest run src/shell/components/__tests__/SpotlightOverlay.test.tsx`
- [ ] All 13 existing tests pass

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All new tests pass (minimum 5 tests)
- [ ] All existing SpotlightOverlay tests still pass (13 tests)
- [ ] Edge cases:
  - Spotlight already open
  - No focused pane
  - Focused pane is in layout branch
  - Keyboard shortcut does not trigger when typing in input field (document this behavior)

## Constraints

- No file over 500 lines (Shell.tsx is ~100 lines, safe to add)
- CSS: var(--sd-*) only
- No stubs
- TDD: tests first

## Acceptance Criteria

- [ ] Ctrl+Shift+P keyboard shortcut implemented in Shell.tsx
- [ ] 5 new tests written and passing in Shell.keyboard.test.tsx
- [ ] All 13 existing SpotlightOverlay tests still pass
- [ ] Keyboard shortcut moves focused pane to spotlight
- [ ] Keyboard shortcut creates empty pane in spotlight if no focused pane
- [ ] No console errors
- [ ] Spotlight can be dismissed via click backdrop (existing behavior, verify still works)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-176-RESPONSE.md`

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
