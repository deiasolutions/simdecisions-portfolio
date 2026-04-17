# TASK-229: Chat Bubbles Verified (W4 — 4.1)

## Objective
Verify and fix the chat bubble rendering: user messages right-aligned, AI messages left-aligned, markdown rendering, copy button, typing indicator, avatar initials, message grouping.

## Context
Wave 4 Product Polish. Chat must look like a real product. The core rendering exists in `chatRenderer.tsx` with `chat-bubbles.css`. This task is verification — audit every feature, fix anything broken, add tests for gaps.

## Source Spec
`docs/specs/WAVE-4-PRODUCT-POLISH.md` — Task 4.1

## Files to Read First
- `browser/src/primitives/text-pane/services/chatRenderer.tsx` — Chat bubble rendering (192 lines)
- `browser/src/primitives/text-pane/chat-bubbles.css` — Chat bubble styles (150 lines)
- `browser/src/primitives/text-pane/services/__tests__/typingIndicator.test.tsx` — Typing indicator tests

## Deliverables
- [ ] Verify user messages render right-aligned with green avatar circle
- [ ] Verify AI messages render left-aligned with purple avatar circle
- [ ] Verify markdown renders correctly inside assistant bubbles (code blocks, lists, links, bold/italic)
- [ ] Verify copy button appears on hover and copies message content
- [ ] Verify typing indicator shows animated dots with model name
- [ ] Verify message grouping: consecutive same-sender messages skip avatar/header
- [ ] Fix any visual issues found during verification
- [ ] Add tests for any untested rendering paths
- [ ] Run: `cd browser && npx vitest run src/primitives/text-pane/`

## Priority
P1

## Model
haiku
