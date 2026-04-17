# SPEC: Diff-Viewer Expand/Collapse

## Priority
P2

## Depends On
MW-020

## Objective
Add expand/collapse functionality for file headers and hunk sections in the diff-viewer, with state persistence in localStorage and keyboard shortcuts.

## Context
Large diffs need collapsible sections:
- File-level collapse: tap file header → collapse/expand entire file diff
- Hunk-level collapse: tap hunk header → collapse/expand hunk (optional, lower priority)
- Collapsed state persisted in localStorage (per file path)
- Keyboard shortcuts: Ctrl+E (expand all), Ctrl+Shift+E (collapse all)
- Visual indicator: chevron icon (▶ collapsed, ▼ expanded)

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/diff-viewer/DiffViewer.tsx` — viewer from MW-020
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/tree-browser/TreeBrowser.tsx` — existing collapse patterns (if any)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/services/commands/commandRegistry.ts` — keyboard shortcut registration

## Acceptance Criteria
- [ ] File header is clickable button with chevron icon (▶/▼)
- [ ] Tap file header → toggle collapse/expand file diff
- [ ] Collapsed state: only file header visible, diff lines hidden
- [ ] Expanded state: file header + diff lines visible
- [ ] State persisted in localStorage: `sd:diff_viewer_collapsed` (JSON map of file paths)
- [ ] Keyboard shortcuts:
  - Ctrl+E: expand all files
  - Ctrl+Shift+E: collapse all files
- [ ] Animation: 200ms height transition (smooth collapse/expand)
- [ ] Optional: hunk-level collapse (tap hunk header @@ → collapse hunk)
- [ ] All CSS variables only (no hardcoded colors)
- [ ] 10+ unit tests (collapse, expand, persistence, shortcuts) + 2 E2E tests
- [ ] Accessible: file headers are buttons, aria-expanded attribute

## Smoke Test
- [ ] Load diff with 5 files → all files expanded by default
- [ ] Tap file header → file collapses (chevron changes to ▶)
- [ ] Tap collapsed file header → file expands (chevron changes to ▼)
- [ ] Keyboard: Ctrl+E → all files expand
- [ ] Keyboard: Ctrl+Shift+E → all files collapse
- [ ] Reload page → collapsed state persisted (collapsed files remain collapsed)

## Model Assignment
sonnet

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/diff-viewer/DiffViewer.tsx` (modify)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/diff-viewer/__tests__/DiffViewer.test.tsx` (modify)
- No new files
- TDD: tests first
- Max 150 lines of changes to DiffViewer.tsx
- Max 50 lines of CSS changes
- localStorage key: `sd:diff_viewer_collapsed`
- Chevron icon: CSS-only (▶ and ▼ Unicode characters, not SVG)
- Animation: use CSS height transition (not max-height for performance)
