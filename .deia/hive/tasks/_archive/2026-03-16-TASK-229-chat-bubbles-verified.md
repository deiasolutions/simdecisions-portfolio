# TASK-229: Chat Bubbles Verified

## Objective
Verify and fix chat bubble rendering: user messages right-aligned with green avatar, AI messages left-aligned with purple avatar, markdown rendering, copy button on hover, typing indicator with animated dots, avatar initials, and message grouping for consecutive same-sender messages.

## Context

This is Wave 4 Product Polish Task 4.1. The goal is to audit the existing chat rendering system and ensure all visual features work correctly. This is a **verification and fix task**, not a new feature build. The core rendering logic exists — audit every deliverable, fix what's broken, add tests for gaps.

### Source Spec
`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\WAVE-4-PRODUCT-POLISH.md` — Task 4.1

### Current Implementation
- Chat renderer: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\chatRenderer.tsx` (192 lines)
- Chat styles: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\chat-bubbles.css` (150 lines)
- Typing indicator animation: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\sd-editor.css` (lines 508-535)
- Existing tests: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\__tests__\typingIndicator.test.tsx` (93 lines, 6 tests)

### What to Verify
1. **User messages**: Right-aligned with green avatar circle (U letter)
2. **AI messages**: Left-aligned with purple avatar circle (first letter of sender name)
3. **Markdown rendering**: Code blocks, lists, links, bold/italic inside assistant bubbles work correctly
4. **Copy button**: Appears on hover for assistant messages, copies message content when clicked
5. **Typing indicator**: Animated dots with model name (or "Assistant" fallback)
6. **Message grouping**: Consecutive same-sender messages skip avatar/header and align properly

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\chatRenderer.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\chat-bubbles.css`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\__tests__\typingIndicator.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\markdownRenderer.tsx`

## Deliverables

### Code Review & Verification
- [ ] Read all chat rendering code (chatRenderer.tsx, chat-bubbles.css, markdownRenderer.tsx)
- [ ] Verify user messages render right-aligned with green avatar circle
- [ ] Verify AI messages render left-aligned with purple avatar circle
- [ ] Verify markdown renders correctly inside assistant bubbles (test code blocks, lists, links, bold/italic)
- [ ] Verify copy button appears on hover and copies message content
- [ ] Verify typing indicator shows animated dots with model name
- [ ] Verify message grouping: consecutive same-sender messages skip avatar/header
- [ ] Check for any hardcoded colors (Rule 3 violation) — only `var(--sd-*)` allowed

### Fixes
- [ ] Fix any visual issues found during verification
- [ ] Remove any hardcoded colors if found
- [ ] Fix any broken rendering paths

### Tests
- [ ] Review existing test coverage in typingIndicator.test.tsx
- [ ] Add tests for any untested rendering paths:
  - [ ] User message alignment and avatar
  - [ ] AI message alignment and avatar
  - [ ] Markdown rendering in assistant bubbles
  - [ ] Copy button functionality
  - [ ] Message grouping behavior
  - [ ] Error message rendering
- [ ] Ensure all new tests use TDD approach (tests first, then fixes)
- [ ] Run test suite: `cd browser && npx vitest run src/primitives/text-pane/`

## Test Requirements

### Required Test Coverage
Write tests for:
1. User message renders right-aligned with `.sde-chat-bubble-row--user` class
2. User message has green avatar with "U" letter
3. AI message renders left-aligned (no `--user` class on row)
4. AI message has purple avatar with first letter of sender name
5. Error message renders with red avatar and "!" letter
6. Markdown rendering in assistant messages (code blocks, lists, bold/italic)
7. Copy button appears on assistant messages
8. Copy button does NOT appear on user messages
9. Message grouping: second consecutive message from same sender has `.sde-chat-bubble--grouped` class
10. Grouped messages skip avatar rendering
11. Grouped messages indent properly (36px margin)

### Edge Cases
- Empty content
- Content with only whitespace
- Messages without sender prefix
- Multiple consecutive messages from same sender
- Mixed user/AI/error messages

## Constraints

- **Rule 3:** NO HARDCODED COLORS. Only CSS variables (`var(--sd-*)`). No hex, no rgb(), no named colors.
- **Rule 4:** No file over 500 lines. Current files are under the limit. Keep them that way.
- **Rule 5:** TDD — tests first, then implementation.
- **Rule 6:** NO STUBS. Every function fully implemented.

## Acceptance Criteria

- [ ] User messages render right-aligned with green avatar circle (U letter)
- [ ] AI messages render left-aligned with purple avatar circle (first letter of sender)
- [ ] Markdown renders correctly inside assistant bubbles (code blocks, lists, links, bold/italic)
- [ ] Copy button appears on hover and copies message content
- [ ] Typing indicator shows animated dots with model name
- [ ] Message grouping: consecutive same-sender messages skip avatar/header
- [ ] No hardcoded colors remain in code
- [ ] All tests pass: `cd browser && npx vitest run src/primitives/text-pane/`
- [ ] Test coverage added for all untested rendering paths
- [ ] All files remain under 500 lines

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-229-RESPONSE.md`

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

## Priority
P1

## Model
haiku
