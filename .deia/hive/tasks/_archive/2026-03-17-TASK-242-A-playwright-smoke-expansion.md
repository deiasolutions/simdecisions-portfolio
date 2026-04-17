# TASK-242-A: Expand Playwright Smoke Tests for Production

## Objective
Add 5 new Playwright tests to `browser/e2e/deploy-smoke.spec.ts` to cover: landing page branding, efemera EGG layout, unauthenticated route rejection, FAB menu interaction (if exposed), and theme toggle (if exposed).

## Context

Wave 5 Ship (WAVE-5-SHIP.md) requires comprehensive smoke tests against production. Current test suite has 9 tests covering page load, health endpoint, EGG rendering, and terminal echo.

**Gap:** Missing tests for:
- Landing page branding verification
- Efemera EGG 4-pane layout
- Auth flow rejection for protected routes
- FAB menu interaction (empty pane state)
- Theme toggle functionality

**Existing patterns from `deploy-smoke.spec.ts`:**
- Use `process.env.DEPLOY_URL || 'https://dev.shiftcenter.com'` for base URL
- All tests use `afterEach` hook for screenshots (already configured)
- Use `page.locator()` with visibility timeouts (15s for shell, 10s for panes)
- Tests must gracefully handle features not yet exposed in production

**Key dependencies:**
- Shell executor routes use `verify_jwt_or_local` (auth required in cloud mode)
- Efemera routes have NO auth checks currently (per `routes.py`)
- Frontend components: EmptyPane has FAB menu trigger, theme switcher location TBD

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\e2e\deploy-smoke.spec.ts` — Current test suite (9 tests, 166 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\playwright.deploy.config.ts` — Playwright config
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\EmptyPane.tsx` — FAB menu trigger location
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\efemera.egg.md` — Efemera EGG layout definition

## Deliverables

Add 5 new tests to `deploy-smoke.spec.ts`:

### 1. Landing Page Branding Test
```typescript
test('should display ShiftCenter branding on landing page', async ({ page }) => {
  await page.goto(baseURL)
  const root = page.locator('#root')
  await expect(root).toBeVisible({ timeout: 15000 })

  // Verify title contains "ShiftCenter" (already verified in test 1, but check body content too)
  const bodyText = await page.textContent('body')
  expect(bodyText).toMatch(/ShiftCenter/i)
})
```

### 2. Efemera EGG Layout Test
```typescript
test('should render efemera EGG with 4 panes', async ({ page }) => {
  await page.goto(`${baseURL}?egg=efemera`)
  const shell = page.locator('.hhp-root')
  await expect(shell).toBeVisible({ timeout: 15000 })

  // Efemera layout: channels tree-browser, members tree-browser, text-pane, terminal
  // Count visible panes (4 total)
  const panes = page.locator('[data-node-id]')
  const count = await panes.count()
  expect(count).toBeGreaterThanOrEqual(4)
})
```

### 3. Protected API Rejection Test
```typescript
test('should reject protected API call without auth', async ({ page }) => {
  // Test /api/shell/exec endpoint (requires auth)
  // In production (cloud mode), this should return 401 or 403
  const resp = await page.request.post(`${baseURL}/api/shell/exec`, {
    data: {
      command: "echo",
      args: ["test"]
    }
  })
  // Expect 401 (unauthorized) or 403 (forbidden)
  expect([401, 403]).toContain(resp.status())
})
```

### 4. FAB Menu Interaction Test (conditional)
```typescript
test('should show FAB menu on empty pane hover', async ({ page }) => {
  await page.goto(baseURL)
  await page.waitForSelector('.hhp-root', { timeout: 15000 })

  // Look for empty pane (if exposed in production)
  const emptyPane = page.locator('.empty-pane').first()

  // Gracefully skip if empty pane not found (not exposed in prod yet)
  const emptyPaneCount = await emptyPane.count()
  if (emptyPaneCount === 0) {
    console.log('Empty pane not found in production - skipping FAB menu test')
    return
  }

  await emptyPane.hover()

  // Check for FAB menu visibility (if implemented)
  const fabMenu = page.locator('.fab-menu')
  await expect(fabMenu).toBeVisible({ timeout: 5000 })
})
```

### 5. Theme Toggle Test (conditional)
```typescript
test('should toggle theme when theme switcher clicked', async ({ page }) => {
  await page.goto(baseURL)
  await page.waitForSelector('.hhp-root', { timeout: 15000 })

  // Look for theme toggle button (selector TBD - check Shell or AppFrame)
  const themeToggle = page.locator('[aria-label="Toggle theme"]')

  // Gracefully skip if theme toggle not found
  const toggleCount = await themeToggle.count()
  if (toggleCount === 0) {
    console.log('Theme toggle not found in production - skipping theme test')
    return
  }

  // Get current theme from body or html data attribute
  const initialTheme = await page.getAttribute('html', 'data-theme')

  await themeToggle.click()

  // Verify theme changed
  const newTheme = await page.getAttribute('html', 'data-theme')
  expect(newTheme).not.toBe(initialTheme)
})
```

## Test Requirements

- [ ] Tests written in TDD style (no implementation needed - testing existing deployment)
- [ ] All 5 tests added to `deploy-smoke.spec.ts`
- [ ] Tests use existing patterns (afterEach screenshot, timeouts, locators)
- [ ] Tests 4 & 5 gracefully skip if features not exposed (console.log + early return)
- [ ] Total test count increases from 9 to 14
- [ ] Run tests against dev.shiftcenter.com: `npx playwright test --config=playwright.deploy.config.ts`
- [ ] All tests pass (or gracefully skip if feature not exposed)
- [ ] File stays under 500 lines (current 166 + ~60 new = ~226 lines)

## Edge Cases

- Empty pane FAB menu may not be exposed in production → graceful skip
- Theme toggle button may not exist yet → graceful skip
- Protected API endpoints may return 401 or 403 depending on auth implementation
- Efemera EGG may not be deployed yet → test should handle 404 gracefully
- Landing page branding may vary (logo, heading, title) → test for "ShiftCenter" text presence

## Constraints

- Rule 4: File must stay under 500 lines (currently 166, adding ~60 = 226 total)
- Rule 5: TDD (tests are testing existing prod deployment, so N/A)
- Rule 6: No stubs (all tests fully implemented)
- Use `process.env.DEPLOY_URL || 'https://dev.shiftcenter.com'` for base URL
- Use existing `afterEach` hook for screenshots (no changes needed)
- Timeout: 15s for shell visibility, 10s for panes, 5s for interactions

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-242-A-RESPONSE.md`

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

## Run Commands

```bash
# Run smoke tests against dev.shiftcenter.com
cd browser
npx playwright test --config=playwright.deploy.config.ts

# Run against custom URL
DEPLOY_URL=https://shiftcenter.com npx playwright test --config=playwright.deploy.config.ts
```
