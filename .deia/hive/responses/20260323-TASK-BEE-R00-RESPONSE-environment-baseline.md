# TASK-BEE-R00: Environment Baseline (Smoke Test) -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-23

## Files Modified

None (READ-ONLY research task)

## What Was Done

- Verified Node.js version: v20.19.1
- Verified Python version: 3.12.10
- Verified `.deia/BOOT.md` exists and is readable (121 lines)
- Verified `.deia/HIVE.md` exists and is readable (376 lines)
- Counted npm packages in browser/: 24 direct dependencies
- Counted pip packages: 300 total installed
- Tested Railway PostgreSQL connection: SUCCESS (gondola.proxy.rlwy.net:11875)
- Ran pytest: **9 collection errors** (missing dependencies: `respx`, `google.generativeai`)
- Ran npm build: **FAILS** at copy-eggs step (node inline script error)
- Ran npx vitest run: **1654 failed, 1605 passed, 40 skipped** (3299 total tests)

## Test Results

### Python Backend (pytest)
- **Status:** Collection errors (9 errors in 8.63s)
- **Issue:** Missing dependencies:
  - `respx` (required by cloud integration tests)
  - `google.generativeai` (required by Gemini adapter tests)
- **Affected test files:**
  - `tests/dispatch/test_child_process_cleanup.py`
  - `tests/hivenode/adapters/cli/test_claude_cli_token_tracking.py`
  - `tests/hivenode/adapters/cli/test_gemini_adapter.py`
  - `tests/hivenode/adapters/cli/test_process_tree_kill.py`
  - `tests/hivenode/adapters/test_gemini.py`
  - `tests/hivenode/storage/test_cloud_adapter.py`
  - `tests/hivenode/storage/test_cloud_adapter_e2e.py`
  - `tests/hivenode/storage/test_cloud_integration.py`
  - `tests/routes/test_heartbeat_metadata.py` (import file mismatch / __pycache__ issue)

### React Frontend (vitest)
- **Status:** RED (1654 failed / 1605 passed / 40 skipped)
- **Test Files:** 187 failed | 85 passed | 4 skipped (276 total)
- **Duration:** 56.01s
- **Common failure pattern:** `ReferenceError: document is not defined`
  - Example: `browser/src/apps/sim/components/flow-designer/simulation/__tests__/useSimulation.test.ts`
  - Hook tests failing due to missing DOM environment setup

### Build (npm run build)
- **Status:** FAILS at copy-eggs step
- **Error:** Node inline script in package.json fails
- **Root cause:** Unknown (script exists in package.json, eggs directory exists with 20 .egg.md files)
- **Note:** EGG files exist in both:
  - Source: `eggs/` (20 files)
  - Destination: `browser/public/` (already has 18 .egg.md files from previous build)

## Build Verification

- **pytest:** Collection errors due to missing dependencies (`respx`, `google.generativeai`)
- **vitest:** 1654 failures (mostly `document is not defined` in React hook tests)
- **npm build:** FAILS at copy-eggs step

## Acceptance Criteria

From task file:

- [x] Run `pytest` from repo root — documented pass/fail count (9 collection errors)
- [x] Run `npm run build` from browser/ — documented errors vs clean build (FAILS at copy-eggs)
- [x] Run `npx vitest run` from repo root — documented pass/fail count (1654 failed, 1605 passed)
- [x] Document Node version (v20.19.1)
- [x] Document Python version (3.12.10)
- [x] List installed npm packages (24 direct dependencies listed)
- [x] List installed pip packages (300 total packages)
- [x] Check if Railway PG is reachable (SUCCESS — connection established)
- [x] Verify `.deia/BOOT.md` and `.deia/HIVE.md` exist and are readable (both verified)

## Clock / Cost / Carbon

- **Clock:** ~8 minutes (test execution: pytest 8.63s, vitest 56.01s, npm build attempts ~3 min, data gathering ~2 min)
- **Cost:** ~$0.02 USD (Sonnet 4.5, minimal token usage for command execution and file reads)
- **Carbon:** ~0.5g CO2e (estimated based on cloud compute + network traffic)

## Issues / Follow-ups

### Critical (P0)
1. **Missing Python dependencies:**
   - `respx` (HTTP mocking for cloud tests)
   - `google.generativeai` (Gemini adapter)
   - Action: Add to `requirements.txt` or `pyproject.toml`

2. **npm build fails at copy-eggs step:**
   - Inline node script in package.json fails
   - EGG files already present in `browser/public/` from previous builds
   - Action: Debug copy-eggs script or remove from build chain (eggs may be served via Vite plugin instead)

### High (P1)
3. **1654 vitest failures (50% failure rate):**
   - Common pattern: `ReferenceError: document is not defined`
   - React hook tests failing due to DOM environment issues
   - Action: Check vitest config for `environment: 'jsdom'` or missing setup files

4. **pytest import file mismatch:**
   - `tests/routes/test_heartbeat_metadata.py` has duplicate in `tests/hivenode/routes/`
   - __pycache__ collision
   - Action: Remove duplicate file or clear __pycache__

### Environment Details
- **Node.js:** v20.19.1
- **Python:** 3.12.10
- **npm packages (browser/):** 24 direct deps (React, Vite, Vitest, Playwright, etc.)
- **pip packages:** 300 total (includes: anthropic, pytest, fastapi, sqlalchemy, psycopg2, etc.)
- **Railway PG:** gondola.proxy.rlwy.net:11875 — REACHABLE

### Next Steps
1. Install missing Python dependencies (`respx`, `google-generativeai`)
2. Fix vitest DOM environment setup (jsdom config)
3. Debug or remove copy-eggs build step
4. Clear __pycache__ and resolve pytest import conflicts
5. Re-run baseline after fixes to establish GREEN state
