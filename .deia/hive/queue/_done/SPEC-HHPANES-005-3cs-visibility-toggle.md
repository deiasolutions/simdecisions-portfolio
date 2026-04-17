# SPEC-HHPANES-005: Three Currencies Visibility Toggle

## Priority
P2

## Depends On
HHPANES-001

## Model Assignment
haiku

## Objective

Make the Three Currencies display (CLOCK, COIN, CARBON) configurable instead of hardcoded in the top menu. Users should be able to choose where 3Cs are displayed or hide them entirely. Data collection continues regardless of visibility.

## Files to Read First

- browser/src/primitives/top-bar/TopBar.tsx
- browser/src/primitives/settings/settingsStore.ts
- browser/src/primitives/settings/types.ts

## Acceptance Criteria

- [ ] 3Cs visibility controlled by user setting
- [ ] Setting options: top-menu, dashboard-widget, hidden
- [ ] Default: top-menu (current behavior preserved)
- [ ] When hidden, 3Cs do not render anywhere
- [ ] Setting change takes effect immediately (no reload)
- [ ] 3Cs data still collected regardless of visibility (display-only toggle)
- [ ] All existing TopBar tests still pass
- [ ] New tests cover each visibility mode

## Smoke Test

- [ ] Load app — confirm 3Cs in top menu (default)
- [ ] Change setting to hidden — confirm 3Cs disappear immediately
- [ ] Confirm RTD events still emitting for 3Cs data collection

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Use var(--sd-*) CSS variables only
- Setting persists via HHPANES-003 once backend persistence is live
