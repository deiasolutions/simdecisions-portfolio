# TASK-201: DNS Configuration Smoke Test Script

## Objective
Create automated smoke test script that verifies dev.shiftcenter.com and api.shiftcenter.com are correctly configured and accessible.

## Context
After Q88N completes manual DNS configuration (TASK-186), we need an automated way to verify both domains are working. This script will be run by Q88N to confirm:
1. DNS records resolve correctly
2. HTTPS loads without errors
3. SSL certificates are valid
4. API endpoint responds

From spec `.deia/hive/queue/2026-03-16-3001-SPEC-w3-02-dev-shiftcenter-dns.md`:

**Smoke Test Requirements:**
- https://dev.shiftcenter.com loads the chat app
- https://api.shiftcenter.com/health returns 200 (or staging equivalent)

**Acceptance Criteria:**
- dev.shiftcenter.com CNAME -> Vercel (cname.vercel-dns.com or similar)
- Vercel custom domain dev.shiftcenter.com assigned to dev branch
- SSL works (Cloudflare flex or full)
- api.shiftcenter.com CNAME verified for Railway
- Both resolve and load correctly

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-16-3001-SPEC-w3-02-dev-shiftcenter-dns.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\inventory.py` (as reference for CLI tool structure)

## Deliverables

### Primary Deliverable
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\_tools\smoke_test_dns.py` — automated smoke test script

### Script Requirements

#### Exit Codes
- [ ] Exit 0 on all tests pass
- [ ] Exit 1 on any test failure
- [ ] Exit 2 on configuration error (missing dependencies)

#### Test 1: DNS Resolution
- [ ] Resolve `dev.shiftcenter.com` using `socket.getaddrinfo()` or `dns.resolver`
- [ ] Resolve `api.shiftcenter.com` using same method
- [ ] Report resolved IP addresses
- [ ] PASS if both resolve, FAIL if either does not

#### Test 2: HTTPS Load Test (dev.shiftcenter.com)
- [ ] HTTP GET to `https://dev.shiftcenter.com`
- [ ] Verify response status 200 or 3xx (redirects OK)
- [ ] Verify SSL certificate is valid (no cert errors)
- [ ] Verify response contains HTML (content-type check)
- [ ] Timeout: 10 seconds
- [ ] PASS if loads successfully, FAIL on timeout or error

#### Test 3: API Health Check (api.shiftcenter.com)
- [ ] HTTP GET to `https://api.shiftcenter.com/health`
- [ ] Verify response status 200
- [ ] Verify SSL certificate is valid
- [ ] Verify response is JSON or text (not HTML error page)
- [ ] Timeout: 10 seconds
- [ ] PASS if returns 200, FAIL on non-200 or timeout

#### Test 4: SSL Certificate Validation
- [ ] Verify dev.shiftcenter.com certificate is trusted (not self-signed)
- [ ] Verify api.shiftcenter.com certificate is trusted
- [ ] Check certificate expiration > 7 days
- [ ] PASS if both valid, FAIL if either has SSL issues

#### Output Format
```
Running DNS Configuration Smoke Tests...

[1/4] DNS Resolution
  dev.shiftcenter.com -> 76.76.21.21 ✓
  api.shiftcenter.com -> 104.28.15.4 ✓
  PASS

[2/4] HTTPS Load Test (dev.shiftcenter.com)
  GET https://dev.shiftcenter.com
  Status: 200 OK ✓
  SSL: Valid ✓
  Content-Type: text/html ✓
  PASS

[3/4] API Health Check (api.shiftcenter.com)
  GET https://api.shiftcenter.com/health
  Status: 200 OK ✓
  SSL: Valid ✓
  PASS

[4/4] SSL Certificate Validation
  dev.shiftcenter.com: Valid until 2026-06-15 ✓
  api.shiftcenter.com: Valid until 2026-06-15 ✓
  PASS

All tests passed! ✓
```

On failure, show clear error message:
```
[1/4] DNS Resolution
  dev.shiftcenter.com -> FAILED: Name or service not known
  FAIL

Test suite failed. See errors above.
```

#### CLI Usage
```bash
python _tools/smoke_test_dns.py
```

Optional verbosity flag:
```bash
python _tools/smoke_test_dns.py --verbose
```

## Test Requirements

### Tests for the Smoke Test Script
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\_tools\test_smoke_test_dns.py`
- [ ] Test script can be imported without errors
- [ ] Test DNS resolution logic (mock DNS calls)
- [ ] Test HTTPS request logic (mock requests)
- [ ] Test exit code behavior (0 on pass, 1 on fail)
- [ ] Test output formatting
- [ ] Edge cases: timeout, SSL errors, 404 responses, DNS failures

**Minimum:** 8 tests covering all 4 smoke test stages

## Constraints

- **No file over 500 lines:** Script should be under 300 lines
- **No hardcoded colors:** Use plain text output (✓ ✗ symbols OK)
- **No stubs:** Every test must be fully implemented
- **Standard library preferred:** Use `socket`, `urllib`, `ssl` (avoid external deps if possible)
- **If using requests:** Add to requirements.txt if not already present

## Dependencies

The script may use:
- `socket` (standard library, DNS resolution)
- `ssl` (standard library, certificate validation)
- `urllib` or `http.client` (standard library, HTTP requests)
- `requests` library (optional, simpler API) — only if already in requirements

## Model Assignment
Haiku

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-201-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — pytest output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Acceptance Criteria

From spec:
- [ ] https://dev.shiftcenter.com loads the chat app (tested by script)
- [ ] https://api.shiftcenter.com/health returns 200 (tested by script)

Task-specific:
- [ ] Script created at `_tools/smoke_test_dns.py`
- [ ] All 4 test stages implemented (DNS, HTTPS, API, SSL)
- [ ] Exit codes correct (0 on pass, 1 on fail)
- [ ] Output formatting clear and actionable
- [ ] Tests written for the script (minimum 8 tests)
- [ ] All tests pass
- [ ] Script can run standalone: `python _tools/smoke_test_dns.py`
