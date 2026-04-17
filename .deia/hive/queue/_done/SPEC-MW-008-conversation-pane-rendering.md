# SPEC: Conversation-Pane Multi-Input Rendering

## Priority
P1

## Depends On
MW-T04, MW-V01

## Objective
Build the conversation-pane primitive that renders multi-turn conversations with support for text, voice, code, images, and interactive command confirmations.

## Context
The conversation-pane is a new primitive for Mobile Workdesk that displays conversational UI:
- User messages (text or voice transcript)
- Assistant responses (text, code blocks, images)
- Command confirmations ("Did you mean X?")
- Disambiguation pickers (list of alternatives)
- Loading states, error states, retry actions

This task builds the rendering layer. MW-009 will add LLM routing, MW-010 will add output surfaces.

Files to read first:
- Search for existing conversation or chat components (if any)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/` — primitive patterns

## Acceptance Criteria
- [ ] `ConversationPane.tsx` component in `browser/src/primitives/conversation-pane/`
- [ ] Message types: `user-text`, `user-voice`, `assistant-text`, `command-confirm`, `command-disambiguate`, `error`, `loading`
- [ ] Message list with auto-scroll to latest message
- [ ] User message: bubble on right, text content, timestamp
- [ ] Assistant message: bubble on left, markdown rendering, code syntax highlighting
- [ ] Command confirm message: "Did you mean X?" with Yes/No buttons
- [ ] Command disambiguate message: list of alternatives with tap-to-select
- [ ] Loading message: typing indicator (animated dots)
- [ ] Error message: red border, error icon, retry button
- [ ] Markdown rendering: use existing markdown renderer or build minimal one
- [ ] Code syntax highlighting: use existing highlighter or Prism.js
- [ ] Mobile-optimized: touch-friendly buttons, readable font sizes, proper spacing
- [ ] Component tests: 15+ tests covering all message types, interactions, edge cases

## Smoke Test
- [ ] Render `<ConversationPane messages={[...]} />` — messages display correctly
- [ ] Render user text message → shows on right
- [ ] Render assistant message with code block → syntax highlighting works
- [ ] Render command confirm message → Yes/No buttons render
- [ ] Render loading message → typing indicator animates
- [ ] Run `npm test ConversationPane.test.tsx` — all tests pass

## Model Assignment
sonnet

## Constraints
- Location: `browser/src/primitives/conversation-pane/ConversationPane.tsx` (new file)
- Location: `browser/src/primitives/conversation-pane/ConversationPane.test.tsx` (new file)
- Location: `browser/src/primitives/conversation-pane/ConversationPane.css` (new file)
- Location: `browser/src/primitives/conversation-pane/types.ts` (message type definitions)
- TDD: Write tests first
- CSS variables only
- Max 400 lines for component
- Max 250 lines for tests
- Max 200 lines for CSS
- NO STUBS — full rendering of all message types
- Use existing markdown/code highlighter if available
