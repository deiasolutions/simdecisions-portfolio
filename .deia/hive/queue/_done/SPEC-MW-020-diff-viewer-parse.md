# SPEC: Diff-Viewer Parsing + Layout

## Priority
P2

## Depends On
MW-T08, MW-V05

## Objective
Build the diff-viewer component that parses unified diff format, renders side-by-side or unified layout, and displays file changes with syntax highlighting (optional) for the Mobile Workdesk.

## Context
The diff-viewer is a destination from mobile-nav that shows file changes from bee responses or git diffs. It must:
- Parse unified diff format (git diff output)
- Render in unified layout (mobile default) or side-by-side layout (desktop/landscape)
- Show file headers (file paths), hunk headers (@@ -1,5 +1,7 @@)
- Color-code additions (green), deletions (red), context (gray)
- Optional: basic syntax highlighting (detect language from file extension)
- Support multiple files in one diff
- Responsive: unified on mobile (<768px), side-by-side on desktop (>=768px)

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/text-pane/TextPane.tsx` — existing text rendering patterns
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/terminal/TerminalApp.tsx` — ANSI color patterns (if applicable)
- Unified diff format specification (https://en.wikipedia.org/wiki/Diff#Unified_format)
- react-diff-view library (optional reference, but implement from scratch)

## Acceptance Criteria
- [ ] `DiffViewer` component with unified diff parsing
- [ ] Parse unified diff: file headers, hunk headers, line prefixes (+, -, space)
- [ ] Unified layout: single column, additions below deletions (mobile default)
- [ ] Side-by-side layout: two columns, additions on right, deletions on left (desktop)
- [ ] Color-code lines: additions (var(--sd-diff-add)), deletions (var(--sd-diff-del)), context (var(--sd-text-secondary))
- [ ] File headers: show file paths (a/file.ts → b/file.ts) with collapse/expand toggle
- [ ] Hunk headers: show line numbers (@@ -1,5 +1,7 @@) with context
- [ ] Multi-file support: render multiple files in one diff (scrollable list)
- [ ] Optional: syntax highlighting (use Prism.js or Highlight.js, lightweight)
- [ ] Responsive: switch layout based on viewport width (768px breakpoint)
- [ ] All CSS variables only (no hardcoded colors)
- [ ] 12+ unit tests (parsing, rendering, layout) + 3 E2E tests
- [ ] Accessible: semantic HTML (pre + code), ARIA labels for file headers

## Smoke Test
- [ ] Load diff with 3 files → all files render with headers
- [ ] Unified layout (mobile): additions/deletions in single column, color-coded
- [ ] Side-by-side layout (desktop): additions on right, deletions on left
- [ ] Tap file header → collapse/expand file diff
- [ ] Diff with 500 lines → smooth scrolling (60fps)

## Model Assignment
sonnet

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/diff-viewer/DiffViewer.tsx` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/diff-viewer/diff-viewer.css` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/diff-viewer/__tests__/DiffViewer.test.tsx`
- TDD: tests first
- Max 400 lines for component
- Max 150 lines for CSS
- Max 200 lines for tests
- Use React.memo for performance (virtualize if >500 lines)
- Syntax highlighting: optional (use Prism.js if available, graceful fallback)
- Diff parsing: use regex or line-by-line parsing (no external diff libs)
