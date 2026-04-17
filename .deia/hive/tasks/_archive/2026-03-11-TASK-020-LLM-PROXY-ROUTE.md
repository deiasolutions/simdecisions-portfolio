# TASK-020: LLM Proxy Route — POST /llm/chat

**Date:** 2026-03-11
**Priority:** P0 (Alpha blocker)
**Assigned to:** BEE (Sonnet)
**Estimated turns:** 40-60

---

## Objective

Add `POST /llm/chat` route to hivenode that proxies LLM calls from the browser. Two key modes:

1. **BYOK** — browser sends the user's API key in the request. Any model allowed.
2. **Server fallback** — no user key provided. Server uses `ANTHROPIC_API_KEY` env var. **Haiku only.**

This replaces the current browser-direct pattern (CORS issues, key exposure in browser dev tools) with a proper server-side proxy. The browser's Frank service `proxy` routing mode gets wired to call this endpoint.

---

## Architecture

```
Browser (Frank service)
  │
  ├─ direct mode (current): browser → api.anthropic.com (BYOK, x-api-key in browser)
  │
  └─ proxy mode (this task): browser → localhost:8420/llm/chat → api.anthropic.com
                                         ↓
                                  Rate limiter (120 req/min/IP)
                                  Key resolution (user BYOK or server fallback)
                                  Model enforcement (Haiku-only for server key)
                                  Cost tracking → Event Ledger
```

---

## Backend (hivenode)

### New files

| File | Purpose |
|------|---------|
| `hivenode/routes/llm_routes.py` | FastAPI router with `POST /llm/chat` |
| `hivenode/llm/proxy.py` | Anthropic API call logic, key resolution, model enforcement |
| `hivenode/llm/rate_limit.py` | Sliding window rate limiter (port from efemera) |
| `hivenode/llm/cost.py` | Per-call cost calculation, Event Ledger emission |

### Route: `POST /llm/chat`

**Request body:**
```json
{
  "messages": [
    { "role": "user", "content": "Hello" },
    { "role": "assistant", "content": "Hi there" },
    { "role": "user", "content": "How are you?" }
  ],
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 4096,
  "system": "You are Fr@nk, an AI assistant."
}
```

**Request headers:**
- `X-Api-Key: sk-ant-...` — User's BYOK key (optional)
- `Content-Type: application/json`

**Response body (success):**
```json
{
  "content": "I'm doing well! How can I help you?",
  "model": "claude-sonnet-4-5-20250929",
  "usage": {
    "input_tokens": 42,
    "output_tokens": 18
  },
  "cost_usd": 0.000396,
  "duration_ms": 1234,
  "key_source": "byok"
}
```

**Response body (error — no key):**
```json
{
  "error": "no_api_key",
  "message": "No API key available. Add your key in Settings (BYOK) or ask your admin to configure the server key.",
  "key_source": "none"
}
```

**Response body (error — rate limited):**
```json
{
  "error": "rate_limited",
  "message": "Rate limit exceeded. Try again in 12 seconds.",
  "retry_after": 12
}
```

### Key resolution logic

```python
def resolve_key(request_key: str | None) -> tuple[str, str, str]:
    """Returns (api_key, key_source, allowed_model_or_any).

    key_source: 'byok' | 'server' | 'none'
    """
    # 1. Check user-provided key
    if request_key and request_key.strip():
        return (request_key.strip(), 'byok', 'any')

    # 2. Check server fallback
    server_key = os.getenv('ANTHROPIC_API_KEY', '')
    if server_key:
        return (server_key, 'server', 'claude-haiku-4-5-20251001')

    # 3. No key available
    return ('', 'none', '')
```

### Model enforcement

When `key_source == 'server'`:
- Only `claude-haiku-4-5-20251001` is allowed
- If client requests a different model, override to Haiku silently
- Include `"model_override": true` in response when this happens

When `key_source == 'byok'`:
- Any model the user requests is passed through to Anthropic
- No override

### Rate limiter

Port from: `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\rate_limit.py`

Sliding window per IP:
- **Standard rate:** 120 requests per 60 seconds
- Track by `request.client.host` (FastAPI)
- Return HTTP 429 with `Retry-After` header and JSON error body
- Thread-safe (asyncio lock or threading lock)
- In-memory — no database needed for MVP

### Cost tracking → Event Ledger

After each successful LLM call, emit to Event Ledger:

```python
ledger_writer.write_event({
    "kind": "LLM_CALL",
    "provider": "anthropic",
    "model": actual_model_used,
    "input_tokens": usage["input_tokens"],
    "output_tokens": usage["output_tokens"],
    "cost_usd": calculated_cost,
    "duration_ms": elapsed_ms,
    "key_source": key_source,  # 'byok' | 'server'
    "client_ip": client_ip,    # For rate limit auditing
})
```

Cost calculation (from `frankService.ts` TOKEN_RATES — keep in sync):
```python
COST_PER_TOKEN = {
    "claude-haiku-4-5": {"input": 0.25e-6, "output": 1.25e-6},
    "claude-sonnet-4-5": {"input": 3e-6, "output": 15e-6},
    "claude-opus-4-6": {"input": 15e-6, "output": 75e-6},
}
```

### Stub fallback

If `ANTHROPIC_API_KEY` is not set AND user provides no BYOK key:
- Return HTTP 200 with `key_source: "none"` error body (NOT a 500)
- Log a warning: `[llm.proxy] No API key available — returning stub response`
- Do NOT crash the server

### Wire into hivenode router

In `hivenode/routes/__init__.py`, add:
```python
from hivenode.routes import llm_routes
router.include_router(llm_routes.router, prefix="/llm", tags=["llm"])
```

---

## Browser (Frank service)

### Modified files

| File | Change |
|------|--------|
| `browser/src/services/frank/frankService.ts` | Implement `proxy` routing mode (currently throws) |
| `browser/src/services/frank/providers/anthropic.ts` | Fix `getApiKey()` — reads `state.apiKeys.anthropic` not `state.apiKey` |
| `browser/src/primitives/terminal/useTerminal.ts` | Pass `routingMode` to `sendMessage` based on hivenode availability |

### Proxy mode implementation

In `frankService.ts`, replace the `throw new Error('Proxy mode not yet implemented')` block:

```typescript
if (routingMode === 'proxy') {
  const proxyUrl = import.meta.env.VITE_HIVENODE_URL || 'http://localhost:8420';
  const apiKey = getApiKey(/* current provider */);

  const response = await fetch(`${proxyUrl}/llm/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(apiKey ? { 'X-Api-Key': apiKey } : {}),
    },
    body: JSON.stringify({
      messages: history,
      model,
      max_tokens: 4096,
      system: systemPrompt,
    }),
  });

  const data = await response.json();

  if (data.error) {
    throw new Error(data.message);
  }

  return {
    content: data.content,
    metrics: calculateMetrics(data.usage, data.model, data.duration_ms),
  };
}
```

### Routing mode detection

`useTerminal` should detect if hivenode is available:
- Check `VITE_HIVENODE_URL` env var
- Or probe `http://localhost:8420/health` once on mount
- If available → `routingMode: 'proxy'`
- If not → `routingMode: 'direct'` (existing BYOK browser-direct path)

---

## Reference code (port from)

| Source | File | What to port |
|--------|------|-------------|
| simdecisions-2 | `api/tasks.py:340-357` | User key vs server key fallback pattern |
| simdecisions-2 | `api/tasks.py:103-201` | `call_anthropic_api()` — HTTP call to Anthropic |
| efemera | `rate_limit.py` | `_SlidingWindow` class, middleware pattern |
| efemera | `oracle/llm_provider.py:55-60` | `_estimate_cost()` function |

---

## Tests

### New test files

| File | Tests |
|------|-------|
| `tests/hivenode/test_llm_proxy.py` | Key resolution (BYOK, server, none), model enforcement, response parsing |
| `tests/hivenode/test_llm_rate_limit.py` | Sliding window logic, 120/min enforcement, thread safety |
| `tests/hivenode/test_llm_cost.py` | Cost calculation accuracy for each model tier |
| `tests/hivenode/test_llm_routes.py` | Full route integration (mock Anthropic API) |

### Test scenarios

1. BYOK key → passes to Anthropic, any model allowed
2. No user key, server key set → Haiku only, model overridden silently
3. No user key, no server key → stub error response, HTTP 200
4. Rate limit at 120 → 121st request returns 429
5. Cost calculation matches browser-side `TOKEN_RATES`
6. Event Ledger entry emitted after successful call
7. Malformed request body → 422 validation error
8. Anthropic API error → forwarded as error response (not 500)

---

## Acceptance Criteria

- [ ] `POST /llm/chat` responds correctly with BYOK key
- [ ] Server fallback uses Haiku only, overrides model silently
- [ ] No key available → graceful error response (not crash)
- [ ] Rate limiter enforces 120 req/min per IP
- [ ] Rate limit exceeded → HTTP 429 with `retry_after`
- [ ] Each LLM call emits `LLM_CALL` event to Event Ledger
- [ ] Cost tracking matches `frankService.ts` TOKEN_RATES
- [ ] Browser `proxy` mode calls `/llm/chat` and works end-to-end
- [ ] `anthropic.ts:getApiKey()` bug fixed (`apiKey` → `apiKeys.anthropic`)
- [ ] All tests pass
- [ ] `python -m hivenode` starts and `/llm/chat` is reachable

---

## NOT in scope (deferred)

- Full 4-level budget hierarchy (task/entity/domain/hive) — Beta
- Key encryption (Fernet) — needs ra96it integration
- Multi-provider proxy (Groq, OpenAI) — Anthropic only for Alpha
- Streaming responses — batch only for now
- WebSocket relay — HTTP only
- Chat persistence to hivenode storage (separate TASK-021)

---

## Dependencies

- **hivenode TASK-019** (FastAPI server) — DONE
- **hivenode BE-001** (Event Ledger) — DONE
- **browser TASK-012** (Frank service) — DONE
- **browser TASK-018** (BYOK settings UI) — DONE
- **Q33NR-DIRECT BYOK wiring fix** — DONE (this session)
