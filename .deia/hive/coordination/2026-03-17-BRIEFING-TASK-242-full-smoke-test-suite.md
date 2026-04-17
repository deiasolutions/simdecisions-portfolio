# BRIEFING: TASK-242 — Full Smoke Test Suite Against Production

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-17
**Source Spec:** `docs/specs/WAVE-5-SHIP.md` — Task 5.3
**Priority:** P1
**Model:** sonnet

---

## Objective

Expand the existing deploy smoke test suite to cover critical user flows against production: page load, EGG loading, auth, chat send/receive, terminal submit, and API endpoint protection.

---

## Context

Wave 5 Ship. We have basic smoke tests in `browser/e2e/deploy-smoke.spec.ts` (9 tests) that cover:
- Page load and root element rendering
- Basic EGG loading (chat, canvas, build-monitor, sim)
- Terminal input echo
- Performance checks

**Gap:** No tests for:
- Auth flow (unauthenticated user sees login prompt)
- Protected API endpoints rejecting without auth (401)
- Chat message send/receive flow
- Terminal submit with IR routing
- Theme toggle functionality
- FAB menu interaction

The spec requires comprehensive coverage of critical flows. Tests must be skippable if production is unreachable (graceful failure).

---

## Files to Read First

### Existing Tests
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\e2e\deploy-smoke.spec.ts` — Current deploy smoke tests (9 tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\playwright.deploy.config.ts` — Playwright config for deploy tests
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_e2e.py` — Existing E2E test patterns for backend

### Auth & Protected Routes
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\auth.py` — Auth verification logic
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\shell.py` — Shell execute endpoint (protected)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\efemera\routes.py` — Efemera endpoints (protected)

### Frontend Components
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\TextPane.tsx` — Chat interface
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalApp.tsx` — Terminal component
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\EmptyPane.tsx` — FAB menu trigger

---

## Requirements

### Deliverables

1. **Expand `browser/e2e/deploy-smoke.spec.ts`:**
   - Add test: landing page shows ShiftCenter branding (verify title, logo, or heading)
   - Add test: `?egg=efemera` loads 4-pane layout
   - Add test: unauthenticated user accessing protected route sees login prompt or error
   - Add test: FAB menu opens on empty pane interaction (if exposed in prod)
   - Add test: theme toggle works (if theme switcher is exposed in prod UI)

2. **Create `tests/smoke/test_production_api.py`:**
   - Test: `/health` returns 200
   - Test: `/api/shell/execute` rejects without auth (401 or 403)
   - Test: `/efemera/channels` rejects without auth (401 or 403)
   - All tests must gracefully skip if production URL is unreachable (use pytest.skip or try/except)

3. **Test Requirements:**
   - All new tests follow existing patterns in `deploy-smoke.spec.ts`
   - Use `afterEach` hook for screenshots (already present)
   - Configure reasonable timeouts (existing: 15s for visibility, 3s for page load)
   - Use `process.env.DEPLOY_URL || 'https://dev.shiftcenter.com'` for base URL
   - Backend tests use `httpx.get()` or `httpx.post()` with timeout

4. **Run Instructions:**
   - Document in file header how to run tests
   - Playwright: `npx playwright test --config=playwright.deploy.config.ts`
   - Backend: `pytest tests/smoke/test_production_api.py -v`

---

## Constraints

- **Rule 5 (TDD):** Tests first, then implementation. (N/A — this task IS writing tests)
- **Rule 6 (NO STUBS):** Every test must be fully implemented. No `test.skip()` placeholders.
- **Rule 3 (NO HARDCODED COLORS):** N/A (no CSS changes)
- **Rule 4 (500 line limit):** `deploy-smoke.spec.ts` is currently 166 lines. Adding ~50-80 lines keeps it under 250. Backend smoke tests should be < 150 lines.
- **Graceful failure:** Tests must not fail the entire suite if production is down. Use `test.skip()` conditionally or pytest.mark.skipif.

---

## Dependencies

- **TASK-241:** Production URLs must be verified first (per spec)
- Production environment must be deployed and accessible

---

## Task Breakdown for Q33N

Q33N: break this into bee-sized tasks:

1. **TASK-242-A:** Expand Playwright smoke tests (`deploy-smoke.spec.ts`)
   - Add 4-6 new tests (branding, efemera EGG, auth flow, FAB menu, theme toggle)
   - Model: Haiku (straightforward Playwright test additions)

2. **TASK-242-B:** Create backend API smoke tests (`tests/smoke/test_production_api.py`)
   - 3 tests: /health, /api/shell/execute (401), /efemera/channels (401)
   - Model: Haiku (simple httpx requests)

---

## Acceptance Criteria

- [ ] `browser/e2e/deploy-smoke.spec.ts` has 13-15 tests total (9 existing + 4-6 new)
- [ ] New tests cover: landing branding, efemera EGG, auth rejection, FAB menu, theme toggle
- [ ] `tests/smoke/test_production_api.py` exists with 3 tests (health, shell reject, efemera reject)
- [ ] All tests pass against dev.shiftcenter.com (or DEPLOY_URL env var)
- [ ] Tests gracefully skip if production unreachable
- [ ] Run instructions documented in file headers
- [ ] All tests use existing patterns (no new test frameworks or helpers)

---

## Response Template

Q33N: after writing task files, return:

1. List of task files created (absolute paths)
2. Summary of task breakdown (which bee does what)
3. Estimated test count increase (current: 9 Playwright + 0 backend → target: 15 Playwright + 3 backend)
4. Any questions or blockers

Do NOT dispatch bees yet. Wait for Q33NR review and approval.

---

## Notes

- Existing `deploy-smoke.spec.ts` already has good patterns for screenshot capture, timeout handling, and EGG loading verification. Extend those patterns.
- Backend smoke tests should be FAST (< 5 seconds total runtime). No waiting, no retries. Just hit endpoint, check status code.
- Production URL is configurable via `DEPLOY_URL` env var (Playwright) or similar pattern for backend tests.
- If a test depends on a feature not yet exposed in production (e.g., theme toggle button not visible), the test should gracefully skip with a reason logged.

---

**Q33NR (signing off)**
