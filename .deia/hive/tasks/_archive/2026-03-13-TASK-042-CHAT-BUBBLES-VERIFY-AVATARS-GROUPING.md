# TASK-042: Chat Bubbles Verification, Avatars, and Message Grouping

## Objective
Verify all existing chat bubble features work correctly (fix if broken), then add sender avatars and message grouping to chat bubbles in text-pane.

## Context
BL-010 (chat bubble renderer) was previously shipped. This task has three parts:
1. **Part 1:** Verify all 7 checklist items from BL-010 work correctly. If any are broken, fix them.
2. **Feature 2:** Add sender avatars (CSS-only, no images) to the left of AI bubbles and right of user bubbles.
3. **Feature 3:** Implement message grouping so consecutive same-sender messages share one header.

All work is in `browser/src/primitives/text-pane/`.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\chatRenderer.tsx` (130 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\sd-editor.css` (586 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx` (510 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\markdownRenderer.tsx` (245 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\__tests__\chatRenderer.test.ts` (144 lines, 13 tests)

## Deliverables

### Part 1: Verify Chat Bubbles (Fix if Broken)

Verify every item below works correctly. If any are broken or missing, fix them in the same task.

| # | Feature | Where it should live | Test requirement |
|---|---------|---------------------|------------------|
| 1 | User messages right-aligned with "You" label + timestamp | `chatRenderer.tsx:72-97`, `sd-editor.css:357-441` | Test: user bubble has class `sde-chat-bubble--user`, aligns right, shows "You" |
| 2 | AI messages left-aligned with model name label + timestamp | `chatRenderer.tsx:72-97`, `sd-editor.css:357-441` | Test: assistant bubble has class `sde-chat-bubble--assistant`, aligns left, shows model name |
| 3 | Each message in own frame with rounded corners | `sd-editor.css` `.sde-chat-bubble` | Test: bubbles have 12px border-radius, 12px padding, max-width 85% |
| 4 | Markdown rendered in AI bubbles (headers, code blocks, lists) | `chatRenderer.tsx:75-77` calls `renderMarkdown()` for assistant | Test: assistant message with markdown renders correctly |
| 5 | Copy button per AI message, position: sticky when scrolling | `chatRenderer.tsx:86-94`, `sd-editor.css` `.sde-chat-copy` | **CRITICAL:** Test sticky positioning actually works during scroll |
| 6 | Newest message at bottom, auto-scroll on new message | `chatRenderer.tsx:106-113` | Test: new message triggers scroll to bottom |
| 7 | Scrollable container | `sd-editor.css` `.sde-chat-container` | Test: container has overflow auto, flex column, 12px gap |

**Expected outcome:** All 7 items confirmed working with tests. If copy button sticky positioning is broken, fix it.

### Feature 2: Sender Avatars

**What:** Circle icon to the left of AI bubbles and to the right of user bubbles. CSS-only for MVP (no images).

**Visual spec:**
- 28px circle, `border-radius: 50%`
- AI avatar: first letter of model name, `background: var(--sd-purple-dim)`, `color: var(--sd-text-primary)`
- User avatar: "U" letter, `background: var(--sd-green-dim)`, `color: var(--sd-text-primary)`
- Error avatar: "!" letter, `background: var(--sd-red-dim)`, `color: var(--sd-text-primary)`
- Avatar sits outside the bubble in a flex row: `[avatar] [bubble]` for assistant, `[bubble] [avatar]` for user
- Avatar vertically aligned to top of bubble (flex-start)

**Implementation:**
- [ ] Modify `ChatBubble` component in `chatRenderer.tsx` to render avatar element
- [ ] Avatar letter extracted from `message.sender` (first char) for assistant, "U" for user, "!" for error
- [ ] Wrap bubble + avatar in flex row container
- [ ] Add CSS classes in `sd-editor.css`:
  - `.sde-chat-bubble-row` — flex row wrapper
  - `.sde-chat-avatar` — base avatar styles (28px circle, centered text)
  - `.sde-chat-avatar--user`, `.sde-chat-avatar--assistant`, `.sde-chat-avatar--error` — role-specific colors
- [ ] Avatar vertically aligned to top (align-items: flex-start on row)

### Feature 3: Message Grouping

**What:** Consecutive messages from the same sender share one header. First message shows avatar + name + timestamp. Subsequent messages from same sender show only the bubble (indented to align with first bubble, no repeated avatar/name).

**Logic:**
- Compare `messages[i].sender` with `messages[i-1].sender`
- If same sender: set `grouped: true` on the bubble
- Grouped bubbles: no avatar, no header, reduced top margin (4px instead of 12px)
- Non-grouped bubbles: full header + avatar + standard margin

**Visual spec:**
- Grouped bubble has class `sde-chat-bubble--grouped`
- Left margin matches avatar width + gap (28px + 8px = 36px for assistant, auto + 36px for user)
- Gap between grouped messages: 4px. Gap between different senders: 12px (existing).

**Implementation:**
- [ ] Add grouping logic to `ChatView` component in `chatRenderer.tsx`
- [ ] Pass `isGrouped` prop to `ChatBubble`
- [ ] Conditionally render avatar and header based on `isGrouped`
- [ ] Add CSS class `.sde-chat-bubble--grouped` in `sd-editor.css` with:
  - Margin-top: 4px (instead of default 12px from gap)
  - Margin-left: 36px for assistant (avatar width + gap)
  - Margin-right: 36px for user
- [ ] First message in group: full avatar + header
- [ ] Subsequent messages in group: no avatar, no header, indented

## Test Requirements

Write tests FIRST (TDD).

### Part 1 Verification Tests (7 minimum)
- [ ] User bubble right-aligned with "You" label
- [ ] Assistant bubble left-aligned with model name label
- [ ] Bubbles have correct border-radius and max-width
- [ ] Markdown renders in assistant bubbles
- [ ] Copy button renders for assistant messages
- [ ] **Copy button sticky positioning works** (verify CSS applied correctly)
- [ ] Auto-scroll to newest message works

### Feature 2: Avatar Tests (4 minimum)
- [ ] User avatar renders with "U" and green background
- [ ] Assistant avatar renders with first letter of sender name and purple background
- [ ] Error avatar renders with "!" and red background
- [ ] Avatar letter matches sender name

### Feature 3: Grouping Tests (5 minimum)
- [ ] Single message not grouped (has avatar + header)
- [ ] Consecutive same-sender messages grouped
- [ ] Sender change breaks group (new avatar + header)
- [ ] First in group has avatar + header
- [ ] Grouped messages have no avatar, no header, correct indent

**Total minimum: 16 new tests**

All existing tests in `browser/src/primitives/text-pane/services/__tests__/chatRenderer.test.ts` (13 tests) must continue to pass.

## Constraints
- **CSS:** `var(--sd-*)` only. No hex, no rgb(), no named colors.
- **No file over 500 lines.** `sd-editor.css` is at 586 — if adding styles pushes it over 600, extract chat styles into a separate `chat-bubbles.css` and import it in `sd-editor.css`.
- **TDD.** Tests first for all new features.
- **No stubs.** Every feature fully working.
- **No images for avatars.** CSS-only (letter + background color) for MVP.

## Acceptance Criteria
- [ ] All 7 Part 1 items verified working (tests pass)
- [ ] Copy button sticky positioning verified working
- [ ] Avatars render as CSS circles with correct letters and colors
- [ ] Avatar flex layout: `[avatar][bubble]` for assistant, `[bubble][avatar]` for user
- [ ] Consecutive same-sender messages grouped under one header
- [ ] Grouped messages indented to align with first message bubble
- [ ] All existing chatRenderer tests (13) still pass
- [ ] 16+ new tests passing
- [ ] No file over 600 lines (split `sd-editor.css` if needed)
- [ ] Build passes: `cd browser && npx vitest run`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260313-TASK-042-RESPONSE.md`

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
