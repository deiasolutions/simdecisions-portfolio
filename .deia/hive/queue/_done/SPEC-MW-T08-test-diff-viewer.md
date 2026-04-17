# SPEC: TEST — Diff-Viewer Component Coverage

## Priority
P1

## Objective
Write comprehensive test suite for the DiffViewer component that validates unified diff parsing, layout modes, expand/collapse hunks, swipe actions, and syntax highlighting with 100% coverage.

## Context
This is a TDD task — write tests FIRST, before implementation exists. Tests must fail initially, then pass after MW-020/MW-021/MW-022 implementation.

Test coverage must include:
- Component render: diff displayed in stacked or side-by-side layout
- Diff parsing: unified diff text parsed into hunks with file paths, line numbers, changes
- Layout modes: stacked on mobile (<768px), side-by-side on tablet (≥768px)
- Expand/collapse: hunks collapsed by default (3 lines), expand button shows full hunk
- Swipe actions: swipe right → approve, swipe left → reject
- Syntax highlighting: code within diffs highlighted based on file extension
- Line numbers: before/after line numbers displayed
- Empty state: "No changes" if diffText is empty

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-S08-diff-viewer.md` — spec to test against
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/code-editor/__tests__/CodeEditor.test.tsx` — test patterns (if exists)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:76` — task context

## Acceptance Criteria
- [ ] Test file: `browser/src/primitives/diff-viewer/__tests__/DiffViewer.test.tsx` (Jest + React Testing Library)
- [ ] 10+ test cases covering: render, parsing, layouts, expand, swipe, highlighting, line numbers, empty
- [ ] Test render: diff displayed with 3 hunks
- [ ] Test parsing: unified diff text parsed correctly (file paths, hunks, line numbers)
- [ ] Test stacked layout: on mobile viewport (<768px) → stacked before/after blocks
- [ ] Test side-by-side layout: on tablet viewport (≥768px) → side-by-side columns
- [ ] Test collapse: hunk shows first 3 lines only, "Expand ↓" button visible
- [ ] Test expand: click "Expand ↓" → full hunk visible (all lines)
- [ ] Test swipe right: swipe gesture on hunk → checkmark appears, onApprove called
- [ ] Test swipe left: swipe gesture on hunk → X appears, onReject called
- [ ] Test syntax highlighting: code in JS file highlighted (keywords, strings)
- [ ] Test line numbers: before/after line numbers displayed for each change
- [ ] Test empty state: empty diffText → "No changes" message displayed
- [ ] Tests initially FAIL (no implementation exists yet)
- [ ] All tests use screen.getByRole, screen.getByText for queries
- [ ] No stubs in tests — real assertions with expected values

## Smoke Test
- [ ] Run `npm test DiffViewer.test.tsx` → 10+ tests FAIL (component doesn't exist yet)
- [ ] Check test_render() → asserts 3 hunks displayed
- [ ] Check test_parsing() → asserts file path extracted correctly
- [ ] Check test_expand() → asserts full hunk visible after expand click
- [ ] Check test_swipe_right() → asserts onApprove called
- [ ] All tests use descriptive names (it("should ..."))

## Model Assignment
sonnet

## Depends On
MW-S08

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/diff-viewer/__tests__/DiffViewer.test.tsx` (new file)
- TDD: tests MUST be written before implementation (they will fail initially)
- Max 300 lines for test file
- Use @testing-library/react for component testing
- Use fireEvent for swipe gesture simulation
- Mock window.matchMedia for viewport testing (mobile vs tablet)
- No implementation code in this task — tests only
- Tests must be runnable even if `DiffViewer.tsx` doesn't exist yet (import should handle missing module gracefully)
