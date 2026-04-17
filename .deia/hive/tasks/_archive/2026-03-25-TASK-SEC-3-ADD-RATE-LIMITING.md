# TASK-SEC-3: Add Rate Limiting to LLM Routes

## Objective
Install `slowapi` and add rate limiting to LLM-facing routes to prevent abuse.

## Context
Currently there is no rate limiting on LLM routes. This task adds basic rate limiting (10 requests/minute) using `slowapi` library to protect against abuse.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\llm_routes.py` (if it exists)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\pyproject.toml`

## Deliverables
- [ ] Add `slowapi>=0.1.9` to `pyproject.toml` dependencies
- [ ] In `hivenode/main.py`, add limiter setup:
  ```python
  from slowapi import Limiter
  from slowapi.util import get_remote_address
  from slowapi.errors import RateLimitExceeded
  from starlette.responses import JSONResponse

  limiter = Limiter(key_func=get_remote_address)
  app.state.limiter = limiter

  @app.exception_handler(RateLimitExceeded)
  async def rate_limit_handler(request, exc):
      return JSONResponse(status_code=429, content={"error": "Too many requests"})
  ```
- [ ] Find all LLM-facing routes in `hivenode/routes/` (routes that call LLM APIs or accept chat messages)
- [ ] Apply `@limiter.limit("10/minute")` decorator to those routes
- [ ] Write tests verifying rate limiting works (11th request within 1 minute returns 429)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test: First 10 requests succeed
- [ ] Test: 11th request within 1 minute returns 429 with "Too many requests"
- [ ] Test: After 1 minute window, requests succeed again
- [ ] All existing tests still pass

## Constraints
- No file over 500 lines
- No stubs
- TDD — tests first
- Do NOT add rate limiting to health check or internal routes

## Model
Sonnet (requires finding LLM routes and careful integration)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260325-TASK-SEC-3-RESPONSE.md`

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
