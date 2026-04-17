# VERIFY: Conversation-Pane End-to-End

## Priority
P1

## Depends On
MW-010

## Objective
Comprehensive verification of conversation-pane: message rendering, LLM routing, streaming responses, output surfaces, error handling, and mobile UX.

## Context
MW-008, MW-009, MW-010 built the conversation-pane stack. This task verifies it works correctly end-to-end with real conversations, edge cases, and mobile interactions.

This is a VERIFY task — focused on testing, not building new features.

Files to verify:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/conversation-pane/ConversationPane.tsx`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/conversation-pane/useLLMRouter.ts`
- All output surface components (CodeBlock, ImageOutput, etc.)

## Acceptance Criteria
- [ ] E2E test: send command → routes to interpreter → executes → result renders
- [ ] E2E test: send question → routes to Claude → streams response → renders incrementally
- [ ] E2E test: send code request → generates code → code block renders with syntax highlighting
- [ ] E2E test: copy code → clipboard contains code
- [ ] E2E test: send message with image response → image renders → tap → lightbox opens
- [ ] E2E test: network error → error message renders → click retry → succeeds
- [ ] Mobile test: conversation scrolls smoothly on mobile viewport
- [ ] Mobile test: code blocks are horizontally scrollable, not cut off
- [ ] Mobile test: action buttons are touch-friendly (min 44px tap target)
- [ ] Performance: streaming response updates <50ms latency per token
- [ ] Integration test file: `browser/src/primitives/conversation-pane/ConversationPane.integration.test.tsx`
- [ ] All integration tests pass

## Smoke Test
- [ ] Run `npm test ConversationPane.integration.test.tsx` — all tests pass
- [ ] Manual test: open conversation-pane → send "What is React?" → response streams in
- [ ] Manual test: send "open terminal" → command executes → result shows
- [ ] Manual test (mobile): scroll conversation → smooth, no jank
- [ ] Manual test: click copy on code block → code in clipboard

## Model Assignment
sonnet

## Constraints
- Location: `browser/src/primitives/conversation-pane/ConversationPane.integration.test.tsx` (new file)
- 10-15 E2E test cases covering full conversation flow
- Max 400 lines for integration tests
- Use real component rendering and HTTP requests (mock LLM responses)
- Test output: clear pass/fail with performance metrics (latency, frame time)
