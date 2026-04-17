# BRIEFING: Playwright Debug — canvas2 EGG Fails to Load

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-28
**Priority:** P0

## Context

Vite dev server is running on `http://localhost:5173`. Hivenode is running on port 8420. When navigating to `http://localhost:5173/?egg=canvas2`, the user sees "Failed to load EGG" on screen. The egg file itself serves correctly (curl returns 200 with valid content). Something in the client-side load pipeline is throwing.

## Your Mission

**Write and run a Playwright script that loads canvas2, captures ALL console output, and reports the exact error.**

### 1. Install Playwright if needed

Run `npx playwright install chromium` in the browser directory if not already installed.

### 2. Write a diagnostic Playwright script

Create file: `browser/src/shell/__tests__/egg-load-debug.spec.ts`

The script should:

a) **Capture ALL console messages** — log, warn, error, info. Every single one. Listen for `page.on('console')` and `page.on('pageerror')` BEFORE navigation.

b) **Navigate to `http://localhost:5173/?egg=canvas2`** — wait for networkidle or 15 seconds, whichever comes first.

c) **Capture the page content** — after load, get `document.body.innerText` and report it.

d) **Check for error elements** — look for any element containing "Failed to load" or "Error" text.

e) **Capture network requests** — listen for all fetch/XHR requests and their responses. Report any that failed (non-200 status). Pay special attention to requests for `.egg.md` files.

f) **Take a screenshot** — save to `.deia/hive/responses/20260328-canvas2-debug.png`

g) **Try to extract the exact error** — execute in page context:
```js
// The error state is in React component state
// Look for error text in the DOM
document.querySelector('[class*="error"]')?.textContent
```

h) **Also test the chat egg** — navigate to `http://localhost:5173/?egg=chat` and capture the same info. Does chat also fail?

i) **Also test with no egg param** — navigate to `http://localhost:5173/` (defaults to chat egg via hostname mapping). Does this work?

### 3. Run the script

Run it with: `npx playwright test egg-load-debug.spec.ts --reporter=list` from the browser directory.

### 4. If Playwright won't install or run

Fall back to using curl + Node.js to test the pipeline:
- curl each URL the app would fetch during load
- Check `/canvas2.egg.md` response
- Check if there are any TypeScript compile errors by running `npx tsc --noEmit` from browser/

## Deliverable

Write to: `.deia/hive/responses/20260328-EGG-LOAD-DEBUG.md`

Include:
1. **Every console message** captured during page load (verbatim)
2. **Every network request** and its status code
3. **The exact error message** shown to the user
4. **Screenshot path**
5. **Comparison** — does chat egg also fail? Does no-egg-param work?
6. **Root cause assessment** — what is throwing and why
7. **Fix recommendation** if root cause is identified

## Constraints

- You MAY create the Playwright test file
- You MAY run Playwright and tsc
- You MUST NOT modify any source files other than the test file
- Vite is already running on port 5173, do NOT start another instance

## Model Assignment

Sonnet — diagnostic script, read output, report findings.
