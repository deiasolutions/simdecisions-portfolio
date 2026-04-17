# BUG-017: OAuth Redirect Shows LandingPage Instead of Logged-In State (P0)

## Objective
Fix `shouldShowLanding()` in `App.tsx` so that ra96it.com OAuth redirects (and ra96it.com visits in general) load the `login` EGG instead of the ShiftCenter LandingPage marketing page.

## Context
The entire ra96it.com auth flow is visually broken. GitHub OAuth completes successfully — the token IS saved to localStorage — but the user sees the ShiftCenter marketing page instead of the LoginPage's "You are logged in" state. This is a P0 blocker for the auth flow.

Root cause: `shouldShowLanding()` in `App.tsx` (lines 58-63) short-circuits the EGG system for any root-path visit without `?egg=` param. After `extractTokenFromUrl()` strips the token from the URL, `shouldShowLanding()` returns true and renders the static `LandingPage` component.

## Source Briefing
`.deia/hive/coordination/2026-03-17-BRIEFING-BUG-017-OAUTH-REDIRECT-LANDING.md`

## Files to Read First
- `browser/src/App.tsx` — the bug lives here (lines 25-68)
- `browser/src/primitives/auth/authStore.ts` — `isAuthenticated()` function
- `browser/src/eggs/eggResolver.ts` — hostname → EGG mapping (lines 94-96)
- `browser/src/pages/LandingPage.tsx` — static page that incorrectly renders

## Deliverables
- [ ] Fix `shouldShowLanding()` to check hostname (ra96it domains → never show landing)
- [ ] Fix `shouldShowLanding()` to check `isAuthenticated()` (logged-in users → never show landing)
- [ ] Add `isAuthenticated` to the import line in App.tsx
- [ ] 6+ tests covering the new shouldShowLanding logic
- [ ] All existing App/Shell tests still pass

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - ra96it.com hostname → returns false
  - www.ra96it.com hostname → returns false
  - dev.ra96it.com hostname → returns false
  - Authenticated user on any hostname → returns false
  - Unauthenticated user on shiftcenter root with no ?egg= → returns true (preserved)
  - Any hostname with ?egg= param → returns false (preserved)

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- TDD

## Model
Haiku — small surgical fix, well-scoped

## Priority
P0 — blocks ra96it.com sign-in flow for all users
