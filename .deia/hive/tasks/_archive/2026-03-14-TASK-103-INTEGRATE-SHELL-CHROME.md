# TASK-103: Integrate Shell Chrome Components into Shell

## Objective
Wire all ported shell chrome components (from TASK-100, TASK-101, TASK-102) into Shell.tsx and ShellNodeRenderer.tsx. Add EGG config toggles for top chrome bars.

## Context
Final integration task after all 3 waves complete. This task makes the ported components visible and functional in the shell. The spec is at `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-SHELL-001-shell-chrome-port.md` (lines 321–338).

**Rule:** Integration only. Do NOT modify the ported components. Wire them into existing shell infrastructure.

**Dependencies:** TASK-100, TASK-101, TASK-102 must all complete successfully.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-SHELL-001-shell-chrome-port.md` (lines 321–338)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx` (current shell with MenuBar/ShellTabBar stubs)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx` (renders shell nodes)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx` (current chrome, may need PaneMenu integration)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\useEggInit.ts` (EggUiConfig type)
- All 13 ported components from TASK-100, TASK-101, TASK-102

## Deliverables
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx`:
  - Replace MenuBar stub with real component (import from TASK-102)
  - Replace ShellTabBar stub with real component (import from TASK-102)
  - Add WorkspaceBar above MenuBar when `uiConfig.workspaceBar: true`
  - Add SpotlightOverlay rendering for `state.root.spotlight` nodes (replace current inline spotlight rendering)
  - Add PinnedPaneWrapper rendering for `state.root.pinned` nodes
  - Add NotificationModal rendering at shell level (driven by notification state — may need new state slice)
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellNodeRenderer.tsx`:
  - Wrap each AppFrame in GovernanceProxy (nodeId, permissions from node.meta or default)
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx`:
  - Wire hamburger button to open PaneMenu (import from TASK-101) instead of inline ContextMenu
  - PaneMenu should replace or augment existing pane menu logic
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\useEggInit.ts`:
  - Add `workspaceBar?: boolean` to `EggUiConfig` interface (if not present)
- [ ] Create integration test: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\ShellChromeIntegration.test.tsx`
  - Test MenuBar appears when `uiConfig.menuBar: true`
  - Test ShellTabBar appears when `uiConfig.shellTabBar: true`
  - Test WorkspaceBar appears when `uiConfig.workspaceBar: true`
  - Test SpotlightOverlay renders when `state.root.spotlight` has a node
  - Test PinnedPaneWrapper renders for pinned nodes
  - Test GovernanceProxy wraps AppFrame

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - EGG config toggles: menuBar, shellTabBar, workspaceBar all default to false (no chrome unless opted in)
  - Spotlight overlay: click backdrop dismisses, click inside does not
  - Pinned panes: render at fixed positions from node.meta
  - GovernanceProxy: wraps all occupied panes, not empty panes
  - NotificationModal: driven by shell-level notification state (may need reducer updates)

## Constraints
- No file over 500 lines
- CSS: `var(--sd-*)` only
- No stubs
- Do NOT modify ported components from TASK-100/101/102 — integration only
- Preserve existing Shell.tsx behavior (float panes, layout rendering)
- Portal target: `.hhp-root`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-103-RESPONSE.md`

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
