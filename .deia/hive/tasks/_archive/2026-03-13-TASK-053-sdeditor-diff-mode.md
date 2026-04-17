# TASK-053: SDEditor Diff Mode Implementation

## Objective
Implement diff view mode for SDEditor — displays unified diff format with side-by-side or inline view, read-only.

## Context
Diff mode shows changes between two versions of content. It uses unified diff format (like git diff output).

Requirements:
- Read-only (no editing)
- Accepts unified diff string as input
- Inline view: shows added lines in green, removed lines in red, context lines in default color
- Line numbers for both old and new versions
- Optional side-by-side view (future enhancement — inline is MVP)

This mode is used when terminal sends diff output or when comparing file versions.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\unifiedDiff.ts` (unified diff parser exists)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\sd-editor.css`

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\DiffView.tsx`
- [ ] DiffView component structure: parse unified diff, render with line numbers, color-code changes
- [ ] Parse diff hunks using existing unifiedDiff.ts helper
- [ ] Render added lines with `var(--sd-green)` background
- [ ] Render removed lines with `var(--sd-red)` background
- [ ] Render context lines with default background
- [ ] Show old/new line numbers in gutter (two columns)
- [ ] Read-only (no textarea)
- [ ] Update SDEditor.tsx to use DiffView when `mode === 'diff'`
- [ ] Add diff mode styles to sd-editor.css (prefix: `sde-diff-*`)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing tests pass
- [ ] 6+ new tests in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\__tests__\DiffView.test.tsx`:
  - DiffView renders unified diff
  - Added lines show in green
  - Removed lines show in red
  - Context lines show in default color
  - Line numbers show old and new positions
  - Empty diff shows "No changes" message

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- DiffView.tsx must be under 300 lines

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260313-TASK-053-RESPONSE.md`

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

## Model Assignment
sonnet

## Dependencies
- Depends on TASK-050 (mode refactor)

## Notes for Bee
- Use unifiedDiff.ts for parsing if possible — don't rewrite diff parser
- Focus on inline view — side-by-side can be a future enhancement
- Handle malformed diffs gracefully (show error message, don't crash)
