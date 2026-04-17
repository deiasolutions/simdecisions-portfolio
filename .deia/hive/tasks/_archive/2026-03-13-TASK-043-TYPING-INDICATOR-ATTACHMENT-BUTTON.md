# TASK-043: Typing Indicator and Attachment Button

## Objective
Add typing indicator to chat view (appears during LLM calls) and file attachment button to terminal input (allows users to attach text files as context).

## Context
Two new features for the chat system:
1. **Feature 1 (Typing Indicator):** "Claude is thinking..." with animated dots appears in chat view while waiting for LLM response. Terminal emits new bus messages when loading state changes.
2. **Feature 4 (Attachment Button):** File picker icon in terminal input area. User selects a text file, filename displayed as a chip, file content prepended to LLM prompt.

Work touches both terminal (`browser/src/primitives/terminal/`) and text-pane (`browser/src/primitives/text-pane/`).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (588 lines) — terminal hook, loading state at line 82
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalApp.tsx` (176 lines) — terminal layout, prompt area
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\terminal.css` (451 lines) — terminal styles
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\types.ts` (117 lines) — TerminalEntry, TerminalEggConfig
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx` (510 lines) — bus subscription
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\chatRenderer.tsx` (130 lines) — ChatView component
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\sd-editor.css` (586 lines) — chat styles

## Deliverables

### Feature 1: Typing Indicator

**What:** "Claude is thinking..." with animated dots appears in the chat view while waiting for LLM response. Disappears when response arrives.

**Architecture:**
- Terminal (`useTerminal.ts`) already tracks `loading` state (set to `true` during LLM call at line 82)
- Terminal must send **new bus messages** when loading state changes:
  - `terminal:typing-start` — sent when LLM call begins (before fetch)
  - `terminal:typing-end` — sent when LLM response is complete or errors
- `SDEditor.tsx` subscribes to these messages and passes a `typing` boolean to `ChatView`
- `ChatView` renders a typing indicator bubble at the bottom (before the scroll anchor)

**Visual spec:**
- Bubble styled like assistant bubble but with `sde-chat-bubble--typing` class
- Content: model name + " is thinking" + animated dots (CSS `@keyframes`)
- Three dots that fade in/out sequentially (pure CSS animation, no JS interval)
- Indicator disappears immediately when `terminal:typing-end` received

**Implementation:**
- [ ] Modify `useTerminal.ts` `handleSubmit()` function:
  - Send `terminal:typing-start` bus message when `setLoading(true)` (line 379)
  - Send `terminal:typing-end` bus message when `setLoading(false)` (line 492)
  - Include model name in typing-start message data
  - Send typing-end in both success and error paths
- [ ] Modify `SDEditor.tsx` bus subscription (line 250):
  - Subscribe to `terminal:typing-start` and `terminal:typing-end`
  - Add state: `const [isTyping, setIsTyping] = useState(false)`
  - Add state: `const [typingModel, setTypingModel] = useState<string | null>(null)`
  - Set `isTyping` true on typing-start, false on typing-end
  - Pass `typing={isTyping}` and `typingModel={typingModel}` to `ChatView` (line 401)
- [ ] Modify `chatRenderer.tsx` `ChatView` component:
  - Accept `typing?: boolean` and `typingModel?: string | null` props
  - Render typing indicator bubble before `<div ref={endRef} />` when `typing` is true
  - Typing bubble content: `{typingModel || 'Assistant'} is thinking...`
  - Three animated dots rendered after "thinking" text
- [ ] Add CSS in `sd-editor.css`:
  - `.sde-chat-bubble--typing` — base typing bubble styles (like assistant bubble)
  - `.sde-typing-dots` — container for three dots
  - `.sde-typing-dot` — individual dot (inline-block, 4px circle)
  - `@keyframes sde-typing-dot-pulse` — fade in/out animation
  - Stagger animation delays: dot 1 (0s), dot 2 (0.3s), dot 3 (0.6s)

### Feature 4: Attachment Button

**What:** File picker icon in the terminal input area. User clicks, selects a file, filename displayed as a chip above the input. File content included as context in next LLM message.

**Architecture:**
- Add a hidden `<input type="file">` and a clickable icon button next to the terminal input
- On file selection: read file as text via `FileReader`, store in state
- Display filename as a removable chip/tag above the input textarea
- Chip shows filename + "x" button to remove attachment
- When user sends a message with an attachment: prepend file content to the prompt as a fenced code block
- Clear attachment state after sending
- Max file size: 100KB (show error chip if exceeded)
- Accept: `.txt`, `.md`, `.json`, `.py`, `.ts`, `.tsx`, `.js`, `.jsx`, `.css`, `.yml`, `.yaml`, `.toml`, `.csv` (text files only)

**Visual spec:**
- Icon button: paperclip or document icon (Unicode: 📎 U+1F4CE or 📄 U+1F4C4). Positioned left of the input area.
- Chip: `background: var(--sd-surface-alt)`, `border: 1px solid var(--sd-border)`, `border-radius: 12px`, `padding: 2px 8px`, `font-size: var(--sd-font-xs)`
- Chip "x" button: `color: var(--sd-text-muted)`, hover `color: var(--sd-red)`

**CRITICAL: `useTerminal.ts` is already at 668 lines.** Do NOT add attachment logic to it. Extract to a new hook.

**Implementation:**
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useAttachment.ts` — new hook:
  - State: `const [attachment, setAttachment] = useState<{ name: string; content: string } | null>(null)`
  - Function: `handleFileSelect(file: File)` — read file via FileReader, validate size (max 100KB) and type, set attachment state
  - Function: `removeAttachment()` — clear attachment state
  - Function: `formatPromptWithAttachment(text: string): string` — if attachment exists, prepend to prompt: `` ```{attachment.name}\n{attachment.content}\n```\n\n{text} ``, clear attachment after
  - Return `attachment`, `handleFileSelect`, `removeAttachment`, `formatPromptWithAttachment`
  - Accepted file types: `.txt`, `.md`, `.json`, `.py`, `.ts`, `.tsx`, `.js`, `.jsx`, `.css`, `.yml`, `.yaml`, `.toml`, `.csv`
- [ ] Modify `useTerminal.ts` (MINIMAL changes only):
  - Import `useAttachment` from `./useAttachment`
  - Call `const { attachment, handleFileSelect, removeAttachment, formatPromptWithAttachment } = useAttachment()`
  - In `handleSubmit()`: call `formatPromptWithAttachment(text)` to get final prompt text
  - Return `attachment`, `handleFileSelect`, `removeAttachment` in hook return value
  - **Total additions to useTerminal.ts: ~8 lines max**
- [ ] Modify `TerminalApp.tsx`:
  - Import `attachment`, `handleFileSelect`, `removeAttachment` from terminal hook
  - Pass to `TerminalPrompt` component
- [ ] Modify `TerminalPrompt.tsx` (or create new component if needed):
  - Add hidden `<input type="file" ref={fileInputRef} accept=".txt,.md,.json,.py,.ts,.tsx,.js,.jsx,.css,.yml,.yaml,.toml,.csv" />`
  - Add icon button to trigger file input click
  - Render attachment chip above textarea when attachment is set
  - Chip shows filename + "x" button that calls `removeAttachment()`
  - On file input change, validate file size (max 100KB), call `handleFileSelect(file)`
  - If file too large, show error chip instead
- [ ] Add CSS in `terminal.css`:
  - `.terminal-attachment-btn` — icon button styles
  - `.terminal-attachment-chip` — chip container styles
  - `.terminal-attachment-filename` — filename text
  - `.terminal-attachment-remove` — "x" button styles

## Test Requirements

Write tests FIRST (TDD).

### Feature 1: Typing Indicator Tests (5 minimum)
- [ ] Bus message `terminal:typing-start` emitted when LLM call begins
- [ ] Bus message `terminal:typing-end` emitted when LLM response completes
- [ ] Typing indicator appears in ChatView when typing state is true
- [ ] Typing indicator disappears when typing state is false
- [ ] Typing indicator does NOT appear when renderMode is not 'chat'

### Feature 4: Attachment Tests (6 minimum)
- [ ] File picker opens when icon button clicked
- [ ] Filename chip renders after file selection
- [ ] Chip removable via "x" button
- [ ] File content prepended to prompt when message sent
- [ ] Attachment state cleared after sending message
- [ ] Oversized file (>100KB) rejected with error message

**Total minimum: 11 new tests**

All existing tests must continue to pass:
- `browser/src/primitives/text-pane/services/__tests__/chatRenderer.test.ts` (13 tests)
- `browser/src/primitives/terminal/__tests__/useTerminal.test.ts` (existing tests)
- `browser/src/primitives/terminal/__tests__/TerminalOutput.test.tsx` (16 tests)

## Constraints
- **CSS:** `var(--sd-*)` only. No hex, no rgb(), no named colors.
- **No file over 500 lines.** If `sd-editor.css` exceeds 600 lines after adding typing styles, extract chat styles into `chat-bubbles.css` and import it.
- **TDD.** Tests first for all new features.
- **No stubs.** Every feature fully working.
- **No external dependencies.** Pure CSS animations for typing dots. `FileReader` API for attachment (built-in).
- **No images for icons.** Use Unicode characters (📎 or 📄) for attachment button.

## File Changes Expected
- `browser/src/primitives/terminal/useAttachment.ts` — NEW file, all attachment logic (state, file reading, validation, prompt formatting)
- `browser/src/primitives/terminal/useTerminal.ts` — import useAttachment, bus messages for typing indicator (~8 lines added, keep under 680)
- `browser/src/primitives/terminal/TerminalApp.tsx` — pass attachment props to TerminalPrompt
- `browser/src/primitives/terminal/TerminalPrompt.tsx` — file input, icon button, chip rendering
- `browser/src/primitives/terminal/terminal.css` — attachment button + chip styles
- `browser/src/primitives/terminal/types.ts` — add attachment type if needed
- `browser/src/primitives/text-pane/SDEditor.tsx` — subscribe to typing messages, pass to ChatView
- `browser/src/primitives/text-pane/services/chatRenderer.tsx` — render typing indicator
- `browser/src/primitives/text-pane/sd-editor.css` — typing bubble + dot animation styles
- Test files for both features

## Acceptance Criteria
- [ ] Typing indicator visible during LLM call in chat mode
- [ ] Typing indicator shows model name + "is thinking" + animated dots
- [ ] Three dots animate with staggered fade in/out (pure CSS)
- [ ] Indicator disappears immediately when response arrives
- [ ] File attachment button renders in terminal prompt area
- [ ] File picker opens on button click
- [ ] Filename chip displays after file selection
- [ ] Chip removable via "x" button
- [ ] File content prepended to LLM prompt as fenced code block
- [ ] Attachment cleared after sending message
- [ ] Oversized files (>100KB) rejected with error
- [ ] Only text file types accepted (.txt, .md, .json, etc.)
- [ ] All existing tests still pass
- [ ] 11+ new tests passing
- [ ] No file over 600 lines (split `sd-editor.css` if needed)
- [ ] Build passes: `cd browser && npx vitest run`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260313-TASK-043-RESPONSE.md`

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
