# SPEC: Chat Pane Polish — Typing Indicator, Avatars, Grouping, Attachments

## Priority
P0

## Objective
Add four polish features to the chat experience: typing indicator, sender avatars, message grouping, and attachment button.

## Context
Two components across two directories:

### text-pane (browser/src/primitives/text-pane/)
1. **Typing indicator**: Show "Claude is thinking..." with animated dots (CSS animation) while waiting for LLM response. Disappears when response arrives. Wire to the terminal's `isLoading` or `isStreaming` state via bus message.
2. **Sender avatars**: CSS circles — robot icon (unicode or SVG) left of AI bubbles, person icon right of user bubbles. 32px diameter. `var(--sd-*)` colors only. No images.
3. **Message grouping**: Consecutive messages from same sender share one header. Subsequent bubbles indent without repeating name/avatar. Determined by checking `sender` field of adjacent messages.

### terminal (browser/src/primitives/terminal/)
4. **Attachment button**: File picker icon in input area. When clicked, opens native file dialog. Selected file's content included as context in next LLM message. Filename shown as chip/tag above input with X to remove.

Files to read first:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\markdownRenderer.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalOutput.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalInput.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts`

## Acceptance Criteria
- [ ] Typing indicator appears when LLM is processing, disappears on response
- [ ] Animated CSS dots (not a GIF, not an image)
- [ ] Sender avatars: 32px circles, robot left of AI, person right of user
- [ ] Avatars use var(--sd-*) CSS variables only
- [ ] Consecutive same-sender messages grouped under one header
- [ ] Attachment button in terminal input area
- [ ] File picker opens on click, reads file content
- [ ] Filename chip shown above input with remove button
- [ ] File content included in next LLM message context
- [ ] 15+ tests across all four features
- [ ] No file over 500 lines

## Model Assignment
sonnet

## Constraints
- Do NOT modify envelope routing or LLM adapter code
- CSS animations only (no JS animation libraries)
- No external image assets — use unicode or inline SVG for icons
- Each feature can be a separate sub-component file
