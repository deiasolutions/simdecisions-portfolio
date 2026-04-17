# TASK-241: Production URL Smoke Test Script (W5 — 5.2)

## Objective
Write an automated smoke test script that verifies all production URLs are accessible and return expected responses.

## Context
Wave 5 Ship. Before declaring the product shipped, every production URL must respond correctly. This script runs as a pre-ship checklist item.

## Source Spec
`docs/specs/WAVE-5-SHIP.md` — Task 5.2

## Files to Read First
- `browser/e2e/deploy-smoke.spec.ts` — Existing deploy smoke test (if any)
- `_tools/smoke_test_dns.py` — Existing DNS smoke test
- `.deia/hive/smoke/` — Existing smoke test artifacts

## Deliverables
- [ ] Create `_tools/smoke_test_production.py`:
  - Check each URL returns 200 (or expected redirect):
    - `https://shiftcenter.com` — landing page
    - `https://chat.efemera.live` — Efemera chat (should load EGG)
    - `https://code.shiftcenter.com` — Code editor (should load EGG)
    - `https://ra96it.com` — Auth service (should show login or API)
    - `https://deiasolutions.org` — Global Commons (if deployed)
  - Check each URL has valid TLS certificate
  - Check response time < 5 seconds
  - Output: PASS/FAIL for each URL, summary at end
  - Exit code 0 if all pass, 1 if any fail
- [ ] Add `--verbose` flag for detailed output
- [ ] Add test in `tests/_tools/test_smoke_production.py` (mock HTTP calls)
- [ ] Run: `python -m pytest tests/_tools/`

## Priority
P1

## Model
haiku
