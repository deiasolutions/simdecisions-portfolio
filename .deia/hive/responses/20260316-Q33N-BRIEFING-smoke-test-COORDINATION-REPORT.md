# Q33N Coordination Report: Smoke Test Suite

**From:** Q33N (Queen Coordinator)
**To:** Q33NR (Queen Regent)
**Date:** 2026-03-16
**Re:** BRIEFING-smoke-test-suite

---

## Status: TASK FILE READY FOR REVIEW

I have read the briefing and created one task file for implementation.

## Task Files Created

### TASK-192: Automated Smoke Test Suite for Deployed URLs
**File:** `.deia/hive/tasks/2026-03-16-TASK-192-deploy-smoke-tests.md`
**Model:** Sonnet
**Complexity:** Medium

**Deliverables:**
1. `browser/playwright.deploy.config.ts` — separate config for deployed URLs
2. `browser/e2e/deploy-smoke.spec.ts` — 9 smoke tests
3. `.deia/hive/smoke/` directory + `.gitkeep`

**Tests (9 total):**
1. Homepage loads (#root visible, title = "ShiftCenter")
2. API /health returns 200 + `"status": "healthy"`
3. chat.egg.md renders 3 panes (tree-browser, text-pane, terminal)
4. canvas.egg.md renders 5 panes (palette, canvas, chat, ir, properties)
5. monitor.egg.md renders build monitor (tree-browsers visible)
6. Terminal input/response flow (echo test)
7. Page load time < 3 seconds
8. No console errors (filtered for React DevTools warning)
9. sim.egg.md renders shell (.hhp-root visible)

**Key Features:**
- `DEPLOY_URL` env var (defaults to `https://dev.shiftcenter.com`)
- No webServer block (tests deployed URL directly)
- Screenshots saved on EVERY test (success + failure) to `.deia/hive/smoke/`
- 15-second timeouts for slow network
- Console error filtering (ignore React DevTools)

**Verification Steps:**
```bash
# Local verification
cd browser
DEPLOY_URL=http://localhost:5173 npx playwright test --config=playwright.deploy.config.ts

# Deployed verification (when DNS is live)
cd browser
DEPLOY_URL=https://dev.shiftcenter.com npx playwright test --config=playwright.deploy.config.ts

# Check screenshots
ls -la .deia/hive/smoke/
```

**Dependencies:**
- `w3-01-vercel-railway-repoint` — ✅ COMPLETE (verified in `_done/`)
- `w3-02-dev-shiftcenter-dns` — ✅ COMPLETE (verified in `_done/`)

**Note:** If DNS is not yet live or deployment is incomplete, tests will fail with `ENOTFOUND` or timeout. This is expected. The bee is instructed to note this in the response file.

---

## Analysis

### Why One Task Instead of Two?

The briefing suggested potentially splitting into TASK-192 (core tests) + TASK-193 (canvas/monitor tests). I chose to keep it as one task because:

1. **Total line count:** ~350 lines for config + tests — well under 500-line limit
2. **Single test file:** All tests go in `deploy-smoke.spec.ts` — coherent unit of work
3. **Same model:** All tests are similar complexity (Sonnet appropriate)
4. **No dependencies:** Tests are independent and can be written in one pass

If the bee's implementation exceeds 400 lines in `deploy-smoke.spec.ts`, I can dispatch a follow-up task to split the file.

### Pane Counting Strategy

For Test 4 (canvas.egg.md), I specified counting `.hhp-pane` or `[data-node-id]` selectors to reach 5 panes. This is based on the EGG layout structure. If the shell uses different selectors, the bee will adjust after reading the actual rendered HTML.

For Test 5 (monitor.egg.md), I used a simpler assertion: "at least one tree-browser visible." The monitor has 4 tree-browsers, but asserting exact count is fragile (depends on data). The key is that the EGG loads without error.

### Console Error Filtering

Reused the pattern from `chat-smoke.spec.ts`: filter out "Download the React DevTools" warning. Any other console errors = fail. This is strict but correct for smoke tests.

### Screenshot Capture

Configured `screenshot: 'always'` in playwright.deploy.config.ts + `afterEach` hook in tests to save screenshots on every run. This ensures we have visual proof of deployment state even when tests pass.

---

## Constraints Compliance

- ✅ **Rule 3:** No hardcoded colors (tests don't use CSS)
- ✅ **Rule 4:** File < 500 lines (~350 lines total)
- ✅ **Rule 5:** TDD — tests ARE the implementation
- ✅ **Rule 6:** No stubs — every test fully executes
- ✅ **Rule 8:** All file paths absolute

---

## Next Steps

1. Q33NR reviews TASK-192
2. If approved, Q33NR instructs me to dispatch bee
3. I dispatch: `python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-16-TASK-192-deploy-smoke-tests.md --model sonnet --role bee --inject-boot --timeout 3600`
4. Bee implements, runs tests, writes response file
5. I read response file and report results to Q33NR

---

## Questions for Q33NR

None. Task file is complete and ready for review.

---

**End of Report**
