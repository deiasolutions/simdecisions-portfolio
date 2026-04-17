# TASK-051: SDEditor Raw Mode Implementation

## Objective
Implement the raw text editing mode for SDEditor — plain text editing with monospace font and line numbers, no markdown rendering.

## Context
TASK-050 refactored the mode system. Now we need to implement the visual rendering for `raw` mode.

Raw mode requirements:
- Plain text editing (no markdown rendering)
- Monospace font (`var(--sd-font-mono)`)
- Line numbers in left gutter (like code mode)
- No syntax highlighting
- Editable (unlike code mode which may be read-only in future)

This is the simplest mode — just a textarea with line numbers.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\SDEditor.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\codeRenderer.tsx` (reference for line number rendering)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\sd-editor.css`

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\RawView.tsx`
- [ ] RawView component structure: left gutter (line numbers), right textarea (editable)
- [ ] Sync scroll between gutter and textarea
- [ ] Line numbers update dynamically as content changes
- [ ] Update SDEditor.tsx to use RawView when `mode === 'raw'`
- [ ] Add raw mode styles to sd-editor.css (prefix: `sde-raw-*`)
- [ ] All styles use `var(--sd-*)` only

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All existing tests pass
- [ ] 5+ new tests in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\services\__tests__\RawView.test.tsx`:
  - RawView renders with content
  - Line numbers match line count
  - Line numbers update when content changes
  - Textarea is editable
  - Scroll syncs between gutter and textarea

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- RawView.tsx must be under 200 lines

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia\hive\responses\20260313-TASK-051-RESPONSE.md`

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
haiku

## Dependencies
- Depends on TASK-050 (mode refactor)
