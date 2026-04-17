# TASK-245: ra96it Sign-Up Flow Verified (W5 — 5.7)

## Objective
Verify the ra96it sign-up flow works end-to-end: new user creates account, gets JWT, is redirected to ShiftCenter with valid session.

## Context
Wave 5 Ship. ra96it is the auth service (standalone FastAPI at ra96it.com). The sign-up flow must work for new users to onboard. This is verification — if something is broken, fix it.

## Source Spec
`docs/specs/WAVE-5-SHIP.md` — Task 5.7

## Files to Read First
- `ra96it/` — Auth service directory
- `browser/src/shell/components/LoginPage.tsx` — Frontend login page
- `browser/src/services/auth/` — Auth service integration (if exists)
- `hivenode/auth/` — Backend auth verification

## Deliverables
- [ ] Trace the full sign-up flow and document each step:
  1. User visits ShiftCenter → sees LoginPage
  2. Clicks "Sign Up" → redirected to ra96it
  3. Creates account (username, email, password)
  4. Gets JWT token
  5. Redirected back to ShiftCenter with token
  6. ShiftCenter stores token and loads requested EGG
- [ ] Verify each step works (or identify what's broken)
- [ ] Fix any broken steps found during verification
- [ ] Add E2E test: sign-up flow redirects correctly (mock ra96it for CI)
- [ ] Run: `cd browser && npx vitest run`

## Priority
P1

## Model
haiku
