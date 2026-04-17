# SPEC: SDEditor Multi-Mode (raw/preview/diff/code/process-intake)

## Priority
P0

## Objective
Add mode switching to the SDEditor text-pane primitive. The editor currently only renders markdown. It needs five modes selectable via a `mode` prop and a toolbar toggle.

## Context
SDEditor lives at `browser/src/primitives/text-pane/SDEditor.tsx`. It was ported in TASK-010 as a basic markdown editor with co-author overlay. The multi-mode capability was designed in the "Building in-pane apps" conversation (March 2026) but never made it into a task file.

This blocks code.egg.md (the IDE product) which needs raw text editing and code mode with syntax highlighting.

Files to read first:
- `browser/src/primitives/text-pane/SDEditor.tsx` — current editor
- `browser/src/primitives/text-pane/types.ts` — current types
- `browser/src/primitives/text-pane/sd-editor.css` — current styles

## Acceptance Criteria
- [ ] `mode` prop on SDEditor: `document` | `raw` | `code` | `diff` | `process-intake`
- [ ] Toolbar toggle button to switch between modes at runtime
- [ ] **Document mode** (default, current behavior): markdown rendered, co-author overlay works
- [ ] **Raw mode**: plain text editing, no markdown rendering, monospace font, line numbers
- [ ] **Code mode**: syntax highlighting via Prism.js or highlight.js (import from CDN — check what's available in the project). Language selector dropdown (Python, JavaScript, TypeScript, JSON, YAML, Markdown, HTML, CSS). Line numbers. Monospace font.
- [ ] **Diff mode**: side-by-side or inline diff view. Shows changes between two versions of content. Read-only. Uses unified diff format.
- [ ] **Process-intake mode**: same as document mode but the co-author sends content to `to_ir` instead of `to_text`. For future use — just set the routing flag, don't build IR generation.
- [ ] All modes use `var(--sd-*)` CSS variables only
- [ ] No mode exceeds 500 lines — split into sub-components per mode if needed (DocumentView.tsx, RawView.tsx, CodeView.tsx, DiffView.tsx)
- [ ] Existing document mode tests still pass
- [ ] 15+ new tests across all modes

## Smoke Test
- [ ] Load chat.egg.md — text-pane renders in document mode (default, unchanged)
- [ ] Toggle to raw mode — content appears as plain text with line numbers
- [ ] Toggle to code mode — syntax highlighting appears, language selector works
- [ ] Toggle back to document — markdown renders again

## Model Assignment
sonnet

## Constraints
- Do NOT remove or break existing document mode functionality
- Do NOT add heavy dependencies — use CDN imports for syntax highlighting if needed
- Each mode is a separate sub-component file, not one giant switch statement
