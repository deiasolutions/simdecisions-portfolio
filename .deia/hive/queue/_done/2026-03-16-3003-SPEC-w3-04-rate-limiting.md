# SPEC: Rate Limiting on Auth Routes

## Priority
P1

## Objective
Add sliding window rate limiting middleware to all /auth/ routes. Prevent brute force attacks.

## Context
Files to read first:
- `hivenode/routes/auth.py`
- `hivenode/dependencies.py`
- `hivenode/main.py` (middleware setup)

## Acceptance Criteria
- [ ] Sliding window rate limiter: 10 requests per minute per IP on all /auth/ routes
- [ ] Rate limit headers in response: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
- [ ] 429 Too Many Requests response when limit exceeded, with Retry-After header
- [ ] In-memory storage (dict with TTL cleanup) -- no Redis dependency
- [ ] Configurable via environment variable: RATE_LIMIT_AUTH (default 10)
- [ ] Does NOT apply to non-auth routes (other hivenode routes unaffected)
- [ ] 5+ tests: under limit passes, at limit passes, over limit returns 429, different IPs have separate limits, reset after window

## Smoke Test
- [ ] Hit /auth/verify 11 times in 60 seconds -> 11th returns 429

## Model Assignment
haiku
