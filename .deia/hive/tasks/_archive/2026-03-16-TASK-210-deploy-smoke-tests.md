# TASK-210: Automated Smoke Test Suite for Deployed URLs

## Objective

Create a Playwright test suite (`playwright.deploy.config.ts` + smoke tests) that verifies the deployed app at `dev.shiftcenter.com` works correctly. This suite runs as part of the build queue's deploy verification step.

## Context

The existing `browser/playwright.config.ts` is for local development only (starts vite dev server at localhost:5173). This task creates a separate config for deployed URLs that:

- Does NOT start vite server (tests deployed URL directly)
- Accepts `DEPLOY_URL` env var (defaults to `https://dev.shiftcenter.com`)
- Saves screenshots on every test (success AND failure) to `.deia/hive/smoke/`
- Tests 4 EGG files: homepage, chat.egg.md, canvas.egg.md, monitor.egg.md
- Measures performance (page load < 3 seconds)
- Verifies no console errors

Dependencies:
- `w3-01-vercel-railway-repoint` — COMPLETE (see `.deia/hive/queue/_done/`)
- `w3-02-dev-shiftcenter-dns` — COMPLETE (see `.deia/hive/queue/_done/`)

If DNS is not yet live, tests will fail with ENOTFOUND or timeout. This is expected. The bee should note this in the response file.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\playwright.config.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\e2e\chat-smoke.spec.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\e2e\sim-smoke.spec.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\build-monitor.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md`

## Deliverables

### 1. Playwright Deploy Config
- [ ] File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\playwright.deploy.config.ts`
- [ ] `baseURL` configurable via `DEPLOY_URL` env var (default: `https://dev.shiftcenter.com`)
- [ ] NO `webServer` block (we test deployed URL, not localhost)
- [ ] `screenshot: 'always'` (save on success AND failure)
- [ ] `outputDir: '../.deia/hive/smoke/'` for screenshots
- [ ] `timeout: 15000` (generous timeout for slow network)
- [ ] `retries: 0` (no retries in smoke tests)
- [ ] `workers: 1` (sequential tests)
- [ ] `reporter: [['list'], ['html', { outputFolder: 'playwright-report-deploy' }]]`
- [ ] Use same project config as existing playwright.config.ts (chromium only)

### 2. Smoke Test File
- [ ] File: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\e2e\deploy-smoke.spec.ts`
- [ ] 9+ tests (see test requirements below)
- [ ] Each test saves screenshot in `afterEach` hook to `.deia/hive/smoke/<test-name>-<timestamp>.png`
- [ ] Console error filtering (ignore React DevTools warning like chat-smoke.spec.ts)
- [ ] Generous timeouts (10-15 seconds for element visibility)
- [ ] NO API mocking (these are real smoke tests against deployed URLs)
- [ ] Extract `baseURL` from `process.env.DEPLOY_URL` or default to `https://dev.shiftcenter.com`
- [ ] Import `path` module for screenshot paths

### 3. Smoke Directory
- [ ] Directory: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\smoke\` (create if not exists)
- [ ] `.gitkeep` file in directory

## Test Requirements

Write the following tests in `deploy-smoke.spec.ts`:

### Test 1: Homepage loads
```typescript
test('should load homepage and render root element', async ({ page }) => {
  await page.goto(baseURL)
  const root = page.locator('#root')
  await expect(root).toBeVisible({ timeout: 15000 })
  await expect(page).toHaveTitle('ShiftCenter')
})
```

### Test 2: API /health returns 200
```typescript
test('should return 200 from /health endpoint', async ({ page }) => {
  const resp = await page.request.get(`${baseURL}/health`)
  expect(resp.status()).toBe(200)
  const json = await resp.json()
  expect(json.status).toBe('healthy')
})
```

### Test 3: chat.egg.md renders 3 panes
```typescript
test('should render chat EGG with 3 panes', async ({ page }) => {
  await page.goto(`${baseURL}?egg=chat`)
  const shell = page.locator('.hhp-root')
  await expect(shell).toBeVisible({ timeout: 15000 })

  // Assert 3 panes visible
  const treeBrowser = page.locator('.tree-browser')
  const textPane = page.locator('.text-pane')
  const terminal = page.locator('.terminal-pane')

  await expect(treeBrowser).toBeVisible({ timeout: 10000 })
  await expect(textPane).toBeVisible({ timeout: 10000 })
  await expect(terminal).toBeVisible({ timeout: 10000 })
})
```

### Test 4: canvas.egg.md renders 5 panes
```typescript
test('should render canvas EGG with 5 panes', async ({ page }) => {
  await page.goto(`${baseURL}?egg=canvas`)
  const shell = page.locator('.hhp-root')
  await expect(shell).toBeVisible({ timeout: 15000 })

  // Canvas layout: palette, canvas-editor, text-pane, terminal, properties
  // Count visible panes (5 total)
  const panes = page.locator('.hhp-pane')
  await expect(panes).toHaveCount(5, { timeout: 15000 })
})
```

### Test 5: monitor.egg.md renders build monitor
```typescript
test('should render build-monitor EGG', async ({ page }) => {
  await page.goto(`${baseURL}?egg=build-monitor`)
  const shell = page.locator('.hhp-root')
  await expect(shell).toBeVisible({ timeout: 15000 })

  // Build monitor layout: build-service (data service), 4 tree-browsers
  // Look for build-data-service appType or status bar
  // Assert at least one tree-browser visible
  const treeBrowsers = page.locator('.tree-browser')
  await expect(treeBrowsers.first()).toBeVisible({ timeout: 10000 })
})
```

### Test 6: Terminal input/response flow
```typescript
test('should accept terminal input and echo message', async ({ page }) => {
  await page.goto(`${baseURL}?egg=chat`)
  await page.waitForSelector('.terminal-pane', { timeout: 15000 })

  const input = page.locator('.terminal-input')
  await expect(input).toBeVisible()

  await input.fill('hello deploy test')
  await input.press('Enter')

  await expect(input).toHaveValue('')

  await page.waitForTimeout(500)

  const terminalContent = await page.locator('.terminal-pane').textContent()
  expect(terminalContent).toContain('hello deploy test')
})
```

### Test 7: Page load time < 3 seconds
```typescript
test('should load homepage in under 3 seconds', async ({ page }) => {
  const startTime = Date.now()

  await page.goto(baseURL)
  const root = page.locator('#root')
  await expect(root).toBeVisible({ timeout: 15000 })

  const loadTime = Date.now() - startTime
  expect(loadTime).toBeLessThan(3000)
})
```

### Test 8: No console errors
```typescript
test('should have no console errors on homepage', async ({ page }) => {
  const errors: string[] = []
  page.on('console', (msg) => {
    if (msg.type() === 'error') {
      const text = msg.text()
      // Filter out React DevTools warning
      if (!text.includes('Download the React DevTools')) {
        errors.push(text)
      }
    }
  })

  await page.goto(baseURL)
  await page.waitForSelector('#root', { timeout: 15000 })

  // Wait 1 second to catch any delayed errors
  await page.waitForTimeout(1000)

  expect(errors).toHaveLength(0)
})
```

### Test 9: sim.egg.md renders shell
```typescript
test('should render sim EGG with hhp-root', async ({ page }) => {
  await page.goto(`${baseURL}?egg=sim`)
  const shell = page.locator('.hhp-root')
  await expect(shell).toBeVisible({ timeout: 15000 })
})
```

## Test Implementation Notes

1. **Use `afterEach` hook to save screenshots:**
   ```typescript
   test.afterEach(async ({ page }, testInfo) => {
     const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
     const filename = `${testInfo.title.replace(/\s+/g, '-')}-${timestamp}.png`
     const screenshotPath = path.join(__dirname, '../../.deia/hive/smoke', filename)
     await page.screenshot({ path: screenshotPath, fullPage: true })
   })
   ```

2. **Extract `baseURL` from config:**
   ```typescript
   import { test, expect } from '@playwright/test'
   import path from 'path'

   const baseURL = process.env.DEPLOY_URL || 'https://dev.shiftcenter.com'
   ```

3. **Console error filtering:**
   - Reuse pattern from `chat-smoke.spec.ts`
   - Filter out "Download the React DevTools" warning
   - Any other errors = fail

4. **Pane counting strategy:**
   - For canvas.egg.md: use `.hhp-pane` selector
   - Count 5 panes (palette, canvas, chat, ir, properties)
   - For build-monitor: look for `.tree-browser` (there are 4 tree-browsers)

## Constraints

- **Rule 4:** No file over 500 lines. If tests exceed 500 lines, split into multiple spec files.
- **Rule 5:** TDD. Tests are the implementation. No separate "tests for tests."
- **Rule 6:** No stubs. Every test must fully execute and assert.
- **Rule 10:** NO git operations without Q88N approval.

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-210-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Verification Steps

After implementation:

1. **Test against localhost (verify tests work):**
   ```bash
   cd browser
   DEPLOY_URL=http://localhost:5173 npx playwright test --config=playwright.deploy.config.ts
   ```
   All tests should pass (assuming vite is running).

2. **Test against dev.shiftcenter.com (if DNS is live):**
   ```bash
   cd browser
   DEPLOY_URL=https://dev.shiftcenter.com npx playwright test --config=playwright.deploy.config.ts
   ```
   Tests may pass or fail depending on deployment state.

3. **Verify screenshots saved:**
   ```bash
   ls -la .deia/hive/smoke/
   ```
   Should contain 9+ PNG files (one per test).

4. **Check no hardcoded URLs:**
   All URLs must use `baseURL` variable or `process.env.DEPLOY_URL`.

## Notes

- If DNS is not yet live, tests will fail with `ENOTFOUND` or `net::ERR_NAME_NOT_RESOLVED`. This is expected. Note it in the response file under "Issues / Follow-ups."
- If Vercel deployment is not yet pointing to Railway hivenode, `/health` test may fail with 404 or 502. This is expected if backend is not wired.
- The bee should handle slow network gracefully (15-second timeouts).
- The bee should NOT mock API calls in this suite (unlike chat-smoke.spec.ts). These are real smoke tests against deployed URLs.

---

**Model Assignment:** Sonnet
**Estimated Complexity:** Medium (new config + 9 tests)
**Estimated Time:** 45 minutes
