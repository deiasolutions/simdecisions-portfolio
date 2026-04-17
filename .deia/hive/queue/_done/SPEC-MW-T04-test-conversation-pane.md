# SPEC: TEST — Conversation-Pane Component Coverage

## Priority
P1

## Objective
Write comprehensive test suite for the ConversationPane component that validates message rendering, input adapters, output types, mobile gestures, and LLM routing with 100% coverage.

## Context
This is a TDD task — write tests FIRST, before implementation exists. Tests must fail initially, then pass after MW-008/MW-009/MW-010 implementation.

Test coverage must include:
- Component render: message list displays correctly
- Input adapters: voice, text, command inputs handled
- Message types: user, assistant, system, error
- Output rendering: markdown, code blocks, diffs, images, terminal streams
- LLM routing: Claude, Gemini, GPT logos displayed
- Mobile gestures: swipe-to-delete, long-press-to-copy, pinch-to-zoom
- Collapsible threads: long messages collapsed/expanded
- Accessibility: ARIA labels, keyboard navigation

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-S04-conversation-pane.md` — spec to test against
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/text-pane/__tests__/TextPane.test.tsx` — test patterns
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:72` — task context

## Acceptance Criteria
- [ ] Test file: `browser/src/primitives/conversation-pane/__tests__/ConversationPane.test.tsx` (Jest + React Testing Library)
- [ ] 15+ test cases covering: render, inputs, outputs, gestures, LLM routing, a11y
- [ ] Test render: message list with 10 messages displays
- [ ] Test voice input: message with source="voice" shows voice indicator
- [ ] Test text input: message with source="text" shows text indicator
- [ ] Test markdown rendering: markdown content rendered correctly (headers, lists, code)
- [ ] Test code blocks: syntax highlighted code displayed
- [ ] Test LLM logos: Claude message shows Claude logo, Gemini shows Gemini logo
- [ ] Test swipe-to-delete: swipe gesture triggers delete confirmation
- [ ] Test long-press-to-copy: long press triggers copy-to-clipboard
- [ ] Test collapsible: long message shows "Show more" button, expands on click
- [ ] Test accessibility: ARIA labels for messages, keyboard navigation
- [ ] Tests initially FAIL (no implementation exists yet)
- [ ] All tests use screen.getByRole, screen.getByText for queries
- [ ] No stubs in tests — real assertions with expected values

## Smoke Test
- [ ] Run `npm test ConversationPane.test.tsx` → 15+ tests FAIL (component doesn't exist yet)
- [ ] Check test_render() → asserts 10 messages displayed
- [ ] Check test_voice_input() → asserts voice indicator present
- [ ] Check test_markdown() → asserts heading rendered from markdown
- [ ] Check test_swipe_delete() → asserts delete confirmation shown
- [ ] All tests use descriptive names (it("should ..."))

## Model Assignment
sonnet

## Depends On
MW-S04

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/conversation-pane/__tests__/ConversationPane.test.tsx` (new file)
- TDD: tests MUST be written before implementation (they will fail initially)
- Max 350 lines for test file
- Use @testing-library/react for component testing
- Use fireEvent for gesture simulation (touchstart, touchmove, touchend)
- No implementation code in this task — tests only
- Tests must be runnable even if `ConversationPane.tsx` doesn't exist yet (import should handle missing module gracefully)
