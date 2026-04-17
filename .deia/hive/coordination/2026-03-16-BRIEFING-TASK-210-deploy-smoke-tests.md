# BRIEFING: TASK-210 Deploy Smoke Test Suite

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-16
**Priority:** P0 (part of deploy verification pipeline)

---

## Objective

Create a Playwright test suite that verifies the deployed app at `dev.shiftcenter.com` works correctly. This suite runs as part of the build queue's deploy verification step. Unlike the existing `playwright.config.ts` (which tests localhost:5173 with vite dev server), this suite tests deployed URLs directly with NO vite server.

---

## Context from Q88N

The spec is TASK-210 (already in `.deia/hive/tasks/`). Key points:

1. **New config file:** `playwright.deploy.config.ts` (separate from existing `playwright.config.ts`)
2. **No vite server:** Tests deployed URL directly (default: `https://dev.shiftcenter.com`)
3. **Screenshots on every test:** Success AND failure, saved to `.deia/hive/smoke/`
4. **9+ tests:** Homepage, /health API, 4 EGG files (chat, canvas, build-monitor, sim), terminal flow, performance, console errors
5. **DNS dependency:** Tests may fail with ENOTFOUND if DNS is not yet live — this is expected and should be noted in response

Dependencies (both complete):
- `w3-01-vercel-railway-repoint` — COMPLETE
- `w3-02-dev-shiftcenter-dns` — COMPLETE

---

## Files to Review Before Writing Task

**Existing Playwright setup:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\playwright.config.ts` — local dev config (has webServer block)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\e2e\chat-smoke.spec.ts` — 5 tests, console error filtering pattern
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\e2e\sim-smoke.spec.ts` — 3 tests, shell rendering

**EGG files to test:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\build-monitor.egg.md` — 5 panes (data-service + 4 tree-browsers)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas.egg.md` — 5 panes (palette, canvas, chat, ir terminal, properties)

**Notes:**
- Build-monitor layout: top 4% data-service, then 3-column split (bees/queue left, log center, completed right)
- Canvas layout: 5 panes with unique nodeIds: `canvas-palette`, `canvas-editor`, `canvas-chat`, `canvas-ir`, `canvas-properties`

---

## Task Requirements

Q33N should write ONE task file for a BEE (sonnet model) to:

### Deliverables

1. **playwright.deploy.config.ts**
   - `baseURL` from `DEPLOY_URL` env var (default: `https://dev.shiftcenter.com`)
   - NO `webServer` block
   - `screenshot: 'always'`
   - `outputDir: '../.deia/hive/smoke/'`
   - `timeout: 15000` (generous for network)
   - `retries: 0`, `workers: 1`

2. **e2e/deploy-smoke.spec.ts**
   - 9+ tests (see spec for exact test scenarios)
   - `afterEach` hook to save screenshots to `.deia/hive/smoke/<test-name>-<timestamp>.png`
   - Console error filtering (ignore React DevTools warning)
   - Generous timeouts (10-15 seconds)
   - No API mocking (unlike chat-smoke.spec.ts) — these are real smoke tests

3. **.deia/hive/smoke/** directory
   - Create with `.gitkeep` file

### Test List (from spec)

1. Homepage loads (#root visible, title correct)
2. /health returns 200 with `status: "healthy"`
3. chat.egg.md renders 3 panes (tree-browser, text-pane, terminal)
4. canvas.egg.md renders 5 panes (use `.hhp-pane` or `[data-node-id]` selector, count 5)
5. build-monitor.egg.md renders (tree-browser visible)
6. Terminal input/response flow (type message, press Enter, verify echo)
7. Page load time < 3 seconds
8. No console errors (filter React DevTools warning)
9. sim.egg.md renders shell (`.hhp-root` visible)

### Verification Steps (BEE must run)

```bash
# Test against localhost first
cd browser
DEPLOY_URL=http://localhost:5173 npx playwright test --config=playwright.deploy.config.ts

# Test against dev.shiftcenter.com (may fail if DNS not live)
cd browser
DEPLOY_URL=https://dev.shiftcenter.com npx playwright test --config=playwright.deploy.config.ts

# Verify screenshots saved
ls -la .deia/hive/smoke/
```

---

## Constraints (from 10 Hard Rules)

- **Rule 3:** CSS uses `var(--sd-*)` only (not applicable to Playwright tests)
- **Rule 4:** No file over 500 lines (tests file should be ~300 lines)
- **Rule 5:** TDD — tests ARE the implementation
- **Rule 6:** NO STUBS — every test must fully execute and assert
- **Rule 8:** All file paths absolute in task file

---

## Model Assignment

**Sonnet** — estimated 45 minutes, medium complexity.

---

## Q33N Next Steps

1. Read the TASK-210 spec file at `.deia/hive/tasks/QUEUE-TEMP-2026-03-16-SPEC-TASK-210-deploy-smoke-tests.md` (or similar)
2. Read the 6 files listed above under "Files to Review"
3. Write ONE task file: `.deia/hive/tasks/2026-03-16-TASK-210-deploy-smoke-tests.md`
4. Include all 8 mandatory response file sections in task
5. Return to Q33NR for review before dispatch

---

## Expected Outcome

After BEE completes:
- 2 new files created (config + test spec)
- 1 new directory created (`.deia/hive/smoke/`)
- 9+ tests written and passing against localhost
- Tests may pass or fail against dev.shiftcenter.com depending on DNS/deployment state
- BEE response file notes any DNS/network issues under "Issues / Follow-ups"

---

## Notes for Q33N

- This is a NEW test suite, not modifications to existing chat-smoke.spec.ts
- Do NOT reuse existing playwright.config.ts — create new deploy-specific config
- Screenshots are ALWAYS saved (not just on failure) — this is intentional for smoke test evidence
- Console error filtering pattern exists in chat-smoke.spec.ts — BEE can reuse that pattern
- If tests fail against dev.shiftcenter.com, this is acceptable — just document in response

---

**Q33N: Please write the task file and return for review.**
