# YOUR ROLE: BEE

# TASK: Rename ra96it module to hodeia_auth

## Objective
The directory `ra96it/` has already been `git mv`'d to `hodeia_auth/`. The test directory `tests/ra96it/` still needs renaming to `tests/hodeia_auth/`. All Python imports, config references, and build paths that say `ra96it` (the module, NOT the domain) must be updated to `hodeia_auth`.

## What to change

### 1. Internal imports in `hodeia_auth/` files
All `from ra96it.` → `from hodeia_auth.` (absolute imports). Relative imports (e.g., `from .config import`) stay unchanged.

Files to update:
- `hodeia_auth/main.py`
- `hodeia_auth/db.py`
- `hodeia_auth/config.py`
- `hodeia_auth/models.py`
- `hodeia_auth/schemas.py`
- `hodeia_auth/routes/*.py`
- `hodeia_auth/services/*.py`

### 2. External imports referencing ra96it
- `hivenode/dependencies.py`
- `hivenode/main.py`
- `hivenode/storage/adapters/cloud.py`
- `hivenode/adapters/cli/claude_cli_subprocess.py`
- `_tools/inventory.py`
- `_tools/check_railway_env.py`
- `_tools/cross_reference.py`
- `_tools/recover_backlog.py`
- `hivenode/inventory/store.py`
- `hivenode/hive_mcp/tests/test_tools_queue.py`

### 3. Test directory
- `git mv tests/ra96it tests/hodeia_auth`
- Update all imports inside `tests/hodeia_auth/*.py` from `from ra96it.` to `from hodeia_auth.`
- Update `tests/hivenode/test_auth_*.py` and `tests/hivenode/test_rate_limiter.py` if they import from ra96it

### 4. Config and build files
- `hodeia_auth/nixpacks.toml`: `ra96it/requirements.txt` → `hodeia_auth/requirements.txt`, `uvicorn ra96it.main:app` → `uvicorn hodeia_auth.main:app`
- Root `nixpacks.toml` (if exists): same changes
- `pyproject.toml`: update any ra96it references
- Comments/docstrings that say "ra96it" as a module name → "hodeia_auth"

### 5. Railway env var
- The `NIXPACKS_START_CMD` and `RAILWAY_START_COMMAND` on Railway reference `ra96it.main:app`. This will be handled separately. Just fix the code.

## What NOT to change
- `ra96it.com` domain strings in eggResolver.ts, test files, config allowed_origins — those are real domain references, keep them
- `.deia/` coordination docs, specs, briefings
- Browser test files referencing ra96it.com as a URL
- Git history

## Test command
```
python -m pytest tests/hodeia_auth/ -x -q
python -m pytest tests/hivenode/test_auth_routes.py tests/hivenode/test_auth_identity.py tests/hivenode/test_auth_dual_issuer.py -x -q
```

## DO NOT commit or push. Just make the changes and report what you did.
