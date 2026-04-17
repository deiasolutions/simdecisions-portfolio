# TASK-SEC-10: Defer config.py Initialization with Lazy Proxy

## Objective
Replace module-level `settings = HivenodeConfig()` with a lazy proxy that defers initialization until first attribute access.

## Context
Currently, `from hivenode.config import settings` triggers `HivenodeConfig()` initialization at import time, which creates directories and writes files. This causes issues in test environments and violates the principle of "import should be side-effect free."

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py`

## Deliverables
- [ ] Replace `settings = HivenodeConfig()` at bottom of config.py with:
  ```python
  class _LazySettings:
      _instance = None
      def __getattr__(self, name):
          if _LazySettings._instance is None:
              _LazySettings._instance = HivenodeConfig()
          return getattr(_LazySettings._instance, name)

  settings = _LazySettings()
  ```
- [ ] Verify `python -c "import hivenode.config"` does NOT create any directories or files
- [ ] Verify `python -c "from hivenode.config import settings; print(settings.mode)"` DOES initialize and works correctly
- [ ] Run full backend test suite: `python -m pytest tests/hivenode/ -v`
- [ ] Verify all tests still pass (no regressions)

## Test Requirements
- [ ] Test: Importing config module does NOT create directories
- [ ] Test: Accessing settings attribute DOES initialize config
- [ ] Test: Second attribute access uses cached instance (no re-init)
- [ ] All existing tests still pass
- [ ] Edge case: Multiple threads accessing settings concurrently initialize once

## Constraints
- No file over 500 lines
- No stubs
- TDD — write verification tests first
- Preserve all existing behavior (only defer initialization timing)

## Model
Sonnet (requires careful refactoring and threading consideration)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260325-TASK-SEC-10-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
