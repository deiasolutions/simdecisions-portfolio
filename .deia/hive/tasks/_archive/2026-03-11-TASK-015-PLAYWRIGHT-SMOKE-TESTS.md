# TASK-015: Playwright Smoke Tests for Chat App

## Objective

Write 5 Playwright end-to-end smoke tests that verify the chat.egg.md product renders and functions in a real browser. Tests go at `browser/e2e/`. Mock LLM API calls — do NOT burn real tokens.

## Context

TASK-013 delivers the first runnable product: `cd browser && npm run dev` starts Vite on localhost:5173, loads chat.egg.md, renders the Shell with a terminal pane. This task validates that the full stack actually works in a browser — not just unit tests with jsdom, but real DOM rendering with Playwright.

**Dependency:** TASK-013 must be complete before this task runs. All source files from TASK-013 must exist.

## Files to Read First

Read these to understand what the app renders:

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\main.tsx` — app entry point
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\App.tsx` — root component, EGG loading
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\vite.config.ts` — dev server config
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\index.html` — HTML entry
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\terminalAdapter.tsx` — terminal registration
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalApp.tsx` — terminal component
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalPrompt.tsx` — prompt input
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` — terminal hook (handles LLM calls)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\frank\frankService.ts` — sendMessage (the function to mock)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\frank\types.ts` — FrankMetrics type
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\Shell.tsx` — shell frame
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\shell-themes.css` — theme variables
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\package.json` — scripts, dependencies
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\chat.egg.md` — product definition

## The 5 Smoke Tests

All tests in `browser/e2e/chat-smoke.spec.ts`.

### Test 1: Vite starts and page loads
- Start Vite dev server (`npm run dev`)
- Navigate to `http://localhost:5173`
- Assert page title or root element exists
- Assert no console errors on load (filter out known warnings like React dev mode)
- Assert the `#root` div has content (not empty)

### Test 2: Shell renders with terminal pane
- Navigate to `http://localhost:5173?egg=chat`
- Wait for shell to render (`.hhp-root` element exists)
- Assert terminal pane is visible (look for terminal-specific CSS class or data-testid)
- Assert status bar renders (model name, currency badges)
- Assert the shell theme variables are applied (background color is not white/default)

### Test 3: hive> prompt accepts input
- Navigate to chat app
- Wait for terminal prompt to appear
- Find the input element (`.terminal-input` or `input[type="text"]` inside terminal)
- Type "hello world" into the prompt
- Assert the input value updates to "hello world"
- Press Enter
- Assert an input entry appears in the output (the typed command rendered back)
- Assert the input field clears after submit

### Test 4: BYOK key storage in browser
- Navigate to chat app
- Execute JS to set localStorage key: `localStorage.setItem('sd-api-key', 'test-key-12345')`
- Reload the page
- Execute JS to read: `localStorage.getItem('sd-api-key')`
- Assert value is still `'test-key-12345'` (persistence works)
- Assert no API key appears in any network request headers (key stays in browser)
- Clear the key and verify it's gone

### Test 5: Send message and receive LLM response (mocked)
- **Mock the LLM API call** — intercept the outbound fetch/XHR to the Anthropic/Groq/OpenAI endpoint using Playwright's `page.route()`. Return a mock response:
  ```json
  {
    "content": [{"type": "text", "text": "Hello! I'm a mock response from the test suite."}],
    "usage": {"input_tokens": 10, "output_tokens": 15}
  }
  ```
- Set a mock API key in localStorage so the app thinks BYOK is configured
- Type a message in the prompt and press Enter
- Wait for the response to appear in the terminal output
- Assert the mock response text appears: "Hello! I'm a mock response from the test suite."
- Assert metrics appear in the status bar (clock, cost, carbon values update from zero)
- Assert no real API calls escaped the mock (verify route handler was called)

## Setup Requirements

### Playwright Configuration

Create `browser/playwright.config.ts`:
- Base URL: `http://localhost:5173`
- Web server command: `npm run dev` (auto-start Vite)
- Web server port: 5173
- Web server reuseExistingServer: true (for dev convenience)
- Timeout: 30s per test
- Retries: 0 (smoke tests should be deterministic)
- Reporter: list (for CI) + html (for local debug)
- Browser: chromium only (smoke tests, not cross-browser)

### Package Updates

Update `browser/package.json`:
- Add devDependencies: `@playwright/test`
- Add script: `"test:e2e": "playwright test"`
- Add script: `"test:e2e:ui": "playwright test --ui"` (for debugging)

### Install Playwright Browsers

After updating package.json, run:
```bash
cd browser && npx playwright install chromium
```

## Deliverables

### Test Files (1)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\e2e\chat-smoke.spec.ts` — 5 smoke tests

### Config Files (1)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\playwright.config.ts` — Playwright configuration

### Package Updates (1)
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\package.json` — Add @playwright/test, e2e scripts

### Verification
- [ ] All 5 tests pass with `npx playwright test`
- [ ] Vite dev server starts and stops cleanly
- [ ] No real LLM API tokens consumed during test run
- [ ] Tests complete in under 30 seconds total

**Total: 3 deliverables + verification**

## Constraints

- TypeScript strict mode
- Playwright test runner (NOT Jest, NOT Vitest for e2e)
- All tests in `browser/e2e/` directory (separate from unit tests)
- Mock ALL outbound LLM API calls — zero real tokens burned
- Do NOT modify any source files — only create test/config files and update package.json
- Tests must be deterministic (no flaky waits — use Playwright's auto-waiting)
- No hardcoded timeouts — use `page.waitForSelector()`, `expect(locator).toBeVisible()` etc.

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-015-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** -- task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** -- every file created/modified/deleted, full paths
3. **What Was Done** -- bullet list of concrete changes
4. **Test Results** -- test files run, pass/fail counts
5. **Build Verification** -- playwright output summary
6. **Acceptance Criteria** -- copy deliverables above, mark [x] or [ ]
7. **Clock / Cost / Carbon** -- all three, never omit any
8. **Issues / Follow-ups** -- edge cases, dependencies, recommended next tasks

DO NOT skip any section. A response without all 8 sections is incomplete.
