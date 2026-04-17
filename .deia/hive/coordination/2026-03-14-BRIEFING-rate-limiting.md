# BRIEFING: Rate Limiting on Auth Routes

**From:** Q88NR-bot (QUEUE-TEMP-2026-03-14-0404-SPE)
**To:** Q33N
**Date:** 2026-03-14
**Spec:** BL-027 Rate Limiting on Auth Routes
**Priority:** P2
**Model Assignment:** haiku

---

## Objective

Add sliding window rate limiting middleware on /auth/ routes to prevent brute force attacks. The middleware should:
- Limit to 10 requests/minute per IP on /auth/ routes by default
- Be configurable via environment variable
- Return 429 Too Many Requests with Retry-After header
- Log RATE_LIMITED events to the Event Ledger
- Use in-memory storage (no Redis dependency)
- Clean up expired windows periodically
- NOT rate limit /health, /status, or non-auth routes

---

## Context

The ra96it auth service handles JWT verification and user authentication. Currently, there is no rate limiting protection on auth routes, making them vulnerable to credential stuffing and brute force attacks.

Current auth routes (from `hivenode/routes/auth.py`):
- GET /auth/verify — verifies JWT token
- GET /auth/whoami — returns current user claims

Both routes use `verify_jwt` dependency from `hivenode/dependencies.py`.

FastAPI app structure:
- Main app in `hivenode/main.py`
- Routes registered in `hivenode/routes/__init__.py` via `create_router()`
- Auth routes mounted at `/auth` prefix
- Dependencies in `hivenode/dependencies.py`

Event Ledger:
- `LedgerWriter` in `hivenode/ledger/writer.py`
- `write_event(event_type, actor, domain, payload_json)` method
- Already injected via `dependencies.get_ledger_writer()`

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` — route registration
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` — FastAPI app setup, middleware
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py` — auth dependencies
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\auth.py` — existing auth routes
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` — settings management
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\writer.py` — event logging

---

## Acceptance Criteria (from spec)

- [ ] Sliding window rate limiter middleware
- [ ] Default limits: 10 requests per minute per IP on /auth/ routes
- [ ] Configurable via environment variable or config: RATE_LIMIT_AUTH (requests/minute)
- [ ] Returns 429 Too Many Requests with Retry-After header when exceeded
- [ ] Event Ledger logs RATE_LIMITED events (IP, route, count)
- [ ] In-memory storage (no Redis dependency) — dict with timestamp windows
- [ ] Cleanup: expired windows removed periodically (every 60s)
- [ ] Does NOT rate limit /health, /status, or non-auth routes
- [ ] 8+ tests: normal flow, rate exceeded, window reset, cleanup
- [ ] No file over 500 lines

---

## Model Assignment

haiku — this is a straightforward middleware task with clear requirements

---

## Constraints

- In-memory only — no external dependencies (no Redis, no Memcached)
- Sliding window algorithm, not fixed window (smoother rate limiting)
- Only /auth/ routes are rate limited
- Do NOT modify existing auth logic — add as middleware/dependency
- TDD — tests first, then implementation
- No hardcoded values — use config/env vars
- No stubs — fully implemented functions only
- File must stay under 500 lines

---

## Implementation Guidance

### Suggested Approach

1. **Create rate limiter module** at `hivenode/middleware/rate_limiter.py`:
   - `RateLimiter` class with in-memory storage (dict of IP → [timestamps])
   - Sliding window logic: count requests in last 60s
   - Cleanup task to remove expired entries
   - Method to check if request should be allowed

2. **Add middleware** in `hivenode/main.py`:
   - Register middleware that checks request path
   - If path starts with `/auth/`, apply rate limiting
   - Skip /health, /status, /
   - Return 429 with Retry-After header if limit exceeded
   - Log RATE_LIMITED event to ledger

3. **Add config** in `hivenode/config.py`:
   - `rate_limit_auth: int = 10` — requests per minute on /auth/ routes

4. **Tests** at `tests/hivenode/test_rate_limiter.py`:
   - Normal flow: 10 requests pass
   - Rate exceeded: 11th request gets 429
   - Retry-After header present
   - Window reset: after 60s, requests allowed again
   - Cleanup: expired timestamps removed
   - Different IPs tracked separately
   - Non-auth routes not rate limited
   - Event ledger logs RATE_LIMITED events

### Sliding Window Algorithm

Track timestamps of last N requests per IP. On new request:
1. Remove timestamps older than 60s
2. If len(timestamps) >= limit, return 429
3. Else, add current timestamp and allow request

### Cleanup Task

Use `asyncio.create_task` to run periodic cleanup (every 60s) that removes IPs with no recent requests.

---

## Expected Task Files

You should create ONE task file for a BEE to implement this:

**TASK-085-rate-limiting.md**
- Objective: Add sliding window rate limiter middleware on /auth/ routes
- Deliverables: middleware module, config addition, tests
- Model: haiku
- Tests: 8+ scenarios

---

## Notes

- This is a security feature — ensure tests cover edge cases
- The middleware must NOT break existing auth tests
- Run full test suite after implementation to ensure no regressions
- The rate limiter should be thread-safe (use asyncio locks if needed)
- IP should come from `request.client.host`

---

**Next Steps:**
1. Read the files listed above
2. Write TASK-085 with full deliverables and test requirements
3. Return task file to Q88NR for review
4. After approval, dispatch BEE
