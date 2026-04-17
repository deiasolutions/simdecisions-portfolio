# TASK-242: Full Smoke Test Suite Against Production (W5 — 5.3)

## Objective
Write a comprehensive smoke test suite that exercises critical user flows against production: page load, EGG loading, auth, chat send/receive, terminal submit.

## Context
Wave 5 Ship. Beyond URL checks (TASK-241), this tests actual functionality. Uses Playwright for browser tests and httpx for API tests. Runs against the deployed production environment.

## Depends On
- TASK-241 (production URLs must be verified first)

## Source Spec
`docs/specs/WAVE-5-SHIP.md` — Task 5.3

## Files to Read First
- `browser/e2e/deploy-smoke.spec.ts` — Existing deploy smoke test
- `browser/playwright.deploy.config.ts` — Deploy Playwright config
- `tests/hivenode/test_e2e.py` — Existing E2E test patterns

## Deliverables
- [ ] Create/update `browser/e2e/deploy-smoke.spec.ts`:
  - Test: landing page loads, shows ShiftCenter branding
  - Test: `?egg=chat` loads 3-pane layout
  - Test: `?egg=canvas` loads 5-pane layout
  - Test: `?egg=efemera` loads 4-pane layout
  - Test: unauthenticated user sees login prompt
  - Test: terminal renders and accepts input
  - Test: theme toggle works (if exposed)
  - Test: FAB menu opens on empty pane click
- [ ] Create API smoke tests in `tests/smoke/test_production_api.py`:
  - Test: `/health` returns 200
  - Test: `/api/shell/execute` rejects without auth (401)
  - Test: `/efemera/channels` rejects without auth (401)
- [ ] All tests must be skippable if production is unreachable
- [ ] Run instructions in file header

## Priority
P1

## Model
sonnet
