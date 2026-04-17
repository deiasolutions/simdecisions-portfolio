# SPEC: Diff-Viewer Mobile Component

## Priority
P1

## Objective
Design a mobile-optimized diff viewer component that parses unified diffs, renders side-by-side or stacked layout, supports expand/collapse hunks, and enables swipe actions for approve/reject.

## Context
The diff-viewer is used in:
- Conversation-pane output (when LLM suggests code changes)
- Queue-pane spec details (showing file changes from bee commits)
- Terminal output (git diff rendering)

It must support:
- Unified diff parsing (parse `diff --git`, `@@` hunks)
- Mobile layout: stacked (before/after) or side-by-side (tablet)
- Expand/collapse hunks (show first 3 lines, expand to full)
- Swipe actions: swipe right → approve diff, swipe left → reject
- Syntax highlighting for code within diffs

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/code-editor/CodeEditor.tsx` — syntax highlighting patterns
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/text-pane/TextPane.tsx` — text rendering
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:64` — task context

## Acceptance Criteria
- [ ] `DiffViewer` component accepts `{ diffText: string, layout: "stacked" | "side-by-side" }`
- [ ] Unified diff parser: extract file paths, hunks, line numbers, +/- changes
- [ ] Stacked layout: before block (red bg), after block (green bg), side-by-side on tablet (>768px)
- [ ] Expand/collapse hunks: show first 3 lines by default, "Expand ↓" button to show full hunk
- [ ] Syntax highlighting: detect language from file extension, apply prism.js or similar
- [ ] Swipe actions: swipe hunk right → green checkmark (approve), left → red X (reject)
- [ ] Line numbers: display line numbers for before/after
- [ ] Empty state: "No changes" if diffText is empty
- [ ] Accessibility: ARIA labels for hunks, keyboard navigation (arrow keys to expand)
- [ ] 10+ unit tests + 2 E2E tests (parse diff, expand hunk, swipe action)

## Smoke Test
- [ ] Render diff viewer with unified diff (3 hunks, 20 lines changed)
- [ ] Stacked layout renders on mobile (<768px), side-by-side on tablet
- [ ] First hunk shows 3 lines, tap "Expand" → full hunk visible
- [ ] Swipe hunk right → checkmark appears, approve event fired
- [ ] Swipe hunk left → X appears, reject event fired
- [ ] Syntax highlighting applied to code (JS/TS files)

## Model Assignment
sonnet

## Depends On
None (Phase 0 spec)

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/diff-viewer/DiffViewer.tsx` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/diff-viewer/diff-viewer.css` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/diff-viewer/__tests__/DiffViewer.test.tsx`
- TDD: tests first
- Max 450 lines for component
- Max 150 lines for CSS
- Max 200 lines for tests
- CSS variables only, no hardcoded colors
- No external diff libs — custom parser using regex
- No stubs — full diff parsing + swipe gesture handling
