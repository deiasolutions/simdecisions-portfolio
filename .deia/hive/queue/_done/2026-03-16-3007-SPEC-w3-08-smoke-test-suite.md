# SPEC: Automated Smoke Test Suite for Deployed URLs

## Priority
P1

## Objective
Playwright test suite that verifies the deployed app works after every push. Runs as part of the build queue's deploy verification step.

## Context
Files to read first:
- `browser/playwright.config.ts` (if exists)
- `tests/e2e/` (existing Playwright tests from TASK-015)

## Acceptance Criteria
- [ ] Playwright config points to dev.shiftcenter.com (configurable via env var)
- [ ] Test: homepage loads, contains #root div
- [ ] Test: API /health returns 200
- [ ] Test: chat.egg.md renders 3 panes (tree-browser, text-pane, terminal)
- [ ] Test: canvas.egg.md renders 5 panes (via ?egg=canvas)
- [ ] Test: monitor.egg.md renders build monitor (via ?egg=monitor)
- [ ] Test: type message in terminal -> response appears in text-pane
- [ ] Test: page load time < 3 seconds
- [ ] Test: no console errors
- [ ] Screenshot saved per test to .deia/hive/smoke/
- [ ] 8+ tests total

## Smoke Test
- [ ] Run: npx playwright test --config=tests/e2e/playwright.config.ts
- [ ] All tests pass against dev.shiftcenter.com (or localhost:5173 for local verification)

## Depends On
- w3-01-vercel-railway-repoint
- w3-02-dev-shiftcenter-dns

## Model Assignment
sonnet
