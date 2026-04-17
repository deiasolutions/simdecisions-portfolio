# BRIEFING: Deploy Smoke Test Suite

**From:** Q33NR (Regent)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-16
**Model Assignment:** Sonnet
**Priority:** P1 (part of W3 deployment wave)

---

## Objective

Create a Playwright test suite that verifies the deployed app at `dev.shiftcenter.com` works correctly. This suite runs as part of the build queue's deploy verification step.

---

## Context from Q88N

The existing `browser/playwright.config.ts` is for local development only (starts vite dev server at localhost:5173). We need a separate config for deployed URLs that:

- Does NOT start vite server (tests deployed URL directly)
- Accepts `DEPLOY_URL` env var (defaults to `https://dev.shiftcenter.com`)
- Saves screenshots on every test (success AND failure) to `.deia/hive/smoke/`
- Tests 4 EGG files: homepage, chat.egg.md, canvas.egg.md, monitor.egg.md
- Measures performance (page load < 3 seconds)
- Verifies no console errors

**Dependencies:**
- `w3-01-vercel-railway-repoint` — COMPLETE (see `.deia/hive/queue/_done/`)
- `w3-02-dev-shiftcenter-dns` — COMPLETE (see `.deia/hive/queue/_done/`)

**Important:** If DNS is not yet live, tests will fail with ENOTFOUND or timeout. This is expected. The bee should note this in the response file.

---

## Files to Reference

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\playwright.config.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\e2e\chat-smoke.spec.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\e2e\sim-smoke.spec.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\build-monitor.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md`

---

## Required Deliverables

### 1. Playwright Deploy Config
- File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\playwright.deploy.config.ts`
- `baseURL` configurable via `DEPLOY_URL` env var (default: `https://dev.shiftcenter.com`)
- NO `webServer` block (we test deployed URL, not localhost)
- `screenshot: 'always'` (save on success AND failure)
- `outputDir: '../.deia/hive/smoke/'` for screenshots
- `timeout: 15000` (generous timeout for slow network)
- `retries: 0` (no retries in smoke tests)
- `workers: 1` (sequential tests)

### 2. Smoke Test File
- File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\e2e\deploy-smoke.spec.ts`
- 9+ tests (see detailed test requirements in original spec)
- Each test saves screenshot in afterEach hook to `.deia/hive/smoke/<test-name>-<timestamp>.png`
- Console error filtering (ignore React DevTools warning)
- Generous timeouts (10-15 seconds for element visibility)

### 3. Smoke Directory
- Directory: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\smoke\` (create if not exists)
- `.gitkeep` file in directory

---

## Test Requirements (9 tests minimum)

1. **Homepage loads** — verify #root visible, page title
2. **API /health returns 200** — verify endpoint health
3. **chat.egg.md renders 3 panes** — verify tree-browser, text-pane, terminal-pane
4. **canvas.egg.md renders 5 panes** — verify all 5 panes from canvas layout
5. **monitor.egg.md renders build monitor** — verify at least one tree-browser
6. **Terminal input/response flow** — verify terminal accepts input and echoes
7. **Page load time < 3 seconds** — performance test
8. **No console errors** — verify clean console (filter DevTools warning)
9. **sim.egg.md renders shell** — verify .hhp-root visible

---

## Test Implementation Patterns

**Screenshot saving (afterEach hook):**
```typescript
test.afterEach(async ({ page }, testInfo) => {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
  const filename = `${testInfo.title.replace(/\s+/g, '-')}-${timestamp}.png`
  const screenshotPath = path.join(__dirname, '../../.deia/hive/smoke', filename)
  await page.screenshot({ path: screenshotPath, fullPage: true })
})
```

**Console error filtering:**
```typescript
const errors: string[] = []
page.on('console', (msg) => {
  if (msg.type() === 'error') {
    const text = msg.text()
    if (!text.includes('Download the React DevTools')) {
      errors.push(text)
    }
  }
})
```

---

## Constraints

- **Rule 4:** No file over 500 lines. If tests exceed 500 lines, split into multiple spec files.
- **Rule 5:** TDD. Tests are the implementation. No separate "tests for tests."
- **Rule 6:** No stubs. Every test must fully execute and assert.
- **Rule 10:** No git operations without Q88N approval.

---

## Verification Steps

After implementation:

1. **Test against localhost (verify tests work):**
   ```bash
   cd browser
   DEPLOY_URL=http://localhost:5173 npx playwright test --config=playwright.deploy.config.ts
   ```

2. **Test against dev.shiftcenter.com (if DNS is live):**
   ```bash
   cd browser
   DEPLOY_URL=https://dev.shiftcenter.com npx playwright test --config=playwright.deploy.config.ts
   ```

3. **Verify screenshots saved:**
   ```bash
   ls -la .deia/hive/smoke/
   ```

4. **Check no hardcoded URLs:**
   All URLs must use `baseURL` variable or `process.env.DEPLOY_URL`.

---

## Notes

- If DNS is not yet live, tests will fail with `ENOTFOUND` or `net::ERR_NAME_NOT_RESOLVED`. This is expected.
- If Vercel deployment is not yet pointing to Railway hivenode, `/health` test may fail with 404 or 502.
- The bee should handle slow network gracefully (15-second timeouts).
- The bee should NOT mock API calls in this suite. These are real smoke tests against deployed URLs.

---

## Response Requirements

The bee MUST write a response file with all 8 sections:
1. Header (task ID, title, status, model, date)
2. Files Modified (every file, absolute paths)
3. What Was Done (bullet list of concrete changes)
4. Test Results (test files run, pass/fail counts)
5. Build Verification (test/build output summary)
6. Acceptance Criteria (copy from task, mark [x] or [ ])
7. Clock / Cost / Carbon (all three, never omit any)
8. Issues / Follow-ups (edge cases, dependencies, next tasks)

---

## Q33N — Your Task

1. **Read the files** listed in "Files to Reference" section
2. **Write a task file** to `.deia/hive/tasks/` with:
   - All deliverables clearly specified
   - All 9 test scenarios detailed
   - Absolute file paths
   - Test requirements (TDD, all tests pass)
   - Response file requirements
3. **Return task file to me (Q33NR) for review**
4. **Do NOT dispatch bees yet** — wait for my approval

---

**End of Briefing**
