# TASK-085: Rate Limiting on Auth Routes

## Objective

Add sliding window rate limiting middleware on /auth/ routes to prevent brute force attacks and credential stuffing.

## Context

The ra96it auth service handles JWT verification at /auth/verify and /auth/whoami routes. Currently, there is no rate limiting protection, making these endpoints vulnerable to brute force attacks. This task adds a sliding window rate limiter that:

- Limits requests per IP address (not per user, since attackers may not have valid credentials)
- Uses in-memory storage (no Redis dependency) for simplicity and zero external dependencies
- Only applies to /auth/ routes (not /health, /status, or other routes)
- Returns 429 Too Many Requests with Retry-After header when limit exceeded
- Logs RATE_LIMITED events to the Event Ledger for security monitoring

**FastAPI app structure:**
- Main app in `hivenode/main.py` — middleware registered here via `app.add_middleware()`
- Routes registered in `hivenode/routes/__init__.py` via `create_router()`
- Auth routes at `/auth/verify` and `/auth/whoami` in `hivenode/routes/auth.py`
- Dependencies in `hivenode/dependencies.py` (ledger writer, JWT verification)
- Config in `hivenode/config.py` (pydantic-settings, env vars)

**Event Ledger:**
- `LedgerWriter` in `hivenode/ledger/writer.py`
- Method: `write_event(event_type, actor, domain, payload_json)`
- Already injected via `dependencies.get_ledger_writer()`

**Sliding Window Algorithm:**
Track timestamps of requests per IP. On new request:
1. Remove timestamps older than 60 seconds
2. If remaining count >= limit, reject with 429
3. Else, add current timestamp and allow request

**Cleanup Task:**
Run periodic cleanup (every 60s) to remove IPs with no recent requests, preventing memory bloat.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` — FastAPI app setup, middleware registration
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\auth.py` — existing auth routes
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` — settings management
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\writer.py` — event logging
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_auth_routes.py` — existing auth tests (for reference)

## Deliverables

- [ ] **Rate limiter module** at `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\middleware\rate_limiter.py`:
  - `RateLimiterMiddleware` class that implements `BaseHTTPMiddleware`
  - In-memory storage: dict of IP → list of timestamps
  - Sliding window logic: only count requests in last 60 seconds
  - Thread-safe using `asyncio.Lock` (FastAPI is async)
  - Periodic cleanup task (every 60s) to remove stale entries
  - Only rate limit paths starting with `/auth/`
  - Skip `/health`, `/status`, `/` (root)
  - Return 429 with `Retry-After` header (seconds until window resets)
  - Log `RATE_LIMITED` events to Event Ledger

- [ ] **Config addition** in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py`:
  - Add `rate_limit_auth: int = 10` field to `HivenodeConfig` class
  - Env var: `HIVENODE_RATE_LIMIT_AUTH` (defaults to 10 requests/minute)

- [ ] **Middleware registration** in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py`:
  - Import `RateLimiterMiddleware`
  - Add after CORS middleware: `app.add_middleware(RateLimiterMiddleware)`
  - Pass `max_requests=settings.rate_limit_auth` to middleware

- [ ] **Test file** at `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_rate_limiter.py`:
  - 10+ test scenarios (see Test Requirements below)
  - Use `AsyncClient` with `ASGITransport` (same pattern as `test_auth_routes.py`)
  - Use `mock_settings` fixture (already defined in conftest.py)

## Test Requirements

Write tests FIRST (TDD). All tests must pass before implementation is complete.

Test scenarios (minimum 10):

1. **Normal flow:** 10 requests to /auth/verify pass (within limit)
2. **Rate exceeded:** 11th request to /auth/verify gets 429
3. **Retry-After header:** 429 response includes `Retry-After` header with integer seconds
4. **Window reset:** After 60+ seconds, request allowed again
5. **Different IPs:** Two different IPs tracked separately (each gets 10 requests)
6. **Event logging:** RATE_LIMITED event written to ledger with IP and route
7. **Non-auth routes not limited:** 100 requests to /health all pass
8. **Root not limited:** 100 requests to / all pass
9. **Sliding window:** Requests spread over time (not just first 10 in burst)
10. **Cleanup task:** Stale entries removed after 120+ seconds of inactivity
11. **Concurrent requests:** Multiple async requests from same IP handled correctly

Edge cases to cover:
- Missing `client.host` (IP) — should still function (use fallback like "unknown")
- Requests during cleanup task — no race conditions
- Rate limit of 1 (edge case for very restrictive limits)

## Constraints

- **No file over 500 lines** — rate_limiter.py should be ~200-250 lines
- **TDD** — Write tests first, then implementation
- **NO STUBS** — Every function fully implemented
- **In-memory only** — No Redis, no Memcached, no external dependencies
- **Thread-safe** — Use `asyncio.Lock` for shared state (FastAPI is async)
- **No hardcoded values** — Use `settings.rate_limit_auth` from config
- **No modification of existing auth logic** — Add as middleware only
- **Cleanup must not block requests** — Run as background task

## Implementation Notes

### Middleware Structure

```python
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import asyncio
from datetime import datetime, UTC
from typing import Dict, List

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 10, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: Dict[str, List[float]] = {}  # IP → [timestamps]
        self._lock = asyncio.Lock()
        self._cleanup_task = None

    async def dispatch(self, request: Request, call_next):
        # 1. Check if path should be rate limited
        # 2. Get client IP
        # 3. Check if rate limit exceeded
        # 4. If exceeded, return 429 with Retry-After
        # 5. Else, record request and call next
        pass
```

### Sliding Window Logic

```python
async def _is_rate_limited(self, ip: str) -> tuple[bool, int]:
    """Check if IP is rate limited. Returns (is_limited, retry_after_seconds)."""
    async with self._lock:
        now = datetime.now(UTC).timestamp()

        # Get requests for this IP
        if ip not in self._requests:
            self._requests[ip] = []

        # Remove timestamps outside window
        cutoff = now - self.window_seconds
        self._requests[ip] = [ts for ts in self._requests[ip] if ts > cutoff]

        # Check if limit exceeded
        if len(self._requests[ip]) >= self.max_requests:
            # Calculate retry_after (seconds until oldest request expires)
            oldest = min(self._requests[ip])
            retry_after = int(oldest + self.window_seconds - now) + 1
            return True, retry_after

        # Add current timestamp
        self._requests[ip].append(now)
        return False, 0
```

### Cleanup Task

```python
async def _start_cleanup_task(self):
    """Start background cleanup task."""
    self._cleanup_task = asyncio.create_task(self._cleanup_loop())

async def _cleanup_loop(self):
    """Periodically remove stale entries."""
    while True:
        await asyncio.sleep(60)  # Run every 60 seconds
        await self._cleanup()

async def _cleanup(self):
    """Remove IPs with no requests in last 120 seconds."""
    async with self._lock:
        now = datetime.now(UTC).timestamp()
        cutoff = now - (self.window_seconds * 2)  # 120 seconds

        stale_ips = [
            ip for ip, timestamps in self._requests.items()
            if not timestamps or max(timestamps) < cutoff
        ]

        for ip in stale_ips:
            del self._requests[ip]
```

### Event Logging

Log to Event Ledger when rate limit is hit:

```python
from hivenode import dependencies

ledger = dependencies.get_ledger_writer()
ledger.write_event(
    event_type="RATE_LIMITED",
    actor=f"ip:{ip}",
    domain="auth",
    payload_json={
        "route": request.url.path,
        "ip": ip,
        "count": len(self._requests[ip])
    }
)
```

### Middleware Registration (main.py)

```python
from hivenode.middleware.rate_limiter import RateLimiterMiddleware

# After CORS middleware
app.add_middleware(
    RateLimiterMiddleware,
    max_requests=settings.rate_limit_auth
)
```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-085-RESPONSE.md`

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

## Model Assignment

**haiku** — This is a straightforward middleware task with clear requirements and standard patterns.

## Next Steps After Completion

After BEE completes this task:
1. Verify all tests pass
2. Run full test suite to ensure no regressions
3. Archive task file to `.deia/hive/tasks/_archive/`
4. Add to feature inventory: `python _tools/inventory.py add --id BL-027 --title 'Rate Limiting on Auth Routes' --task TASK-085 --layer security --tests 10`
5. Export inventory: `python _tools/inventory.py export-md`

## Security Notes

- This protects against credential stuffing and brute force attacks on auth endpoints
- Rate limiting by IP is not perfect (shared IPs, VPNs) but provides reasonable protection
- For production, consider adding user-level rate limiting after successful auth
- The 10 req/min default is conservative — legitimate users rarely hit this
- Event Ledger logging enables security monitoring and IP blocking policies
