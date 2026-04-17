# SPEC-MW-055-chrome-dedup: Remove duplicate user status from menu bar and currencies from top bar

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

On the workdesk set, user identity (name + initials/avatar) appears in BOTH the top-bar and the menu bar. It should only appear in the top-bar. Remove the user status display from MenuBarPrimitive entirely. Note: simdecisions's MenuBarPrimitive.tsx has a `UserStatus()` function at the bottom that displays the logged-in user and a logout button — this should be removed from the menu bar.

Also, the three currencies indicator (clock, coin, carbon) appears in both the top-bar and the bottom status bar. Currencies belong ONLY in the status bar (bottom chrome) where they are explicitly configured in the set file. Remove any currency/balance display from the TopBar component. The TopBar should show: app name, hamburger, avatar, kebab — nothing else.

## Files to Read First

- browser/src/primitives/top-bar/TopBar.tsx
- browser/src/primitives/menu-bar/MenuBarPrimitive.tsx
- browser/src/primitives/status-bar/StatusBar.tsx
- browser/sets/workdesk.set.md

## Acceptance Criteria

- [ ] MenuBarPrimitive does NOT render any user status, name, avatar, or initials
- [ ] The `UserStatus` component (or equivalent) is removed from MenuBarPrimitive.tsx
- [ ] TopBar does NOT render currency/balance indicators (clock, coin, carbon)
- [ ] StatusBar (bottom chrome) still renders the three currencies correctly
- [ ] TopBar still renders: app name, hamburger menu button, user avatar, kebab menu
- [ ] No TypeScript compilation errors (`npx tsc --noEmit` passes)

## Smoke Test

- [ ] Open `http://localhost:5173/?set=workdesk` — verify user identity appears ONLY in top-bar avatar, NOT in menu bar
- [ ] Verify currency indicators appear ONLY in the bottom status bar, NOT in the top-bar

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Use var(--sd-*) CSS variables only
- Do not remove the UserStatus component file if it exists separately — just remove its usage from MenuBarPrimitive
- Do not modify the status bar — it is working correctly
