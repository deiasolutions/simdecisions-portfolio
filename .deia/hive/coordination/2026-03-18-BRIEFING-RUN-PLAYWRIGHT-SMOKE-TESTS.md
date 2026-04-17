# BRIEFING: Run Playwright Smoke Tests + Report

**Date:** 2026-03-18
**From:** Q33NR
**To:** Q33N
**Priority:** P1

## Objective

Run all 3 Playwright e2e smoke tests against the live dev server (already running on localhost:5173) and report what they cover and whether they pass.

## What Q33N Must Do

1. **Read the test files first** to understand what each smoke test covers:
   - `browser/e2e/chat-smoke.spec.ts`
   - `browser/e2e/sim-smoke.spec.ts`
   - `browser/e2e/deploy-smoke.spec.ts`

2. **Run the Playwright suite:**
   ```
   cd browser && npx playwright test
   ```
   Vite is already running on 5173. Config at `browser/playwright.config.ts` has `reuseExistingServer: true`.

3. **Report back to Q33NR with:**
   - What each test covers (1-line summary per spec)
   - Pass/fail results
   - Any failures: full error output
   - Recommendations: are these tests useful? Do they cover the right things? What's missing?

## Constraints

- Do NOT modify any code or test files. Run only.
- Do NOT dispatch bees. This is investigation + execution.
- Report back to Q33NR with findings.
