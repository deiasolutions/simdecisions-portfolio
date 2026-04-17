# TASK-234: Empty States — Helpful Text in Empty Panes (W4 — 4.6)

## Objective
Empty panes should show helpful guidance text, not blank boxes. When a pane has no loaded applet, show a message explaining what the user can do.

## Context
Wave 4 Product Polish. `EmptyPane.tsx` already shows a centered FAB (+) button. But new users see a blank dark box with a small + button and have no idea what to do. Add contextual help text.

## Source Spec
`docs/specs/WAVE-4-PRODUCT-POLISH.md` — Task 4.6

## Files to Read First
- `browser/src/shell/components/EmptyPane.tsx` — Current empty pane implementation (~200 lines)
- `browser/src/shell/components/shell.css` — Shell layout styles

## Deliverables
- [ ] Add help text below the FAB button in EmptyPane:
  - Primary text: "Empty pane" (subtle, muted)
  - Secondary text: "Click + or right-click to add content" (smaller, dimmer)
  - Use `var(--sd-text-muted)` and `var(--sd-text-dimmer)` for colors
  - Text should not compete with the FAB — keep it understated
- [ ] When a pane has tabs but the active tab is empty, show the same help
- [ ] Ensure the help text is not shown when an applet is loading (defer to loading state)
- [ ] Add test: empty pane renders help text, FAB click opens menu
- [ ] Run: `cd browser && npx vitest run src/shell/`

## Priority
P1

## Model
haiku
