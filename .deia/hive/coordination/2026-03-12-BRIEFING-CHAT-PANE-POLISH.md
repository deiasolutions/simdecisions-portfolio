# BRIEFING: Chat Pane Polish

**Date:** 2026-03-12
**From:** Q33NR
**To:** Q33N
**Model:** Sonnet (for task file authoring)
**Bee model:** Sonnet (these tasks touch rendering logic + bus protocol + new components)

---

## Objective

Two-part sprint. Part 1 verifies and fixes existing chat bubble rendering (BL-010, already built). Part 2 adds four new features: typing indicator, sender avatars, message grouping, and attachment button.

All work is in `browser/src/primitives/text-pane/` and `browser/src/primitives/terminal/`.

---

## Part 1 — Verify Chat Bubbles (Fix if Broken)

BL-010 (chat bubble renderer) was shipped. Q33N must write a task that verifies every item below works correctly. If any are broken or missing, the bee fixes them in the same task.

### Checklist

| # | Feature | Where it should live | Current state |
|---|---------|---------------------|---------------|
| 1 | User messages right-aligned with "You" label + timestamp | `chatRenderer.tsx:72-97`, `sd-editor.css:357-441` | BUILT — `.sde-chat-bubble--user` is right-aligned, sender label shows "You", timestamp renders when present |
| 2 | AI messages left-aligned with model name label + timestamp | `chatRenderer.tsx:72-97`, `sd-editor.css:357-441` | BUILT — `.sde-chat-bubble--assistant` is left-aligned, sender label shows model name |
| 3 | Each message in own frame with rounded corners | `sd-editor.css` `.sde-chat-bubble` | BUILT — 12px border-radius, 12px padding, max-width 85% |
| 4 | Markdown rendered in AI bubbles (headers, code blocks, lists) | `chatRenderer.tsx:75-77` calls `renderMarkdown()` for assistant, `parseInline()` for user | BUILT — `markdownRenderer.tsx` (245 lines) handles headings, code blocks, lists, inline formatting |
| 5 | Copy button per AI message, position: sticky when scrolling | `chatRenderer.tsx:86-94`, `sd-editor.css` `.sde-chat-copy` | BUILT — button renders for non-user messages. **VERIFY sticky positioning actually works during scroll** |
| 6 | Newest message at bottom, auto-scroll on new message | `chatRenderer.tsx:106-113` | BUILT — `scrollIntoView({ behavior: 'smooth' })` on content change via `useEffect` |
| 7 | Scrollable container | `sd-editor.css` `.sde-chat-container` | BUILT — flex column, overflow auto, 12px gap |

**Expected outcome:** All 7 items confirmed working with tests. If copy button sticky positioning is broken, fix it.

---

## Part 2 — Four New Features

### Feature 1: Typing Indicator

**What:** "Claude is thinking..." with animated dots appears in the chat view while waiting for LLM response. Disappears when response arrives.

**Architecture:**
- Terminal (`useTerminal.ts`) already tracks `loading` state (set to `true` during LLM call)
- Terminal must send **new bus messages** when loading state changes:
  - `terminal:typing-start` — sent when LLM call begins (before fetch)
  - `terminal:typing-end` — sent when LLM response is complete or errors
- `SDEditor.tsx` subscribes to these messages and passes a `typing` boolean to `ChatView`
- `ChatView` renders a typing indicator bubble at the bottom (before the scroll anchor)

**Visual spec:**
- Bubble styled like assistant bubble but with `sde-chat-bubble--typing` class
- Content: model name + "is thinking" + animated dots (CSS `@keyframes`)
- Three dots that fade in/out sequentially (pure CSS animation, no JS interval)
- Indicator disappears immediately when `terminal:typing-end` received

**Files to modify:**
- `browser/src/primitives/terminal/useTerminal.ts` — emit typing bus messages
- `browser/src/primitives/text-pane/SDEditor.tsx` — subscribe to typing messages, pass to ChatView
- `browser/src/primitives/text-pane/services/chatRenderer.tsx` — render typing indicator
- `browser/src/primitives/text-pane/sd-editor.css` — typing bubble + dot animation styles

### Feature 2: Sender Avatars

**What:** Circle icon to the left of AI bubbles and to the right of user bubbles. CSS-only for MVP (no images).

**Visual spec:**
- 28px circle, `border-radius: 50%`
- AI avatar: first letter of model name, `background: var(--sd-purple-dim)`, `color: var(--sd-text-primary)`
- User avatar: "U" letter, `background: var(--sd-green-dim)`, `color: var(--sd-text-primary)`
- Error avatar: "!" letter, `background: var(--sd-red-dim)`, `color: var(--sd-text-primary)`
- Avatar sits outside the bubble in a flex row: `[avatar] [bubble]` for assistant, `[bubble] [avatar]` for user
- Avatar vertically aligned to top of bubble (flex-start)

**Files to modify:**
- `browser/src/primitives/text-pane/services/chatRenderer.tsx` — add avatar element to ChatBubble
- `browser/src/primitives/text-pane/sd-editor.css` — avatar styles, flex row wrapper

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

**Files to modify:**
- `browser/src/primitives/text-pane/services/chatRenderer.tsx` — grouping logic in ChatView, pass `isGrouped` prop to ChatBubble
- `browser/src/primitives/text-pane/sd-editor.css` — grouped bubble styles

### Feature 4: Attachment Button

**What:** File picker icon in the terminal input area. User clicks, selects a file, filename displayed as a chip above the input. File content included as context in next LLM message.

**Architecture:**
- Add a hidden `<input type="file">` and a clickable icon button next to the terminal input
- On file selection: read file as text via `FileReader`, store in state
- Display filename as a removable chip/tag above the input textarea
- Chip shows filename + "x" button to remove attachment
- When user sends a message with an attachment: prepend file content to the prompt as a fenced code block: `` ```filename\n{content}\n``` ``
- Clear attachment state after sending
- Max file size: 100KB (show error chip if exceeded)
- Accept: `.txt`, `.md`, `.json`, `.py`, `.ts`, `.tsx`, `.js`, `.jsx`, `.css`, `.yml`, `.yaml`, `.toml`, `.csv` (text files only)

**Visual spec:**
- Icon button: paperclip or document icon (Unicode character, not an image). Positioned left of the input area.
- Chip: `background: var(--sd-surface-alt)`, `border: 1px solid var(--sd-border)`, `border-radius: 12px`, `padding: 2px 8px`, `font-size: var(--sd-font-xs)`
- Chip "x" button: `color: var(--sd-text-muted)`, hover `color: var(--sd-red)`

**Files to modify:**
- `browser/src/primitives/terminal/useTerminal.ts` — attachment state, prepend to prompt
- `browser/src/primitives/terminal/TerminalApp.tsx` — render file input, icon button, chip
- `browser/src/primitives/terminal/terminal.css` — attachment button, chip styles
- `browser/src/primitives/terminal/types.ts` — add attachment type if needed

---

## Task Decomposition Guidance

Q33N should split this into **two tasks**:

| Task | Scope | Dependencies |
|------|-------|-------------|
| TASK-042 | Part 1 (verify/fix chat bubbles) + Feature 2 (avatars) + Feature 3 (grouping) | None — all in text-pane |
| TASK-043 | Feature 1 (typing indicator) + Feature 4 (attachment button) | None — typing touches both terminal + text-pane, attachment is terminal-only |

Both tasks are independent and can be dispatched in parallel. They touch overlapping files (`chatRenderer.tsx`, `sd-editor.css`) but in non-conflicting areas: TASK-042 modifies ChatBubble structure and adds grouping logic, TASK-043 adds the typing indicator below the message list and the attachment UI in terminal.

**If Q33N prefers a different split, that's fine — but no more than 3 tasks total for this work.**

---

## Files Reference (Read Before Writing Tasks)

### Text-pane (chat rendering)
- `browser/src/primitives/text-pane/services/chatRenderer.tsx` (130 lines) — ChatBubble, ChatView, parseChatMessages
- `browser/src/primitives/text-pane/services/markdownRenderer.tsx` (245 lines) — renderMarkdown, parseInline
- `browser/src/primitives/text-pane/SDEditor.tsx` (510 lines) — main editor, bus subscription, chat mode routing
- `browser/src/primitives/text-pane/sd-editor.css` (586 lines) — all chat bubble styles at lines 357-441
- `browser/src/primitives/text-pane/types.ts` (61 lines) — SDEditorProps, PaneContext

### Terminal (input + bus)
- `browser/src/primitives/terminal/useTerminal.ts` (588 lines) — terminal hook, chat mode at lines 354-471, loading state
- `browser/src/primitives/terminal/TerminalApp.tsx` (176 lines) — terminal layout, prompt area
- `browser/src/primitives/terminal/terminal.css` (451 lines) — terminal styles
- `browser/src/primitives/terminal/types.ts` (117 lines) — TerminalEntry, TerminalEggConfig

### Existing tests (bees must not break these)
- `browser/src/primitives/text-pane/services/__tests__/chatRenderer.test.ts` (144 lines, 13 tests)
- `browser/src/primitives/text-pane/services/__tests__/markdownRenderer.test.tsx` (239 lines, 30+ tests)
- `browser/src/primitives/text-pane/services/__tests__/codeRenderer.test.tsx` (100 lines, 10 tests)
- `browser/src/primitives/terminal/__tests__/TerminalOutput.test.tsx` (430 lines, 16 tests)

### Adapters (read-only context for bees)
- `browser/src/apps/textPaneAdapter.tsx` (38 lines) — passes renderMode to SDEditor
- `browser/src/apps/terminalAdapter.tsx` (86 lines) — passes bus + egg config to TerminalApp

---

## Constraints

- **CSS:** `var(--sd-*)` only. No hex, no rgb(), no named colors.
- **No file over 500 lines.** `sd-editor.css` is at 586 — if adding styles pushes it further, extract chat styles into a separate `chat-bubbles.css` and import it.
- **TDD.** Tests first for all new features. Existing 69+ browser tests in these files must not regress.
- **No stubs.** Every feature fully working.
- **No images for avatars.** CSS-only (letter + background color) for MVP.
- **No external dependencies.** Pure CSS animations for typing dots. `FileReader` API for attachment (built-in).

---

## Test Requirements per Feature

| Feature | Minimum tests |
|---------|--------------|
| Part 1 verify | 7 (one per checklist item — can be lightweight if already covered) |
| Typing indicator | 5 (bus message emission, indicator appears, indicator disappears, error case clears, no indicator when not in chat mode) |
| Avatars | 4 (user avatar renders, assistant avatar renders, error avatar renders, avatar letter matches sender) |
| Message grouping | 5 (single message not grouped, consecutive same-sender grouped, sender change breaks group, first in group has header, grouped has no header) |
| Attachment | 6 (file picker opens, filename chip renders, chip removable, content prepended to prompt, file cleared after send, oversized file rejected) |
| **Total minimum** | **27 new tests** |

---

## Success Criteria

1. All 7 Part 1 items verified working
2. Typing indicator visible during LLM call, gone when response arrives
3. Avatars render as CSS circles with correct letters and colors
4. Consecutive same-sender messages grouped under one header
5. File attachment works: pick file, see chip, send message with content, chip cleared
6. All existing tests still pass (`npx vitest run`)
7. No file over 500 lines (split `sd-editor.css` if needed)
8. 27+ new tests passing

---

**End of briefing. Q33N: read the files listed above, then write task files and return for review.**
