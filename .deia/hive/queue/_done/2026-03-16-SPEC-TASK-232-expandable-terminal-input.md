# TASK-232: Expandable Terminal Input (W4 — 4.4)

## Objective
Verify the expandable terminal input works correctly — textarea grows as user types, expands upward when content exceeds 3 lines, and collapses back when content is cleared.

## Context
Wave 4 Product Polish (BL-003). TerminalPrompt.tsx already has auto-resize (min 22px, max 200px) and expand-up mode that triggers at >3 lines. CSS support exists in terminal.css with absolute positioning, max-height 50vh, and box shadow. This task verifies everything works smoothly.

## Source Spec
`docs/specs/WAVE-4-PRODUCT-POLISH.md` — Task 4.4

## Files to Read First
- `browser/src/primitives/terminal/TerminalPrompt.tsx` — Auto-resize logic (lines 59-88)
- `browser/src/primitives/terminal/terminal.css` — Expand-up CSS (lines 268-278)

## Deliverables
- [ ] Verify textarea grows vertically as user types multiple lines
- [ ] Verify expand-up mode triggers at >3 lines (input lifts above prompt area)
- [ ] Verify expand-up has proper shadow (`--sd-shadow-lg`) to separate from content
- [ ] Verify collapsing back to normal when content is cleared or submitted
- [ ] Verify Shift+Enter creates newlines, Enter submits
- [ ] Verify scrollbar appears when content exceeds max-height (50vh)
- [ ] Fix any visual issues (jumpy resize, clipped text, focus loss)
- [ ] Add test: expand triggers at correct line count, collapses on clear
- [ ] Run: `cd browser && npx vitest run src/primitives/terminal/`

## Priority
P1

## Model
haiku
