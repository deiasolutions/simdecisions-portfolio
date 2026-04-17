# SPEC: BL-027 Rate Limiting on Auth Routes

## Priority
P2

## Objective
Add sliding window rate limiting middleware on /auth/ routes to prevent brute force attacks.

## Context
The ra96it auth service handles JWT verification and user authentication. Auth routes need rate limiting to prevent credential stuffing and brute force attacks.

Files to read first:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` — route registration
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` — FastAPI app setup
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\dependencies.py` — auth dependencies

## Acceptance Criteria
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

## Model Assignment
haiku

## Constraints
- In-memory only — no external dependencies (no Redis, no Memcached)
- Sliding window algorithm, not fixed window (smoother rate limiting)
- Only /auth/ routes are rate limited
- Do NOT modify existing auth logic — add as middleware/dependency
