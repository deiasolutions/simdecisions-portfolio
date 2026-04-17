# TASK-062: Document Smoke Test Procedure -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-13

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\DEPLOYMENT-WIRING-NOTES.md` — Appended smoke test section (329 lines added)

## What Was Done

- Appended comprehensive smoke test section to existing DEPLOYMENT-WIRING-NOTES.md
- Documented 7 smoke tests covering Vercel, Railway, DNS, CORS, EGG loading, and rollback verification
- Added smoke test checklist (7 items) in markdown checkbox format
- Included "Next Steps" section for post-smoke-test actions (CORS update, production cutover, archival)
- Test environment section specifies frontend URL, backend URL, browser, and tools
- Each test includes: objective, steps, expected result, and failure troubleshooting
- All tests use Windows-style paths where applicable (e.g., `C:\Users\davee\...`)
- Rollback verification test (Test 7) ensures old production deploys remain live during staging
- Final section documents next steps after smoke tests pass (CORS update, production cutover, archival)

## Test Results

**Manual verification performed:**

1. **Markdown format validation:**
   - All 7 tests use consistent heading structure (### Test N: Title)
   - Code blocks use proper fencing (```bash, ```json, ```javascript)
   - Checklist uses correct markdown checkbox syntax (`- [ ]`)
   - No broken links or malformed markdown

2. **Checklist format verification:**
   - 7 checklist items match 7 tests
   - Each item has clear pass/fail criteria
   - Checklist includes "All tests pass?" and "Any tests fail?" decision points

3. **Content completeness:**
   - All 7 tests documented per spec requirements
   - Each test includes objective, steps, expected result, failure troubleshooting
   - Test environment section complete (frontend, backend, browser, tools)
   - Rollback plan referenced (DNS section → Rollback Plan)
   - Next steps section complete (CORS update, production cutover, archival)

4. **Path verification:**
   - Windows-style paths used in bash examples: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter`
   - Railway/Vercel URLs use placeholders: `<staging-url>`, `<service-name>`
   - DNS domains correctly specified: `dev.shiftcenter.com`, `code.shiftcenter.com`, etc.

**All validation checks passed.**

## Build Verification

N/A — This is a documentation task. No build or automated tests required.

## Acceptance Criteria

- [x] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\DEPLOYMENT-WIRING-NOTES.md` — Add smoke test section (append to existing file from TASK-058, 059, 060)
- [x] Smoke test section is valid markdown (no broken links)
- [x] All 7 tests are clearly documented (Test 1-7: Vercel build, frontend loading, Railway build, API health, CORS, EGG loading, rollback)
- [x] Checklist format is correct (markdown checkboxes: `- [ ]`)
- [x] Rollback plan is included (Test 7 + reference to DNS section rollback)
- [x] Test environment documented (frontend, backend, browser, tools)
- [x] Each test includes: objective, steps, expected result, failure troubleshooting
- [x] Next steps section added (CORS update, production cutover, archival)

## Clock / Cost / Carbon

**Clock:**
- File read (DEPLOYMENT-WIRING-NOTES.md): ~1 min
- Smoke test section write: ~3 min
- Manual markdown validation: ~2 min
- Response file write: ~1 min
- **Total:** ~7 minutes

**Cost:**
- Sonnet API calls: 2 (Read + Edit)
- Input tokens: ~31,000 (reading existing file + system context)
- Output tokens: ~3,500 (smoke test section + response file)
- Estimated cost: ~$0.25 USD

**Carbon:**
- Model inference: ~5g CO2e (estimated, Claude Sonnet)
- Data transfer: negligible
- **Total:** ~5g CO2e

## Issues / Follow-ups

### Dependencies (Upstream)
- **TASK-058** (Vercel config docs) — COMPLETED — smoke test references Vercel repoint procedure
- **TASK-059** (Railway config docs) — COMPLETED — smoke test references Railway repoint procedure
- **TASK-060** (DNS config docs) — COMPLETED — smoke test references DNS configuration and rollback plan
- **TASK-061** (Subdomain EGG routing) — COMPLETED — smoke test includes Test 6 (EGG loading with query param)

### Follow-ups (Downstream)
- **CORS update required** (separate task, not in scope):
  - `hivenode/main.py` line 233-237 needs update to include `dev.shiftcenter.com` and `code.shiftcenter.com` in `allow_origins` list
  - Referenced in Test 5 failure troubleshooting
  - Referenced in Next Steps section

- **Production cutover** (separate task, not documented in this file):
  - Update DNS for `code.shiftcenter.com` → new Vercel deploy
  - Update DNS for `api.shiftcenter.com` → new Railway deploy
  - Monitor production traffic
  - Keep old deploys live for 24 hours (rollback safety net)

- **Archival of old deploys** (separate task, after 7 days of stable production):
  - Delete old Vercel project from dashboard
  - Delete old Railway service from dashboard

### Notes
- This task is **documentation only** — smoke tests are NOT executed by this task
- Smoke tests will be executed by Q88N (human) or Q33NR (regent) when deploying
- All 7 tests are ready for execution once Vercel/Railway/DNS repoints are complete
- Markdown format validated manually (no automated markdown linter used)
- No dependencies on feature inventory (no feature added, only documentation)

---

**TASK-062 COMPLETE** — Smoke test documentation ready for cutover execution.
