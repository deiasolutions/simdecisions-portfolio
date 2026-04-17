# RESPONSE: TASK-020 — LLM Proxy Route

**Date:** 2026-03-11
**Respondent:** BEE (sonnet) + Q33NR (fixes)
**Status:** COMPLETE

---

## Summary

POST /llm/chat route implemented with BYOK + server Haiku fallback, sliding window rate limiter (120/min per IP), per-call cost tracking emitted to Event Ledger, and stub fallback for missing keys.

## Work Completed

### BEE (Sonnet) — Core Implementation

1. **`hivenode/routes/llm_routes.py`** — POST /llm/chat endpoint:
   - Request/response Pydantic models
   - Rate limit check (429 with retry_after)
   - Key resolution (BYOK → server → none)
   - Model enforcement (server key → Haiku only)
   - Anthropic API call via httpx
   - Cost calculation + ledger emission
   - Graceful no-key response

2. **`hivenode/llm/proxy.py`** — Core proxy logic:
   - `resolve_key()`: BYOK > server > none
   - `enforce_model()`: server key restricts to Haiku
   - `call_anthropic_api()`: httpx async call to Anthropic Messages API
   - `extract_text_content()`: Parse Anthropic response blocks

3. **`hivenode/llm/rate_limit.py`** — Sliding window rate limiter:
   - Thread-safe with threading.Lock
   - 120 req/min per IP (configurable)
   - `check_rate_limit()`, `get_remaining()`, `clear_expired()`

4. **`hivenode/llm/cost.py`** — Cost tracking:
   - Per-model token pricing (Haiku, Sonnet, Opus)
   - Carbon footprint calculation
   - `emit_llm_event()` writes LLM_CALL events to Event Ledger

5. **`hivenode/routes/__init__.py`** — Wired LLM routes at `/llm` prefix

### Q33NR Fixes

6. **`hivenode/llm/proxy.py:105`** — Fixed `await response.json()` → `response.json()` (httpx is sync)
7. **`tests/hivenode/llm/test_llm_routes.py`** — Fixed mock to use sync `.json()` method
8. **`tests/hivenode/llm/test_proxy.py`** — Fixed mock to use sync `.json()` method + MagicMock import
9. **`hivenode/storage/adapters/local.py`** — Fixed stat returning float timestamps → ISO strings (pre-existing bug)
10. **`tests/hivenode/test_storage_routes.py`** — Fixed require_auth test to use cloud mode

## Test Results

- LLM proxy tests: **99/99 PASSING**
- Full hivenode suite: **533/533 PASSING**

## Files Created (BEE)

| File | Description |
|------|-------------|
| `hivenode/routes/llm_routes.py` | POST /llm/chat endpoint |
| `hivenode/llm/proxy.py` | Key resolution, model enforcement, API calls |
| `hivenode/llm/rate_limit.py` | Sliding window rate limiter |
| `hivenode/llm/cost.py` | Cost calculation + ledger emission |
| `tests/hivenode/llm/test_llm_routes.py` | Route integration test |
| `tests/hivenode/llm/test_proxy.py` | Proxy unit tests |
| `tests/hivenode/llm/test_rate_limit.py` | Rate limiter tests |
| `tests/hivenode/llm/test_cost.py` | Cost calculation tests |

## Files Modified (Q33NR)

| File | Change |
|------|--------|
| `hivenode/llm/proxy.py` | Fix await on sync .json() |
| `tests/hivenode/llm/test_llm_routes.py` | Fix mock to sync |
| `tests/hivenode/llm/test_proxy.py` | Fix mock to sync + import |
| `hivenode/storage/adapters/local.py` | Fix stat float→ISO timestamps |
| `tests/hivenode/test_storage_routes.py` | Fix auth test to cloud mode |

## Remaining (Not in Scope)

- Browser Frank service proxy mode wiring (`frankService.ts` line 106) — needs separate task
- 4-level budget hierarchy — Beta
