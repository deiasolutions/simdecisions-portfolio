# BL-065: SDEditor multi-mode verify and fix

## Objective
Verify and fix the SDEditor (text-pane) multi-mode system: raw, preview, diff, code, and process-intake modes all work correctly.

## Context
SDEditor supports multiple rendering modes configured per-pane. Each mode (raw text, markdown preview, diff view, code with syntax highlighting, process-intake conversational) should work based on the pane config. Some modes may be broken or incomplete.

## Files to Read First
- `browser/src/primitives/text-pane/`
- `browser/src/primitives/text-pane/SDEditor.tsx`
- `browser/src/primitives/text-pane/services/`
- `browser/src/primitives/text-pane/sd-editor.css`

## Deliverables
- [ ] Verify raw mode works (plain text editing)
- [ ] Verify preview mode works (markdown rendering)
- [ ] Verify code mode works (syntax highlighting)
- [ ] Fix any broken modes
- [ ] Tests for each mode rendering

## Acceptance Criteria
- [ ] Raw mode: editable plain text
- [ ] Preview mode: rendered markdown
- [ ] Code mode: syntax highlighted
- [ ] Mode switching works without losing content
- [ ] Tests pass

## Smoke Test
- [ ] `cd browser && npx vitest run --reporter=verbose src/primitives/text-pane/`
- [ ] `cd browser && npx vitest run`

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment
sonnet

## Priority
P0
