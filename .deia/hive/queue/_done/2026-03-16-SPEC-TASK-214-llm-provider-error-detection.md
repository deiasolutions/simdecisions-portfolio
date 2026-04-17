# TASK-214: Enhanced Error Detection in LLM Providers

## Objective
Improve error detection and classification in LLM provider implementations (Anthropic, Groq, OpenAI) so that specific error types (auth failure, rate limit, server error) are properly identified and surfaced.

## Context
The terminal's error classifier (TASK-187) needs reliable error information from LLM providers. Currently, providers may wrap errors in generic Error objects, losing status codes and error types. We need to:
- Preserve HTTP status codes in thrown errors
- Include error type/code from provider API responses
- Use consistent error structure across all providers
- Handle network errors distinctly from API errors

This task enhances provider error handling without changing provider interfaces. The error classifier (TASK-187) will use the enhanced error info.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\providers\anthropic.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\providers\groq.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\providers\openai-compatible.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\providers\types.ts`

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\providers\errors.ts`
  - Custom error class `ProviderError extends Error`
  - Properties: `statusCode?: number, errorType?: string, provider: string, originalError?: unknown`
  - Factory functions: `createAuthError()`, `createRateLimitError()`, `createServerError()`, `createNetworkError()`
  - Helper: `isProviderError(error: unknown): error is ProviderError`
- [ ] Update `anthropic.ts` catch blocks to throw ProviderError
  - Parse Anthropic API error responses (error.type, error.message fields)
  - Detect 401 → createAuthError('anthropic', statusCode, message)
  - Detect 429 → createRateLimitError('anthropic', statusCode, message)
  - Detect 500-599 → createServerError('anthropic', statusCode, message)
  - Detect network errors (fetch throws) → createNetworkError('anthropic', originalError)
- [ ] Update `groq.ts` catch blocks to throw ProviderError
  - Parse Groq API error responses (same structure as OpenAI)
  - Apply same status code → error type mapping
- [ ] Update `openai-compatible.ts` catch blocks to throw ProviderError
  - Parse OpenAI API error responses (error.code, error.message fields)
  - Apply same status code → error type mapping
- [ ] Export ProviderError and helpers from `providers/index.ts`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Fetch throws TypeError (network offline) → ProviderError with errorType 'network_error'
  - Response.status = 401 → ProviderError with errorType 'auth_failure', statusCode = 401
  - Response.status = 429 → ProviderError with errorType 'rate_limit', statusCode = 429
  - Response.status = 500 → ProviderError with errorType 'server_error', statusCode = 500
  - Response.status = 503 (service unavailable) → ProviderError with errorType 'server_error'
  - API returns error JSON with error.type field → captured in ProviderError.errorType
  - API returns non-JSON error response → ProviderError with generic message
  - Unknown error object → ProviderError with safe fallback message

## Test Files
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\providers\__tests__\errors.test.ts`
- Update existing provider tests:
  - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\__tests__\providers.test.ts`

Expected test count: **8+ tests** (5+ for ProviderError class/factories, 3+ for provider integration)

## Constraints
- No file over 500 lines
- No stubs
- Must preserve all original error information (don't lose details)
- ProviderError must be serializable (for logging/debugging)
- Don't change provider function signatures (internal implementation only)
- Must handle streaming and non-streaming errors consistently

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-214-RESPONSE.md`

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
