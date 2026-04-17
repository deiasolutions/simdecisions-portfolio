# SPEC-MW-052-hide-pane-chrome: Hide pane chrome on workdesk content panes

## Priority
P0

## Depends On
None

## Model Assignment
haiku

## Objective

The workdesk set shows pane chrome (title bar with hamburger, maximize, close buttons) on the chat and queue panes. Fix this by adding `"chrome": false` to `workdesk-chat` and `workdesk-queue`. Also fix the terminal pane (`workdesk-engine`): it currently has no `chrome` or `seamless` setting, and still shows chrome. Add `"chrome": false` to it. The terminal needs its chrome hidden but must NOT be seamless because `seamless: true` has a second effect — it excludes the pane from mobile navigation (ImmersiveNavigator and MobileNav filter out seamless panes). Content panes that should appear in mobile nav must use `chrome: false`, not `seamless: true`. Only true chrome panes (top-bar, menu-bar, status-bar) should be seamless.

## Files to Read First

- browser/sets/workdesk.set.md
- browser/src/shell/components/PaneChrome.tsx

## Acceptance Criteria

- [ ] `workdesk-chat` pane has `"chrome": false`
- [ ] `workdesk-queue` pane has `"chrome": false`
- [ ] `workdesk-engine` (terminal) pane has `"chrome": false` and does NOT have `"seamless": true`
- [ ] Chrome panes (chrome-top, chrome-menu, chrome-status) still have `"seamless": true` (unchanged)
- [ ] Loading `?set=workdesk` on desktop shows NO pane title bars on any content pane
- [ ] The set file remains valid JSON inside the layout code fence

## Smoke Test

- [ ] Open `http://localhost:5173/?set=workdesk` — verify no pane chrome bars are visible on any pane

## Constraints

- Only modify browser/sets/workdesk.set.md
- No git operations
- Add `"chrome": false` to workdesk-chat and workdesk-queue
- On workdesk-engine: add `"chrome": false` (it currently has neither chrome nor seamless set)
- Do not change any other properties on any pane
