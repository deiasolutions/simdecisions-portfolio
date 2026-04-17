# Q33N Response: Rate Limiting Task Files

**From:** Q33N (coordinator)
**To:** Q33NR
**Date:** 2026-03-14
**Briefing:** 2026-03-14-BRIEFING-rate-limit.md
**Spec:** BL-027 Rate Limiting on Auth Routes

---

## Summary

I have read the briefing and codebase. I created ONE task file for a BEE to implement sliding window rate limiting on /auth/ routes.

---

## Task Files Created

### TASK-085: Rate Limiting on Auth Routes
**File:** `.deia/hive/tasks/2026-03-14-TASK-085-rate-limiting.md`
**Model:** haiku
**Objective:** Add sliding window rate limiter middleware on /auth/ routes to prevent brute force attacks

**Deliverables:**
1. Rate limiter middleware module (`hivenode/middleware/rate_limiter.py`)
   - `RateLimiterMiddleware` class extending `BaseHTTPMiddleware`
   - In-memory storage (dict of IP → timestamps)
   - Sliding window algorithm (60-second window)
   - Thread-safe using `asyncio.Lock`
   - Periodic cleanup task (every 60s)
   - Returns 429 with Retry-After header
   - Logs RATE_LIMITED events to Event Ledger

2. Config addition (`hivenode/config.py`)
   - Add `rate_limit_auth: int = 10` field
   - Env var: `HIVENODE_RATE_LIMIT_AUTH`

3. Middleware registration (`hivenode/main.py`)
   - Register middleware after CORS
   - Pass `max_requests=settings.rate_limit_auth`

4. Tests (`tests/hivenode/test_rate_limiter.py`)
   - 10+ test scenarios
   - Normal flow, rate exceeded, window reset, cleanup, etc.
   - Event logging verification

**Test Requirements:**
- 10+ scenarios covering normal flow, rate limit exceeded, window reset, different IPs, cleanup, non-auth routes, concurrent requests
- TDD: tests written first
- All tests must pass

**Constraints Met:**
- ✅ No file over 500 lines (~200-250 expected for rate_limiter.py)
- ✅ TDD — tests first, then implementation
- ✅ No stubs — full implementation required
- ✅ In-memory only — no Redis dependency
- ✅ Thread-safe — uses asyncio.Lock
- ✅ No hardcoded values — uses config
- ✅ Middleware-only — no modification of existing auth logic

---

## Codebase Analysis

**Files Read:**
1. `hivenode/main.py` — FastAPI app setup, CORS middleware registered via `app.add_middleware()`
2. `hivenode/routes/__init__.py` — Routes registered via `create_router()`
3. `hivenode/routes/auth.py` — Two routes: `/auth/verify` and `/auth/whoami`, both use `verify_jwt` dependency
4. `hivenode/config.py` — Pydantic settings with env_prefix="HIVENODE_"
5. `hivenode/dependencies.py` — Global instances, `get_ledger_writer()` dependency
6. `hivenode/ledger/writer.py` — `write_event(event_type, actor, domain, payload_json)` method
7. `tests/hivenode/test_auth_routes.py` — Existing auth tests use `AsyncClient`, `ASGITransport`, `mock_settings` fixture

**Key Findings:**
- FastAPI middleware uses `BaseHTTPMiddleware` from starlette
- Request IP available via `request.client.host`
- Middleware pattern: `async def dispatch(self, request: Request, call_next)`
- Existing tests use `AsyncClient(transport=ASGITransport(app=app), base_url="http://test")`
- Event Ledger uses universal entity ID format: `ip:{address}`
- No existing middleware directory — will create `hivenode/middleware/`

**Implementation Approach:**
- Sliding window algorithm: track timestamps per IP, remove expired, check count
- Cleanup task: `asyncio.create_task()` running every 60s
- Only rate limit paths starting with `/auth/`
- Skip `/health`, `/status`, `/` (root endpoint)
- Return 429 with `Retry-After: {seconds}` header
- Log `RATE_LIMITED` events with IP, route, count

---

## Files to Create

1. `hivenode/middleware/__init__.py` (empty, for Python module)
2. `hivenode/middleware/rate_limiter.py` (~200-250 lines)
3. `tests/hivenode/test_rate_limiter.py` (~300-400 lines for 10+ tests)

---

## Files to Modify

1. `hivenode/config.py` — Add `rate_limit_auth: int = 10` field
2. `hivenode/main.py` — Import and register middleware

---

## Estimated Complexity

**Simple-Medium** — This is a straightforward middleware implementation with well-defined requirements:
- Standard FastAPI middleware pattern
- Standard sliding window algorithm
- Standard asyncio patterns for locks and background tasks
- No external dependencies
- Clear test scenarios

**Haiku is appropriate** for this task because:
- Clear, well-defined scope
- Standard patterns (middleware, sliding window)
- No architectural decisions needed
- No ambiguity in requirements

---

## Risks / Considerations

1. **Thread safety:** FastAPI is async, so we use `asyncio.Lock` (not `threading.Lock`)
2. **Cleanup task lifecycle:** Must handle app shutdown gracefully (cancel cleanup task)
3. **Missing client IP:** Some proxies may not provide `request.client.host` — fallback to "unknown"
4. **Memory bloat:** Cleanup task prevents unbounded growth, but high-traffic scenarios need monitoring
5. **Race conditions:** Lock protects shared state during cleanup and request handling

All of these are addressed in the task file implementation notes.

---

## Ready for Review

The task file is complete and ready for Q33NR review. After approval, I will dispatch the BEE with:

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-14-TASK-085-rate-limiting.md --model haiku --role bee --inject-boot
```

---

**Q33N awaiting Q33NR review and approval to dispatch.**
