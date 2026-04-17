# SPEC-CHAT-EGG-HEADLESS-MENUBAR: Chat EGG Headless Primitives with Standard MenuBar

## Priority
P1

## Objective
Update the Chat EGG (chat.egg.md) so all primitives are headless and the shell provides a single standard menubar showing the app name ("Chat"), File/Edit/View/Help menus, and the logged-in username on the right side. Currently the Chat EGG panes are missing chrome: false, and the ui block has masterTitleBar: true which shows a redundant title bar above the menubar.

## Files to Read First
- browser/sets/chat.egg.md
- browser/src/shell/components/MenuBar.tsx
- browser/src/shell/Shell.tsx
- browser/sets/efemera.egg.md

## Deliverables
1. Add chrome: false to all three panes in chat.egg.md (chat-sidebar, chat-output, chat-main)
2. Add headless: true to chat-output (text-pane showing messages)
3. Update ui block: set masterTitleBar: false to remove duplicate title bar
4. Verify menuBar: true is already set (it is)
5. Ensure displayName "Chat" feeds into MenuBar appName prop
6. No new component code needed — this is an EGG config update only

## Acceptance Criteria
- [ ] All three chat.egg.md panes have chrome: false
- [ ] chat-output pane has headless: true
- [ ] masterTitleBar is false (no duplicate title bar)
- [ ] menuBar remains true
- [ ] MenuBar displays "Chat" as app name
- [ ] MenuBar shows File/Edit/View/Help menus
- [ ] MenuBar shows logged-in username with green dot on the right
- [ ] No per-pane chrome bars visible

## Response File
20260324-TASK-CHAT-EGG-HEADLESS-RESPONSE.md
