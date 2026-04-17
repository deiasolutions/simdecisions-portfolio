# TASK-W3-04: Add Rate Limit Headers to Successful Auth Responses

## Objective

Add `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset` headers to all successful (200-299) responses from `/auth/` routes. The 429 response already includes `Retry-After` and should not be modified.

## Context

**Current state:**
- Rate limiter middleware exists at `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\middleware\rate_limiter.py`
- 9 comprehensive tests pass in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_rate_limiter.py`
- Middleware tracks requests per IP using sliding window (10 req/min default)
- 429 responses include `Retry-After` header
- **Missing:** Standard rate limit headers on successful responses

**Industry standard:** Rate limit headers on successful responses inform clients about remaining quota:
- `X-RateLimit-Limit`: Maximum requests in window (always 10 for /auth/)
- `X-RateLimit-Remaining`: Requests remaining in current window
- `X-RateLimit-Reset`: Unix timestamp when oldest request in window expires (when reset is possible)

**Key pattern:** The middleware already calculates oldest timestamp when checking rate limit. Reuse that logic to compute Reset time.

## Files to Read First

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\middleware\rate_limiter.py` — lines 44-96 (dispatch method, where response is sent)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_rate_limiter.py` — all tests (understand test structure)
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` — lines 54-56 (config is already loaded)
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` — lines 268-272 (middleware registration)

## Deliverables

- [x] Modify `RateLimiterMiddleware._is_rate_limited()` to return reset timestamp in addition to boolean and retry_after
- [x] Add method `_add_rate_limit_headers()` to construct the 3 headers
- [x] Modify `dispatch()` to call `call_next()`, capture response, add headers if status 200-299, and return
- [x] Write test FIRST: successful response includes 3 headers with correct values
- [x] Verify all 9 existing tests still pass
- [x] No file exceeds 500 lines (rate_limiter.py currently ~203 lines, will remain under 250)

## Test Requirements

- [x] **Write test FIRST (TDD):** New test `test_rate_limit_successful_response_includes_headers()` that:
  1. Makes a request to `/auth/verify` (within limit)
  2. Asserts response status is 200
  3. Asserts `X-RateLimit-Limit` header is "10" (or `settings.rate_limit_auth`)
  4. Asserts `X-RateLimit-Remaining` header is "9" (or max_requests - 1)
  5. Asserts `X-RateLimit-Reset` header is a valid Unix timestamp integer (>= now + 55, <= now + 60)
  6. Make 10 requests total, verify Remaining decrements correctly

- [x] **Verify no regressions:** Run all 10 tests (9 existing + 1 new):
  - test_rate_limit_allows_requests_within_limit
  - test_rate_limit_returns_429_when_exceeded
  - test_rate_limit_429_includes_retry_after_header
  - test_rate_limit_window_resets_after_60_seconds
  - test_rate_limit_separate_ips_tracked_separately
  - test_rate_limit_non_auth_routes_not_limited
  - test_rate_limit_root_not_limited
  - test_rate_limit_sliding_window_not_just_burst
  - test_rate_limit_concurrent_requests_same_ip
  - test_rate_limit_edge_case_limit_of_one
  - **NEW:** test_rate_limit_successful_response_includes_headers

- [x] **Edge cases:**
  - Headers present only on 2xx responses (not 429, not other errors)
  - Remaining count is accurate across multiple requests
  - Reset time is correctly calculated based on oldest request in window

## Constraints

- No file over 500 lines (rate_limiter.py will stay ~240 lines)
- TDD: write test first, then implementation
- No stubs. Every function fully implemented.
- Rate limit headers only on successful /auth/ responses (not on 429, not on non-auth routes)
- Remaining and Reset must be accurate per-IP (already per-IP in state dict)

## Implementation Hints

**Step 1:** Write test in `test_rate_limiter.py`:
```python
@pytest.mark.asyncio
async def test_rate_limit_successful_response_includes_headers(rate_limiter_app):
    """Test that successful auth responses include rate limit headers."""
    # Make 1 request, verify 3 headers, repeat up to 10
    # Verify Limit, Remaining, Reset values
```

**Step 2:** Modify `_is_rate_limited()` to return reset timestamp:
```python
async def _is_rate_limited(self, ip: str) -> tuple[bool, int, int]:
    # ... existing logic ...
    # Return: (is_limited, retry_after, reset_timestamp)
```

**Step 3:** Add helper method:
```python
def _add_rate_limit_headers(self, response: Response, limit: int, remaining: int, reset: int) -> Response:
    response.headers["X-RateLimit-Limit"] = str(limit)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Reset"] = str(reset)
    return response
```

**Step 4:** Modify `dispatch()`:
```python
if not self._should_rate_limit(request.url.path):
    return await call_next(request)

ip = self._get_client_ip(request)
is_limited, retry_after, reset = await self._is_rate_limited(ip)

if is_limited:
    return Response(..., status_code=429, headers={"Retry-After": str(retry_after)})

response = await call_next(request)
if 200 <= response.status_code < 300:
    # Add rate limit headers
    remaining = self.max_requests - len(self._requests[ip])
    self._add_rate_limit_headers(response, self.max_requests, remaining, reset)

return response
```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-W3-04-RESPONSE.md`

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
