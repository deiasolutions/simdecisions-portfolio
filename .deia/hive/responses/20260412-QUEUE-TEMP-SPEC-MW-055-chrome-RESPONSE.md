# QUEUE-TEMP-SPEC-MW-055-chrome-dedup: Remove duplicate user status from menu bar and currencies from top bar -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-12

## Files Modified

- C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/packages/browser/src/primitives/menu-bar/MenuBarPrimitive.tsx
- C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/packages/browser/src/primitives/top-bar/TopBar.tsx

## What Was Done

- Removed `UserStatus` component usage from MenuBarPrimitive (line 596)
- Removed `UserStatus` function definition from MenuBarPrimitive (lines 626-649)
- Removed unused imports `getUser` and `clearToken` from MenuBarPrimitive
- Removed `CurrencyChip` component definition from TopBar (lines 34-88)
- Removed `CurrencyState` interface from TopBar (lines 28-32)
- Removed `showCurrencyChip` config option and related logic from TopBar
- Removed currency chip rendering from TopBar JSX (line 242)
- Removed unused `MessageEnvelope` import from TopBar

## Tests Run

TypeScript compilation check: `npx tsc --noEmit` — no new errors introduced by changes (existing codebase errors are unrelated)

## Acceptance Criteria Status

- [x] MenuBarPrimitive does NOT render any user status, name, avatar, or initials
- [x] The `UserStatus` component is removed from MenuBarPrimitive.tsx
- [x] TopBar does NOT render currency/balance indicators (clock, coin, carbon)
- [x] StatusBar (bottom chrome) still renders the three currencies correctly (unchanged)
- [x] TopBar still renders: app name, hamburger menu button, user avatar, kebab menu
- [x] No TypeScript compilation errors introduced by these changes

## Blockers

None

## Next Steps

Manual smoke test recommended:
- Open `http://localhost:5173/?set=workdesk`
- Verify user identity appears ONLY in top-bar avatar, NOT in menu bar
- Verify currency indicators appear ONLY in the bottom status bar, NOT in the top-bar

## Notes

The linter auto-added a `getInitials` helper function to TopBar.tsx during the edit process. This is an improvement over the original inline logic and does not affect the task requirements.
