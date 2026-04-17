# TASK-BUG-043: Fix E2E Server Startup Timeout

## Objective

Debug and fix the E2E server startup failure that causes all 28 integration tests in test_e2e.py to timeout with httpx.ConnectTimeout.

## Context

**Current state:**
- All 28 E2E integration tests fail with `httpx.ConnectTimeout: timed out`
- The test fixture starts a hivenode server in a subprocess and polls `/health` for up to 10 seconds
- Server never responds within that window
- The test fixture tries to capture stdout/stderr logs on failure but they appear empty in test output

**What works:**
- `python -c "from hivenode.main import app"` succeeds (imports cleanly)
- Manual uvicorn startup appears to work (no obvious crash)
- The issue only manifests in the E2E test subprocess environment

**Hypothesis:**
The E2E fixture sets specific environment variables that may be causing startup issues:
```python
env.update({
    "HIVENODE_MODE": "local",
    "HIVENODE_PORT": str(port),
    "HIVENODE_STORAGE_ROOT": str(storage_root),
    "HIVENODE_LEDGER_DB_PATH": str(tmp_dir / "ledger.db"),
    "HIVENODE_NODE_DB_PATH": str(tmp_dir / "nodes.db"),
    "HIVENODE_DATABASE_URL": f"sqlite+aiosqlite:///[REDACTED].db'}",
})
```

**Related work:**
- BUG-042 (BUS signature change) is still in progress but likely NOT the cause here
  - BUG-042 affects governance/dispositions/heartbeat tests
  - Those tests import/instantiate BUS class
  - E2E server startup doesn't fail on import (verified manually)
- Test sweep report shows 58+ BUS-related failures but those are in different test files

## Files to Read First

### E2E test infrastructure:
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_e2e.py (lines 1-120)

### Server initialization:
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py (lines 29-239 - lifespan function)

### Settings/config:
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py (check how environment variables are loaded)

## Investigation Approach

### Phase 1: Capture actual startup logs

Modify the test fixture temporarily to better capture logs:

1. Change subprocess.Popen to NOT pipe stderr/stdout initially (let it go to console)
2. OR: Read from the pipes incrementally during the wait loop
3. OR: Write logs to a temp file that can be read

Goal: See the ACTUAL error message from server startup failure

### Phase 2: Reproduce outside pytest

Create a standalone script that:
1. Sets the same environment variables as the E2E fixture
2. Starts uvicorn in a subprocess
3. Polls /health
4. Captures logs

This will determine if it's a pytest-specific issue or general subprocess issue.

### Phase 3: Fix root cause

Based on findings from Phase 1 and 2, implement the fix. Likely candidates:
- Missing database initialization (hivenode.db not created before startup)
- Path issues (Windows paths with tmp_path_factory)
- Missing config files or directories
- Import errors that only trigger in subprocess
- Async context issues in lifespan

## Deliverables

- [ ] Identify exact error causing E2E server startup failure (capture logs successfully)
- [ ] Determine if related to BUG-042 or separate issue
- [ ] Implement fix (could be test fixture fix OR server startup fix)
- [ ] Verify all 28 E2E tests pass after fix
- [ ] Verify no regressions in other test suites

## Test Requirements

**Primary test suite (E2E):**
```bash
cd tests/hivenode && python -m pytest test_e2e.py -v
```
Expected: 28 tests pass, 0 failures, 0 timeouts

**Verification (ensure no regressions):**
```bash
cd tests/hivenode && python -m pytest test_e2e.py test_routes.py test_storage.py -v
```

**If BUG-042 related (check these after fix):**
```bash
# Only if the fix touches BUS class or related code
cd tests/hivenode && python -m pytest governance/ cloud/ -v
```

## Acceptance Criteria

- [ ] All 28 E2E tests in test_e2e.py pass (no timeouts)
- [ ] Server starts successfully in E2E test fixture within 10 seconds
- [ ] Test output shows clear error messages on failure (improved logging)
- [ ] Root cause documented in response file
- [ ] No new test failures introduced
- [ ] Fix is minimal (don't refactor unrelated code)

## Constraints

- **Priority P0:** Blocks all E2E integration testing
- **TDD:** If modifying server code, write tests first
- **No file over 500 lines:** If creating new modules, keep them modular
- **No stubs:** Full implementation required
- **Do NOT modify BUS class:** That's handled by BUG-042 (separate task)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-BUG-043-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts, specific output
5. **Build Verification** — test/build output summary (last 10-20 lines)
6. **Acceptance Criteria** — copy from task, mark [x] done or [ ] not done with explanation
7. **Clock / Cost / Carbon** — all three, never omit any (estimate if needed)
8. **Issues / Follow-ups** — edge cases, dependencies, recommended next tasks

DO NOT skip any section.

## Example Fix Pattern (if it's a fixture issue)

If the issue is that stderr/stdout are buffered and not flushed:

```python
# Before
process = subprocess.Popen(
    [...],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

# After
process = subprocess.Popen(
    [...],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    bufsize=0,  # Unbuffered
)

# And during wait loop:
import select
while time.time() - start < max_wait:
    # Check if process died
    if process.poll() is not None:
        # Process exited - get logs
        stdout, stderr = process.communicate(timeout=1)
        raise RuntimeError(f"Server crashed: {stderr.decode()}")

    # ... rest of health check logic
```

## Example Fix Pattern (if it's a startup dependency issue)

If server needs database tables created first:

```python
# In fixture, before starting subprocess
from hivenode.inventory.store import init_engine
init_engine(f"sqlite:///[REDACTED].db'}")
```

---

**Model assignment:** Sonnet (investigation + debugging)

**Estimated effort:** 1-2 hours (depends on how hard it is to capture logs)

**Dependencies:** Independent of BUG-042 (can proceed in parallel)
