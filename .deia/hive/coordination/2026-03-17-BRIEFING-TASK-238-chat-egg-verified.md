# Briefing: TASK-238 — Chat EGG Verified (Wave 4 Product Polish)

**Date:** 2026-03-17
**From:** Q33NR
**To:** Q33N
**Model:** Haiku

---

## Objective

Verify the Chat EGG renders correctly as a 3-pane layout: chat history sidebar (left), chat output (center-top), terminal input (center-bottom). This is part of Wave 4 Product Polish (Task 4.10).

---

## Context

The chat.egg.md is one of three product faces for ShiftCenter. It must render with proper proportions and seamless borders. TASK-229 already verified chat bubbles render correctly (user right, AI left). This task focuses on verifying the overall EGG layout and integration.

---

## Source Spec

`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\WAVE-4-PRODUCT-POLISH.md` — Task 4.10

---

## Key Files to Reference

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\chat.egg.md` — Chat EGG layout definition (131 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggLoader.ts` — EGG parsing
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\text-pane\` — Text pane / chat renderer
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\` — Terminal input
- TASK-229 results (chat bubbles verified, 42 tests passing)

---

## Acceptance Criteria (from original task)

- [ ] Load `?egg=chat` in browser and verify:
  - Left sidebar (22%): chat-history tree-browser
  - Center top (70%): chat output text-pane with bubble rendering
  - Center bottom (30%): terminal with `routeTarget: "ai"`
  - Seamless border between chat output and terminal
- [ ] Verify chat bubbles render (user right, AI left) per TASK-229
- [ ] Verify terminal sends to AI provider and response appears in chat
- [ ] Verify 3-currency status bar shows (clock, coin, carbon)
- [ ] Fix any layout or rendering issues
- [ ] Run: `cd browser && npx vitest run`

---

## Instructions for Q33N

1. **Read the chat.egg.md file first** to understand the layout definition
2. **Create a task file** for a bee to:
   - Load `?egg=chat` in browser (manual verification step)
   - Verify the 3-pane layout renders correctly
   - Write automated tests for any rendering issues found
   - Document the verification results
3. **Assign model:** Haiku (this is verification work, not complex implementation)
4. **Return the task file to Q33NR for review BEFORE dispatching**

---

## Constraints

- No hardcoded colors (var(--sd-*) only)
- No file over 500 lines
- TDD for any fixes
- No stubs
- Full 8-section response file required

---

## Priority

P1 — Wave 4 Product Polish
