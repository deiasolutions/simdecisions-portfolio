# BRIEFING: Security + Infrastructure Cleanup

**Date:** 2026-03-25
**From:** Q33NR
**To:** Q33N
**Source:** `C:\Users\davee\Downloads\RUNBOOK-SECURITY-CLEANUP.md`

---

## Objective

Execute the security and infrastructure cleanup runbook. Phase 0 (credential rotation) is already done by Q88N. You are responsible for Phases 1–5, **excluding CORS changes** (TASK 1.3 is explicitly skipped).

---

## PHASE 1: Remove Hardcoded Credentials

### TASK 1.1: Clean config.py

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py`

1. Find where `RAILWAY_DATABASE_URL` and `RAILWAY_DATABASE_PUBLIC_URL` are hardcoded as string constants. **Delete both lines entirely.**

2. Find where `inventory_database_url` falls back to a hardcoded Railway URL. Replace the fallback logic with:

```python
_inv_url = os.environ.get("HIVENODE_INVENTORY_DATABASE_URL", "")
if _inv_url == "local" or not _inv_url:
    inventory_database_url = f"sqlite:///[REDACTED].db'}"
else:
    inventory_database_url = _inv_url
```

3. Search the entire file for any `postgresql://` string. There should be zero hardcoded postgres URLs when done.

4. Verify `database_url` (the main one) reads from `os.environ.get("DATABASE_URL")` with no hardcoded production fallback.

5. Run config tests: `python -m pytest tests/hivenode/test_config.py -v` — update assertions if they expect old hardcoded URLs.

### TASK 1.2: Verify .env and .gitignore

1. Confirm `.env` is in `.gitignore`
2. Confirm `.env` is NOT tracked (`git status .env` should show nothing or untracked)

### TASK 1.4: Add Rate Limiting

1. Install `slowapi` — add to `pyproject.toml` dependencies
2. In `hivenode/main.py`, add limiter setup:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(status_code=429, content={"error": "Too many requests"})
```

3. Apply `@limiter.limit("10/minute")` on any LLM-facing routes (check `hivenode/routes/` for chat/LLM endpoints).

---

## PHASE 2: Scrub Git History — SKIP

**Q88N will handle git history scrubbing separately.** Do NOT run git-filter-repo or force push. Do NOT do any git write operations.

---

## PHASE 3: Repo Hygiene

### TASK 3.1: Identify Junk Files

Look for malformed artifacts in repo root: `{browser`, `{hivenode`, `nul`, files starting with `C...`, and `k.startsWith('RAILWAY')))`. **List them in your response** but do NOT delete them (no git operations without Q88N approval).

### TASK 3.2: Review .gitignore

Check if these patterns are present, list any that are missing:

```
{*
nul
*.tmp
*.bak
__pycache__/
.pytest_cache/
*.pyc
*.pyo
node_modules/
browser/dist/
.env
.env.*
.env.local
.vscode/settings.json
*.swp
*~
Thumbs.db
.DS_Store
```

---

## PHASE 4: Fix Test Environment

### TASK 4.1: Fix Python Tests (Windows tmp_path)

**Problem:** PermissionError creating `tmp_path` under `%TEMP%`.

Add to `tests/conftest.py`:
```python
import tempfile
import os

if os.name == 'nt':
    _test_tmp = os.path.join(os.path.expanduser("~"), ".shiftcenter", "test_tmp")
    os.makedirs(_test_tmp, exist_ok=True)
    tempfile.tempdir = _test_tmp
```

Run backend tests and record results.

### TASK 4.2: Fix Frontend Tests (Vitest esbuild EPERM)

Run `cd browser && npx vitest run --reporter=verbose` and record results. If esbuild spawn fails, try:
1. `cd browser && rm -rf node_modules && rm package-lock.json && npm install`
2. `node node_modules/esbuild/install.js`

### TASK 4.3: Verify Build

Run `cd browser && npm run build`. Must complete without errors.

### TASK 4.4: Record Baseline

Create `.deia/hive/coordination/2026-03-25-TEST-BASELINE.md` with pass/fail/skip counts for both backend and frontend.

---

## PHASE 5: Fix Import-Time Side Effects

### TASK 5.1: Defer config.py Initialization

**Problem:** `settings = HivenodeConfig()` at module level runs at import time, creating directories and writing files.

Replace with lazy proxy:
```python
class _LazySettings:
    _instance = None
    def __getattr__(self, name):
        if _LazySettings._instance is None:
            _LazySettings._instance = HivenodeConfig()
        return getattr(_LazySettings._instance, name)

settings = _LazySettings()
```

This preserves `from hivenode.config import settings` everywhere but defers initialization until first attribute access.

Verify: `python -c "import hivenode.config"` should NOT create any directories.

Run full test suite after this change.

---

## Constraints

- NO git write operations (commit, push, etc.) without Q88N approval
- NO CORS changes (TASK 1.3 is skipped)
- NO git history scrubbing (Phase 2 is skipped)
- NO file deletions without listing them first
- CSS: `var(--sd-*)` only
- No file over 500 lines
- TDD — tests first
- No stubs

## Model Assignment

Dispatch bees at **sonnet** for code tasks. This is infrastructure work requiring careful reading.
