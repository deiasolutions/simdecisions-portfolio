# BUG-017: OAuth redirect to ra96it.com shows LandingPage instead of logged-in state

## Objective
Fix OAuth redirect so after authenticating at ra96it.com, the user returns to ShiftCenter in a logged-in state instead of seeing the LandingPage again.

## Context
After OAuth flow completes and redirects back to ShiftCenter, the app shows the LandingPage instead of recognizing the JWT token in the URL/storage and proceeding to the authenticated state. The token extraction or auth state persistence is broken.

## Files to Read First
- `browser/src/App.tsx`
- `browser/src/pages/LandingPage.tsx`
- `browser/src/services/`
- `ra96it/`

## Deliverables
- [ ] Trace OAuth redirect flow from ra96it back to ShiftCenter
- [ ] Fix token extraction from redirect URL (hash fragment or query param)
- [ ] Fix auth state persistence (localStorage or session)
- [ ] App.tsx should detect auth state and skip LandingPage
- [ ] Tests for redirect token handling

## Acceptance Criteria
- [ ] After OAuth redirect, user sees authenticated app (not LandingPage)
- [ ] JWT token stored correctly
- [ ] Refreshing page maintains auth state
- [ ] Tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/pages/`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment
haiku

## Priority
P0
