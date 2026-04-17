# BRIEFING: Automated Smoke Test Suite for Deployed URLs

**From:** Q33NR (REGENT-QUEUE-TEMP-2026-03-16-3007-SPE)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-16
**Priority:** P1
**Model Assignment:** Sonnet

---

## Objective

Create a Playwright test suite that verifies the deployed app works after every push to dev.shiftcenter.com. This suite runs as part of the build queue's deploy verification step.

---

## Context

### What Exists
- `browser/playwright.config.ts` — current config points to localhost:5173
- `browser/e2e/chat-smoke.spec.ts` — 5 smoke tests for chat.egg.md
- `browser/e2e/sim-smoke.spec.ts` — 3 smoke tests for sim.egg.md

### What's Missing
- Separate config for deployed URLs (dev.shiftcenter.com)
- Tests for canvas.egg.md (5-pane layout)
- Tests for monitor.egg.md (build monitor EGG)
- Performance test (page load < 3 seconds)
- Screenshot capture per test
- No console errors check

### Dependencies
This spec depends on:
- `w3-01-vercel-railway-repoint` — Vercel points to dev.shiftcenter.com
- `w3-02-dev-shiftcenter-dns` — DNS resolves dev.shiftcenter.com

Those specs may or may not be complete. Check `.deia/hive/queue/_done/` to verify. If not done, note the dependency in the task file.

---

## Acceptance Criteria

The Q33N must produce task(s) that deliver:

1. **Playwright config for deployed URLs**
   - New config file: `browser/playwright.deploy.config.ts`
   - `baseURL` configurable via `DEPLOY_URL` env var (defaults to `https://dev.shiftcenter.com`)
   - No `webServer` block (we don't start vite for smoke tests)
   - Screenshots saved to `.deia/hive/smoke/` on failure AND success

2. **Test: Homepage loads**
   - Navigate to base URL
   - Assert `#root` div exists and is visible
   - Assert page title is "ShiftCenter"

3. **Test: API /health returns 200**
   - Fetch `/health` endpoint
   - Assert 200 status
   - Assert response contains `"status": "healthy"`

4. **Test: chat.egg.md renders 3 panes**
   - Navigate to `/?egg=chat`
   - Assert `.hhp-root` visible
   - Assert 3 panes visible: `.tree-browser`, `.text-pane`, `.terminal-pane`

5. **Test: canvas.egg.md renders 5 panes**
   - Navigate to `/?egg=canvas`
   - Assert `.hhp-root` visible
   - Assert 5 panes visible (check for pane IDs or classes from canvas.egg.md)

6. **Test: monitor.egg.md renders build monitor**
   - Navigate to `/?egg=monitor`
   - Assert `.hhp-root` visible
   - Assert build monitor specific element (check `eggs/build-monitor.egg.md` for pane IDs)

7. **Test: Terminal input/response flow**
   - Navigate to `/?egg=chat`
   - Type message in terminal input
   - Press Enter
   - Assert message appears in text-pane (or terminal output)

8. **Test: Page load time < 3 seconds**
   - Navigate to base URL
   - Measure time from navigation start to `#root` visible
   - Assert < 3000ms

9. **Test: No console errors**
   - Navigate to base URL
   - Listen for console errors (filter out React DevTools warning)
   - Assert no errors after 1 second

10. **Screenshot capture**
    - Every test saves screenshot to `.deia/hive/smoke/<test-name>-<timestamp>.png`
    - Use Playwright's `page.screenshot()` in afterEach hook

11. **8+ tests total**
    - Count includes all tests across all spec files
    - Each test is atomic and independent

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\playwright.config.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\e2e\chat-smoke.spec.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\e2e\sim-smoke.spec.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\build-monitor.egg.md` (to identify build monitor pane IDs)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md` (to identify canvas pane IDs)

---

## Constraints

- **Rule 3:** No hardcoded colors. (Not applicable — Playwright tests don't use CSS.)
- **Rule 4:** No file over 500 lines.
- **Rule 5:** TDD. Tests are the implementation — no separate "tests for tests."
- **Rule 6:** No stubs. Every test must fully execute and assert.

---

## Smoke Test Verification

After implementation, the bee must:

1. **Run against localhost (local verification):**
   ```bash
   cd browser
   DEPLOY_URL=http://localhost:5173 npx playwright test --config=playwright.deploy.config.ts
   ```
   All tests pass.

2. **Run against dev.shiftcenter.com (if DNS is live):**
   ```bash
   cd browser
   DEPLOY_URL=https://dev.shiftcenter.com npx playwright test --config=playwright.deploy.config.ts
   ```
   All tests pass (or report failures if deployment is broken).

3. **Verify screenshots saved:**
   Check `.deia/hive/smoke/` directory contains PNG files.

---

## Expected Task Structure

Q33N should break this into 1-2 tasks:

- **TASK-192:** Playwright deploy config + 8 smoke tests for deployed URLs
  - Deliverables:
    - `browser/playwright.deploy.config.ts`
    - `browser/e2e/deploy-smoke.spec.ts` (or split into multiple spec files)
    - `.deia/hive/smoke/.gitkeep` (create directory)
  - Test requirements:
    - 8+ tests (see acceptance criteria)
    - All tests pass against localhost:5173
    - Screenshots saved per test
  - Model: Sonnet (complex test logic)

OR split into:

- **TASK-192:** Playwright deploy config + core smoke tests (homepage, /health, chat, performance)
- **TASK-193:** Canvas + monitor + terminal flow tests

Q33N decides based on file size and complexity.

---

## Notes

- The existing `browser/e2e/chat-smoke.spec.ts` is for localhost development. The new suite is for deployed URLs (CI/CD verification).
- The bee should reuse patterns from existing smoke tests (error filtering, timeout handling).
- The bee should NOT start vite server in the config — we test the deployed URL directly.
- The bee should use `page.waitForSelector()` with generous timeouts (10-15 seconds) to handle slow network.
- The bee should handle the case where `dev.shiftcenter.com` is not yet live (DNS dependency). The task should note: "If DNS is not live, tests will fail — expected."

---

## Q33N: Your Next Steps

1. Read the files listed above.
2. Read `eggs/build-monitor.egg.md` and `eggs/canvas.egg.md` to identify pane IDs for assertions.
3. Write task file(s) to `.deia/hive/tasks/`.
4. Return to Q33NR for review.
5. Do NOT dispatch bees until Q33NR approves.

---

**End of Briefing**
