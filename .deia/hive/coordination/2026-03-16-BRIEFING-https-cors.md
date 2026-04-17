# BRIEFING: HTTPS + CORS Configuration

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Regent)
**Date:** 2026-03-16
**Spec:** 2026-03-16-3008-SPEC-w3-09-https-cors.md
**Model:** haiku

---

## Objective

Configure CORS middleware to support all deployed domains and ensure browser→API communication works without CORS errors. Make CORS origins configurable via environment variable for production security.

---

## Context

### Current State

**File:** `hivenode/main.py` (lines 251-266)

Current CORS configuration:
- Hardcoded origins list in main.py
- Missing: `chat.efemera.live`
- Allow methods/headers: `["*"]` (overly permissive)
- Credentials: `True` (correct for JWT cookies)

**File:** `browser/vite.config.ts` (lines 1-15)

No proxy configured. Browser in dev talks to localhost:8420 (CORS allowed via localhost:5173).

### Required Domains

Allowed origins (per spec):
- `http://localhost:5173` (Vite dev)
- `https://dev.shiftcenter.com` (dev frontend)
- `https://code.shiftcenter.com` (code IDE)
- `https://chat.efemera.live` (Efemera chat)

### Security Requirements

1. **No wildcard in production.** Wildcard (`*`) allows any origin — unacceptable for JWT/cookie-based auth.
2. **Specific methods only.** Allow: GET, POST, DELETE, OPTIONS. (No PUT, PATCH unless needed.)
3. **Specific headers only.** Allow: Authorization, Content-Type.
4. **Configurable via env var.** ALLOWED_ORIGINS env var (comma-separated) for production deployments.

### HTTPS

Cloudflare handles SSL for all custom domains:
- `dev.shiftcenter.com` → Vercel
- `code.shiftcenter.com` → Vercel
- `chat.efemera.live` → Vercel
- `api.shiftcenter.com` → Railway (backend)

**No backend code changes needed for HTTPS.** Cloudflare terminates SSL, forwards HTTP to Railway.

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (CORS middleware setup, lines 250-266)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py` (settings pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_health.py` (test pattern with AsyncClient)

---

## Tasks to Create

### TASK-W3-09-A: Add ALLOWED_ORIGINS Config Field

**Objective:** Add `allowed_origins` field to HivenodeConfig with default value.

**Deliverables:**
- Add `allowed_origins: str` field to `HivenodeConfig` class
- Default value: comma-separated string of all required domains
- Parse comma-separated string into list in `_set_defaults()` or property
- Store parsed list as `_allowed_origins_list: list[str]` property

**Test Requirements:**
- Test default value includes all 4 domains
- Test parsing comma-separated env var
- Test empty string defaults to empty list (block all CORS)

**Files:**
- `hivenode/config.py`

### TASK-W3-09-B: Update CORS Middleware to Use Config

**Objective:** Replace hardcoded origins with config-based origins.

**Deliverables:**
- Replace `allow_origins=[...]` with `allow_origins=settings._allowed_origins_list`
- Replace `allow_methods=["*"]` with `allow_methods=["GET", "POST", "DELETE", "OPTIONS"]`
- Replace `allow_headers=["*"]` with `allow_headers=["Authorization", "Content-Type"]`
- Keep `allow_credentials=True`

**Test Requirements:**
- None (covered by TASK-W3-09-C)

**Files:**
- `hivenode/main.py`

### TASK-W3-09-C: Add CORS Tests

**Objective:** Verify CORS behavior for allowed/disallowed origins and preflight OPTIONS.

**Deliverables:**
- Test file: `tests/hivenode/test_cors.py`
- Test 1: Allowed origin (localhost:5173) → response includes `Access-Control-Allow-Origin` header
- Test 2: Disallowed origin (example.com) → response does NOT include `Access-Control-Allow-Origin` header
- Test 3: Preflight OPTIONS request → 200 OK with CORS headers

**Test Requirements:**
- 3+ tests (per spec acceptance criteria)
- Use AsyncClient with custom Origin header
- Test GET /health endpoint (simple, always available)

**Files:**
- `tests/hivenode/test_cors.py` (new file)

---

## Acceptance Criteria (from spec)

- [ ] CORSMiddleware allows: dev.shiftcenter.com, chat.efemera.live, code.shiftcenter.com, localhost:5173
- [ ] Wildcard NOT used in production (security)
- [ ] Allowed methods: GET, POST, DELETE, OPTIONS
- [ ] Allowed headers: Authorization, Content-Type
- [ ] Credentials: true (for JWT cookies if used)
- [ ] CORS origins configurable via ALLOWED_ORIGINS env var (comma-separated)
- [ ] HTTPS verified on all custom domains (Cloudflare handles SSL) — **NO CODE CHANGES NEEDED**
- [ ] 3+ tests: allowed origin passes, disallowed origin blocked, preflight OPTIONS works

---

## Dependencies

Depends on: w3-01-vercel-railway-repoint (domains must be configured before CORS can be tested)

---

## Constraints

- **Rule 3:** No hardcoded colors (N/A — backend only)
- **Rule 4:** No file over 500 lines (N/A — small changes)
- **Rule 5:** TDD (tests first for TASK-W3-09-C)
- **Rule 6:** No stubs

---

## Model Assignment

haiku (simple config + middleware update + tests)

---

## Review Checklist

Before approving task files, verify:

- [ ] All 3 tasks present (config, middleware, tests)
- [ ] Task files specify absolute paths
- [ ] Test requirements specify scenarios (allowed/disallowed/preflight)
- [ ] No wildcard (`*`) in allow_origins
- [ ] ALLOWED_ORIGINS env var documented in task
- [ ] Response file template included in each task

---

## Notes

- **HTTPS is handled by Cloudflare.** No backend code changes needed. Railway receives HTTP from Cloudflare proxy.
- **Vite dev proxy is NOT needed.** Browser at localhost:5173 can call localhost:8420 directly (CORS allows localhost).
- **Smoke test:** Manual verification (not automated). Browser at dev.shiftcenter.com should call api.shiftcenter.com without CORS error after deploy.

---

**Q33N: Read this briefing, read the files listed, write 3 task files, return for Q33NR review.**
