# SPEC: Conversation-Pane Multi-LLM Routing

## Priority
P1

## Depends On
MW-008

## Objective
Build the LLM routing layer for conversation-pane that routes user messages to appropriate LLM endpoints (Claude, GPT, local, etc.) and handles streaming responses.

## Context
MW-008 built the rendering layer. Now we add the intelligence routing:
- Route commands to command-interpreter (fast, local)
- Route questions to Claude/GPT (slow, remote)
- Route code generation to specialized models
- Stream responses in real-time
- Handle retries, timeouts, errors

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/conversation-pane/ConversationPane.tsx` — rendering layer
- Search for existing LLM integration code (if any)

## Acceptance Criteria
- [ ] `useLLMRouter()` hook in `browser/src/primitives/conversation-pane/useLLMRouter.ts`
- [ ] Hook returns: `{ send, messages, isLoading, error, retry }`
- [ ] `send(message: string, type: 'command' | 'question' | 'code')` method
- [ ] Command type: route to command-interpreter → fast local execution
- [ ] Question type: route to Claude API → streaming response
- [ ] Code type: route to code-specialized model or Claude with code prompt
- [ ] Streaming: update message incrementally as tokens arrive
- [ ] Error handling: network error, API error, timeout → show retry button
- [ ] Retry logic: exponential backoff, max 3 retries
- [ ] Message history: store in React state, persist to localStorage (optional)
- [ ] Backend route: `POST /api/llm/chat` that proxies to LLM providers
- [ ] Unit tests: 10+ tests covering routing, streaming, errors, retries
- [ ] Integration test: send message → stream response → update UI

## Smoke Test
- [ ] Send command "open terminal" → routes to command-interpreter → fast response
- [ ] Send question "What is React?" → routes to Claude → streaming response updates UI
- [ ] Send question with network error → shows error + retry button
- [ ] Click retry → retries request, shows loading state
- [ ] Run `npm test useLLMRouter.test.ts` — all tests pass

## Model Assignment
sonnet

## Constraints
- Location: `browser/src/primitives/conversation-pane/useLLMRouter.ts` (new file)
- Location: `browser/src/primitives/conversation-pane/useLLMRouter.test.ts` (new file)
- Location: `hivenode/routes/llm_routes.py` (new file)
- Location: `hivenode/routes/tests/test_llm_routes.py` (new file)
- TDD: Write tests first
- Use existing HTTP client patterns
- Max 350 lines for hook
- Max 200 lines for hook tests
- Max 300 lines for backend route
- Max 150 lines for backend tests
- NO STUBS — full implementation of streaming and routing
- Use Server-Sent Events (SSE) for streaming responses
