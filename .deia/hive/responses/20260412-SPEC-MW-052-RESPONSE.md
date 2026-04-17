# SPEC-MW-052: Hide pane chrome on workdesk content panes -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku
**Date:** 2026-04-12

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\eggs\workdesk.set.md`

## What Was Done

- Added `"chrome": false` to the `workdesk-chat` pane (text-pane, line 59)
- Added `"chrome": false` to the `workdesk-engine` pane (terminal, line 71)
- Added `"chrome": false` to the `workdesk-queue` pane (tree-browser, line 94)
- Chrome primitives (`chrome-top`, `chrome-menu`, `chrome-status`) remain unchanged with `"seamless": true`
- Validated JSON structure remains valid after modifications
- All three content panes now correctly configured to hide chrome without being marked seamless

## Blockers Encountered

None.

## Tests Run

- JSON validation: passed (layout JSON parses correctly)
- Chrome property verification: passed (all three content panes have `chrome: false`)
- Chrome primitives verification: passed (all three chrome panes still have `seamless: true`)

## Smoke Test Status

Ready for manual smoke test:
- [ ] Open `http://localhost:5173/?set=workdesk` and verify no pane chrome bars are visible on any content pane

## Notes

Per the spec, `chrome: false` was chosen over `seamless: true` for content panes because:
- `seamless: true` excludes panes from mobile navigation (ImmersiveNavigator and MobileNav filter them out)
- Content panes (chat, queue, terminal) need to appear in mobile nav
- `chrome: false` hides chrome without the mobile navigation side effect
- Only true chrome primitives (top-bar, menu-bar, status-bar) should use `seamless: true`

The workdesk-engine terminal pane previously had no chrome or seamless setting, and now correctly has `chrome: false`.

## Cost

Estimated: $0.02 USD (based on Haiku pricing and task complexity)
