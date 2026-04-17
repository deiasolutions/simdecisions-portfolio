# Briefing: TASK-241 — Production URL Smoke Test Script

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-17
**Source Spec:** `docs/specs/WAVE-5-SHIP.md` (Task 5.2)
**Priority:** P1
**Model:** haiku

---

## Objective

Write an automated Python smoke test script that verifies all production URLs are accessible, return expected responses, have valid TLS certificates, and respond within 5 seconds.

This is Wave 5 Ship Task 5.2 — verifying production URLs work before declaring the product shipped.

---

## Context

### Existing Infrastructure
We already have:
1. **`_tools/smoke_test_dns.py`** — DNS smoke test for dev.shiftcenter.com and api.shiftcenter.com
   - Tests DNS resolution, HTTPS load, API health, SSL validation
   - Pattern: 4 test functions, exit code 0/1, `--verbose` flag
2. **`browser/e2e/deploy-smoke.spec.ts`** — Playwright E2E smoke tests
   - Tests deployed app at dev.shiftcenter.com
   - Tests EGG rendering, terminal input, page load time, console errors
   - Saves screenshots to `.deia/hive/smoke/`

### What's Missing
We need a **production URL verification script** that checks all production URLs are live:
- `https://shiftcenter.com` — landing page
- `https://chat.efemera.live` — Efemera chat (should load EGG)
- `https://code.shiftcenter.com` — Code editor (should load EGG)
- `https://ra96it.com` — Auth service (should show login or API)
- `https://deiasolutions.org` — Global Commons (if deployed, may be 404 for now)

### Pattern to Follow
Follow the same pattern as `smoke_test_dns.py`:
- Test functions that return bool (pass/fail)
- Exit code 0 if all pass, 1 if any fail
- `--verbose` flag for detailed output
- Clear section headers: `[1/N] Test Name`
- ASCII-safe symbols: `[OK]`, `[FAIL]`, `[WARN]`
- Timeout: 5 seconds per request
- SSL validation (Python stdlib handles this via `urllib`)

---

## Acceptance Criteria

- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\smoke_test_production.py`
  - Check each URL returns 200 (or expected redirect 3xx):
    - `https://shiftcenter.com` — landing page (200 or 3xx)
    - `https://chat.efemera.live` — Efemera chat (200, should load EGG)
    - `https://code.shiftcenter.com` — Code editor (200, should load EGG)
    - `https://ra96it.com` — Auth service (200, should show login or API)
    - `https://deiasolutions.org` — Global Commons (200 or 404/503 acceptable)
  - Check each URL has valid TLS certificate (SSL validation via urllib)
  - Check response time < 5 seconds per URL
  - Output: PASS/FAIL for each URL, summary at end
  - Exit code 0 if all pass, 1 if any fail
- [ ] Add `--verbose` flag for detailed output
- [ ] Add test in `tests\_tools\test_smoke_production.py` (mock HTTP calls using unittest.mock)
- [ ] Run: `python -m pytest tests/_tools/` — all tests must pass

---

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\smoke_test_dns.py` — pattern reference
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\WAVE-5-SHIP.md` — source spec

---

## Test Requirements (TDD)

Create `tests\_tools\test_smoke_production.py`:
- Mock `urllib.request.urlopen` to return mock responses
- Test scenarios:
  - All URLs return 200 → exit code 0
  - One URL fails → exit code 1
  - Timeout exceeded → exit code 1
  - SSL error → exit code 1
  - Verbose flag → more output
- At least 5 test cases

Run: `python -m pytest tests/_tools/test_smoke_production.py -v`

---

## Constraints

- No file over 500 lines (modularize at 500, hard limit 1,000)
- No hardcoded colors (N/A — this is CLI tool)
- No stubs — every function fully implemented
- Use Python stdlib only (urllib, ssl, socket, argparse, sys)
- No external dependencies (no requests, no httpx)
- Follow smoke_test_dns.py pattern exactly

---

## Notes

- `deiasolutions.org` may return 404 or 503 if not yet deployed — this should be WARN, not FAIL
- Response time check: measure from request start to response headers received
- SSL validation: urllib handles this automatically, will raise URLError on invalid cert
- Exit codes: 0 = all pass, 1 = one or more fail, 2 = config error (reserved for future use)

---

## Response File Requirements

When complete, write:
`.deia/hive/responses/20260317-TASK-241-RESPONSE.md`

Include all 8 mandatory sections:
1. Header (status, model, date)
2. Files Modified (absolute paths)
3. What Was Done (concrete changes)
4. Test Results (test files, pass/fail counts)
5. Build Verification (test output summary)
6. Acceptance Criteria (mark [x] done or [ ] not done)
7. Clock / Cost / Carbon (all three)
8. Issues / Follow-ups (edge cases, next tasks)

---

## Model Assignment

**haiku** — straightforward Python script following existing pattern, no complex logic.
