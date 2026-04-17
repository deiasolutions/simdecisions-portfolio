# SPEC-CODE-EGG-HEADLESS-MENUBAR: Code EGG Headless Primitives with Standard MenuBar

## Priority
P1

## Objective
Update the Code EGG (code.egg.md) so all primitives are headless and the shell provides a single standard menubar showing the app name ("ShiftCenter Code"), File/Edit/View/Help menus, and the logged-in username on the right side. The MenuBar component already supports appName prop and UserStatus display (implemented for Efemera). The Code EGG ui block currently uses old-format keys (hideMenuBar, hideStatusBar) that need updating to the standard format (menuBar, statusBar, etc.).

## Files to Read First
- browser/sets/code.egg.md
- browser/src/shell/components/MenuBar.tsx
- browser/src/shell/Shell.tsx
- browser/sets/efemera.egg.md

## Deliverables
1. Update code.egg.md ui block from old format (hideMenuBar/hideStatusBar) to standard format (menuBar: true, masterTitleBar: false, statusBar: false, shellTabBar: false)
2. Verify all panes already have chrome: false (they do) and add headless: true to text-pane if applicable
3. Ensure displayName "ShiftCenter Code" feeds into MenuBar appName prop (already wired in Shell.tsx)
4. Confirm UserStatus component in MenuBar shows logged-in user (already implemented)
5. No new component code needed — this is an EGG config update only

## Acceptance Criteria
- [ ] code.egg.md ui block uses menuBar: true (not hideMenuBar: false)
- [ ] code.egg.md ui block uses masterTitleBar: false (removes duplicate title bar)
- [ ] All panes have chrome: false
- [ ] MenuBar displays "ShiftCenter Code" as app name
- [ ] MenuBar shows File/Edit/View/Help menus
- [ ] MenuBar shows logged-in username with green dot on the right
- [ ] No per-pane chrome bars visible

## Response File
20260324-TASK-CODE-EGG-HEADLESS-RESPONSE.md
