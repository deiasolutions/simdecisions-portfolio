# SPEC-MW-050: Workdesk Mobile Navigation Rationalization

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Objective

Fix broken mobile navigation in the workdesk egg. The factory build produced 3 duplicate MobileNav implementations — Shell.tsx imports the broken one (hub nav with dead buttons). The working one (auto-discovers panes, dispatches SET_FOCUS) is not wired in. Additionally, the terminal pane has seamless:true which hides it from mobile navigation, and 3 primitives lack app adapter registrations.

## Acceptance Criteria

- [ ] Shell.tsx imports MobileNav from ./MobileNav (shell/components/) not from primitives/mobile-nav/
- [ ] workdesk.set.md terminal pane (workdesk-engine) does NOT have seamless:true
- [ ] primitives/mobile-nav/ directory is deleted (MobileNav.tsx, mobile-nav.css, __tests__/)
- [ ] shell/components/MobileNavHub.tsx is deleted along with its test and CSS
- [ ] apps/index.ts registers conversation-pane adapter
- [ ] apps/index.ts registers diff-viewer adapter
- [ ] apps/index.ts registers voice-overlay adapter
- [ ] Each new adapter follows the same thin-wrapper pattern as QueuePaneAdapter
- [ ] No remaining imports reference deleted files (grep confirms zero hits)
- [ ] npx tsc --noEmit passes with zero new errors

## Smoke Test

- [ ] Load /?set=workdesk in Chrome DevTools mobile emulation (width 375px) — bottom nav shows tab buttons for each content pane
- [ ] Tap each tab — the corresponding pane renders (Conversation, Command, Queue)

## Files to Read First

browser/src/shell/components/Shell.tsx
browser/src/shell/components/MobileNav.tsx
browser/src/primitives/mobile-nav/MobileNav.tsx
browser/src/shell/components/MobileNavHub.tsx
browser/src/shell/components/ImmersiveNavigator.tsx
browser/src/apps/index.ts
browser/src/apps/queuePaneAdapter.tsx
browser/sets/workdesk.set.md

## Constraints

- Do NOT modify ImmersiveNavigator.tsx — it works correctly
- Do NOT modify shell/components/MobileNav.tsx — it is the correct implementation, just wire it in
- Do NOT modify ShellBusSubscriber.tsx — SET_FOCUS is already whitelisted
- Each new adapter file must be under 30 lines
- No file over 500 lines
- No stubs — every function complete
- No git operations
