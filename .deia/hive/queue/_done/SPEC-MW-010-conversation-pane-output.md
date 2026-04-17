# SPEC: Conversation-Pane Output Surfaces

## Priority
P1

## Depends On
MW-009

## Objective
Build output surfaces for conversation-pane: text output, code output with copy button, image rendering, file attachments, and action buttons for command execution results.

## Context
MW-008 built rendering, MW-009 added LLM routing. Now we add rich output surfaces:
- Code blocks with syntax highlighting and copy button
- Image rendering (inline, lightbox on tap)
- File attachments (download links)
- Action buttons (e.g., "Open file", "Run command")
- Command execution results (success, error, output)

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/conversation-pane/ConversationPane.tsx` — base component
- Look for existing code block or syntax highlighting components

## Acceptance Criteria
- [ ] `CodeBlock.tsx` component with syntax highlighting (Prism.js or similar)
- [ ] Code block has copy button (copies code to clipboard)
- [ ] Code block has language badge (e.g., "TypeScript", "Python")
- [ ] `ImageOutput.tsx` component for inline images
- [ ] Tap image → opens lightbox with full-size view
- [ ] `FileAttachment.tsx` component for downloadable files
- [ ] File shows: icon, filename, size, download button
- [ ] `ActionButton.tsx` component for command results
- [ ] Action button: "Open file" → triggers file open action
- [ ] Command result output: success (green check), error (red X), stdout/stderr
- [ ] All outputs mobile-optimized: touch-friendly, readable on small screens
- [ ] Component tests: 12+ tests covering all output types, interactions
- [ ] Integration test: render code → click copy → clipboard updated

## Smoke Test
- [ ] Render code block → syntax highlighting works, copy button present
- [ ] Click copy button → code copied to clipboard, button shows "Copied!"
- [ ] Render image → displays inline, tap → lightbox opens
- [ ] Render file attachment → download button works
- [ ] Render command result → success/error state shows correctly
- [ ] Run `npm test CodeBlock.test.tsx ImageOutput.test.tsx` — all tests pass

## Model Assignment
sonnet

## Constraints
- Location: `browser/src/primitives/conversation-pane/CodeBlock.tsx` (new file)
- Location: `browser/src/primitives/conversation-pane/ImageOutput.tsx` (new file)
- Location: `browser/src/primitives/conversation-pane/FileAttachment.tsx` (new file)
- Location: `browser/src/primitives/conversation-pane/ActionButton.tsx` (new file)
- Location: Tests for each component (4 new test files)
- TDD: Write tests first
- CSS variables only
- Max 250 lines per component
- Max 150 lines per test file
- NO STUBS — full implementation of all output types
- Use existing clipboard API for copy functionality
- Use existing syntax highlighter if available, otherwise add Prism.js
