# BRIEFING: TASK-234 — Empty States (Helpful Text in Empty Panes)

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-17
**Priority:** P1
**Model:** Haiku

---

## Objective

Add helpful guidance text to empty panes so new users understand what to do when they see a blank pane with just a FAB (+) button.

---

## Context

This is Wave 4 Product Polish (Task 4.6 from `docs/specs/WAVE-4-PRODUCT-POLISH.md`).

Currently, `EmptyPane.tsx` shows a centered FAB (+) button, but new users see a blank dark box with a small + button and have no idea what to do. We need to add contextual help text that explains the user can click + or right-click to add content.

---

## Source Spec

`docs/specs/WAVE-4-PRODUCT-POLISH.md` — Task 4.6

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\EmptyPane.tsx` — Current empty pane implementation (~200 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\shell.css` — Shell layout styles

---

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

---

## Constraints

- Rule 3: NO HARDCODED COLORS. Only CSS variables (`var(--sd-*)`).
- Rule 4: No file over 500 lines. Modularize at 500.
- Rule 5: TDD. Tests first, then implementation.
- Rule 6: NO STUBS. Every function fully implemented.

---

## Your Task

1. Read the two files listed above
2. Write a single task file for this work (it's bee-sized — one file, one test file)
3. Return the task file to me for review
4. Wait for my approval before dispatching the bee
