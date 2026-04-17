# Q33N Report: TASK-241 Ready for Review

**From:** Q33N
**To:** Q33NR
**Date:** 2026-03-17
**Status:** AWAITING REVIEW

---

## Task File Created

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-17-TASK-241-production-url-smoke-test.md`

**Objective:** Write a Python smoke test script that verifies all production URLs (shiftcenter.com, chat.efemera.live, code.shiftcenter.com, ra96it.com, deiasolutions.org) return expected responses, have valid TLS certificates, and respond within 5 seconds.

---

## Task Breakdown

### Deliverables
1. **`_tools/smoke_test_production.py`** (new file, ~200 lines)
   - Test function for each of 5 production URLs
   - Check: HTTP 200 or 3xx (redirects OK)
   - Check: Response time < 5 seconds
   - Check: SSL validation (urllib handles automatically)
   - Special case: `deiasolutions.org` 404/503 → WARN not FAIL
   - Exit codes: 0 (all pass), 1 (any fail)
   - Pattern follows `smoke_test_dns.py` exactly

2. **`tests/_tools/test_smoke_production.py`** (new file, ~150 lines)
   - 5+ test cases using `unittest.mock.patch`
   - Mock `urllib.request.urlopen`
   - Tests: all success, one fail, timeout, SSL error, 404 acceptable
   - TDD: write tests FIRST

### Test Requirements (TDD)
- Write tests FIRST before implementation
- Minimum 5 test cases
- Mock HTTP calls using `unittest.mock`
- All tests must pass
- Run: `python -m pytest tests/_tools/test_smoke_production.py -v`

### Constraints Verified
- ✅ No file over 500 lines (script ~200 lines like reference)
- ✅ No hardcoded colors (CLI tool, ASCII symbols only)
- ✅ No stubs (every function fully implemented)
- ✅ Python stdlib only (urllib, ssl, socket, argparse, sys, time)
- ✅ No external dependencies
- ✅ Follows `smoke_test_dns.py` pattern

---

## Files to be Created

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\smoke_test_production.py`
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\_tools\test_smoke_production.py`

---

## Pattern Reference

Task follows the exact pattern from `smoke_test_dns.py`:
- Test functions return bool (pass/fail)
- Clear section headers: `[1/5] Testing {domain}`
- ASCII-safe symbols: `[OK]`, `[FAIL]`, `[WARN]`
- Exit code 0/1
- urllib handles SSL validation automatically
- Timeout via `urllib.request.urlopen(req, timeout=5)`

---

## Special Cases Handled

1. **deiasolutions.org**: May return 404 or 503 if not yet deployed
   - Behavior: Print `[WARN]`, return True (not False)
   - Script exits 0 (pass) not 1 (fail)

2. **Response time**: Measure elapsed time, warn if > 5 seconds
   - Use `time.time()` before/after request

3. **SSL validation**: urllib validates automatically
   - No explicit SSL check needed
   - URLError raised on invalid cert → test fails

---

## Model Assignment

**haiku** — Straightforward Python script following existing pattern, no complex logic.

---

## Acceptance Criteria (from Task File)

- [ ] `_tools/smoke_test_production.py` created
  - Tests all 5 production URLs
  - Timeout 5 seconds per URL
  - SSL validated automatically
  - Exit code 0 if all pass, 1 if any fail
  - `deiasolutions.org` 404/503 → WARN not FAIL
- [ ] `tests/_tools/test_smoke_production.py` created
  - At least 5 test cases
  - Uses `unittest.mock.patch`
  - All tests pass
- [ ] Run: `python -m pytest tests/_tools/test_smoke_production.py -v` → all pass
- [ ] No file exceeds 500 lines
- [ ] No stubs

---

## Ready for Dispatch?

**YES** — Task file is complete and follows all DEIA rules:
- ✅ All file paths absolute
- ✅ TDD requirements specified
- ✅ Concrete acceptance criteria
- ✅ No stubs allowed
- ✅ Pattern reference provided
- ✅ Test count specified (5+)
- ✅ Response file requirements (8 sections mandatory)
- ✅ Exit checklist included

**Awaiting Q33NR approval to dispatch.**

---

## Dispatch Command (when approved)

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-17-TASK-241-production-url-smoke-test.md --model haiku --role bee --inject-boot
```
