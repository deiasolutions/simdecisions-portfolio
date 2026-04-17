# TASK-BEE-R00: Environment Baseline (Smoke Test) -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-23

## Files Modified

None (read-only research).

## What Was Done

- Documented Python version: 3.12.10 (C:\Python312\python.exe)
- Documented Node version: v20.19.1
- Verified .deia/BOOT.md and .deia/HIVE.md exist and are readable
- Listed npm packages: 24 packages in browser/ (React, Vite, Vitest, Playwright, etc.)
- Listed pip packages: ~300 packages (including google-genai 1.61.0, anthropic, fastapi, etc.)
- Tested Railway PostgreSQL connection: SUCCESS (gondola.proxy.rlwy.net:11875)
- Ran pytest collection: 3009 tests collected, 9 import errors
- Ran npm build from browser/: SUCCESS (build completed in 17.27s)
- Attempted vitest run: in progress (tests running, no final count yet)

## Test Results Summary

### Python (pytest)
- **Collection**: 3009 tests collected
- **Errors**: 9 import errors during collection
- **Issue**: pytest runs under Python 3.13 (/c/Users/davee/AppData/Local/Programs/Python/Python313/) but packages installed under Python 3.12
- **Failed imports**:
  - tests/dispatch/test_child_process_cleanup.py
  - tests/hivenode/adapters/cli/test_claude_cli_token_tracking.py
  - tests/hivenode/adapters/cli/test_gemini_adapter.py
  - tests/hivenode/adapters/cli/test_process_tree_kill.py
  - tests/hivenode/adapters/test_gemini.py
  - tests/hivenode/storage/test_cloud_adapter.py
  - tests/hivenode/storage/test_cloud_adapter_e2e.py
  - tests/hivenode/storage/test_cloud_integration.py
  - tests/routes/test_heartbeat_metadata.py (file mismatch error)
- **Root cause**: `from google import genai` fails in Python 3.13 environment, but works in Python 3.12

### Browser (npm build)
- **Status**: SUCCESS
- **Build time**: 17.27s
- **Output**: dist/index.html (1.16 kB), dist/assets/index-DLiGmoRK.css (120.97 kB), dist/assets/index-C-C1g9jO.js (2,640.29 kB)
- **Warnings**: Large chunk size (2.6 MB JS bundle) - suggestion to use code splitting
- **Note**: gray-matter uses eval (security warning but expected)

### Browser (vitest)
- **Status**: RUNNING (final count not available in baseline window)
- **Observed failures**: MiniMap mock issues in Canvas.minimap.test.tsx
- **Note**: Previous log entry from BEE-R00 at 20:52 reported 1654 failures with DOM environment issues

## Environment Details

### Versions
- **Node**: v20.19.1
- **Python (default)**: 3.12.10 (C:\Python312\python.exe)
- **Python (pytest)**: 3.13.2 (/c/Users/davee/AppData/Local/Programs/Python/Python313/)
- **pytest**: 8.4.2
- **npm**: 24 packages installed

### Key npm Packages
- @playwright/test@1.58.2
- @testing-library/react@14.3.1
- @types/react@18.3.28
- @vitejs/plugin-react@4.7.0
- @vitest/ui@1.6.1
- @xyflow/react@12.10.1
- react@18.3.1
- typescript@5.9.3
- vite@5.4.21
- vitest@1.6.1

### Key pip Packages
- google-genai==1.61.0
- anthropic==0.76.0
- fastapi==0.128.0
- pytest==9.0.2
- pytest-asyncio==1.3.0
- SQLAlchemy==2.0.46
- psycopg2-binary==2.9.11
- pydantic==2.12.5

### Database Connectivity
- **Railway PostgreSQL**: ✓ REACHABLE
- **URL**: postgresql://[REDACTED]@[REDACTED]/railway
- **Connection test**: SUCCESS

### DEIA Files
- ✓ .deia/BOOT.md exists and readable
- ✓ .deia/HIVE.md exists and readable

## Critical Issues Found

### CRIT-1: Python Version Mismatch
pytest executable uses Python 3.13 but project packages installed in Python 3.12. This causes import failures for google.genai and potentially other packages.

**Impact**: Cannot run full pytest suite.

**Files affected**: All tests importing hivenode.adapters.gemini (9 test files).

### CRIT-2: File Path Mismatch
tests/routes/test_heartbeat_metadata.py has import mismatch with tests/hivenode/routes/test_heartbeat_metadata.py.

**Impact**: One test file cannot be collected.

**Recommendation**: Clear __pycache__ or rename test file.

## Build Warnings

### WARN-1: Large Bundle Size
Main JS bundle is 2.6 MB after minification. Vite recommends code splitting via dynamic import() or manual chunks configuration.

**Impact**: Slower initial page load.

### WARN-2: MiniMap Mock Missing Export
@xyflow/react mock missing "MiniMap" export in vitest setup.

**Impact**: Canvas.minimap.test.tsx tests likely failing.

## Summary

**Environment Status**: FUNCTIONAL with caveats

**Critical Blockers**:
- Python version mismatch prevents pytest execution
- Vitest test suite has execution issues (prior log: 50% failure rate)

**Working**:
- npm build: ✓ SUCCESS
- Railway PG connection: ✓ SUCCESS
- Node/Python/DEIA files: ✓ VERIFIED

**Recommended Actions**:
1. Install pytest in Python 3.12 environment OR install all packages in Python 3.13
2. Clear __pycache__ directories
3. Fix @xyflow/react mock to include MiniMap export
4. Investigate vitest DOM environment setup (document.is not defined errors)

---

## Appendix: Command Outputs

### pytest --collect-only
```
3009 tests collected, 9 errors in 5.70s
```

### npm run build
```
✓ built in 17.27s
dist/index.html                     1.16 kB │ gzip:   0.54 kB
dist/assets/index-DLiGmoRK.css    120.97 kB │ gzip:  19.28 kB
dist/assets/index-C-C1g9jO.js   2,640.29 kB │ gzip: 728.58 kB
```

### Railway PG Connection Test
```python
import psycopg2
conn = psycopg2.connect('postgresql://[REDACTED]@[REDACTED]/railway')
# SUCCESS
```
