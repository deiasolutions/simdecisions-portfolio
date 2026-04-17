# QUEUE-TEMP-SPEC-MW-050-workdesk-rationalization -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-12

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\packages\browser\src\shell\components\Shell.tsx` — Fixed MobileNav import to use `./MobileNav` instead of `../../primitives/mobile-nav/MobileNav`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\eggs\workdesk.set.md` — Removed `seamless: true` from terminal pane config
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\packages\browser\src\apps\conversationPaneAdapter.tsx` — Created new adapter
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\packages\browser\src\apps\diffViewerAdapter.tsx` — Created new adapter
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\packages\browser\src\apps\voiceOverlayAdapter.tsx` — Created new adapter
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\packages\browser\src\apps\index.ts` — Added imports and registrations for three new adapters
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\packages\browser\src\__tests__\rtd-bus-integration.test.tsx` — Updated MobileNav import to use correct path
- Deleted: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\packages\browser\src\primitives\mobile-nav\` directory (MobileNav.tsx, mobile-nav.css, __tests__/MobileNav.test.tsx)
- Deleted: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\packages\browser\src\shell\components\MobileNavHub.tsx`
- Deleted: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\packages\browser\src\shell\components\__tests__\MobileNavHub.test.tsx`
- Deleted: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\packages\browser\src\shell\components\mobile-nav-hub.css`

## What Was Done

- Changed Shell.tsx line 19 to import MobileNav from `./MobileNav` (shell/components/) instead of `../../primitives/mobile-nav/MobileNav`
- Removed `"seamless": true` property from workdesk-engine terminal pane in workdesk.set.md (was line 70)
- Created conversationPaneAdapter.tsx (14 lines) — thin wrapper for ConversationPane primitive with proper type guards
- Created diffViewerAdapter.tsx (29 lines) — thin wrapper for DiffViewer primitive with proper type guards
- Created voiceOverlayAdapter.tsx (20 lines) — thin wrapper for VoiceOverlay primitive with proper type guards
- Added imports for three new adapters in apps/index.ts
- Registered conversation-pane, diff-viewer, and voice-overlay apps in registerApps() function
- Deleted entire primitives/mobile-nav/ directory (3 files)
- Deleted MobileNavHub.tsx and related test and CSS files (3 files)
- Fixed rtd-bus-integration.test.tsx to import MobileNav from correct location
- Verified no remaining imports reference deleted files using grep
- Ran `npx tsc --noEmit` — zero NEW errors (pre-existing test errors unrelated to this task remain)

## Acceptance Criteria Status

- [x] Shell.tsx imports MobileNav from ./MobileNav (shell/components/) not from primitives/mobile-nav/
- [x] workdesk.set.md terminal pane (workdesk-engine) does NOT have seamless:true
- [x] primitives/mobile-nav/ directory is deleted (MobileNav.tsx, mobile-nav.css, __tests__/)
- [x] shell/components/MobileNavHub.tsx is deleted along with its test and CSS
- [x] apps/index.ts registers conversation-pane adapter
- [x] apps/index.ts registers diff-viewer adapter
- [x] apps/index.ts registers voice-overlay adapter
- [x] Each new adapter follows the same thin-wrapper pattern as QueuePaneAdapter
- [x] No remaining imports reference deleted files (grep confirms zero hits)
- [x] npx tsc --noEmit passes with zero new errors

## Tests Run

- TypeScript compilation check passed (no new errors introduced)
- Grep verification passed (no orphaned imports)

## Notes

All three new adapters follow the QueuePaneAdapter pattern: thin wrapper files (under 30 lines each) that map AppRendererProps to the primitive component's props. Proper type guards ensure config properties are validated before passing to primitives.

The terminal pane will now appear in mobile navigation since seamless:true was removed, allowing users to access it via the bottom nav bar on mobile viewports.

Pre-existing TypeScript errors in test files (byok-flow, smoke.test, authAdapter.test, etc.) are unrelated to this task and were not introduced by these changes.
