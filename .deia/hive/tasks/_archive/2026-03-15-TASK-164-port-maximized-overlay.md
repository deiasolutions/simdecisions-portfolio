# TASK-164: Port MaximizedOverlay component

## Objective
Port MaximizedOverlay.jsx from platform to browser/src/shell/components/MaximizedOverlay.tsx. This is the final shell chrome component (27 lines). Renders full-screen overlay when a pane is maximized.

## Context
This is the last missing piece from the shell chrome porting sequence. The other 5 components (NotificationModal, ShortcutsPopup, LayoutSwitcher, PinnedPaneWrapper, dragDropUtils) are already ported and have passing tests.

MaximizedOverlay renders a full-screen overlay (z-index 200) when a pane is maximized. It uses the maximizedPaneId from shell state, finds the node, and renders it via ShellNodeRenderer.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\overlays\MaximizedOverlay.jsx` (source)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx` (dependency)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts` (types)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\hooks.ts` (useShell hook)

## Deliverables
- [ ] Port MaximizedOverlay.tsx to `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\MaximizedOverlay.tsx`
- [ ] Convert from JSX to TSX with proper TypeScript types
- [ ] Use useShellStore hook (not useShell context which doesn't exist in shiftcenter)
- [ ] Import ShellNodeRenderer from `./ShellNodeRenderer`
- [ ] Use findNode utility or equivalent from shell utils
- [ ] Verify CSS variables only (var(--sd-*))
- [ ] File must be under 500 lines (source is 27 lines)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Create test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\MaximizedOverlay.test.tsx`
- [ ] Test cases:
  - [ ] Returns null when maximizedPaneId is null
  - [ ] Returns null when node not found
  - [ ] Renders overlay with correct styles when maximized
  - [ ] Renders ShellNodeRenderer with correct node
  - [ ] Applies correct z-index (200)
  - [ ] Uses var(--sd-*) CSS variables only
  - [ ] Applies animation class
- [ ] All new tests pass
- [ ] All existing shell tests still pass (634 tests)
- [ ] Edge cases: missing node, undefined maximizedPaneId

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (no hardcoded colors)
- No stubs
- TDD: tests first, then implementation
- Use TypeScript strict mode
- Import patterns must match existing shell components
- POST heartbeat to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  ```json
  {
    "task_id": "2026-03-15-TASK-164-port-maximized-overlay",
    "status": "running",
    "model": "haiku",
    "message": "working"
  }
  ```

## Adaptation Notes
The platform version uses:
- `useShell()` from shell.context.js — REPLACE with `useShellStore()` from `../../stores/shellStore`
- `findNode(root, id)` utility — CHECK if this exists in shiftcenter shell utils or implement inline
- `ShellNodeRenderer` — exists in shiftcenter, import from `./ShellNodeRenderer`

The shiftcenter version should:
- Use Zustand store instead of context
- Use proper TypeScript types for all props and state
- Follow existing shell component patterns (see PinnedPaneWrapper.tsx as reference)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-164-RESPONSE.md`

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

## Success Criteria
- MaximizedOverlay.tsx exists and compiles
- Tests pass (minimum 7 tests)
- No new shell test failures
- No hardcoded colors
- File under 500 lines
- No stubs
