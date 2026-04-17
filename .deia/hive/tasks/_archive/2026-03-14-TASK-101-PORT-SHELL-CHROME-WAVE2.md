# TASK-101: Port Shell Chrome — Wave 2 (Shell Context Components)

## Objective
Port 4 shell-context-dependent chrome components from old repo to shiftcenter: PaneMenu, PinnedPaneWrapper, SpotlightOverlay, GovernanceProxy. These require integration with existing shell reducer/dispatch/context.

## Context
Wave 2 of a 3-wave shell chrome port. These components use shell context, dispatch actions, and wrap other components (PaneChrome, AppFrame, EmptyPane). The spec is at `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-SHELL-001-shell-chrome-port.md`.

**Rule:** PORT, NOT REWRITE. Same props, same logic, same CSS classes. TypeScript conversion + `var(--sd-*)` theming only.

**Dependencies:** Wave 1 (TASK-100) must complete first to provide HighlightOverlay.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-SHELL-001-shell-chrome-port.md` (lines 132–177 for these 4 components)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\PaneMenu.jsx` (111 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\PinnedPaneWrapper.jsx` (73 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\SpotlightOverlay.jsx` (93 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\components\shell\GovernanceProxy.tsx` (160 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts` (ShellNode types)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\reducer.ts` (actions)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\useShell.ts` (useShell hook)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx` (existing chrome)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\AppFrame.tsx` (existing frame)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\EmptyPane.tsx` (existing empty)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ContextMenu.tsx` (existing menu)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ChromeBtn.tsx` (existing button)

## Deliverables
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneMenu.tsx` (port from old)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PinnedPaneWrapper.tsx` (port from old)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\SpotlightOverlay.tsx` (port from old)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\GovernanceProxy.tsx` (port from old)
- [ ] Vitest unit tests for all 4 components

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - PaneMenu: portal to `.hhp-root`, outside-click handler with containment check, act() wrapper closes menu, disabled states when locked, swap pending toggle
  - PinnedPaneWrapper: fixed position from node.meta (x, y, w, h), defaults (100, 100, 600, 400), orange border, SET_FOCUS on mouseDown, renders PaneChrome or EmptyPane
  - SpotlightOverlay: 800×600 modal, orange border, backdrop click → REPARENT_TO_BRANCH, renders PaneChrome or EmptyPane
  - GovernanceProxy: intercepts bus.send/subscribe, platform invariants always allowed, logs blocked events via LOG_EVENT

## Constraints
- No file over 500 lines (none are close)
- CSS: `var(--sd-*)` only
- No stubs
- Props interfaces MUST match spec exactly
- CSS class names MUST match spec
- Portal target: `.hhp-root`
- PaneMenu uses existing ContextMenu component from shiftcenter
- PaneMenu uses existing ChromeBtn component from shiftcenter
- GovernanceProxy: verify existing `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\gate_enforcer\` aligns with old `ResolvedPermissions` shape

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-101-RESPONSE.md`

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
