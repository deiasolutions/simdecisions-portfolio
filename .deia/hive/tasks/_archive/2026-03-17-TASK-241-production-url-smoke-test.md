# TASK-241: Production URL Smoke Test Script

**From:** Q33N
**To:** BEE (haiku)
**Date:** 2026-03-17
**Source:** Briefing TASK-241, Wave 5 Ship Task 5.2
**Priority:** P1

---

## Objective

Write a Python smoke test script that verifies all production URLs return expected responses, have valid TLS certificates, and respond within 5 seconds.

---

## Context

### What Exists
We have `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\smoke_test_dns.py` which tests dev.shiftcenter.com and api.shiftcenter.com. It follows these patterns:
- 4 test functions returning bool
- Exit code 0 (all pass) or 1 (any fail)
- `--verbose` flag
- ASCII-safe symbols: `[OK]`, `[FAIL]`, `[WARN]`
- Timeout: 10 seconds
- Uses Python stdlib: urllib, ssl, socket
- Clear section headers: `[1/N] Test Name`

### What's Missing
We need a production URL verification script for Wave 5 Ship (Task 5.2) that tests all production URLs:
1. `https://shiftcenter.com` — landing page
2. `https://chat.efemera.live` — Efemera chat (should load EGG)
3. `https://code.shiftcenter.com` — Code editor (should load EGG)
4. `https://ra96it.com` — Auth service (login or API)
5. `https://deiasolutions.org` — Global Commons (may be 404/503 for now)

### Expected Behavior
- Each URL should return 200 (or 3xx redirect)
- Response time < 5 seconds per URL
- Valid TLS certificate (urllib validates automatically)
- For `deiasolutions.org`: 404/503 acceptable → WARN not FAIL
- Exit code 0 if all tests pass, 1 if any fail

---

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\smoke_test_dns.py` — pattern reference (250 lines)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\WAVE-5-SHIP.md` — source spec

---

## Deliverables

- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\smoke_test_production.py`
  - Test function for each URL: `test_url(url, domain_name, allow_404=False) -> bool`
  - Check: HTTP status 200 or 3xx (redirects acceptable)
  - Check: Response time < 5 seconds
  - Check: Valid SSL/TLS certificate (urllib validates)
  - For `deiasolutions.org`: allow 404/503 as WARN not FAIL
  - Output format: `[N/5] Testing {domain_name}`
  - Exit code 0 if all pass, 1 if any fail
- [ ] Add `--verbose` flag for detailed output (optional, not required in Phase 1)
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\_tools\test_smoke_production.py`
  - Mock `urllib.request.urlopen` using `unittest.mock`
  - Test scenarios:
    1. All URLs return 200 → exit code 0
    2. One URL fails → exit code 1
    3. Timeout exceeded → exit code 1
    4. SSL error (URLError) → exit code 1
    5. deiasolutions.org returns 404 → WARN (exit code 0)
  - At least 5 test cases
- [ ] Run: `python -m pytest tests/_tools/test_smoke_production.py -v` — all tests pass

---

## Test Requirements (TDD)

Write tests FIRST in `tests\_tools\test_smoke_production.py`.

### Test Cases (minimum 5)
1. **test_all_urls_success**: Mock all 5 URLs return 200 → script exits 0
2. **test_one_url_fails**: Mock one URL returns 500 → script exits 1
3. **test_timeout**: Mock one URL times out (raise socket.timeout) → script exits 1
4. **test_ssl_error**: Mock one URL raises URLError (SSL issue) → script exits 1
5. **test_deiasolutions_404_acceptable**: Mock deiasolutions.org returns 404 → WARN printed, script exits 0

Use `unittest.mock.patch` to mock `urllib.request.urlopen`.

Example test structure:
```python
import pytest
from unittest.mock import patch, MagicMock
import sys
import io

# Import the script under test
sys.path.insert(0, 'C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\shiftcenter\\_tools')
import smoke_test_production


@patch('smoke_test_production.urllib.request.urlopen')
def test_all_urls_success(mock_urlopen):
    # Mock successful responses for all 5 URLs
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.headers.get.return_value = 'text/html'
    mock_urlopen.return_value.__enter__.return_value = mock_response

    # Run main and capture exit code
    with pytest.raises(SystemExit) as exc_info:
        smoke_test_production.main()

    assert exc_info.value.code == 0
```

Run command: `python -m pytest tests/_tools/test_smoke_production.py -v`

---

## Constraints

- No file over 500 lines (this script will be ~200 lines like smoke_test_dns.py)
- No hardcoded colors (N/A — CLI tool, ASCII symbols only)
- No stubs — every function fully implemented
- Use Python stdlib only: `urllib.request`, `urllib.error`, `socket`, `ssl`, `argparse`, `sys`, `time`
- No external dependencies (no `requests`, no `httpx`)
- Follow `smoke_test_dns.py` pattern exactly

---

## Implementation Notes

### URL Test Function Pattern
```python
def test_url(url: str, domain_name: str, allow_not_found: bool = False) -> bool:
    """Test a single production URL.

    Args:
        url: Full URL to test (e.g., "https://shiftcenter.com")
        domain_name: Human-readable name for output (e.g., "ShiftCenter Landing")
        allow_not_found: If True, 404/503 returns WARN not FAIL

    Returns:
        True if test passes, False otherwise.
    """
    # Test logic here
```

### Timeout Handling
Use `timeout=5` parameter in `urllib.request.urlopen()`:
```python
with urllib.request.urlopen(req, timeout=5) as response:
    # Check status, SSL is auto-validated by urllib
```

### SSL Validation
urllib handles SSL validation automatically. If certificate is invalid, it raises `urllib.error.URLError`. No need for explicit SSL check like in smoke_test_dns.py.

### Response Time Measurement
```python
import time
start = time.time()
# ... make request ...
elapsed = time.time() - start
if elapsed > 5.0:
    print(f"  {WARN}: Response time {elapsed:.2f}s > 5s")
```

### Main Function Structure
```python
def main():
    parser = argparse.ArgumentParser(description='Production URL Smoke Test')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    args = parser.parse_args()

    print("Running Production URL Smoke Tests...")

    results = []
    results.append(test_url("https://shiftcenter.com", "ShiftCenter Landing"))
    results.append(test_url("https://chat.efemera.live", "Efemera Chat"))
    results.append(test_url("https://code.shiftcenter.com", "ShiftCenter Code"))
    results.append(test_url("https://ra96it.com", "ra96it Auth"))
    results.append(test_url("https://deiasolutions.org", "Global Commons", allow_not_found=True))

    if all(results):
        print("All tests passed! [OK]")
        sys.exit(0)
    else:
        print("Test suite failed. See errors above.")
        sys.exit(1)
```

---

## Acceptance Criteria

When complete, mark each item:

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\smoke_test_production.py` created
  - Tests all 5 production URLs
  - Uses `urllib.request` (no external deps)
  - Timeout 5 seconds per URL
  - SSL validated automatically by urllib
  - Exit code 0 if all pass, 1 if any fail
  - `deiasolutions.org` 404/503 → WARN not FAIL
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\_tools\test_smoke_production.py` created
  - At least 5 test cases (all success, one fail, timeout, SSL error, 404 acceptable)
  - Uses `unittest.mock.patch` to mock urllib
  - All tests pass
- [ ] Run: `python -m pytest tests/_tools/test_smoke_production.py -v` → all tests pass
- [ ] No file exceeds 500 lines
- [ ] No stubs — all functions fully implemented

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
`.deia\hive\responses\20260317-TASK-241-RESPONSE.md`

The response MUST contain these 8 sections:

1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full absolute paths
3. **What Was Done** — bullet list of concrete changes (not intent)
4. **Test Results** — test files run, pass/fail counts, command output
5. **Build Verification** — test output summary (last 10 lines showing pass counts)
6. **Acceptance Criteria** — copy from task, mark [x] done or [ ] not done
7. **Clock / Cost / Carbon** — all three metrics, never omit any
8. **Issues / Follow-ups** — edge cases, known limitations, next tasks

DO NOT skip any section. Include absolute file paths. Include test pass counts. Include all three metrics (Clock/Cost/Carbon).

---

## Exit Checklist

Before writing your response file:

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] No file over 500 lines
- [ ] No stubs (every function implemented)
- [ ] Script exits 0 on success, 1 on failure
- [ ] SSL validation works (urllib handles it)
- [ ] Timeout works (5 seconds per URL)
- [ ] `deiasolutions.org` 404/503 → WARN not FAIL
- [ ] Response file has all 8 sections
