# BRIEFING: Rate Limiting on Auth Routes

**From:** Q33NR (Regent)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-16
**Spec:** `.deia/hive/queue/2026-03-16-3003-SPEC-w3-04-rate-limiting.md`

---

## Situation

Spec requests rate limiting on /auth/ routes with:
- Sliding window (10 req/min per IP)
- Rate limit headers in responses
- 429 with Retry-After when exceeded
- In-memory storage (no Redis)
- Configurable via RATE_LIMIT_AUTH env var
- Only applies to /auth/ routes
- 5+ tests

## Current State

**ALREADY IMPLEMENTED:**
- ✅ `hivenode/middleware/rate_limiter.py` - Full sliding window rate limiter
- ✅ Applied to auth routes only (`_should_rate_limit()` checks `/auth/` prefix)
- ✅ 429 response with `Retry-After` header
- ✅ In-memory storage with TTL cleanup loop (dict with periodic cleanup)
- ✅ Configurable via `settings.rate_limit_auth` (env: `HIVENODE_RATE_LIMIT_AUTH`, default 10)
- ✅ Registered in `hivenode/main.py` line 269-272
- ✅ Config loaded in `hivenode/config.py` line 55 (`rate_limit_auth: int = 10`)
- ✅ **9 comprehensive tests** in `tests/hivenode/test_rate_limiter.py`:
  - Within limit passes
  - At limit passes
  - Over limit returns 429
  - 429 includes Retry-After header
  - Window reset after 60 seconds
  - Different IPs tracked separately
  - Non-auth routes not limited
  - Root route not limited
  - Sliding window (not just burst)

**MISSING:**
- ❌ Rate limit headers in **successful responses**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

The spec acceptance criteria says "Rate limit headers in response" but the implementation only adds `Retry-After` on 429 responses. Industry standard is to include rate limit headers in all successful responses too.

## Task

Create one task to add the missing headers:
- Add `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` to successful responses from /auth/ routes
- Only add to successful responses (200-299), not 429 (which already has Retry-After)
- Calculate `X-RateLimit-Reset` as Unix timestamp when oldest request in window expires
- TDD: Write test first to verify headers present in successful response
- Run existing 9 tests to ensure no regression

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\middleware\rate_limiter.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_rate_limiter.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` (lines 54-56)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (lines 268-272)

## Model Assignment

haiku (small enhancement to existing middleware)

## Acceptance Criteria (from spec)

- [x] Sliding window rate limiter: 10 requests per minute per IP on all /auth/ routes
- [ ] Rate limit headers in response: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset (MISSING)
- [x] 429 Too Many Requests response when limit exceeded, with Retry-After header
- [x] In-memory storage (dict with TTL cleanup) -- no Redis dependency
- [x] Configurable via environment variable: RATE_LIMIT_AUTH (default 10)
- [x] Does NOT apply to non-auth routes (other hivenode routes unaffected)
- [x] 5+ tests: under limit passes, at limit passes, over limit returns 429, different IPs have separate limits, reset after window (HAVE 9 TESTS)

## Notes

- Most of the spec is already done. This is a small enhancement.
- The existing implementation is production-quality (cleanup loop, async locks, ledger logging).
- Just need to add 3 headers to successful responses.
- Smoke test in spec: "Hit /auth/verify 11 times in 60 seconds -> 11th returns 429" — this already works.
