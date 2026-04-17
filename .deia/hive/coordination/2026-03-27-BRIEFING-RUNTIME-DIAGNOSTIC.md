# BRIEFING: Runtime Diagnostic — Why Aren't Chrome Primitives Rendering?

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-27 evening
**Priority:** P0

## Context

The EGG files reference chrome primitives (menu-bar, top-bar, status-bar). APP_REGISTRY has all seven chrome primitives registered. But when the app loads, the old UI renders — no new chrome bars appear.

Something in the runtime pipeline is dropping, hiding, or failing to render the chrome primitives. Your job is to trace the pipeline using Playwright and find where it breaks.

## Your Mission

**Use Playwright to load the app, inspect the DOM, and trace the rendering pipeline. Report what you find.**

### 1. Start the local dev server

Run `cd browser && npx vite --port 5174` in the background. Wait for it to be ready.

### 2. Write a Playwright diagnostic script

Write a Playwright test that:

a) **Loads canvas2** — navigate to `http://localhost:5174/?egg=canvas2`, wait for the app to render

b) **Dumps the DOM structure** — capture the full DOM tree of the app root. Report:
   - How many pane nodes are rendered?
   - What `data-app-type` attributes exist on each pane?
   - Is there a node with `data-app-type="menu-bar"`?
   - Is there a node with `data-app-type="status-bar"`?
   - What are the computed heights of any chrome pane nodes?

c) **Checks for legacy chrome** — search the DOM for:
   - Any element with class containing `WorkspaceBar`, `MasterTitleBar`, `ShellTabBar`
   - Any element rendered OUTSIDE the pane tree that looks like shell chrome
   - Report what's found

d) **Captures console errors** — listen for all console errors and warnings during page load. Report every error. Chrome primitives might be throwing on mount.

e) **Captures a screenshot** — save to `.deia/hive/responses/20260327-canvas2-diagnostic.png`

f) **Checks the inflated shell tree** — execute in page context:
   ```js
   // Try to access the shell state from React DevTools or window globals
   // The shell reducer state should contain the tree
   // Look for any debug globals the app exposes
   ```
   Report whatever tree structure you can extract.

g) **Checks APP_REGISTRY at runtime** — execute in page context:
   ```js
   // See if APP_REGISTRY is accessible as a module or window global
   // Check what appTypes are actually registered at runtime
   ```

### 3. Also test chat.egg.md

Repeat the DOM inspection for `http://localhost:5174/?egg=chat` — chat.egg.md also references menu-bar and top-bar. Compare results.

### 4. Check Shell.tsx source

Read `browser/src/shell/Shell.tsx` and report:
- Does it still render legacy chrome components (WorkspaceBar, MenuBar, ShellTabBar, MasterTitleBar) as direct children outside the pane tree?
- How does it render the pane tree? Does it pass through all node types or filter some?

### 5. Check the EGG inflater

Read the EGG loading pipeline:
- `browser/src/eggs/parseEggMd.ts`
- `browser/src/shell/eggToShell.ts`
- Any other file in the inflation chain

Report: is there any code that filters out, skips, or special-cases chrome appTypes during inflation?

## Deliverable

Write to: `.deia/hive/responses/20260327-RUNTIME-DIAGNOSTIC.md`

Structure:
1. **DOM inspection results** — what pane nodes exist, what appTypes rendered
2. **Legacy chrome check** — what old chrome components are in the DOM
3. **Console errors** — every error during load
4. **Screenshot** — path to the captured screenshot
5. **Shell.tsx analysis** — legacy chrome still rendering?
6. **Inflater analysis** — anything filtering chrome nodes?
7. **Root cause** — your best assessment of why chrome isn't rendering
8. **Fix recommendation** — what specific code changes would make chrome render

## Constraints

- You MAY write Playwright test code and run it
- You MAY read source files
- You MUST NOT modify any source files other than your Playwright test
- Put your Playwright test in `browser/src/shell/__tests__/chrome-diagnostic.spec.ts` or similar

## Model Assignment

Sonnet — needs to read code, write Playwright, analyze DOM output.
