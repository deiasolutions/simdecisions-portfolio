# SPEC: Conversation-Pane Multi-Input Multi-LLM Component

## Priority
P1

## Objective
Design a conversation pane component for the Mobile Workdesk that supports multi-input (voice, text, command) and multi-LLM routing (Claude, Gemini, GPT) with output rendering for code, diffs, images, and terminal output.

## Context
The conversation-pane is the primary interaction surface for the Mobile Workdesk. It must:
- Accept input from multiple sources: voice transcript, typed command, command-interpreter output
- Route requests to different LLM backends based on user preference or task type
- Render diverse output types: markdown, code blocks, diffs, images, terminal streams
- Maintain conversation history with collapsible message threads
- Support mobile gestures: swipe to delete, long-press to copy, pinch to zoom images

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/text-pane/TextPane.tsx` — text rendering patterns
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/terminal/Terminal.tsx` — terminal output handling
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/code-editor/CodeEditor.tsx` — code rendering
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:60` — task context

## Acceptance Criteria
- [ ] `ConversationPane` component with message list rendering
- [ ] Input adapter: accepts `{ source: "voice" | "text" | "command", content: string, llm: "claude" | "gemini" | "gpt" }`
- [ ] Message types: user message, assistant response, system notification, error
- [ ] Output rendering: markdown (with syntax highlighting), code blocks, diff viewer, image viewer, terminal stream
- [ ] LLM routing: configurable backend per message, visual indicator (Claude logo, Gemini logo, GPT logo)
- [ ] Conversation history: scrollable list, auto-scroll to latest, load more (paginated)
- [ ] Mobile gestures: swipe-to-delete message, long-press-to-copy, pinch-to-zoom images
- [ ] Collapsible message threads: long responses collapsible with "Show more" / "Show less"
- [ ] CSS variables only, responsive layout (max-width 800px on tablet)
- [ ] Accessibility: ARIA labels, keyboard navigation, screen reader support
- [ ] 15+ unit tests + 3 E2E tests (voice→response, command→response, multi-LLM conversation)

## Smoke Test
- [ ] Render conversation pane with 10 messages (mixed user/assistant)
- [ ] Send voice input → new user message appears with "voice" indicator
- [ ] Receive assistant response → markdown rendered correctly with Claude logo
- [ ] Swipe message left → delete confirmation appears
- [ ] Long-press message → copy-to-clipboard works
- [ ] Switch LLM to Gemini → next message shows Gemini logo

## Model Assignment
sonnet

## Depends On
None (Phase 0 spec)

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/conversation-pane/ConversationPane.tsx` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/conversation-pane/conversation-pane.css` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/conversation-pane/__tests__/ConversationPane.test.tsx`
- TDD: tests first
- Max 500 lines for component
- Max 150 lines for CSS
- Max 200 lines for tests
- No external markdown libs — use existing text-pane markdown renderer
- No stubs — full rendering pipeline for all output types
